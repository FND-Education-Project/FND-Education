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
Markdown. The **57 current lessons** count toward progress; module introductions and
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

## October 26, 2026 — one canonical 19-module course

At the owner's explicit request, the dual-edition/legacy-preservation
approach was abandoned while the learner system is still in private testing.
Curriculum PR #191 now contains **19 uniformly named module directories and
57 current focused lessons**, with the 34 superseded course lessons and nine
superseded module overviews removed. Current URLs are `/course/m1/` through
`/course/m19/`; the temporary `/course/v2/` paths are retired.

**Account progress contract for this new course:**
- One valid lesson key `m<module>-<local-page>` for each of the 57 lessons.
  Both numbers follow the current canonical curriculum, not an older syllabus.
- The Worker now validates exactly 19 module lengths totaling 57. Old
  `m20`–`m23` keys and superseded extra lesson numbers cannot be written.
- Only these 57 lessons may display a visited/completed flag or confirmation
  checkbox. Every change still requires the correct session, CSRF token,
  and prominently displayed username confirmation.
- The generated curriculum manifest must contain **five Parts, 19 Modules,
  57 lessons, zero earlier-edition modules**, and 57 eligible unique IDs.
- The browser may resume from saved progress only when that ID exists in
  the same currently published manifest. Displayed lesson numbers and actual
  API identity are no longer separate concepts.
- Email/Google return paths admit current `/course/m1/`–`m19/` reading
  locations, never the retired v2 URLs; credentialed CORS stays exact-origin.

**Test-data reset is required before the changed Worker + site go live.**
The Cloudflare learner D1 currently contains **test accounts** used for the
previous 74/75-lesson preview. A key such as `m6-1` could now mean a
different lesson; allowing old checkmarks would be misleading. The reset
in `tools/learner-cloudflare/reset-test-course-progress.sql` intentionally
clears `learner_progress` and all `learners.last_lesson` pointers; it does
**not** remove usernames, verified emails, themes, sessions or identities.
It is NOT automated: the owner must review test-only records, export anything
worth preserving, then run it against `fnd-learner-accounts` explicitly, never
the statistics database. Do not deploy the updated validator before the
database reset and coordinated public manifest/client change.

**Branch integration pending:** PR #191 should be merged independently,
then PR #154's generator/manifest and client changes must be reconciled
against its actual canonical `tools/site/prepare_site.py`. A stand-alone
synthetic 19/57 contract test exists, but it is not proof of the future merged
site. Test the real generated JSON, Jekyll links, Node/Worker suite, Chrome
and mobile sign-in, 2-account isolation, resume, themes and deletion. Keep
PR #154 a draft and public sign-in disabled until those gates pass.

**Earlier private browser acceptance:** Passwordless email with Turnstile
and Resend, confirmed completion, refresh/sign-out persistence, two accounts
staying separate (1 vs 3 prior test completions), and three appearance choices.
These establish auth and isolation, not correctness of the new 57-lesson data;
the prior completion flags must be cleared and retested.

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
