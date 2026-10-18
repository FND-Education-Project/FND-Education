# Account-based learner progress and preferences

Status: feature implementation and backend deployment plan in PR #154.
**Not enabled in production.** No learner database, OAuth credentials, account
Worker deployment or public sign-in has been activated.

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

Learner credentials are managed by Google/Apple (provider integrations
require live verification); the project never has their passwords. Only a
provider's opaque subject plus a generated internal learner ID is needed.
Do not store provider emails, personal profiles or diagnosis history.

A dedicated Cloudflare Worker verifies OIDC identities and uses Secure
HttpOnly cookies, sliding session renewal, state + nonce + PKCE, exact CORS,
account-bound CSRF and server-authorized D1 reads/writes. No learner data is
joined to anonymous aggregate analytics. Provider emails must never be used
to link accounts without proving control of both identities.

The production Worker is not connected: see
`tools/learner-cloudflare/README.md` for separate D1, custom-domain,
OAuth registration, Apple browser support, security acceptance, rate limits,
provider policy, privacy notice and enablement gates.

## Build and accessibility validation

GitHub Actions runs the website generator, generated-source validation,
Jekyll/Pagefind, built-artifact checks, JS syntax and offline Worker boundary
tests. The latter are **not** complete security tests.

Before allowing public accounts, perform real provider sign-in testing,
including Apple mobile Safari, cross-origin cookies, account A/B isolation,
fresh login, persistent session renewal and revocation, optional idle
sign-out, all completion confirmations, keyboard focus/escape, themes,
tablet/phone, export/delete, clear progress, and failures/offline behavior.

Canonical lesson sources remain unchanged. The implementation is separated
from the editorial audits and existing metrics Worker.
