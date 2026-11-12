# Optional email login — staged rollout

Public reading never requires an account. This change prepares Google plus
passwordless email, with Apple deferred. Do not enable the public API endpoint
or merge as a live launch until the real-domain acceptance checks pass.

## Existing Codespace / database

1. Pull the reviewed branch without overwriting the ignored local
   `wrangler.toml`, `.dev.vars`, or existing D1 binding. Do not create another
   database merely because the example contains a placeholder.
2. Back up the isolated learner D1. Apply
   `migrations/0002-email-login.sql` to that database using its local Wrangler
   configuration. This is additive, repeatable, and preserves Google identity,
   session and progress tables. Do not apply it to anonymous analytics.
3. Fresh databases use `schema.sql`, which includes the email tables already.
   Existing databases require the additive migration before running this Worker,
   even if email login remains disabled (cleanup and export use the new tables).

## Resend and DNS

1. Use Resend's free transactional plan. Verify a dedicated sending subdomain,
   such as `mail.fndeducationproject.org`. Copy the exact DKIM and SPF/MX
   records Resend supplies into Cloudflare. Do not change apex website records
   or replace unrelated mail records; keep mail DNS records DNS-only.
2. Configure the sender as `login@mail.fndeducationproject.org`, matching
   `EMAIL_FROM`. Configure DMARC for the sending domain after checking Resend's
   current instructions. Disable open and click tracking in Resend.
3. Create a sending-only API key scoped to that sending domain. Store it with
   `wrangler secret put RESEND_API_KEY`, never in public JS, a screenshot,
   the repository or this document. No email is sent during local tests.
4. Production recipient sending requires verified-domain setup; Resend's
   default testing sender is not a public signup solution. Test actual inboxes,
   spam placement and delivery delay before launch. Provider acceptance of a
   send does not guarantee inbox delivery.

## Turnstile and Worker configuration

1. Create a free Turnstile widget restricted to `fndeducationproject.org`.
   The browser uses action `email_login`; the server verifies success, hostname
   and action before reserving a send. The widget loads only after email is chosen.
2. Add `TURNSTILE_SITE_KEY` and `EMAIL_FROM` to local `[vars]`.
3. Set secrets `TURNSTILE_SECRET_KEY` and `EMAIL_AUTH_SECRET` (a securely generated
   independent random value of at least 32 characters). The latter protects
   stored code digests and rate-limit identifiers; rotating it invalidates
   pending codes and resets the effective email/IP rate-limit namespaces.
4. Keep `EMAIL_LOGIN_ENABLED = "false"` until sender and widget setup are done;
   then enable only for a deliberate acceptance deployment. Google can work
   independently when its real client ID and secret are configured. Neither
   Apple credentials nor a placeholder Google ID publish a login button.
5. Deploy only the learner Worker using the existing custom accounts domain.
   Keep `learner_api_endpoint` commented out on the public site until tested.
   Test through an unpublished/local-preview front end with an explicitly
   configured test environment, or a controlled production-origin acceptance
   page. Do not weaken production Origin/hostname checks for previews.

## Free-tier safeguards and operations

- Codes: eight numeric digits, one use, ten minutes, five verification attempts,
  bound to the requesting browser's HttpOnly cookie and an opaque challenge ID.
- Delivery limits: one/address/minute bucket, three/address/hour,
  ten/address/day, ten/IP/hour, ninety total/day, 2,700 total/calendar month.
  Fixed buckets allow boundary bursts; these are ceilings, not delivery promises.
- All reservations use atomic SQL. Failed/uncertain sends still consume budget.
  There is no automatic retry that could send duplicate messages. Resend sends
  include an idempotency key. No application-level paid overages are enabled.
- These caps assume a dedicated Resend account with no other senders. They do
  not account for dashboard/test emails or other applications. Monitor provider
  usage; pause this feature before a shared quota is exhausted. Set external
  account spending controls if offered; application caps are not billing controls.
- Use the Cloudflare dashboard to watch Worker errors, CPU and D1 usage.
  A failed provider send emits only `learner_email_delivery_failed`. Never log
  bodies, recipient addresses, codes, bearer tokens or API keys. Disable request
  body logging in any platform instrumentation. Add edge rate limits for auth
  endpoints before launch; Turnstile and application limits do not stop all DoS.
- Daily Cron deletes expired pending addresses/challenges and limiter buckets.
  A ten-minute challenge may remain in storage until the next successful daily
  cleanup; monitor failures. Global counters remain until their period ends.
- Existing sessions and Google login can continue if email sending is limited.
  Public course reading always remains available. New email login may require
  waiting for a quota reset or service recovery; do not imply unlimited access.

## Identity and privacy

- Email is case-insensitive for this service; dots and plus tags are preserved.
  Current form supports conventional ASCII addresses. Internationalized mailbox
  local parts are not supported yet; this limitation must be visible in help.
- Email belongs to one learner, and a learner can have one verified email.
  A Google learner can add it while signed in, with CSRF plus email proof.
  A different email cannot silently replace it. Email changes/unlinking and
  attaching Google to an email-first account are not implemented in this release.
- If an email already belongs to another account, linking refuses to merge.
  Do not merge by matching a Google email or display username. Guest signup UI
  tells Google users to sign in first and attach email to preserve their progress.
- Verified email is included in personal export and cascades on account deletion.
  Deletion also cancels pending login challenges for that address. Anonymous
  metrics remain in a separate database with no identity joins.
- Resend receives the address and code email; Turnstile processes verification
  information. Publish this disclosure and applicable provider retention terms
  before launch. Delivery logs/backups are not instantly erased by deleting D1.
- Google-only accounts still do not store email. All accounts retain the existing
  three-year inactivity policy; no deletion-reminder emails are sent.
- Loss of access to the sole login mailbox can mean loss of access to the account.
  Do not invent a support recovery path that bypasses verified ownership.

## Acceptance checks (required after local tests)

Run `node --test tools/learner-cloudflare/test-*.mjs` with Node 24, then test:

- Google and email separately; anonymous full course reading; missing-provider UI.
- Actual Resend delivery to several mailbox providers; timeout/failure messages.
- Correct/wrong/expired/reused codes, resends, browser restart and separate devices.
- Two people sharing a browser; separate browser sessions; username confirmations.
- Google -> add email -> sign out -> email sign-in -> same progress and preferences.
- Linking conflicts, expired session while linking, logout and account deletion.
- Keyboard-only use, focus, screen-reader status, narrow/mobile layout, dark mode,
  Safari cookies, autofill/paste, Turnstile blocked/expired and network failures.
- Exact production CORS/Origin, sender-domain DNS, quotas, Cron cleanup and CPU.

Only then enable public account controls. No production secrets or sending-domain
configuration are created by the source-code commit.
