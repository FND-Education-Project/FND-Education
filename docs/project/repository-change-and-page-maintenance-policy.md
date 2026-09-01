# Repository Change and Page Maintenance Policy

<!-- NAV-BREADCRUMB:START -->
[Home](../../README.md) › Project Documentation › **Repository Change and Page Maintenance Policy**
<!-- NAV-BREADCRUMB:END -->

Use this checklist whenever a course or reference page is added, removed, renamed or moved. Open only the policy point needed for the change. The top-level numbered points are the only drill-down controls.

> **Basic rule:** A page is not fully added, removed, renamed or moved until its navigation, indexes, counts, cross-links, evidence records and site map agree with the change.

## Course modules and pages

<details>
<summary><strong>1. Add a course module</strong></summary>

1. Create the numbered module folder in the correct course part.
2. Add a short `README.md` module overview and the planned focused pages, following the structure and audience sections used by neighbouring modules.
3. Add forward navigation from the previous module’s last page to the new overview, through every new page, and onward to the next existing module when there is one.
4. Add the module and every page to the [course index](../../course/README.md), [site map](../../SITEMAP.md), detailed syllabus and the relevant file in `docs/project/syllabus/`.
5. Update every stated module, overview, focused-page and total-page count in the main README and project documentation.
6. Add or update glossary terms, citation records, research notes and related reference-page links introduced by the module.

</details>

<details>
<summary><strong>2. Add a focused course page to an existing module</strong></summary>

1. Use the next logical numbered filename unless an approved reordering requires renaming later pages.
2. Add the page to its module overview, the course index, the site map, the detailed syllabus and the module’s syllabus file.
3. Update the previous and next reading links so the module remains one uninterrupted route.
4. Update focused-page and total-page counts wherever they appear.
5. Add the page’s research package, compact citation table and central citation-index links before changing its evidence-review status.
6. Add relevant glossary and reference-library cross-links without duplicating the full explanation.

</details>

<details>
<summary><strong>3. Remove, rename or move a course module or page</strong></summary>

1. Decide whether the old path needs a redirect or short moved-page notice so existing links are not silently broken.
2. Remove or change the entry in the module overview, course index, site map, detailed syllabus and relevant module syllabus file.
3. Repair the previous and next reading links on both sides of the change.
4. Search the whole repository for the old title, filename and path; update every course, reference, glossary, research and project-documentation link.
5. Update all affected module and page counts.
6. Keep stable citation IDs even when their last current-use link is removed; record that the source is not currently used rather than renumbering later sources.

</details>

## Reference pages

<details>
<summary><strong>4. Add a diagnostic-sign reference page</strong></summary>

1. Confirm that the page describes positive clinical evidence and its limits, not a self-diagnostic test or diagnosis by exclusion.
2. Add a numbered page in `reference/diagnostic-signs/` using the three audience sections, emergency or reassessment guidance, media brief and standalone citation table.
3. Add it to the diagnostic collection index, reference-library index and site map.
4. Pair it with the matching recovery page, or state why no recovery page is ready and link to the closest safe material.
5. Update the former last page’s navigation and give the new page a previous-page link; repair both directions if the page is inserted between existing pages.
6. Update reference-page counts, scope statements, glossary terms, related course links and the central citation index.

</details>

<details>
<summary><strong>5. Add a recovery-technique reference page</strong></summary>

1. Add a numbered page in `reference/recovery-techniques/` paired to the diagnostic page.
2. Separate research-supported, consensus, emerging and community-reported material; state when evidence applies only to a broader programme or another symptom group.
3. Include practical person, supporter and clinician sections, episode or flare guidance, safety limits, reassessment triggers and continuing support when improvement is limited.
4. Add the page and every indexed technique to the recovery collection index and master technique index.
5. Add it to the reference-library index and site map, then update the former last page and all relevant cross-links.
6. Update reference-page counts, scope statements, central citations and any community source notebook affected by the new material.

</details>

<details>
<summary><strong>6. Remove, rename or move a reference page</strong></summary>

1. Decide whether the old path needs a redirect or short moved-page notice.
2. Repair collection-order navigation on the pages before and after it.
3. Update its paired diagnostic or recovery page, collection README, reference-library README, master technique index and site map.
4. Search the repository for the old title, filename and path; update course, glossary, research, community-notebook and project-documentation links.
5. Update all affected collection counts and scope statements.
6. Preserve stable citation IDs and exact source history even if a source becomes unused.

</details>

## Navigation, indexes and counts

<details>
<summary><strong>7. Change numbered-page navigation</strong></summary>

1. Treat collection order as a chain: each page points to the correct previous and next destination.
2. When appending a page, replace the former last page’s end-of-collection state with a `Continue` link to the new page.
3. Give the new last page a `Previous in this collection` link and keep its collection, paired-page, course and global navigation links.
4. When inserting or removing a page, check both neighbouring pages rather than editing only the changed page.
5. If filenames are renumbered, search for every old numbered path and repair incoming links before the change is complete.

</details>

<details>
<summary><strong>8. Update indexes, maps and stated totals</strong></summary>

1. Update the closest module or collection README first.
2. Update the course or reference-library index, main README and site map.
3. Update the detailed syllabus, planned repository structure, project status and other documents that describe the changed scope.
4. Update master lists such as the technique index, glossary and citation index when their subject matter changes.
5. Search for the old count and the old scope phrase, including forms such as “all 13,” “same 13,” “13 presentations” and “26 pages.”
6. Use exact current totals rather than words such as “about” when the repository can be counted.

</details>

## Evidence and community material

<details>
<summary><strong>9. Add, change or stop using a research source</strong></summary>

1. Follow the [research and citation policy](research-and-citation-policy.md) and [evidence standard](evidence-standard.md).
2. Assign each new source the next stable `FND-CIT` ID; never renumber or reuse an existing ID.
3. Add a full entry and a current-use link to the central [citation index](../../research/citation-index.md).
4. Give every standalone educational page its own compact citation and link the stable ID back to the index.
5. State the source type, population, limitations and whether support is direct, broader, adjacent, consensus-based or emerging.
6. If a source is no longer used, remove its page-use links but retain its stable index record and note that it is not currently used.

</details>

<details>
<summary><strong>10. Add, change or remove a community quotation</strong></summary>

1. Use only material that is publicly accessible and link directly to the source post or comment where possible.
2. Keep quotations short, exact, de-identified in the page text and accompanied by the context needed to avoid changing their meaning.
3. Label every quotation as lived experience, not proof, medical advice, mechanism or a cure claim.
4. Do not turn one person’s technique into a project **L** recommendation; the same basic practice needs at least two independent qualifying reports and a safety review.
5. Record conflicting, neutral and adverse experiences when they materially change interpretation; do not manufacture a balanced quote set when sources are missing.
6. Update the relevant community source notebook and remove a quotation if privacy, consent, accuracy, source stability or safety concerns cannot be resolved.

</details>

## Verification and review

<details>
<summary><strong>11. Run the pre-commit content check</strong></summary>

1. Search for old paths, titles, counts and scope wording.
2. Check every changed relative Markdown link and every new citation anchor.
3. Confirm paired diagnostic and recovery links work in both directions.
4. Confirm collection-order, breadcrumb, related-page and global navigation links.
5. Check that working-draft, review-status and evidence-search dates are accurate.
6. Run the repository’s available formatting, link and site-build checks, then review the rendered pages where layout may have changed.

</details>

<details>
<summary><strong>12. Record the change for human review</strong></summary>

1. In the commit or pull request, list pages added, removed, renamed or moved.
2. Name every index, count, navigation chain and policy document updated.
3. Summarize the evidence added and its main limitations.
4. Identify community quotations separately from research and note privacy or representativeness limits.
5. Record the checks run and any known gaps.
6. State which human, clinical, lived-experience, accessibility or privacy reviews remain pending; an automatically generated draft is not silently promoted to approved material.

</details>

*Policy created: September 1, 2026 · Repository-maintainer review pending*

<!-- NAV-CONTEXT:START -->
**Project:** [Project status](project-status.md) · [Core principles](core-principles.md) · [Research and citation policy](research-and-citation-policy.md)

**Navigate:** [Home](../../README.md) · [Course](../../course/README.md) · [Reference Library](../../reference/README.md) · [Site Map](../../SITEMAP.md)
<!-- NAV-CONTEXT:END -->
