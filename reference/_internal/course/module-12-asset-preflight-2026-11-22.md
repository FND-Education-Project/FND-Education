# Module 12 — image, colouring and crossword asset preflight (November 22, 2026)

**PR:** [#210](https://github.com/FND-Education-Project/FND-Education/pull/210), branch `editorial/module-12-psychological-treatment-handoff-20261117`.  
**Original preflight baseline:** `f6b33e8919032b79a87723a1876363c272560ef2` on November 22, 2026.  
**Corrected current finding:** **All original Module 12 images, colouring books and crossword files were already present on newer `main`; the initial missing-asset conclusion was wrong because it used an outdated main commit and a Module 12 branch that had not yet synchronized.** The project lead correctly identified merged [image and colouring PR #211](https://github.com/FND-Education-Project/FND-Education/pull/211). Current `main` also contains four Module 12 crossword sets.

This report corrects and supersedes the original saved version. The original audit believed the files were missing from the repository; **they were only missing from the unsynchronized PR branch**. No separate upload from the project lead is needed.

## Completed integration on Module 12 PR #210

**Branch synchronization:** Safely merged current `main` commit `6e0943b14feba03f86292d29c12f7e41ca39d31c` into the existing Module 12 branch with two-parent merge commit `4c8976d593561fa3f9b7dc58cbf86f6b3286ff76`. The two branches had **zero overlapping changed paths**, so all Module 12 narrative and audit changes could be overlaid without discarding Module 11 or the already merged binary assets. PR #210 itself **was not merged**.

**Approved colour illustrations:**

| Lesson | Embedded illustration and exact original PNG | Owner-approved figure text | Status |
|---|---|---|---|
| 36 — Nadia | `assets/images/lesson-36-illustration.png` after her appointment | A: “Nadia leaves with her questions unanswered—but they're still hers to ask.” | Present; original figure placement, caption and alt preserved |
| 37 — Graham | `assets/images/lesson-37-illustration.png` after the unsent park message | A: “Graham considers one small step toward enjoying the park again.” | Present; original figure placement, caption and alt preserved |
| 38 — Callum | `assets/images/lesson-38-illustration.png` during therapy conversation about the phone | A: “Callum explains why his phone matters, helping his psychologist reconsider the exercise.” | Present; original figure placement, caption and alt preserved |

All three approved PNGs were inherited from merged PR #211. **Original PNG pixel fidelity to the approved alt descriptions was not visually inspected**: the connected GitHub file content provider returned the Git blob SHA but empty binary image content for these large PNGs. Do not claim image-to-alt visual acceptance until a renderer or image inspection can view the pixels.

**Colouring books:** Exact existing files from PR #211 are present and now linked in Lessons 36–38. Each lesson has a printable PDF `assets/puzzles/colouring/lesson-N-coloring-book.pdf` and its PNG thumbnail `assets/puzzles/colouring/lesson-N-coloring-book.png`. The optional activity after the Person reflection links the PDF, displays the thumbnail and offers the puzzle-browser collection.

**Crosswords:** Four sets (Lessons 36, 37 and 38, plus Module 12 review) already exist on merged `main`. Each includes **Easy, Normal, Answer Key PDF** and `*-sources.json`, for **16 existing files**. New accurate grid-outline SVG previews were generated from the included word coordinates in the uploaded `*-sources.json` records (without revealing filled answers), named `assets/puzzles/thumbnails/*-m12-*-normal.svg`. Lessons 36–38 now offer previews, puzzle-browser navigation and the three PDF download choices. The Module 12 overview links its review crossword.

**Puzzle-browser integration:** The shared `assets/puzzles/catalog.json` includes exactly **seven Module 12 entries** (three lesson crossword, three lesson colouring, one module review crossword) **without deleting the seven Module 10 or seven Module 11 entries**. Updated `assets/puzzles/README.md` fallback to include Lesson 36–38 crossword and colouring links and the Module 12 review, plus jump navigation and thumbnails.

## Checks, limits and publication gate

**Structurally checked:** Exact PR branch blob-path presence, original figure markup and location, lesson activity references, PDF source-manifest files, new grid-preview SVG markup, browser-catalogue record counts and retained earlier-module items. Confirm that all referenced internal PDF/PNG/SVG files exist on the final branch head; re-run any check after later source changes.

**Still requires Work Audit 2:** Actual visual examination of original colour PNG contents and alt-text fidelity, colouring-book PDF legibility, real crossword PDF layout, correspondence of clues/answers and answer keys, screen-reader and mobile layout, actual live site routing/links, curriculum/navigation/source checks and exact-head GitHub CI. A correct Git path is **not** equivalent to a rendered or accessibility-approved page. Do not mark original medical or community sources verified by these file checks.

**Final status:** **Module 12 files are now present and the requested asset links/catalogue integration are committed to PR #210; no missing-asset publication blocker remains.** The initial false finding is closed. The separate **visual/technical checks and Work Audit 2 remain pending**, and PR #210 remains draft and unmerged.
