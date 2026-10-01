# History and professional roles review — October 1, 2026

## Scope and ownership

Continues the interrupted “Next Recovery Symptom” task. The final handoff identified the history and professional-roles pages from PR #96, not the earlier diagnostic symptom pair. Base: 45fefa890e804273fd3aeafd0e661fefab204613. No human-authored course material changed. Both remain automatically generated drafts awaiting human review.

The history page owns a selective timeline and interpretation of milestones. The roles page owns concise profession-specific routing, retaining the requested specialty table, merged help/when paragraphs and search synonyms. Both use the existing reference-topic layout and topic menus; no new layout or duplicated symptom audience structure was introduced.

## Changes

- Register both explicit routes with the generator; reproduced the unclassified-reference failure before editing. Keep the public allowlist and internal exclusion intact.
- Complete local citation tables and stable source-use records. Add FND-CIT-0237–0242 for historical/criteria/model sources; retain all existing IDs.
- Link Hoover's original 1908 paper and contextualize historical terminology. Separate original reports from later historical interpretation.
- Distinguish primary and secondary outcomes in CODES and Physio4FMD. Explain the selected populations, multiple comparisons and pandemic exclusions proportionately.
- Date the AAN guideline's online/issue publication correctly and bound the 2026 sensory, tremor and communication findings.
- Add missing professional-role support and acute-care/FCD sources; qualify scope by local professional rules. Explain the actual conditional OT equipment recommendations without converting consensus into proof about aid withdrawal.
- Make specialty-table names jump to sections; repeat topic menus; move contextual navigation above Sources; use Home/Course/Reference/Site Map consistently. Fix the unmapped course-directory destination and contributor link.
- Add both pages under Reference in the source sitemap. Existing reference landing/index links and the Module 13 cross-link remain intact.

## Source access and limitations

Live bibliographic, abstract and indexed publisher/author records checked October 1, 2026. This was targeted verification, not an exhaustive systematic search.

- CODES: UCL author-repository abstract, including primary and secondary results and multiplicity statement (https://discovery.ucl.ac.uk/id/eprint/10100403/).
- Physio4FMD: PubMed abstract, including analysis population and pandemic exclusions (https://pubmed.ncbi.nlm.nih.gov/38768621/).
- OT: accessible author-manuscript Aids and Adaptations section, pages 14–15 in the PDF (https://openaccess.sgul.ac.uk/id/eprint/112209/6/OT%20Cons%20Rec%20for%20FND%20Revised%20Manuscript%20CLEAN%20COPY.pdf).
- Lehn, Baker, Rutten, sensory study and tremor synthesis: indexed author/publisher/NIH records and relevant excerpts. Some direct full-text attempts returned access errors; no claim of exhaustive full-text review.
- AAN: official guideline summary and publication record (https://pubmed.ncbi.nlm.nih.gov/41370742/).
- Communication review: publisher and PubMed record identified (https://pubmed.ncbi.nlm.nih.gov/42632320/); full methods not retrieved. Retained as a research milestone without a pooled-effect claim.
- Hoover: original publisher record/opening extract checked (https://jamanetwork.com/journals/jama/article-abstract/428015); not the later 1908 correspondence with the same title.
- Slater: original metadata; interpretation bounded by the later 2005 systematic review. Full historical-paper appraisal pending.
- Stone 2016: author-institution abstract/metadata; full chapter pending. Early timeline remains a selective later interpretation, not primary archival historiography.
- Stone 2011 and Edwards 2012: bibliographic/abstract and indexed discussion checks; distinguish proposed criteria and theoretical model from established facts.

## Validation and remaining review

Source generation and validation pass: 98 course pages, 272 Reference pages, 377 public routes; 17 internal Reference documents remain excluded. Both pages' relative destinations and rendered Markdown anchors checked with Pandoc. Existing heading and citation anchors retained. Whitespace checks pass.

Full Jekyll build and built-artifact validation run in GitHub Actions; Ruby/Bundler unavailable locally. Pandoc HTML was generated for link/structure checks, but browser screenshot review could not run because the installed Playwright package has no browser executable. Rendered desktop/mobile review remains pending. Human historical, clinical, professional-scope, lived-experience and accessibility review remain pending. Keep the pull request unmerged for Robert's review.
