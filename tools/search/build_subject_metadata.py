#!/usr/bin/env python3
"""
Build reviewable subject metadata for the generated FND Education Project site.

Search has three knowledge layers:

1. Site structure supplies high-confidence inherited subjects.
2. The approved subject index supplies controlled terminology.
3. The embedding model may add supplementary page/section subjects.

A new substantive top-level Reference folder that is not structurally mapped is
written to subject-candidates.json for human review. It is never silently added
to the approved subject index.

Codespaces full rebuild:
    python tools/search/build_subject_metadata.py \
        --site _site --all-stale --report subject-search-report.json

GitHub Pages CI:
    python tools/search/build_subject_metadata.py --site _site --cache-only
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable


DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"
DEFAULT_PAGE_SCORE = 0.76
DEFAULT_SECTION_SCORE = 0.76
DEFAULT_MAX_PAGE_SUBJECTS = 2
DEFAULT_MAX_SECTION_SUBJECTS = 2
DEFAULT_BATCH_SIZE = 8
CACHE_VERSION = 3
MAX_PAGE_CONTEXT_CHARS = 3200
MAX_SECTION_CONTEXT_CHARS = 1800

SEARCH_META_NAMES = (
    "fnd-structural-subjects",
    "fnd-structural-lay-phrases",
    "fnd-ai-subjects",
    "fnd-ai-lay-phrases",
    "fnd-search-misspellings",
    # Remove metadata emitted by the earlier experimental implementation too.
    "fnd-primary-subjects",
    "fnd-primary-lay-phrases",
    "fnd-section-subjects",
    "fnd-section-lay-phrases",
)

SEARCH_META_RE = re.compile(
    r"\s*<meta\s+name=[\"'](?:"
    + "|".join(re.escape(name) for name in SEARCH_META_NAMES)
    + r")[\"'].*?>",
    re.IGNORECASE | re.DOTALL,
)


@dataclass(frozen=True)
class Subject:
    subject_id: str
    label: str
    category: str
    definition: str
    aliases: tuple[str, ...]
    abbreviations: tuple[str, ...]
    lay_phrases: tuple[str, ...]
    misspellings: tuple[str, ...]
    broader: tuple[str, ...]
    narrower: tuple[str, ...]
    related: tuple[str, ...]

    @property
    def semantic_text(self) -> str:
        parts = [
            self.label,
            self.definition,
            *self.aliases,
            *self.abbreviations,
            *self.lay_phrases,
        ]
        return ". ".join(part.strip() for part in parts if part.strip())


@dataclass
class Section:
    anchor: str
    title: str
    level: int
    text_parts: list[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        return normalize_text(" ".join(self.text_parts))

    @property
    def semantic_text(self) -> str:
        return normalize_text(
            f"{self.title}. {self.text[:MAX_SECTION_CONTEXT_CHARS]}"
        )


@dataclass
class PageDocument:
    path: Path
    route: str
    title: str
    description: str
    body: str
    page_context: str
    sections: list[Section]


class PageExtractor(HTMLParser):
    SKIP_TAGS = {"nav", "script", "style", "form", "button", "footer"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_main = False
        self.skip_depth = 0
        self.title = ""
        self.description = ""
        self.body_parts: list[str] = []
        self.heading_tag: str | None = None
        self.heading_id = ""
        self.heading_parts: list[str] = []
        self.sections: list[Section] = []
        self.current_section: Section | None = None

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        tag = tag.lower()
        attributes = {
            key.lower(): (value if value is not None else "")
            for key, value in attrs
        }

        if tag == "meta":
            if attributes.get("name", "").lower() == "description":
                self.description = attributes.get("content", "").strip()
            return

        if tag == "main":
            self.in_main = "data-pagefind-body" in attributes
            return

        if not self.in_main:
            return

        if self.skip_depth:
            if tag in self.SKIP_TAGS:
                self.skip_depth += 1
            return

        if tag in self.SKIP_TAGS:
            self.skip_depth = 1
            return

        if tag in {"h1", "h2", "h3"}:
            self.heading_tag = tag
            self.heading_id = attributes.get("id", "")
            self.heading_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()

        if tag == "main":
            self.in_main = False
            self.skip_depth = 0
            return

        if not self.in_main:
            return

        if self.skip_depth:
            if tag in self.SKIP_TAGS:
                self.skip_depth -= 1
            return

        if self.heading_tag == tag:
            heading = normalize_text(" ".join(self.heading_parts))

            if tag == "h1" and heading and not self.title:
                self.title = heading

            if tag in {"h2", "h3"} and heading:
                self.current_section = Section(
                    anchor=self.heading_id.strip() or slugify(heading),
                    title=heading,
                    level=int(tag[1]),
                )
                self.sections.append(self.current_section)

            self.heading_tag = None
            self.heading_id = ""
            self.heading_parts = []

    def handle_data(self, data: str) -> None:
        if not self.in_main or self.skip_depth:
            return

        cleaned = normalize_text(data)
        if not cleaned:
            return

        self.body_parts.append(cleaned)

        if self.heading_tag:
            self.heading_parts.append(cleaned)
        elif self.current_section is not None:
            self.current_section.text_parts.append(cleaned)


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def slugify(value: str) -> str:
    lowered = value.casefold()
    lowered = re.sub(r"[^a-z0-9\s-]", "", lowered)
    lowered = re.sub(r"[\s-]+", "-", lowered)
    return lowered.strip("-") or "section"


def route_for_html(site_root: Path, html_path: Path) -> str:
    relative = html_path.relative_to(site_root)
    if relative.as_posix() == "index.html":
        return "/"
    if relative.name == "index.html":
        return "/" + relative.parent.as_posix().strip("/") + "/"
    return "/" + relative.as_posix()


def load_page(site_root: Path, path: Path) -> PageDocument | None:
    source = path.read_text(encoding="utf-8")
    extractor = PageExtractor()
    extractor.feed(source)

    if not extractor.body_parts:
        return None

    body = normalize_text(" ".join(extractor.body_parts))
    headings = ". ".join(section.title for section in extractor.sections)
    intro = body[:1400]
    page_context = normalize_text(
        ". ".join(
            part
            for part in [
                extractor.title,
                extractor.description,
                headings,
                intro,
            ]
            if part
        )
    )[:MAX_PAGE_CONTEXT_CHARS]

    return PageDocument(
        path=path,
        route=route_for_html(site_root, path),
        title=extractor.title,
        description=extractor.description,
        body=body,
        page_context=page_context,
        sections=[
            section
            for section in extractor.sections
            if section.semantic_text
        ],
    )


def load_subjects(path: Path) -> tuple[list[Subject], str]:
    raw_bytes = path.read_bytes()
    data = json.loads(raw_bytes)

    if data.get("version") != 1:
        raise ValueError(
            f"Unsupported subject index version: {data.get('version')!r}"
        )

    subjects: list[Subject] = []
    for raw in data.get("subjects", []):
        subjects.append(
            Subject(
                subject_id=str(raw["id"]),
                label=str(raw["label"]),
                category=str(raw.get("category", "")),
                definition=str(raw.get("definition", "")),
                aliases=tuple(str(v) for v in raw.get("aliases", [])),
                abbreviations=tuple(
                    str(v) for v in raw.get("abbreviations", [])
                ),
                lay_phrases=tuple(
                    str(v) for v in raw.get("lay_phrases", [])
                ),
                misspellings=tuple(
                    str(v) for v in raw.get("misspellings", [])
                ),
                broader=tuple(str(v) for v in raw.get("broader", [])),
                narrower=tuple(str(v) for v in raw.get("narrower", [])),
                related=tuple(str(v) for v in raw.get("related", [])),
            )
        )

    if not subjects:
        raise ValueError("Subject index contains no subjects")

    ids = [subject.subject_id for subject in subjects]
    if len(ids) != len(set(ids)):
        raise ValueError("Subject IDs must be unique")

    known = set(ids)
    for subject in subjects:
        for field_name in ("broader", "narrower", "related"):
            for target in getattr(subject, field_name):
                if target not in known:
                    raise ValueError(
                        f"Unknown {field_name} subject {target!r} "
                        f"referenced by {subject.subject_id!r}"
                    )

        # A spelling cannot simultaneously be an approved alias/abbreviation.
        accepted = {
            value.casefold()
            for value in (
                subject.label,
                *subject.aliases,
                *subject.abbreviations,
            )
        }
        overlap = [
            value
            for value in subject.misspellings
            if value.casefold() in accepted
        ]
        if overlap:
            raise ValueError(
                f"Subject {subject.subject_id!r} has accepted terms also "
                f"listed as misspellings: {overlap}"
            )

    return subjects, hashlib.sha256(raw_bytes).hexdigest()


def load_structure_map(
    path: Path,
    known_subject_ids: set[str],
) -> tuple[dict[str, object], str]:
    raw_bytes = path.read_bytes()
    data = json.loads(raw_bytes)

    if data.get("version") != 1:
        raise ValueError(
            f"Unsupported structure-map version: {data.get('version')!r}"
        )

    for rule_group in ("route_prefix_rules", "segment_modifier_rules"):
        for rule in data.get(rule_group, []):
            for subject_id in rule.get("subjects", []):
                if subject_id not in known_subject_ids:
                    raise ValueError(
                        f"Unknown subject {subject_id!r} in {rule_group}"
                    )

    return data, hashlib.sha256(raw_bytes).hexdigest()


def inherited_subjects_for_route(
    route: str,
    structure: dict[str, object],
) -> list[str]:
    inherited: list[str] = []
    seen: set[str] = set()

    def add(subject_id: str) -> None:
        if subject_id not in seen:
            seen.add(subject_id)
            inherited.append(subject_id)

    for rule in structure.get("route_prefix_rules", []):
        prefix = str(rule.get("prefix", ""))
        if prefix and route.startswith(prefix):
            for subject_id in rule.get("subjects", []):
                add(str(subject_id))

    segments = [segment for segment in route.strip("/").split("/") if segment]
    for rule in structure.get("segment_modifier_rules", []):
        if str(rule.get("segment", "")) in segments:
            for subject_id in rule.get("subjects", []):
                add(str(subject_id))

    return inherited


def discover_subject_candidates(
    pages: list[PageDocument],
    structure: dict[str, object],
) -> list[dict[str, object]]:
    config = structure.get("candidate_discovery", {})
    root = str(config.get("root", "/reference/"))
    ignored = {
        str(value)
        for value in config.get("ignore_top_level_segments", [])
    }
    require_landing = bool(config.get("require_landing_page", True))

    mapped_segments: set[str] = set()
    for rule in structure.get("route_prefix_rules", []):
        prefix = str(rule.get("prefix", ""))
        if not prefix.startswith(root):
            continue
        remainder = prefix[len(root):].strip("/")
        if remainder:
            mapped_segments.add(remainder.split("/", 1)[0])

    groups: dict[str, list[PageDocument]] = {}
    for page in pages:
        if not page.route.startswith(root):
            continue
        remainder = page.route[len(root):].strip("/")
        if not remainder:
            continue
        segment = remainder.split("/", 1)[0]
        if segment in ignored or segment in mapped_segments:
            continue
        groups.setdefault(segment, []).append(page)

    candidates: list[dict[str, object]] = []
    for segment, group in sorted(groups.items()):
        prefix = f"{root}{segment}/"
        landing = next(
            (page for page in group if page.route == prefix),
            None,
        )
        if require_landing and landing is None:
            continue

        candidates.append(
            {
                "status": "needs-human-review",
                "proposed_id": segment,
                "route_prefix": prefix,
                "label": (
                    landing.title
                    if landing and landing.title
                    else segment.replace("-", " ").title()
                ),
                "page_count": len(group),
                "page_titles": [
                    {
                        "route": page.route,
                        "title": page.title,
                    }
                    for page in sorted(group, key=lambda item: item.route)[:25]
                ],
                "approval_action": (
                    "If this is a real search subject, add it to "
                    "subject-index.json and add its route prefix to "
                    "structure-map.json. Otherwise explicitly ignore or map "
                    "the folder to an existing subject."
                ),
            }
        )

    return candidates


def load_cache(path: Path) -> dict[str, object]:
    if not path.exists():
        return {"version": CACHE_VERSION, "pages": {}}

    cache = json.loads(path.read_text(encoding="utf-8"))
    if cache.get("version") != CACHE_VERSION:
        return {"version": CACHE_VERSION, "pages": {}}

    if not isinstance(cache.get("pages"), dict):
        raise ValueError("Subject classification cache pages must be an object")

    return cache


def save_cache(path: Path, cache: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(cache, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def page_fingerprint(
    page: PageDocument,
    subject_digest: str,
    structure_digest: str,
    inherited_subjects: list[str],
    model_name: str,
    page_score: float,
    section_score: float,
    max_page_subjects: int,
    max_section_subjects: int,
    ignored_section_titles: list[str],
) -> str:
    payload = {
        "route": page.route,
        "full_body_sha256": hashlib.sha256(
            page.body.encode("utf-8")
        ).hexdigest(),
        "page_context": page.page_context,
        "sections": [
            {
                "anchor": section.anchor,
                "title": section.title,
                "text_sha256": hashlib.sha256(
                    section.text.encode("utf-8")
                ).hexdigest(),
            }
            for section in page.sections
        ],
        "subject_digest": subject_digest,
        "structure_digest": structure_digest,
        "inherited_subjects": inherited_subjects,
        "model": model_name,
        "page_score": page_score,
        "section_score": section_score,
        "max_page_subjects": max_page_subjects,
        "max_section_subjects": max_section_subjects,
        "ignored_section_titles": sorted(
            title.casefold() for title in ignored_section_titles
        ),
    }
    encoded = json.dumps(
        payload,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def normalized_matrix(vectors: Iterable[object]):
    import numpy as np

    matrix = np.asarray(list(vectors), dtype=np.float32)
    if matrix.ndim != 2:
        raise ValueError(
            f"Expected a 2D embedding matrix, got {matrix.shape}"
        )

    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return matrix / norms


def best_matches(
    scores,
    subjects: list[Subject],
    minimum_score: float,
    maximum: int,
    excluded_ids: set[str] | None = None,
) -> list[tuple[Subject, float]]:
    excluded_ids = excluded_ids or set()
    ranked = sorted(
        (
            (subject, float(scores[index]))
            for index, subject in enumerate(subjects)
            if subject.subject_id not in excluded_ids
            and float(scores[index]) >= minimum_score
        ),
        key=lambda item: item[1],
        reverse=True,
    )
    return ranked[:maximum]


def should_classify_section(
    section: Section,
    ignored_section_titles: set[str],
) -> bool:
    return (
        section.title.casefold() not in ignored_section_titles
        and len(section.text) >= 60
    )


def classify_pages(
    pages: list[PageDocument],
    subjects: list[Subject],
    inherited_by_route: dict[str, list[str]],
    ignored_section_titles: set[str],
    model_name: str,
    page_score: float,
    section_score: float,
    max_page_subjects: int,
    max_section_subjects: int,
) -> dict[str, dict[str, object]]:
    from fastembed import TextEmbedding

    model = TextEmbedding(model_name=model_name)
    subject_vectors = normalized_matrix(
        model.query_embed([subject.semantic_text for subject in subjects])
    )
    page_vectors = normalized_matrix(
        model.passage_embed(
            [page.page_context for page in pages],
            batch_size=64,
        )
    )

    results: dict[str, dict[str, object]] = {}

    for page_index, page in enumerate(pages):
        inherited = inherited_by_route.get(page.route, [])
        page_scores = page_vectors[page_index] @ subject_vectors.T
        supplemental = best_matches(
            page_scores,
            subjects,
            minimum_score=page_score,
            maximum=max_page_subjects,
            excluded_ids=set(inherited),
        )

        eligible_sections = [
            section
            for section in page.sections
            if should_classify_section(section, ignored_section_titles)
        ]
        section_records: list[dict[str, object]] = []

        if eligible_sections:
            section_vectors = normalized_matrix(
                model.passage_embed(
                    [
                        section.semantic_text
                        for section in eligible_sections
                    ],
                    batch_size=64,
                )
            )

            for section_index, section in enumerate(eligible_sections):
                scores = section_vectors[section_index] @ subject_vectors.T
                matches = best_matches(
                    scores,
                    subjects,
                    minimum_score=section_score,
                    maximum=max_section_subjects,
                )
                if matches:
                    section_records.append(
                        {
                            "anchor": section.anchor,
                            "title": section.title,
                            "subjects": [
                                {
                                    "id": subject.subject_id,
                                    "score": round(score, 6),
                                }
                                for subject, score in matches
                            ],
                        }
                    )

        results[page.route] = {
            "inherited_subjects": inherited,
            "ai_subjects": [
                {
                    "id": subject.subject_id,
                    "score": round(score, 6),
                }
                for subject, score in supplemental
            ],
            # Section classifications stay reviewable in the cache/report but
            # are deliberately NOT flattened into page-wide Pagefind metadata.
            "sections": section_records,
        }

    return results


def unique_terms(
    subject_ids: Iterable[str],
    subjects_by_id: dict[str, Subject],
    attribute_names: tuple[str, ...],
) -> list[str]:
    terms: list[str] = []
    seen: set[str] = set()

    for subject_id in subject_ids:
        subject = subjects_by_id.get(subject_id)
        if subject is None:
            continue

        for attribute_name in attribute_names:
            values = getattr(subject, attribute_name)
            if isinstance(values, str):
                values = (values,)

            for value in values:
                cleaned = normalize_text(str(value))
                key = cleaned.casefold()
                if cleaned and key not in seen:
                    seen.add(key)
                    terms.append(cleaned)

    return terms


def meta_tag(name: str, pagefind_key: str, terms: list[str]) -> str:
    if not terms:
        return ""

    content = html.escape(" | ".join(terms), quote=True)
    return (
        "\n  <meta"
        f' name="{name}"'
        f' content="{content}"'
        f' data-pagefind-meta="{pagefind_key}[content]"'
        ">\n"
    )


def inject_metadata(
    page: PageDocument,
    inherited_subject_ids: list[str],
    record: dict[str, object] | None,
    subjects_by_id: dict[str, Subject],
) -> None:
    source = page.path.read_text(encoding="utf-8")
    source = SEARCH_META_RE.sub("", source)

    ai_ids: list[str] = []
    if record:
        ai_ids = [
            str(item.get("id"))
            for item in record.get("ai_subjects", [])
            if isinstance(item, dict) and item.get("id")
        ]

    structural_exact = unique_terms(
        inherited_subject_ids,
        subjects_by_id,
        ("label", "aliases", "abbreviations"),
    )
    structural_lay = unique_terms(
        inherited_subject_ids,
        subjects_by_id,
        ("lay_phrases",),
    )
    ai_exact = unique_terms(
        ai_ids,
        subjects_by_id,
        ("label", "aliases", "abbreviations"),
    )
    ai_lay = unique_terms(
        ai_ids,
        subjects_by_id,
        ("lay_phrases",),
    )
    misspellings = unique_terms(
        [*inherited_subject_ids, *ai_ids],
        subjects_by_id,
        ("misspellings",),
    )

    tags = "".join(
        [
            meta_tag(
                "fnd-structural-subjects",
                "subject_structural",
                structural_exact,
            ),
            meta_tag(
                "fnd-structural-lay-phrases",
                "subject_structural_lay",
                structural_lay,
            ),
            meta_tag(
                "fnd-ai-subjects",
                "subject_ai",
                ai_exact,
            ),
            meta_tag(
                "fnd-ai-lay-phrases",
                "subject_ai_lay",
                ai_lay,
            ),
            meta_tag(
                "fnd-search-misspellings",
                "subject_misspellings",
                misspellings,
            ),
        ]
    )

    if tags:
        if "</head>" not in source:
            raise ValueError(f"Missing </head> in {page.path}")
        source = source.replace("</head>", tags + "</head>", 1)

    page.path.write_text(source, encoding="utf-8")


def validate_cached_record(
    entry: object,
    expected_fingerprint: str,
    subjects_by_id: dict[str, Subject],
) -> dict[str, object] | None:
    if not isinstance(entry, dict):
        return None

    if entry.get("fingerprint") != expected_fingerprint:
        return None

    for subject_id in entry.get("inherited_subjects", []):
        if str(subject_id) not in subjects_by_id:
            return None

    for item in entry.get("ai_subjects", []):
        if (
            not isinstance(item, dict)
            or str(item.get("id")) not in subjects_by_id
        ):
            return None

    for section in entry.get("sections", []):
        if not isinstance(section, dict):
            return None
        for item in section.get("subjects", []):
            if (
                not isinstance(item, dict)
                or str(item.get("id")) not in subjects_by_id
            ):
                return None

    return entry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, default=Path("_site"))
    parser.add_argument(
        "--subjects",
        type=Path,
        default=Path("tools/search/subject-index.json"),
    )
    parser.add_argument(
        "--structure",
        type=Path,
        default=Path("tools/search/structure-map.json"),
    )
    parser.add_argument(
        "--cache",
        type=Path,
        default=Path("tools/search/subject-cache.json"),
    )
    parser.add_argument(
        "--candidates",
        type=Path,
        default=Path("tools/search/subject-candidates.json"),
    )
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--page-score", type=float, default=DEFAULT_PAGE_SCORE)
    parser.add_argument(
        "--section-score",
        type=float,
        default=DEFAULT_SECTION_SCORE,
    )
    parser.add_argument(
        "--max-page-subjects",
        type=int,
        default=DEFAULT_MAX_PAGE_SUBJECTS,
    )
    parser.add_argument(
        "--max-section-subjects",
        type=int,
        default=DEFAULT_MAX_SECTION_SUBJECTS,
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
    )
    parser.add_argument(
        "--all-stale",
        action="store_true",
        help="Process every stale page in this run.",
    )
    parser.add_argument(
        "--cache-only",
        action="store_true",
        help="Apply valid cache plus structural inheritance; never run model.",
    )
    parser.add_argument("--report", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not (
        0 <= args.page_score <= 1
        and 0 <= args.section_score <= 1
    ):
        print("Classification score thresholds must be between 0 and 1")
        return 1

    if args.max_page_subjects < 1 or args.max_section_subjects < 1:
        print("Maximum subject counts must be at least 1")
        return 1

    if args.batch_size < 0:
        print("--batch-size cannot be negative")
        return 1

    site_root = args.site.resolve()
    if not site_root.exists():
        print(f"Built site not found: {site_root}")
        return 1

    subjects, subject_digest = load_subjects(args.subjects.resolve())
    subjects_by_id = {
        subject.subject_id: subject
        for subject in subjects
    }
    structure, structure_digest = load_structure_map(
        args.structure.resolve(),
        set(subjects_by_id),
    )
    ignored_section_titles = {
        str(title).casefold()
        for title in structure.get("ignored_section_titles", [])
    }

    pages = [
        page
        for path in sorted(site_root.rglob("*.html"))
        if (page := load_page(site_root, path)) is not None
    ]

    inherited_by_route = {
        page.route: inherited_subjects_for_route(
            page.route,
            structure,
        )
        for page in pages
    }

    candidates = discover_subject_candidates(pages, structure)
    candidates_payload = {
        "version": 1,
        "status": (
            "review-needed" if candidates else "no-unmapped-folders"
        ),
        "candidates": candidates,
    }
    args.candidates.parent.mkdir(parents=True, exist_ok=True)
    args.candidates.write_text(
        json.dumps(
            candidates_payload,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    cache_path = args.cache.resolve()
    cache = load_cache(cache_path)
    cache_pages = cache["pages"]
    assert isinstance(cache_pages, dict)

    fingerprints = {
        page.route: page_fingerprint(
            page,
            subject_digest=subject_digest,
            structure_digest=structure_digest,
            inherited_subjects=inherited_by_route[page.route],
            model_name=args.model,
            page_score=args.page_score,
            section_score=args.section_score,
            max_page_subjects=args.max_page_subjects,
            max_section_subjects=args.max_section_subjects,
            ignored_section_titles=list(ignored_section_titles),
        )
        for page in pages
    }

    valid_records: dict[str, dict[str, object]] = {}
    stale_pages: list[PageDocument] = []

    for page in pages:
        record = validate_cached_record(
            cache_pages.get(page.route),
            fingerprints[page.route],
            subjects_by_id,
        )
        if record is None:
            stale_pages.append(page)
        else:
            valid_records[page.route] = record

    to_process: list[PageDocument] = []
    if not args.cache_only and stale_pages:
        to_process = (
            stale_pages
            if args.all_stale
            else stale_pages[: args.batch_size]
        )

    if to_process:
        try:
            fresh = classify_pages(
                pages=to_process,
                subjects=subjects,
                inherited_by_route=inherited_by_route,
                ignored_section_titles=ignored_section_titles,
                model_name=args.model,
                page_score=args.page_score,
                section_score=args.section_score,
                max_page_subjects=args.max_page_subjects,
                max_section_subjects=args.max_section_subjects,
            )
        except ImportError:
            print(
                "Subject inference requires fastembed. Install "
                "tools/search/requirements.txt or use --cache-only."
            )
            return 1

        for page in to_process:
            record = fresh[page.route]
            record["fingerprint"] = fingerprints[page.route]
            record["title"] = page.title
            cache_pages[page.route] = record
            valid_records[page.route] = record

        live_routes = {page.route for page in pages}
        for route in list(cache_pages):
            if route not in live_routes:
                del cache_pages[route]

        cache.update(
            {
                "version": CACHE_VERSION,
                "model": args.model,
                "page_score": args.page_score,
                "section_score": args.section_score,
                "max_page_subjects": args.max_page_subjects,
                "max_section_subjects": args.max_section_subjects,
                "subject_index_digest": subject_digest,
                "structure_map_digest": structure_digest,
            }
        )
        save_cache(cache_path, cache)

    for page in pages:
        inject_metadata(
            page,
            inherited_by_route[page.route],
            valid_records.get(page.route),
            subjects_by_id,
        )

    stale_routes = [
        page.route
        for page in pages
        if page.route not in valid_records
    ]

    report = {
        "subject_index_status": "reviewed-input-only",
        "structure_map_status": "deterministic-inheritance",
        "candidate_subject_count": len(candidates),
        "candidate_subjects": candidates,
        "model": args.model,
        "page_score": args.page_score,
        "section_score": args.section_score,
        "max_ai_page_subjects": args.max_page_subjects,
        "max_section_subjects": args.max_section_subjects,
        "cache_only": args.cache_only,
        "page_count": len(pages),
        "valid_cached_or_processed": len(valid_records),
        "processed_this_run": [
            page.route for page in to_process
        ],
        "remaining_stale_page_count": len(stale_routes),
        "remaining_stale_pages": stale_routes,
        "pages": [
            {
                "route": page.route,
                "title": page.title,
                "inherited_subjects": inherited_by_route[page.route],
                "classification": valid_records.get(page.route),
            }
            for page in pages
        ],
    }

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            json.dumps(
                report,
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

    inherited_page_count = sum(
        1 for values in inherited_by_route.values() if values
    )

    print("Subject search classification completed.")
    print(f"  Approved subjects:         {len(subjects)}")
    print(f"  Indexable pages:           {len(pages)}")
    print(f"  Structurally mapped pages: {inherited_page_count}")
    print(f"  New-folder candidates:     {len(candidates)}")
    print(f"  Cached/processed pages:    {len(valid_records)}")
    print(f"  Processed this run:        {len(to_process)}")
    print(f"  Remaining stale pages:     {len(stale_routes)}")
    print(
        "  Cache mode:                "
        + ("read-only" if args.cache_only else "incremental")
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
