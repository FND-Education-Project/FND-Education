#!/usr/bin/env python3
"""Publish an allowlisted, validated, read-only JSON snapshot of the Excel clue bank.

No dependency on Excel, Streamlit, or a server in the public website. The
workbook remains the authoring source; this file runs in the Pages build.
Only five approved fields are exported. Do not publish private spreadsheets.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile, BadZipFile

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "tools/puzzles/FND_Crossword_Question_Bank_Template.xlsx"
OUTPUT = ROOT / "web/assets/data/crossword-bank.json"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
RELS = "{http://schemas.openxmlformats.org/package/2006/relationships}"
FIELDS = ("clue", "answer", "priority", "lesson", "module")
MAX_ROWS = 10000


def col_index(ref: str) -> int:
    prefix = re.match(r"^[A-Z]+", ref)
    if not prefix:
        raise ValueError("Invalid spreadsheet cell position")
    number = 0
    for ch in prefix.group():
        number = number * 26 + ord(ch) - 64
    return number - 1


def rows_from_xlsx(path: Path):
    if not path.is_file() or path.stat().st_size > 15_000_000:
        raise ValueError("Missing or too-large approved crossword workbook")
    with ZipFile(path) as book:
        shared = []
        if "xl/sharedStrings.xml" in book.namelist():
            root = ET.fromstring(book.read("xl/sharedStrings.xml"))
            for si in root.findall("m:si", NS):
                shared.append("".join(node.text or "" for node in si.findall(".//m:t", NS)))
        wb = ET.fromstring(book.read("xl/workbook.xml"))
        first = wb.find("m:sheets/m:sheet", NS)
        if first is None:
            raise ValueError("Excel has no worksheet")
        rel_id = first.get("{" + NS["r"] + "}id")
        rels = ET.fromstring(book.read("xl/_rels/workbook.xml.rels"))
        rel = next((x for x in rels.findall(RELS + "Relationship")
                    if x.get("Id") == rel_id), None)
        if rel is None:
            raise ValueError("Could not find the first worksheet")
        target = rel.get("Target", "").lstrip("/")
        sheet_path = target if target.startswith("xl/") else "xl/" + target
        if ".." in sheet_path.split("/"):
            raise ValueError("Invalid worksheet reference")
        sheet = ET.fromstring(book.read(sheet_path))
        for row in sheet.findall("m:sheetData/m:row", NS):
            result = {}
            for cell in row.findall("m:c", NS):
                index = col_index(cell.get("r", ""))
                ctype = cell.get("t", "")
                if ctype == "inlineStr":
                    string = "".join(n.text or "" for n in cell.findall(".//m:is//m:t", NS))
                else:
                    v = cell.find("m:v", NS)
                    string = "" if v is None or v.text is None else v.text
                    if ctype == "s" and string:
                        string = shared[int(string)]
                result[index] = string.strip()
            yield result


def positive_integer(text: str, label: str, row: int) -> int:
    found = re.fullmatch(r"(?:module|lesson)?[\s_#:-]*(\d+)", text.strip(), re.I)
    if not found or int(found.group(1)) < 1:
        raise ValueError(f"Row {row}: invalid {label}")
    return int(found.group(1))


def export_bank(source: Path = SOURCE, destination: Path = OUTPUT) -> list[dict]:
    lines = iter(rows_from_xlsx(source))
    header = next(lines, None)
    if header is None:
        raise ValueError("Empty crossword question bank")
    fields = {str(value).strip().lower(): idx for idx, value in header.items()}
    if any(name not in fields for name in FIELDS):
        raise ValueError("Crossword workbook needs clue, answer, priority, lesson, module")
    entries = []
    for number, raw in enumerate(lines, 2):
        if not any(str(v).strip() for v in raw.values()):
            continue
        if number > MAX_ROWS + 1:
            raise ValueError("Too many crossword questions")
        value = lambda name: str(raw.get(fields[name], "")).strip()
        clue, original = value("clue"), value("answer")
        answer = re.sub(r"[\s-]+", "", original).upper()
        if not clue or len(clue) > 500:
            raise ValueError(f"Row {number}: clue must contain 1–500 characters")
        if not re.fullmatch(r"[A-Z]{2,}", answer) or len(answer) > 40:
            raise ValueError(f"Row {number}: use 2–40 A–Z letters in the answer")
        p = value("priority").lower()
        priorities = {"": 2, "high": 1, "medium": 2, "normal": 2,
                      "low": 3, "1": 1, "2": 2, "3": 3}
        if p not in priorities:
            raise ValueError(f"Row {number}: priority must be 1, 2 or 3")
        entries.append({"clue": clue, "answer": answer, "display_answer": original,
                        "priority": priorities[p],
                        "lesson": positive_integer(value("lesson"), "lesson", number),
                        "module": positive_integer(value("module"), "module", number)})
    if not entries:
        raise ValueError("No usable questions in workbook")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps({"schema": 1, "questions": entries}, ensure_ascii=False,
                   separators=(",", ":")) + "\n", encoding="utf-8")
    return entries


if __name__ == "__main__":
    entries = export_bank()
    print(f"Published {len(entries)} crossword clues from approved Excel bank")
