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
