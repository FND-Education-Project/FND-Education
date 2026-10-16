import { adminPage, adminScript } from "./admin-dashboard.mjs";

/**
 * First-party, anonymous COUNTS ONLY for the FND Education Project.
 *
 * The application never requests or stores IPs, cookies, referrers, user
 * agents, identifiers, URLs, search terms, individual activity or timestamps.
 * Network/platform operators may separately process connection metadata.
 *
 * Never log the request or its body; unexpected fields are rejected.
 * Database access is private to this Worker. A separate read-only dashboard
 * fails closed unless signed Cloudflare Access identity and an explicit
 * GitHub-only admin allowlist are configured.
 */
const SITE_ORIGIN = "https://fndeducationproject.org";
const EVENT_TYPES = new Set([
  "page_view", "search_used", "search_result_click", "pdf_download",
  "puzzle_download", "not_found"
]);
const SECTIONS = new Set([
  "home", "course", "reference", "glossary", "puzzles",
  "booklets", "search", "contact", "other"
]);

function response(status, origin = "", body = "") {
  const headers = new Headers({
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff"
  });
  if (origin === SITE_ORIGIN) {
    headers.set("Access-Control-Allow-Origin", SITE_ORIGIN);
    headers.set("Vary", "Origin");
  }
  if (body) headers.set("Content-Type", "text/plain; charset=utf-8");
  return new Response(body || null, { status, headers });
}

async function readLimitedBody(request, maxBytes) {
  // Enforce input limits even if a client omits or lies about Content-Length.
  if (!request.body) return "";
  const reader = request.body.getReader();
  const decoder = new TextDecoder();
  let result = "";
  let size = 0;
  try {
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      size += value.byteLength;
      if (size > maxBytes) {
        await reader.cancel();
        return null;
      }
      result += decoder.decode(value, { stream: true });
    }
    return result + decoder.decode();
  } finally {
    reader.releaseLock();
  }
}


// GitHub-only administrator access must be enforced by a Cloudflare Access
// application policy. Worker also verifies the Access JWT cryptographically
// and checks its explicitly allowlisted admin email; neither check alone is
// intended to replace the other. No custom password or user database.
let certCache = { host: "", expires: 0, keys: [] };

function adminConfigured(env) {
  const host = String(env.ACCESS_TEAM_DOMAIN || "");
  return /^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?\.cloudflareaccess\.com$/i.test(host) &&
    /^[a-f0-9]{32,128}$/i.test(String(env.ACCESS_APP_AUD || "")) &&
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(env.ADMIN_ALLOWED_EMAIL || ""));
}

function decodePart(segment) {
  if (!/^[A-Za-z0-9_-]+$/.test(segment)) throw new Error("Malformed JWT");
  const padded = segment.replace(/-/g, "+").replace(/_/g, "/")
    .padEnd(Math.ceil(segment.length / 4) * 4, "=");
  const text = atob(padded);
  return Uint8Array.from(text, c => c.charCodeAt(0));
}

function accessToken(request) {
  const header = request.headers.get("Cf-Access-Jwt-Assertion");
  if (header) return header;
  const cookie = request.headers.get("Cookie") || "";
  const match = cookie.match(/(?:^|;\s*)CF_Authorization=([^;\s]+)/);
  return match ? match[1] : "";
}

async function validAdmin(request, env) {
  if (!adminConfigured(env)) return false;
  const token = accessToken(request);
  if (token.length < 50 || token.length > 8192) return false;
  try {
    const parts = token.split(".");
    if (parts.length !== 3) return false;
    const header = JSON.parse(new TextDecoder().decode(decodePart(parts[0])));
    const claims = JSON.parse(new TextDecoder().decode(decodePart(parts[1])));
    if (header.alg !== "RS256" || typeof header.kid !== "string") return false;
    const now = Math.floor(Date.now() / 1000);
    const aud = claims.aud;
    if (claims.iss !== "https://" + env.ACCESS_TEAM_DOMAIN ||
        !(Array.isArray(aud) ? aud.includes(env.ACCESS_APP_AUD) :
          aud === env.ACCESS_APP_AUD) ||
        typeof claims.sub !== "string" || !claims.sub ||
        !Number.isFinite(claims.exp) || claims.exp <= now ||
        (claims.nbf !== undefined && claims.nbf > now) ||
        (claims.iat !== undefined && claims.iat > now + 60) ||
        typeof claims.email !== "string" ||
        claims.email.toLowerCase() !== env.ADMIN_ALLOWED_EMAIL.toLowerCase()) {
      return false;
    }
    let keys = certCache.keys;
    if (certCache.host !== env.ACCESS_TEAM_DOMAIN ||
        certCache.expires < Date.now() ||
        !keys.some(k => k.kid === header.kid)) {
      const resp = await fetch("https://" + env.ACCESS_TEAM_DOMAIN +
        "/cdn-cgi/access/certs", { redirect: "error" });
      if (!resp.ok) return false;
      const document = await resp.json();
      if (!Array.isArray(document.keys) || document.keys.length > 20) return false;
      keys = document.keys;
      certCache = { host: env.ACCESS_TEAM_DOMAIN,
        expires: Date.now() + 15 * 60 * 1000, keys };
    }
    const jwk = keys.find(k => k.kid === header.kid && k.kty === "RSA" &&
      k.alg === "RS256" && k.use === "sig");
    if (!jwk) return false;
    const key = await crypto.subtle.importKey(
      "jwk", jwk, { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" },
      false, ["verify"]
    );
    return crypto.subtle.verify("RSASSA-PKCS1-v1_5", key,
      decodePart(parts[2]), new TextEncoder().encode(parts[0] + "." + parts[1]));
  } catch {
    // No token contents, network errors, or credentials are written to logs.
    return false;
  }
}

function privateReply(status, content = "", type = "text/plain; charset=utf-8") {
  return new Response(content || null, { status, headers: {
    "Content-Type": type,
    "Cache-Control": "private, no-store, max-age=0",
    "Pragma": "no-cache",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Content-Security-Policy": "default-src 'none'; script-src 'self'; " +
      "connect-src 'self'; style-src 'unsafe-inline'; " +
      "img-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'"
  } });
}

async function handleAdmin(request, env, path) {
  if (!adminConfigured(env)) return response(404); // OFF by default
  if (!["/admin", "/admin/", "/admin/app.js", "/admin/api/summary"].includes(path)) {
    return response(404);
  }
  if (request.method !== "GET") return privateReply(405);
  if (!(await validAdmin(request, env))) return privateReply(403, "Access denied.");
  if (path === "/admin" || path === "/admin/") {
    return privateReply(200, adminPage, "text/html; charset=utf-8");
  }
  if (path === "/admin/app.js") {
    return privateReply(200, adminScript, "text/javascript; charset=utf-8");
  }
  if (!env.DB || typeof env.DB.prepare !== "function") return privateReply(503);
  const url = new URL(request.url);
  const days = url.searchParams.get("days") || "30";
  if (!["7", "30", "90"].includes(days) || url.searchParams.size > 1) {
    return privateReply(400, "Unsupported period.");
  }
  const today = new Date().toISOString().slice(0, 10);
  const since = new Date(Date.now() - (Number(days) - 1) * 86400000)
    .toISOString().slice(0, 10);
  try {
    const result = await env.DB.prepare(
      "SELECT day, event, section, total FROM daily_counts " +
      "WHERE day >= ?1 AND day <= ?2 " +
      "ORDER BY day DESC, event, section LIMIT 5000"
    ).bind(since, today).all();
    const safe = (result.results || []).filter(row =>
      /^\d{4}-\d{2}-\d{2}$/.test(row.day) &&
      EVENT_TYPES.has(row.event) && SECTIONS.has(row.section) &&
      Number.isSafeInteger(row.total) && row.total >= 0);
    return privateReply(200, JSON.stringify({ days: Number(days), today, rows: safe }),
      "application/json; charset=utf-8");
  } catch {
    return privateReply(503, "Statistics are temporarily unavailable.");
  }
}

export default {
  async fetch(request, env) {
    const path = new URL(request.url).pathname;
    if (path === "/admin" || path.startsWith("/admin/")) {
      return handleAdmin(request, env, path);
    }
    if (path === "/health" && request.method === "GET") {
      return response(200, "", "ok");
    }
    if (path !== "/v1/event") return response(404);
    const origin = request.headers.get("Origin") || "";
    if (origin !== SITE_ORIGIN) return response(403);
    if (request.method === "OPTIONS") {
      const answer = response(204, origin);
      answer.headers.set("Access-Control-Allow-Methods", "POST, OPTIONS");
      answer.headers.set("Access-Control-Allow-Headers", "Content-Type");
      answer.headers.set("Access-Control-Max-Age", "600");
      return answer;
    }
    if (request.method !== "POST") return response(405, origin);
    const contentType = (request.headers.get("Content-Type") || "").toLowerCase();
    if (!/^text\/plain(?:;\s*charset=utf-8)?$/.test(contentType)) {
      return response(415, origin);
    }
    const declaredSize = Number(request.headers.get("Content-Length") || "0");
    if (declaredSize > 256) return response(413, origin);

    let payload;
    try {
      const raw = await readLimitedBody(request, 256);
      if (raw === null) return response(413, origin);
      payload = JSON.parse(raw);
    } catch {
      return response(400, origin);
    }
    if (
      !payload || typeof payload !== "object" || Array.isArray(payload) ||
      Object.keys(payload).length !== 2 ||
      !Object.hasOwn(payload, "event") || !Object.hasOwn(payload, "section") ||
      typeof payload.event !== "string" || !EVENT_TYPES.has(payload.event) ||
      typeof payload.section !== "string" || !SECTIONS.has(payload.section)
    ) {
      return response(400, origin);
    }
    if (!env.DB || typeof env.DB.prepare !== "function") {
      return response(503, origin);
    }
    // Store a DAILY aggregate, never a row identifying an individual visit.
    const day = new Date().toISOString().slice(0, 10);
    try {
      await env.DB.prepare(
        "INSERT INTO daily_counts (day, event, section, total) " +
        "VALUES (?1, ?2, ?3, 1) " +
        "ON CONFLICT(day, event, section) " +
        "DO UPDATE SET total = total + 1"
      ).bind(day, payload.event, payload.section).run();
    } catch {
      // Never echo data or runtime/database details to a visitor.
      return response(503, origin);
    }
    return response(204, origin);
  }
};
