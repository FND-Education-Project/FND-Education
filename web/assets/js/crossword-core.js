/* FND crossword placement engine. Local-only: no tracking, accounts or network. */
/* global globalThis */
(function (root) {
  "use strict";
  function random(seed) {
    let s = (seed >>> 0) || 1;
    return function () {
      s += 0x6D2B79F5;
      let t = s;
      t = Math.imul(t ^ t >>> 15, t | 1);
      t ^= t + Math.imul(t ^ t >>> 7, t | 61);
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  const key = (r, c) => r + "," + c;
  function poolFor(rows, scope, moduleNumber, lessonNumber) {
    if (!Array.isArray(rows)) throw new Error("Question bank was not loaded.");
    let primary, loans = [];
    if (scope === "lesson") {
      primary = rows.filter(q => q.module === moduleNumber && q.lesson === lessonNumber);
      loans = rows.filter(q => q.module < moduleNumber ||
        (q.module === moduleNumber && q.lesson < lessonNumber))
        .sort((a, b) => b.module - a.module || b.lesson - a.lesson ||
          a.priority - b.priority);
    } else if (scope === "module") {
      primary = rows.filter(q => q.module === moduleNumber);
    } else if (scope === "all") {
      primary = rows.slice();
    } else {
      throw new Error("Choose lesson, module or all.");
    }
    if (!primary.length) throw new Error("There are no questions for that selection.");
    // Only one clue can describe a given answer within a crossword.
    const seen = new Set();
    primary = primary.slice().sort((a, b) => a.priority - b.priority)
      .filter(q => !seen.has(q.answer) && seen.add(q.answer));
    loans = loans.filter(q => !seen.has(q.answer) && seen.add(q.answer));
    return { primary, loans };
  }
  function board() {
    return { cells: new Map(), placed: [], minR: 0, minC: 0, maxR: 0, maxC: 0 };
  }
  function dimension(b, r, c) {
    if (!b.placed.length) return { rows: 1, cols: 1, area: 1 };
    const minR = Math.min(b.minR, r), maxR = Math.max(b.maxR, r);
    const minC = Math.min(b.minC, c), maxC = Math.max(b.maxC, c);
    return { rows: maxR - minR + 1, cols: maxC - minC + 1,
      area: (maxR - minR + 1) * (maxC - minC + 1) };
  }
  function check(b, word, row, col, dir) {
    const dr = dir === "down" ? 1 : 0, dc = dir === "across" ? 1 : 0;
    const before = b.cells.get(key(row - dr, col - dc));
    const after = b.cells.get(key(row + word.length * dr, col + word.length * dc));
    if (before || after) return null;
    let crosses = 0;
    for (let i = 0; i < word.length; i++) {
      const r = row + dr * i, c = col + dc * i;
      const at = b.cells.get(key(r, c));
      if (at) {
        if (at.ch !== word[i] || at.dirs.has(dir)) return null;
        crosses++;
      } else if (
        b.cells.has(key(r + dc, c + dr)) ||
        b.cells.has(key(r - dc, c - dr))
      ) return null;
    }
    if (b.placed.length && !crosses) return null;
    // One-sheet printable crosswords: keep a modest bounded working grid.
    let minR = row, maxR = row + dr * (word.length - 1);
    let minC = col, maxC = col + dc * (word.length - 1);
    if (b.placed.length) {
      minR = Math.min(minR, b.minR); maxR = Math.max(maxR, b.maxR);
      minC = Math.min(minC, b.minC); maxC = Math.max(maxC, b.maxC);
    }
    const rows = maxR - minR + 1, cols = maxC - minC + 1;
    if (rows > 23 || cols > 32) return null;
    return { crosses, area: rows * cols, rows, cols };
  }
  function insert(b, entry, r, c, dir) {
    const dr = dir === "down" ? 1 : 0, dc = dir === "across" ? 1 : 0;
    for (let i = 0; i < entry.answer.length; i++) {
      const rr = r + dr * i, cc = c + dc * i, k = key(rr, cc);
      const cell = b.cells.get(k);
      if (cell) cell.dirs.add(dir);
      else b.cells.set(k, { ch: entry.answer[i], dirs: new Set([dir]) });
    }
    b.placed.push({ entry, row: r, col: c, direction: dir });
    const ranges = b.placed.length === 1 ?
      [r, c, r + dr * (entry.answer.length - 1), c + dc * (entry.answer.length - 1)] :
      [Math.min(b.minR, r), Math.min(b.minC, c),
       Math.max(b.maxR, r + dr * (entry.answer.length - 1)),
       Math.max(b.maxC, c + dc * (entry.answer.length - 1))];
    [b.minR, b.minC, b.maxR, b.maxC] = ranges;
  }
  function bestPosition(b, entry, rng) {
    if (!b.placed.length) {
      if (entry.answer.length > 23) return null;
      return { r: 0, c: 0, dir: rng() < 0.5 ? "across" : "down" };
    }
    const candidates = [];
    for (const [where, cell] of b.cells) {
      const [r, c] = where.split(",").map(Number);
      for (let i = 0; i < entry.answer.length; i++) {
        if (cell.ch !== entry.answer[i]) continue;
        for (const dir of ["across", "down"]) {
          const rr = r - (dir === "down" ? i : 0);
          const cc = c - (dir === "across" ? i : 0);
          const result = check(b, entry.answer, rr, cc, dir);
          if (!result) continue;
          candidates.push({ r: rr, c: cc, dir,
            score: result.crosses * 35 - result.area * 0.12 -
              Math.abs(result.rows - result.cols) * 0.5 + rng() * 9 });
        }
      }
    }
    if (!candidates.length) return null;
    candidates.sort((a, b) => b.score - a.score);
    return candidates[0];
  }
  function normalize(b) {
    const rows = b.maxR - b.minR + 1, cols = b.maxC - b.minC + 1;
    const cells = Array.from({ length: rows }, () => Array(cols).fill(null));
    for (const [pos, cell] of b.cells) {
      const [r, c] = pos.split(",").map(Number);
      cells[r - b.minR][c - b.minC] = cell.ch;
    }
    const placed = b.placed.map(p => ({
      entry: p.entry, row: p.row - b.minR, col: p.col - b.minC,
      direction: p.direction
    }));
    const numbers = new Map();
    Array.from(new Set(placed.map(p => key(p.row, p.col))))
      .map(s => s.split(",").map(Number)).sort((a, b) => a[0] - b[0] || a[1] - b[1])
      .forEach(([r, c], i) => numbers.set(key(r, c), i + 1));
    for (const p of placed) p.number = numbers.get(key(p.row, p.col));
    const crossings = Array.from(b.cells.values()).filter(c => c.dirs.size > 1).length;
    const score = placed.length * 15 + crossings * 8 -
      rows * cols * 0.03;
    return { cells, placed, rows, cols, score,
      crosses: crossings,
      signature: placed.map(p => p.entry.answer + ":" + p.row + "," + p.col +
        p.direction).sort().join("|") };
  }
  function buildLayout(ordered, maxWords, rng) {
    const b = board();
    for (const entry of ordered) {
      if (b.placed.length >= maxWords) break;
      if (entry.answer.length > 25) continue;
      const at = bestPosition(b, entry, rng);
      if (at) insert(b, entry, at.r, at.c, at.dir);
    }
    return b.placed.length >= 5 ? normalize(b) : null;
  }
  function createCandidates(rows, scope, moduleNumber, lessonNumber, seed = 1,
                            maxWords = 18, effort = 90) {
    const { primary, loans } = poolFor(rows, scope, moduleNumber, lessonNumber);
    const rand = random(Number(seed) || 1), winners = [], unique = new Set();
    maxWords = Math.max(6, Math.min(24, Number(maxWords) || 18));
    effort = Math.max(10, Math.min(160, Number(effort) || 90));
    for (let trial = 0; trial < effort; trial++) {
      const ordered = primary.map(q => ({ q, t: rand() }))
        .sort((a, b) => a.q.priority - b.q.priority ||
          a.t - b.t).map(item => item.q);
      // Borrow earlier-lesson terms only when the selected lesson needs them.
      if (scope === "lesson") ordered.push(...loans);
      const layout = buildLayout(ordered, maxWords, rand);
      if (!layout || unique.has(layout.signature)) continue;
      if (layout.placed.filter(p => primary.includes(p.entry)).length < 4) continue;
      unique.add(layout.signature);
      const shape = Math.abs(layout.cols - layout.rows);
      layout.score -= shape * 1.3;
      winners.push(layout);
      winners.sort((a, b) => b.score - a.score);
      if (winners.length > 5) winners.pop();
    }
    if (!winners.length) throw new Error("Not enough intersecting answers yet. Try a wider selection.");
    return winners;
  }
  function validateLayout(layout) {
    const b = board();
    for (const p of layout.placed) {
      if (b.placed.length && !check(b, p.entry.answer, p.row, p.col, p.direction)) {
        throw new Error("Invalid crossword crossing.");
      }
      insert(b, p.entry, p.row, p.col, p.direction);
    }
    const reconstructed = normalize(b);
    if (reconstructed.cells.flat().filter(Boolean).length !==
        layout.cells.flat().filter(Boolean).length) throw new Error("Invalid grid.");
    return true;
  }
  const api = { poolFor, createCandidates, validateLayout, random };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (root) root.FNDCrosswordCore = api;
})(typeof window === "undefined" ? null : window);
