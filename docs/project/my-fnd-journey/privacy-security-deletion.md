# Privacy, security, consent and deletion

**Status:** Security architecture proposal; requires formal threat review and privacy/legal review before launch. “Local only” is a data-minimization choice, **not** a promise of secrecy from anyone using the same device/profile.

## Data categories and strict boundary — Agreed

**Local device only:** symptom labels/states, daily check-ins, room scenes/layouts, activities/participation, self-reported capacity, journal free text, notes, drafts, generated reports, and local settings.

**Existing learner server, only after optional linking:** account identity/authentication, lesson visits and explicitly confirmed completions, site themes/account preferences; **no** local health-like records. The course tracker is already an undeployed draft PR #154.

**Public/static:** app source, static art, approved vocabulary/aliases, glossary and canonical lessons. Static files must never embed a person's journal or symptoms.

**Not collected:** diagnosis, symptom usage analytics, journal text, recordings, medical profiles, device fingerprints, advertising IDs, cloud health telemetry or app-specific identifiers on our server.

## Threat model

1. **Shared/unlocked device:** Anyone with access to the app's origin in that browser profile may read unencrypted IndexedDB. Signing out of the course account does not protect local records.
2. **Lost/stolen device or copied browser profile:** Local at-rest protection needs independent encryption and device security; browser origin isolation alone is insufficient.
3. **Malicious/dependency script/XSS on app origin:** Can access app state and often decrypted content while unlocked. Restrict code, inputs, assets and CSP; encryption cannot fully protect while active.
4. **Export leakage:** Downloads can be exposed through shared downloads/cloud backup, print queues, screenshots, accidental sharing.
5. **Cross-origin account credential misuse:** Companion app is a new origin; the draft Worker currently accepts only the apex website. Maintain exact trusted origins, least-privilege cookie/CSRF checks; never use wildcard credentials CORS.
6. **Sync/third-party SDKs:** Avoid entirely in first release. No remote logging of search strings or symptom notes.
7. **Data loss:** Browsers can evict storage, users can clear site data, private browsing is ephemeral, and PWAs can be removed. Offer clear backup guidance with recoverability tests.

## Storage-protection design — Proposed, not yet UX-settled

- Default is **device-local only** and always explain that this alone does not make shared-device content private.
- Present a well-labelled **optional protected vault**, preferably setup choice with passphrase lock and authenticated AES-GCM encryption for sensitive records. Derive a key with a vetted, calibrated KDF and per-vault random salt; do not store the passphrase or raw key in IndexedDB, URL, or logs.
- The exact default between “locked by default” and “fast access” is **open**, because a forgotten passphrase causes irrecoverable data loss and repeated unlocks can burden people with cognitive symptoms. Evaluate native OS-secure unlock later.
- Encrypt each record or appropriately structured payload with unique nonces, authenticated metadata and versioning. Never build novel crypto formats without review; use vetted browser crypto and test backup/corruption handling.
- A passphrase is **not** account login; server cannot recover local data or keys. No project “reset my health vault” bypass.
- When unlocked, malicious code at the origin or someone at the keyboard may see the data. Do not claim end-to-end secrecy in this condition.

## Application security controls — Proposed

- Strict CSP: scripts and connections limited to app assets; allowlist only exact course API origin for optional authenticated requests. No inline/remote third-party scripts, eval, or trackers.
- Avoid untrusted HTML: render user notes as **text**, not Markdown/HTML from raw input. Protect against DOM XSS, malicious filenames/imports, export formula injection, CSS resource loading and unexpected URL schemes.
- Validate schemas at all user/import boundaries and again before storage; size-limit notes, imports, arrays and URL construction.
- Store no health data in URL fragments/search parameters, push payloads, server logs, crash reports, cookies, browser notification text or app metrics.
- Bundle all matching/detection locally. Do not send symptom typed queries to Pagefind across network or use external AI inference.
- Prefer no analytics in app. If future aggregate app telemetry is wanted, separate consent and privacy design; do not reuse site identity/analytics.
- Updates: pinned dependencies, reviewed lockfiles, dependency audit, isolated deployment, immutable hashed assets, cache migration QA and rollback plan.
- Sensitive actions (delete/import/vault reset) require accessible explicit confirmations; avoid overly elaborate prompts that penalize motor disabilities.

## Learner account link / account deletion

**Two independent deletion scopes** MUST be visible.

**A. Delete my learner account (existing Worker / PR #154):**
- Revoke sessions and delete linked identities, course progress, learner preferences as per the existing security-confirmed server flow.
- Server backup/provider log retention is governed by their policies, not instant guaranteed erasure.
- App must disconnect/clear its course-link state. **Local journal, symptoms, capacity, activity records and exported backups remain on this device.**
- UX: after server confirmation, explain clearly that separate local data deletion is available.

**B. Delete local app data on this device:**
- Wipe app-owned IndexedDB, vault key material/caches where practical, scene preferences, locally saved report drafts; clear decrypted in-memory state. Do not delete server course progress or revoke learner account unless separately requested.
- Can't erase exported PDFs/backups, other browser profiles/devices, OS/browser backups, or copies shared with third parties. Make this visible in plain language.
- Support a “Delete both” guided flow only once both independently confirmed actions exist, with two separate authenticated/explicit steps and partial-failure disclosure. Do not imply the two scopes are atomic.

**Course account disconnection vs deletion:** “Disconnect from app” only signs out locally or removes the optional link; the server learner account and personal local app data stay. “Delete course account” is destructive server action. “Delete device data” is distinct.

### Suggested user-facing notice

> Your symptom, journal and activity records stay on this device. We do not receive them. If you connect your course account, the account stores only your learning progress. Deleting that account does not erase the private records stored in this app. You can delete those separately under Privacy & Data.

Verify this with accessibility and privacy reviewers; the notice cannot be a substitute for a full privacy policy.

## Tests required before any release

Device A/B account isolation; guest/no-network; content injection from journal/import; CSP enforcement; export/import with modified ciphertext and lost passphrase; browser reload and upgrade; lost storage warning; delete all local stores; server account deletion after connection with local data intact; local deletion with server account intact; course CSRF and CORS in production origins; shared-device logout/user-switch, especially if a vault is unlocked.
