/* FND Education Project — optional first-party aggregate counters.
 *
 * ENABLED ONLY when the site owner explicitly sets analytics_endpoint in
 * Jekyll config after deploying and reviewing the Worker. The browser sends
 * exactly { event: <fixed enum>, section: <fixed enum> }.
 *
 * Never send: URL, search words, click destination, time, referrer, cookies,
 * IP address, user-agent, session ID, or a persistent identifier.
 */
(function () {
  "use strict";

  const endpointTag = document.querySelector('meta[name="fnd-analytics-endpoint"]');
  const configured = (endpointTag && endpointTag.content || "").trim();
  let endpoint;
  try {
    endpoint = new URL(configured);
    if (endpoint.protocol !== "https:" || endpoint.username || endpoint.password) {
      return;
    }
    if (endpoint.search || endpoint.hash) return;
    endpoint.pathname = endpoint.pathname.replace(/\/+$/, "") + "/v1/event";
  } catch {
    return;
  }

  const EVENTS = new Set([
    "page_view", "search_used", "search_result_click", "pdf_download",
    "puzzle_download", "not_found"
  ]);
  const SECTIONS = new Set([
    "home", "course", "reference", "glossary", "puzzles",
    "booklets", "search", "contact", "other"
  ]);

  function sectionForLocation() {
    const first = window.location.pathname.split("/").filter(Boolean)[0] || "home";
    return SECTIONS.has(first) ? first : "other";
  }

  function track(event, section) {
    if (!EVENTS.has(event) || !SECTIONS.has(section)) return;
    const data = JSON.stringify({ event, section });
    // No analytics cookie, no referrer or URL, no persistence on the client.
    // keepalive allows a small counter request to finish during navigation.
    try {
      fetch(endpoint.href, {
        method: "POST", mode: "cors", credentials: "omit",
        headers: { "Content-Type": "text/plain;charset=UTF-8" },
        cache: "no-store", referrerPolicy: "no-referrer",
        body: data, keepalive: true
      }).catch(function () { /* Analytics must never interrupt learning. */ });
    } catch {
      // Site use is never dependent on analytics being available.
    }
  }

  let searchTimer = null;
  function searchUsed() {
    // The Pagefind text never enters this function; only a generic signal.
    // Debounce its normalizer's repeated callbacks during typing.
    if (searchTimer !== null) window.clearTimeout(searchTimer);
    searchTimer = window.setTimeout(function () {
      searchTimer = null;
      track("search_used", "search");
    }, 1200);
  }

  // Search.js runs locally; it signals usage only, never the search term.
  window.FNDAnalytics = Object.freeze({ track, searchUsed });

  document.addEventListener("DOMContentLoaded", function () {
    const section = sectionForLocation();
    track("page_view", section);
    if (document.querySelector(".not-found-page")) {
      track("not_found", "other");
    }
    document.addEventListener("click", function (event) {
      const element = event.target;
      if (!element || typeof element.closest !== "function") return;
      const link = element.closest("a[href]");
      if (!link) return;

      // Pagefind's own results. Destination and search text are not sent.
      if (link.closest(".pagefind-ui__result") ||
          link.classList.contains("pagefind-ui__result-link")) {
        track("search_result_click", "search");
        return;
      }
      let url;
      try { url = new URL(link.href, window.location.href); } catch { return; }
      // Only count downloads to our own domain.
      if (url.origin !== window.location.origin) return;
      const path = url.pathname.toLowerCase();
      if (!/\.(pdf|zip)$/.test(path)) return;
      const kind = path.includes("/assets/puzzles/") ?
        "puzzle_download" : "pdf_download";
      track(kind, section);
    }, { passive: true });
  });
})();
