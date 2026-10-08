/*
 * FND Education Project
 *
 * Small site-wide behaviours.
 *
 * Keep JavaScript optional wherever possible:
 * the educational content and navigation should still work
 * when JavaScript is unavailable.
 */


document.addEventListener("DOMContentLoaded", () => {

  /*
   * Keep site-wide search terms out of the HTTP request URL when JavaScript
   * is available. URL fragments are handled only by the browser and are not
   * sent to the web server. The normal GET form remains a no-JavaScript
   * fallback so search navigation still works without scripting.
   */
  for (const form of document.querySelectorAll(".site-search-form")) {
    form.addEventListener("submit", (event) => {
      const input = form.querySelector('input[name="q"]');
      const query = input ? input.value.trim() : "";

      if (!query) {
        return;
      }

      event.preventDefault();

      const target = new URL(
        form.getAttribute("action") || "/search/",
        window.location.href
      );

      target.search = "";
      target.hash = "q=" + encodeURIComponent(query);
      window.location.assign(target.toString());
    });
  }

  /*
   * Glossary-only autocomplete. The list of valid terms comes directly from
   * the rendered glossary H3 headings, so there is no second term index to
   * maintain in JavaScript.
   */
  const glossaryForm =
    document.getElementById("glossary-search-form");
  const glossaryInput =
    document.getElementById("glossary-search-input");
  const glossaryResults =
    document.getElementById("glossary-search-results");

  if (glossaryForm && glossaryInput && glossaryResults) {
    const glossaryTerms = Array.from(
      document.querySelectorAll(".course-content h3[id]")
    ).map((heading) => ({
      label: heading.textContent.trim(),
      id: heading.id,
      heading
    }));

    let currentMatches = [];
    let activeIndex = -1;

    const normalizeGlossaryText = (value) =>
      value
        .toLocaleLowerCase()
        .normalize("NFKD")
        .replace(/[’']/g, "")
        .replace(/[^a-z0-9]+/g, " ")
        .trim();

    function hideGlossaryResults() {
      glossaryResults.hidden = true;
      glossaryResults.replaceChildren();
      glossaryInput.setAttribute("aria-expanded", "false");
      glossaryInput.setAttribute("aria-activedescendant", "");
      currentMatches = [];
      activeIndex = -1;
    }

    function openGlossaryTerm(term) {
      if (!term) {
        return;
      }

      glossaryInput.value = term.label;
      hideGlossaryResults();

      const hash = "#" + encodeURIComponent(term.id);
      if (window.location.hash !== hash) {
        history.pushState(null, "", hash);
      }

      term.heading.setAttribute("tabindex", "-1");
      term.heading.scrollIntoView({
        behavior: window.matchMedia(
          "(prefers-reduced-motion: reduce)"
        ).matches ? "auto" : "smooth",
        block: "start"
      });
      term.heading.focus({ preventScroll: true });
    }

    function setActiveGlossaryResult(index) {
      const buttons = Array.from(
        glossaryResults.querySelectorAll("[role='option']")
      );

      if (!buttons.length) {
        activeIndex = -1;
        glossaryInput.setAttribute("aria-activedescendant", "");
        return;
      }

      activeIndex = Math.max(0, Math.min(index, buttons.length - 1));

      buttons.forEach((button, buttonIndex) => {
        const active = buttonIndex === activeIndex;
        button.setAttribute("aria-selected", String(active));
        button.classList.toggle("is-active", active);
      });

      glossaryInput.setAttribute(
        "aria-activedescendant",
        buttons[activeIndex].id
      );
      buttons[activeIndex].scrollIntoView({ block: "nearest" });
    }

    function updateGlossaryResults() {
      const query = normalizeGlossaryText(glossaryInput.value);

      if (!query) {
        hideGlossaryResults();
        return;
      }

      const startsWith = [];
      const contains = [];

      for (const term of glossaryTerms) {
        const normalized = normalizeGlossaryText(term.label);
        if (normalized.startsWith(query)) {
          startsWith.push(term);
        } else if (normalized.includes(query)) {
          contains.push(term);
        }
      }

      currentMatches = startsWith.concat(contains).slice(0, 10);
      glossaryResults.replaceChildren();
      activeIndex = -1;

      if (!currentMatches.length) {
        const item = document.createElement("li");
        item.className = "glossary-search-empty";
        item.textContent = "No glossary terms match that text.";
        glossaryResults.append(item);
        glossaryResults.hidden = false;
        glossaryInput.setAttribute("aria-expanded", "true");
        return;
      }

      currentMatches.forEach((term, index) => {
        const item = document.createElement("li");
        const button = document.createElement("button");

        button.type = "button";
        button.id = "glossary-result-" + index;
        button.setAttribute("role", "option");
        button.setAttribute("aria-selected", "false");
        button.textContent = term.label;
        button.addEventListener("click", () => openGlossaryTerm(term));

        item.append(button);
        glossaryResults.append(item);
      });

      glossaryResults.hidden = false;
      glossaryInput.setAttribute("aria-expanded", "true");
    }

    glossaryInput.addEventListener("input", updateGlossaryResults);

    glossaryInput.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        hideGlossaryResults();
        return;
      }

      if (!currentMatches.length) {
        return;
      }

      if (event.key === "ArrowDown") {
        event.preventDefault();
        setActiveGlossaryResult(
          activeIndex < currentMatches.length - 1
            ? activeIndex + 1
            : 0
        );
        return;
      }

      if (event.key === "ArrowUp") {
        event.preventDefault();
        setActiveGlossaryResult(
          activeIndex > 0
            ? activeIndex - 1
            : currentMatches.length - 1
        );
        return;
      }

      if (event.key === "Enter") {
        event.preventDefault();
        openGlossaryTerm(
          currentMatches[activeIndex >= 0 ? activeIndex : 0]
        );
      }
    });

    glossaryForm.addEventListener("submit", (event) => {
      event.preventDefault();
      if (currentMatches.length) {
        openGlossaryTerm(
          currentMatches[activeIndex >= 0 ? activeIndex : 0]
        );
      }
    });

    document.addEventListener("click", (event) => {
      if (!glossaryForm.contains(event.target)) {
        hideGlossaryResults();
      }
    });
  }

  const returnToTopButton =
    document.getElementById("return-to-top");


  if (!returnToTopButton) {
    return;
  }


  const reducedMotion =
    window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    );


  function updateReturnToTopButton() {

    const shouldShow =
      window.scrollY > 500;


    returnToTopButton.classList.toggle(
      "is-visible",
      shouldShow
    );


    returnToTopButton.setAttribute(
      "aria-hidden",
      String(!shouldShow)
    );


    returnToTopButton.tabIndex =
      shouldShow ? 0 : -1;
  }


  returnToTopButton.addEventListener(
    "click",
    () => {

      window.scrollTo({
        top: 0,

        behavior:
          reducedMotion.matches
            ? "auto"
            : "smooth"
      });

    }
  );


  window.addEventListener(
    "scroll",
    updateReturnToTopButton,
    { passive: true }
  );


  updateReturnToTopButton();

});
