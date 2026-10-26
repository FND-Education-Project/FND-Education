"""Synthetic #191 curriculum contract: original progress identity never migrates.

This test uses no Cloudflare credentials, D1 rows, live provider or network.
It exercises the actual manifest writer against the exact planned 19/57
current + 9/34 earlier-edition structure before branch reconciliation.
"""
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from tools.site import prepare_site


LEGACY_COUNTS = (4, 2, 3, 2, 3, 4, 5, 4, 4, 3, 5, 3,
                 3, 3, 3, 3, 4, 3, 3, 3, 3, 3, 2)
EARLIER_MODULES = frozenset((6, 7, 8, 9, 10, 11, 12, 14, 15))
NEW_COUNTS = (3, 4, 3, 3, 3)


class ProgressManifestTests(unittest.TestCase):
    def test_revised_course_preserves_75_legacy_ids_and_excludes_16_new_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            course = root / "course"
            web = root / "web"
            course.mkdir()
            (course / "README.md").write_text(
                "# FND Education Course\n\n" +
                "\n".join("#" * 2 + " Part " + word + ": " + word
                          for word in ("One", "Two", "Three", "Four", "Five")),
                encoding="utf-8",
            )
            pages = [SimpleNamespace(kind="course")]
            def put(kind, slot, display, local, is_core, eligible):
                part = (1 if display <= 5 else 2 if display <= 8 else
                        3 if display <= 10 else 4 if display <= 16 else 5)
                folder = course / ("module-" + str(slot))
                folder.mkdir(exist_ok=True)
                location = folder / ("README.md" if kind == "module" else
                                     f"{local:02d}-lesson.md")
                location.write_text(
                    f"# Module {display} — Test module {slot}\n" if kind == "module"
                    else f"# Test module {slot} lesson {local}\n", encoding="utf-8")
                prefix = (f"/course/m{slot}/" if slot <= 23 else
                          f"/course/v2/m{display}/")
                return SimpleNamespace(
                    kind=kind, module_number=slot, part_number=part,
                    display_module_number=display,
                    display_part_number=part, lesson_number=local,
                    source=location, is_core=is_core,
                    progress_eligible=eligible if kind == "lesson" else False,
                    public_url=prefix if kind == "module" else prefix + str(local) + "/",
                )

            # The first five original modules retain their positions.
            # The five concepts-first modules use disjoint source slots 24..28.
            # Former modules 13 and 16..23 are current at display positions 11..19.
            # Earlier edition keeps original routes for 6..12 and 14..15.
            slots = [(number, number, LEGACY_COUNTS[number - 1], True)
                     for number in range(1, 6)]
            slots += [(slot, slot - 18, number, True)
                      for slot, number in zip(range(24, 29), NEW_COUNTS)]
            slots += [(number, display, LEGACY_COUNTS[number - 1], True)
                      for display, number in enumerate(
                          (13, 16, 17, 18, 19, 20, 21, 22, 23), start=11)]
            slots += [(number, number, LEGACY_COUNTS[number - 1], False)
                      for number in sorted(EARLIER_MODULES)]
            for slot, display, count, is_core in slots:
                pages.append(put("module", slot, display, None, is_core, False))
                for local in range(1, count + 1):
                    pages.append(put("lesson", slot, display, local,
                                     is_core, slot <= 23))

            with patch.object(prepare_site, "COURSE_ROOT", course), patch.object(
                prepare_site, "WEB", web
            ):
                prepare_site.write_course_progress_manifest(pages)

            manifest = json.loads(
                (web / "assets/data/course-progress.json").read_text(encoding="utf-8")
            )
            current_modules = [m for part in manifest["parts"] for m in part["modules"]]
            current = [l for mod in current_modules for l in mod["lessons"]]
            earlier = [l for mod in manifest["earlierModules"] for l in mod["lessons"]]
            eligible = [l for l in current + earlier if l["progressEligible"]]
            newly_published = [l for l in current if not l["progressEligible"]]
            self.assertEqual(manifest["version"], 2)
            self.assertEqual(len(current_modules), 19)
            self.assertEqual(len(current), 57)
            self.assertEqual(len(earlier), 34)
            self.assertEqual(len(newly_published), 16)
            self.assertTrue(all(l["id"] is None for l in newly_published))
            self.assertEqual(len(eligible), 75)
            self.assertEqual(manifest["eligibleLessonCount"], 75)
            self.assertEqual(len({l["id"] for l in eligible}), 75)
            originals = {l["id"]: l["url"] for l in eligible}
            self.assertEqual(originals["m4-2"], "/course/m4/2/")
            self.assertEqual(originals["m6-1"], "/course/m6/1/")
            self.assertNotEqual(newly_published[0]["url"], originals["m6-1"])
            self.assertEqual(newly_published[0]["url"], "/course/v2/m6/1/")


if __name__ == "__main__":
    unittest.main()
