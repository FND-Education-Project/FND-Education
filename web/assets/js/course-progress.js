/*
 * FND Education Project — device-local learner progress (version 1).
 *
 * Only public course lesson IDs, completion/visit flags and the last lesson
 * are stored. This file does not send learner history to analytics, a server,
 * an external identity provider, or another browser/device.
 *
 * Curriculum labels/links come from the generated manifest. We build all
 * markup using DOM methods and textContent, never untrusted innerHTML.
 * Core navigation and course content remain available without JavaScript.
 */
(function () {
  "use strict";

  const STORAGE_KEY = "fnd-course-progress-v1";
  const script = document.currentScript;
  const manifestUrl = script && script.dataset.manifestUrl;

  if (!manifestUrl) return;

  // Normalized, same-origin paths are the only link identifiers we accept.
  function normalizedPath(value) {
    try {
      const url = new URL(value, window.location.href);
      if (url.origin !== window.location.origin) return null;
      return url.pathname.replace(/\/index\.html$/i, "/").replace(/\/+$/, "/");
    } catch {
      return null;
    }
  }

  function element(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function emptyState() {
    return { version: 1, lessons: {}, lastLesson: null };
  }

  document.addEventListener("DOMContentLoaded", async function () {
    let manifest;
    try {
      const response = await fetch(manifestUrl, {
        credentials: "same-origin",
        cache: "no-store"
      });
      if (!response.ok) throw new Error("Course index unavailable");
      manifest = await response.json();
      if (manifest.version !== 1 || !Array.isArray(manifest.parts)) {
        throw new Error("Unsupported course index");
      }
    } catch {
      // Continue to offer the original published course index and navigation.
      return;
    }

    const lookup = new Map();
    const orderedLessons = [];

    // Reject malformed or duplicate content instead of building broken links.
    try {
      for (const part of manifest.parts) {
        if (!Array.isArray(part.modules) || typeof part.title !== "string") {
          throw new Error("Invalid course part");
        }
        for (const module of part.modules) {
          if (!Array.isArray(module.lessons) || !Number.isInteger(module.number)) {
            throw new Error("Invalid course module");
          }
          for (const lesson of module.lessons) {
            if (!/^m[0-9]+-[0-9]+$/.test(lesson.id) ||
                typeof lesson.title !== "string" ||
                !/^\/course\/m[0-9]+\/[0-9]+\/$/.test(lesson.url) ||
                lookup.has(lesson.url) || orderedLessons.some((item) => item.id === lesson.id)) {
              throw new Error("Invalid course lesson");
            }
            lookup.set(lesson.url, lesson);
            orderedLessons.push(lesson);
          }
        }
      }
      if (orderedLessons.length === 0) throw new Error("Empty course");
    } catch {
      return;
    }

    const knownIds = new Set(orderedLessons.map((lesson) => lesson.id));
    let storageAvailable = true;

    // Validate stored data without trusting it as a source of page URLs,
    // identity, or permissions. This also tolerates future lesson additions.
    function sanitize(source) {
      const clean = emptyState();
      if (!source || source.version !== 1 ||
          !source.lessons || typeof source.lessons !== "object" ||
          Array.isArray(source.lessons)) return clean;

      for (const id of knownIds) {
        const item = source.lessons[id];
        if (!item || typeof item !== "object") continue;
        if (item.visited === true || item.completed === true) {
          clean.lessons[id] = {
            visited: item.visited === true,
            completed: item.completed === true
          };
        }
      }
      if (knownIds.has(source.lastLesson)) clean.lastLesson = source.lastLesson;
      return clean;
    }

    function readState() {
      try {
        const raw = window.localStorage.getItem(STORAGE_KEY);
        return raw ? sanitize(JSON.parse(raw)) : emptyState();
      } catch {
        storageAvailable = false;
        return emptyState();
      }
    }

    let state = readState();

    function save() {
      try {
        window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
        storageAvailable = true;
      } catch {
        storageAvailable = false;
      }
    }

    function get(id) {
      return state.lessons[id] || { visited: false, completed: false };
    }

    function describe(id) {
      const item = get(id);
      return item.completed ? "Completed" : item.visited ? "Visited" : "Not started";
    }

    function completedCount(items) {
      return items.filter((item) => get(item.id).completed).length;
    }

    function visitedCount() {
      return orderedLessons.filter((item) => get(item.id).visited).length;
    }

    // Completion is always a manual decision. Visiting a page NEVER writes
    // completed:true or overwrites an existing manual completion choice.
    function setComplete(id, checked) {
      if (!knownIds.has(id)) return;
      const old = get(id);
      state.lessons[id] = { visited: old.visited, completed: checked };
      save();
      update();
    }

    function nextLesson() {
      const lastIndex = orderedLessons.findIndex((item) => item.id === state.lastLesson);
      if (lastIndex >= 0 && !get(state.lastLesson).completed) {
        return orderedLessons[lastIndex];
      }
      for (let offset = 1; offset <= orderedLessons.length; offset += 1) {
        const index = (Math.max(lastIndex, -1) + offset) % orderedLessons.length;
        const candidate = orderedLessons[index];
        if (!get(candidate.id).completed) return candidate;
      }
      return null;
    }

    // Record the fact of opening a real lesson, even if the reader stops
    // halfway. We deliberately do not record scroll positions or time spent.
    const current = lookup.get(normalizedPath(window.location.pathname));
    if (current) {
      const old = get(current.id);
      state.lessons[current.id] = {
        visited: true,
        completed: old.completed
      };
      state.lastLesson = current.id;
      save();
    }

    const overview = document.getElementById("course-progress");
    const lessonControls = document.getElementById("lesson-progress-controls");
    const resume = document.getElementById("home-learning-resume");

    function statusBadge(id) {
      const status = describe(id);
      const badge = element("span", "course-progress-state", "");
      badge.classList.add(
        status === "Completed" ? "is-complete" :
        status === "Visited" ? "is-visited" : "is-new"
      );
      const icon = element("span", "course-progress-state-icon",
        status === "Completed" ? "✓" : status === "Visited" ? "◉" : "○");
      icon.setAttribute("aria-hidden", "true");
      badge.append(icon, document.createTextNode(" " + status));
      return badge;
    }

    function checkboxFor(lesson, extraClass) {
      const label = element("label", extraClass || "course-progress-checkbox");
      const check = document.createElement("input");
      check.type = "checkbox";
      check.checked = get(lesson.id).completed;
      check.setAttribute("aria-label", "Mark complete: " + lesson.title);
      check.dataset.progressCheckbox = lesson.id;
      check.addEventListener("change", function () {
        setComplete(lesson.id, check.checked);
        const replacement = document.querySelector(
          '[data-progress-checkbox="' + lesson.id + '"]'
        );
        if (replacement) replacement.focus();
      });
      label.append(check, element("span", "", "Complete"));
      return label;
    }

    function makeDetails(key, summaryText, countText, openKeys) {
      const details = element("details", "course-progress-details");
      details.dataset.progressGroup = key;
      details.open = openKeys.has(key);
      const summary = element("summary", "course-progress-summary");
      summary.append(
        element("span", "course-progress-summary-title", summaryText),
        element("span", "course-progress-count", countText)
      );
      details.append(summary);
      return details;
    }

    function renderOverview() {
      if (!overview) return;
      const opened = new Set(
        Array.from(overview.querySelectorAll("details[open]"))
          .map((item) => item.dataset.progressGroup)
      );
      const hadRendered = overview.dataset.rendered === "true";
      if (!hadRendered) {
        opened.add("part-1");
        opened.add("module-1");
      }

      const fragment = document.createDocumentFragment();
      const heading = element("h2", "", "My Learning Progress");
      const count = completedCount(orderedLessons);
      const summary = element(
        "p", "course-progress-summary-line",
        count + " of " + orderedLessons.length + " lessons completed · " +
        visitedCount() + " visited"
      );
      const bar = element("progress", "course-progress-bar");
      bar.max = orderedLessons.length;
      bar.value = count;
      bar.setAttribute("aria-label", "Course lessons completed");
      fragment.append(heading, summary, bar);

      const explanation = element(
        "p", "course-progress-help",
        "Opening a lesson marks it as visited. Tick Complete when you feel " +
        "finished, or untick it at any time. Module introductions and " +
        "crosswords are optional and do not affect your progress."
      );
      fragment.append(explanation);

      const next = nextLesson();
      if (next) {
        const resumeLink = element("a", "course-progress-resume",
          state.lastLesson ? "Continue learning →" : "Start with Lesson 1 →");
        resumeLink.href = next.url;
        fragment.append(resumeLink);
      } else {
        fragment.append(element("p", "course-progress-help",
          "All lessons are marked complete. You can revisit or untick any lesson."));
      }

      for (const part of manifest.parts) {
        const partLessons = part.modules.flatMap((mod) => mod.lessons);
        const partDetails = makeDetails(
          "part-" + part.number,
          "Part " + part.number + ": " + part.title,
          completedCount(partLessons) + "/" + partLessons.length,
          opened
        );
        for (const mod of part.modules) {
          const details = makeDetails(
            "module-" + mod.number,
            "Module " + mod.number + ": " + mod.title,
            completedCount(mod.lessons) + "/" + mod.lessons.length,
            opened
          );

          // The module introduction remains accessible but is not counted
          // as a lesson. No private data is present in any course link.
          const intro = element("a", "course-progress-intro",
            "Module overview");
          intro.href = mod.url;
          details.append(intro);

          const list = element("ul", "course-progress-lessons");
          for (const lesson of mod.lessons) {
            const row = element("li", "course-progress-lesson");
            const link = element("a", "course-progress-lesson-link", lesson.title);
            link.href = lesson.url;
            const main = element("div", "course-progress-lesson-main");
            main.append(link, statusBadge(lesson.id));
            row.append(main, checkboxFor(lesson));
            list.append(row);
          }
          details.append(list);
          partDetails.append(details);
        }
        fragment.append(partDetails);
      }

      const privacy = element(
        "p", "course-progress-help",
        "Saved only in this browser on this device, not to an account. " +
        "Clearing browser data or using private browsing may erase progress. " +
        "Cross-device sign-in is not available yet."
      );
      const clear = element("button", "course-progress-clear", "Clear my progress");
      clear.type = "button";
      clear.addEventListener("click", function () {
        if (!window.confirm("Clear all saved course progress on this device?")) return;
        state = emptyState();
        save();
        update();
      });
      fragment.append(privacy, clear);

      if (!storageAvailable) {
        fragment.append(element("p", "course-progress-warning",
          "Browser storage is blocked. Changes will last only while this page is open."));
      }

      overview.replaceChildren(fragment);
      overview.hidden = false;
      overview.dataset.rendered = "true";

      // Hide ONLY the six duplicate curriculum lists after the interactive
      // overview is successfully built. Keep the About section and all
      // original content available when scripting is disabled or fails.
      const content = document.querySelector(".course-content");
      if (content && !content.dataset.progressFallbackHidden) {
        let isSyllabus = false;
        for (const child of Array.from(content.children)) {
          if (child.matches("h2") && /^Part One:/.test(child.textContent.trim())) {
            isSyllabus = true;
          } else if (child.matches("h2") &&
                     /^About This Course/.test(child.textContent.trim())) {
            isSyllabus = false;
          }
          if (isSyllabus) child.hidden = true;
        }
        content.dataset.progressFallbackHidden = "true";
      }
    }

    function renderLessonControls() {
      if (!lessonControls || !current) return;
      const fragment = document.createDocumentFragment();
      fragment.append(element("h2", "", "Your lesson progress"));
      fragment.append(element("p", "course-progress-help",
        "Visiting this lesson does not mean you have finished it. " +
        "You can change your choice at any time."));
      fragment.append(checkboxFor(current, "course-progress-lesson-toggle"));
      fragment.append(statusBadge(current.id));

      const nextLink = document.querySelector(".course-page > .page-navigation .page-navigation-next a");
      if (nextLink) {
        const path = normalizedPath(nextLink.href);
        if (path && path.startsWith("/course/")) {
          const button = element("button", "course-progress-resume",
            "Mark complete & continue →");
          button.type = "button";
          button.addEventListener("click", function () {
            setComplete(current.id, true);
            window.location.assign(nextLink.href);
          });
          fragment.append(button);
        }
      }
      if (!storageAvailable) {
        fragment.append(element("p", "course-progress-warning",
          "Browser storage is blocked. Your progress may not be saved."));
      }
      lessonControls.replaceChildren(fragment);
      lessonControls.hidden = false;
    }

    // Only course-navigation links carry progress markers; editorial inline
    // links and research citations remain visually uncluttered.
    function updateNavigationMarks() {
      const links = Array.from(document.querySelectorAll(
        ".page-navigation a, .course-entry-actions a"
      ));
      if (document.body.querySelector(".page-context") &&
          document.querySelector(".course-content h2")) {
        const heading = Array.from(document.querySelectorAll(
          ".course-content h2"
        )).find((node) => node.textContent.trim() === "Pages");
        const list = heading && heading.nextElementSibling;
        if (list && list.matches("ul")) {
          links.push(...list.querySelectorAll("li > a, li > strong > a"));
        }
      }
      for (const link of new Set(links)) {
        const lesson = lookup.get(normalizedPath(link.href));
        const previous = link.querySelector(".course-navigation-progress");
        if (previous) previous.remove();
        if (!lesson) continue;
        const mark = element("span", "course-navigation-progress", "");
        mark.append(statusBadge(lesson.id));
        link.append(mark);
      }
    }

    function renderResume() {
      if (!resume) return;
      const next = nextLesson();
      const anyVisited = visitedCount() > 0;
      resume.hidden = !next || !anyVisited;
      if (!next || !anyVisited) return;
      const link = resume.querySelector("a");
      if (link) link.href = next.url;
      const label = document.getElementById("home-learning-resume-label");
      if (label) label.textContent = next.title;
    }

    function update() {
      renderOverview();
      renderLessonControls();
      renderResume();
      updateNavigationMarks();
    }

    // Respect changes made in another tab on the same browser.
    window.addEventListener("storage", function (event) {
      if (event.key !== STORAGE_KEY) return;
      state = readState();
      update();
    });

    update();
  });
})();
