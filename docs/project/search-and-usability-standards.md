# Search and Usability Standards

<!-- NAV-BREADCRUMB:START -->
[Home](../../README.md) › Project Documentation › **Search and Usability Standards**
<!-- NAV-BREADCRUMB:END -->

A major goal of FND Education is to make information easy to find, understand, revisit, and share.

## Page requirements

Every substantive educational page will include:

- a plain-language title;
- relevant clinical terminology and common synonyms;
- a short summary near the top;
- the standard page sections;
- repeated on-page links to the person, supporter, clinician, and research sections;
- short sections with descriptive headings;
- important terms defined where they first appear;
- links to related topics;
- a dedicated support-person section;
- a practical “What can I try at home?” section;
- a “When should this be medically reassessed?” section;
- references to the research and guidance used;
- a last-reviewed date;
- descriptive alternative text for meaningful images;
- transcripts or captions for audio and video;
- wording that avoids unnecessary jargon and stigma.

## Search terminology

Pages should include both modern and historically common terms when that helps people find reliable information. Examples include:

- Functional Neurological Disorder — **FND**
- Functional Neurological Symptom Disorder — **FNSD**
- Functional seizures — **dissociative seizures**, **psychogenic nonepileptic seizures**, **PNES**
- Functional Movement Disorder — **FMD**
- Functional Cognitive Disorder — **FCD**
- Functional weakness — **functional limb weakness**, **functional paralysis**

Older terms should be labelled historical, outdated, disputed, or potentially stigmatizing when appropriate rather than silently treated as preferred terminology.

## Navigation and retrieval

- Use one canonical page for each main subject and redirect or cross-link synonymous terms to it.
- Give files and URLs stable, descriptive names.
- Link related symptoms, treatments, safety topics, and support-person material in both directions.
- Make major subjects reachable through the course, symptom pathways, glossary, and search.
- Avoid duplicating full explanations across several pages; summarize and link to the canonical explanation.
- Use meaningful link text that explains the destination.
- Keep summaries and practical actions easy to relocate on a return visit.
- Show the four standard section links in two predictable places: once near the top, before the first audience section, and once after the clinician section, before contextual navigation and the research or resources section.

### Site-wide navigation pattern

- Every reader-facing Markdown page should have a compact breadcrumb immediately below its title so a reader arriving from search can see where the page sits in the project.
- Every page should provide the four predictable global destinations: **Home**, **Course**, **Reference Library**, and **Site Map**.
- Contextual navigation belongs **below all other reader-facing content and immediately before the page's research, evidence, or sources section**. If a page has no source section, place it at the end of the page.
- Each module overview should provide one forward contextual link to the first focused page in that module.
- Each course article should provide one forward contextual link. It should lead to the next page in the module, or from the module's last page to the next module overview. The last page of Module 23 should return to the course index.
- Breadcrumbs and the global Course link provide the route back to a module overview or the course index; do not repeat previous-page, previous-module, or module-index links in the contextual block.
- Symptom reference pages should link to their collection index, the corresponding diagnostic or recovery page, and the most directly related course page where one exists.
- Deeper collections should use contextual links that reflect their real hierarchy rather than treating a numbered booklet or subdocument as a numbered symptom page.
- Maintain the human-readable root [`SITEMAP.md`](../../SITEMAP.md) whenever a reader-facing page is added, moved, renamed, or removed. It should use collapsible nested sections so the whole project can be explored without displaying the entire hierarchy at once.
- `SITEMAP.md` is the reader navigation map. A machine-readable `sitemap.xml`, when used for search engines, serves a different purpose and does not replace it.

Use the [repository change and page maintenance policy](repository-change-and-page-maintenance-policy.md) as the operational checklist whenever a course or reference page is added, removed, renamed or moved.

<!-- NAV-CONTEXT:START -->
**Project:** [Project status](project-status.md) · [Core principles](core-principles.md)

**Navigate:** [Home](../../README.md) · [Course](../../course/README.md) · [Reference Library](../../reference/README.md) · [Site Map](../../SITEMAP.md)
<!-- NAV-CONTEXT:END -->
