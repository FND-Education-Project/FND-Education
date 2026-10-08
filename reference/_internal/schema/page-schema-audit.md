# Page-Level Structured-Data Audit

**Status:** Internal audit for Stage 2 on the `schema-page-level` branch.

## Scope

This stage adds conservative page-level Schema.org nodes on top of the Stage 1 site-wide graph and glossary schema.

Included:

- `WebPage`
- `CollectionPage`
- stable page `@id` values
- canonical page URLs
- page titles and existing descriptions
- `isPartOf` → site `WebSite`
- `publisher` → FND Education Project `Organization`
- conservative `about` → canonical FND `MedicalCondition`
- structural `hasPart` relationships for real page collections
- glossary page `mainEntity` → glossary `DefinedTermSet`

Explicitly deferred:

- `Article`
- `MedicalWebPage`
- breadcrumb schema
- page-specific medical entities inferred from prose
- `mentions`
- citation / `ScholarlyArticle` relationships
- audience schema
- author / reviewer schema
- medical-review dates

## Governing policy

The machine-readable policy is:

`reference/_internal/schema/page-schema-policy.json`

The policy intentionally uses only two page types.

### WebPage

Used for substantive leaf pages and ordinary project pages, including:

- course lessons
- diagnostic and recovery overviews
- individual diagnostic and recovery techniques
- diagnostic concepts
- co-occurring-condition pages
- biopsychosocial-experience pages
- cross-cutting Reference topics
- recovery guide
- About
- Contact
- Search

### CollectionPage

Used only when the primary purpose is to organize a collection, including:

- site home
- Course landing
- module landings
- Reference landing and indexes
- diagnosis and recovery collection pages
- diagnostic technique inventories
- co-occurring and biopsychosocial collection landings
- glossary
- booklets
- puzzles
- sitemap

A supported page kind may exist in the policy even when no current page instantiates it. A newly discovered page kind without a policy entry fails generation.

## Authority rule

`MedicalWebPage` is not used merely because a page contains medical information.

It remains reserved for a later authority/review model with an explicit signal strong enough to justify the classification.

`Article` is also not used simply because content is long or substantive. A future article type should require a genuine authored editorial object and appropriate publication metadata.

## Page relationships

### Site membership

Every page node contains:

- `isPartOf` → `/#website`
- `publisher` → `/#organization`
- `inLanguage`: `en`

### About FND

The canonical FND `MedicalCondition` is used as `about` only where the page's placement makes that relationship clear without interpreting prose:

- all Course pages
- all Reference pages
- home
- glossary
- booklets
- puzzles

It is deliberately omitted from:

- Contact
- About the Project
- sitemap
- Search

No narrower medical entity is inferred from body text in this stage.

### Collection hierarchy

`hasPart` comes only from explicit route structure, never from scraping links.

Examples:

- Home → Course, Reference, Glossary, Booklets, Puzzles
- Course → modules
- Module → lessons
- Reference → major Reference collections and cross-cutting topics
- Diagnosis → diagnostic concepts, index and symptom overviews
- Diagnostic concepts → individual concept pages
- Diagnostic index → symptom diagnosis overviews
- Diagnostic technique inventory/collection → technique pages
- Recovery → guide, index and symptom recovery overviews
- Recovery index → symptom recovery overviews
- Recovery technique collection → technique pages
- Co-occurring conditions → individual condition pages
- Biopsychosocial experiences → individual experience pages

Collection relationships are generated from page kinds, symptom slugs and route structure already used by the site generator.

### Glossary

The glossary page points to the existing `DefinedTermSet` through `mainEntity`.

The 109 glossary entries remain `DefinedTerm` nodes. This stage does not convert them into medical entities.

## No canonical Markdown metadata added

Stage 2 does not require schema fields in authored Markdown.

Python reads:

- existing generated page kinds
- route structure
- generated title/description front matter
- the internal page-schema policy

The generated page schema is written to:

`web/_data/generated/page_schema.json`

and rendered through the existing single JSON-LD block.

## Validation

Generation fails when:

- a discovered page kind has no policy type;
- a required resource route is missing from policy;
- page route/type maps disagree;
- a generated page has no title;
- `hasPart` points to an unknown route;
- generated `hasPart` would be placed on a non-`CollectionPage`.

Built HTML validation checks:

- exactly one JSON-LD block;
- existing Stage 1 `Organization`, `WebSite` and FND `MedicalCondition`;
- exactly one page node matching the current canonical page `@id`;
- rendered page node exactly matches the generated page-schema object;
- page type is only `WebPage` or `CollectionPage`;
- `Article` and `MedicalWebPage` are absent;
- existing glossary `DefinedTermSet` and all 109 `DefinedTerm` nodes remain valid;
- glossary page `mainEntity` points to the glossary term set.

## CI result

Draft PR #119 was used for production-equivalent validation.

The first run intentionally failed on an over-strict policy check because `diagnostic-techniques-home` is a supported page kind but has no current page instance. The generator was corrected so supported-but-unused kinds are allowed, while newly discovered unclassified kinds still fail.

The corrected full run passed on October 8, 2026:

- site preparation: passed
- generated-source validation: passed
- Jekyll production build: passed
- reviewed subject-search metadata: passed
- Pagefind: passed
- rendered built-artifact validation: passed
- public routes: **428**
- Pagefind pages indexed: **428**
- structured-data pages checked: **429**
- glossary `DefinedTerm` nodes checked: **109**
- built HTML files checked: **430**

## Deferred next decisions

The next schema work should be considered separately rather than automatically inferred:

1. Whether to expose narrower page subjects from the controlled subject index.
2. Whether selected pages genuinely qualify as `Article`.
3. What explicit authority/review signal would justify `MedicalWebPage`.
4. Citation relationships and `ScholarlyArticle` nodes.
5. Audience schema.
6. Breadcrumb schema.
