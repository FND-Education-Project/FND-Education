import assert from "node:assert/strict";
import test from "node:test";
import worker from "../src/worker.mjs";

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

test("public event Worker cannot expose dashboard even with administrator secrets", async () => {
  const storage = { ...env(), ACCESS_TEAM_DOMAIN: "test.cloudflareaccess.com",
    ACCESS_APP_AUD: "a".repeat(64), ADMIN_ALLOWED_EMAIL: "owner@example.org" };
  for (const path of ["/admin", "/admin/", "/admin/app.js", "/admin/api/summary"]) {
    const result = await worker.fetch(new Request(API.replace("/v1/event", path)), storage);
    assert.equal(result.status, 404);
  }
  assert.equal(storage.statements.length, 0);
});
