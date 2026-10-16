/**
 * First-party, anonymous COUNTS ONLY for the FND Education Project.
 *
 * The application never requests or stores IPs, cookies, referrers, user
 * agents, identifiers, URLs, search terms, individual activity or timestamps.
 * Network/platform operators may separately process connection metadata.
 *
 * Never log the request or its body; unexpected fields are rejected.
 * Database access is private to this Worker; there is no public dashboard.
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

export default {
  async fetch(request, env) {
    const path = new URL(request.url).pathname;
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
