/* Downloadable one-page, letter-size, selectable-text crossword PDFs.
 * No external PDF service or third-party library. PDF values are escaped.
 */
(function (root) {
  "use strict";
  const W = 612, H = 792, M = 34;
  function ascii(s) {
    return String(s).normalize("NFKD")
      .replace(/[\u2018\u2019]/g, "'").replace(/[\u201C\u201D]/g, '"')
      .replace(/[\u2013\u2014]/g, "-").replace(/\u2026/g, "...")
      .replace(/[^\x20-\x7E]/g, "").replace(/\s+/g, " ").trim();
  }
  const escapePdf = s => ascii(s).replace(/\\/g, "\\\\").replace(/\(/g, "\\(")
    .replace(/\)/g, "\\)");
  const fmt = n => Number(n.toFixed(2)).toString();
  function measure(text, size, bold) {
    // Conservative estimate used for wrapping without an external font package.
    return Array.from(ascii(text)).reduce((n, c) =>
      n + size * (/[il.,:'!| ]/.test(c) ? 0.28 :
        /[MW@#]/.test(c) ? 0.85 : 0.54), 0) * (bold ? 1.03 : 1);
  }
  function wrap(text, width, size, bold = false) {
    const words = ascii(text).split(/\s+/).filter(Boolean), lines = [];
    let line = "";
    for (const word of words) {
      if (measure(word, size, bold) > width) {
        throw new Error("Clue contains a word too long for a readable PDF.");
      }
      const candidate = line ? line + " " + word : word;
      if (measure(candidate, size, bold) <= width) line = candidate;
      else { if (line) lines.push(line); line = word; }
    }
    if (line) lines.push(line);
    return lines;
  }
  function plan(layout, edition, title) {
    title = ascii(title).slice(0, 100);
    if (!title || measure(title, 15, true) > W - M * 2) {
      throw new Error("Please shorten the puzzle title to fit one line.");
    }
    const square = Math.min(16, (W - M * 2) / layout.cols, 370 / layout.rows);
    if (square < 14) throw new Error("The grid is too large. Try fewer answers.");
    const gridTop = 59, gridBottom = gridTop + layout.rows * square;
    const bankText = layout.placed.map(p =>
      p.entry.display_answer || p.entry.answer).sort((a, b) => a.localeCompare(b))
      .join("   |   ");
    const bankLines = edition === "easy" ? wrap(bankText, W - M * 2, 9.5) : [];
    const bankStart = edition === "easy" ? H - M - 19 - bankLines.length * 12 : H - M;
    const cols = { across: [], down: [] };
    for (const d of ["across", "down"]) {
      const list = layout.placed.filter(p => p.direction === d)
        .sort((a, b) => a.number - b.number);
      cols[d].push({ text: d === "across" ? "Across" : "Down", bold: true });
      for (const p of list) {
        const lines = wrap(p.number + ". " + p.entry.clue, 255, 12);
        cols[d].push(...lines.map(text => ({ text, bold: false })));
        cols[d].push({ text: "", bold: false });
      }
    }
    const start = gridBottom + 20, lineH = 15.2;
    const available = bankStart - start - 10;
    const taller = Math.max(cols.across.length, cols.down.length) * lineH;
    if (available < taller) {
      throw new Error("Clues cannot fit at 12 pt on one page. Try fewer answers or another layout.");
    }
    return { square, gridTop, gridBottom, start, cols, bankLines,
      bankStart, title };
  }
  function makePdf(layout, title, edition) {
    if (!["normal", "easy", "key"].includes(edition)) {
      throw new Error("Unknown crossword edition.");
    }
    const p = plan(layout, edition, title);
    const draw = [];
    const cmd = s => draw.push(s);
    function stroke(gray, width = 0.5) {
      cmd(fmt(gray) + " G " + fmt(width) + " w");
    }
    function rect(x, top, w, h, gray = 0.1, weight = 0.4) {
      stroke(gray, weight);
      cmd([fmt(x), fmt(H - top - h), fmt(w), fmt(h), "re S"].join(" "));
    }
    function dot(x, top) {
      cmd("0.76 g " + fmt(x) + " " + fmt(H - top) + " 0.58 0 360 arc f");
    }
    function text(s, x, top, size = 12, bold = false, gray = 0) {
      if (!ascii(s)) return;
      cmd(fmt(gray) + " g BT /" + (bold ? "F2" : "F1") + " " +
        fmt(size) + " Tf " + fmt(x) + " " + fmt(H - top - size) +
        " Td (" + escapePdf(s) + ") Tj ET");
    }
    // Decorative dots in inactive cells are small filled rectangles; no solid
    // black cell backgrounds, so the puzzle is economical to print.
    text(p.title, M, 22, 15, true);
    text("FND EDUCATION PROJECT  |  " + edition.toUpperCase(), M, 43, 8, false, 0.4);
    const gx = (W - layout.cols * p.square) / 2;
    const numbers = new Map(layout.placed.map(item =>
      [item.row + "," + item.col, item.number]));
    for (let r = 0; r < layout.rows; r++) {
      for (let c = 0; c < layout.cols; c++) {
        const x = gx + c * p.square, y = p.gridTop + r * p.square;
        rect(x, y, p.square, p.square, layout.cells[r][c] ? 0.1 : 0.74, 0.32);
        if (layout.cells[r][c]) {
          const number = numbers.get(r + "," + c);
          if (number) text(number, x + 1.2, y + 0.7, 5.5);
          if (edition === "key") text(layout.cells[r][c],
            x + p.square / 2 - 3.4, y + p.square / 2 - 5.3, 10, true);
        } else {
          for (const n of [4, 8, 12]) {
            const xx = x + p.square * n / 16;
            const yy = y + p.square * n / 16;
            cmd("0.68 g " + fmt(xx) + " " + fmt(H - yy) + " 0.55 0.55 re f");
          }
        }
      }
    }
    for (const [direction, x] of [["across", M], ["down", W / 2 + 12]]) {
      let y = p.start;
      for (const line of p.cols[direction]) {
        text(line.text, x, y, line.bold ? 13 : 12, line.bold);
        y += 15.2;
      }
    }
    if (edition === "easy") {
      stroke(0.4, 0.6);
      cmd(fmt(M) + " " + fmt(H - p.bankStart - 4) + " m " +
        fmt(W - M) + " " + fmt(H - p.bankStart - 4) + " l S");
      text("Word bank", M, p.bankStart + 3, 10, true);
      p.bankLines.forEach((line, index) => {
        text(line, M, p.bankStart + 17 + index * 12, 9.5);
      });
    }
    text("Free educational activity  |  fndeducationproject.org", M, H - 19, 8, false, 0.5);
    // Minimal, standards-compliant vector/text PDF with xref byte offsets.
    // The stream only emits ASCII (Latin text is transliterated above).
    const content = draw.join("\n") + "\n";
    const objects = [
      "<< /Type /Catalog /Pages 2 0 R >>",
      "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
      "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>",
      "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
      "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>",
      "<< /Length " + content.length + " >>\nstream\n" + content + "endstream"
    ];
    let output = "%PDF-1.4\n", offsets = [0];
    for (let i = 0; i < objects.length; i++) {
      offsets.push(output.length);
      output += (i + 1) + " 0 obj\n" + objects[i] + "\nendobj\n";
    }
    const start = output.length;
    output += "xref\n0 " + (objects.length + 1) + "\n0000000000 65535 f \n";
    for (let i = 1; i < offsets.length; i++) {
      output += String(offsets[i]).padStart(10, "0") + " 00000 n \n";
    }
    output += "trailer\n<< /Size " + (objects.length + 1) + " /Root 1 0 R >>\n";
    output += "startxref\n" + start + "\n%%EOF\n";
    return Uint8Array.from(output, c => c.charCodeAt(0));
  }
  const api = { makePdf, plan, wrap, ascii };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (root) root.FNDCrosswordPdf = api;
})(typeof window === "undefined" ? null : window);
