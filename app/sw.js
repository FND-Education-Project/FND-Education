/*
 * Minimal app-shell offline cache. Explicit asset allowlist only.
 *
 * Never cache private account responses, imported data, or arbitrary fetches.
 * When shell assets change, bump CACHE_VERSION so updates take effect.
 */
const CACHE_VERSION = "fnd-journey-phase0-v1";
const SHELL = [
  "./", "./index.html", "./styles.css", "./manifest.webmanifest",
  "./icon.svg", "./src/app.mjs", "./src/scene-model.mjs",
  "./src/storage.mjs", "./assets/scene.png"
];
const allowedPaths = new Set(SHELL.map(path => new URL(path, self.registration.scope).pathname));

self.addEventListener("install", event => {
  event.waitUntil(caches.open(CACHE_VERSION).then(cache => cache.addAll(SHELL)));
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  event.waitUntil((async () => {
    for (const key of await caches.keys()) {
      if (key.startsWith("fnd-journey-phase0-") && key !== CACHE_VERSION) {
        await caches.delete(key);
      }
    }
    await self.clients.claim();
  })());
});

self.addEventListener("fetch", event => {
  const request = event.request;
  if (request.method !== "GET") return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin || !allowedPaths.has(url.pathname)) return;
  event.respondWith((async () => {
    const cache = await caches.open(CACHE_VERSION);
    const cached = await cache.match(request, { ignoreSearch: true });
    if (cached) return cached;
    return fetch(request);
  })());
});
