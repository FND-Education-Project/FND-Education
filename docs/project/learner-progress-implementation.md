# Account-based learner progress and preferences

Status: feature implementation and backend deployment plan in PR #154.
**Public sign-in is not enabled in the committed site configuration.**
Database provisioning has begun separately; this document is not live-state telemetry.

## Approved learning experience

All course and Reference material is public without a sign-in. Learners who
choose to save progress must sign in; we do **not** save course status in a
shared browser's localStorage.

The course index displays collapsible Parts > Modules > Lessons from
`web/assets/data/course-progress.json`, regenerated from canonical course
Markdown. The 74 lessons count toward progress; module introductions and
optional crosswords do not.

- Each visitor can read any page without an account.
- A signed-in learner sees their username prominently in the site header.
- Opening a lesson records **Visited** for the active account, not Completed.
- Clicking or unclicking **Complete** always opens a new confirmation dialog
  with the **active username in large type**. There is no bypass toggle.
- The combined **Mark completed & continue** action does the same check.
- Home and course pages can continue at the account's previous lesson.
- Only contextual course-navigation links get compact status indicators.
- Learners can reset progress while keeping their identity, or export and
  delete their learner account separately.
- Without a configured/available account API, published lesson content and
  static course index remain readable, not replaced by fictitious progress.

## October 26, 2026 — curriculum #191 compatibility (not deployed)

PR #191's new canonical course has **19 modules / 57 current lessons**.
Its older 75 lessons, nine superseded module overviews and original URL/key
pairs remain public as an earlier edition. Of the current 57 lessons, 16
new concepts-first lessons live at /course/v2/m6/.../m10/; they use
reserved internal source slots 24–28, *not* legacy Module 6–10 identities.
Thus the 57-lesson path contains 41 original progress-eligible lessons;
34 original lessons remain earlier-edition reading. All 75 original lesson
progress records must remain intact across a curriculum change.

**Completed on this feature branch, not in production:**
- Correct the Worker legacy allowlist from 74 to 75, including `m4-2`.
  Retain its strict m1–m23 allowlist; the new source slots 24–28 and
  arbitrary IDs remain rejected by the server.
- Add a v2 manifest contract with `progressEligible`, a separate
  `earlierModules` collection, immutable legacy IDs and explicit URLs.
  The 16 new lessons have null API IDs; they are readable but do not
  offer any Visit/Complete mutation or misleading Not Started status.
- Keep the account client compatible with v1 local previews while enabling
  v2 core and earlier-edition views, and resume earlier stored keys at
  their exact old routes (e.g., original `m6-1` seizures).
- Never map current display module numbers to API IDs; never migrate D1
  values, reinterpret existing checkmarks, or discard unrecognized saved
  rows. No schema change or account deployment is part of this update.
- Whitelist new `/course/v2/m6/…/m10/` pages as safe return destinations
  for optional provider sign-in without granting those lessons completion IDs.
  Keep strict origin-independent path validation and reject external redirects.
- Add synthetic curriculum tests for 19 current modules / 57 current
  lessons / 34 earlier lessons / 75 immutable eligible legacy IDs and
  16 newly readable, untracked lessons.

**Required before reconciling and merging:** PR #191 is an independent,
currently unmerged course publication, with conflicting generator work.
After its separate approval/merge into main, reconcile the manifest writer
with the canonical `tools/site/prepare_site.py` from #191 **without losing
either branch's discovery/navigation work**. Test a fresh site build and
generated JSON against the real #191 course. Ensure 19 current modules,
57 current lessons, 34 earlier lessons and 75 preserved original keys.
Then run Node contract tests, site validation, browser checks on course
and earlier-edition pages, and two-account sign-in/reauthentication
acceptance before enabling the public account endpoint.

**Existing real-browser tests (private Chrome Local Overrides):**
Passwordless email/Turnstile and Resend; one learner's completion survived
refresh, sign-out, and return; two email-based learner accounts stayed isolated
through repeated switching (one completion versus three); all appearance
choices persisted and applied with the feature CSS. This verifies the old
progress contract and account isolation, **not** #191 publication integration
or eligibility-aware new lesson behavior.

Do not merge PR #154 automatically or deploy the Worker when PR #191 lands;
the feature remains gated until the shared contract and real browser tests
pass. The public course may publish independently.

## Account preferences and shared devices

Display username, theme (`system`, `light`, `dark`), and optional
inactivity sign-out (`Off`, 15 min, 1h, 1 day, 7 days) belong to each account
in a dedicated D1 database.

**Off is the default**, so there is no inactivity-based sign-out for people
who prefer to stay signed in. Server credentials nevertheless have a
renewable 180-day safety cap. This differs from a default auto-logout
schedule. Logout/switch-user visibly revokes the active session.

A prominent username makes accidental actions less likely but cannot
prevent a caregiver accidentally browsing under another account. Completed
status always requires confirmation. A read-only course page is public.

## Security and privacy

Learners can use Google or optional passwordless email codes sent by Resend.
The project never handles passwords. Google retains only its opaque subject;
email authentication retains the verified email in a separate ownership table.
Do not store Google profile emails, personal profiles or diagnosis history.
Apple is deferred. Google learners can explicitly verify and add an email to
that same account; automatic account merging is prohibited.

A dedicated Cloudflare Worker verifies OIDC identities and uses Secure
HttpOnly cookies, sliding session renewal, state + nonce + PKCE, exact CORS,
account-bound CSRF and server-authorized D1 reads/writes. No learner data is
joined to anonymous aggregate analytics. Provider emails must never be used
to link accounts without proving control of both identities.

The production Worker is not connected: see
`tools/learner-cloudflare/README.md` for separate D1, custom-domain,
OAuth registration, Resend/Turnstile setup, security acceptance, rate limits,
provider policy, privacy notice and enablement gates.

## Build and accessibility validation

GitHub Actions runs the website generator, generated-source validation,
Jekyll/Pagefind, built-artifact checks, JS syntax and offline Worker boundary
tests. The latter are **not** complete security tests.

Before allowing public accounts, perform real provider sign-in testing,
including mobile Safari, email codes, cross-origin cookies, account A/B isolation,
fresh login, persistent session renewal and revocation, optional idle
sign-out, all completion confirmations, keyboard focus/escape, themes,
tablet/phone, export/delete, clear progress, and failures/offline behavior.

Canonical lesson sources remain unchanged. The implementation is separated
from the editorial audits and existing metrics Worker.


## Database maintenance and retention

### Automatic cleanup

The learner Worker includes a **daily Cron maintenance task** (04:00 UTC)
that deletes expired OAuth login attempts and expired server sessions.
It also removes at most **100 learner accounts per run** if they have had
**no authenticated account activity in three calendar years**. A fresh
authenticated request updates `last_seen_at` (at most once per day), and
a learner with an unexpired session is excluded from deletion.

The three-year rule is separate from each learner's optional inactivity
*sign-out* setting. Disabling automatic sign-out does not exempt an account
from long-term deletion. A genuinely active learner keeps their progress.

Deletion relies on enforced SQLite/D1 foreign-key cascades: removing the
learner must remove linked identity provider identifiers, lessons, preferences,
and sessions. If migrations, constraints, or related tables change, test
this explicitly with D1 before deployment. Cron should run without requiring
visitors, and a failed job must be monitored and retried; never ignore errors.

### User-initiated deletion

A signed-in learner can select **Delete my learner account** in account
preferences. The interface asks them to type their active username and
confirm the permanent deletion. The Worker checks the secure session,
exact-origin CSRF token, and username confirmation; it deletes the owning
learner record and cascades associated data. It then clears that device's
session cookie. A separate action resets lesson progress without deleting
the learner account.

### Privacy limitations

Email authentication addresses are retained privately. Inactivity-deletion
reminders are not implemented, regardless of login method. Before first login and
in account preferences, disclose the three-year policy. Export progress
is available before deletion. Keep accounts no longer than necessary and
do not join this database to anonymous statistics.

Deletes remove records from the *active D1 database*. Cloudflare backups,
PITR/time-travel copies, and provider platform logs might remain for a
provider-controlled retention window; review and document those terms
before claiming complete immediate erasure of every backup. Rate-limit
destructive calls and test browser/account recovery cases.

All cleanup work in this branch is unprovisioned; it becomes active only
after the isolated learner D1 and Worker pass the production setup gates.
