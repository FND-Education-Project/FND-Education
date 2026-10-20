# Administration, public crosswords, and optional saved course progress

Status: reference security plan. Learner account UI/API code is under review,
but no learner registration service has been enabled or deployed. Existing
analytics is managed separately from this document.

## Separate identities and privileges

- Public pages and public crossword generation: freely accessible, no account.
  Published clue/answer data may be downloaded/inspected, but editable controls
  and source workbook stay in the administrator workspace.
- Administrator: managed Cloudflare Access sign-in with the owner's existing
  GitHub identity, verified on every protected API request. Configure an
  allowlist for just the authorized admin identity and enable MFA or passkeys
  on GitHub. Password changes, forgot-password recovery, and backup methods
  are administered by the identity provider, not a new FND password database.
- Learner: entirely optional federated login with an established provider
  (Google or Apple first; Amazon and Facebook only after verifying provider
  integrations, policies and free availability). There is no FND-site learner
  password, password-reset email or recovery-code system. Each learner has
  access only to their own course progress. Never allow an authenticated
  learner to access administrator actions or analytics.

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

## Optional federated learner accounts

Reading and public crossword generation NEVER require signing in. Visitors
who choose to save progress may select "Continue with Google" or "Continue
with Apple". Support for Amazon or Facebook may be added after provider setup and
verification. Neither is part of the initial Google/Apple implementation
and neither should be advertised before independent OAuth integration tests.

The sign-in provider handles password changes and forgotten-password
recovery. The project does not receive or store the learner's password.
Because learners sign in with an existing account, no separate learner
password or email-based FND recovery mechanism is required.

Maintain only a random internal learner ID, the provider name and opaque
provider subject ID, optional display username (chosen by the learner,
not a required identity), minimal per-lesson progress, and bounded
server-side session metadata. Do not persist the provider's email address
or profile information unless a later feature explicitly requires it and
the learner consents. Some providers may still disclose profile/email
claims during login; minimize their processing. A provider account and
course history are pseudonymous personal data even without a collected
email address.

SECURITY GATES before enabling public sign-in:
- Use OpenID Connect where supported, or vetted OAuth 2.0 identity flows
  with PKCE, state, nonce when applicable, exact redirect URI validation,
  HTTPS, strict provider issuer/audience/signature/expiry validation, and
  key rotation. Never treat an unsigned email or display name as identity.
- Server-issued Secure HttpOnly SameSite sessions, CSRF protection, bounded
  renewable session credentials, logout and revocation. Default inactivity
  sign-out is disabled, with optional learner-chosen inactivity limits.
  Credential lifetime retains a rolling server-side security cap.
  Never store provider tokens in local storage or page HTML. Protect
  against open redirects.
- Authorize **every** progress read/write by the authenticated server-side
  learner ID. Authentication does not confer an admin role; that requires
  separate Cloudflare Access identity and authorization.
- Keep provider identities namespaced (provider + stable opaque subject).
  Never automatically merge accounts solely because emails match, including
  Apple's private relay addresses. Offer deliberate verified linking only
  after the learner has authenticated with both providers.
- Provider logout/reset/recovery occurs on that provider's website. If
  provider access is permanently lost and no second linked provider exists,
  we cannot prove ownership of the stored progress; make a new account.
- Offer export and deletion of progress and account-linked identity records;
  review inactive-data retention, accessible UX, children/teen eligibility,
  and implications of inferred medical interest before enrollment.
- Avoid extra providers and third-party auth services unless their current
  free quotas, privacy terms, operational limits and app-review conditions
  have been verified. Facebook and Reddit must not be treated as built-in
  Cloudflare Zero Trust learner providers without evidence.

Anonymous usage analytics and learner progress MUST be separate databases
or tables, with distinct access permissions; never mix provider IDs with
anonymous metrics.

## Budget and infrastructure boundaries

Keep public reading and most public crossword generation on GitHub Pages.
Approved published clues may be processed entirely by the visitor browser,
avoiding per-generation server charges. Reserve the backend for analytics,
user authentication/progress and protected administrative tasks.

The supplied Workers Free plan lists 100,000 requests/day, at most 10 ms
CPU per invocation, and D1 allowances of 5 GB storage, 5 million rows
read/day, and 100,000 rows written/day. These are not a forecast of actual
usage. Delegating learner passwords to an identity provider avoids building
a CPU-intensive site-specific password-hashing and recovery-email service.
Use browser-side crossword generation to keep server CPU use low. The
supplied Free plan does not include Cloudflare Email Sending, which is not
needed for ordinary federated-login password recovery.

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
5. Add Google/Apple account-based course progress after provider integration,
   security and privacy review. Public reading needs no sign-in; saving
   progress does. Evaluate Amazon and Facebook separately and do not advertise
   providers that have not been verified.

No public visitor accounts or backend deployment are activated by this plan.
