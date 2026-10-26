> **Superseded plan — October 26, 2026:** The project lead explicitly chose one 19-module/57-lesson course, with the 34 superseded source lessons removed. No live learner-progress history needs to be preserved: only test accounts exist. The legacy 75-ID migration/rollback procedures below are retained for historical research, **not** active rollout instructions. Instead, reconcile account PR #154 with the canonical course and explicitly clear the test-only `learner_progress` rows and `learners.last_lesson` values before deploying the new 57-ID Worker. The public account interface remains disabled. See updated PR #191 and #154 descriptions.

# Curriculum redesign — learner-state and publication migration plan

**Current release scope:** Robert subsequently authorized publication-readiness work so PR #191 can publish automatically generated working lessons before human authoring. The [publication audit](prepublication-audit-191-2026-10-26.md) supersedes earlier planning-only gates for this release. Original routes and progress identity are preserved; no D1 migration or account-service rollout is included.

**Planning only — October 26, 2026.** This document authorizes no D1 query/write, deployment, public renumbering or account change. It accompanies [PR #191](https://github.com/FND-Education-Project/FND-Education/pull/191).

## Verified source snapshots

- Main/content baseline: `e1d9f85521561fc427a5795f088c7996ce1924b8`.
- Curriculum PR reviewed: `0a01e73bbc071c3f68e79e2565f9792cbe13165c`.
- Account implementation inspected read-only: [draft PR #154](https://github.com/FND-Education-Project/FND-Education/pull/154), head `23aa1a2680201130c636f4b1c28aeae7c482d2d5`, branch `feature/local-course-progress`. It is open, unmerged and currently conflicts with main.
- These are repository snapshots, **not a verified description of the deployed Worker or D1**. Obtain the deployed version/schema and an owner-controlled backup before any future release.

The [planning inventory](syllabus-redesign-identity-map-2026-10-26.json) records all **75 current source lessons**, their paths/URLs and the account branch's corresponding key, plus **16 proposed new lessons**. It is internal data for review; no application reads it.

## Current identifiers and collision

| Surface in account PR #154 | Observed contract | Migration consequence |
|---|---|---|
| `tools/site/prepare_site.py`, `write_course_progress_manifest` | Manifest version 1; lesson ID is `m{module_number}-{lesson_number}`. The second number is the **module-local filename number**. | Overall labels such as “Lesson 15” are not `m6-15`. Moving/renumbering folders currently changes generated identity even if content stays the same. |
| `tools/learner-cloudflare/schema.sql` | `learner_progress` primary key is `(learner_id, lesson_id)`, with independent `visited`, `completed` and `updated_at`. | Names/labels cannot safely stand in for durable content identity. Preserve both status flags and provenance. |
| `learners.last_lesson` | One stored lesson key, returned as `lastLesson`. | Resume position also needs a curriculum-aware plan. Do not accidentally resume a different topic with the same numbers. |
| `worker.js`, `validLesson` | Numeric regex restricted to modules 1–23 and a hardcoded per-module count array. | A new namespace needs coordinated API validation; changing only generated HTML/JSON is insufficient. Do not weaken to arbitrary user-supplied IDs. |
| `course-progress.js` | Client checks the numeric ID format and manifest `version === 1`; it filters progress using known keys. | New IDs/revisions require an explicit client/manifest contract. Otherwise history can disappear from view or be assigned to new content. |
| Progress endpoints | Server chooses the learner from the authenticated session; completion requires CSRF, confirmation and active username. Opening records Visited only. | Preserve account isolation, confirmation semantics, readable guest/offline pages, preferences and accessible focus. |
| Current public routes | `/course/m6/1/`, for example, already represents a seizure lesson. | Do not reuse that URL/key for new attention teaching. A redirect to unrelated content is not preservation. |

**Example:** a completed legacy `m6-1` must never make the new attention lesson appear completed. Preserve the legacy seizure record. Give attention teaching a fresh identity and show it as not started until the learner acts.

### Cross-PR mismatch already present

Main has **75 focused lessons**; the account snapshot's allowlist totals **74**. Module 4 now has two source lessons, but the account array still permits only one. Thus `m4-2` would be rejected by that server validator if the snapshots were combined without reconciliation. This is a source-contract finding, not a claim that a live learner lost progress.

Rebase/reconcile the account implementation against current content **in its own authorized PR**, regenerate its manifest, and validate client/server agreement before curriculum migration. Do not copy that runtime code into this documentation branch. Do not combine independent account-feature rollout with curriculum release implicitly.

## Proposed identity and completion policy

Use durable **content identity**, curriculum position, route and display lesson number as separate fields. The exact new ID syntax/schema is a future implementation decision; inventory `plan_key` values are planning handles, not accepted API IDs.

1. **Foundations 1–5:** keep source content, URLs and existing identity. Preserve progress exactly, including separately reconciling `m4-2`.
2. **Retained later modules:** for unchanged content from legacy 13 and 16–23, retain the same identity even when its module display position changes. A display-number change alone must not clear completion.
3. **New concepts and navigation lessons:** create fresh identities; never reuse keys from legacy 6–12. No transfer just because numbers or a few concepts overlap.
4. **Reworked rehabilitation/pacing:** old 14–15 lessons are candidates for proposed 25–30, but all six transfers remain **on hold** until human content-equivalence review. A materially new/split lesson starts uncompleted. If a genuinely unchanged lesson is only relocated, retain its original identity; document that decision.
5. **Superseded symptom-course material:** preserve all 28 lesson records and reading pages as legacy history. Link each to current relevant reading after editorial review. Reading old material does not silently complete a new synthesis lesson.
6. **Unexpected stored keys:** retain/export for reconciliation; do not delete unknown rows because the latest manifest lacks them.
7. **Undo and timestamps:** preserve both independent status flags, timestamps and intentional removal of completion. Do not rerun a migration that re-completes a lesson after the learner undoes it.
8. **Account ownership:** no translation by username, email or browser storage. All projection/migration remains scoped to the authenticated internal learner ID.
9. **Resume:** retain a legacy resume key until a reviewed destination is known. Offer a clearly labelled legacy-reading route or new-course start; do not guess that equivalent ordinal means equivalent content.
10. **Partial work:** only Visited/Completed exist now. Preserve those distinctions; do not invent percentages, section-level completion or prior quiz results.

Prefer preserving original rows and recording a reviewed, versioned identity/alias history over destructive bulk renumbering. Any approved derived completion needs origin, revision and idempotence tracking so rollback and a learner's later changes are respected. Decide how per-curriculum resume cursors work before adding a second course revision; today's single `last_lesson` field is not sufficient by assumption.

## URL, search and asset preservation

New teaching must not take over the old semantic URL space. A versioned route namespace such as `/course/v2/...` is a **candidate**, not an approved public path. Final route selection and any changes to foundations' entry points need review.

- Preserve exact old route and fragment inventories, including audience/share IDs, before editing. Retain a legacy page where no one-to-one semantic replacement exists.
- Use redirects only for an equivalent destination. Static hosting cannot choose a different page based on an old fragment sent only to the browser; keep needed anchor IDs at a compatible destination or retain the old page.
- Regenerate sequence navigation, breadcrumbs, course landing, module selectors, Pagefind metadata, canonical URLs, schemas and sitemap together. Never point a “next lesson” action into a new unrelated legacy slot.
- Freeze existing PDFs, thumbnails and source filenames. Asset names use **overall lesson labels**, not the account's module-local key. Example: `assets/puzzles/crosswords/Module-4-Lesson-11/building-and-using-your-symptom-map-m4-11-sources.json` records selection module 4 / lesson 11; the corresponding course/account slot is `m4-2`.
- Audit workbook Module/Lesson columns, JSON `selection` and included-item provenance, PDF title text/form tab order, image/caption/alt text, colouring links and puzzle selectors. A filename rename alone does not revise what a PDF teaches.
- Keep community quote provenance and human authorship notices with their content. Do not bulk relabel or copy symptom-specific teaching into Reference without its own content review.
- Redirects, legacy pages and route counts are separate from the **57 proposed core focused lessons**; do not set production total-route checks from that number.

## Unique-content review before retiring old lessons

| Legacy modules | Owner after reorganization; review what is unique before moving |
|---|---|
| 6: episodes | Module 5 for concise safety links; seizure/episode Reference for full event care. Preserve uncertainty, witness descriptions and recovery costs. |
| 7: movement | New 6/9 for general concepts; symptom Reference for specific examinations, techniques and aids. |
| 8: sensory/visual/balance | New 8 for descriptive routing; new 13 for access; relevant Reference for clinical distinctions. |
| 9: speech/voice/swallowing/breathing | New 13 for communication access; specialist Reference for airway/swallowing assessment and techniques. |
| 10: cognition/dissociation | New 7/8 for appropriate concepts/descriptions; new 13–14 for memory supports and shared history; FCD/dissociation Reference. |
| 11: pain/migraine/fatigue/sleep | New 8/10/11 for navigation, capacity and care coordination; co-occurring Reference for condition-specific detail. |
| 12: autonomic/whole body | New 7 for limited arousal concepts; new 8/10/11 and appropriate medical Reference for assessment and support. |

These are ownership proposals. No unique material is marked deleted or already migrated.

## Staged release and rollback gates

**A — Evidence and content:** human-edit all required audience sections, review meaningful scientific claims, approve source-use records and glossary links, then approve a one-to-one/split/new-content map. This PR stops before that publication work.

**B — Reconcile contracts in isolation:** inspect actual deployed/schema/client versions with owner authorization, reconcile #154 with the 75-lesson source, introduce durable IDs and a shared reviewed allowlist/manifest, and plan old-client behavior. No sensitive production data belongs in Git or logs.

**C — Dry run on synthetic or securely handled staging data:** include account A/B with different progress/themes; old keys (especially `m6-1`, `m14-1`, `m4-2`); independent Visited/Completed flags; unknown keys; legacy resume; disabled account API; export/reset/deletion. Prove idempotence and rollback. Verify migrations do not transfer completion to new content, leak identities, or join learner data to analytics or the separate symptom app.

**D — Two-account browser acceptance before any release:** sign in as A, change one completion and theme, refresh; sign out; sign in as B with different records; repeat refresh and sign-out/in. Verify B never sees A's history or confirmation name, preferences take effect, new lessons remain uncompleted, unchanged lessons retain status, legacy material remains findable, and resume does not cross topics. Test touch/keyboard focus, failure/retry/offline states and export/deletion. Existing author-reported tests are useful history, not acceptance for a new migration.

**E — Separately approved deployment:** record owner-reviewed backups, versioned manifests/content map, migration checkpoint and rollback procedure; preserve production history. Rollback must restore matching client/Worker/content contracts without discarding progress recorded during the new release. An old binary may reject new IDs: do not “roll back” by deploying it without a compatible preservation/read strategy.

## What has been tested here

Current source preparation and validation pass at 429 routes; identity inventory is checked against both Git snapshots. The untouched #154 code's **34 offline tests** pass using SQLite and mocked identity/email services. One additional review-only synthetic A/B test passed using the same unchanged Worker and in-memory fixture: account-specific progress and themes survived repeated reads/logout/re-authentication; wrong-account confirmation and CSRF failed; `m4-2` and unimplemented planning IDs were rejected as expected. No migration code exists yet, no live D1 or provider login was exercised, and no real messages were sent. This is not a deployment or security certification.

