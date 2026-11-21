# Account-based learner progress (deployment gated)

This is an **unpublished, separate learner account service**. It is not part of
the existing private aggregate-statistics Worker and **must not use its D1
database, secrets, routes, or authorization policy**.

## What the implementation does

- Public site and all lesson text remain readable without signing in.
- Account-based progress is the **only** tracking method. No device-local
  or anonymous progress records are written.
- Learners may choose Google or passwordless email codes delivered by Resend.
  Google stores only the provider name and stable opaque subject ID. Email
  sign-in stores a verified email separately. Apple is deferred and disabled.
  Available methods are discovered from `/v1/auth/options`; unset methods are hidden.
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
5. Follow [the Resend rollout](RESEND-SETUP.md) for optional email sign-in:
   apply the additive migration, verify a dedicated sending subdomain, set
   sending-only Resend and Turnstile credentials, and verify deliverability.
   Apple is deferred; its old code paths cannot be activated by credentials.
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

- A Google learner can add verified email sign-in in account preferences.
  A guest email login creates or opens its email-owned account. Never merge
  by matching Google email, username or an unverified form entry. Adding
  Google to an email-first account is not implemented in this release; the
  UI explains how Google learners should attach email before switching.
- Google production policies and browser behavior still require deployment review.
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
node --test tools/learner-cloudflare/test-*.mjs
python tools/site/prepare_site.py
python tools/site/validate.py
```

These checks run in the Pages pull-request workflow, alongside Jekyll and
built-site validation. They do not deploy the account service.

## Current deployment status

**Public accounts remain disabled in the committed website configuration.** This code
provides the account-first implementation and deployment foundation, but
provider credentials, domain, database setup and end-to-end acceptance
remain prerequisites. Do not merge as a public account launch.


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

Email addresses are retained only for optional email authentication. No
inactivity-deletion reminders are implemented for either sign-in method. Before first login and
in account preferences, disclose the three-year policy. Export progress
is available before deletion. Keep accounts no longer than necessary and
do not join this database to anonymous statistics.

Deletes remove records from the *active D1 database*. Cloudflare backups,
PITR/time-travel copies, and provider platform logs might remain for a
provider-controlled retention window; review and document those terms
before claiming complete immediate erasure of every backup. Rate-limit
destructive calls and test browser/account recovery cases.

Cleanup becomes available with this Worker; it becomes active only
after the isolated learner D1 and Worker pass the production setup gates.
