/*
 * Account-scoped FND course progress interface.
 *
 * No localStorage, IndexedDB or browser profile stores lesson progress.
 * The API resolves each learner from an authenticated HttpOnly session.
 * Every completion/uncompletion uses a fresh confirmation dialog showing
 * the signed-in username prominently; automatic visits do not complete.
 *
 * Without a configured or available account API, original static lesson
 * content and course navigation continue to work without modification.
 */
(function () {
  "use strict";
  const script = document.currentScript;
  const manifestUrl = script && script.dataset.manifestUrl;
  if (!manifestUrl) return;

  function el(tag, className, text) {
    const result = document.createElement(tag);
    if (className) result.className = className;
    if (text !== undefined) result.textContent = text;
    return result;
  }
  function pathOf(url) {
    try {
      const result = new URL(url, location.href);
      if (result.origin !== location.origin) return null;
      return result.pathname.replace(/\/index\.html$/i, "/").replace(/\/+$/, "/");
    } catch { return null; }
  }
  function statusText(item) {
    return item.completed ? "Completed" : item.visited ? "Visited" : "Not started";
  }
  function displayStatus(item) {
    const badge = el("span", "course-progress-state");
    const status = statusText(item);
    badge.classList.add(
      item.completed ? "is-complete" :
      item.visited ? "is-visited" : "is-new"
    );
    const symbol = el("span", "course-progress-state-icon",
      item.completed ? "✓" : item.visited ? "◉" : "○");
    symbol.setAttribute("aria-hidden", "true");
    badge.append(symbol, document.createTextNode(" " + status));
    return badge;
  }

  document.addEventListener("DOMContentLoaded", async function () {
    if (!window.FNDAccount) return; // No public sign-in deployment yet.
    const account = await window.FNDAccount.ready;
    const overview = document.getElementById("course-progress");
    const controls = document.getElementById("lesson-progress-controls");
    const homeResume = document.getElementById("home-learning-resume");
    if (!account) {
      if (overview) {
        overview.replaceChildren(
          el("h2", "", "My Learning Progress"),
          el("p", "course-progress-help",
            "Your course is free to read. Sign in above if you would " +
            "like to save personal lesson progress across devices.")
        );
        overview.hidden = false;
      }
      return;
    }

    let manifest;
    try {
      const response = await fetch(manifestUrl, { cache: "no-store" });
      if (!response.ok) throw new Error("Manifest unavailable");
      manifest = await response.json();
      if (![1, 2].includes(manifest.version) || !Array.isArray(manifest.parts)) {
        throw new Error("Unknown curriculum");
      }
      if (manifest.version === 2 && !Array.isArray(manifest.earlierModules)) {
        throw new Error("Missing earlier-edition history");
      }
    } catch { return; }
    const lookup = new Map(); // Exact route -> lesson; NEVER display module number -> ID.
    const identity = new Map(); // Original immutable account ID -> original route.
    const ordered = []; // Current reading sequence, including untracked new lessons.
    const earlier = []; // Original edition stays visible and retains its progress.
    function register(lesson, destination) {
      if (!lesson || typeof lesson.url !== "string" || lookup.has(lesson.url)) return false;
      const tracked = manifest.version === 1 || lesson.progressEligible === true;
      if (tracked) {
        if (typeof lesson.id !== "string" ||
            !/^m([1-9]|1[0-9]|2[0-3])-[1-9][0-9]*$/.test(lesson.id)) return false;
        const match = /^m([1-9][0-9]*)-([1-9][0-9]*)$/.exec(lesson.id);
        if (lesson.url !== "/course/m" + match[1] + "/" + match[2] + "/" ||
            identity.has(lesson.id)) return false;
      } else if (manifest.version !== 2 || lesson.progressEligible !== false ||
                 lesson.id !== null ||
                 !/^\/course\/v2\/m(?:6|7|8|9|10)\/[1-9][0-9]*\/$/.test(lesson.url)) {
        return false;
      }
      const entry = { ...lesson, progressEligible: tracked };
      lookup.set(lesson.url, entry);
      if (tracked) identity.set(lesson.id, entry);
      destination.push(entry);
      return true;
    }
    for (const part of manifest.parts) {
      if (!Array.isArray(part.modules)) return;
      for (const mod of part.modules) {
        if (!Array.isArray(mod.lessons)) return;
        for (const lesson of mod.lessons) {
          if (!register(lesson, ordered)) return;
        }
      }
    }
    if (manifest.version === 2) {
      for (const mod of manifest.earlierModules) {
        if (!Array.isArray(mod.lessons)) return;
        for (const lesson of mod.lessons) {
          if (!register(lesson, earlier)) return;
        }
      }
      if (identity.size !== manifest.eligibleLessonCount) return;
    }
    if (!ordered.length) return;
    const known = new Set(identity.keys());
    const eligible = [...ordered, ...earlier].filter(item => item.progressEligible);
    let state;
    try {
      state = await window.FNDAccount.apiRequest("/v1/progress");
    } catch { return; }
    if (!state || !state.lessons) return;

    // Server values are constrained to the published lesson identifiers
    // before they are used to render statuses or link destinations.
    function get(id) {
      const item = known.has(id) && state.lessons[id];
      return {
        visited: !!(item && item.visited === true),
        completed: !!(item && item.completed === true)
      };
    }
    function count(lessons) {
      return lessons.filter(lesson => get(lesson.id).completed).length;
    }
    function nextLesson() {
      // Never reinterpret a saved original m6-1 (seizures) as new Module 6
      // attention. If the saved position is earlier-edition, resume THERE.
      const archivedResume = identity.get(state.lastLesson);
      if (archivedResume && earlier.includes(archivedResume)) return archivedResume;
      const position = ordered.findIndex(item =>
        item.progressEligible && item.id === state.lastLesson);
      if (position >= 0 && !get(state.lastLesson).completed) {
        return ordered[position];
      }
      for (let n = 1; n <= ordered.length; n++) {
        const candidate = ordered[(Math.max(position, -1) + n) % ordered.length];
        if (!candidate.progressEligible || !get(candidate.id).completed) return candidate;
      }
      return null;
    }

    const current = lookup.get(pathOf(location.pathname));
    if (current && current.progressEligible) {
      try {
        await window.FNDAccount.apiRequest("/v1/progress/visit", "POST", {
          lessonId: current.id
        });
        state.lessons[current.id] = { ...get(current.id), visited: true };
        state.lastLesson = current.id;
      } catch {
        // Never claim server persistence when it failed.
      }
    }

    let feedbackTarget = null;
    function alertFeedback(message) {
      if (feedbackTarget) feedbackTarget.textContent = message;
    }

    // An explicit confirmation is required EVERY time, for checking and
    // unchecking alike, including the combined Complete & Continue action.
    // No "remember my choice" preference or silent completion route exists.
    function confirmation(lesson, completing, resetAll = false) {
      return new Promise(resolve => {
        const dlg = el("dialog", "course-progress-confirmation");
        if (typeof dlg.showModal !== "function") {
          resolve(false); return;
        }
        const title = el("h2", "", "Confirm lesson progress");
        const prompt = el("p", "",
          (resetAll ? "Clear ALL lesson progress for:" :
            completing ? "Mark this lesson completed for:" :
            "Remove the completion checkmark for:"));
        const username = el("strong", "course-confirm-username", account.username);
        const lessonName = el("p", "course-confirm-lesson", lesson.title);
        const note = el("p", "course-progress-help",
          "Please check that this is your account, especially when " +
          "sharing a device with another learner.");
        const buttons = el("div", "course-confirm-actions");
        const cancel = el("button", "", "Cancel");
        cancel.type = "button";
        const confirm = el("button", "course-progress-resume",
          resetAll ? "Yes, clear all progress" :
          completing ? "Yes, mark completed" : "Yes, remove checkmark");
        confirm.type = "button";
        let accepted = false;
        cancel.addEventListener("click", () => dlg.close());
        confirm.addEventListener("click", () => {
          accepted = true;
          dlg.close();
        });
        dlg.addEventListener("close", () => {
          dlg.remove();
          resolve(accepted);
        }, { once: true });
        buttons.append(cancel, confirm);
        dlg.append(title, prompt, username, lessonName, note, buttons);
        document.body.append(dlg);
        dlg.showModal();
        cancel.focus();
      });
    }
    let mutationPending = false;
    async function setCompletion(lesson, checked, destination) {
      if (mutationPending || !lesson.progressEligible || !known.has(lesson.id)) return;
      mutationPending = true;
      try {
        if (!(await confirmation(lesson, checked))) return;
        await window.FNDAccount.apiRequest(
          "/v1/progress/completion", "POST", {
            lessonId: lesson.id,
            completed: checked,
            confirmed: true,
            confirmedUsername: account.username
          }
        );
        state.lessons[lesson.id] = { ...get(lesson.id), completed: checked };
        if (destination) {
          window.location.assign(destination); return;
        }
        render();
        const focused = document.querySelector(
          'input[data-progress-lesson="' + lesson.id + '"]'
        );
        if (focused) focused.focus();
      } catch (error) {
        alertFeedback(error.message || "Progress was not saved. Try again.");
      } finally { mutationPending = false; }
    }

    function checkbox(lesson) {
      if (!lesson.progressEligible || !known.has(lesson.id)) {
        return el("span", "course-progress-help", "Completion tracking not yet available");
      }
      const label = el("label", "course-progress-checkbox");
      const input = el("input");
      input.type = "checkbox";
      input.dataset.progressLesson = lesson.id;
      input.checked = get(lesson.id).completed;
      input.setAttribute("aria-label", "Change completion for " + lesson.title);
      input.addEventListener("change", function () {
        // Keep the old value until the identity dialog and API both succeed.
        input.checked = get(lesson.id).completed;
        setCompletion(lesson, !get(lesson.id).completed);
      });
      label.append(input, el("span", "", "Complete"));
      return label;
    }

    function group(key, title, total, openKeys) {
      const item = el("details", "course-progress-details");
      item.dataset.progressGroup = key;
      item.open = openKeys.has(key);
      const summary = el("summary", "course-progress-summary");
      summary.append(
        el("span", "course-progress-summary-title", title),
        el("span", "course-progress-count", total)
      );
      item.append(summary);
      return item;
    }

    function renderOverview() {
      if (!overview) return;
      const opened = new Set(Array.from(overview.querySelectorAll(
        "details[open]"
      )).map(item => item.dataset.progressGroup));
      if (!overview.dataset.rendered) {
        opened.add("part-1");
        opened.add("module-1");
      }
      const fragment = document.createDocumentFragment();
      fragment.append(el("h2", "", "My Learning Progress"));
      const total = count(eligible);
      const visited = eligible.filter(item => get(item.id).visited).length;
      fragment.append(el("p", "course-progress-summary-line",
        total + " of " + eligible.length + " progress-enabled lessons completed · " +
        visited + " visited"));
      const bar = el("progress", "course-progress-bar");
      bar.max = eligible.length;
      bar.value = total;
      bar.setAttribute("aria-label", "Course lessons completed");
      fragment.append(bar);
      fragment.append(el("p", "course-progress-help",
        "Opening a progress-enabled lesson marks it visited. Completion always " +
        "requires confirmation of your active username. You can undo a checkmark."));
      if (manifest.version === 2) {
        const untracked = ordered.filter(item => !item.progressEligible).length;
        if (untracked) fragment.append(el("p", "course-progress-help",
          "The " + untracked + " new concepts-first lessons are readable now, " +
          "but their cloud completion tracking is not yet enabled. " +
          "Earlier-edition completion history is preserved below."));
      }
      const next = nextLesson();
      if (next) {
        const link = el("a", "course-progress-resume", "Continue learning →");
        link.href = next.url;
        fragment.append(link);
      }

      for (const part of manifest.parts) {
        const lessons = part.modules.flatMap(m => m.lessons);
        const partGroup = group("part-" + part.number,
          "Part " + part.number + ": " + part.title,
          count(lessons) + "/" + lessons.filter(item => item.progressEligible).length +
          " tracked", opened);
        for (const mod of part.modules) {
          const moduleGroup = group("module-" + (mod.sourceModule || mod.number),
            "Module " + mod.number + ": " + mod.title,
            count(mod.lessons) + "/" +
            mod.lessons.filter(item => item.progressEligible).length + " tracked", opened);
          const intro = el("a", "course-progress-intro", "Module overview");
          intro.href = mod.url;
          moduleGroup.append(intro);
          const ul = el("ul", "course-progress-lessons");
          for (const lesson of mod.lessons) {
            const row = el("li", "course-progress-lesson");
            const main = el("div", "course-progress-lesson-main");
            const link = el("a", "course-progress-lesson-link", lesson.title);
            link.href = lesson.url;
            if (lesson.progressEligible) {
              main.append(link, displayStatus(get(lesson.id)));
              row.append(main, checkbox(lesson));
            } else {
              main.append(link, el("span", "course-progress-help",
                "Read now · completion tracking not yet available"));
              row.append(main);
            }
            ul.append(row);
          }
          moduleGroup.append(ul);
          partGroup.append(moduleGroup);
        }
        fragment.append(partGroup);
      }
      if (earlier.length) {
        const previous = group("earlier", "Earlier-edition reading",
          count(earlier) + "/" + earlier.length + " tracked", opened);
        previous.append(el("p", "course-progress-help",
          "Your original lesson checkmarks remain linked to their original topics. " +
          "These lessons are outside the current reading sequence."));
        for (const mod of manifest.earlierModules) {
          const section = group("earlier-module-" + mod.sourceModule,
            "Earlier Module " + mod.number + ": " + mod.title,
            count(mod.lessons) + "/" + mod.lessons.length, opened);
          const intro = el("a", "course-progress-intro", "Earlier module overview");
          intro.href = mod.url;
          section.append(intro);
          const ul = el("ul", "course-progress-lessons");
          for (const original of mod.lessons) {
            const lesson = identity.get(original.id);
            if (!lesson) continue;
            const row = el("li", "course-progress-lesson");
            const main = el("div", "course-progress-lesson-main");
            const link = el("a", "course-progress-lesson-link", lesson.title);
            link.href = lesson.url;
            main.append(link, displayStatus(get(lesson.id)));
            row.append(main, checkbox(lesson));
            ul.append(row);
          }
          section.append(ul);
          previous.append(section);
        }
        fragment.append(previous);
      }
      fragment.append(el("p", "course-progress-help",
        "Progress and preferences belong only to the account shown above, " +
        "not everyone who uses this browser. Reading is always free without signing in."));

      const reset = el("button", "course-progress-clear", "Clear my course progress");
      reset.type = "button";
      reset.addEventListener("click", async () => {
        if (mutationPending) return;
        mutationPending = true;
        try {
          const confirmed = await confirmation({
            title: "All course lessons"
          }, false, true);
          if (!confirmed) return;
          await window.FNDAccount.apiRequest("/v1/progress/reset", "POST", {
            confirmed: true, confirmedUsername: account.username
          });
          state = { lessons: {}, lastLesson: null };
          render();
        } catch (error) {
          alertFeedback(error.message || "Could not clear progress.");
        } finally { mutationPending = false; }
      });
      fragment.append(reset);

      const feedback = el("p", "course-progress-warning");
      feedback.setAttribute("role", "status");
      fragment.append(feedback);
      overview.replaceChildren(fragment);
      feedbackTarget = feedback;
      overview.hidden = false;
      overview.dataset.rendered = "true";

      // Only hide duplicate canonical syllabus lists after the active
      // account's full course view has been assembled successfully.
      const source = document.querySelector(".course-content");
      if (manifest.version === 1 && source && !source.dataset.progressFallbackHidden) {
        let inSyllabus = false;
        for (const child of Array.from(source.children)) {
          if (child.matches("h2") && /^Part One:/.test(child.textContent.trim())) {
            inSyllabus = true;
          } else if (child.matches("h2") &&
                     /^About This Course/.test(child.textContent.trim())) {
            inSyllabus = false;
          }
          if (inSyllabus) child.hidden = true;
        }
        source.dataset.progressFallbackHidden = "true";
      }
    }

    function renderLessonControls() {
      if (!controls || !current) return;
      const fragment = document.createDocumentFragment();
      if (!current.progressEligible) {
        fragment.append(el("h2", "", "Your lesson progress"));
        fragment.append(el("p", "course-progress-help",
          "This new course lesson is available to read, but saved " +
          "completion and visit tracking have not yet been enabled. " +
          "Earlier-edition lesson history is unaffected."));
        controls.replaceChildren(fragment);
        controls.hidden = false;
        return;
      }
      fragment.append(el("h2", "", "Your lesson progress"));
      fragment.append(el("p", "course-progress-help",
        "The account shown at the top must be yours. " +
        "Completion requires confirmation every time."));
      fragment.append(checkbox(current), displayStatus(get(current.id)));
      const next = document.querySelector(
        ".course-page > .page-navigation .page-navigation-next a"
      );
      if (next && pathOf(next.href)?.startsWith("/course/")) {
        const advance = el("button", "course-progress-resume",
          "Mark completed & continue →");
        advance.type = "button";
        advance.addEventListener("click", () =>
          setCompletion(current, true, next.href));
        fragment.append(advance);
      }
      const note = el("p", "course-progress-warning");
      note.setAttribute("role", "status");
      fragment.append(note);
      controls.replaceChildren(fragment);
      feedbackTarget = note;
      controls.hidden = false;
    }

    function navMarkers() {
      const links = Array.from(document.querySelectorAll(
        ".page-navigation a, .course-entry-actions a"
      ));
      const heading = Array.from(document.querySelectorAll(
        ".course-content h2"
      )).find(h => h.textContent.trim() === "Pages");
      const list = heading && heading.nextElementSibling;
      if (list && list.matches("ul")) {
        links.push(...list.querySelectorAll("li > a, li > strong > a"));
      }
      for (const link of new Set(links)) {
        const lesson = lookup.get(pathOf(link.href));
        const old = link.querySelector(".course-navigation-progress");
        if (old) old.remove();
        if (!lesson || !lesson.progressEligible) continue;
        const span = el("span", "course-navigation-progress");
        span.append(displayStatus(get(lesson.id)));
        link.append(span);
      }
    }

    function renderHomeResume() {
      if (!homeResume) return;
      const lesson = nextLesson();
      const hasHistory = eligible.some(item => get(item.id).visited);
      homeResume.hidden = !(lesson && hasHistory);
      if (!lesson || !hasHistory) return;
      const link = homeResume.querySelector("a");
      if (link) link.href = lesson.url;
      const title = document.getElementById("home-learning-resume-label");
      if (title) title.textContent = lesson.title;
    }

    function render() {
      renderOverview();
      renderLessonControls();
      navMarkers();
      renderHomeResume();
    }
    render();
  });
})();
