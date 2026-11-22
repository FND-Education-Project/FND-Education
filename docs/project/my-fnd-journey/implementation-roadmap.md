# Implementation roadmap, decision log and quality gates

**Status:** Planning only. Commit codes/assets in later targeted PRs. Maintain a documented no-recurring-fees budget; free tiers can change and have quotas, and are not a permanent price guarantee.

## Release slices

| Phase | Deliverable | Acceptance gate |
| --- | --- | --- |
| 0: Architecture spike | Isolated static app shell, IndexedDB, one existing PNG scene, two/three temporary sprites; proof of coordinate/zoom/list parity | Test portrait scroll, drag/tap, offscreen recovery, reload, offline. **No final artwork** |
| 1: Private core | Reviewed symptom catalogue, typeahead/custom symptoms, three-state check-in, journal, local persistence, deletion and export/backup | No health data network requests; local data survives safe updates; QA on shared-device mode |
| 2: Activity Room | Drawers, sprite placement/history, optional activity check-in, accessible list view, end-day/next-morning capacity reflections | Clutter allowed; no auto-cleanup, restrictions or inferred readiness claims |
| 3: Understand / communicate | Deterministic patterns with denominators, conservative journal suggestions, education links, previewable selective report/print | No unsupported medical conclusions; user chooses quoted note content |
| 4: Optional course link | Read existing progress, open actual next lesson, disconnect and clear deletion explanations | Only after draft PR #154 is deployed/tested; exact origin, cookie, CSRF and account A/B isolation verified |
| 5: Convenience / art | Four/five original PNG scenes, curated sprite packs/scale factors, optional reminder methods, UX refinement | Recheck screen reader, motion, low vision, low motor accuracy; no new recurring backend dependency |

Phase order is flexible, except do not ship personal health tracking without the privacy/backup/deletion foundations, and do not promise course linking before account API is safely live.

## Design choices: resolved versus open

**Agreed:**
- App first; installable PWA is preferred economical initial form.
- No user-role or reading-mode distinctions anywhere in app/login integration.
- Optional course progress link; app home opens next lesson if linked.
- Local-only personal records, opt-in reminders, no AI service required.
- Symptom dropdown/typeahead with reviewed synonyms and personal terms.
- Empty/unrecorded is not symptom absence.
- Drawers for outside, chores, rest/relax, social (male/female/neutral presentation choices), and optional positive supports.
- Activity sprites pre-coloured. Four or five background scenes later, using coordinate records and scale overrides. Clutter allowed.
- Portrait sideways scroll, zoom anchored at viewport center, overlapping z-order, partial clipping with guaranteed recovery route, selection outline, drag and tap/list alternatives.
- Capacity as an explained, glossary-linked **subjective** reflection; next-day check-in optionally offered.

**Proposed pending trial:** TypeScript/Vite/Web Components; separate GitHub Pages site/origin; per-scene normalizations and fallback sprite; shape of activity reflection prompts; default threshold for asking about room density; low-presence supportive shelf; explicit private vault and report library features.

**Open decisions (do not silently settle):**
1. Whether vault passphrase protection is recommended by default versus user choice with clear shared-device warning.
2. Can a PWA satisfy user-selected clock-time notifications across supported mobile devices without paid services? Fall back to calendar instructions/in-app reminders if not.
3. Exact initial scene names/art sizes, final accessible contrast/motion design and human character representations.
4. Text/editorial review for `available capacity` glossary tooltip and conservative message templates.
5. Whether optional room reflections should be prompted by count, crowding/density, time, or only on explicit request (no inferred clinical capacity).
6. Where a separate isolated app origin is hosted; verify GitHub Pages free policy and DNS ownership before deployment.
7. Whether full app private storage needs encryption at rest by default; confirm recovery/backup UX.

## Suggested implementation sequence

1. Establish `app/` with a static build and locked dependencies, CI tests, explicit Content Security Policy, minimal accessible shell and offline check.
2. Implement validated `LocalRepository` with migration tests and a local backup/export/delete vertical slice **before** free-text journal records.
3. Build pure functions for scene coordinates, hit tests, z-index, viewport-center zoom and list recovery using placeholders.
4. Add reviewed symptom search catalogue with stable IDs and user-defined terms; explicitly persist `not_recorded` semantics.
5. Add activity definitions/drawers and daily room; optional per-activity check-in and capacity reflection.
6. Implement journal suggestions and insights as pure, auditable rule functions; medically review wording and coverage thresholds.
7. Generate local report from opt-in selections; include report preview and printer/PDF output.
8. Integrate deployed course API behind a strict connector only after origin/security acceptance; add actual images last and test scale normalization on all scenes.

## Engineering quality checklist

### Security, privacy and cost
- [ ] Static site release sends no personal symptom/journal/room/capacity payloads over network (browser network inspector, automated interception test).
- [ ] Content Security Policy, sanitization/text-only journal rendering, dependency scanning, import abuse testing and secure URL construction.
- [ ] Local delete/export/import/forgotten-passphrase behaviour documented and tested.
- [ ] App-only logs exclude symptom terms, typed searches, report text and user IDs.
- [ ] No subscriptions, background AI API, paid push provider, hosted error collector or mandatory app-store account.
- [ ] PWA hosting, account connection, key security and privacy notices separately reviewed.

### Function and integrity
- [ ] Data migration 1→2, atomic error rollback, timezone and date edge cases, duplicates on import and large journals.
- [ ] Symptom numerator/denominator test: unrecorded is never absent.
- [ ] Placing sprite never asserts activity occurred; optional check-in remains optional.
- [ ] Visual clutter never gates further activity placement or assigns medical readiness.
- [ ] Deterministic report includes only user-selected journal content and truthful date/coverage labels.
- [ ] Archive custom symptom without rewriting old entries.

### Accessibility and performance
- [ ] Keyboard-only placement/selection/nudge/z-order, screen reader labels and status announcement, non-color focus indication.
- [ ] Tap-to-place/list parity, big touch targets, undo, zoom center anchoring and overlaid object recovery.
- [ ] 320px portrait, tablets, phone landscape, 200%/400% text zoom, reduced motion, dark/light/system themes, hyperacusis/migraine visual safety.
- [ ] Offline after first install, repeat visits and upgrade; never wipe IndexedDB during service worker update.
- [ ] Efficient scene redraw on drag, avoid storing scene bitmap snapshots for each day; test dozens of placed sprites and long histories.

### Review and governance
- [ ] Peer review security, accessibility, clinical/medical boundary messaging, lived experience and plain language.
- [ ] Record decisions and any divergences from this documentation in code PR notes, with affected tests.
- [ ] Explicit owner approval before registering new domain/origin, changing DNS, deploying Workers, enabling public accounts or accepting cost.

## Pull-request expectations

Future PRs should reference this folder, list **implemented vs merely proposed** features, name any migrations and privacy changes, show tests run, mention free-tier/cost implications, and flag account-service coupling. Do not bundle artwork creation, learner auth changes and health-like local storage into one unreviewable implementation PR.
