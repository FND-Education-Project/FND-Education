# FND Education Project — privacy-first aggregate counters

**Status (2026-10-16): Worker and D1 deployed and tested.** The
public GitHub Pages site does **not** send analytics until the separate
website-activation PR is reviewed, merged and deployed. This is an optional
first-party usage counter, not a third-party analytics product or a
traditional always-on server.

## What it measures

The free GitHub Pages site remains the site host, and Pagefind stays local
in the browser. A Cloudflare Worker receives just two fixed labels per
request: event and broad section. D1 stores daily counts only.

Events: page_view, search_used, search_result_click, pdf_download,
puzzle_download, not_found.

Sections: home, course, reference, glossary, puzzles, booklets, search,
contact, other.

- page_view is a **page load**, not a unique person or even a visit.
- search_used is a Pagefind search initiated, with one-second debouncing.
- search_result_click is a search-result click, never the clicked URL.
- pdf_download and puzzle_download count PDF/ZIP **link clicks**, not
  guaranteed completed downloads.
- not_found counts rendered not-found pages.

There is no stored row for individual actions, no search terms, complete
paths, query strings, click destinations, form inputs, referrers, IPs,
user agents, cookies, session IDs, or fingerprints. Nothing identifies or
tracks a person across pages.

**Important qualification:** Cloudflare, like any host, must process
network addresses and other connection information to handle HTTP. The
application deliberately does not read or store that metadata. Review
Cloudflare's own operational logging and privacy terms before deploying.

The totals are not tamper-proof (anonymous sites can receive bots), and
privacy tools may block requests. Neither unique people nor unique visits
are measured.

## Cost and maintenance

Cloudflare Workers + D1 was the previously preferred low-maintenance,
serverless candidate for this project. The code is intended for a very
small workload on a free allowance, but hosting company prices, quotas and
eligibility rules are **not guaranteed for one or two years**. Recheck the
current plan, whether payment details are required, and D1 limits before
creating the service. Do not enable paid logs, optional monitoring,
subscriptions or plans without explicit approval.

There is no visitor tracking dashboard or public metrics API. Initially
review totals using the private Cloudflare D1 dashboard. A future moderated
forum or survey service requires its own permissions, moderation and privacy
review and should not share this anonymous event table for personal data.

## Deployment status and site activation

**Cloudflare backend — already deployed and tested, not a future setup task:**

- Worker: `fnd-aggregate-metrics`
- HTTPS endpoint: `https://fnd-aggregate-metrics.fnd-aggregate-metrics.workers.dev`
- Health: `https://fnd-aggregate-metrics.fnd-aggregate-metrics.workers.dev/health`
- Remote D1 database: `fnd-aggregate-analytics`, with `daily_counts` table.
- The non-secret D1 database ID is stored in `wrangler.toml`.
- A controlled POST to `/v1/event` returned HTTP 204, and the daily
  aggregate was verified in the D1 console. Its test record was then removed.
- These checks establish a working backend; they do not establish that
  traffic from the public website is already being counted.

**Activation requires two distinct reviews/merges, in order:**

1. Merge the approved home-page privacy notice (PR #142), which introduces
   `home-privacy` immediately below the three landing-page cards. This
   alone does not enable analytics.
2. Review and merge the separate activation PR. It sets `analytics_endpoint`
   in `web/_config.yml` to the deployed Worker URL. The default layout
   already loads `analytics.js` only when this setting is present. The
   notice switches automatically from future to present tense. A CI guard
   requires the privacy notice when analytics are enabled.
3. After the published GitHub Pages build updates, visit the site and
   inspect the private D1 console for new grouped counts. Do not expect
   unique users or search terms, which are deliberately not collected.

**Operational credentials and redeployment:** Wrangler uses a restricted
Cloudflare API token held in a secure password manager. In Codespaces it
can be entered without terminal echo using
`read -rsp "Cloudflare API token: " CLOUDFLARE_API_TOKEN; echo; export CLOUDFLARE_API_TOKEN`.
The environment variable is scoped to the current terminal; when it
expires, Wrangler may fall back to browser OAuth, which was unreliable in
Codespaces. Never paste a token into Git, logs or chat. For future approved
code redeployment only, run `npx wrangler deploy` in this folder after
authenticating. Do not recreate the existing D1 database or rerun schema
initialization to enable website analytics.

The Worker explicitly rejects unrecognized input, rejects unknown browser
origins, and has no public read or administration endpoint. Origin checks
reduce accidental cross-site use but are **not** a proof against malicious
automated POST requests. Deploy appropriate provider rate controls as
needed, without adding visitor identifiers.

Privately inspect D1 in the Cloudflare console with:

    SELECT day, event, section, total FROM daily_counts
    ORDER BY day DESC, event, section;

Or calculate monthly totals:

    SELECT substr(day, 1, 7) AS month, event, SUM(total) AS total
    FROM daily_counts GROUP BY month, event ORDER BY month DESC, event;

## Private statistics dashboard (not yet deployed)

The optional /admin dashboard code is built in src/admin-dashboard.mjs
and src/worker.mjs. It is OFF by default: without Access application
configuration it returns HTTP 404. With valid settings, every admin
HTML, client-script and aggregate API response requires a cryptographically
verified Cloudflare Access JWT for the expressly allowlisted administrator.
This PR does not redeploy the Worker or configure Access. Only the account
owner can perform that step.

The dashboard reads grouped D1 counts for 7, 30 or 90 days. It never stores
individual visitor activity or an administrator session in D1. See
ADMIN-DASHBOARD.md for the GitHub-only security checklist.

## Tests

From repository root:

    node --test tools/analytics/cloudflare/tests/worker.test.mjs
    node --check web/assets/js/analytics.js
    node --check web/assets/js/search.js

No third-party runtime npm packages or site user accounts are required.
