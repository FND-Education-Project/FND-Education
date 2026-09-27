#!/usr/bin/env python3
"""
Validate generated Jekyll source and, when available, the built Pages artifact.

Run after tools/site/prepare_site.py. If _site exists, built HTML links are
checked too. The validator never edits canonical or generated content.
"""

from __future__ import annotations

import argparse
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
    "/sitemap/": WEB / "sitemap" / "index.md",
}

VERIFICATION_FILE = "google65d5cac3c1021024.html"


class LinkCollector(HTMLParser):
    """Collect href/src values from rendered HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        for name, value in attrs:
            if value and name.lower() in {"href", "src"}:
                self.links.append(value)


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


def check_generated_source(errors: list[str]) -> tuple[int, int, int]:
    course_pages, reference_pages, routes = expected_routes()
    ensure_unique_routes(routes, errors)

    for page in course_pages:
        if not page.destination.exists():
            errors.append(
                "Missing generated course page: "
                + str(page.destination.relative_to(ROOT))
            )

    for page in reference_pages:
        if not page.destination.exists():
            errors.append(
                "Missing generated Reference page: "
                + str(page.destination.relative_to(ROOT))
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

    if not machine_sitemap.exists():
        errors.append("Missing generated web/sitemap.xml")
    if not robots.exists():
        errors.append("Missing generated web/robots.txt")

    generated_roots = [
        WEB / "course",
        WEB / "reference",
        WEB / "glossary",
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


def check_built_site(
    site_root: Path,
    baseurl: str,
    errors: list[str],
) -> int:
    _course, _reference, routes = expected_routes()

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

    html_files = sorted(site_root.rglob("*.html"))

    for html_file in html_files:
        text = html_file.read_text(encoding="utf-8")

        if "reference/_internal/" in text or "/_internal/" in text:
            errors.append(
                "Internal Reference path leaked into built HTML: "
                + str(html_file.relative_to(site_root))
            )

        parser = LinkCollector()
        parser.feed(text)

        current_route = built_file_to_route(site_root, html_file)

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
