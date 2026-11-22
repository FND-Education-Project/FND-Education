# Module 12 — image, colouring and crossword preflight (November 22, 2026)

**PR:** [#210](https://github.com/FND-Education-Project/FND-Education/pull/210) — `editorial/module-12-psychological-treatment-handoff-20261117`.  
**Reviewed head:** `f6b33e8919032b79a87723a1876363c272560ef2`.  
**Purpose:** Determine whether the lesson assets already exist, whether approved image placement/caption/alt text is present, and whether additional public links can be safely added **before** Chat Audit 1. This is an asset-presence and structural preflight, **not a successful rendering, PDF, image accessibility, independent clinical or Work source audit**.

## What exists in lesson content

| Lesson | Original colour figure already in approved Person scene | Owner-approved caption and alt | Referenced PNG | Raw PNG file at that path |
|---|---|---|---|---|
| 36 — Nadia | After the difficult psychological assessment, before “Two different questions” | **A:** “Nadia leaves with her questions unanswered—but they're still hers to ask.” Alt identifies wraparound rose-tinted glasses, brimmed hat, crumpled questions sheet | `assets/images/lesson-36-illustration.png` | **ABSENT** |
| 37 — Graham | After the unsent invitation/park discussion, before “What happens between appointments?” | **A:** “Graham considers one small step toward enjoying the park again.” Alt identifies Graham composing a message and imagining Lena/park | `assets/images/lesson-37-illustration.png` | **ABSENT** |
| 38 — Callum | During the therapy exercise, just after Callum describes why he needs his phone | **A:** “Callum explains why his phone matters, helping his psychologist reconsider the exercise.” Alt identifies Callum in the psychologist's office, reaching toward phone | `assets/images/lesson-38-illustration.png` | **ABSENT** |

**Assessment:** The **approved placement, captions and alt text are already committed in lesson Markdown**. They must be retained, not re-authored. However, the linked three PNG files are not present in the Git tree of PR #210, current `main`, or the other open editorial PR branches checked (course reflection #214, Module 13 #215). Until the original approved PNGs are available and checked visually, these three existing links remain **broken** and no pixel-to-alt fidelity claim is possible.

## Colouring books (three lessons)

- **Not in the available repository:** `assets/puzzles/colouring/lesson-36-coloring-book.pdf` and preview PNG, and the corresponding `lesson-37-` and `lesson-38-` pairs. These are **six missing binary files**, not just missing Markdown links.
- The established naming and placement convention from earlier modules is **Lesson N — Optional colouring activity** with a small responsive PNG preview opening the existing printable PDF. **Do not insert links to absent PDF or preview files.**
- Recover or upload the **previously approved line-art versions** of the three specific scene illustrations. Do not generate a substitute and treat it as author-approved. Check legibility, contrast, file content, thumbnail scaling and access descriptions before release.

## Crossword puzzles (Lessons 36–38 and Module 12 review)

- **Not in the available repository:** There are **no** `assets/puzzles/crosswords/Module-12-*` directories, Easy/Normal/Answer Key PDFs, `*-sources.json` records or Module 12 crossword thumbnails on PR #210, current `main`, or the other checked open PR branches. Thus neither the lesson crossword links nor the Module 12 review crossword can currently be completed.
- If a clue-and-answer worksheet exists in a **separate ChatGPT chat or offline workflow**, that is **not** proof the rendered puzzle PDFs have been uploaded. Require actual puzzle files and source manifests before linking.
- After the files arrive, add an **Optional crossword** section to each Person lesson using the site's established easy/normal/answer/thumbnail pattern, and link the Module 12 review from its overview. Check for correct crossword titles, answers, source JSON, Easy and Normal differences, working PDF downloads and no redundant/unmatched records.

## Gallery, branch and validation handoff

- Current `assets/puzzles/catalog.json` and puzzle gallery must **retain all approved preceding modules**, including Module 11 records, when Module 12 entries are added. Do not overwrite the shared catalogue from a stale branch.
- PR #210 was **4 commits behind** current `main` at preflight and is a stacked independent draft alongside PR #214's cross-course reflection changes. Before Work Audit 2 final validation, safely reconcile `main`, the separate reflection PR and the most recent live catalogue **without silently rewriting approved Person reflections or discarding source mappings**.
- **The Chat reviewer cannot upload absent original binary art/PDF files from GitHub text-only contents actions.** File presence is a real blocker. Do not invent a successful integration or issue new working sandbox links for files that are not present.
- **Work Audit 2:** verify every binary file and link after upload, visually compare approved captions and alt text with the actual images, inspect desktop/mobile presentation and accessibility where supported, audit source/page identities, run relevant validators, course-progress tests and CI, and report unavailable checks honestly.

**Result:** **Asset integration is not complete and cannot be certified on the current branch.** The original approved three image figures remain in the correct story locations, but their linked raw PNGs and all six colouring files and crossword files are missing. No public prose, image captions or alt text was modified during preflight. **Do not merge or deploy.**
