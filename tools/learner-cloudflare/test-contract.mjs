/*
 * Offline, dependency-free boundary tests. These do not substitute for
 * end-to-end sign-in, D1, CSRF, provider, and cross-device acceptance tests.
 */
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import worker from "./worker.js";

const site = "https://fndeducationproject.org";
const api = "https://accounts.fndeducationproject.org";
const env = {
  PUBLIC_ORIGIN: site,
  API_ORIGIN: api,
  DB: {}
};
const courseScript = readFileSync(
  new URL("../../web/assets/js/course-progress.js", import.meta.url), "utf8"
);
const accountScript = readFileSync(
  new URL("../../web/assets/js/account-shell.js", import.meta.url), "utf8"
);

test("guest progress requests never succeed without authentication", async () => {
  const result = await worker.fetch(
    new Request(api + "/v1/progress", { headers: { Origin: site } }), env
  );
  assert.equal(result.status, 401);
  assert.match(await result.text(), /Sign in/);
});

test("untrusted origins cannot complete preflight", async () => {
  const bad = await worker.fetch(new Request(api + "/v1/progress", {
    method: "OPTIONS",
    headers: { Origin: "https://evil.example" }
  }), env);
  assert.equal(bad.status, 403);
  const good = await worker.fetch(new Request(api + "/v1/progress", {
    method: "OPTIONS",
    headers: { Origin: site }
  }), env);
  assert.equal(good.status, 204);
  assert.equal(good.headers.get("Access-Control-Allow-Origin"), site);
  assert.equal(good.headers.get("Access-Control-Allow-Credentials"), "true");
});

test("login cannot start without configured provider credentials", async () => {
  const result = await worker.fetch(new Request(
    api + "/v1/auth/start/google"
  ), env);
  assert.equal(result.status, 404);
});

test("account client never uses browser-local progress storage", () => {
  // A storage API mentioned in a documentation comment is not an API call.
  // Test executable code, retaining detection of calls or property access.
  const executableClient = (courseScript + accountScript)
    .replace(/\/\*[\s\S]*?\*\//g, "")
    .replace(/^\s*\/\/[^\n]*$/gm, "");
  assert.doesNotMatch(executableClient,
    /(?:window\.)?(?:localStorage|sessionStorage|indexedDB)\s*[.[(]/);
  assert.match(courseScript, /dlg\.showModal\(\)/);
  assert.match(courseScript, /confirmedUsername: account\.username/);
  assert.match(courseScript, /confirm.*lesson progress/i);
  assert.match(accountScript, /idleMinutes/);
  assert.match(accountScript, /applyTheme/);
});

test("course reading remains accessible without account API", () => {
  assert.match(courseScript, /if \(!window\.FNDAccount\) return/);
});

test("server requires verified ownership and account CSRF", () => {
  const server = readFileSync(new URL("./worker.js", import.meta.url), "utf8");
  assert.match(server, /csrfValid\(req, account, env\)/);
  assert.match(server, /account\.learner_id/);
  assert.match(server, /confirmedUsername !== account\.username/);
  assert.match(server, /HttpOnly; SameSite=Lax/);
});


test("account deletion is present, confirmed, and cascades learner records", () => {
  const server = readFileSync(new URL("./worker.js", import.meta.url), "utf8");
  const schema = readFileSync(new URL("./schema.sql", import.meta.url), "utf8");
  assert.match(accountScript, /Delete my learner account/);
  assert.match(accountScript, /type your username exactly/);
  assert.match(server, /DELETE FROM learners WHERE id = \?/);
  assert.match(server, /input\.confirmedUsername !== account\.username/);
  for (const name of ["identities", "learner_progress", "learner_sessions"]) {
    assert.match(schema,
      new RegExp("CREATE TABLE IF NOT EXISTS " + name + "[\\s\\S]*?" +
        "REFERENCES learners\\(id\\) ON DELETE CASCADE"));
  }
});

test("inactive learner maintenance preserves recent accounts and sessions", async () => {
  const operations = [];
  let background;
  const db = {
    prepare(sql) {
      return {
        bind(...values) {
          const op = { sql, values };
          operations.push(op);
          return {
            ...op,
            async run() { return { success: true }; }
          };
        }
      };
    },
    async batch(statements) {
      assert.equal(statements.length, 4);
      return statements.map(() => ({ success: true }));
    }
  };
  worker.scheduled(null, { DB: db }, {
    waitUntil(promise) { background = promise; }
  });
  await background;
  assert.equal(operations.length, 5);
  assert.match(operations[0].sql, /DELETE FROM oauth_flows/);
  assert.match(operations[1].sql, /DELETE FROM learner_sessions/);
  assert.match(operations[4].sql, /DELETE FROM learners/);
  assert.match(operations[4].sql, /last_seen_at < \?/);
  assert.match(operations[4].sql, /NOT EXISTS/);
  assert.match(operations[4].sql, /s\.expires_at > \?/);
  assert.match(operations[4].sql, /LIMIT 100/);
  const yearsAgo = new Date();
  yearsAgo.setUTCFullYear(yearsAgo.getUTCFullYear() - 3);
  assert.ok(Math.abs(operations[4].values[0] -
    Math.floor(yearsAgo.getTime() / 1000)) < 10);
});

test("inactivity and sign-out rules are distinct and explained", () => {
  const schema = readFileSync(new URL("./schema.sql", import.meta.url), "utf8");
  assert.match(schema, /idle_minutes INTEGER NOT NULL DEFAULT 0/);
  assert.match(schema, /last_seen_at INTEGER NOT NULL/);
  assert.match(accountScript, /unused for three years/);
  assert.match(accountScript, /Automatic sign-out/);
});
