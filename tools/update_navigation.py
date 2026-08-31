from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BREAD_START = "<!-- NAV-BREADCRUMB:START -->"
BREAD_END = "<!-- NAV-BREADCRUMB:END -->"
CTX_START = "<!-- NAV-CONTEXT:START -->"
CTX_END = "<!-- NAV-CONTEXT:END -->"

PART_LABELS = {
    "part-1-understanding-fnd": "Part One: Understanding FND",
    "part-2-safety-and-symptoms": "Part Two: Safety and Symptom Knowledge",
    "part-3-non-motor-symptoms": "Part Three: Common Non-Motor Difficulties",
    "part-4-treatment-and-rehabilitation": "Part Four: Treatment and Rehabilitation",
    "part-5-living-with-fnd": "Part Five: Living With FND",
    "part-6-long-term-management": "Part Six: Long-Term Management",
}

MODULE_LABELS = {
    "module-01-what-fnd-is": "Module 1: What FND Is",
    "module-02-how-fnd-is-diagnosed": "Module 2: How FND Is Diagnosed",
    "module-03-causes-mechanisms-and-honest-uncertainty": "Module 3: Causes, Mechanisms, and Honest Uncertainty",
    "module-04-mapping-your-individual-condition": "Module 4: Mapping Your Individual Condition",
    "module-05-medical-safety-and-new-symptoms": "Module 5: Medical Safety and New Symptoms",
    "module-06-functional-seizures-and-episodic-symptoms": "Module 6: Functional Seizures and Episodic Symptoms",
    "module-07-functional-movement-weakness-and-gait-symptoms": "Module 7: Movement, Weakness, and Gait Symptoms",
    "module-08-sensory-visual-balance-and-dizziness-symptoms": "Module 8: Sensory, Visual, Balance, and Dizziness Symptoms",
    "module-09-speech-voice-swallowing-and-breathing-symptoms": "Module 9: Speech, Voice, Swallowing, and Breathing Symptoms",
    "module-10-cognition-memory-and-dissociation": "Module 10: Cognition, Memory, and Dissociation",
    "module-11-pain-migraine-fatigue-and-sleep": "Module 11: Pain, Migraine, Fatigue, and Sleep",
    "module-12-autonomic-and-whole-body-symptoms": "Module 12: Autonomic and Whole-Body Symptoms",
    "module-13-building-an-individual-treatment-team": "Module 13: Building an Individual Treatment Team",
    "module-14-rehabilitation-and-neuroplastic-change": "Module 14: Rehabilitation and Neuroplastic Change",
    "module-15-pacing-activity-and-the-boom-and-bust-cycle": "Module 15: Pacing, Activity, and Boom-and-Bust",
    "module-16-psychological-treatment-without-blame": "Module 16: Psychological Treatment Without Blame",
    "module-17-daily-living-accessibility-and-equipment": "Module 17: Daily Living, Accessibility, and Equipment",
    "module-18-relationships-identity-and-grief": "Module 18: Relationships, Identity, and Grief",
    "module-19-healthcare-communication-and-self-advocacy": "Module 19: Healthcare Communication and Self-Advocacy",
    "module-20-work-disability-and-community-participation": "Module 20: Work, Disability, and Community Participation",
    "module-21-setbacks-relapse-and-changing-symptoms": "Module 21: Setbacks, Relapse, and Changing Symptoms",
    "module-22-building-your-personal-fnd-handbook": "Module 22: Building Your Personal FND Handbook",
    "module-23-reviewing-progress": "Module 23: Reviewing Progress",
}

RELATED_COURSE = {
    "01": "course/part-2-safety-and-symptoms/module-07-functional-movement-weakness-and-gait-symptoms/01-functional-weakness-and-paralysis.md",
    "02": "course/part-2-safety-and-symptoms/module-07-functional-movement-weakness-and-gait-symptoms/02-tremor-jerks-and-spasms.md",
    "03": "course/part-2-safety-and-symptoms/module-07-functional-movement-weakness-and-gait-symptoms/02-tremor-jerks-and-spasms.md",
    "04": "course/part-2-safety-and-symptoms/module-07-functional-movement-weakness-and-gait-symptoms/03-functional-dystonia-and-fixed-postures.md",
    "05": "course/part-2-safety-and-symptoms/module-07-functional-movement-weakness-and-gait-symptoms/04-gait-falls-and-movement-retraining.md",
    "06-diagnostic": "course/part-2-safety-and-symptoms/module-06-functional-seizures-and-episodic-symptoms/01-what-functional-seizures-are-and-how-they-are-diagnosed.md",
    "06-recovery": "course/part-2-safety-and-symptoms/module-06-functional-seizures-and-episodic-symptoms/03-recovery-treatment-and-daily-life.md",
    "07": "course/part-2-safety-and-symptoms/module-08-sensory-visual-balance-and-dizziness-symptoms/01-numbness-altered-sensation-and-hypersensitivity.md",
    "08": "course/part-2-safety-and-symptoms/module-08-sensory-visual-balance-and-dizziness-symptoms/02-visual-symptoms-photophobia-and-sensory-overload.md",
    "09": "course/part-2-safety-and-symptoms/module-09-speech-voice-swallowing-and-breathing-symptoms/01-speech-voice-and-word-blocking.md",
    "10": "course/part-2-safety-and-symptoms/module-09-speech-voice-swallowing-and-breathing-symptoms/02-swallowing-globus-and-nutrition-safety.md",
    "11": "course/part-2-safety-and-symptoms/module-09-speech-voice-swallowing-and-breathing-symptoms/03-cough-breathing-and-upper-airway-symptoms.md",
    "12": "course/part-3-non-motor-symptoms/module-10-cognition-memory-and-dissociation/01-attention-memory-word-finding-and-functional-cognitive-disorder.md",
    "13": "course/part-2-safety-and-symptoms/module-08-sensory-visual-balance-and-dizziness-symptoms/03-dizziness-balance-and-vestibular-overlap.md",
}


def h1(path: Path) -> str:
    if not path.exists():
        return path.stem.replace("-", " ").title()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("-", " ").title()


def rel(current: Path, target: str | Path) -> str:
    target = Path(target)
    return Path(os.path.relpath(ROOT / target, start=current.parent)).as_posix()


def link(current: Path, label: str, target: str | Path) -> str:
    return f"[{label}]({rel(current, target)})"


def strip_marked(text: str, start: str, end: str) -> str:
    pattern = re.compile(rf"\n?{re.escape(start)}.*?{re.escape(end)}\n?", re.S)
    return pattern.sub("\n", text)


def breadcrumb_for(path: Path) -> str:
    rp = path.relative_to(ROOT)
    parts = rp.parts
    crumbs: list[str] = []

    if rp == Path("README.md"):
        crumbs = ["**Home**"]
    else:
        crumbs.append(link(path, "Home", "README.md"))

        if parts[0] == "course":
            crumbs.append(link(path, "Course", "course/README.md"))
            if len(parts) >= 2 and parts[1] in PART_LABELS:
                crumbs.append(PART_LABELS[parts[1]])
            if len(parts) >= 3 and parts[2] in MODULE_LABELS:
                crumbs.append(link(path, MODULE_LABELS[parts[2]], Path("course") / parts[1] / parts[2] / "README.md"))
            if path.name != "README.md":
                crumbs.append(f"**{h1(path)}**")

        elif parts[0] == "reference":
            crumbs.append(link(path, "Reference Library", "reference/README.md"))
            if len(parts) >= 2:
                if parts[1] == "diagnostic-signs":
                    crumbs.append(link(path, "Diagnostic Signs", "reference/diagnostic-signs/README.md"))
                elif parts[1] == "recovery-techniques":
                    crumbs.append(link(path, "Recovery Techniques", "reference/recovery-techniques/README.md"))
            if "functional_seizures" in parts:
                crumbs.append(link(path, "Functional Seizure Recovery Materials", "reference/recovery-techniques/functional_seizures/README.md"))
            if "unified_cbt_booklets" in parts:
                crumbs.append(link(path, "Unified CBT Booklets", "reference/recovery-techniques/functional_seizures/unified_cbt_booklets/README.md"))
            if path.name != "README.md":
                crumbs.append(f"**{h1(path)}**")

        elif parts[0] == "glossary":
            crumbs.append("**Glossary**")

        elif parts[0] == "research":
            crumbs.extend(["Research", f"**{h1(path)}**"])

        elif parts[0] == "docs" and len(parts) >= 2 and parts[1] == "project":
            crumbs.append("Project Documentation")
            if len(parts) >= 3 and parts[2] == "syllabus":
                crumbs.append("Detailed Syllabus")
            crumbs.append(f"**{h1(path)}**")

        elif rp == Path("SITEMAP.md"):
            crumbs.append("**Site Map**")
        else:
            crumbs.append(f"**{h1(path)}**")

    return f"{BREAD_START}\n{' › '.join(crumbs)}\n{BREAD_END}"


def module_readmes() -> list[Path]:
    paths = list((ROOT / "course").glob("part-*/*/README.md"))
    return sorted(paths, key=lambda p: int(re.search(r"module-(\d+)", p.parent.name).group(1)))


def course_context(path: Path) -> list[str]:
    rp = path.relative_to(ROOT)
    lines: list[str] = []

    if rp == Path("course/README.md"):
        first = module_readmes()[0]
        lines.append(f"**Continue:** {link(path, 'Start with Module 1', first.relative_to(ROOT))}")
        return lines

    if path.name == "README.md" and "module-" in path.parent.name:
        mods = module_readmes()
        idx = mods.index(path)
        nav: list[str] = []
        if idx > 0:
            nav.append(link(path, "← Previous module", mods[idx - 1].relative_to(ROOT)))
        nav.append(link(path, "Course index", "course/README.md"))
        if idx < len(mods) - 1:
            nav.append(link(path, "Next module →", mods[idx + 1].relative_to(ROOT)))
        lines.append("**Course:** " + " · ".join(nav))
        return lines

    if "module-" in path.parent.name:
        siblings = sorted(p for p in path.parent.glob("[0-9][0-9]-*.md"))
        idx = siblings.index(path)
        nav: list[str] = []
        if idx > 0:
            nav.append(link(path, "← Previous", siblings[idx - 1].relative_to(ROOT)))
        nav.append(link(path, "Module overview", path.parent.joinpath("README.md").relative_to(ROOT)))
        if idx < len(siblings) - 1:
            nav.append(link(path, "Next →", siblings[idx + 1].relative_to(ROOT)))
        lines.append("**In this module:** " + " · ".join(nav))
    return lines


def reference_context(path: Path) -> list[str]:
    rp = path.relative_to(ROOT)
    parts = rp.parts
    lines: list[str] = []

    if rp == Path("reference/README.md"):
        lines.append(
            "**Browse:** "
            + " · ".join(
                [
                    link(path, "Diagnostic Signs", "reference/diagnostic-signs/README.md"),
                    link(path, "Recovery Techniques", "reference/recovery-techniques/README.md"),
                ]
            )
        )
        return lines

    if rp == Path("reference/diagnostic-signs/README.md"):
        lines.append(
            "**Reference:** "
            + " · ".join(
                [
                    link(path, "Reference Library", "reference/README.md"),
                    link(path, "Recovery Techniques", "reference/recovery-techniques/README.md"),
                ]
            )
        )
        return lines

    if rp == Path("reference/recovery-techniques/README.md"):
        lines.append(
            "**Reference:** "
            + " · ".join(
                [
                    link(path, "Reference Library", "reference/README.md"),
                    link(path, "Diagnostic Signs", "reference/diagnostic-signs/README.md"),
                    link(path, "Technique Index", "reference/recovery-techniques/technique-index.md"),
                ]
            )
        )
        return lines

    if len(parts) >= 3 and parts[1] in {"diagnostic-signs", "recovery-techniques"} and re.match(r"\d\d-", path.name):
        num = path.name[:2]
        current_collection = parts[1]
        other_collection = "recovery-techniques" if current_collection == "diagnostic-signs" else "diagnostic-signs"
        other_path = ROOT / "reference" / other_collection / path.name
        nav: list[str] = []
        nav.append(link(path, "Collection index", Path("reference") / current_collection / "README.md"))
        if other_path.exists():
            label = "Recovery techniques for this symptom" if current_collection == "diagnostic-signs" else "Diagnostic signs for this symptom"
            nav.append(link(path, label, other_path.relative_to(ROOT)))
        key = f"{num}-{'diagnostic' if current_collection == 'diagnostic-signs' else 'recovery'}" if num == "06" else num
        target = RELATED_COURSE.get(key)
        if target and (ROOT / target).exists():
            nav.append(link(path, "Related course page", target))
        lines.append("**Related:** " + " · ".join(nav))
        return lines

    if rp == Path("reference/recovery-techniques/technique-index.md"):
        lines.append(
            "**Reference:** "
            + " · ".join(
                [
                    link(path, "Recovery Techniques", "reference/recovery-techniques/README.md"),
                    link(path, "Reference Library", "reference/README.md"),
                ]
            )
        )
        return lines

    if "unified_cbt_booklets" in parts:
        nav = [
            link(path, "Booklet collection", "reference/recovery-techniques/functional_seizures/unified_cbt_booklets/README.md"),
            link(path, "Functional-seizure recovery materials", "reference/recovery-techniques/functional_seizures/README.md"),
            link(path, "Functional-seizure recovery page", "reference/recovery-techniques/06-functional-seizures.md"),
        ]
        if path.name != "README.md":
            is_guide = "content-creator-guide" in path.name
            peers = sorted(
                p for p in path.parent.glob("*.md")
                if p.name != "README.md" and (("content-creator-guide" in p.name) == is_guide)
            )
            if path in peers:
                idx = peers.index(path)
                if idx > 0:
                    nav.insert(0, link(path, "← Previous", peers[idx - 1].relative_to(ROOT)))
                if idx < len(peers) - 1:
                    nav.append(link(path, "Next →", peers[idx + 1].relative_to(ROOT)))
        lines.append("**CBT materials:** " + " · ".join(nav))
        return lines

    if "functional_seizures" in parts:
        lines.append(
            "**Functional seizures:** "
            + " · ".join(
                [
                    link(path, "Recovery Techniques", "reference/recovery-techniques/README.md"),
                    link(path, "Functional-seizure recovery page", "reference/recovery-techniques/06-functional-seizures.md"),
                    link(path, "Unified CBT booklets", "reference/recovery-techniques/functional_seizures/unified_cbt_booklets/README.md"),
                ]
            )
        )
    return lines


def contextual_lines(path: Path) -> list[str]:
    rp = path.relative_to(ROOT)
    lines: list[str] = []

    if rp.parts[0] == "course":
        lines.extend(course_context(path))
    elif rp.parts[0] == "reference":
        lines.extend(reference_context(path))
    elif rp == Path("README.md"):
        lines.append(
            "**Explore:** "
            + " · ".join(
                [
                    link(path, "Course", "course/README.md"),
                    link(path, "Reference Library", "reference/README.md"),
                    link(path, "Glossary", "glossary/README.md"),
                ]
            )
        )
    elif rp.parts[0] == "research":
        lines.append("**Research:** " + link(path, "Research and citation policy", "docs/project/research-and-citation-policy.md"))
    elif rp.parts[:2] == ("docs", "project"):
        lines.append(
            "**Project:** "
            + " · ".join(
                [
                    link(path, "Project status", "docs/project/project-status.md"),
                    link(path, "Core principles", "docs/project/core-principles.md"),
                ]
            )
        )

    global_nav = "**Navigate:** " + " · ".join(
        [
            link(path, "Home", "README.md"),
            link(path, "Course", "course/README.md"),
            link(path, "Reference Library", "reference/README.md"),
            link(path, "Site Map", "SITEMAP.md"),
        ]
    )
    lines.append(global_nav)
    return lines


def render_context(path: Path) -> str:
    return f"{CTX_START}\n" + "\n\n".join(contextual_lines(path)) + f"\n{CTX_END}"


def insert_navigation(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = strip_marked(text, BREAD_START, BREAD_END)
    text = strip_marked(text, CTX_START, CTX_END)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"

    bread = breadcrumb_for(path)
    lines = text.splitlines()
    h1_index = next((i for i, line in enumerate(lines) if line.startswith("# ")), None)
    if h1_index is not None:
        lines[h1_index + 1:h1_index + 1] = ["", bread, ""]
        text = "\n".join(lines).strip() + "\n"
    else:
        text = bread + "\n\n" + text

    context = render_context(path)
    source_heading = re.compile(
        r"(?im)^##\s+(?:Research and Sources|Sources|Evidence and Sources|Research Sources)\s*$"
    )
    matches = list(source_heading.finditer(text))
    if matches:
        pos = matches[-1].start()
        before = text[:pos].rstrip()
        after = text[pos:].lstrip()
        text = before + "\n\n" + context + "\n\n" + after
    else:
        text = text.rstrip() + "\n\n" + context + "\n"

    path.write_text(text, encoding="utf-8")


def details(summary: str, body: str, open_by_default: bool = False) -> str:
    open_attr = " open" if open_by_default else ""
    return f"<details{open_attr}>\n<summary><strong>{summary}</strong></summary>\n\n{body.strip()}\n\n</details>"


def page_list(paths: list[Path], current: Path) -> str:
    return "\n".join(f"- {link(current, h1(p), p.relative_to(ROOT))}" for p in paths)


def generate_sitemap() -> None:
    sitemap = ROOT / "SITEMAP.md"
    out: list[str] = [
        "# FND Education Site Map",
        "",
        "Use the sections below to drill down into the course, reference library, research material, and project documentation. Only pages that currently exist in the repository are listed.",
        "",
        f"- {link(sitemap, 'Home', 'README.md')}",
        f"- {link(sitemap, 'Course index', 'course/README.md')}",
        f"- {link(sitemap, 'Reference Library', 'reference/README.md')}",
        f"- {link(sitemap, 'Glossary', 'glossary/README.md')}",
        "",
    ]

    course_body: list[str] = [f"- {link(sitemap, 'Course index', 'course/README.md')}", ""]
    for part_dir in sorted((ROOT / "course").glob("part-*")):
        if not part_dir.is_dir():
            continue
        module_blocks: list[str] = []
        for module_dir in sorted(part_dir.glob("module-*"), key=lambda p: int(re.search(r"module-(\d+)", p.name).group(1))):
            readme = module_dir / "README.md"
            pages = sorted(module_dir.glob("[0-9][0-9]-*.md"))
            body = f"- {link(sitemap, 'Module overview', readme.relative_to(ROOT))}"
            if pages:
                body += "\n" + page_list(pages, sitemap)
            module_blocks.append(details(MODULE_LABELS.get(module_dir.name, h1(readme)), body))
        course_body.append(details(PART_LABELS.get(part_dir.name, part_dir.name), "\n\n".join(module_blocks)))
    out.append(details("Course", "\n\n".join(course_body), open_by_default=True))
    out.append("")

    diagnostic_pages = sorted((ROOT / "reference/diagnostic-signs").glob("[0-9][0-9]-*.md"))
    recovery_pages = sorted((ROOT / "reference/recovery-techniques").glob("[0-9][0-9]-*.md"))
    fs_root = ROOT / "reference/recovery-techniques/functional_seizures"
    booklet_root = fs_root / "unified_cbt_booklets"
    fs_misc = sorted(p for p in fs_root.glob("*.md") if p.name != "README.md")
    booklets = sorted(p for p in booklet_root.glob("*.md") if p.name != "README.md" and "content-creator-guide" not in p.name)
    creator_guides = sorted(p for p in booklet_root.glob("*.md") if "content-creator-guide" in p.name)

    reference_body = [
        f"- {link(sitemap, 'Reference Library index', 'reference/README.md')}",
        details(
            "Symptom-Specific Diagnostic Signs",
            f"- {link(sitemap, 'Diagnostic Signs index', 'reference/diagnostic-signs/README.md')}\n" + page_list(diagnostic_pages, sitemap),
        ),
        details(
            "Symptom Recovery and Management Techniques",
            "\n".join(
                [
                    f"- {link(sitemap, 'Recovery Techniques index', 'reference/recovery-techniques/README.md')}",
                    f"- {link(sitemap, 'Technique index', 'reference/recovery-techniques/technique-index.md')}",
                    page_list(recovery_pages, sitemap),
                ]
            ),
        ),
        details(
            "Functional Seizure Recovery Materials",
            "\n".join(
                [
                    f"- {link(sitemap, 'Functional seizure materials index', 'reference/recovery-techniques/functional_seizures/README.md')}",
                    page_list(fs_misc, sitemap),
                    details(
                        "Unified CBT Booklets",
                        f"- {link(sitemap, 'Booklet collection index', 'reference/recovery-techniques/functional_seizures/unified_cbt_booklets/README.md')}\n"
                        + page_list(booklets, sitemap),
                    ),
                    details("Content-Creator Guides", page_list(creator_guides, sitemap)),
                ]
            ),
        ),
        details(
            "Community and Review Working Material",
            page_list(
                [
                    ROOT / "reference/recovery-techniques/community-experience-quotes.md",
                    ROOT / "reference/recovery-techniques/episodic-flare-community-quote-review.md",
                ],
                sitemap,
            ),
        ),
    ]
    out.append(details("Reference Library", "\n\n".join(reference_body), open_by_default=True))
    out.append("")

    research_body = "\n".join(
        [
            f"- {link(sitemap, 'Glossary', 'glossary/README.md')}",
            f"- {link(sitemap, 'Citation Index', 'research/citation-index.md')}",
            f"- {link(sitemap, 'Research and Citation Policy', 'docs/project/research-and-citation-policy.md')}",
            f"- {link(sitemap, 'Evidence Standard', 'docs/project/evidence-standard.md')}",
        ]
    )
    out.append(details("Glossary and Research", research_body))
    out.append("")

    project_files = sorted(p for p in (ROOT / "docs/project").glob("*.md"))
    syllabus_files = sorted((ROOT / "docs/project/syllabus").glob("*.md"), key=lambda p: int(re.search(r"module-(\d+)", p.name).group(1)))
    project_body = page_list(project_files, sitemap) + "\n\n" + details("Detailed Module Syllabus Files", page_list(syllabus_files, sitemap))
    out.append(details("Project and Contributor Documentation", project_body))
    out.append("")

    sitemap.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    generate_sitemap()
    markdown_files = sorted(
        p for p in ROOT.rglob("*.md")
        if ".git" not in p.parts and ".github" not in p.parts
    )
    for path in markdown_files:
        insert_navigation(path)
    print(f"Updated navigation in {len(markdown_files)} Markdown files.")


if __name__ == "__main__":
    main()
