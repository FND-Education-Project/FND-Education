# Account-based learner progress (deployment gated)

This is an **unpublished, separate learner account service**. It is not part of
the existing private aggregate-statistics Worker and **must not use its D1
database, secrets, routes, or authorization policy**.

## What the implementation does

- Public site and all lesson text remain readable without signing in.
- Account-based progress is the **only** tracking method. No device-local
  or anonymous progress records are written.
- Learners sign in with an established identity provider (Google and Apple
  authorization flows are implemented in the Worker). The provider verifies
  the identity; we store only its provider name and stable opaque subject ID.
- Each account gets a self-editable display username, lesson visits/completion
  flags, a preferred `system/light/dark` theme, and an optional inactivity
  sign-out limit (default: off).
- All progress writes are resolved by the server-side authenticated session,
  never a browser-provided user ID.
- Toggling completion, including unchecking and completing-and-continuing,
  opens a new dialog with the account username in oversized type. Each click
  must be confirmed, without a bypass or remember-my-choice setting.
- Explicit account-confirmed progress reset, personal export and permanent
  account deletion are available.
- No third-party analytics integration or account-linked marketing data.

## Persistent login — safety trade-off

The default account preference is **Automatic sign-out: Off**. That means
there is no *inactivity* timeout selected for that user, allowing convenient
use on a shared device when the account is deliberately kept active.

For protection against a leaked credential, every session still has a
**180-day sliding server-side expiration**. Successful `/v1/me` requests
renew it before expiration; a user absent for more than the cap needs to
authenticate again. Signing out revokes the current session immediately.

This is not a promise of mathematically infinite sign-in. An unbounded
credential would pose a disproportionate risk for an FND health-interest site.
Shorter inactivity limits (15 min, 1 hour, 1 day, 7 days) are an account
preference only. Users can sign out or switch accounts whenever they want.

The active username is persistently shown in the site header. This is
important because merely *visiting* a lesson can be logged automatically
under the active learner; completing a lesson always requires confirmation.
Do not interpret course status as a medical or treatment outcome.

## Activation / security gates (do not bypass)

1. Review relevant privacy laws, retention, deletion, age eligibility, and
   risks of inferred medical interest. Publish updated public privacy text.
2. Create a **new, separate D1** database, apply `schema.sql` with
   `wrangler d1 execute ... --remote --file=schema.sql`, and verify D1
   foreign-key cascades, backups, quotas, recovery and retention.
3. Set up **accounts.fndeducationproject.org** as an HTTPS Worker custom
   domain while keeping the public site hosted on GitHub Pages at the apex.
   This same-site domain and exact-origin CORS policy are intentional.
   Do not simply substitute a `*.workers.dev` domain.
4. Register Google OAuth/OIDC with exact production callback
   `https://accounts.fndeducationproject.org/v1/auth/callback/google`;
   verify current consent-screen and provider policy requirements.
5. Register Sign in with Apple Service ID, keys and exact callback
   `https://accounts.fndeducationproject.org/v1/auth/callback/apple`.
   Generate/rotate Apple's short-lived signed client secret securely.
   Validate provider support for PKCE and `form_post`, browser cookie handling,
   Apple-specific consent flow and mobile Safari before enabling its button.
   **If Apple flow is not working in a supported browser, do not launch both
   sign-in buttons until the provider integration is corrected.**
6. Review Cloudflare Worker and provider billing/free quotas, WAF/rate-limits
   on sign-in and writes, and production TLS, cookie and CORS behavior.
   Enable appropriate abuse prevention and monitoring with redaction of
   credentials and account-specific medical-interest data.
7. Create deployment settings from `wrangler.toml.example` (not the
   placeholders). Set client secrets with `wrangler secret put`; do not
   commit real credentials. Confirm that the Worker receives only the
   dedicated D1 binding and the required secrets.
8. Independently test account isolation, concurrent sessions, logout,
   cross-device sync, reset/delete, username changes, CSRF, token replay,
   session-expiry renewal, session persistence, and multi-tab changes.
   Review WCAG keyboard/dialog focus, phone layout and theme contrast.
9. Only **after** successful deployment and real-world acceptance testing:
   add `learner_api_endpoint: https://accounts.fndeducationproject.org/`
   to `web/_config.yml` and enable the public account controls.
   Before this, the website remains in its normal, static course mode.

The Worker must never run with the same database/permissions as the
existing aggregate metrics Worker.

## Caveats to resolve before production

- Both Google and Apple identities are separate accounts unless deliberately
  linked after verifying control of both. Never merge based on provider email.
- Apple and Google policies and endpoints require up-to-date verification:
  web verification was not available while this branch was authored.
- The API validates lesson identifiers against the 74 lessons currently
  published. Update its `LESSON_COUNTS` alongside any curriculum changes,
  or replace this with a signed/validated shared manifest.
- For deployment, add a tested rate-limit rule and run provider/browser
  integration tests; offline boundary tests are not a substitute.
- The same-site cross-origin login cookie and export/download behavior
  require browser testing with the actual domain and Cloudflare proxy.
- Verify atomicity under concurrent first-time provider logins; enforce
  cleanup of orphaned rows in unusual simultaneous-sign-in scenarios.
- The current UI refreshes progress when opening a page. Cross-device
  writes are reflected after navigation or refresh, not live-pushed.

## Automated checks

```
node --check tools/learner-cloudflare/worker.js
node --check web/assets/js/account-shell.js
node --check web/assets/js/course-progress.js
node --test tools/learner-cloudflare/test-contract.mjs
python tools/site/prepare_site.py
python tools/site/validate.py
```

These checks run in the Pages pull-request workflow, alongside Jekyll and
built-site validation. They do not deploy the account service.

## Current deployment status

**Not configured, not deployed, no public accounts created.** This code
provides the account-first implementation and deployment foundation, but
provider credentials, domain, database setup and end-to-end acceptance
remain prerequisites. Do not merge as a public account launch.
