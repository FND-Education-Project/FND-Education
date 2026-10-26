"""Synthetic 19-module/57-lesson account progress manifest contract.

Tests the manifest builder without credentials, live D1 or the public site.
The old 75-lesson test dataset has no place in this new course.
"""
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from tools.site import prepare_site

COUNTS = (4, 2, 3, 2, 3, 3, 4, 3, 3, 3,
          3, 3, 4, 3, 3, 3, 3, 3, 2)


class ProgressManifestTests(unittest.TestCase):
    def test_57_current_lessons_and_no_earlier_edition(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            course = root / "course"
            web = root / "web"
            course.mkdir()
            (course / "README.md").write_text(
                "# Course\n\n" +
                "\n".join("## Part " + word + ": Current"
                          for word in ("One", "Two", "Three", "Four", "Five")),
                encoding="utf-8",
            )
            pages = [SimpleNamespace(kind="course")]
            for module, count in enumerate(COUNTS, 1):
                part = (1 if module <= 5 else 2 if module <= 8 else
                        3 if module <= 10 else 4 if module <= 16 else 5)
                base = course / f"module-{module:02d}-example"
                base.mkdir()
                overview = base / "README.md"
                overview.write_text(f"# Module {module} — Example\n", encoding="utf-8")
                prefix = f"/course/m{module}/"
                pages.append(SimpleNamespace(
                    kind="module", module_number=module, part_number=part,
                    source=overview, public_url=prefix,
                    display_module_number=module,
                    display_part_number=part, is_core=True))
                for number in range(1, count + 1):
                    lesson = base / f"{number:02d}-example.md"
                    lesson.write_text(f"# Example lesson {number}\n", encoding="utf-8")
                    pages.append(SimpleNamespace(
                        kind="lesson", module_number=module, part_number=part,
                        lesson_number=number, source=lesson,
                        public_url=prefix + str(number) + "/",
                        display_module_number=module,
                        display_part_number=part, is_core=True,
                        progress_eligible=True))
            with patch.object(prepare_site, "COURSE_ROOT", course), patch.object(
                prepare_site, "WEB", web
            ):
                prepare_site.write_course_progress_manifest(pages)
            manifest = json.loads(
                (web / "assets/data/course-progress.json").read_text(encoding="utf-8"))
            modules = [mod for part in manifest["parts"] for mod in part["modules"]]
            lessons = [lesson for mod in modules for lesson in mod["lessons"]]
            self.assertEqual(len(modules), 19)
            self.assertEqual(len(lessons), 57)
            self.assertEqual(manifest["eligibleLessonCount"], 57)
            self.assertEqual(manifest["earlierModules"], [])
            self.assertTrue(all(item["progressEligible"] for item in lessons))
            self.assertEqual(len({item["id"] for item in lessons}), 57)
            self.assertEqual(lessons[0]["id"], "m1-1")
            self.assertEqual(modules[5]["lessons"][0]["id"], "m6-1")
            self.assertEqual(modules[-1]["lessons"][-1]["id"], "m19-2")
            self.assertEqual(modules[5]["lessons"][0]["url"], "/course/m6/1/")


if __name__ == "__main__":
    unittest.main()
