# Private FND website statistics — separate Cloudflare Worker

**State:** PR #146 contains reviewable code only. The private Worker has
NOT been deployed or connected to Cloudflare Access; existing public event
collection and GitHub Pages hosting must remain unchanged.

## Why two Workers?

The Workers-specific Cloudflare Access application screen offers a Worker's
**production and preview URLs**, rather than a path-level rule. Applying
that policy to the public analytics Worker might require site visitors to
sign in just to send anonymous counts. We will **not** do that.

- **Public Worker** — existing `fnd-aggregate-metrics` from
  `wrangler.toml`. Keeps public `POST /v1/event`, `GET /health`, and
  daily D1 inserts. Code is unchanged by PR #146.
- **Private Worker** — new `fnd-private-statistics` from
  `wrangler-admin.toml`. Serves only `/admin`, `/admin/app.js`, and
  `/admin/api/summary?days=7|30|90`. Reads the **same** existing D1
  database using the same binding name, DB, and database ID. No insert,
  update, or delete queries are available through its endpoints.

Access protects **the entirety of the private Worker**, including its
preview addresses. There is no need to move Namecheap DNS, rehost the public
website, make the public analytics Worker private, or open new public
statistics endpoints.

## Security: two independent conditions must hold

1. Configure a Cloudflare **Access application** for the private Worker's
   production and preview URLs, with **GitHub as the sole login provider**
   and a narrow allow policy for the owner's authorized account. Do not
   choose *Accept all available identity providers*. Cloudflare OAuth
   identity-provider connection is already set up; this is an application
   authorization policy in addition to the login provider.
2. The Worker itself checks a signed Access RS256 JWT (issuer, audience,
   signature, expiry, subject) and matches one authorized admin email.
   Until three explicit Worker secrets are present and valid, all its
   routes return 404. Without a valid signed JWT, requests return 403.
   Cloudflare's policy is still required: an email claim alone does not
   establish that the session used GitHub.

This feature is administrator-only. Neither Worker stores identifiable
website visitor information. Cloudflare Access itself necessarily processes
administrative login/session and network metadata separately.

## Safe step-by-step deployment (only after review and approval)

**Do not run these deployment steps just because the PR exists.**
Cloudflare Free-plan usage limits, Worker availability and whether the
Worker-selection UI protects both production AND preview URLs should be
checked in the account first. Do not accept paid upgrades.

1. Review PR #146 and merge only after the owner approves the code.
   Confirm its two test suites pass. The GitHub repository does not
   automatically deploy either Worker.
2. **Bootstrap the private Worker in the disabled state:** from the
   repository's `tools/analytics/cloudflare` folder, deploy only the
   dedicated configuration, never the public one:
   `npx wrangler deploy --config wrangler-admin.toml`
   No admin secrets exist at this point, so the new Worker's URL should
   return **404**, even at `/admin`. Check this before proceeding.
   This creates a named Worker so it can be selected in Cloudflare Access.
3. In **Cloudflare Zero Trust → Access → Applications**, add a Self-hosted
   and private application using the **Workers** destination. Select
   `fnd-private-statistics` only, and its production/preview URL type.
   Do **not** select `fnd-aggregate-metrics`, the existing public Worker.
   Set the app name, then add a policy allowing just the owner's GitHub
   identity. Under Authentication disable *Accept all available identity
   providers*, and select **GitHub only**. Never add a bypass rule.
4. After you confirm the application is protecting the new Worker, note
   its Application Audience (AUD) and the Access team domain. In the
   **private Worker** environment, configure only these three secrets:

       ACCESS_TEAM_DOMAIN   = your-team.cloudflareaccess.com
       ACCESS_APP_AUD       = the new Access application's audience tag
       ADMIN_ALLOWED_EMAIL = your authorized GitHub-account email

   The Access AUD must be a 32–128 character hexadecimal tag, per current
   code validation. Keep API tokens, OAuth secrets, and any other keys
   out of chat, repository files, screenshots and terminal command history.
   The existing public Worker must NOT receive these secrets.
5. Test an unauthenticated/incognito session and another GitHub account:
   neither should see the dashboard or its JSON API. The owner's GitHub
   login should reach the private dashboard. Confirm all graphs load
   from D1; verify that the public `/health` endpoint and public site
   analytics still work. If any request is unexpectedly accessible,
   immediately disable the private Worker or unset its required secrets.
6. Bookmark the private Worker address; no public site navigation link
   is added. Cloudflare API credentials can be revoked when finished.

**Rollback:** unset any of the three required private-Worker secrets to
make all private endpoints return 404. The existing public analytics Worker
and D1 database continue without interruption.

## Temporary login diagnostic (for a persistent "Access denied.")

If Cloudflare Access accepts GitHub authentication but the Worker responds
with plain `Access denied.`, its independent JWT verification is rejecting
the request. **Do not change GitHub OAuth, Access provider, database, DNS or
public analytics for this diagnosis.** Password or Google sign-in are both
valid ways to sign in to the *same* GitHub account.

The diagnostic is **off by default**. It is controlled by a *private Worker*
secret; never use a GitHub Actions secret for a runtime setting. GitHub
Actions secrets are for build/deploy-time workflows and are unnecessary here.

When the owner explicitly chooses to troubleshoot, deploy the reviewed
diagnostic Worker revision, then temporarily enable this private Worker
secret using the *existing* configuration:

```sh
cd "$(git rev-parse --show-toplevel)/tools/analytics/cloudflare"
npx wrangler secret put ADMIN_AUTH_DIAGNOSTIC --config wrangler-admin.toml
```

Enter `enabled` when prompted. Refresh the private `/admin` page after
signing in via Cloudflare. A 403 now contains **only** a fixed diagnostic
code, never the email, token, key, JWT claims or request headers:

| Code | Meaning |
| --- | --- |
| A01 | No Access assertion header or authorization cookie reached the Worker |
| A02–A03 | Token format or signing header rejected |
| A04 | Token issuer does not match the configured Access team domain |
| A05 | JWT audience does not match the Access application's AUD |
| A06–A07 | Missing subject or invalid token validity time |
| A08 | Signed JWT email missing or not matching the allowed email |
| A09–A10 | Access public-certificates request or response failed |
| A11 | No public verification key matched the signed token |
| A12–A13 | Cryptographic key import or signature verification failed |
| A99 | Other token parsing or verification failure |

A signed JWT must **still** pass all existing checks; diagnostic mode does
not enable access or reduce security requirements. The owner should report
**only the short diagnostic code** for targeted investigation.

**Immediately disable the diagnostic after use**, with:

```sh
npx wrangler secret delete ADMIN_AUTH_DIAGNOSTIC --config wrangler-admin.toml
```

Without that exact secret set to `enabled`, denial responses return the
original generic `Access denied.`. The three Access authorization secrets
must remain in place. Diagnostic output is shown only in the private
dashboard's 403 response; it is **not logged or stored** by the application.
Cloudflare's own standard platform logging is separate.

## What's on the dashboard

The opening screen is a visual overview inspired by cPanel AWStats, using
only the **daily aggregate data this project actually stores**:

- Five summary figures: page openings, searches, search-result clicks,
  download-link clicks and 404-page events.
- Five graphs for the chosen 7-, 30- or 90-day period: page openings by
  day; searches alongside search-result clicks; search-result/PDF/puzzle
  clicks by day; combined downloads by day; and 404 events by day.
- Broad section comparison and a separate event totals table. The precise
  daily figures are available in an expandable accessible table beneath
  the charts.
- Zero-count days remain visible, rather than disappearing from the chart.

These are **counts of page loads and interactions**, not people, sessions,
completed downloads, or conversions attributable to individual users.
There are no hourly charts, top individual page URLs, referring websites,
geographic maps, device/browser profiles, or IP-based AWStats-style
statistics, because those fields are intentionally never recorded.

There are no usernames, search queries, destination URLs, unique-visitor
profiles, stored admin sessions or information about individual people.

This is a read-only statistics dashboard, **not** a spreadsheet editor.
The owner edits the five-column question bank directly in GitHub, as
agreed. The separate original Python crossword generator remains private in
Codespaces and is started with `python crossword.py`; this dashboard does
not publish or modify puzzle questions.
