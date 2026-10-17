/* Read-only administrator statistics dashboard.
 * The Worker returns HTML/JS only after verifying a Cloudflare Access JWT.
 * No public stats endpoint and no access to visitor identities.
 */
export const adminPage = `<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>Site statistics | FND Education Project</title>
<style>
:root{font:16px/1.5 system-ui,-apple-system,Segoe UI,sans-serif;color-scheme:light dark}
body{margin:0;background:Canvas;color:CanvasText}
header{padding:1.25rem max(1rem,calc((100vw - 73rem)/2));background:color-mix(in srgb,CanvasText 5%,Canvas);border-bottom:1px solid color-mix(in srgb,CanvasText 24%,transparent)}
main{max-width:73rem;padding:1.4rem 1.15rem 3rem;margin:auto}
h1{margin:.15rem 0;font-size:clamp(1.75rem,4vw,2.45rem)}
h2{font-size:1.3rem;margin:0 0 .35rem}
a{color:LinkText}p{max-width:75ch}
.controls{display:flex;flex-wrap:wrap;gap:.7rem;align-items:center;margin:1.3rem 0}
select{font:inherit;padding:.55rem;border-radius:.4rem;border:1px solid GrayText;background:Canvas;color:CanvasText}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,10rem),1fr));gap:.85rem;margin:1.3rem 0 1.5rem}
.kpi{border:1px solid color-mix(in srgb,CanvasText 27%,transparent);border-radius:.7rem;padding:1rem 1.05rem;background:color-mix(in srgb,CanvasText 4%,Canvas)}
.kpi dt{font-size:.86rem}.kpi dd{font-size:clamp(1.6rem,4vw,2.15rem);font-weight:750;margin:.2rem 0;font-variant-numeric:tabular-nums}
.kpi small{font-size:.75rem;color:GrayText}
.chart-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;margin-top:1.2rem}
.chart-panel{min-width:0;padding:1.05rem;border:1px solid color-mix(in srgb,CanvasText 26%,transparent);border-radius:.75rem;background:Canvas}
.chart-panel.featured{grid-column:1/-1}
.chart-panel p{margin:.3rem 0 .55rem;font-size:.88rem}
.chart{display:block;width:100%;height:auto;max-height:19rem;overflow:visible;background:color-mix(in srgb,CanvasText 3%,Canvas);border-radius:.35rem}
.chart text{font:12px system-ui,-apple-system,Segoe UI,sans-serif;fill:CanvasText}
.chart .grid-line{stroke:color-mix(in srgb,CanvasText 17%,Canvas)}
.chart .data-line{fill:none;stroke-width:2.7;stroke-linejoin:round;stroke-linecap:round}
.chart .data-bar{opacity:.85}
.chart .data-point{stroke:Canvas;stroke-width:1.5}
.legend{display:flex;gap:.5rem 1.25rem;flex-wrap:wrap;margin:.65rem 0 0;padding:0;list-style:none}
.legend li{display:flex;align-items:center;gap:.4rem;font-size:.82rem;margin:0}
.legend-swatch{display:inline-block;width:1.3rem;height:.25rem;border-radius:.3rem}
.tables{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,19rem),1fr));gap:1.2rem;margin-top:1.6rem}
.table-wrap{overflow:auto;border:1px solid color-mix(in srgb,CanvasText 26%,transparent);border-radius:.5rem}
table{width:100%;border-collapse:collapse}
th,td{padding:.55rem .7rem;text-align:left;border-bottom:1px solid color-mix(in srgb,CanvasText 17%,transparent)}
td:not(:first-child){text-align:right;font-variant-numeric:tabular-nums}
th{font-size:.89rem;background:color-mix(in srgb,CanvasText 6%,Canvas)}
.history{margin:1.5rem 0}
.history details{border:1px solid color-mix(in srgb,CanvasText 26%,transparent);border-radius:.6rem;padding:1rem}
.history summary{font-weight:700;cursor:pointer}
.history .table-wrap{margin-top:.8rem}
.muted{color:GrayText}
#error{color:CanvasText;font-weight:650}
button:focus-visible,select:focus-visible,a:focus-visible,summary:focus-visible{outline:3px solid Highlight;outline-offset:2px}
@media(max-width:44rem){.chart-grid{grid-template-columns:1fr}.chart-panel.featured{grid-column:auto}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
</style></head><body>
<header><p>FND EDUCATION PROJECT · PRIVATE ADMINISTRATION</p><h1>Website statistics</h1></header>
<main>
<p>Anonymous daily totals. These charts show how the website is used over time—not who uses it.</p>
<div class="controls"><label for="period">Show trends for</label>
<select id="period"><option value="7">Last 7 days</option><option value="30" selected>Last 30 days</option><option value="90">Last 90 days</option></select>
<span id="updated" class="muted" aria-live="polite"></span></div>
<p id="error" role="alert" hidden></p>
<dl class="kpis">
<div class="kpi"><dt>Page openings</dt><dd id="k-pages">—</dd><small>Not unique visitors</small></div>
<div class="kpi"><dt>Searches used</dt><dd id="k-search">—</dd><small>Search interactions</small></div>
<div class="kpi"><dt>Search results opened</dt><dd id="k-clicks">—</dd><small>Result-link clicks</small></div>
<div class="kpi"><dt>Download-link clicks</dt><dd id="k-downloads">—</dd><small>PDFs and puzzles</small></div>
<div class="kpi"><dt>Not-found pages</dt><dd id="k-missing">—</dd><small>404 events</small></div>
</dl>
<div class="chart-grid">
<section class="chart-panel featured" aria-labelledby="views-title">
<h2 id="views-title">Page openings by day</h2>
<p class="muted">How reading activity changes over the selected time period.</p>
<svg id="views-chart" class="chart" role="img" aria-label="Daily page openings bar chart" viewBox="0 0 720 225"></svg>
</section>
<section class="chart-panel" aria-labelledby="search-title">
<h2 id="search-title">Search activity over time</h2>
<p class="muted">Compare searches with selections from search results.</p>
<svg id="search-chart" class="chart" role="img" aria-label="Daily searches and search-result clicks line chart" viewBox="0 0 720 225"></svg>
<ul class="legend"><li><span class="legend-swatch" style="background:#257ab8"></span>Searches used</li>
<li><span class="legend-swatch" style="background:#a855aa"></span>Result clicks</li></ul>
</section>
<section class="chart-panel" aria-labelledby="clicks-title">
<h2 id="clicks-title">Clicks by day</h2>
<p class="muted">Result selections and download-link clicks, grouped by type.</p>
<svg id="clicks-chart" class="chart" role="img" aria-label="Daily search-result, PDF, and puzzle link clicks line chart" viewBox="0 0 720 225"></svg>
<ul class="legend"><li><span class="legend-swatch" style="background:#a855aa"></span>Search results</li>
<li><span class="legend-swatch" style="background:#b56a15"></span>PDF links</li>
<li><span class="legend-swatch" style="background:#287b5d"></span>Puzzle links</li></ul>
</section>
<section class="chart-panel" aria-labelledby="download-title">
<h2 id="download-title">Downloads over time</h2>
<p class="muted">Daily clicks on PDF and puzzle download links—not completed downloads.</p>
<svg id="download-chart" class="chart" role="img" aria-label="Daily combined download-link clicks bar chart" viewBox="0 0 720 225"></svg>
</section>
<section class="chart-panel" aria-labelledby="errors-title">
<h2 id="errors-title">Missing-page requests over time</h2>
<p class="muted">Daily 404-page events may reveal broken links or outdated bookmarks.</p>
<svg id="errors-chart" class="chart" role="img" aria-label="Daily not-found page events bar chart" viewBox="0 0 720 225"></svg>
</section>
</div>
<div class="tables">
<section aria-labelledby="sections-title"><h2 id="sections-title">Page openings by website section</h2>
<p class="muted">Find which broad areas are most used.</p><div class="table-wrap">
<table><thead><tr><th scope="col">Section</th><th scope="col">Page opens</th></tr></thead>
<tbody id="sections-body"></tbody></table></div></section>
<section aria-labelledby="events-title"><h2 id="events-title">Activity totals</h2>
<p class="muted">All event types in the selected period.</p><div class="table-wrap">
<table><thead><tr><th scope="col">Event</th><th scope="col">Total</th></tr></thead>
<tbody id="events-body"></tbody></table></div></section>
</div>
<section class="history" aria-labelledby="history-title"><h2 id="history-title">Detailed daily figures</h2>
<details><summary>Show daily table for this period</summary>
<div class="table-wrap"><table><thead><tr><th scope="col">Date (UTC)</th><th scope="col">Pages</th><th scope="col">Searches</th><th scope="col">Result clicks</th><th scope="col">Downloads</th><th scope="col">404s</th></tr></thead>
<tbody id="history-body"></tbody></table></div></details></section>
<p class="muted">Dates use UTC. Search counts are debounced; links clicked are not proof of completed downloads. Bots can inflate totals and privacy tools can block counters. No unique visitors, IP addresses, search words, referrers, or individual pages are stored in project analytics.</p>
<p><a href="https://fndeducationproject.org/">Return to the public website</a></p>
</main><script src="/admin/app.js" defer></script></body></html>`;

export const adminScript = `"use strict";
(function () {
  const $ = id => document.getElementById(id);
  const EVENT_LABELS = {
    page_view: "Page openings", search_used: "Searches used",
    search_result_click: "Search results opened",
    pdf_download: "PDF link clicks", puzzle_download: "Puzzle link clicks",
    not_found: "404 pages"
  };
  const SECTIONS = {
    home: "Home", course: "Course", reference: "Reference",
    glossary: "Glossary", puzzles: "Puzzles", booklets: "Booklets",
    search: "Search", contact: "Contact", other: "Other"
  };
  const format = n => Number(n).toLocaleString();
  function clear(node) { node.replaceChildren(); }
  function td(text) { const el = document.createElement("td"); el.textContent = String(text); return el; }
  function row(tbody, label, total) {
    const tr = document.createElement("tr");
    tr.append(td(label), td(format(total)));
    tbody.append(tr);
  }
  function chart(days, daily) {
    const svg = $("daily-chart"); clear(svg);
    const xmlns = "http://www.w3.org/2000/svg";
    const max = Math.max(1, ...days.map(d => daily[d]?.page_view || 0));
    const width = 668 / Math.max(days.length, 1);
    for (let i = 0; i < days.length; i++) {
      const n = daily[days[i]]?.page_view || 0, height = n / max * 165;
      const bar = document.createElementNS(xmlns, "rect");
      bar.setAttribute("x", String(20 + i * width + 1));
      bar.setAttribute("y", String(182 - height));
      bar.setAttribute("width", String(Math.max(1, width - 2)));
      bar.setAttribute("height", String(Math.max(0, height)));
      bar.setAttribute("fill", "currentColor");
      const tooltip = document.createElementNS(xmlns, "title");
      tooltip.textContent = days[i] + ": " + n + " page openings";
      bar.append(tooltip); svg.append(bar);
    }
    const label = document.createElementNS(xmlns, "text");
    label.setAttribute("x", "20"); label.setAttribute("y", "202");
    label.setAttribute("fill", "currentColor"); label.setAttribute("font-size", "12");
    label.textContent = days[0] + " — " + days[days.length - 1];
    svg.append(label);
  }
  function show(data) {
    const totals = Object.fromEntries(Object.keys(EVENT_LABELS).map(k => [k, 0]));
    const sections = Object.fromEntries(Object.keys(SECTIONS).map(k => [k, 0]));
    const daily = {};
    for (const item of data.rows) {
      if (!Object.hasOwn(totals, item.event) ||
          !Object.hasOwn(sections, item.section) ||
          !/^\\d{4}-\\d{2}-\\d{2}$/.test(item.day)) continue;
      const n = Number(item.total);
      if (!Number.isSafeInteger(n) || n < 0) continue;
      totals[item.event] += n;
      if (item.event === "page_view") sections[item.section] += n;
      const entry = daily[item.day] || (daily[item.day] = {});
      entry[item.event] = (entry[item.event] || 0) + n;
    }
    $("k-pages").textContent = format(totals.page_view);
    $("k-search").textContent = format(totals.search_used);
    $("k-clicks").textContent = format(totals.search_result_click);
    $("k-downloads").textContent =
      format(totals.pdf_download + totals.puzzle_download);
    const eventRows = $("events-body"), sectionRows = $("sections-body"),
      history = $("history-body");
    clear(eventRows); clear(sectionRows); clear(history);
    Object.keys(EVENT_LABELS).forEach(key => row(eventRows, EVENT_LABELS[key], totals[key]));
    Object.keys(SECTIONS).forEach(key => row(sectionRows, SECTIONS[key], sections[key]));
    const dates = Array.from({ length: data.days }, (_, i) => {
      const d = new Date(data.today + "T00:00:00Z");
      d.setUTCDate(d.getUTCDate() - (data.days - i - 1));
      return d.toISOString().slice(0, 10);
    });
    for (const day of dates.slice().reverse()) {
      const v = daily[day] || {}, tr = document.createElement("tr");
      tr.append(td(day), td(format(v.page_view || 0)),
        td(format(v.search_used || 0)),
        td(format(v.search_result_click || 0)),
        td(format((v.pdf_download || 0) + (v.puzzle_download || 0))));
      history.append(tr);
    }
    chart(dates, daily);
    $("updated").textContent = "Updated from aggregate counters (UTC)";
  }
  async function load() {
    $("error").hidden = true;
    $("updated").textContent = "Loading…";
    try {
      const days = $("period").value;
      const response = await fetch("/admin/api/summary?days=" + days,
        { credentials: "same-origin", cache: "no-store", redirect: "error" });
      if (!response.ok) throw new Error("Could not load private statistics (" +
        response.status + "). Check your Cloudflare Access login.");
      const data = await response.json();
      if (!Array.isArray(data.rows) || data.days !== Number(days)) {
        throw new Error("Unexpected statistics response.");
      }
      show(data);
    } catch (error) {
      $("error").textContent = error.message;
      $("error").hidden = false;
      $("updated").textContent = "";
    }
  }
  $("period").addEventListener("change", load);
  load();
})();`;
