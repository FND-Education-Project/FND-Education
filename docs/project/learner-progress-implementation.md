# Local learner-progress implementation and account rollout

## Current scope: browser-local progress

This is a **guest-friendly, no-account-required** progress layer. The canonical
course Markdown stays unchanged. The website generator publishes
`/assets/data/course-progress.json` directly from its canonical module and
lesson discovery. A local JavaScript enhancement builds a collapsible view of
the six course parts and 23 modules. The list of lessons adapts to curriculum
updates without requiring hand-maintained JavaScript lesson titles.

Progress states:

- **Not started:** the lesson has not been visited or manually completed.
- **Visited:** a learner opened the lesson, regardless of time spent or scrolling.
- **Completed:** the learner explicitly checked Complete or used Mark complete
  and continue. They can uncheck completion, and revisiting does not recheck it.
- Only the 74 focused lessons count toward totals. Module overview pages,
  reference pages, crosswords, and other activities are not prerequisites.

Navigation affordances:

- Course landing page: expandable parts and modules, a completion total,
  a native progress bar, direct lesson links and reversible checkboxes.
- Lesson pages: completion control, current status, and an optional
  Mark complete and continue button pointing to the existing next course page.
- Lesson and module-navigation links: contextual visited/completed markers
  where they assist readers. Avoid decorating every editorial inline link.
- Home: Continue where you left off appears after visiting a lesson.
- Site menu: My Progress points to the course overview.
- If JavaScript or the manifest fails, the existing static course
  index, lesson text and Previous/Next navigation remain in place.

## Local data and privacy

The browser saves only a versioned object containing stable lesson IDs,
visited/completed Boolean flags, and the most recently opened lesson ID in
localStorage under `fnd-course-progress-v1`.

- No name, email, device identifier, scroll tracking, time-on-page, medical
  symptom record, provider credential, or free-text answer is saved.
- No course progress leaves the browser, and nothing is joined to
  anonymous analytics.
- Clearing site data, switching devices/browsers, or using private browsing
  can lose progress. If storage is blocked, status works temporarily in the
  active page, with a visible warning.
- Learners can clear local progress from the overview, with confirmation.
- URLs are derived only from validated, same-origin published course routes.
  Saved local data is treated as untrusted and sanitized.

No external account / cross-device sync is live. Do not imply otherwise in
public UI or the privacy notice.

## Future optional accounts — security gates

Follow the separate `tools/analytics/cloudflare/ACCESS-AND-PROGRESS-PLAN.md`
before enabling any learner sign-in. Do not deploy an empty or
non-functioning Google, Apple, Amazon, or Facebook sign-in button.

Next stage: provision **separate learner** D1 data/access controls and Worker
endpoints, independent from anonymous analytics and Cloudflare Access admin
authorization. Select provider integrations after validating current free
allowances, terms, privacy implications, redirects and registration requirements.

Use supported OIDC/OAuth flows with PKCE, CSRF state, nonce where relevant,
strict token issuer/audience/signature verification, exact redirects and
secure HttpOnly sessions. Authorize all reads/writes using a verified learner
identity, not a client-provided learner ID. Link providers only with explicit
proof of control of both accounts. Offer export, deletion, and deliberate
device-to-account transfer and merge after tested conflict handling.

Do not silently upload historical browser-local progress at sign-in; ask first.
Keep any learner's course history out of public analytics. Account recovery
belongs to their provider; the site must not store learner passwords.

## Validation and accessibility checklist

Automated site build:

1. Run `python tools/site/prepare_site.py`.
2. Run `python tools/site/validate.py`. This now asserts the generated
   manifest includes every published module and lesson URL once, uses
   unique stable lesson IDs and includes valid titles.
3. Build Jekyll and validate the built artifact via the existing Pages CI.

Manual browser review before merge:

- Guest visiting a lesson changes Not started to Visited, never Completed.
- Checking and unchecking a lesson works from both overview and lesson page.
- Revisiting an unchecked lesson does not mark it complete again.
- Navigating back from a lesson preserves completed status and open groups.
- Clear my progress resets status and Continue links after confirmation.
- Refresh and another tab show saved status; private/blocked storage shows
  an appropriate warning.
- Course overview still navigates with no JavaScript or missing manifest.
- Keyboard, screen reader, focus retention, text zoom, dark/light themes and
  narrow phones remain usable.
- Anonymous metrics have no new learner-related events or identifiers.

## Future usability refinements

Optional, after feedback: explicit JSON export/import for guest backup;
a review activity link beside each module, with no scoring requirement;
and deliberate device-to-account sync. Do not make puzzles a completion
requirement or use lesson completion as a health outcome.
