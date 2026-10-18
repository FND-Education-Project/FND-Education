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
  assert.doesNotMatch(courseScript + accountScript,
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
