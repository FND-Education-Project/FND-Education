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
