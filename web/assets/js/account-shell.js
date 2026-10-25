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

  // Load the anti-abuse widget only after a visitor chooses email sign-in.
  // No login identity, challenge or code is persisted in browser storage.
  let turnstileLoading;
  function loadTurnstile() {
    if (window.turnstile) return Promise.resolve(window.turnstile);
    if (!turnstileLoading) turnstileLoading = new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";
      script.async = true;
      script.onload = () => resolve(window.turnstile);
      script.onerror = () => { turnstileLoading = null; script.remove(); reject(new Error("Verification could not load. Please try again.")); };
      document.head.append(script);
    });
    return turnstileLoading;
  }

  /** Accessible two-stage form shared by guest login and deliberate linking. */
  function emailControl(options, linking = false) {
    const box = node("details", undefined, "account-email-login");
    box.append(node("summary", linking ? "Add email sign-in to this account" : "Continue with email"));
    box.append(node("p", linking
      ? "Verify an email to sign in to this same learner account without Google. An email already belonging to another learner account cannot be linked."
      : "No password needed. We will email an 8-digit code. If you already use Google here, sign in with Google first and add email in Account & preferences to keep the same progress."));
    box.append(node("p", "Email sign-in stores your email privately and uses Resend to deliver codes. We do not send marketing emails. Read the course without signing in whenever you prefer."));
    const form = node("form");
    const emailLabel = node("label", "Email address");
    const email = node("input");
    email.type = "email"; email.required = true; email.maxLength = 254;
    email.autocomplete = "email"; emailLabel.append(email); form.append(emailLabel);
    form.append(node("small", "Use an email address with standard English letters, numbers and symbols; international-character mailbox names are not supported yet."));
    const nameLabel = node("label", "Display username (for a new account)");
    const name = node("input");
    name.type = "text"; name.minLength = 2; name.maxLength = 40;
    name.autocomplete = "nickname";
    nameLabel.append(name);
    if (!linking) {
      form.append(nameLabel, node("p", "Optional: leave blank to start as Learner. Existing accounts keep their username."));
    }
    // Keep text-entry focus stable: load the third-party challenge only on
    // an explicit action after the visitor finishes entering account details.
    const beginVerification = node("button", "Continue to human verification");
    beginVerification.type = "button";
    const widget = node("div");
    widget.hidden = true;
    const send = node("button", "Send sign-in code");
    send.type = "submit"; send.disabled = true;
    const feedback = node("p", "", "account-feedback");
    feedback.setAttribute("role", "status"); feedback.setAttribute("aria-live", "polite");
    form.append(beginVerification, widget, send);
    const verify = node("form"); verify.hidden = true;
    const codeLabel = node("label", "8-digit code from your email");
    const code = node("input"); code.type = "text"; code.inputMode = "numeric";
    code.autocomplete = "one-time-code"; code.pattern = "[0-9]{8}";
    code.minLength = 8; code.maxLength = 8; code.required = true;
    codeLabel.append(code);
    const confirm = node("button", linking ? "Verify and add email" : "Verify and sign in");
    confirm.type = "submit";
    const again = node("button", "Request another code / change email"); again.type = "button";
    verify.append(codeLabel, confirm, again);
    box.append(form, verify, feedback);
    let token = "", widgetId, challengeId, busy = false;
    async function prepareWidget() {
      beginVerification.disabled = true;
      widget.hidden = false;
      feedback.textContent = "Complete the human verification, then select Send sign-in code.";
      try {
        const ts = await loadTurnstile();
        if (!ts || typeof ts.render !== "function") throw new Error("Verification could not load. Please try again.");
        // A previous challenge can expire or fail. Only rebuild it after
        // another explicit click, never while a visitor is entering an email.
        if (widgetId !== undefined) { ts.remove(widgetId); widgetId = undefined; }
        widgetId = ts.render(widget, { sitekey: options.turnstileSiteKey, action: "email_login",
          callback(value) { token = value; send.disabled = busy; },
          "expired-callback"() { token = ""; send.disabled = true; },
          "error-callback"() { token = ""; send.disabled = true; beginVerification.disabled = false; feedback.textContent = "Verification could not finish. Select Continue to human verification to retry."; }
        });
      } catch {
        // The visitor can retry deliberately; never start a widget while
        // they're in the middle of typing into either account field.
        widget.hidden = true;
        beginVerification.disabled = false;
        feedback.textContent = "Verification could not load. Please try again.";
      }
    }
    beginVerification.addEventListener("click", () => {
      if (!form.reportValidity()) return;
      prepareWidget();
    });
    async function post(stage, payload) {
      const headers = { "Content-Type": "application/json", Accept: "application/json" };
      if (linking) headers["X-FND-CSRF"] = me.csrfToken;
      const path = linking ? "/v1/account/email/" : "/v1/auth/email/";
      const response = await fetch(new URL(path + stage, api), {
        method: "POST", headers, credentials: "include", cache: "no-store",
        referrerPolicy: "no-referrer", body: JSON.stringify(payload),
        signal: AbortSignal.timeout(25000)
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || "Sign-in is temporarily unavailable.");
      return result;
    }
    form.addEventListener("submit", async event => {
      event.preventDefault();
      if (busy || !token) return;
      busy = true; send.disabled = true; feedback.textContent = "Sending your code…";
      try {
        const result = await post("start", { email: email.value, username: name.value,
          turnstileToken: token });
        challengeId = result.challengeId;
        form.hidden = true; verify.hidden = false; code.value = ""; code.focus();
        feedback.textContent = "Check your inbox and spam folder. Enter the code here within 10 minutes. Keep this browser tab open.";
      } catch (error) {
        feedback.textContent = error.name === "TimeoutError" ? "The request took too long. Please try again later." : error.message;
      } finally {
        busy = false;
        clearVerification();
      }
    });
    function clearVerification() {
      token = ""; send.disabled = true;
      if (window.turnstile && widgetId !== undefined) {
        window.turnstile.remove(widgetId);
        widgetId = undefined;
      }
      widget.hidden = true;
      beginVerification.disabled = false;
    }
    again.addEventListener("click", () => {
      challengeId = null; verify.hidden = true; form.hidden = false;
      clearVerification();
      feedback.textContent = "Wait at least one minute between code requests. Requesting a new code replaces the previous code in this browser.";
      // Wait for an explicit verification click after any email edits.
      email.focus();
    });
    verify.addEventListener("submit", async event => {
      event.preventDefault();
      if (busy || !challengeId) return;
      busy = true; confirm.disabled = true; again.disabled = true;
      feedback.textContent = "Checking your code…";
      try {
        await post("verify", { challengeId, code: code.value.trim() });
        // Reload obtains identity from the server session, never form values.
        if (linking) {
          verify.hidden = true;
          feedback.textContent = "Email sign-in added to this learner account. You can now use either Google (if already linked) or this email.";
        } else { location.reload(); }
      } catch (error) { feedback.textContent = error.message; }
      finally { busy = false; confirm.disabled = false; again.disabled = false; }
    });
    return box;
  }

  // The Promise resolves even for guests. Course progress rendering is gated
  // on the authenticated result, never on a profile left in browser storage.
  const optionsReady = request("/v1/auth/options").catch(() => ({}));
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
    const options = await optionsReady;
    shell.replaceChildren();
    const status = node("div", undefined, "account-status");

    if (!me) {
      // Login buttons are published only after credentials and the API
      // endpoint have been approved and configured.
      status.append(node("strong", "Save your learning progress"));
      status.append(node("span",
        "Sign in to keep your own lesson checkmarks and theme preferences. " +
        "Accounts unused for three years are deleted automatically, " +
        "without deletion reminders. Reading the course is free and needs no account."));
      const actions = node("span", undefined, "account-actions");
      if (options.google) {
        const link = node("a", "Continue with Google");
        link.href = loginUrl("google");
        actions.append(link);
      }
      if (options.email) actions.append(emailControl(options));
      if (!options.google && !options.email) {
        actions.append(node("span", "Sign-in is temporarily unavailable. You can still read every lesson."));
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
    // The same retention rule applies regardless of the login method.
    const retention = node("p",
      "To protect privacy, learner accounts unused for three years are " +
      "automatically removed, including their lesson progress. " +
      "Signing in and using the account resets that period. " +
      "Deletion reminders are not sent. Email sign-in addresses are kept privately for authentication and removed when the account is deleted.",
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
    if (options.email) settings.append(emailControl(options, true));

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
