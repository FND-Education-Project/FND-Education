/*
 * FND Education: site-wide account controls and preferences.
 *
 * Loaded only when the optional learner API has been deliberately configured.
 * Never store account identity, session tokens, theme preferences, or progress
 * in localStorage. All persistent preferences belong to the signed-in learner.
 */
(function () {
  "use strict";
  const script = document.currentScript;
  const endpoint = script && script.dataset.apiEndpoint;
  if (!endpoint) return;
  let api;
  try {
    api = new URL(endpoint);
    if (api.protocol !== "https:" ||
        api.origin !== "https://accounts.fndeducationproject.org" ||
        api.pathname !== "/") return;
  } catch { return; }

  let me = null;
  function node(tag, text, className) {
    const n = document.createElement(tag);
    if (text !== undefined) n.textContent = text;
    if (className) n.className = className;
    return n;
  }
  function applyTheme(theme) {
    if (theme === "light" || theme === "dark") {
      document.documentElement.dataset.theme = theme;
    } else {
      delete document.documentElement.dataset.theme;
    }
  }
  async function request(route, method = "GET", data) {
    const headers = { Accept: "application/json" };
    if (method !== "GET") {
      if (!me || !me.csrfToken) throw new Error("Please sign in again.");
      headers["X-FND-CSRF"] = me.csrfToken;
      headers["Content-Type"] = "application/json";
    }
    const response = await fetch(new URL(route, api), {
      method,
      headers,
      credentials: "include",
      cache: "no-store",
      referrerPolicy: "no-referrer",
      body: method === "GET" ? undefined : JSON.stringify(data || {})
    });
    if (!response.ok) {
      throw new Error(response.status === 401
        ? "Your sign-in needs to be renewed."
        : "Could not save your changes. Please try again.");
    }
    return response.json();
  }
  function loginUrl(provider) {
    const path = /^\/course\/(?:m\d+\/(?:\d+\/)?)?$/.test(location.pathname)
      ? location.pathname : "/course/";
    const url = new URL("/v1/auth/start/" + provider, api);
    url.searchParams.set("return", path);
    return url.href;
  }

  // The Promise resolves even for guests. Course progress rendering is gated
  // on the authenticated result, never on a profile left in browser storage.
  const ready = request("/v1/me").then(data => {
    me = data;
    applyTheme(me.theme);
    return data;
  }).catch(() => null);

  window.FNDAccount = Object.freeze({
    ready,
    get user() { return me; },
    apiRequest: request,
    loginUrl
  });

  document.addEventListener("DOMContentLoaded", async function () {
    const shell = document.getElementById("learner-account-shell");
    if (!shell) return;
    await ready;
    shell.replaceChildren();
    const status = node("div", undefined, "account-status");

    if (!me) {
      // Login buttons are published only after credentials and the API
      // endpoint have been approved and configured.
      status.append(node("strong", "Save your learning progress"));
      status.append(node("span",
        "Sign in to keep your own lesson checkmarks and theme preferences."));
      const actions = node("span", undefined, "account-actions");
      for (const provider of ["google", "apple"]) {
        const link = node("a",
          "Continue with " + (provider === "google" ? "Google" : "Apple"));
        link.href = loginUrl(provider);
        actions.append(link);
      }
      shell.append(status, actions);
      shell.hidden = false;
      return;
    }

    status.append(node("span", "Signed in as", "account-caption"));
    status.append(node("strong", me.username, "account-username"));
    shell.append(status);

    const settings = node("details", undefined, "account-settings");
    const summary = node("summary", "Account & preferences");
    settings.append(summary);
    const form = node("form", undefined, "account-settings-form");
    form.setAttribute("aria-label", "Learner account preferences");

    const nameLabel = node("label", "Display username");
    const nameInput = node("input");
    nameInput.type = "text";
    nameInput.maxLength = 40;
    nameInput.minLength = 2;
    nameInput.required = true;
    nameInput.value = me.username;
    nameLabel.append(nameInput);
    form.append(nameLabel);

    function field(labelText, options, initial) {
      const label = node("label", labelText);
      const select = node("select");
      for (const [value, title] of options) {
        const opt = node("option", title);
        opt.value = value;
        select.append(opt);
      }
      select.value = String(initial);
      label.append(select);
      form.append(label);
      return select;
    }

    const theme = field("Appearance", [
      ["system", "Follow device setting"],
      ["light", "Light theme"],
      ["dark", "Dark theme"]
    ], me.theme);
    const idle = field("Automatic sign-out", [
      ["0", "Off — stay signed in"],
      ["15", "After 15 minutes of inactivity"],
      ["60", "After 1 hour of inactivity"],
      ["1440", "After 1 day of inactivity"],
      ["10080", "After 7 days of inactivity"]
    ], me.idleMinutes);

    const notice = node("p",
      "Stay signed in is the default. For security, login credentials still " +
      "have a renewable lifespan and can be revoked.",
      "account-note");
    form.append(notice);
    // No email is retained, so no email warning can be sent to a learner
    // before the long-term inactivity deletion policy takes effect.
    const retention = node("p",
      "To protect privacy, learner accounts unused for three years are " +
      "automatically removed, including their lesson progress. " +
      "Signing in and using the account resets that period. " +
      "We do not store an email address to send deletion reminders.",
      "account-note");
    form.append(retention);
    const message = node("p", "", "account-feedback");
    message.setAttribute("role", "status");
    const save = node("button", "Save preferences");
    save.type = "submit";
    form.append(save, message);

    form.addEventListener("submit", async function (event) {
      event.preventDefault();
      save.disabled = true;
      message.textContent = "";
      try {
        const prefs = await request("/v1/settings", "PATCH", {
          username: nameInput.value.trim(),
          theme: theme.value,
          idleMinutes: Number(idle.value)
        });
        Object.assign(me, prefs);
        status.querySelector(".account-username").textContent = me.username;
        applyTheme(me.theme);
        message.textContent = "Preferences saved.";
      } catch (error) {
        message.textContent = error.message;
      } finally { save.disabled = false; }
    });
    settings.append(form);

    const signout = node("button", "Sign out / switch learner");
    signout.type = "button";
    signout.addEventListener("click", async function () {
      signout.disabled = true;
      try {
        await request("/v1/logout", "POST", {});
        location.reload();
      } catch (error) {
        message.textContent = error.message;
        settings.open = true;
        signout.disabled = false;
      }
    });
    settings.append(signout);

    const exportLink = node("a", "Export my saved progress");
    exportLink.href = new URL("/v1/export", api).href;
    exportLink.target = "_blank";
    exportLink.rel = "noopener noreferrer";
    // Export via a same-site credential cookie uses a navigation, not JS.
    settings.append(exportLink);

    const deleteButton = node("button", "Delete my learner account");
    deleteButton.type = "button";
    deleteButton.addEventListener("click", async function () {
      const typed = window.prompt(
        "To permanently delete your account and lesson progress, " +
        "type your username exactly:\n" + me.username
      );
      if (typed !== me.username) return;
      if (!window.confirm(
        "Delete this learner account, linked login identity, " +
        "preferences and ALL saved lesson progress now? " +
        "This cannot be undone."
      )) return;
      deleteButton.disabled = true;
      try {
        await request("/v1/account", "DELETE", {
          confirmed: true, confirmedUsername: me.username
        });
        location.reload();
      } catch (error) {
        message.textContent = error.message;
        settings.open = true;
        deleteButton.disabled = false;
      }
    });
    settings.append(deleteButton);

    shell.append(settings);
    shell.hidden = false;
  });
})();
