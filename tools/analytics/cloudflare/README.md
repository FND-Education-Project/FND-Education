# FND Education Project — privacy-first aggregate counters

**Status: NOT DEPLOYED.** This is an optional first-party usage counter,
not a third-party analytics product or a traditional always-on server.

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

## Future setup — requires your Cloudflare account

**Do not deploy merely to review this draft PR.**

1. Confirm a free eligible Cloudflare Workers + D1 plan under your own
   account. Check the provider's live prices and data-processing terms.
2. In Codespaces, change directory to tools/analytics/cloudflare.
3. Run: npx wrangler login
   Follow the browser authorization. Do not paste credentials into this
   repository or chat.
4. Run: npx wrangler d1 create fnd-aggregate-analytics
   Copy the returned *database ID*, not a secret, into wrangler.toml.
5. Run: npx wrangler d1 execute fnd-aggregate-analytics --remote --file=schema.sql
6. Run: npx wrangler deploy
   Test the returned Worker URL plus the /health endpoint.
7. On a deployment-approved branch only, add to web/_config.yml:

       analytics_endpoint: https://WORKER.SUBDOMAIN.workers.dev

   This optional setting causes the site to load analytics.js. Without it
   **nothing is sent** to Cloudflare by the browser script.
8. Check the public privacy notice, validate Pagefind, check the rendered
   site and confirm the proposed integration before merging/deploying.

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

## Tests

From repository root:

    node --test tools/analytics/cloudflare/tests/worker.test.mjs
    node --check web/assets/js/analytics.js
    node --check web/assets/js/search.js

No third-party runtime npm packages or site user accounts are required.
