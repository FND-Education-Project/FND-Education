/**
 * Separate, access-protected, READ-ONLY FND daily statistics Worker.
 * DO NOT ROUTE PUBLIC /v1/event TRAFFIC HERE.
 * Bind the EXISTING D1 database; configure Cloudflare Access for the
 * entire Worker and GitHub-only administrator identity.
 * Fails closed until all three Access settings are present.
 */
import { adminPage, adminScript } from "./admin-dashboard.mjs";

const EVENT_TYPES = new Set([
  "page_view", "search_used", "search_result_click", "pdf_download",
  "puzzle_download", "not_found"
]);
const SECTIONS = new Set([
  "home", "course", "reference", "glossary", "puzzles",
  "booklets", "search", "contact", "other"
]);

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

// All diagnostic results are fixed non-identifying codes: never return,
// log, or persist token content, identity details, request headers or IPs.
// Diagnostic mode is OFF unless the owner explicitly enables a temporary
// ADMIN_AUTH_DIAGNOSTIC Worker secret. The normal denial remains unchanged.
function denied(code) { return { authorized: false, code }; }

async function checkAdmin(request, env) {
  if (!adminConfigured(env)) return denied("A00"); // missing/invalid configuration
  const token = accessToken(request);
  if (!token) return denied("A01"); // no Access assertion or cookie
  if (token.length < 50 || token.length > 8192) return denied("A02");
  try {
    const parts = token.split(".");
    if (parts.length !== 3) return denied("A02");
    const header = JSON.parse(new TextDecoder().decode(decodePart(parts[0])));
    const claims = JSON.parse(new TextDecoder().decode(decodePart(parts[1])));
    if (header.alg !== "RS256" || typeof header.kid !== "string") {
      return denied("A03"); // unsupported signing header
    }
    const now = Math.floor(Date.now() / 1000);
    if (claims.iss !== "https://" + env.ACCESS_TEAM_DOMAIN) {
      return denied("A04"); // issuer mismatch
    }
    const aud = claims.aud;
    if (!(Array.isArray(aud) ? aud.includes(env.ACCESS_APP_AUD) :
          aud === env.ACCESS_APP_AUD)) {
      return denied("A05"); // Access application audience mismatch
    }
    if (typeof claims.sub !== "string" || !claims.sub) {
      return denied("A06"); // missing subject
    }
    if (!Number.isFinite(claims.exp) || claims.exp <= now ||
        (claims.nbf !== undefined && claims.nbf > now) ||
        (claims.iat !== undefined && claims.iat > now + 60)) {
      return denied("A07"); // JWT validity time
    }
    if (typeof claims.email !== "string" ||
        claims.email.toLowerCase() !== env.ADMIN_ALLOWED_EMAIL.toLowerCase()) {
      return denied("A08"); // administrator email claim
    }

    let keys = certCache.keys;
    if (certCache.host !== env.ACCESS_TEAM_DOMAIN ||
        certCache.expires < Date.now()) {
      // No certificate, header, JWT, or URL data enters diagnostic output.
      // Separate transport, HTTP status, and JSON errors for one-time
      // troubleshooting; manual redirect handling keeps an unexpected
      // redirect as an inspectable 3xx rather than a thrown fetch error.
      // We never follow redirected certificate URLs. When diagnostics are
      // disabled every denial remains the original generic response.
      let certResponse;
      try {
        certResponse = await fetch("https://" + env.ACCESS_TEAM_DOMAIN +
          "/cdn-cgi/access/certs", { redirect: "manual" });
      } catch {
        return denied("A09F"); // fetch rejected (network, TLS or redirect)
      }
      if (!certResponse.ok) {
        return denied("A09H" + certResponse.status); // public HTTP status only
      }
      let document;
      try {
        document = await certResponse.json();
      } catch {
        return denied("A09J"); // received non-JSON/unparseable response
      }
      if (!Array.isArray(document.keys) || document.keys.length > 20) {
        return denied("A10"); // certs content rejected
      }
      keys = document.keys;
      certCache = { host: env.ACCESS_TEAM_DOMAIN,
        expires: Date.now() + 15 * 60 * 1000, keys };
    }
    const jwk = keys.find(k => k.kid === header.kid && k.kty === "RSA" &&
      k.alg === "RS256" && k.use === "sig");
    if (!jwk) return denied("A11"); // no matching trusted key

    let key;
    try {
      key = await crypto.subtle.importKey(
        "jwk", jwk, { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" },
        false, ["verify"]
      );
    } catch {
      return denied("A12"); // public JWK cannot be imported
    }
    const valid = await crypto.subtle.verify("RSASSA-PKCS1-v1_5", key,
      decodePart(parts[2]), new TextEncoder().encode(parts[0] + "." + parts[1]));
    return valid ? { authorized: true } : denied("A13"); // signature
  } catch {
    return denied("A99"); // malformed token or unexpected verification failure
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
  if (!adminConfigured(env)) return privateReply(404); // OFF by default
  if (!["/admin", "/admin/", "/admin/app.js", "/admin/api/summary", "/admin/api/monthly"].includes(path)) {
    return privateReply(404);
  }
  if (request.method !== "GET") return privateReply(405);
  const access = await checkAdmin(request, env);
  if (!access.authorized) {
    const diagnostic = env.ADMIN_AUTH_DIAGNOSTIC === "enabled"
      ? " Diagnostic code: " + access.code + "."
      : "";
    return privateReply(403, "Access denied." + diagnostic);
  }
  if (path === "/admin" || path === "/admin/") {
    return privateReply(200, adminPage, "text/html; charset=utf-8");
  }
  if (path === "/admin/app.js") {
    return privateReply(200, adminScript, "text/javascript; charset=utf-8");
  }
  if (!env.DB || typeof env.DB.prepare !== "function") return privateReply(503);
  const url = new URL(request.url);
  if (path === "/admin/api/monthly") {
    if (url.searchParams.size) return privateReply(400, "Unexpected parameters.");
    const cutoff = new Date();
    cutoff.setUTCFullYear(cutoff.getUTCFullYear() - 5);
    const since = cutoff.toISOString().slice(0, 7);
    try {
      const result = await env.DB.prepare(
        "SELECT month, event, SUM(total) AS total FROM monthly_counts " +
        "WHERE month >= ?1 GROUP BY month, event " +
        "ORDER BY month DESC, event LIMIT 500"
      ).bind(since).all();
      const safe = (result.results || []).filter(row =>
        /^\d{4}-\d{2}$/.test(row.month) &&
        EVENT_TYPES.has(row.event) &&
        Number.isSafeInteger(row.total) && row.total >= 0);
      return privateReply(200, JSON.stringify({ rows: safe }),
        "application/json; charset=utf-8");
    } catch {
      // If the monthly table is not migrated, the primary dashboard
      // and the existing 7/30/90-day API must continue working.
      return privateReply(503, "Monthly totals are not available yet.");
    }
  }
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
    // The private dashboard deliberately has NO public counter routes.
    return handleAdmin(request, env, new URL(request.url).pathname);
  }
};
