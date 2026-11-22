import test from "node:test";
import assert from "node:assert/strict";
import {
  CURRENT_COURSE, validateCourseManifest, chooseNextLesson, canonicalLessonUrl
} from "../src/course-contract.mjs";

/** Mirrors the canonical 19-module/57-lesson manifest in PR #154 tests. */
function currentManifest() {
  const breaks = [5, 8, 10, 16, 19];
  const parts = [];
  let number = 0;
  for (const boundary of breaks) {
    const modules = [];
    while (number < boundary) {
      number += 1;
      modules.push({
        lessons: Array.from({ length: CURRENT_COURSE.moduleCounts[number - 1] },
          (_, index) => ({
            id: "m" + number + "-" + (index + 1),
            url: "/course/m" + number + "/" + (index + 1) + "/",
            title: "Lesson " + number + "." + (index + 1),
            progressEligible: true
          }))
      });
    }
    parts.push({ modules });
  }
  return { version: 2, parts, eligibleLessonCount: 57, earlierModules: [] };
}

test("current canonical course contains five parts, 19 modules, 57 lessons", () => {
  const ordered = validateCourseManifest(currentManifest());
  assert.equal(ordered.length, 57);
  assert.equal(ordered[0].id, "m1-1");
  assert.equal(ordered.at(-1).id, "m19-2");
  assert.equal(ordered[15].id, "m6-2");
  assert.equal(canonicalLessonUrl(ordered.at(-1)), "https://fndeducationproject.org/course/m19/2/");
});

test("rejects retired manifest version, earlier editions or old course size", () => {
  const manifest = currentManifest();
  assert.throws(() => validateCourseManifest({ ...manifest, version: 1 }));
  assert.throws(() => validateCourseManifest({ ...manifest, earlierModules: [{ id: "old" }] }));
  assert.throws(() => validateCourseManifest({ ...manifest, eligibleLessonCount: 74 }));
  assert.throws(() => validateCourseManifest({ ...manifest, parts: manifest.parts.slice(0, 4) }));
});

test("rejects stale, duplicated, incomplete and noncanonical paths", () => {
  const manifest = currentManifest();
  manifest.parts[1].modules[0].lessons[0].url = "/course/v2/m6/1/";
  assert.throws(() => validateCourseManifest(manifest));
  const manifest2 = currentManifest();
  manifest2.parts[4].modules.at(-1).lessons[1].id = "m23-2";
  assert.throws(() => validateCourseManifest(manifest2));
  const manifest3 = currentManifest();
  manifest3.parts[0].modules[0].lessons.pop();
  assert.throws(() => validateCourseManifest(manifest3));
  const manifest4 = currentManifest();
  manifest4.parts[1].modules[0].lessons[0].progressEligible = false;
  assert.throws(() => validateCourseManifest(manifest4));
});

test("current progress resumes safely from manifest-only canonical URLs", () => {
  const ordered = validateCourseManifest(currentManifest());
  assert.equal(chooseNextLesson(ordered, { lessons: {}, lastLesson: "m6-1" }).id, "m6-1");
  assert.equal(chooseNextLesson(ordered, { lessons: { "m6-1": { completed: true } },
    lastLesson: "m6-1" }).id, "m6-2");
  assert.equal(chooseNextLesson(ordered, { lessons: {}, lastLesson: "m23-1" }).id, "m1-1");
  const allDone = Object.fromEntries(ordered.map(item => [item.id, { completed: true }]));
  assert.equal(chooseNextLesson(ordered, { lessons: allDone, lastLesson: "m19-2" }), null);
});

test("untrusted progress fields cannot create an external redirect", () => {
  const ordered = validateCourseManifest(currentManifest());
  const next = chooseNextLesson(ordered, {
    lastLesson: "m6-1",
    lessons: { "m6-1": { completed: false, url: "https://attacker.invalid" } }
  });
  assert.equal(canonicalLessonUrl(next), "https://fndeducationproject.org/course/m6/1/");
  assert.throws(() => canonicalLessonUrl({ id: "m6-1", url: "https://attacker.invalid/" }));
});
