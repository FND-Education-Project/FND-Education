# Architecture, stack, modules and class responsibilities

**Status:** Proposed architecture, **not a current implementation**. No dependency choices are binding until a proof of concept and security/accessibility review. No monthly subscription, proprietary hosted AI, or app-store developer account is required for the first PWA build.

## Current repository constraints (confirmed in PR #154)

- Website: statically built Jekyll/GitHub Pages, with vanilla browser JS.
- Educational search: Pagefind and human-reviewed `tools/search/subject-index.json` + site route metadata.
- Course accounts: separate Cloudflare Worker + D1, authenticated with cookie, exact-origin CORS and CSRF. Implementation in draft PR #154; **public sign-in disabled**.
- Canonical lesson manifest: generated `/assets/data/course-progress.json` from course Markdown; the browser determines next lesson using account progress and ordered lesson data.
- Existing Worker currently trusts `https://fndeducationproject.org` as its sole public origin, which is an integration blocker for a separate app subdomain. Do not assume CORS automatically works.

## Proposed runtime topology

```text
app.fndeducationproject.org  [future separate-origin PWA, public static assets]
  UI (installable app, service worker, local assets and glossary)
    |
    +-- LOCAL ONLY --> IndexedDB (check-ins, journal, scenes, capacity, settings)
    |                 + optional encrypted vault/backup, on-device reports
    |
    +-- STATIC PUBLIC --> versioned symptom vocabulary and course metadata
    |
    +-- OPTIONAL AUTHENTICATED --> accounts.fndeducationproject.org
                                    (existing learner Worker and D1)
                                    course status / preferences only
                                    NO symptom / activity / journal data

fndeducationproject.org --> public canonical lessons and reference pages
```

**Origin isolation:** A dedicated app origin limits the educational site's ability to access the app's IndexedDB directly (same-origin policy). It does not make browser-resident private data invulnerable to malicious code served from the app origin. Keep static asset and external-script supply chain tightly controlled.

## Proposed stack — no new hosted service

| Layer | Candidate | Reason / caveat |
| --- | --- | --- |
| UI | TypeScript + standard Web Components (or lightweight Lit only if justified) | Reuse web platform, clear boundaries, low runtime weight; component a11y still requires explicit work |
| Bundler | Vite (pinned and lockfile committed) | Local dev, hashed production assets, static output |
| PWA | Web app manifest + reviewed service worker | Offline shell; explicit update/cache strategy; native widget support not implied |
| State | Small local view models/services, no heavyweight global store | Avoid complexity and medical data leaking to URL/query strings |
| Storage | IndexedDB, versioned stores/transactions; thin wrapper | Browser-local, no database server |
| Crypto | Web Crypto AES-GCM + established password-based KDF if vault chosen | No home-grown encryption; test key management and lost-passphrase UX |
| Charts | Accessible SVG/HTML-based deterministic views | Text equivalents and exported tables |
| Reports | Local print styles; vetted client-side PDF only if necessary | No report upload |
| Matching | Offline curated term index + conservative fuzzy matching | No model inference or network query of private user text |
| Tests | Vitest/unit + Playwright browsers/accessibility checks | Keyboard, touch, offline, storage persistence, security boundaries |
| Hosting | Separate static GitHub Pages deployment under a dedicated origin | Needs separate Pages site/repository or another verified static host; do **not** assume one Pages site serves two unrelated custom domains |
| Existing backend | Cloudflare learner Worker/D1 only when linked | No new tracker backend or user health records |

Dependencies and hosting are subject to current free plan limits and project owner approval. No remote monitoring, crash reporting, telemetry, notifications or CSP exceptions should be enabled by default.

## Proposed source layout (new app subproject, not yet created)

```text
app/
  package.json
  src/
    bootstrap.ts
    app-shell.ts
    domain/
      symptom.ts
      check-in.ts
      activity.ts
      scene.ts
      capacity.ts
      journal.ts
      report.ts
    components/
      home-view.ts
      symptom-picker.ts
      check-in-view.ts
      activity-room-view.ts
      object-drawer.ts
      journal-view.ts
      patterns-view.ts
      report-preview.ts
      app-settings.ts
    services/
      local-repository.ts
      symptom-matcher.ts
      scene-layout.ts
      analytics-engine.ts
      journal-suggestions.ts
      report-builder.ts
      course-connector.ts
      backup-vault.ts
      reminder-service.ts
    assets/
      catalog/
      scenes/
      sprites/
    styles/
    service-worker.ts
  tests/
    unit/
    integration/
    e2e/
```

This is a responsibility map, not a mandate to create large stateful classes. Prefer pure domain functions for calculations and composition over inheritance.

## Components/services and contracts

| Component/service | Responsibility | Forbidden/important boundary |
| --- | --- | --- |
| `LocalRepository` | IndexedDB migrations, atomic CRUD, validated persistence | Never `fetch` private data or use localStorage for records |
| `SymptomMatcher` | Canonical/alias/fuzzy matching in reviewed local catalogue | No diagnostic label assignment or journal upload |
| `CheckInService` | Date rules, explicit three-state assessment, revisions | No implicit “not checked means absent” |
| `SceneLayoutEngine` | World-coordinate placement, scale, scroll/zoom, z-order, hit tests, undo | Independent of image sizes and UI framework |
| `ActivityLogService` | Link optional activity check-ins with placed object IDs | Placement != activity completion |
| `CapacityReflectionService` | Explicit self-reported day-end/next-day capacity | Never compute a clinical readiness score from clutter |
| `JournalSuggestionService` | Conservative local phrase matching with negation/person filters | Suggestions only; no silent symptom changes |
| `PatternsEngine` | Aggregates with known denominators/coverage thresholds | No causation, predictive medical claims or missing=zero |
| `ReportBuilder` | Deterministic user-selected summaries/printable reports | Must not auto-include sensitive notes |
| `CourseConnector` | Read optional authenticated progress + public manifest; open canonical URL | **No** symptom or journal payload on account API |
| `LocalVault` | Optional storage lock, encryption/decryption, export/import | Do not retain passphrase or keys in logs/URLs |
| `ReminderAdapter` | Opt-in scheduling/cancel; expose platform capability | No promised silent closed-app PWA timers |
| `ActivityRoomView` | Accessible touch, keyboard, drag, list and visual controls | Show selected state without color alone; no forced landscape |

## Trust boundaries

1. Static app code is public and does not imply access to user records.
2. IndexedDB/private vault belongs to one **device/browser profile/origin**, not a Cloudflare learner ID. Avoid correlating local record identifiers with server ID.
3. Only `CourseConnector` may call the learner Worker; centralize a strict request allowlist and payload schema.
4. All symptom education links are ordinary public navigations; do not include personal data in URLs, referrer or query strings.
5. On failure or offline state, app functions continue without course sign-in; never fabricate saved lesson progress.
6. One shared device can expose local browser storage to other people unless protected by browser profile/OS/vault. Account logout alone does not purge it.

## Platform specifics

- **PWA:** installable and useful offline, but cross-device sync absent. Reliable user-timed notifications while closed depend on browser/platform push support, permission and possibly a backend; widget support is not cross-platform. Do not promise those in Release 1.
- **Future native Android/iOS:** portability achieved through a domain-services layer; SQLite, Keychain/Keystore and OS local notifications can replace infrastructure adapters. Store/app signing and platform fees are separate from infrastructure; iOS App Store typically entails a recurring developer fee.

## Nonfunctional architecture targets (proposed)

Offline-first check-in; safe schema migrations; no private records in logs or crash diagnostics; CSP without third-party scripts; accessible large touch targets with keyboard equivalents; preserve scenes without rendering/storing full composited PNGs; tolerate partial records; bounded memory for big journals; app updates must not overwrite records; rollback/recovery plan for failed imports.
