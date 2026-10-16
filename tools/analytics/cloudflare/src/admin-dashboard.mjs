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
body{margin:0;background:Canvas;color:CanvasText}header{padding:1.3rem max(1rem,calc((100vw - 68rem)/2));background:color-mix(in srgb,CanvasText 5%,Canvas);border-bottom:1px solid GrayText}
main{max-width:68rem;padding:1.2rem 1.15rem 3rem;margin:auto}h1{margin:.1rem 0;font-size:clamp(1.7rem,4vw,2.4rem)}
h2{font-size:1.25rem;margin:1.9rem 0 .6rem}p{max-width:70ch}a{color:LinkText}
.controls{display:flex;flex-wrap:wrap;gap:.65rem;align-items:center;margin:1rem 0}
select{font:inherit;padding:.55rem;border-radius:.4rem;border:1px solid GrayText;background:Canvas;color:CanvasText}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(9rem,1fr));gap:.8rem;margin:1.3rem 0}
.kpi{border:1px solid GrayText;border-radius:.65rem;padding:1rem;background:color-mix(in srgb,CanvasText 4%,Canvas)}
.kpi dt{font-size:.9rem}.kpi dd{font-size:clamp(1.6rem,4vw,2.1rem);font-weight:750;margin:.25rem 0}
#daily-chart{width:100%;max-width:64rem;height:14rem;background:color-mix(in srgb,CanvasText 3%,Canvas);border:1px solid GrayText;border-radius:.5rem}
.tables{display:grid;grid-template-columns:repeat(auto-fit,minmax(16rem,1fr));gap:1.3rem}
.table-wrap{overflow:auto;border:1px solid GrayText;border-radius:.5rem}table{width:100%;border-collapse:collapse}
th,td{padding:.48rem .65rem;text-align:left;border-bottom:1px solid color-mix(in srgb,GrayText 30%,transparent)}
td:last-child{text-align:right;font-variant-numeric:tabular-nums}th{font-size:.9rem;background:color-mix(in srgb,CanvasText 6%,Canvas)}
.muted{color:GrayText}#error{color:CanvasText;font-weight:650}button:focus-visible,select:focus-visible,a:focus-visible{outline:3px solid Highlight;outline-offset:2px}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
</style></head><body>
<header><p>FND EDUCATION PROJECT · PRIVATE ADMINISTRATION</p><h1>Website statistics</h1></header>
<main>
<p>Daily totals only. No visitor profiles, unique-person estimates, search terms or personal histories.</p>
<div class="controls"><label for="period">Time range</label>
<select id="period"><option value="7">Last 7 days</option><option value="30" selected>Last 30 days</option><option value="90">Last 90 days</option></select>
<span id="updated" class="muted" aria-live="polite"></span></div>
<p id="error" role="alert" hidden></p>
<dl class="kpis">
<div class="kpi"><dt>Page openings</dt><dd id="k-pages">—</dd></div>
<div class="kpi"><dt>Searches used</dt><dd id="k-search">—</dd></div>
<div class="kpi"><dt>Search results opened</dt><dd id="k-clicks">—</dd></div>
<div class="kpi"><dt>PDF/ZIP link clicks</dt><dd id="k-downloads">—</dd></div>
</dl>
<section aria-labelledby="daily-title"><h2 id="daily-title">Daily page activity</h2>
<svg id="daily-chart" role="img" aria-label="Bar chart of page openings by day" viewBox="0 0 700 210"></svg>
<p class="muted">Bars represent page openings, not unique people or sessions.</p></section>
<div class="tables">
<section aria-labelledby="events-title"><h2 id="events-title">Actions</h2><div class="table-wrap">
<table><thead><tr><th scope="col">Event</th><th scope="col">Total</th></tr></thead>
<tbody id="events-body"></tbody></table></div></section>
<section aria-labelledby="sections-title"><h2 id="sections-title">Page openings by section</h2><div class="table-wrap">
<table><thead><tr><th scope="col">Section</th><th scope="col">Opens</th></tr></thead>
<tbody id="sections-body"></tbody></table></div></section>
</div>
<section aria-labelledby="history-title"><h2 id="history-title">Daily breakdown</h2>
<div class="table-wrap"><table><thead><tr><th>Date (UTC)</th><th>Pages</th><th>Searches</th><th>Results</th><th>Downloads</th></tr></thead>
<tbody id="history-body"></tbody></table></div></section>
<p class="muted">Searches are counted after a typing pause; link clicks do not guarantee completed downloads.
Counts may include bots or omit requests blocked by privacy tools. Data is grouped in UTC.</p>
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
