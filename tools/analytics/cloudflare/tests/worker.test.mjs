import assert from "node:assert/strict";
import test from "node:test";
import worker from "../src/worker.mjs";
import { adminPage, adminScript } from "../src/admin-dashboard.mjs";
import { webcrypto } from "node:crypto";

const API = "https://example-account.workers.dev/v1/event";
const SITE = "https://fndeducationproject.org";

function env() {
  const statements = [];
  return {
    statements,
    DB: {
      prepare(sql) {
        assert.match(sql, /ON CONFLICT\(day, event, section\)/);
        return {
          bind(...args) {
            return {
              async run() {
                statements.push(args);
                return { success: true };
              }
            };
          }
        };
      }
    }
  };
}

function post(body, origin = SITE, type = "text/plain;charset=UTF-8") {
  return new Request(API, {
    method: "POST", headers: { "Origin": origin, "Content-Type": type },
    body: JSON.stringify(body)
  });
}

test("valid anonymous counters add only day, event, section", async () => {
  const storage = env();
  const result = await worker.fetch(post({ event: "search_used", section: "search" }), storage);
  assert.equal(result.status, 204);
  assert.equal(result.headers.get("Access-Control-Allow-Origin"), SITE);
  assert.equal(storage.statements.length, 1);
  assert.match(storage.statements[0][0], /^\d{4}-\d{2}-\d{2}$/);
  assert.deepEqual(storage.statements[0].slice(1), ["search_used", "search"]);
});

test("unknown origin is refused", async () => {
  const storage = env();
  assert.equal((await worker.fetch(post({ event: "page_view", section: "home" }, "https://attacker.example"), storage)).status, 403);
  assert.equal(storage.statements.length, 0);
});

test("search terms and extra fields are rejected, never recorded", async () => {
  const storage = env();
  assert.equal((await worker.fetch(post({ event: "search_used", section: "search", query: "seizures" }), storage)).status, 400);
  assert.equal(storage.statements.length, 0);
});

test("reject unknown event, unrecognized section and oversized input", async () => {
  const storage = env();
  assert.equal((await worker.fetch(post({ event: "login", section: "home" }), storage)).status, 400);
  assert.equal((await worker.fetch(post({ event: "page_view", section: "/private/path" }), storage)).status, 400);
  assert.equal((await worker.fetch(post({ event: "search_used", section: "search", padding: "x".repeat(400) }), storage)).status, 413);
  assert.equal(storage.statements.length, 0);
});

test("no public access to aggregate counts; health only", async () => {
  const storage = env();
  assert.equal((await worker.fetch(new Request(API.replace("/v1/event", "/admin")), storage)).status, 404);
  assert.equal((await worker.fetch(new Request(API.replace("/v1/event", "/health")), storage)).status, 200);
});

test("missing DB binding and DB errors return no private information", async () => {
  assert.equal((await worker.fetch(post({ event: "page_view", section: "other" }), {})).status, 503);
  const failing = { DB: { prepare() { return { bind() { return { run() { throw new Error("private DB connection"); } }; } }; } } };
  const result = await worker.fetch(post({ event: "page_view", section: "other" }), failing);
  assert.equal(result.status, 503);
  assert.equal(await result.text(), "");
});


test("administrator dashboard and data API are disabled until all access settings exist", async () => {
  const storage = env();
  const paths = ["/admin", "/admin/", "/admin/app.js", "/admin/api/summary"];
  for (const path of paths) {
    assert.equal((await worker.fetch(new Request(API.replace("/v1/event", path)), storage)).status, 404);
  }
  assert.equal((await worker.fetch(new Request(API.replace("/v1/event", "/admin")),
    { ...storage, ACCESS_TEAM_DOMAIN: "team.cloudflareaccess.com" })).status, 404);
});

test("private resources deny unsigned and forged credentials, even when configured", async () => {
  const configured = { ...env(), ACCESS_TEAM_DOMAIN: "fnd-test.cloudflareaccess.com",
    ACCESS_APP_AUD: "a".repeat(64), ADMIN_ALLOWED_EMAIL: "owner@example.org" };
  for (const path of ["/admin", "/admin/app.js", "/admin/api/summary?days=30"]) {
    const req = new Request(API.replace("/v1/event", path),
      { headers: { "Cf-Access-Jwt-Assertion": "not-a-signed-token" } });
    assert.equal((await worker.fetch(req, configured)).status, 403);
  }
  const attack = new Request(API.replace("/v1/event", "/admin"),
    { headers: { Cookie: "CF_Authorization=not-a-signed-token" } });
  assert.equal((await worker.fetch(attack, configured)).status, 403);
});

test("signed Access JWT, audience and admin allowlist gate read-only daily counts", async () => {
  const pair = await webcrypto.subtle.generateKey(
    { name: "RSASSA-PKCS1-v1_5", modulusLength: 2048,
      publicExponent: new Uint8Array([1, 0, 1]), hash: "SHA-256" },
    true, ["sign", "verify"]);
  const jwk = { ...await webcrypto.subtle.exportKey("jwk", pair.publicKey),
    kid: "private-test-key", alg: "RS256", use: "sig" };
  const host = "fnd-test.cloudflareaccess.com", aud = "a".repeat(64);
  const now = Math.floor(Date.now() / 1000);
  const encode = value => Buffer.from(JSON.stringify(value)).toString("base64url");
  const prefix = encode({ alg: "RS256", kid: jwk.kid }) + "." +
    encode({ iss: "https://" + host, aud: [aud], exp: now + 120,
      nbf: now - 10, sub: "access-subject", email: "owner@example.org" });
  const signature = await webcrypto.subtle.sign("RSASSA-PKCS1-v1_5",
    pair.privateKey, Buffer.from(prefix));
  const token = prefix + "." + Buffer.from(signature).toString("base64url");
  const originalFetch = globalThis.fetch;
  let jwksCalls = 0;
  globalThis.fetch = async url => {
    assert.equal(url, "https://" + host + "/cdn-cgi/access/certs");
    jwksCalls++;
    return new Response(JSON.stringify({ keys: [jwk] }), { status: 200 });
  };
  const rows = [{ day: new Date().toISOString().slice(0, 10), event: "page_view",
    section: "home", total: 4 }];
  const storage = { ACCESS_TEAM_DOMAIN: host, ACCESS_APP_AUD: aud,
    ADMIN_ALLOWED_EMAIL: "owner@example.org",
    DB: { prepare(sql) {
      assert.match(sql, /SELECT day, event, section, total FROM daily_counts/);
      return { bind() { return { async all() { return { results: rows }; } }; } };
    } } };
  try {
    const page = await worker.fetch(new Request(API.replace("/v1/event", "/admin"),
      { headers: { "Cf-Access-Jwt-Assertion": token } }), storage);
    assert.equal(page.status, 200);
    assert.match(await page.text(), /Website statistics/);
    assert.match(page.headers.get("Content-Security-Policy"), /script-src 'self'/);
    assert.equal(page.headers.get("Access-Control-Allow-Origin"), null);
    const app = await worker.fetch(new Request(API.replace("/v1/event", "/admin/app.js"),
      { headers: { Cookie: "CF_Authorization=" + token } }), storage);
    assert.equal(app.status, 200);
    assert.match(await app.text(), /Daily page activity|Daily breakdown|page_view/);
    const api = await worker.fetch(new Request(
      API.replace("/v1/event", "/admin/api/summary?days=7"),
      { headers: { "Cf-Access-Jwt-Assertion": token } }), storage);
    assert.equal(api.status, 200);
    const result = await api.json();
    assert.equal(result.days, 7);
    assert.deepEqual(result.rows, rows);
    assert.equal(jwksCalls, 1);
    const impostor = { ...storage, ADMIN_ALLOWED_EMAIL: "another@example.org" };
    assert.equal((await worker.fetch(new Request(API.replace("/v1/event", "/admin"),
      { headers: { "Cf-Access-Jwt-Assertion": token } }), impostor)).status, 403);
    const malformed = await worker.fetch(new Request(
      API.replace("/v1/event", "/admin/api/summary?days=100"),
      { headers: { "Cf-Access-Jwt-Assertion": token } }), storage);
    assert.equal(malformed.status, 400);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("private dashboard scripts parse and contain no browser-side third-party analytics", () => {
  assert.match(adminPage, /<script src="\/admin\/app.js"/);
  assert.doesNotThrow(() => new Function(adminScript));
  assert.doesNotMatch(adminPage + adminScript, /google-analytics\.com|unpkg\.com/);
});


test("AWStats-style dashboard draws five dated graphs from anonymous daily counts", async () => {
  class FakeElement {
    constructor(tag) {
      this.tag = tag;
      this.children = [];
      this.textContent = "";
      this.hidden = false;
      this.value = "";
      this.attrs = {};
      this.listeners = {};
    }
    replaceChildren(...nodes) { this.children = [...nodes]; }
    append(...nodes) { this.children.push(...nodes); }
    setAttribute(key, value) { this.attrs[key] = String(value); }
    addEventListener(event, callback) { this.listeners[event] = callback; }
  }
  const nodes = new Map();
  const getNode = id => {
    if (!nodes.has(id)) nodes.set(id, new FakeElement(id));
    return nodes.get(id);
  };
  const document = {
    getElementById: getNode,
    createElement: tag => new FakeElement(tag),
    createElementNS: (_ns, tag) => new FakeElement(tag)
  };
  getNode("period").value = "30";
  const today = "2026-10-17";
  const data = {
    days: 30, today, rows: [
      { day: today, event: "page_view", section: "course", total: 12 },
      { day: today, event: "search_used", section: "search", total: 5 },
      { day: today, event: "search_result_click", section: "search", total: 3 },
      { day: today, event: "pdf_download", section: "reference", total: 2 },
      { day: today, event: "puzzle_download", section: "puzzles", total: 1 },
      { day: today, event: "not_found", section: "other", total: 1 },
      { day: "2026-10-16", event: "page_view", section: "home", total: 6 }
    ]
  };
  const queried = [];
  const fetch = async url => {
    queried.push(url);
    const days = Number(new URL(url, "https://worker.example").searchParams.get("days"));
    return new Response(JSON.stringify({ ...data, days }), { status: 200 });
  };
  new Function("document", "fetch", adminScript)(document, fetch);
  await new Promise(resolve => setImmediate(resolve));
  assert.equal(getNode("k-pages").textContent, "18");
  assert.equal(getNode("k-search").textContent, "5");
  assert.equal(getNode("k-clicks").textContent, "3");
  assert.equal(getNode("k-downloads").textContent, "3");
  assert.equal(getNode("k-missing").textContent, "1");
  const plots = ["views-chart", "search-chart", "clicks-chart",
    "download-chart", "errors-chart"];
  for (const name of plots) {
    assert.ok(getNode(name).children.length > 4, name + " has chart content");
  }
  assert.equal(getNode("search-chart").children.filter(n => n.tag === "polyline").length, 2);
  assert.equal(getNode("clicks-chart").children.filter(n => n.tag === "polyline").length, 3);
  assert.ok(getNode("views-chart").children.some(n => n.tag === "rect"));
  assert.ok(getNode("download-chart").children.some(n => n.tag === "rect"));
  assert.equal(getNode("history-body").children.length, 30);
  assert.match(getNode("updated").textContent, /2026-10-17 \(UTC\)/);
  assert.equal(getNode("error").hidden, true);
  getNode("period").value = "7";
  await getNode("period").listeners.change();
  await new Promise(resolve => setImmediate(resolve));
  assert.ok(queried.some(url => url.endsWith("days=7")));
  assert.equal(getNode("history-body").children.length, 7);
});
