/*
 * FND Education learner API — independent from aggregate analytics.
 *
 * Deployment is BLOCKED until a dedicated D1 database, an HTTPS accounts
 * subdomain, OIDC provider credentials, domain/CORS review, and the security
 * checklist in README.md are configured. No passwords are handled here.
 *
 * Each request identifies the learner by an HttpOnly random bearer cookie;
 * neither a browser-supplied learner_id nor username authorizes any action.
 * State changes require the exact trusted Origin and an account-bound CSRF
 * header. Server data never joins the anonymous statistics database.
 */
"use strict";
import { emailEnabled, startEmail, finishEmail } from "./email-auth.js";

const DAY = 86400;
const SESSION_LIFE = 180 * DAY; // Sliding safety cap, not inactivity logout.
const RETAIN_INACTIVE_YEARS = 3; // Long-term abandoned account cleanup only.
const FLOW_LIFE = 600;
const SESSION_COOKIE = "__Host-fnd_learner_session";
const FLOW_COOKIE = "__Host-fnd_oauth_flow";

const PROVIDERS = {
  google: {
    authorization: "https://accounts.google.com/o/oauth2/v2/auth",
    token: "https://oauth2.googleapis.com/token",
    keys: "https://www.googleapis.com/oauth2/v3/certs",
    issuer: ["https://accounts.google.com", "accounts.google.com"]
  },
  apple: {
    authorization: "https://appleid.apple.com/auth/authorize",
    token: "https://appleid.apple.com/auth/token",
    keys: "https://appleid.apple.com/auth/keys",
    issuer: ["https://appleid.apple.com"]
  }
};

function now() { return Math.floor(Date.now() / 1000); }
function inactivityCutoff() {
  // Calendar years, not a fixed 365-day approximation.
  const cutoff = new Date();
  cutoff.setUTCFullYear(cutoff.getUTCFullYear() - RETAIN_INACTIVE_YEARS);
  return Math.floor(cutoff.getTime() / 1000);
}
function randomToken(bytes = 32) {
  const raw = new Uint8Array(bytes);
  crypto.getRandomValues(raw);
  return b64url(raw);
}
function b64url(bytes) {
  let text = "";
  for (const byte of bytes) text += String.fromCharCode(byte);
  return btoa(text).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}
function bytesFromB64url(value) {
  if (!/^[A-Za-z0-9_-]+$/.test(value)) throw new Error("Invalid token");
  const raw = atob(value.replace(/-/g, "+").replace(/_/g, "/"));
  return Uint8Array.from(raw, c => c.charCodeAt(0));
}
async function sha(value) {
  return [...new Uint8Array(await crypto.subtle.digest(
    "SHA-256", new TextEncoder().encode(value)
  ))].map(n => n.toString(16).padStart(2, "0")).join("");
}
function cookie(req, name) {
  const match = (req.headers.get("Cookie") || "").match(
    new RegExp("(?:^|;\\s*)" + name + "=([^;]+)")
  );
  return match ? match[1] : null;
}
function sessionCookie(token, maxAge = SESSION_LIFE) {
  return SESSION_COOKIE + "=" + token +
    "; Path=/; Max-Age=" + maxAge +
    "; Secure; HttpOnly; SameSite=Lax";
}
function flowCookie(value, maxAge = FLOW_LIFE) {
  // Apple's cross-site form_post callback requires SameSite=None.
  return FLOW_COOKIE + "=" + value +
    "; Path=/; Max-Age=" + maxAge +
    "; Secure; HttpOnly; SameSite=None";
}
function policyHeaders() {
  return {
    "Cache-Control": "no-store",
    "Referrer-Policy": "no-referrer",
    "X-Content-Type-Options": "nosniff",
    "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'"
  };
}
function cors(req, env) {
  const origin = req.headers.get("Origin");
  if (origin !== env.PUBLIC_ORIGIN) return {};
  return {
    "Access-Control-Allow-Origin": env.PUBLIC_ORIGIN,
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Allow-Headers": "Content-Type, X-FND-CSRF",
    "Access-Control-Allow-Methods": "GET, POST, PATCH, DELETE, OPTIONS",
    "Vary": "Origin"
  };
}
function reply(req, env, body, status = 200, extra = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      ...policyHeaders(), ...cors(req, env),
      "Content-Type": "application/json; charset=utf-8", ...extra
    }
  });
}
function redirect(location, cookies = []) {
  const headers = new Headers({ ...policyHeaders(), Location: location });
  for (const value of cookies) headers.append("Set-Cookie", value);
  return new Response(null, { status: 303, headers });
}
function err(req, env, status, message) {
  return reply(req, env, { error: message }, status);
}
function safeReturnPath(raw) {
  if (typeof raw !== "string" || raw.length > 200 ||
      raw.includes("\\") || raw.includes("//") ||
      !/^\/(?:$|course\/(?:m[0-9]+\/(?:[0-9]+\/)?)?$)/.test(raw)) {
    return "/course/";
  }
  return raw;
}
// Original course identities are immutable, even after the concepts-first
// publication rearranges reading order. Module 4 has TWO original lessons.
// The new /course/v2/m6..m10/ teaching uses reserved source slots 24..28
// and is deliberately NOT authorized for learner progress here. Changes to
// this allowlist require a separately reviewed client/manifest/API contract.
const LESSON_COUNTS = [
  4, 2, 3, 2, 3, 4, 5, 4, 4, 3, 5, 3,
  3, 3, 3, 3, 4, 3, 3, 3, 3, 3, 2
];
function validLesson(id) {
  const match = /^m([1-9]|1[0-9]|2[0-3])-([1-9][0-9]?)$/.exec(id || "");
  if (!match) return false;
  return Number(match[2]) <= LESSON_COUNTS[Number(match[1]) - 1];
}
async function jsonInput(req) {
  if (!(req.headers.get("Content-Type") || "").startsWith("application/json") ||
      Number(req.headers.get("Content-Length") || 0) > 4096) {
    throw new Error("Expected a small JSON request");
  }
  const reader = req.body?.getReader();
  if (!reader) throw new Error("Missing body");
  const chunks = [];
  let size = 0;
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    size += value.byteLength;
    if (size > 4096) { await reader.cancel(); throw new Error("Request too large"); }
    chunks.push(value);
  }
  const raw = new Uint8Array(size);
  let offset = 0;
  for (const chunk of chunks) { raw.set(chunk, offset); offset += chunk.byteLength; }
  const input = new TextDecoder().decode(raw);
  const parsed = JSON.parse(input);
  if (!parsed || Array.isArray(parsed) || typeof parsed !== "object") {
    throw new Error("Invalid JSON object");
  }
  return parsed;
}
function providerEnabled(env, provider) {
  // Apple is deferred. A placeholder must never publish a broken button.
  return provider === "google" && !!env.GOOGLE_CLIENT_SECRET &&
    typeof env.GOOGLE_CLIENT_ID === "string" &&
    env.GOOGLE_CLIENT_ID.endsWith(".apps.googleusercontent.com");
}
function clientId(env, provider) {
  return provider === "google" ? env.GOOGLE_CLIENT_ID :
    provider === "apple" ? env.APPLE_CLIENT_ID : null;
}
function clientSecret(env, provider) {
  return provider === "google" ? env.GOOGLE_CLIENT_SECRET :
    provider === "apple" ? env.APPLE_CLIENT_SECRET : null;
}
function callbackUrl(env, provider) {
  return env.API_ORIGIN + "/v1/auth/callback/" + provider;
}
function validSetup(env) {
  try {
    const publicUrl = new URL(env.PUBLIC_ORIGIN);
    const apiUrl = new URL(env.API_ORIGIN);
    return publicUrl.protocol === "https:" &&
      apiUrl.protocol === "https:" &&
      publicUrl.origin === "https://fndeducationproject.org" &&
      apiUrl.origin === "https://accounts.fndeducationproject.org" &&
      !!env.DB;
  } catch { return false; }
}

async function beginLogin(req, env, provider) {
  if (!providerEnabled(env, provider)) {
    return err(req, env, 404, "Sign-in provider not configured");
  }
  const url = new URL(req.url);
  const state = randomToken();
  const nonce = randomToken();
  const verifier = randomToken(48);
  const challenge = b64url(new Uint8Array(await crypto.subtle.digest(
    "SHA-256", new TextEncoder().encode(verifier)
  )));
  const returnPath = safeReturnPath(url.searchParams.get("return") || "/course/");
  await env.DB.prepare(
    "INSERT INTO oauth_flows (state_hash, provider, pkce_verifier, nonce, return_path, expires_at) VALUES (?, ?, ?, ?, ?, ?)"
  ).bind(await sha(state), provider, verifier, nonce, returnPath, now() + FLOW_LIFE).run();

  const target = new URL(PROVIDERS[provider].authorization);
  target.searchParams.set("client_id", clientId(env, provider));
  target.searchParams.set("redirect_uri", callbackUrl(env, provider));
  target.searchParams.set("response_type", "code");
  target.searchParams.set("scope", "openid");
  target.searchParams.set("state", state);
  target.searchParams.set("nonce", nonce);
  target.searchParams.set("code_challenge", challenge);
  target.searchParams.set("code_challenge_method", "S256");
  // On shared devices, Google must offer a deliberate account choice.
  if (provider === "google") target.searchParams.set("prompt", "select_account");
  if (provider === "apple") target.searchParams.set("response_mode", "form_post");
  return redirect(target.toString(), [flowCookie(state)]);
}
async function verifiedIdToken(jwt, provider, expectedNonce, env) {
  const sections = jwt.split(".");
  if (sections.length !== 3 || jwt.length > 12000) throw new Error("Bad ID token");
  const header = JSON.parse(new TextDecoder().decode(bytesFromB64url(sections[0])));
  const claims = JSON.parse(new TextDecoder().decode(bytesFromB64url(sections[1])));
  if (header.alg !== "RS256" || typeof header.kid !== "string") {
    throw new Error("Unsupported ID token signing algorithm");
  }
  const jwksResponse = await fetch(PROVIDERS[provider].keys, { cf: { cacheTtl: 300 } });
  if (!jwksResponse.ok) throw new Error("Provider key lookup failed");
  const jwks = await jwksResponse.json();
  const jwk = jwks.keys.find(k =>
    k.kid === header.kid && k.kty === "RSA" &&
    (!k.use || k.use === "sig") && (!k.alg || k.alg === "RS256")
  );
  if (!jwk) throw new Error("Unrecognized signing key");
  const key = await crypto.subtle.importKey(
    "jwk", jwk, { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" },
    false, ["verify"]
  );
  const signatureOk = await crypto.subtle.verify(
    "RSASSA-PKCS1-v1_5", key, bytesFromB64url(sections[2]),
    new TextEncoder().encode(sections[0] + "." + sections[1])
  );
  const t = now();
  const aud = claims.aud;
  if (!signatureOk ||
      !PROVIDERS[provider].issuer.includes(claims.iss) ||
      !(aud === clientId(env, provider) ||
        (Array.isArray(aud) && aud.includes(clientId(env, provider)) &&
         claims.azp === clientId(env, provider))) ||
      claims.nonce !== expectedNonce ||
      typeof claims.sub !== "string" || claims.sub.length < 1 ||
      !Number.isInteger(claims.iat) || claims.iat > t + 60 ||
      !Number.isInteger(claims.exp) || claims.exp < t - 60) {
    throw new Error("ID token validation failed");
  }
  return claims.sub;
}
async function callback(req, env, provider) {
  if (!providerEnabled(env, provider)) return err(req, env, 404, "Unknown provider");
  let code, state;
  if (provider === "apple" && req.method === "POST") {
    const raw = await req.text();
    if (raw.length > 8192) return err(req, env, 400, "Invalid callback");
    const params = new URLSearchParams(raw);
    code = params.get("code");
    state = params.get("state");
  } else if (provider === "google" && req.method === "GET") {
    const params = new URL(req.url).searchParams;
    code = params.get("code");
    state = params.get("state");
  } else {
    return err(req, env, 405, "Invalid callback method");
  }
  const originalFlow = cookie(req, FLOW_COOKIE);
  if (!code || code.length > 4000 || !state ||
      state !== originalFlow || state.length > 200) {
    return err(req, env, 400, "Sign-in verification failed");
  }
  const stateHash = await sha(state);
  // Atomically consume a flow. A callback is never usable twice.
  const flow = await env.DB.prepare(
    "DELETE FROM oauth_flows WHERE state_hash = ? AND provider = ? AND expires_at >= ? RETURNING *"
  ).bind(stateHash, provider, now()).first();
  if (!flow) return err(req, env, 400, "Expired sign-in. Please try again.");

  const exchange = await fetch(PROVIDERS[provider].token, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "authorization_code",
      code,
      redirect_uri: callbackUrl(env, provider),
      client_id: clientId(env, provider),
      client_secret: clientSecret(env, provider),
      code_verifier: flow.pkce_verifier
    }),
    redirect: "error"
  });
  if (!exchange.ok) return err(req, env, 400, "Provider verification failed");
  const tokens = await exchange.json();
  if (typeof tokens.id_token !== "string") {
    return err(req, env, 400, "Provider ID token missing");
  }
  const subject = await verifiedIdToken(tokens.id_token, provider, flow.nonce, env);

  let identity = await env.DB.prepare(
    "SELECT learner_id FROM identities WHERE provider = ? AND subject = ?"
  ).bind(provider, subject).first();
  if (!identity) {
    const id = crypto.randomUUID();
    const name = "Learner " + randomToken(5).slice(0, 6).toUpperCase();
    await env.DB.batch([
      env.DB.prepare(
        "INSERT INTO learners (id, username, created_at, last_seen_at) SELECT ?, ?, ?, ? " +
        "WHERE NOT EXISTS (SELECT 1 FROM identities WHERE provider = ? AND subject = ?)"
      ).bind(id, name, now(), now(), provider, subject),
      env.DB.prepare(
        "INSERT INTO identities (provider, subject, learner_id) SELECT ?, ?, id FROM learners WHERE id = ?"
      ).bind(provider, subject, id)
    ]);
    identity = await env.DB.prepare(
      "SELECT learner_id FROM identities WHERE provider = ? AND subject = ?"
    ).bind(provider, subject).first();
  }

  const session = await createSession(env, identity.learner_id);
  return redirect(env.PUBLIC_ORIGIN + flow.return_path,
    [flowCookie("", 0), sessionCookie(session)]);
}
/** All authentication methods issue the same opaque, revocable session. */
async function createSession(env, learnerId) {
  const session = randomToken();
  await env.DB.prepare(
    "INSERT INTO learner_sessions (token_hash, learner_id, csrf_token, expires_at, last_active, created_at) VALUES (?, ?, ?, ?, ?, ?)"
  ).bind(await sha(session), learnerId, randomToken(),
    now() + SESSION_LIFE, now(), now()).run();
  return session;
}

async function authorize(req, env) {
  const token = cookie(req, SESSION_COOKIE);
  if (!token || token.length > 200) return null;
  const hash = await sha(token);
  const account = await env.DB.prepare(
    "SELECT s.*, l.username, l.theme, l.idle_minutes, l.last_lesson FROM learner_sessions s " +
    "JOIN learners l ON l.id = s.learner_id " +
    "WHERE s.token_hash = ? AND s.expires_at > ?"
  ).bind(hash, now()).first();
  if (!account) return null;
  if (account.idle_minutes > 0 &&
      now() - account.last_active > account.idle_minutes * 60) {
    await env.DB.prepare("DELETE FROM learner_sessions WHERE token_hash = ?")
      .bind(hash).run();
    return null;
  }
  // Track authenticated account activity; not the public browsing history.
  // The retained timestamp prevents deletion of people actively using the
  // course. Write it only once per day to avoid unnecessary D1 writes.
  await env.DB.batch([
    env.DB.prepare(
      "UPDATE learner_sessions SET last_active = ? WHERE token_hash = ? AND last_active < ?"
    ).bind(now(), hash, account.idle_minutes > 0 ? now() : now() - DAY),
    env.DB.prepare(
      "UPDATE learners SET last_seen_at = ? WHERE id = ? AND last_seen_at < ?"
    ).bind(now(), account.learner_id, now() - DAY)
  ]);
  account.session_token = token;
  return account;
}
function csrfValid(req, account, env) {
  return req.headers.get("Origin") === env.PUBLIC_ORIGIN &&
    req.headers.get("X-FND-CSRF") === account.csrf_token;
}
async function progress(req, env, account) {
  const rows = await env.DB.prepare(
    "SELECT lesson_id, visited, completed FROM learner_progress WHERE learner_id = ?"
  ).bind(account.learner_id).all();
  return reply(req, env, {
    lessons: Object.fromEntries(rows.results.map(row => [
      row.lesson_id, {
        visited: row.visited === 1,
        completed: row.completed === 1
      }
    ])),
    lastLesson: account.last_lesson
  });
}
async function visit(req, env, account, input) {
  if (!validLesson(input.lessonId)) {
    return err(req, env, 400, "Unknown lesson identifier");
  }
  await env.DB.batch([
    env.DB.prepare(
      "INSERT INTO learner_progress (learner_id, lesson_id, visited, completed, updated_at) " +
      "VALUES (?, ?, 1, 0, ?) ON CONFLICT(learner_id, lesson_id) " +
      "DO UPDATE SET visited = 1, updated_at = excluded.updated_at"
    ).bind(account.learner_id, input.lessonId, now()),
    env.DB.prepare("UPDATE learners SET last_lesson = ? WHERE id = ?")
      .bind(input.lessonId, account.learner_id)
  ]);
  return reply(req, env, { ok: true });
}
async function completion(req, env, account, input) {
  if (!validLesson(input.lessonId) || typeof input.completed !== "boolean" ||
      input.confirmed !== true ||
      typeof input.confirmedUsername !== "string" ||
      input.confirmedUsername !== account.username) {
    return err(req, env, 400, "Completion requires account confirmation");
  }
  await env.DB.prepare(
    "INSERT INTO learner_progress (learner_id, lesson_id, visited, completed, updated_at) " +
    "VALUES (?, ?, 0, ?, ?) ON CONFLICT(learner_id, lesson_id) DO UPDATE SET " +
    "completed = excluded.completed, updated_at = excluded.updated_at"
  ).bind(account.learner_id, input.lessonId, input.completed ? 1 : 0, now()).run();
  return reply(req, env, { ok: true });
}
function cleanUsername(name) {
  if (typeof name !== "string") return null;
  const trimmed = name.trim();
  if (trimmed.length < 2 || trimmed.length > 40 ||
      /[\u0000-\u001f\u007f-\u009f\u202a-\u202e\u2066-\u2069<>]/.test(trimmed)) {
    return null;
  }
  return trimmed;
}
async function updateSettings(req, env, account, input) {
  const username = Object.hasOwn(input, "username") ?
    cleanUsername(input.username) : account.username;
  const theme = Object.hasOwn(input, "theme") ? input.theme : account.theme;
  const idle = Object.hasOwn(input, "idleMinutes") ?
    input.idleMinutes : account.idle_minutes;
  if (!username || !["system", "light", "dark"].includes(theme) ||
      ![0, 15, 60, 1440, 10080].includes(idle)) {
    return err(req, env, 400, "Invalid account preferences");
  }
  await env.DB.batch([
    env.DB.prepare(
      "UPDATE learners SET username = ?, theme = ?, idle_minutes = ? WHERE id = ?"
    ).bind(username, theme, idle, account.learner_id),
    // Turning on an idle limit must start from this authenticated interaction,
    // not the throttled activity timestamp of a previously persistent session.
    env.DB.prepare("UPDATE learner_sessions SET last_active = ? WHERE token_hash = ?")
      .bind(now(), account.token_hash)
  ]);
  return reply(req, env, { username, theme, idleMinutes: idle });
}
async function exportAccount(req, env, account) {
  const rows = await env.DB.prepare(
    "SELECT lesson_id, visited, completed, updated_at FROM learner_progress " +
    "WHERE learner_id = ?"
  ).bind(account.learner_id).all();
  const email = await env.DB.prepare("SELECT email FROM learner_emails WHERE learner_id = ?")
    .bind(account.learner_id).first();
  return reply(req, env, {
    email: email?.email || null,
    username: account.username, theme: account.theme,
    idleMinutes: account.idle_minutes, lastLesson: account.last_lesson,
    lessons: rows.results
  }, 200, {
    "Content-Disposition": "attachment; filename=\"fnd-course-progress.json\""
  });
}
async function handle(req, env) {
  if (!validSetup(env)) return new Response("Not configured", { status: 503 });
  const u = new URL(req.url);
  if (u.origin !== env.API_ORIGIN) return new Response("Not found", { status: 404 });
  if (req.method === "OPTIONS") {
    if (req.headers.get("Origin") !== env.PUBLIC_ORIGIN) {
      return new Response(null, { status: 403 });
    }
    return new Response(null, { status: 204, headers: cors(req, env) });
  }

  if (req.method === "GET" && u.pathname === "/v1/auth/options") {
    return reply(req, env, {
      google: providerEnabled(env, "google"), email: emailEnabled(env),
      turnstileSiteKey: emailEnabled(env) ? env.TURNSTILE_SITE_KEY : null
    });
  }
  // Unauthenticated email endpoints require exact Origin and JSON. Combined
  // with browser-bound challenges, this prevents cross-site login CSRF.
  if (["/v1/auth/email/start", "/v1/auth/email/verify"].includes(u.pathname)) {
    if (req.method !== "POST" || req.headers.get("Origin") !== env.PUBLIC_ORIGIN) {
      return err(req, env, 403, "Use the sign-in form on the website.");
    }
    let input;
    try { input = await jsonInput(req); }
    catch { return err(req, env, 400, "Invalid request"); }
    return u.pathname.endsWith("/start")
      ? startEmail(req, env, input, emailHelpers)
      : finishEmail(req, env, input, emailHelpers);
  }

  const start = /^\/v1\/auth\/start\/(google|apple)$/.exec(u.pathname);
  if (start && req.method === "GET") return beginLogin(req, env, start[1]);
  const finish = /^\/v1\/auth\/callback\/(google|apple)$/.exec(u.pathname);
  if (finish) return callback(req, env, finish[1]);

  // No unauthenticated endpoint can read or write learner progress.
  const account = await authorize(req, env);
  if (!account) return err(req, env, 401, "Sign in to save course progress");

  if (req.method === "GET" && u.pathname === "/v1/me") {
    const response = reply(req, env, {
      username: account.username, theme: account.theme,
      idleMinutes: account.idle_minutes, csrfToken: account.csrf_token
    });
    // Default has no idle timeout, while credentials have a rolling
    // 180-day server cap to limit leaked-cookie damage.
    if (account.expires_at < now() + 90 * DAY) {
      await env.DB.prepare(
        "UPDATE learner_sessions SET expires_at = ? WHERE token_hash = ?"
      ).bind(now() + SESSION_LIFE, account.token_hash).run();
      response.headers.append("Set-Cookie",
        sessionCookie(account.session_token));
    }
    return response;
  }
  if (req.method === "GET" && u.pathname === "/v1/progress") {
    return progress(req, env, account);
  }
  if (req.method === "GET" && u.pathname === "/v1/export") {
    return exportAccount(req, env, account);
  }
  if (!["POST", "PATCH", "DELETE"].includes(req.method) ||
      !csrfValid(req, account, env)) {
    return err(req, env, 403, "Account confirmation required");
  }
  if (req.method === "POST" && u.pathname === "/v1/logout") {
    await env.DB.prepare("DELETE FROM learner_sessions WHERE token_hash = ?")
      .bind(account.token_hash).run();
    return reply(req, env, { ok: true }, 200, {
      "Set-Cookie": sessionCookie("", 0)
    });
  }

  let input;
  try { input = await jsonInput(req); }
  catch { return err(req, env, 400, "Invalid request"); }

  if (req.method === "POST" && u.pathname === "/v1/account/email/start") {
    return startEmail(req, env, input, emailHelpers, account);
  }
  if (req.method === "POST" && u.pathname === "/v1/account/email/verify") {
    return finishEmail(req, env, input, emailHelpers, account);
  }

  if (req.method === "POST" && u.pathname === "/v1/progress/visit") {
    return visit(req, env, account, input);
  }
  if (req.method === "POST" && u.pathname === "/v1/progress/completion") {
    return completion(req, env, account, input);
  }
  if (req.method === "POST" && u.pathname === "/v1/progress/reset") {
    if (input.confirmed !== true ||
        input.confirmedUsername !== account.username) {
      return err(req, env, 400, "Account confirmation required");
    }
    await env.DB.batch([
      env.DB.prepare("DELETE FROM learner_progress WHERE learner_id = ?")
        .bind(account.learner_id),
      env.DB.prepare("UPDATE learners SET last_lesson = NULL WHERE id = ?")
        .bind(account.learner_id)
    ]);
    return reply(req, env, { ok: true });
  }
  if (req.method === "PATCH" && u.pathname === "/v1/settings") {
    return updateSettings(req, env, account, input);
  }
  if (req.method === "DELETE" && u.pathname === "/v1/account") {
    if (input.confirmedUsername !== account.username ||
        input.confirmed !== true) {
      return err(req, env, 400, "Account deletion requires confirmation");
    }
    await env.DB.batch([
      // Cancel pending login codes for this email before deleting ownership.
      env.DB.prepare("DELETE FROM email_challenges WHERE email IN (SELECT email FROM learner_emails WHERE learner_id = ?)")
        .bind(account.learner_id),
      env.DB.prepare("DELETE FROM learners WHERE id = ?").bind(account.learner_id)
    ]); // Cascades progress, sessions, provider identities and verified email.
    return reply(req, env, { ok: true }, 200, {
      "Set-Cookie": sessionCookie("", 0)
    });
  }
  return err(req, env, 404, "Not found");
}
const emailHelpers = { now, randomToken, sha, cookie, cleanUsername,
  reply, err, sessionCookie, createSession };

export default {
  async scheduled(_event, env, ctx) {
    // Bounded database cleanup; do not record or log learner identities.
    ctx.waitUntil((async () => {
      // Clean sessions first. A learner deletion removes all linked
      // identities, session records, and lesson progress via CASCADE.
      // Keep deletion batches small to respect Workers Free plan limits.
      await env.DB.batch([
        env.DB.prepare("DELETE FROM oauth_flows WHERE expires_at < ?")
          .bind(now()),
        env.DB.prepare("DELETE FROM learner_sessions WHERE expires_at < ?")
          .bind(now()),
        env.DB.prepare("DELETE FROM email_challenges WHERE expires_at < ?").bind(now()),
        env.DB.prepare("DELETE FROM email_limits WHERE expires_at < ?").bind(now())
      ]);
      await env.DB.prepare(
        "DELETE FROM learners WHERE id IN (" +
          "SELECT l.id FROM learners l " +
          "WHERE l.last_seen_at < ? AND NOT EXISTS (" +
            "SELECT 1 FROM learner_sessions s " +
            "WHERE s.learner_id = l.id AND s.expires_at > ?" +
          ") ORDER BY l.last_seen_at ASC LIMIT 100" +
        ")"
      ).bind(inactivityCutoff(), now()).run();
    })());
  },
  async fetch(req, env) {
    try {
      return await handle(req, env);
    } catch {
      // Never log OAuth codes, signed tokens, sessions, or medical interest.
      return err(req, env, 500, "Service temporarily unavailable");
    }
  }
};
