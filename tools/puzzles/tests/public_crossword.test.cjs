"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const core = require("../../../web/assets/js/crossword-core.js");
const pdf = require("../../../web/assets/js/crossword-pdf.js");

const words = [
  ["BRAIN", "Part of the nervous system inside the head", 1, 1, 1],
  ["NERVE", "Carries body messages", 1, 2, 1],
  ["BODY", "The physical part of a person", 1, 3, 1],
  ["CARE", "Support provided to another person", 2, 1, 1],
  ["PAIN", "An unpleasant body sensation", 2, 2, 1],
  ["REST", "A break from activity", 2, 3, 1],
  ["CALM", "Less tense or worried", 2, 4, 1],
  ["HELP", "Support you can ask for", 2, 5, 1],
  ["MOOD", "How someone feels emotionally", 2, 6, 1],
  ["FLARE", "Temporary rise in symptoms", 2, 7, 1],
  ["TIC", "Brief involuntary movement or sound", 2, 1, 2],
  ["SIGNS", "Clues a clinician looks for", 2, 2, 2],
  ["TEST", "A clinical examination or check", 2, 3, 2],
  ["VOICE", "Speech and sound production", 2, 4, 2],
  ["SLEEP", "A period of nightly rest", 2, 5, 2],
  ["FEEL", "Notice a sensation", 2, 6, 2]
].map(([answer, clue, priority, lesson, module]) => ({
  answer, display_answer: answer, clue, priority, lesson, module
}));

test("lesson borrows only from earlier lessons, not future lessons", () => {
  const selected = core.poolFor(words, "lesson", 1, 3);
  assert.equal(selected.primary[0].answer, "BODY");
  assert.ok(selected.loans.every(q => q.module < 1 || q.lesson < 3));
  assert.ok(!selected.loans.some(q => q.lesson > 3));
});

test("one clue per answer, with higher priority kept", () => {
  const extra = { ...words[0], priority: 3, clue: "Wrong duplicate" };
  const selected = core.poolFor([...words, extra], "module", 1);
  assert.equal(selected.primary.filter(q => q.answer === "BRAIN").length, 1);
  assert.equal(selected.primary.find(q => q.answer === "BRAIN").clue, words[0].clue);
});

test("grid generator makes reproducible, legally intersecting candidates", () => {
  const a = core.createCandidates(words, "all", 1, 1, 28, 11, 45);
  const b = core.createCandidates(words, "all", 1, 1, 28, 11, 45);
  assert.ok(a.length >= 1 && a.length <= 5);
  assert.deepEqual(a.map(p => p.signature), b.map(p => p.signature));
  for (const layout of a) {
    assert.ok(layout.placed.length >= 5);
    assert.ok(layout.rows <= 23 && layout.cols <= 32);
    assert.ok(core.validateLayout(layout));
  }
});

test("Normal, Easy, and Answer Key PDF are self-contained one-page downloads", () => {
  const layout = core.createCandidates(words, "all", 1, 1, 1, 8, 75)
    .find(candidate => {
      try { pdf.plan(candidate, "easy", "FND review"); return true; }
      catch { return false; }
    });
  assert.ok(layout, "At least one sample layout must be printable");
  for (const edition of ["normal", "easy", "key"]) {
    const bytes = pdf.makePdf(layout, "FND review", edition);
    const content = Buffer.from(bytes).toString("latin1");
    assert.ok(content.startsWith("%PDF-1.4"));
    assert.ok(content.includes("/Type /Page"));
    assert.ok(content.includes("xref\n0 7\n"));
    assert.ok(content.includes("%%EOF"));
    assert.ok(content.includes("FND review"));
    assert.ok(bytes.length > 300);
  }
});

test("unsafe title symbols are escaped and overlong titles rejected", () => {
  assert.equal(pdf.ascii("Care — recovery"), "Care - recovery");
  assert.ok(pdf.wrap("Short clue for a crossword", 150, 12).length >= 1);
  const layout = core.createCandidates(words, "all", 1, 1, 4, 7, 30)[0];
  assert.throws(() => pdf.plan(layout, "easy", "X".repeat(100)), /shorten/);
});
