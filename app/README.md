# My FND Journey — Phase 0 runnable prototype

> **Curriculum compatibility verified October 26, 2026:** Merged [PR #191](https://github.com/FND-Education-Project/FND-Education/pull/191) changed the canonical FND course to **5 Parts, 19 modules and 57 lessons**. The Phase 0 Activity Room uses no course IDs and was not broken. The future Continue Learning feature must use version **2** of the generated lesson manifest from draft [PR #154](https://github.com/FND-Education-Project/FND-Education/pull/154), with 57 eligible lessons and no retired `/course/v2/` or `m20`–`m23` paths. Pure, unconnected compatibility validation in `src/course-contract.mjs` and `tests/course-contract.test.mjs` now enforces those assumptions. The old **private test-only course progress** must be reset **with project-owner approval** before the updated Worker is deployed, because reused lesson IDs may mean different lessons. Public app authentication and course links remain **unimplemented**. Draft PR #192 is updating the glossary/search vocabulary for a later reviewed symptom catalogue.


**Status: early development, local browser prototype only. Not deployed and not ready for personal health records.** Design source: [My FND Journey documentation PR #177](https://github.com/FND-Education-Project/FND-Education/pull/177). Course account service in draft PR #154 remains unchanged/disabled.

This spike tests the **Activity Room interaction engine**, not a complete app. It has no account creation, lesson linking, symptom diary, clinical guidance, analytics, or remote health data service.

## Run locally (no npm install)

From the repository root (Node.js 20+ required):

```sh
cd app
npm test
npm run build
python -m http.server 4173 --directory dist
```

Then open **http://localhost:4173/** in your browser. Close the server with Ctrl+C. For mobile-browser testing, use an HTTPS preview you explicitly authorize; this PR deliberately does not deploy a test site or change DNS.

**The builder copies an existing file**: `assets/images/available-capacity.png` -> `app/dist/assets/scene.png`, solely as temporary scenery. It is not a designed room background and is never committed twice. Three already-coloured emoji cards stand in for future PNG sprites; these are deliberately disposable art placeholders.

The installable-PWA manifest and service worker cache a small fixed static shell for offline revisit on supported secure contexts (including localhost). Some browsers require a suitable raster PNG icon to offer full installability; adding production icons is not part of Stage 0.

## What you can test now

1. Choose a day using the date picker.
2. Open a drawer (chores, rest, positive activities), choose Vacuum/Book/Headphones, then touch/click the scene **or** choose **Add at centre**.
3. Drag placed objects. In narrow portrait layouts, use horizontal scrolling without rotating the device. Zoom in/out with controls (the **visible viewport centre** is the zoom anchor).
4. Select an object to show a visible outline, then move it with arrow keys or the buttons. Use Shift+arrow for fine 4-unit increments.
5. Put objects over one another or partly off-scene; objects can be recovered via **Objects in my room → Locate** or **Bring to front**. Overlapping foreground objects normally cover rear objects rather than being transparent to taps.
6. Change date and return to verify layout persistence; refresh, disconnect your internet and reopen after a successful first load/cache install.
7. Undo edits, remove a selected object, delete one day's layout, or delete all saved prototype layouts.

**Placing an object does not mean the activity happened.** Activity check-ins, capacity prompts, symptom search and reports are later phases.

## Project structure

- `src/scene-model.mjs`: pure world-coordinate, clipping, stacking and zoom functions (unit-tested).
- `src/storage.mjs`: transactional IndexedDB `rooms` store (version 1).
- `src/app.mjs`: accessible shell interactions, pointer handling, scene/list parity, undo and persistence.
- `styles.css`: theme-aware responsive UI and scene viewport.
- `sw.js`, `manifest.webmanifest`, `icon.svg`: minimal offline-first app shell.
- `scripts/build.mjs`: dependency-free static build, copying one repository PNG.
- `tests/`: Node-native geometry and data-integrity tests. Automated real-mobile browser acceptance is still pending.

## Privacy and limitations

- No app server and no external runtime scripts. IndexedDB saves only object IDs, date, positions, scale and z-order; rendered images aren't stored repeatedly.
- Local browser data **is not encrypted** in this proof of concept. Anyone who can access the same browser profile may see it. Do not enter sensitive information.
- Clearing site data, removing the app, or some storage policies may erase rooms. There is **no export/backup** yet; do not rely on this as a permanent record.
- App account authentication, account deletion integration, reminders and notifications are intentionally **not implemented**.
- Touch/pinch zoom, full screen-reader testing, keyboard focus retention, persistence across tabs, database failure scenarios, and PWA installation across iOS/Android need manual validation before a public preview.
- The CSP is specified in HTML for development, but `frame-ancestors` and other HTTP header protections need an appropriate production host. Hosting and TLS choices remain open.
- Stage 0 uses native ES modules without Vite or third-party dependencies to isolate interaction correctness. A full TypeScript/build stack may be chosen after these mechanics pass QA.

## Next steps (separate PRs)

Secure local backup/export/import and user choice of at-rest encryption; reviewed symptom catalogue; three-state check-ins; activity entries/capacity reflections; journal and factual reports; secure optional course link only when PR #154 and origin/cookie reviews are complete. Build original four/five PNG scenes and sprite art last.

**Nothing here changes the live FND Education website, Cloudflare account Worker, public analytics, or existing lesson tracker.**
