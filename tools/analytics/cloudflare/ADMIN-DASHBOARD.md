# GitHub-only administrator statistics: secure setup

**Status:** Code prepared for review only. This change does not configure
Cloudflare Access, add Worker secrets, deploy the edited Worker or expose
a statistics service. Existing public anonymous counters continue to work.

## Boundary between public and private

- GitHub Pages stays public and free to browse.
- The Cloudflare Worker provides a private dashboard at /admin, its own
  same-origin script at /admin/app.js and a read-only D1 summary API at
  /admin/api/summary?days=7|30|90.
- Every route verifies a signed Cloudflare Access JWT: exact issuer and app
  audience, RS256 signature and key, token expiry, subject, and expressly
  allowlisted administrator email.
- **Cloudflare Access itself must offer GitHub as the ONLY login provider**
  for this application, and restrict the policy to the owner's authorized
  GitHub identity. The signed email by itself does not prove which IdP
  Access used. Access policy enforcement is essential.
- No FND username, password, password reset service, login cookies or user
  database is added by the project. Cloudflare Access owns its own cookies.
- Missing or invalid settings cause all admin routes to respond with 404.
  Signed identity failure causes 403. No public stats endpoint exists.
- /v1/event and /health are unchanged, including their anonymous-only
  data rules. The public site must never need admin login to record counters.

## Owner configuration after reviewing this PR

1. Confirm the account's Cloudflare Zero Trust Free allowance, MFA on both
   Cloudflare and GitHub, and the current supported login methods. Avoid
   paid upgrades. Leave the public Namecheap/GitHub Pages setup unchanged.
2. Configure a GitHub identity provider in Cloudflare Zero Trust. If the
   current account cannot offer **GitHub-only login** for an Access
   application covering the existing workers.dev Worker, stop and reassess
   rather than substituting email OTP or another identity provider.
3. Create a Cloudflare Access application scoped only to the private
   /admin path group of the Worker URL. Set its policy to authorize just
   the owner's GitHub account, and disable other login providers for this
   application. Do not protect /v1/event or /health by mistake. Note the
   **Application Audience (AUD)** tag and the account's Access team domain.
4. After CI and security review, deploy the reviewed Worker code using a
   restricted short-lived Cloudflare API token in Codespaces. Do not paste
   the token in Git, logs or chat.
5. In Cloudflare's secret settings for this Worker, configure:

       ACCESS_TEAM_DOMAIN   = your-team.cloudflareaccess.com
       ACCESS_APP_AUD       = the application audience hex tag
       ADMIN_ALLOWED_EMAIL = the sole admin email authorized by Access

   These are Worker environment secrets, NOT fields in wrangler.toml,
   source code, an HTML page or a URL. The current app expects one
   administrator. Secrets may alternatively be set using the Wrangler
   'secret put' command after authenticating via an environment token.
   Re-deploy if needed for the secrets to bind.
6. Verify in an incognito window and with a different GitHub account
   that the private dashboard, its script and API refuse access. Then
   verify that your authorized GitHub account opens the dashboard and
   reads only aggregate counts. Confirm /health still returns OK and
   public analytics events still record correctly.
7. Bookmark the private dashboard address instead of linking it publicly.
   To disable the feature in an emergency, remove the required Worker
   secrets; /admin then fails closed with 404. Revoke the Cloudflare API
   deployment token after setup.

Cloudflare's Access availability, provider choices and Free-plan limits
can change; verify them in the actual dashboard before configuration.

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
agreed. A separate Pages build publishes approved clues to the public
browser crossword generator.
