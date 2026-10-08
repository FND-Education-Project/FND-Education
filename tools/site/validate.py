#!/usr/bin/env python3
"""
Validate generated Jekyll source and, when available, the built Pages artifact.

Run after tools/site/prepare_site.py. If _site exists, built HTML links are
checked too. The validator never edits canonical or generated content.
"""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

import prepare_site


ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / "web"

FIXED_ROUTES = {
    "/": WEB / "index.md",
    "/contact/": WEB / "contact" / "index.md",
    "/about/": WEB / "about" / "index.md",
    "/glossary/": WEB / "glossary" / "index.md",
    "/booklets/": WEB / "booklets" / "index.md",
    "/puzzles/": WEB / "puzzles" / "index.md",
    "/sitemap/": WEB / "sitemap" / "index.md",
}

VERIFICATION_FILE = "google65d5cac3c1021024.html"

LEGACY_PAGES_ORIGIN = (
    "https://fnd-education-project.github.io/FND-Education"
)


class LinkCollector(HTMLParser):
    """Collect rendered links, fragment targets and navigation relations."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.hrefs: list[str] = []
        self.ids: list[str] = []
        self.previous_links: list[str] = []
        self.next_links: list[str] = []
        self.html_lang: str | None = None
        self.main_count = 0
        self.h1_count = 0
        self.images_without_alt = 0
        self.canonical_links: list[str] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        attributes = {
            name.lower(): value
            for name, value in attrs
            if value is not None
        }

        lowered_tag = tag.lower()

        if lowered_tag == "html":
            self.html_lang = attributes.get("lang")

        if lowered_tag == "main":
            self.main_count += 1

        if lowered_tag == "h1":
            self.h1_count += 1

        if lowered_tag == "img" and "alt" not in attributes:
            self.images_without_alt += 1

        if lowered_tag == "link":
            relations = {
                item.strip().lower()
                for item in attributes.get("rel", "").split()
                if item.strip()
            }
            canonical_href = attributes.get("href")
            if canonical_href and "canonical" in relations:
                self.canonical_links.append(canonical_href)

        element_id = attributes.get("id")
        if element_id:
            self.ids.append(element_id)

        if lowered_tag == "a":
            legacy_name = attributes.get("name")
            if legacy_name:
                self.ids.append(legacy_name)

        href = attributes.get("href")
        src = attributes.get("src")

        if href:
            self.links.append(href)
            self.hrefs.append(href)

        if src:
            self.links.append(src)

        if tag.lower() != "a":
            return

        rel = attributes.get("rel", "")
        relations = {
            item.strip().lower()
            for item in rel.split()
            if item.strip()
        }

        if href and "prev" in relations:
            self.previous_links.append(href)

        if href and "next" in relations:
            self.next_links.append(href)


def configured_baseurl() -> str:
    value = prepare_site.read_config_scalar("baseurl").strip()
    if not value:
        return ""
    return "/" + value.strip("/")


def expected_routes() -> tuple[
    list[prepare_site.CoursePage],
    list[prepare_site.ReferencePage],
    list[str],
]:
    course_pages = prepare_site.discover_course_pages()
    reference_pages = prepare_site.discover_reference_pages()

    routes = [
        *FIXED_ROUTES.keys(),
        *[page.public_url for page in course_pages],
        *[page.public_url for page in reference_pages],
    ]

    return course_pages, reference_pages, routes


def ensure_unique_routes(routes: list[str], errors: list[str]) -> None:
    seen: set[str] = set()
    duplicates: set[str] = set()

    for route in routes:
        if route in seen:
            duplicates.add(route)
        seen.add(route)

    if duplicates:
        errors.append(
            "Duplicate public routes: "
            + ", ".join(sorted(duplicates))
        )


AUDIENCE_HEADINGS = (
    "## For the Person With FND",
    "## For Family, Friends, and Other Supporters",
    "## For Clinicians and the Care Team",
    "## Research and Sources",
)

AUDIENCE_MENU_RE = re.compile(
    r"\[For the Person With FND\]\(#for-the-person-with-fnd\)<br>\s*\n"
    r"\[For Family, Friends, and Other Supporters\]"
    r"\(#for-family-friends-and-other-supporters\)<br>\s*\n"
    r"\[For Clinicians and the Care Team\]"
    r"\(#for-clinicians-and-the-care-team\)<br>\s*\n"
    r"\[Research and Sources\]\(#research-and-sources\)",
    re.MULTILINE,
)


def audit_audience_structure(
    path: Path,
    require_audiences: bool,
    errors: list[str],
) -> None:
    """
    Check the four-audience educational structure in generated Markdown.

    Course lessons always require it. Reference pages require it whenever any
    of the three audience headings is present, which lets technique/index pages
    use their intentionally different structures without false failures.
    """
    if not path.exists():
        return

    text = path.read_text(encoding="utf-8")
    audience_present = any(
        heading in text
        for heading in AUDIENCE_HEADINGS[:3]
    )

    if not require_audiences and not audience_present:
        return

    label = str(path.relative_to(ROOT))

    positions: list[int] = []
    for heading in AUDIENCE_HEADINGS:
        count = text.count(heading)

        if count != 1:
            errors.append(
                f"Audience heading count on {label}: "
                f"{heading!r} appears {count} times"
            )
            continue

        positions.append(text.index(heading))

    if len(positions) == len(AUDIENCE_HEADINGS):
        if positions != sorted(positions):
            errors.append(
                f"Audience sections are out of order on {label}"
            )

        previous_boundary = 0
        for heading, position in zip(AUDIENCE_HEADINGS, positions):
            preceding = text[previous_boundary:position]
            menus = list(AUDIENCE_MENU_RE.finditer(preceding))

            if not menus:
                errors.append(
                    f"Audience menu missing immediately before "
                    f"{heading!r} on {label}"
                )

            previous_boundary = position + len(heading)


def check_generated_source(errors: list[str]) -> tuple[int, int, int]:
    course_pages, reference_pages, routes = expected_routes()
    ensure_unique_routes(routes, errors)

    for page in course_pages:
        if not page.destination.exists():
            errors.append(
                "Missing generated course page: "
                + str(page.destination.relative_to(ROOT))
            )
            continue

        audit_audience_structure(
            path=page.destination,
            require_audiences=(page.kind == "lesson"),
            errors=errors,
        )

    for page in reference_pages:
        if not page.destination.exists():
            errors.append(
                "Missing generated Reference page: "
                + str(page.destination.relative_to(ROOT))
            )
            continue

        audit_audience_structure(
            path=page.destination,
            require_audiences=False,
            errors=errors,
        )

    for route, path in FIXED_ROUTES.items():
        if not path.exists():
            errors.append(
                f"Missing source for public route {route}: "
                f"{path.relative_to(ROOT)}"
            )

    verification = WEB / VERIFICATION_FILE
    if not verification.exists():
        errors.append(
            f"Missing Google verification file: web/{VERIFICATION_FILE}"
        )

    machine_sitemap = WEB / "sitemap.xml"
    robots = WEB / "robots.txt"
    search_source = WEB / "search" / "index.html"

    if not search_source.exists():
        errors.append("Missing website search source: web/search/index.html")

    if not machine_sitemap.exists():
        errors.append("Missing generated web/sitemap.xml")
    if not robots.exists():
        errors.append("Missing generated web/robots.txt")

    generated_roots = [
        WEB / "course",
        WEB / "reference",
        WEB / "glossary",
        WEB / "booklets",
        WEB / "puzzles",
        WEB / "sitemap",
    ]

    for root in generated_roots:
        if not root.exists():
            continue

        for path in root.rglob("*"):
            if not path.is_file():
                continue

            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            if "reference/_internal/" in text or "/_internal/" in text:
                errors.append(
                    "Internal Reference path leaked into generated site: "
                    + str(path.relative_to(ROOT))
                )

            if LEGACY_PAGES_ORIGIN in text:
                errors.append(
                    "Legacy GitHub Pages URL leaked into generated site: "
                    + str(path.relative_to(ROOT))
                )

    internal_root = ROOT / "reference" / "_internal"
    if internal_root.exists():
        internal_sources = {
            path.resolve()
            for path in internal_root.rglob("*.md")
        }
        public_sources = {
            page.source.resolve()
            for page in reference_pages
        }
        overlap = internal_sources & public_sources
        if overlap:
            errors.append(
                "Internal Reference files classified as public: "
                + ", ".join(
                    str(path.relative_to(ROOT))
                    for path in sorted(overlap)
                )
            )

    if machine_sitemap.exists():
        try:
            root = ET.parse(machine_sitemap).getroot()
            ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            locs = [
                item.text or ""
                for item in root.findall("sm:url/sm:loc", ns)
            ]

            if len(locs) != len(set(routes)):
                errors.append(
                    "Machine sitemap route count mismatch: "
                    f"expected {len(set(routes))}, found {len(locs)}"
                )

            if len(locs) != len(set(locs)):
                errors.append("Machine sitemap contains duplicate URLs")

            if any("_internal" in loc for loc in locs):
                errors.append(
                    "Machine sitemap contains an internal Reference URL"
                )
        except ET.ParseError as exc:
            errors.append(f"web/sitemap.xml is not valid XML: {exc}")

    page_schema_path = WEB / "_data" / "generated" / "page_schema.json"
    if not page_schema_path.exists():
        errors.append("Missing generated page-level schema data")
    else:
        try:
            page_schema = json.loads(
                page_schema_path.read_text(encoding="utf-8")
            )
            expected_schema_routes = set(routes) | {"/search/"}
            actual_schema_routes = set(page_schema)
            if actual_schema_routes != expected_schema_routes:
                errors.append(
                    "Page schema route set mismatch: "
                    f"missing={sorted(expected_schema_routes - actual_schema_routes)}, "
                    f"extra={sorted(actual_schema_routes - expected_schema_routes)}"
                )
        except json.JSONDecodeError as exc:
            errors.append(f"Generated page schema is invalid JSON: {exc}")

    return len(course_pages), len(reference_pages), len(set(routes))


def route_to_built_file(site_root: Path, route: str) -> Path:
    if route == "/":
        return site_root / "index.html"

    clean = route.strip("/")
    return site_root / clean / "index.html"


def built_file_to_route(site_root: Path, html_file: Path) -> str:
    relative = html_file.relative_to(site_root)

    if relative.as_posix() == "index.html":
        return "/"

    if relative.name == "index.html":
        parent = relative.parent.as_posix().strip("/")
        return "/" + parent + "/"

    return "/" + relative.as_posix()


def local_target_path(
    current_route: str,
    raw_target: str,
    baseurl: str,
) -> str | None:
    """Resolve one rendered local href/src to a site-root path."""
    raw_target = raw_target.strip()
    if not raw_target or raw_target.startswith("#"):
        return None

    parsed = urlparse(raw_target)
    if parsed.scheme or parsed.netloc:
        return None

    target = unquote(parsed.path)
    if not target:
        return None

    if target.startswith("/"):
        if baseurl and (
            target == baseurl
            or target.startswith(baseurl + "/")
        ):
            target = target[len(baseurl):] or "/"
    else:
        target = urljoin(current_route, target)

    target = "/" + posixpath.normpath(target).lstrip("/")

    if raw_target.endswith("/") and not target.endswith("/"):
        target += "/"

    return target


def target_exists(site_root: Path, target: str) -> bool:
    """Check a rendered site-root target against artifact files."""
    clean = target.split("?", 1)[0].split("#", 1)[0]

    if clean == "/":
        return (site_root / "index.html").exists()

    relative = clean.lstrip("/")
    direct = site_root / relative

    if direct.is_file():
        return True

    if direct.is_dir() and (direct / "index.html").exists():
        return True

    if clean.endswith("/"):
        return (site_root / relative / "index.html").exists()

    if "." not in Path(relative).name:
        return (site_root / relative / "index.html").exists()

    return False


def navigation_target_route(
    current_route: str,
    target: str,
    baseurl: str,
) -> str | None:
    """Resolve one Previous/Next href to its public route."""
    resolved = local_target_path(
        current_route=current_route,
        raw_target=target,
        baseurl=baseurl,
    )
    if resolved is None:
        return None

    if resolved.endswith("/index.html"):
        resolved = resolved[: -len("index.html")]

    return resolved


def audit_page_navigation(
    current_route: str,
    parser: LinkCollector,
    expected: prepare_site.NavigationLinks | None,
    baseurl: str,
    errors: list[str],
) -> None:
    """
    Require Previous and Next navigation everywhere except Home and Contact.

    Educational pages can repeat the same control after audience sections.
    Every repeated rel=prev/rel=next target must agree with the site-wide
    sequence so duplicated controls cannot silently diverge.
    """
    exempt = {"/", "/contact/"}

    if current_route in exempt:
        if parser.previous_links or parser.next_links:
            errors.append(
                f"Navigation should be absent on exempt page {current_route}"
            )
        return

    if expected is None:
        errors.append(
            f"No expected navigation sequence defined for {current_route}"
        )
        return

    if not parser.previous_links:
        errors.append(
            f"Missing Previous page navigation on {current_route}"
        )

    if not parser.next_links:
        errors.append(
            f"Missing Next page navigation on {current_route}"
        )

    expected_pairs = (
        (
            "Previous",
            parser.previous_links,
            expected.previous_url,
        ),
        (
            "Next",
            parser.next_links,
            expected.next_url,
        ),
    )

    for label, links, expected_url in expected_pairs:
        if not links or not expected_url:
            continue

        resolved_targets = {
            navigation_target_route(
                current_route=current_route,
                target=target,
                baseurl=baseurl,
            )
            for target in links
        }
        resolved_targets.discard(None)

        if resolved_targets != {expected_url}:
            errors.append(
                f"{label} navigation mismatch on {current_route}: "
                f"expected {expected_url}, found "
                + ", ".join(sorted(resolved_targets))
            )


def normalize_route_path(path: str) -> str:
    """Normalize one local HTML destination to the site's pretty route form."""
    if not path:
        return "/"

    clean = "/" + path.lstrip("/")

    if clean.endswith("/index.html"):
        clean = clean[: -len("index.html")]

    if clean == "/index.html":
        return "/"

    if "." not in Path(clean).name and not clean.endswith("/"):
        clean += "/"

    return clean


def resolve_fragment_href(
    current_route: str,
    raw_href: str,
    baseurl: str,
) -> tuple[str, str] | None:
    """Resolve a local href containing #fragment to (route, fragment)."""
    parsed = urlparse(raw_href)

    if parsed.scheme or parsed.netloc or not parsed.fragment:
        return None

    fragment = unquote(parsed.fragment)

    if not fragment:
        return None

    if not parsed.path:
        return current_route, fragment

    path = unquote(parsed.path)

    if path.startswith("/"):
        if baseurl and (
            path == baseurl
            or path.startswith(baseurl + "/")
        ):
            path = path[len(baseurl):] or "/"
    else:
        path = urljoin(current_route, path)

    return normalize_route_path(path), fragment


def audit_fragment_links(
    parsed_by_route: dict[str, LinkCollector],
    baseurl: str,
    errors: list[str],
) -> None:
    """
    Verify same-site #fragment links and duplicate HTML IDs.

    This catches broken citation numbers, section-jump links, glossary anchors,
    and accidental duplicate IDs after Markdown/Jekyll rendering.
    """
    ids_by_route = {
        route: set(parser.ids)
        for route, parser in parsed_by_route.items()
    }

    for route, parser in parsed_by_route.items():
        duplicates = sorted(
            {
                element_id
                for element_id in parser.ids
                if parser.ids.count(element_id) > 1
            }
        )

        if duplicates:
            errors.append(
                f"Duplicate HTML IDs on {route}: "
                + ", ".join(duplicates)
            )

        for href in parser.hrefs:
            resolved = resolve_fragment_href(
                current_route=route,
                raw_href=href,
                baseurl=baseurl,
            )
            if resolved is None:
                continue

            target_route, fragment = resolved
            target_ids = ids_by_route.get(target_route)

            # Fragments on PDFs or other non-HTML files are not DOM anchors.
            if target_ids is None:
                continue

            if fragment not in target_ids:
                errors.append(
                    f"Broken fragment link on {route}: "
                    f"{href} (missing #{fragment} on {target_route})"
                )


def audit_document_shell(
    current_route: str,
    text: str,
    parser: LinkCollector,
    baseurl: str,
    errors: list[str],
) -> None:
    """Audit the common rendered shell, accessibility basics and site nav."""
    if parser.html_lang != "en":
        errors.append(
            f"Missing or unexpected html lang on {current_route}: "
            f"{parser.html_lang!r}"
        )

    if parser.main_count != 1:
        errors.append(
            f"Expected one <main> on {current_route}; "
            f"found {parser.main_count}"
        )

    if parser.h1_count != 1:
        errors.append(
            f"Expected one <h1> on {current_route}; "
            f"found {parser.h1_count}"
        )

    if parser.images_without_alt:
        errors.append(
            f"Images without alt attributes on {current_route}: "
            f"{parser.images_without_alt}"
        )

    if len(parser.canonical_links) != 1:
        errors.append(
            f"Expected one canonical URL on {current_route}; "
            f"found {len(parser.canonical_links)}"
        )
    else:
        origin = prepare_site.public_origin_with_base().rstrip("/")
        expected_canonical = (
            origin + "/"
            if current_route == "/"
            else origin + current_route
        )
        if parser.canonical_links[0] != expected_canonical:
            errors.append(
                f"Canonical URL mismatch on {current_route}: "
                f"expected {expected_canonical}, "
                f"found {parser.canonical_links[0]}"
            )

    nav_blocks = re.findall(
        r'<nav class="site-nav(?: site-nav-bottom)?" '
        r'aria-label="Main navigation">(.*?)</nav>',
        text,
        re.DOTALL,
    )

    if len(nav_blocks) != 2:
        errors.append(
            f"Expected top and bottom main navigation on {current_route}; "
            f"found {len(nav_blocks)}"
        )
    else:
        for index, block in enumerate(nav_blocks, start=1):
            if 'href="/contact/"' not in block:
                errors.append(
                    f"Contact missing from main navigation {index} "
                    f"on {current_route}"
                )

    footer = re.search(
        r'<footer class="site-footer">(.*?)</footer>',
        text,
        re.DOTALL,
    )
    if footer is None:
        errors.append(f"Missing site footer on {current_route}")
        return

    footer_html = footer.group(1)
    sitemap_pos = footer_html.find('href="/sitemap/"')
    contact_pos = footer_html.find('href="/contact/"')
    project_pos = footer_html.find("footer-project-name")

    if sitemap_pos < 0 or contact_pos < 0:
        errors.append(
            f"Footer Sitemap/Contact links missing on {current_route}"
        )

    if (
        sitemap_pos >= 0
        and contact_pos >= 0
        and project_pos >= 0
        and max(sitemap_pos, contact_pos) > project_pos
    ):
        errors.append(
            f"Footer links must precede project name on {current_route}"
        )


def audit_structured_data(
    current_route: str,
    text: str,
    expected_page_schema: dict[str, dict[str, object]],
    errors: list[str],
) -> int:
    """
    Validate the rendered JSON-LD graph.

    Stage 1 checks the site-wide Organization, WebSite, FND MedicalCondition
    and glossary DefinedTermSet. Stage 2 also requires exactly one conservative
    page node whose type and relationships match the generated policy output.
    """
    blocks = re.findall(
        r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>',
        text,
        re.IGNORECASE | re.DOTALL,
    )
    if len(blocks) != 1:
        errors.append(
            f"Expected one JSON-LD block on {current_route}; found {len(blocks)}"
        )
        return 0

    try:
        payload = json.loads(blocks[0])
    except json.JSONDecodeError as exc:
        errors.append(
            f"Invalid JSON-LD on {current_route}: {exc}"
        )
        return 0

    if payload.get("@context") != "https://schema.org":
        errors.append(
            f"Unexpected JSON-LD context on {current_route}: "
            f"{payload.get('@context')!r}"
        )

    graph = payload.get("@graph")
    if not isinstance(graph, list):
        errors.append(f"JSON-LD @graph missing on {current_route}")
        return 0

    by_type: dict[str, list[dict[str, object]]] = {}
    for node in graph:
        if not isinstance(node, dict):
            errors.append(
                f"Non-object JSON-LD node on {current_route}"
            )
            continue

        raw_type = node.get("@type")
        types = raw_type if isinstance(raw_type, list) else [raw_type]
        for node_type in types:
            if isinstance(node_type, str):
                by_type.setdefault(node_type, []).append(node)

    for required_type in ("Organization", "WebSite", "MedicalCondition"):
        count = len(by_type.get(required_type, []))
        if count != 1:
            errors.append(
                f"Expected one {required_type} node on {current_route}; "
                f"found {count}"
            )

    origin = prepare_site.public_origin_with_base().rstrip("/")
    expected_ids = {
        "Organization": f"{origin}/#organization",
        "WebSite": f"{origin}/#website",
        "MedicalCondition": (
            f"{origin}/#functional-neurological-disorder"
        ),
    }
    for node_type, expected_id in expected_ids.items():
        nodes = by_type.get(node_type, [])
        if len(nodes) == 1 and nodes[0].get("@id") != expected_id:
            errors.append(
                f"{node_type} @id mismatch on {current_route}: "
                f"{nodes[0].get('@id')!r}"
            )

    # Stage 2: exact page node generated from the reviewed page policy.
    expected_page = expected_page_schema.get(current_route)
    if expected_page is None:
        errors.append(
            f"No generated page schema expected for {current_route}"
        )
    else:
        expected_page_id = expected_page.get("@id")
        page_nodes = [
            node
            for node in graph
            if isinstance(node, dict)
            and node.get("@id") == expected_page_id
        ]

        if len(page_nodes) != 1:
            errors.append(
                f"Expected one page node on {current_route}; "
                f"found {len(page_nodes)}"
            )
        else:
            actual_page = page_nodes[0]
            if actual_page != expected_page:
                errors.append(
                    f"Rendered page schema mismatch on {current_route}"
                )

            page_type = actual_page.get("@type")
            if page_type not in {"WebPage", "CollectionPage"}:
                errors.append(
                    f"Unsupported page type on {current_route}: "
                    f"{page_type!r}"
                )

            for forbidden in ("Article", "MedicalWebPage"):
                if forbidden in (
                    page_type
                    if isinstance(page_type, list)
                    else [page_type]
                ):
                    errors.append(
                        f"Forbidden page type {forbidden} on {current_route}"
                    )

    glossary_sets = by_type.get("DefinedTermSet", [])
    if current_route != "/glossary/":
        if glossary_sets:
            errors.append(
                f"Glossary DefinedTermSet leaked onto {current_route}"
            )
        return 0

    if len(glossary_sets) != 1:
        errors.append(
            f"Expected one DefinedTermSet on /glossary/; "
            f"found {len(glossary_sets)}"
        )
        return 0

    term_set = glossary_sets[0]
    raw_terms = term_set.get("hasDefinedTerm")
    if not isinstance(raw_terms, list):
        errors.append("Glossary hasDefinedTerm is not a list")
        return 0

    type_map = prepare_site.load_glossary_type_map()
    expected_codes = {
        entry["term_code"]
        for entry in type_map.values()
    }

    actual_codes: list[str] = []
    for index, term in enumerate(raw_terms, start=1):
        if not isinstance(term, dict):
            errors.append(
                f"Glossary DefinedTerm #{index} is not an object"
            )
            continue

        if term.get("@type") != "DefinedTerm":
            errors.append(
                f"Glossary term {term.get('name')!r} has unexpected @type "
                f"{term.get('@type')!r}"
            )

        code = term.get("termCode")
        if not isinstance(code, str) or not code:
            errors.append(
                f"Glossary term {term.get('name')!r} has no termCode"
            )
        else:
            actual_codes.append(code)

        if not term.get("name") or not term.get("description"):
            errors.append(
                f"Glossary DefinedTerm #{index} is missing name/description"
            )

        in_set = term.get("inDefinedTermSet")
        expected_set_id = f"{origin}/glossary/#defined-term-set"
        if (
            not isinstance(in_set, dict)
            or in_set.get("@id") != expected_set_id
        ):
            errors.append(
                f"Glossary term {term.get('name')!r} has invalid "
                "inDefinedTermSet"
            )

    if len(actual_codes) != len(set(actual_codes)):
        errors.append("Glossary schema contains duplicate termCode values")

    actual_code_set = set(actual_codes)
    if actual_code_set != expected_codes:
        missing = sorted(expected_codes - actual_code_set)
        extra = sorted(actual_code_set - expected_codes)
        errors.append(
            "Glossary schema/type-map code mismatch: "
            f"missing={missing}, extra={extra}"
        )

    expected_glossary_page = expected_page_schema.get("/glossary/", {})
    main_entity = expected_glossary_page.get("mainEntity")
    if main_entity != {
        "@id": f"{origin}/glossary/#defined-term-set"
    }:
        errors.append(
            "Glossary page schema does not point to DefinedTermSet "
            "as mainEntity"
        )

    return len(raw_terms)


def audit_reference_menu_separators(text: str, errors: list[str]) -> None:
    """Catch a menu's trailing Markdown rule rendered as an inline dash."""
    menus = list(re.finditer(
        r'<a\b[^>]*href="#more-fnd-reference-topics"[^>]*>More Reference Topics</a>',
        text,
    ))
    if not menus or any(
        not re.match(r'\s*</p>\s*<hr\s*/?>', text[menu.end():])
        for menu in menus
    ):
        errors.append("Reference landing menu must end with a separate horizontal rule")


def check_built_site(
    site_root: Path,
    baseurl: str,
    errors: list[str],
) -> int:
    course_pages, reference_pages, routes = expected_routes()
    navigation_map = prepare_site.build_global_navigation(
        course_pages,
        reference_pages,
    )

    page_schema_path = WEB / "_data" / "generated" / "page_schema.json"
    try:
        expected_page_schema = json.loads(
            page_schema_path.read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Could not load generated page schema: {exc}")
        expected_page_schema = {}

    if not site_root.exists():
        errors.append(f"Built site does not exist: {site_root}")
        return 0

    for route in sorted(set(routes)):
        expected = route_to_built_file(site_root, route)
        if not expected.exists():
            errors.append(
                f"Built route missing {route}: "
                f"{expected.relative_to(site_root)}"
            )

    for filename in (VERIFICATION_FILE, "sitemap.xml", "robots.txt"):
        if not (site_root / filename).exists():
            errors.append(f"Built artifact missing {filename}")

    required_search_files = (
        "search/index.html",
        "pagefind/pagefind.js",
        "pagefind/pagefind-ui.js",
        "pagefind/pagefind-ui.css",
    )
    for filename in required_search_files:
        if not (site_root / filename).exists():
            errors.append(f"Built search artifact missing {filename}")

    html_files = sorted(site_root.rglob("*.html"))
    parsed_by_route: dict[str, LinkCollector] = {}
    text_by_route: dict[str, str] = {}
    schema_pages_checked = 0
    glossary_terms_checked = 0

    for html_file in html_files:
        text = html_file.read_text(encoding="utf-8")
        current_route = built_file_to_route(site_root, html_file)

        parser = LinkCollector()
        parser.feed(text)


        parsed_by_route[current_route] = parser
        text_by_route[current_route] = text


    audit_fragment_links(
        parsed_by_route=parsed_by_route,
        baseurl=baseurl,
        errors=errors,
    )

    for html_file in html_files:
        current_route = built_file_to_route(site_root, html_file)
        text = text_by_route[current_route]
        parser = parsed_by_route[current_route]

        if current_route == "/reference/":
            audit_reference_menu_separators(text, errors)

        if "reference/_internal/" in text or "/_internal/" in text:
            errors.append(
                "Internal Reference path leaked into built HTML: "
                + str(html_file.relative_to(site_root))
            )

        if LEGACY_PAGES_ORIGIN in text:
            errors.append(
                "Legacy GitHub Pages URL leaked into built HTML: "
                + str(html_file.relative_to(site_root))
            )

        if current_route in routes or current_route == "/search/":
            glossary_term_count = audit_structured_data(
                current_route=current_route,
                text=text,
                expected_page_schema=expected_page_schema,
                errors=errors,
            )
            schema_pages_checked += 1
            if current_route == "/glossary/":
                glossary_terms_checked = glossary_term_count
            audit_document_shell(
                current_route=current_route,
                text=text,
                parser=parser,
                baseurl=baseurl,
                errors=errors,
            )

        if current_route in routes:
            audit_page_navigation(
                current_route=current_route,
                parser=parser,
                expected=navigation_map.get(current_route),
                baseurl=baseurl,
                errors=errors,
            )

        for target in parser.links:
            resolved = local_target_path(
                current_route=current_route,
                raw_target=target,
                baseurl=baseurl,
            )
            if resolved is None:
                continue

            if not target_exists(site_root, resolved):
                errors.append(
                    "Broken built-site link: "
                    f"{html_file.relative_to(site_root)} -> {target}"
                )

    print(
        "  Structured-data pages:     "
        f"{schema_pages_checked}"
    )
    print(
        "  Glossary DefinedTerm nodes:"
        f" {glossary_terms_checked}"
    )

    return len(html_files)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--built-site",
        type=Path,
        default=None,
        help="Optional built Jekyll artifact to validate, usually _site.",
    )
    parser.add_argument(
        "--baseurl",
        default=None,
        help="Override the configured baseurl when validating built HTML.",
    )
    args = parser.parse_args()

    errors: list[str] = []

    course_count, reference_count, route_count = check_generated_source(
        errors
    )

    html_count = 0
    if args.built_site is not None:
        baseurl = (
            args.baseurl
            if args.baseurl is not None
            else configured_baseurl()
        )
        html_count = check_built_site(
            args.built_site.resolve(),
            baseurl,
            errors,
        )

    if errors:
        print("Site validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Site validation passed.")
    print(f"  Course pages:              {course_count}")
    print(f"  Reference pages:           {reference_count}")
    print(f"  Total public routes:       {route_count}")
    if args.built_site is not None:
        print(f"  Built HTML files checked:  {html_count}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
