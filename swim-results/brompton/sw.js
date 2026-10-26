/* Kill switch for the retired club apps (Netlify + GitHub Pages, retired 24 Oct 2026).
   Their old service worker served its saved copy forever, so a parent's home-screen icon kept
   opening a snapshot of the club's data after the sites were deleted (James saw it, 25 Oct).
   Browsers re-check sw.js when the app opens; this one replaces the old worker, deletes every
   saved copy, unregisters itself and reloads the open window onto the plain page. No data here. */
self.addEventListener("install", function () { self.skipWaiting(); });
self.addEventListener("activate", function (e) {
  e.waitUntil(caches.keys()
    .then(function (ks) { return Promise.all(ks.map(function (k) { return caches.delete(k); })); })
    .then(function () { return self.registration.unregister(); })
    .then(function () { return self.clients.matchAll({ type: "window" }); })
    .then(function (cs) { cs.forEach(function (c) { c.navigate(c.url); }); }));
});
self.addEventListener("fetch", function (e) { e.respondWith(fetch(e.request)); });
