/**
 * Future companion-app lesson manifest contract (NOT yet wired to UI/API).
 *
 * PR #191 merged the canonical five-part, 19-module, 57-lesson course.
 * Draft account PR #154 generates manifest version 2. Previous syllabus
 * and /course/v2/ routes are NOT valid progress destinations.
 *
 * Pure functions: no network requests, local data changes, or login.
 */
export const CURRENT_COURSE = Object.freeze({
  manifestVersion: 2,
  partCount: 5,
  moduleCounts: Object.freeze([4, 2, 3, 2, 3, 3, 4, 3, 3, 3, 3, 3, 4, 3, 3, 3, 3, 3, 2]),
  lessonCount: 57
});
export const COURSE_SITE_ORIGIN = "https://fndeducationproject.org";

/**
 * Validate the generator's ordered manifest before using account progress.
 * Fail closed for retired modules/URLs and unknown schema; maintain in sync
 * with the generator and Worker if the curriculum changes again.
 */
export function validateCourseManifest(manifest) {
  const counts = CURRENT_COURSE.moduleCounts;
  if (!manifest || typeof manifest !== "object" ||
      manifest.version !== CURRENT_COURSE.manifestVersion ||
      manifest.eligibleLessonCount !== CURRENT_COURSE.lessonCount ||
      !Array.isArray(manifest.earlierModules) || manifest.earlierModules.length !== 0 ||
      !Array.isArray(manifest.parts) ||
      manifest.parts.length !== CURRENT_COURSE.partCount) {
    throw new Error("Unsupported or retired course manifest");
  }

  const ordered = [];
  const ids = new Set();
  let moduleIndex = 0;

  for (const part of manifest.parts) {
    if (!part || !Array.isArray(part.modules)) throw new Error("Invalid course part");
    for (const module of part.modules) {
      moduleIndex += 1;
      const number = moduleIndex;
      if (number > counts.length ||
          !module || !Array.isArray(module.lessons) ||
          module.lessons.length !== counts[number - 1]) {
        throw new Error("Unexpected course module or lesson count");
      }
      for (let lessonIndex = 0; lessonIndex < module.lessons.length; lessonIndex += 1) {
        const lesson = module.lessons[lessonIndex];
        const id = "m" + number + "-" + (lessonIndex + 1);
        const url = "/course/m" + number + "/" + (lessonIndex + 1) + "/";
        if (!lesson || lesson.progressEligible !== true ||
            lesson.id !== id || lesson.url !== url ||
            typeof lesson.title !== "string" || !lesson.title.trim() ||
            ids.has(id)) {
          throw new Error("Unknown, duplicated or outdated lesson identifier");
        }
        ids.add(id);
        ordered.push(Object.freeze({ id, title: lesson.title, url }));
      }
    }
  }
  if (moduleIndex !== counts.length || ordered.length !== CURRENT_COURSE.lessonCount) {
    throw new Error("Course manifest is incomplete");
  }
  return Object.freeze(ordered);
}

/** Never navigate to a user/account-supplied URL as if it were a lesson. */
export function canonicalLessonUrl(lesson) {
  if (!lesson || !/^m(?:[1-9]|1[0-9])-[1-9][0-9]*$/.test(lesson.id)) {
    throw new Error("Invalid lesson");
  }
  const [moduleNumber, pageNumber] = lesson.id.slice(1).split("-").map(Number);
  if (moduleNumber < 1 || moduleNumber > CURRENT_COURSE.moduleCounts.length ||
      pageNumber < 1 || pageNumber > CURRENT_COURSE.moduleCounts[moduleNumber - 1] ||
      lesson.url !== "/course/m" + moduleNumber + "/" + pageNumber + "/") {
    throw new Error("Noncanonical course URL");
  }
  return COURSE_SITE_ORIGIN + lesson.url;
}

/**
 * Resume based on an already validated manifest and authenticated progress.
 *
 * The account API has no curriculum generation marker yet; clearing old
 * private TEST progress before deploying the new worker is mandatory.
 * A reused ID can describe different content after PR #191 and cannot be
 * distinguished by validating the ID alone.
 */
export function chooseNextLesson(ordered, progress) {
  if (!Array.isArray(ordered) || !ordered.length ||
      !progress || typeof progress !== "object" ||
      !progress.lessons || typeof progress.lessons !== "object") {
    throw new Error("Invalid lesson progress");
  }
  const index = ordered.findIndex(item => item.id === progress.lastLesson);
  const completed = item => progress.lessons[item.id]?.completed === true;
  if (index >= 0 && !completed(ordered[index])) return ordered[index];
  for (let offset = 1; offset <= ordered.length; offset += 1) {
    const next = ordered[(Math.max(index, -1) + offset) % ordered.length];
    if (!completed(next)) return next;
  }
  return null; // All 57 current lessons completed.
}
