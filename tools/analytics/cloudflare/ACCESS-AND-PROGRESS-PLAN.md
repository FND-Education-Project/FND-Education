# Administration, public crosswords, and optional saved course progress

Status: implementation plan only. Nothing here enables learner registration,
a public editor, or any active analytics service.

## Separate identities and privileges

- Public pages and public crossword generation: freely accessible, no account.
  Published clue/answer data may be downloaded/inspected, but editable controls
  and source workbook stay in the administrator workspace.
- Administrator: managed Cloudflare Access sign-in with the owner's existing
  GitHub identity, verified on every protected API request. Configure an
  allowlist for just the authorized admin identity and enable MFA or passkeys
  on GitHub. Password changes, forgot-password recovery, and backup methods
  are administered by the identity provider, not a new FND password database.
- Learner: entirely optional account with a chosen username, password or
  passkey, and narrowly scoped access to that learner's own course progress.
  A recovery email address is optional, not required. If supplied it must be
  verified before it can be used to reset a password. Never give learners any
  route to administrator actions or analytics.

Do not use hidden keyboard commands or an embedded web-page password as an
access-control mechanism. Do not expose the private Streamlit/Codespaces
development server as a public application.

## Administrator controls

Phase 1: Private Cloudflare D1 dashboard offers basic aggregated counts.
Phase 2: A secure admin statistics UI reads only grouped day/week/month
totals from a private API after verifying a managed Access identity.
Phase 3: Build a separate admin question-bank editor; until proven secure,
continue using the existing Codespaces editor. A changed published question
bank must go through content validation before release.

The user need not manage an additional admin password if a managed existing
GitHub sign-in is used. GitHub owns its password changing and recovery. The
Cloudflare account separately needs strong MFA and emergency account-recovery
settings before site deployment.

## Anonymous analytics

The existing analytics Worker holds ONLY date, broad site section, type of
action, and aggregate count. It stores no visitor history, search text,
cookie, browser fingerprint or account ID. Do not join learner account
data to these anonymous usage counts. Page views count opens rather than
unique people; download events count link clicks, not completed downloads.

## Separate optional learner accounts

A learner may choose a unique, non-identifying username. No legal name,
email, phone number, date of birth, or medical details are required.
An **email address is optional** and may be provided for account recovery.
It is neither publicly displayed nor used for marketing; absence of an email
must not block enrollment, learning, or progress saving.

Store only an opaque account ID, username, strong salted credential verifier,
a hash of one-time recovery codes, minimal per-lesson progress, and
short-lived session metadata. If supplied, store the recovery email with a
verification status and an appropriate protection/retention policy. A learner
can add, verify, update or remove their email, and save, inspect, export, reset
and delete their own account and progress.

SECURITY GATES before public enrollment:
- HTTPS, Secure HttpOnly SameSite session cookies, CSRF protection, bounded
  sessions, and restrictive CORS.
- Slow password hashing (or passkey credential verification), throttle and
  monitor abuse at the edge without exposing raw credentials in logs.
- Offer BOTH recovery options: (a) a single-use, short-lived password-reset
  link sent only to a previously verified recovery email, OR (b) an unused
  single-use recovery code given to the learner during account setup.
  Recovery codes should be stored only as salted/slow verifiers and shown once.
  Never include credentials in logs or analytics. Rate-limit signup, email
  verification, recovery requests and code guesses; send generic responses
  that do not reveal whether a username or email is registered. Expire and
  invalidate used reset links/codes. If neither a verified email nor a valid
  recovery code remains, account ownership cannot be securely demonstrated.
- Emails must use an approved transactional sender with verified sending
  identity. The supplied Cloudflare Workers Free plan explicitly excludes
  Cloudflare Email Sending; do not promise free email resets or implement a
  paid delivery dependency without pricing and privacy approval. Until a
  sender is configured, recovery codes are the supported reset method.
- Verify every learner read/write against server-side session identity;
  never accept claimed account IDs from the browser as authorization.
- Automated negative tests for accessing someone else's records, escalating
  to admin rights, CSRF, replay/reused codes, and forgotten credentials.
- User-owned export/deletion, sensible inactive-data retention, and
  accessibility/privacy review including implications of inferred health
  interests and younger visitors.

A username and individual course history are pseudonymous account data,
and an optional email address is personal contact information. Do not promise
that this is literally no personal information. Update the public privacy
notice before account enrollment to describe voluntary email storage,
verification, password-reset purposes, deletion and retention. Anonymous
analytics and personal progress MUST use separate tables/storage and
separate permissions.

## Budget and infrastructure boundaries

Keep public reading and most public crossword generation on GitHub Pages.
Approved published clues may be processed entirely by the visitor browser,
avoiding per-generation server charges. Reserve the backend for analytics,
user authentication/progress and protected administrative tasks.

The supplied Workers Free plan lists 100,000 requests/day, at most 10 ms
CPU per invocation, and D1 allowances of 5 GB storage, 5 million rows
read/day, and 100,000 rows written/day. These are not a forecast of actual
usage. In particular, 10 ms CPU may be unsuitable for intentionally costly
password hashing and substantial server-side crossword generation. Use
browser-side crossword processing and evaluate managed authentication or
passkeys before choosing the credential runtime. The supplied Free plan also
lists no Cloudflare Email Sending.

Cloudflare Workers, D1 and Access are candidates for low-volume hosting.
There is NO provider guarantee of two years of free service. Verify current
account-specific limits, billing/payment requirements, storage quotas and
account policies before provisioning. Seek hard spending limits, alerts and
fail-closed handling where available. Never enable a paid service or change
DNS/domain hosting without a separate explicit decision.

Rollout:
1. Create and secure a Cloudflare account. Keep Namecheap domain and
   GitHub Pages hosting where they are.
2. Privately deploy tested metrics Worker and D1; check current pricing,
   provider privacy policies and approved home-page notice.
3. Configure managed administrator access and a private stats dashboard.
4. Add a public browser-based crossword generator using published
   question data, with no sign-in required.
5. Add opt-in learner progress accounts with recovery codes and optional,
   verified recovery emails after selecting a secure, affordable email sender
   and completing separate security and privacy review.

No public visitor accounts or backend deployment are activated by this plan.
