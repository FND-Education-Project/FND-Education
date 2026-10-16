/* Visitor-facing crossword workshop. No upload, login, server generation or tracking.
 * Approved bank is exported on each Pages build from the owner's Excel file.
 */
/* global FNDCrosswordCore, FNDCrosswordPdf */
(function () {
  "use strict";
  const $ = id => document.getElementById(id);
  const root = $("crossword-app");
  if (!root) return;
  const state = { rows: [], candidates: [], selected: 0 };
  const scope = $("cw-scope"), mod = $("cw-module"), lesson = $("cw-lesson");
  const count = $("cw-count"), title = $("cw-title"), size = $("cw-size");
  const seed = $("cw-seed"), effort = $("cw-effort"), status = $("cw-status");
  const choices = $("cw-choices"), preview = $("cw-preview");
  const download = $("cw-download"), generate = $("cw-generate");
  const pdf = FNDCrosswordPdf, core = FNDCrosswordCore;
  function message(s, error = false) {
    status.textContent = s;
    status.classList.toggle("cw-error", error);
  }
  function options(select, values, titleFor) {
    select.replaceChildren();
    for (const value of values) {
      const option = document.createElement("option");
      option.value = String(value);
      option.textContent = titleFor(value);
      select.append(option);
    }
  }
  function currentPool() {
    return core.poolFor(state.rows, scope.value, Number(mod.value), Number(lesson.value));
  }
  function refresh() {
    const mode = scope.value;
    mod.closest(".cw-field").hidden = mode === "all";
    lesson.closest(".cw-field").hidden = mode !== "lesson";
    const modules = [...new Set(state.rows.map(q => q.module))].sort((a, b) => a - b);
    const lastMod = mod.value;
    options(mod, modules, n => "Module " + n);
    if (modules.includes(Number(lastMod))) mod.value = lastMod;
    const lessons = [...new Set(state.rows.filter(q => q.module === Number(mod.value))
      .map(q => q.lesson))].sort((a, b) => a - b);
    const lastLesson = lesson.value;
    options(lesson, lessons, n => "Lesson " + n);
    if (lessons.includes(Number(lastLesson))) lesson.value = lastLesson;
    try {
      const pool = currentPool();
      count.textContent = pool.primary.length + " questions in this selection" +
        (mode === "lesson" ? " (earlier lessons may help fill crossings)" : "") + ".";
      const label = mode === "all" ? "FND Review Crossword" :
        mode === "module" ? "Module " + mod.value + " Crossword" :
          "Module " + mod.value + " - Lesson " + lesson.value + " Crossword";
      title.value = label;
    } catch (e) {
      count.textContent = e.message;
    }
    state.candidates = [];
    choices.replaceChildren();
    preview.replaceChildren();
    download.hidden = true;
  }
  function create(tag, text, className) {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (className) node.className = className;
    return node;
  }
  function drawPreview(layout) {
    preview.replaceChildren();
    const headline = create("h3", "Selected crossword preview");
    const caption = create("p",
      layout.placed.length + " answers · " + layout.crosses +
      " crossing squares · " + layout.rows + " rows by " + layout.cols + " columns",
      "cw-caption");
    const gridScroll = create("div", undefined, "cw-grid-scroll");
    const grid = create("div", undefined, "cw-grid");
    grid.style.gridTemplateColumns = "repeat(" + layout.cols + ", minmax(1.1rem, 1fr))";
    const numbers = new Map(layout.placed.map(p => [p.row + "," + p.col, p.number]));
    for (let r = 0; r < layout.rows; r++) {
      for (let c = 0; c < layout.cols; c++) {
        const letter = layout.cells[r][c];
        const cell = create("div", undefined, "cw-square" +
          (letter ? " cw-square-open" : " cw-square-dotted"));
        const number = numbers.get(r + "," + c);
        if (number) cell.append(create("span", String(number), "cw-number"));
        grid.append(cell);
      }
    }
    grid.setAttribute("role", "img");
    grid.setAttribute("aria-label", "Blank " + layout.rows + " by " +
      layout.cols + " crossword grid. All numbered clues follow.");
    gridScroll.append(grid);
    preview.append(headline, caption, gridScroll);
    const columns = create("div", undefined, "cw-clue-columns");
    for (const dir of ["across", "down"]) {
      const block = create("section");
      block.append(create("h4", dir === "across" ? "Across" : "Down"));
      const list = create("ol", undefined, "cw-clues");
      const clues = layout.placed.filter(p => p.direction === dir)
        .sort((a, b) => a.number - b.number);
      for (const p of clues) {
        const li = create("li", p.entry.clue);
        li.value = p.number;
        list.append(li);
      }
      block.append(list);
      columns.append(block);
    }
    preview.append(columns);
  }
  function selectChoice(index) {
    state.selected = index;
    drawPreview(state.candidates[index]);
    download.hidden = false;
    choices.querySelectorAll("button").forEach((button, i) =>
      button.setAttribute("aria-pressed", String(i === index)));
  }
  async function produce() {
    generate.disabled = true;
    message("Generating possible crossword layouts in your browser…");
    choices.replaceChildren();
    preview.replaceChildren();
    download.hidden = true;
    await new Promise(resolve => setTimeout(resolve, 30));
    try {
      const mode = scope.value, m = Number(mod.value), l = Number(lesson.value);
      const proposed = core.createCandidates(state.rows, mode, m, l,
        Number(seed.value), Number(size.value), Number(effort.value));
      state.candidates = proposed.filter(p => {
        try { pdf.plan(p, "easy", title.value); return true; } catch { return false; }
      });
      if (!state.candidates.length) {
        for (const limit of [14, 11, 8]) {
          const smaller = core.createCandidates(state.rows, mode, m, l,
            Number(seed.value) + limit, limit, Number(effort.value));
          state.candidates = smaller.filter(p => {
            try { pdf.plan(p, "easy", title.value); return true; } catch { return false; }
          });
          if (state.candidates.length) break;
        }
      }
      if (!state.candidates.length) throw new Error(
        "This selection has no layouts that fit the one-page PDF at readable size. " +
        "Try a shorter title, another lesson or a module review.");
      state.candidates.forEach((layout, i) => {
        const button = create("button",
          "Option " + (i + 1) + " — " + layout.placed.length +
          " words, " + layout.crosses + " crossings", "cw-choice");
        button.type = "button";
        button.addEventListener("click", () => selectChoice(i));
        choices.append(button);
      });
      selectChoice(0);
      message(state.candidates.length + " printable crossword choices are ready. " +
        "Choose a layout and download a PDF edition.");
    } catch (e) {
      message(e.message || "Unable to create a crossword for this selection.", true);
    } finally {
      generate.disabled = false;
    }
  }
  function filename(s) {
    return pdf.ascii(s).toLowerCase().replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "").slice(0, 65) || "fnd-crossword";
  }
  function saveEdition(edition) {
    try {
      const layout = state.candidates[state.selected];
      if (!layout) throw new Error("Generate a puzzle before downloading.");
      const bytes = pdf.makePdf(layout, title.value.trim(), edition);
      const blob = new Blob([bytes], { type: "application/pdf" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = filename(title.value) + "-" + edition + ".pdf";
      document.body.append(link);
      link.click();
      link.remove();
      window.setTimeout(() => URL.revokeObjectURL(url), 2000);
      // Public anonymous PDF click analytics is handled by the site for
      // ordinary links; blob-generated downloads deliberately reveal no title.
    } catch (e) { message(e.message, true); }
  }
  scope.addEventListener("change", refresh);
  mod.addEventListener("change", refresh);
  lesson.addEventListener("change", refresh);
  generate.addEventListener("click", produce);
  title.addEventListener("input", () => {
    if (state.candidates.length) {
      try { pdf.plan(state.candidates[state.selected], "easy", title.value); 
        message("Title fits the PDF."); }
      catch (e) { message(e.message, true); }
    }
  });
  for (const edition of ["normal", "easy", "key"]) {
    $("cw-" + edition).addEventListener("click", () => saveEdition(edition));
  }
  async function load() {
    try {
      const url = root.dataset.bankUrl;
      if (!url) throw new Error("Question-bank URL is not configured.");
      const response = await fetch(url, { cache: "no-store", credentials: "omit" });
      if (!response.ok) throw new Error("The published question bank could not be loaded.");
      const parsed = await response.json();
      if (parsed.schema !== 1 || !Array.isArray(parsed.questions) ||
          !parsed.questions.length) throw new Error("Unexpected crossword data.");
      state.rows = parsed.questions.filter(q =>
        typeof q.clue === "string" && /^[A-Z]{2,40}$/.test(q.answer) &&
        Number.isInteger(q.lesson) && Number.isInteger(q.module) &&
        [1, 2, 3].includes(q.priority));
      if (!state.rows.length) throw new Error("No usable crossword questions were published.");
      generate.disabled = false;
      refresh();
      message("Ready. All puzzle creation happens on your device; no login needed.");
    } catch (e) { message(e.message, true); }
  }
  load();
})();
