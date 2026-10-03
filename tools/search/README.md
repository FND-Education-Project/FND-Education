# Search development

The website search has four layers:

1. **Pagefind** indexes the finished Jekyll site and provides dependable lexical search.
2. **Site structure** supplies high-confidence inherited subjects from known folders and route segments.
3. **The subject index** provides a controlled FND vocabulary and relationships.
4. **The embedding classifier** may add supplementary page and section subjects from that approved vocabulary.

The semantic layer does not generate reader-facing medical content and does not diagnose.

## Why structure comes first

The repository already knows many things with certainty.

For example, any page under:

```text
/reference/functional-limb-weakness/
```

belongs to the functional-limb-weakness subject.

Likewise, a route containing `/diagnosis/` inherits the FND-diagnosis context, and a route containing `/recovery/` inherits the FND-recovery context.

Those relationships are stored in:

```text
tools/search/structure-map.json
```

They do not consume an AI guess.

This prevents the embedding model from wasting its limited subject slots rediscovering information the site structure already provides.

## New substantive folders become subject candidates

A new top-level Reference folder is not silently turned into an approved search subject.

Instead, if a new folder appears under `/reference/` and no structural mapping exists for it, the classifier writes a proposal to:

```text
tools/search/subject-candidates.json
```

The candidate contains:

- the proposed ID,
- folder/route prefix,
- landing-page title,
- page count,
- and the child-page titles.

The candidate remains **needs-human-review**.

If approved, add it to both:

```text
tools/search/subject-index.json
tools/search/structure-map.json
```

If the folder is merely organizational, explicitly ignore it or map it to an existing approved subject instead.

The current `biopsychosocial-experiences` folder is the first real example of this workflow.

## Subject index

`subject-index.json` is the controlled search vocabulary.

`subject-index-review.md` is a human-readable review view.

Each approved subject may contain:

- a canonical label,
- a short definition,
- true or near-equivalent aliases,
- abbreviations,
- plain-language search phrases,
- reviewed misspellings,
- broader subjects,
- narrower subjects,
- and related-but-not-equivalent subjects.

Those distinctions matter. A related concept is not automatically a synonym.

## AI classification

The current classifier uses:

```text
BAAI/bge-small-en-v1.5
```

through FastEmbed.

It is an embedding model, not a generative medical assistant.

Its role is limited to matching page and section meaning against the already-approved subject index.

### Page subjects

After structural subjects are inherited, the embedding model may add up to two supplementary page subjects.

The default page similarity threshold is now:

```text
0.76
```

The earlier calibration run used 0.62 and effectively filled all three available subject slots on every page. The stronger threshold is intentionally more selective.

### Section subjects

H2 and H3 sections may also be classified for review, using a default threshold of 0.76.

Repeated structural headings are excluded from semantic section classification, including audience headings, Research and Sources, citation tables, Crosswords, and similar template sections.

Section classifications remain available in the cache/report, but are **not flattened into page-wide Pagefind metadata**.

Normal Pagefind still indexes the visible section text and headings and can return anchored sub-results.

## Pagefind weighting

Semantic metadata is tiered.

Current intent:

- normal Pagefind title relevance: strongest,
- deterministic structural subjects: strong semantic help,
- structural lay phrases: moderate help,
- AI-added page subjects: smaller help,
- AI lay phrases: smaller again,
- reviewed misspellings: weakest help.

Search metadata is removed in `processResult` before rendering, so visitors do not see internal `Subject_*` fields in results.

## Persistent cache

`subject-cache.json` stores AI classifications.

A cache entry is invalidated when relevant inputs change, including:

- complete indexed page content,
- page semantic context,
- section content,
- subject index,
- structure map,
- model,
- score thresholds,
- or classifier guardrails.

A new page is also stale because it has no AI cache entry.

Structural inheritance is recalculated every build and does not depend on the AI cache.

## Calibration baseline

The first full run classified 380 pages with:

```text
page threshold: 0.62
section threshold: 0.64
maximum page subjects: 3
maximum section subjects: 2
```

That report was useful as a calibration dataset, but the generated cache is version 2 and is intentionally incompatible with the new structural classifier.

The new classifier uses cache version 3.

Before running the new classifier in an existing Codespace, preserve the old calibration files if desired.

## Full Codespaces rebuild

From the repository root:

```bash
bundle install
python -m pip install -r tools/search/requirements.txt
python tools/site/prepare_site.py
python tools/site/validate.py
bundle exec jekyll build --source web --destination _site

python tools/search/build_subject_metadata.py \
  --site _site \
  --all-stale \
  --report subject-search-report.json

npx --yes pagefind@1.5.2 --site _site
python tools/site/validate.py --built-site _site
```

Then serve the finished artifact directly:

```bash
python -m http.server 4000 --directory _site
```

Do not run another Jekyll build after Pagefind unless Pagefind is run again afterward, because Jekyll can recreate `_site` and remove the generated `_site/pagefind/` bundle.

## Review after the next full run

Inspect:

```bash
git diff -- tools/search/subject-cache.json
cat tools/search/subject-candidates.json
```

and review:

```text
subject-search-report.json
```

The most useful checks are:

- inherited subjects are correct,
- AI subjects are genuinely supplementary,
- irrelevant second/third guesses are reduced,
- template headings no longer produce repeated false section concepts,
- new-folder candidates are appropriate,
- and ordinary searches return a smaller, more useful result set.

## Later incremental runs

After the new full cache is accepted, omit `--all-stale`.

```bash
python tools/search/build_subject_metadata.py \
  --site _site \
  --report subject-search-report.json
```

Only stale pages are processed. The default local batch size is eight pages.

A full one-shot refresh can still be requested with `--all-stale`.

## GitHub Pages behavior during testing

For now, GitHub Pages CI runs the classifier in:

```bash
--cache-only
```

That means normal CI:

- recalculates deterministic structural subjects,
- detects new unmapped Reference folders,
- applies valid committed AI classifications,
- does not download the embedding model,
- and does not make new AI classification decisions.

After the new cache is reviewed, the Actions workflow can be changed to reassess only new or changed pages and persist reviewed cache updates.

## Future LLM-assisted subject discovery

The current new-folder proposal is structural and reviewable. It does not invent medical taxonomy.

A later generative-LLM discovery pass can enrich candidates by proposing:

- definitions,
- aliases,
- broader/narrower relationships,
- and related subjects.

Those proposals should remain review-only until approved into the controlled subject index.
