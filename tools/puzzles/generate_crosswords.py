#!/usr/bin/env python3
"""Build five scored, ready-to-review crossword alternatives from an Excel file.

Examples:
  python tools/puzzles/generate_crosswords.py questions.xlsx --module 1 --lesson 2
  python tools/puzzles/generate_crosswords.py questions.xlsx --module 1
  python tools/puzzles/generate_crosswords.py questions.xlsx --all
  python tools/puzzles/generate_crosswords.py questions.xlsx --list
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

from crossword_builder import (
    export_gallery, is_printable, read_workbook, select_entries, top_layouts,
    verify_layout,
)


DEFAULT_OUTPUT = Path("tools/puzzles/.crossword-output")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create scored crossword layouts and three matched PDFs "
                    "for each of the top five options."
    )
    parser.add_argument("workbook", type=Path, help=".xlsx with clue, answer, "
                        "priority, lesson, module columns.")
    group = parser.add_argument_group("Selection: one lesson, one module, or all")
    group.add_argument("--module", type=int, help="Module number (required for lessons)")
    group.add_argument("--lesson", type=int, help="Lesson number within --module")
    group.add_argument("--all", action="store_true", help="Use the entire workbook")
    group.add_argument("--list", action="store_true", help="List available "
                       "modules and lessons, without generating PDFs")
    parser.add_argument("--max-words", type=int, default=24,
                        help="Maximum answers per crossword (default: 24)")
    parser.add_argument("--max-side", type=int, default=29,
                        help="Maximum grid rows/columns (default: 29)")
    parser.add_argument("--attempts", type=int, default=250,
                        help="Number of layouts to try (default: 250)")
    parser.add_argument("--top", type=int, default=5,
                        help="Number of top printable alternatives (default: 5)")
    parser.add_argument("--seed", type=int, default=1,
                        help="Reproducible generation seed (default: 1)")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT,
                        help="Output directory (default: tools/puzzles/.crossword-output)")
    parser.add_argument("--title", default=None,
                        help="Printed crossword title, if different from selection")
    args = parser.parse_args(argv)
    if args.module is not None and args.module < 1:
        parser.error("--module must be positive.")
    if args.lesson is not None and args.lesson < 1:
        parser.error("--lesson must be positive.")
    if args.all and (args.module is not None or args.lesson is not None):
        parser.error("--all cannot be used with --module or --lesson.")
    if args.lesson is not None and args.module is None:
        parser.error("--lesson requires --module.")
    if not (args.list or args.all or args.module is not None):
        parser.error("Select --module N [--lesson N], --all, or --list.")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        entries, notes = read_workbook(args.workbook)
        if args.list:
            print(f"Workbook: {args.workbook} ({len(entries)} source questions)")
            for mod, les in sorted({(e.module, e.lesson) for e in entries}):
                n = sum(e.module == mod and e.lesson == les for e in entries)
                print(f"  Module {mod}, Lesson {les}: {n} questions")
            return 0

        mode = "all" if args.all else "lesson" if args.lesson else "module"
        primary, loans, duplicates = select_entries(
            entries, mode, args.module, args.lesson
        )
        notes.extend(duplicates)
        default_title = (
            "FND Education — Full Course Review" if mode == "all" else
            f"FND Education — Module {args.module} Review" if mode == "module" else
            f"FND Education — Module {args.module}, Lesson {args.lesson}"
        )
        title = args.title or default_title
        if len(primary) < 3 and len(primary) + len(loans) < 3:
            raise ValueError("At least three distinct usable answers are required.")
        candidates = top_layouts(
            primary, loans, attempts=args.attempts, top=args.top,
            max_words=args.max_words, max_side=args.max_side, seed=args.seed,
        )
        # The paper standard is non-negotiable: never shrink below 14pt,
        # spill clues over extra pages, or silently drop a word bank.
        eligible = [candidate for candidate in candidates if is_printable(candidate)]
        chosen = eligible[:args.top]
        if not chosen:
            raise ValueError(
                "No valid one-page layouts found. Try more --attempts, fewer "
                "--max-words, a smaller --max-side, or more crossing-friendly "
                "answers; the 14-point print standard was not relaxed."
            )
        for layout in chosen:
            verify_layout(layout)
        selection = {
            "mode": mode, "module": args.module, "lesson": args.lesson,
            "attempts": args.attempts, "seed": args.seed,
            "max_words": args.max_words, "max_side": args.max_side,
            "selected_question_count": len(primary),
            "eligible_earlier_question_count": len(loans),
        }
        export_gallery(chosen, args.out, title, primary, notes, selection)
        print(f"Generated {len(chosen)} of {args.top} requested distinct "
              f"printable layouts in {args.out}/")
        print(f"Open {args.out / 'index.html'} in your browser.")
        print(f"See {args.out / 'report.json'} for borrowed and unused answers.")
        for i, layout in enumerate(chosen, 1):
            print(f"  Option {i}: score {layout.score:.2f}/100; "
                  f"{layout.metrics['words']} answers; "
                  f"{layout.metrics['borrowed_words']} borrowed; "
                  f"{layout.metrics['words_with_2plus_crossings']} with 2+ crossings")
        if len(chosen) < args.top:
            print("Note: fewer than five distinct layouts met the one-page standard.")
        return 0
    except (ValueError, OSError, ImportError) as error:
        print(f"Crossword generator error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
