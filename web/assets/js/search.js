/*
 * FND Education Project search
 *
 * Pagefind performs the actual static-site search. This file adds only a
 * conservative normalization layer in front of it. The visible query is never
 * changed; normalized wording is passed to Pagefind behind the scenes.
 *
 * Keep this layer deliberately small. Medical concepts should not be inferred
 * here unless the relationship is unambiguous and has been reviewed.
 */

(function () {
  "use strict";

  /*
   * Explicit spelling corrections are safer than broad automatic edit-distance
   * correction on a medical site. Broad correction can turn an ordinary word
   * into a medical term the reader did not intend.
   */
  const SPELLING_REPLACEMENTS = [
    [/\bsiezures\b/gi, "seizures"],
    [/\bsiezure\b/gi, "seizure"],
    [/\bseziures\b/gi, "seizures"],
    [/\bseziure\b/gi, "seizure"],
    [/\bseizueres\b/gi, "seizures"],
    [/\bseizuer\b/gi, "seizure"],
    [/\bnuerological\b/gi, "neurological"],
    [/\bneuroligical\b/gi, "neurological"],
    [/\bfunctionnal\b/gi, "functional"],
    [/\bdistonia\b/gi, "dystonia"]
  ];

  /*
   * These are terminology aliases rather than diagnoses. They translate a few
   * common search terms into the wording used most consistently on this site.
   * Additions should be reviewed as the FND concept vocabulary grows.
   */
  const TERM_ALIASES = [
    [/\bpsychogenic\s+non[-\s]?epileptic\s+seizures?\b/gi, "functional seizures"],
    [/\bnon[-\s]?epileptic\s+seizures?\b/gi, "functional seizures"],
    [/\bnonepileptic\s+seizures?\b/gi, "functional seizures"],
    [/\bpnes\b/gi, "functional seizures"],
    [/\bhoovers?\s+sign\b/gi, "Hoover's sign"]
  ];


  function normalizeSearchTerm(term) {
    let normalized = String(term || "")
      .normalize("NFKC")
      .replace(/[‘’]/g, "'")
      .replace(/\s+/g, " ")
      .trim();

    for (const [pattern, replacement] of SPELLING_REPLACEMENTS) {
      normalized = normalized.replace(pattern, replacement);
    }

    for (const [pattern, replacement] of TERM_ALIASES) {
      normalized = normalized.replace(pattern, replacement);
    }

    return normalized;
  }


  function showUnavailableMessage(container) {
    const message = document.createElement("p");

    message.className = "search-unavailable";
    message.textContent =
      "Search could not load. The rest of the FND Education Project remains available through the main navigation and sitemap.";

    container.replaceChildren(message);
  }


  document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("pagefind-search");

    if (!container) {
      return;
    }

    if (typeof window.PagefindUI !== "function") {
      showUnavailableMessage(container);
      return;
    }

    const search = new window.PagefindUI({
      element: "#pagefind-search",
      showSubResults: true,
      showImages: false,
      pageSize: 8,
      excerptLength: 18,
      debounceTimeoutMs: 300,
      processTerm: normalizeSearchTerm,
      processResult: function (result) {
        // Pagefind's Default UI displays every custom metadata field. Keep
        // subject metadata available for ranking, but remove it before the
        // result is rendered so visitors see content rather than search internals.
        if (result && result.meta) {
          const cleanedMeta = { ...result.meta };

          for (const key of Object.keys(cleanedMeta)) {
            if (key.startsWith("subject_")) {
              delete cleanedMeta[key];
            }
          }

          result.meta = cleanedMeta;
        }

        return result;
      },
      ranking: {
        metaWeights: {
          title: 5.0,
          description: 2.0,

          // Site structure is deterministic and therefore stronger evidence
          // than AI-added supplementary associations.
          subject_structural: 2.0,
          subject_structural_lay: 1.2,
          subject_ai: 0.9,
          subject_ai_lay: 0.55,
          subject_misspellings: 0.2
        }
      },
      translations: {
        placeholder: "Search the FND Education Project",
        zero_results: "No results found for [SEARCH_TERM]"
      }
    });

    const initialQuery =
      new URLSearchParams(window.location.search).get("q");

    if (initialQuery && initialQuery.trim()) {
      search.triggerSearch(initialQuery.trim());
    }
  });
})();
