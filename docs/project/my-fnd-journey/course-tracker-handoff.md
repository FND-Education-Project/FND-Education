# Companion-app integration handoff for learner-progress PR #154

**Audience:** Maintainer of [draft PR #154](https://github.com/FND-Education-Project/FND-Education/pull/154) and future app developer. This file describes **requested future integration**, not changes already made to the Worker. All public registration remains disabled until PR #154 rollout gates pass.

## What has changed in product design

1. Optional companion **My FND Journey** has a home-card **Continue Learning**, opening the learner's actual next lesson from the existing course system. It is not a separate account provider or progress database.
2. **Remove the proposed app/user reading-mode or role preference entirely.** Do **not** add sufferer/supporter/clinician audience labels, all-perspectives reading mode, or audience progress flags to this API. The three sections remain visible on the website; encourage clinicians to read all three in editorial content only.
3. Symptom, activity, room, journal, capacity and report records are **device-only**. PR #154 must not create tables or endpoints for these records. No analytics join or user identity inference.
4. Account deletion needs honest **two-scope** language: server deletion does not erase private local app data. Optional app connection is not account creation, and “disconnect” is not “delete.”
5. Artwork is deferred. Integration does not depend on sprites, scenes, or reminder features.

## Observed PR #154 behaviour (read on Oct 23, 2026)

- `tools/learner-cloudflare/worker.js`: cookie-based learner identity, exact-origin CORS, account-bound CSRF. `cors()` trusts only `env.PUBLIC_ORIGIN`, and `validSetup()` expects `https://fndeducationproject.org` plus `https://accounts.fndeducationproject.org`; an app hosted at `https://app.fndeducationproject.org` is **not yet an authorized origin**.
- `web/assets/js/course-progress.js`: fetches `/assets/data/course-progress.json`, calls `/v1/progress` via `window.FNDAccount.apiRequest`, computes `nextLesson()` client-side using `lastLesson`, `completed` flags and ordered manifest. It has no separate next-lesson API endpoint today.
- `docs/project/learner-progress-implementation.md` in PR #154: public account controls not enabled, visits vs completed are distinguished, explicit completion confirmation and active username, separate D1 from analytics, three-year inactive-account retention and full-account deletion.
- Canonical content URLs must derive from a validated generated manifest; do not accept arbitrary `returnUrl` or untrusted lesson paths from the app.

## Proposed integration contract (not yet implemented)

### Option A — preferred initially: reuse progress + static manifest

- Signed-in app calls **GET `/v1/progress`** using an authenticated session (credentials and exact Origin/CSRF restrictions maintained).
- App obtains a **versioned static manifest** of ordered public lessons with their canonical IDs, titles and URLs from the website. Bundle or fetch it without private fields.
- In a small, tested shared function, select: if `lastLesson` is recognized and not completed, resume it; otherwise the next uncompleted lesson after last visited; fallback first uncompleted; when all finished, show “Review lessons” not an invented extra lesson.
- Render a **Continue Learning** card with title and link. The link must be a validated `https://fndeducationproject.org/course/...` canonical URL, never an arbitrary server/user string.
- Navigating to the lesson may log **Visited** per site behaviour, but the app itself never silently logs Completed. Website continues to require every completion confirmation.
- Unlinked/offline/error shows **Visit Course** / last publicly known link with an honest unavailable state, never an invented personalized next lesson.

### Option B — future convenience: read-only `GET /v1/progress/next`

May reduce duplicate next-lesson computations, but must validate against the same canonical lesson manifest and avoid a mismatched Worker hard-coded lesson count. Evaluate only after the existing manifest/version strategy is clear. No new API endpoint is required in this design PR.

### Cross-origin identity and request requirements

- If app is a separate origin, authorize **only** the two reviewed web origins in Worker CORS/origin validation; no wildcard `Access-Control-Allow-Origin` on credentialed requests. Exact allowlisted Origin must be echoed with `Vary: Origin`.
- Verify session cookie SameSite behaviour for **same-site but cross-origin** subdomains on actual mobile browsers; `fetch` must explicitly send credentials. Existing anti-CSRF checks must apply to any app write and sensitive action. A PWA must not stash credentials or IDs in localStorage.
- For sign-in callbacks or account settings, carefully validate return paths, redirects and CSRF. Prefer opening existing account UX on `fndeducationproject.org` rather than building duplicate login flows inside the app.
- Decide whether the isolated app will call the Worker directly or temporarily open course pages for authenticated progress. Either way test on device; avoid weakening server security to make an app fetch succeed.
- App must not assume that logging out of the learner account removes device-local tracker records.

## Account deletion / disconnection copy — REQUIRED handoff

Current server deletion is appropriately confirmed by active username and deletes learner data through D1 cascades. Retain this. Extend future account-facing documentation/UI with:

> Deleting your learner account removes your saved course progress and account information from our service. If you use My FND Journey, symptom, journal, activity, and capacity records stored on your device are **separate** and are not erased by this step. Open the app's Privacy & Data settings if you also want to delete local records. Exported files must be deleted separately.

**Scope distinctions:**
- `Disconnect app` = stop app's course link / sign out there; does not delete server account or local tracker data.
- `Delete learner account` = server identity/session/progress/preferences deletion, possible provider backups retained per provider policy; preserve user's local tracker data.
- `Delete app data` = explicit app-local wipe; server learner account untouched.
- `Delete both` (future) = coordinated **two confirmed independent** steps; report partial failure. Never imply one action automatically wipes all copies/devices/exports.

A new app cannot be used as a pretext to broaden the learner DB with health records. The original account inactivity retention policy applies to course accounts only, not as an implicit schedule for app local data deletion.

## Specific developer checklist for PR #154 owner

- [ ] Link this doc in the PR description or discussion; mark companion design future-scope and **not deployed**.
- [ ] Keep currently disabled account rollout gates unchanged.
- [ ] Decide approved secondary app origin + test production CORS/cookie/CSRF before enabling companion login.
- [ ] Ensure a stable, versioned course manifest is available to app; review hard-coded Worker `LESSON_COUNTS` drift.
- [ ] Expose progress read to approved companion origin only under existing authenticated/authorized constraints.
- [ ] Reuse next lesson selection logic or define shared tested behaviour; no arbitrary redirects.
- [ ] Add user-friendly server/local deletion distinction to relevant UX/privacy notice **before companion launch**.
- [ ] No role/reading-mode preference, new health records, diagnostic tracking or automatic “completed” actions.
- [ ] Cover account A vs B, logged-out guest, cross-browser app/origin, session expiration, mobile Safari, and two independent deletion flows in acceptance tests.

**Merge sequencing:** this design PR can merge independently. PR #154 may merge as a disabled account implementation after its existing review; companion integration needs a distinct implementation PR and explicit security acceptance. Do not treat documentation approval as permission to deploy.
