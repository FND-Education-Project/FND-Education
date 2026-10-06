# Functional limb weakness: first diagnostic expansion

September 26, 2026. Working draft; clinical, lived-experience and accessibility review remains pending.

**October 6, 2026 update:** At the project lead’s request, personal accounts and the human-draft notice have been removed from the public diagnosis page. The complete pre-edit source and attributed passages are preserved in the [internal human-content archive](../../reference/_internal/diagnostic-signs/human-content-archive.md). The preservation statements below describe the original September expansion, not the current publication state.

## Scope and migration

This implements the first stage of the [preparation plan](diagnostic-expansion-preparation.md) using the [authoring structures](diagnostic-page-authoring-structures.md). It adds one detailed technique, Hoover’s sign, three shared explanations and their navigation overview. The original sixteen-entry inventory is retained separately. These are not sixteen newly validated tests or sixteen completed expansions; the historical [170-entry baseline](diagnostic-expansion-baseline.md) remains unchanged.

Work is based on `migrate-to-pages` at `dd4598f`. Canonical reference Markdown remains under `reference/`. The current Pages generator publishes the course, not the reference collection; this change does not claim that new reference routes are deployed. Root sitemaps retain their existing source-document convention. Course generation remains at 98 documents (course landing, 23 module landings and 74 lessons).

## Content ownership and preservation

| Material | Current home and treatment |
| --- | --- |
| Symptom explanation, time course, safety and care-team awareness | [Weakness overview](../../reference/diagnostic-signs/01-functional-limb-weakness.md), with short Quick Reference and audience sections |
| Both project-lead quotations | Preserved verbatim in the symptom overview, including the distinction between the leg sign and an adapted arm demonstration |
| All sixteen inventory entries and original source anchors | [Inventory](../../reference/diagnostic-signs/functional_limb_weakness/technique-inventory.md); legacy anchors retained on the symptom page |
| Hoover anatomy, examination outline and media brief | [Hoover’s sign](../../reference/diagnostic-signs/functional_limb_weakness/01-hoovers-sign.md), organized by clinician topics with accessible definitions |
| Positive diagnosis and investigations | Shared [positive diagnosis](../../reference/diagnostic-concepts/01-positive-diagnosis.md) and [investigations](../../reference/diagnostic-concepts/03-tests-and-investigations.md) pages |
| Assessment versus disability | New shared topic [10: assessment and everyday function](../../reference/diagnostic-concepts/10-assessment-and-everyday-function.md), extending the original nine-topic plan under the clinician-awareness guidance |
| Episodic recovery instructions and supporter cues | [Paired recovery overview](../../reference/recovery-techniques/01-functional-limb-weakness.md#episodic-weakness-and-supporter-cues); diagnostic safety remains local |

The remaining fifteen entries keep their original brief summaries and evidence boundaries. Their proposed disposition in the preparation plan still applies, including shared or paralysis-owned topics and the arm-drop caution. Expansion proceeds one technique at a time.

## Evidence and media limits

Existing citation IDs are reused. Bennett et al. (2021) and Dolbow et al. (2025) were read in full; the occupational-therapy authors’ supplementary assessment guidance, Stone et al. (2010) abstract and NHS stroke guidance were also checked. The original McWhirter et al. (2011) full text was not retrieved: the institutional abstract supports the reported cohort and accuracy figures, while examination wording was cross-checked against the reviews. Full-text review of that primary study remains outstanding. The targeted search did not establish a newer large prospective replication; it was not a systematic review.

The existing Hoover illustration is preserved unchanged but not embedded as a procedural guide. The panels do not clearly depict hand placement under the affected heel and resistance at the opposite thigh. Correct the illustration and verify attribution before using it for examination teaching.

Diagnostic findings are not presented as measures of disability, dependable daily performance or assistance needs. Everyday impact is discussed across clinical professions, with variability, repeated activity, quality of life and mental health addressed without assigning a psychological cause.

## Review gates

Clinical review must check the examination sequence, suitability and limitations, primary full text, source interpretation and any future illustration. Human review must check clarity, lived experience and accessibility. Reference generation and published-site navigation require separate migration implementation before these drafts appear as rendered reference pages.

## Validation completed

Relative links and Markdown anchors passed across all 18 changed or new files. Both project-lead quotation lines match the original exactly; the inventory retains all sixteen headings. Sitemap XML parses without duplicate URLs. The course generator produced all 98 expected documents. Whitespace checks passed with the existing XML CRLF convention respected. A full Jekyll rendering was not run because Bundler is unavailable in this environment; rendered reference-site behavior is not claimed.
