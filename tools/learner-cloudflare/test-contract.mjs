/*
 * Offline, dependency-free boundary tests. These do not substitute for
 * end-to-end sign-in, D1, CSRF, provider, and cross-device acceptance tests.
 */
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import worker, { safeReturnPath } from "./worker.js";

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

test("email typing is uninterrupted until explicit human verification", () => {
  // Turnstile's asynchronous iframe rendering must not begin merely because
  // a visitor opens the email form or returns to edit their address.
  assert.match(accountScript, /beginVerification\.addEventListener\("click"/);
  assert.match(accountScript, /form\.reportValidity\(\)/);
  assert.match(accountScript, /widget\.hidden = true/);
  assert.match(accountScript, /clearVerification\(\)/);
  assert.doesNotMatch(accountScript, /box\.addEventListener\("toggle"/);
  assert.doesNotMatch(accountScript, /email\.focus\(\);\s*prepareWidget\(\)/);
});

test("signed-in light and dark themes override the device setting", () => {
  const css = readFileSync(
    new URL("../../web/assets/css/site.css", import.meta.url), "utf8"
  );
  assert.match(accountScript, /document\.documentElement\.dataset\.theme = theme/);
  assert.match(css, /html\[data-theme="light"\]\s*\{[^}]*color-scheme:\s*light;/);
  assert.match(css, /html\[data-theme="dark"\]\s*\{[^}]*color-scheme:\s*dark;/);
  assert.match(css, /html\[data-theme="light"\]\s*\{[^}]*--background:/);
  assert.match(css, /html\[data-theme="dark"\]\s*\{[^}]*--background:/);
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


test("canonical 19-module allowlist has exactly 57 valid lesson positions", () => {
  const server = readFileSync(new URL("./worker.js", import.meta.url), "utf8");
  const counts = /const LESSON_COUNTS = \[([\s\S]*?)\];/.exec(server);
  assert.ok(counts);
  const lengths = [...counts[1].matchAll(/\d+/g)].map(item => Number(item[0]));
  assert.equal(lengths.length, 19);
  assert.equal(lengths.reduce((a, b) => a + b, 0), 57);
  assert.equal(lengths[3], 2);
  assert.equal(lengths[5], 3); // Current Module 6 = attention.
  assert.equal(lengths[6], 4);
  assert.equal(lengths[18], 2);
  assert.match(server, /const match = \/\^m\(\[1-9\]\|1\[0-9\]\)/);
});

test("progress UI uses the single current 19-module course", () => {
  assert.match(courseScript, /\[1, 2\]\.includes\(manifest\.version\)/);
  assert.match(courseScript, /manifest\.earlierModules\.length/);
  assert.match(courseScript, /identity\.size !== manifest\.eligibleLessonCount/);
  assert.match(courseScript, /current && current\.progressEligible/);
  assert.match(courseScript, /!lesson\.progressEligible \|\| !known\.has\(lesson\.id\)/);
  assert.doesNotMatch(courseScript, /Earlier-edition reading/);
  assert.doesNotMatch(courseScript, /archivedResume/);
});

test("sign-in returns to current course pages but rejects retired v2 paths", () => {
  for (const path of ["/", "/course/", "/course/m1/", "/course/m4/2/",
    "/course/m6/1/", "/course/m19/2/"]) {
    assert.equal(safeReturnPath(path), path);
  }
  for (const path of ["https://evil.example", "//evil.example",
    "/course/../admin", "/course/m20/", "/course/m23/1/",
    "/course/v2/m6/1/", "/course/m6/0/", "/course/m6/1//",
    "/course/m6/1/?redirect=evil", "/account"]) {
    assert.equal(safeReturnPath(path), "/course/");
  }
  assert.ok(!accountScript.includes(String.raw`v2\/m(?:6|7|8|9|10)`));
});
