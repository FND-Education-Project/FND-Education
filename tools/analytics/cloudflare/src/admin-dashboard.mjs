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
<section class="history" aria-labelledby="monthly-history-title">
<h2 id="monthly-history-title">Archived monthly statistics</h2>
<details id="monthly-history">
<summary>Show older monthly totals (up to five years)</summary>
<p class="muted">Older daily records are combined by month. Numbers are
events, not individual visitors. Recently completed months remain in the
daily view until the 120-day retention period ends.</p>
<p id="monthly-message" role="status"></p>
<div class="table-wrap"><table>
<thead><tr><th scope="col">Month (UTC)</th><th scope="col">Page opens</th>
<th scope="col">Searches</th><th scope="col">Result clicks</th>
<th scope="col">Download clicks</th><th scope="col">404 events</th></tr></thead>
<tbody id="monthly-body"></tbody></table></div>
</details></section>
<p class="muted">Dates use UTC. Search counts are debounced; links clicked are not proof of completed downloads. Bots can inflate totals and privacy tools can block counters. No unique visitors, IP addresses, search words, referrers, or individual pages are stored in project analytics.</p>
<p><a href="https://fndeducationproject.org/">Return to the public website</a></p>
</main><script src="/admin/app.js" defer></script></body></html>`;

export const adminScript = `"use strict";
(function () {
  const $ = id => document.getElementById(id);
  const EVENT_LABELS = {
    page_view: "Page openings",
    search_used: "Searches used",
    search_result_click: "Search results opened",
    pdf_download: "PDF link clicks",
    puzzle_download: "Puzzle link clicks",
    not_found: "404 pages"
  };
  const SECTIONS = {
    home: "Home", course: "Course", reference: "Reference",
    glossary: "Glossary", puzzles: "Puzzles", booklets: "Booklets",
    search: "Search", contact: "Contact", other: "Other"
  };
  const COLOR = {
    views: "#3273a6", searches: "#257ab8", clicks: "#a855aa",
    pdf: "#b56a15", puzzles: "#287b5d", errors: "#b34f48",
    downloads: "#287b5d"
  };
  const SVG = "http://www.w3.org/2000/svg";
  const number = n => Number(n).toLocaleString();
  function clear(node) { node.replaceChildren(); }
  function cell(text) {
    const td = document.createElement("td");
    td.textContent = String(text);
    return td;
  }
  function row(tbody, label, total) {
    const tr = document.createElement("tr");
    tr.append(cell(label), cell(number(total)));
    tbody.append(tr);
  }
  function svgElement(tag, attrs = {}, label) {
    const node = document.createElementNS(SVG, tag);
    for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, String(value));
    if (label !== undefined) node.textContent = String(label);
    return node;
  }
  function count(daily, day, event) {
    const dayCounts = daily[day] || {};
    if (event === "downloads") {
      return (dayCounts.pdf_download || 0) + (dayCounts.puzzle_download || 0);
    }
    return dayCounts[event] || 0;
  }
  function plot(id, dates, daily, series, kind) {
    const svg = $(id);
    clear(svg);
    const left = 48, right = 703, top = 20, bottom = 184;
    const spanX = right - left, spanY = bottom - top;
    const maximum = Math.max(0, ...dates.flatMap(day =>
      series.map(s => count(daily, day, s.event))));
    const chartMax = maximum || 1;
    const yPosition = n => bottom - spanY * n / chartMax;
    for (const fraction of [0, 0.5, 1]) {
      const y = yPosition(fraction * chartMax);
      svg.append(svgElement("line", {
        x1: left, x2: right, y1: y, y2: y, class: "grid-line"
      }));
      svg.append(svgElement("text", {
        x: left - 8, y: y + 4, "text-anchor": "end"
      }, number(Math.round(fraction * chartMax))));
    }
    if (!dates.length) return;
    svg.append(svgElement("text", { x: left, y: 209 }, dates[0]));
    svg.append(svgElement("text", {
      x: right, y: 209, "text-anchor": "end"
    }, dates[dates.length - 1]));
    if (maximum === 0) {
      svg.append(svgElement("text", {
        x: (left + right) / 2, y: 110,
        "text-anchor": "middle"
      }, "No recorded activity in this period"));
      return;
    }
    if (kind === "bars") {
      const step = spanX / dates.length;
      const barWidth = Math.max(1.5, Math.min(26, step - 2));
      dates.forEach((day, index) => {
        const value = count(daily, day, series[0].event);
        const height = Math.max(0, bottom - yPosition(value));
        if (!height) return;
        const bar = svgElement("rect", {
          x: left + index * step + (step - barWidth) / 2,
          y: bottom - height, width: barWidth, height,
          fill: series[0].color, class: "data-bar"
        });
        bar.append(svgElement("title", {}, day + ": " + number(value) +
          " " + series[0].label));
        svg.append(bar);
      });
      return;
    }
    const step = spanX / Math.max(1, dates.length - 1);
    for (const entry of series) {
      const points = dates.map((day, index) =>
        (left + index * step).toFixed(1) + "," +
        yPosition(count(daily, day, entry.event)).toFixed(1)).join(" ");
      const line = svgElement("polyline", {
        points, stroke: entry.color, class: "data-line"
      });
      line.append(svgElement("title", {}, entry.label + " across " +
        dates.length + " days"));
      svg.append(line);
      dates.forEach((day, index) => {
        const value = count(daily, day, entry.event);
        const point = svgElement("circle", {
          cx: left + index * step, cy: yPosition(value),
          r: dates.length <= 14 ? 3.7 : 2.3,
          fill: entry.color, class: "data-point"
        });
        point.append(svgElement("title", {}, day + ": " + number(value) +
          " " + entry.label));
        svg.append(point);
      });
    }
  }
  function show(data) {
    const totals = Object.fromEntries(Object.keys(EVENT_LABELS).map(k => [k, 0]));
    const sections = Object.fromEntries(Object.keys(SECTIONS).map(k => [k, 0]));
    const daily = Object.create(null);
    const selectedDays = data.days;
    const today = new Date(data.today + "T00:00:00Z");
    if (!Number.isFinite(today.getTime())) throw new Error("Invalid report date.");
    const dates = Array.from({ length: selectedDays }, (_, index) => {
      const date = new Date(today);
      date.setUTCDate(date.getUTCDate() - (selectedDays - index - 1));
      return date.toISOString().slice(0, 10);
    });
    const allowedDates = new Set(dates);
    for (const item of data.rows) {
      if (!Object.hasOwn(totals, item.event) ||
          !Object.hasOwn(sections, item.section) ||
          !allowedDates.has(item.day)) continue;
      const value = Number(item.total);
      if (!Number.isSafeInteger(value) || value < 0) continue;
      totals[item.event] += value;
      if (item.event === "page_view") sections[item.section] += value;
      const group = daily[item.day] || (daily[item.day] = Object.create(null));
      group[item.event] = (group[item.event] || 0) + value;
    }
    $("k-pages").textContent = number(totals.page_view);
    $("k-search").textContent = number(totals.search_used);
    $("k-clicks").textContent = number(totals.search_result_click);
    $("k-downloads").textContent =
      number(totals.pdf_download + totals.puzzle_download);
    $("k-missing").textContent = number(totals.not_found);
    plot("views-chart", dates, daily, [
      { event: "page_view", label: "page openings", color: COLOR.views }
    ], "bars");
    plot("search-chart", dates, daily, [
      { event: "search_used", label: "searches", color: COLOR.searches },
      { event: "search_result_click", label: "result clicks", color: COLOR.clicks }
    ], "lines");
    plot("clicks-chart", dates, daily, [
      { event: "search_result_click", label: "search-result clicks", color: COLOR.clicks },
      { event: "pdf_download", label: "PDF clicks", color: COLOR.pdf },
      { event: "puzzle_download", label: "puzzle clicks", color: COLOR.puzzles }
    ], "lines");
    plot("download-chart", dates, daily, [
      { event: "downloads", label: "download-link clicks", color: COLOR.downloads }
    ], "bars");
    plot("errors-chart", dates, daily, [
      { event: "not_found", label: "not-found pages", color: COLOR.errors }
    ], "bars");
    const eventsBody = $("events-body"), sectionsBody = $("sections-body");
    const history = $("history-body");
    clear(eventsBody);
    clear(sectionsBody);
    clear(history);
    Object.keys(EVENT_LABELS).forEach(key =>
      row(eventsBody, EVENT_LABELS[key], totals[key]));
    Object.keys(SECTIONS).sort((a, b) => sections[b] - sections[a])
      .forEach(key => row(sectionsBody, SECTIONS[key], sections[key]));
    for (const day of dates.slice().reverse()) {
      const tr = document.createElement("tr");
      tr.append(
        cell(day),
        cell(number(count(daily, day, "page_view"))),
        cell(number(count(daily, day, "search_used"))),
        cell(number(count(daily, day, "search_result_click"))),
        cell(number(count(daily, day, "downloads"))),
        cell(number(count(daily, day, "not_found")))
      );
      history.append(tr);
    }
    $("updated").textContent = "Period: " + dates[0] + " to " +
      dates[dates.length - 1] + " (UTC)";
  }
  async function load() {
    $("error").hidden = true;
    $("updated").textContent = "Loading private daily totals…";
    try {
      const days = $("period").value;
      const response = await fetch("/admin/api/summary?days=" + days, {
        credentials: "same-origin", cache: "no-store", redirect: "error"
      });
      if (!response.ok) throw new Error("Could not load private statistics (" +
        response.status + "). Check your Cloudflare Access sign-in.");
      const data = await response.json();
      if (!data || !Array.isArray(data.rows) ||
          data.days !== Number(days) ||
          typeof data.today !== "string") {
        throw new Error("Unexpected statistics response.");
      }
      show(data);
    } catch (error) {
      $("error").textContent = error.message;
      $("error").hidden = false;
      $("updated").textContent = "";
    }
  }
  // Archived totals are requested only on demand and never from the public
  // event collector. Build rows with textContent, never HTML interpolation.
  const monthlyPanel = $("monthly-history");
  let loadedMonths = false;
  monthlyPanel.addEventListener("toggle", async function () {
    if (!monthlyPanel.open || loadedMonths) return;
    const message = $("monthly-message");
    message.textContent = "Loading archived monthly totals…";
    try {
      const response = await fetch("/admin/api/monthly", {
        credentials: "same-origin", cache: "no-store", redirect: "error"
      });
      if (!response.ok) throw new Error("Monthly archive is not available yet.");
      const data = await response.json();
      if (!data || !Array.isArray(data.rows)) {
        throw new Error("Unexpected monthly archive response.");
      }
      const grouped = new Map();
      for (const item of data.rows) {
        if (!/^\\d{4}-\\d{2}$/.test(item.month) ||
            !Object.hasOwn(EVENT_LABELS, item.event) ||
            !Number.isSafeInteger(item.total) || item.total < 0) continue;
        const counts = grouped.get(item.month) || Object.create(null);
        counts[item.event] = (counts[item.event] || 0) + item.total;
        grouped.set(item.month, counts);
      }
      const body = $("monthly-body");
      clear(body);
      for (const [month, counts] of Array.from(grouped.entries())
        .sort((a, b) => b[0].localeCompare(a[0]))) {
        const tr = document.createElement("tr");
        tr.append(
          cell(month),
          cell(number(counts.page_view || 0)),
          cell(number(counts.search_used || 0)),
          cell(number(counts.search_result_click || 0)),
          cell(number((counts.pdf_download || 0) +
            (counts.puzzle_download || 0))),
          cell(number(counts.not_found || 0))
        );
        body.append(tr);
      }
      message.textContent = grouped.size
        ? "Archived monthly totals (UTC)." :
          "No months have been archived yet.";
      loadedMonths = true;
    } catch (error) {
      message.textContent = error.message;
    }
  });
  $("period").addEventListener("change", load);
  load();
})();`;
