# FND Education Project — Crossword Clue Authoring Standard

**Status:** Internal editorial guidance, November 7, 2026.  
**Applies to:** New crossword clue-and-answer banks for course lessons.  
**Primary source:** The lesson's **For the Person With FND** section, not the clinician or supporter section.

> **Purpose:** Create engaging, accessible crossword *candidate banks*. This document governs what to write and how to review it, not PDF layout or publication. For finished puzzles, also follow [the separate print and accessibility standard](../../../tools/puzzles/CROSSWORD_FORMATTING.md).

## 1. Sources and context

1. Read the person-facing lesson text before drafting. Find its main teaching ideas, useful vocabulary, and familiar everyday experiences. Give the core teaching ideas priority over incidental objects, names, or anecdotes.
2. Inspect the master question bank, normally `tools/puzzles/FND_Crossword_Question_Bank_Template.xlsx` (or the current master workbook supplied by the project lead), **before** generating new entries. Check earlier *clues*, *answers*, and concepts across lessons/modules; avoid recycling them or changing a few words to disguise a repeat.
3. When an original and project-lead-edited set are both available, compare them first. Treat human edits as the preferred style reference: shorter answers when useful, clearer clue wording, fewer abstract terms, and removal of repetitive or weak entries. Infer preferences carefully; do not treat every individual edit as a universal prohibition.
4. Refer to the repository lesson as the source of educational content. The crossword should **not** depend on the reader seeing the lesson first.

## 2. Clue voice and solvability

- Keep clues short, conversational, and naturally phrased. **Usually aim for 3–10 words**, but never cut a necessary word merely to satisfy a count.
- Make around **one-third** playful, witty, or lightly humorous when good material allows. Use familiar expressions, clever associations, gentle misdirection, and everyday language. Wit must not become cryptic or unfair. Avoid humour at the expense of people with FND.
- Mix direct definitions, relatable situations, associations, and playful clues. Avoid producing 35 variations of the same sentence form.
- Every clue must be **independently solvable** without the lesson, an image, a named character, an earlier clue, or specific course terminology that is not explained within the clue.
- Avoid vague prompts with many plausible answers, circular clues that merely repeat the answer, and 'what is the word for' quiz language. Test whether another reasonable answer would fit; rewrite when ambiguity is excessive.
- Prefer recognizable words and plain language. Include necessary clinical terms **when the lesson teaches them**, but ensure clues are accurate, fair, and accessible.
- Preserve a respectful, hopeful, non-stigmatizing tone. Do not imply FND symptoms are feigned, voluntary, or always caused by psychological factors; do not turn a simplified clue into a medical claim.
- Do not use answer-length notation or additional commentary inside the clue cells unless the puzzle workflow explicitly requires it.

**Examples (illustrative, not a reusable clue bank):**
- Avoid: `What Natalie learns in the basketball scene` — requires lesson-specific context.
- Better: `The brain's best guess about what comes next` → `PREDICTION`.
- Playful: `A brain forecast without a weather app` → `PREDICTION`.
- Avoid: `What helps when things are hard?` — vague, too many plausible answers.

When two possible clues have similar educational value, prefer the one that gives the solver a satisfying “Of course!” moment.

## 3. Answer selection and lengths

Unless the project lead requests otherwise, draft **35 candidate clue–answer pairs per lesson**:

| Length after removing spaces/hyphens | Per lesson |
| --- | ---: |
| 3–6 letters | 20 |
| 7–9 letters | 11 |
| 10 or more letters | 4 |
| **Total** | **35** |

- These are **candidate-bank targets**, not a requirement that all 35 appear in the final printed crossword. The crossword generator selects a workable subset; do not silently rewrite approved clue wording to force a grid layout.
- Prefer simple, familiar **single words**. A multiword or hyphenated answer is acceptable only when natural, informative, and supported by the puzzle builder.
- Use uppercase Latin A–Z letters for answer entries; the generator strips spaces and hyphens. Avoid punctuation, numbers, obscure abbreviations, and unnatural spellings. Do not introduce two answers that normalize to the same sequence of letters.
- Short answers must earn their place with relevance or enjoyable clue quality; **do not add filler merely to meet the short-word quota**. If a lesson cannot fairly support the exact balance, report the shortage rather than manufacture poor clues.
- Distribute clues across the lesson's main ideas, not just its first paragraph or most visible symptom.
- Preserve important longer terms even if the answer-length targets need a small, explicitly reported exception.

## 4. Priorities

Use numeric priorities consistently:
- **1 — Essential:** Primary teaching concepts, useful vocabulary, or unusually strong accessible clues.
- **2 — Good:** Relevant supporting concepts, familiar experiences, and enjoyable clues.
- **3 — Optional:** Less central material, alternate words, or entries the puzzle builder can drop first.

Avoid assigning priority 1 to every entry; the distinction should help select a meaningful final puzzle.

## 5. Workbook structure and delivery

Produce **one XLSX workbook per requested module**, with **one worksheet** containing all its lessons and **exactly these five columns in order**:

`clue | answer | priority | lesson | module`

- Use lowercase header names above; place **one clue–answer pair per row**.
- Use uppercase answers, numeric priority values (1–3), and numeric lesson/module numbers.
- Keep rows logically grouped by lesson, with no decorative headers, merged cells, narrative rows, or empty separators that could interfere with the puzzle builder.
- The workbook must open cleanly in Excel and be compatible with `tools/puzzles/crossword_builder/core.py`.
- Deliver the generated workbook for project-lead review. Do not overwrite the master question bank or publish puzzles unless specifically asked.

## 6. Required editorial quality gate

Before handing over a workbook:

1. Re-read every clue without looking at its lesson: can a reader fairly solve it?
2. Check each clue's intended answer against other plausible answers. Repair vague, misleading, or overly obscure clues.
3. Eliminate duplicate answers within a lesson and repeated/near-repeated clues or concepts from earlier lessons and the master bank.
4. Check balance: core ideas, variety of clue styles, natural wit, and a spread of ordinary experiences instead of excessive jargon.
5. Check FND accuracy and person-first tone; no claim should exceed what the lesson supports.
6. Validate answer normalization, duplicate normalized answers, all five required columns, numeric fields, and correct lesson/module assignments.
7. Count entries and answer lengths **for each lesson**, not just the whole module; report any exceptions honestly.
8. Inspect for AI-like repetitive phrasing, awkward constructions, or filler. Replace them.

**Editorial principle:** A good crossword should feel thoughtfully edited by a human. The goal is recognition, reinforcement, and enjoyment—not a disguised examination of whether the reader memorized the lesson.
