/* Service worker do Bilhete: deixa instalar como app e guarda a casca para abrir rápido.
   Os dados sempre vêm do Supabase (nunca do cache). As notificações entram aqui na próxima etapa. */
const V = 'bilhete-v3';
const SHELL = ['./', 'index.html', 'supa.js', 'config.js', 'manifest.webmanifest', 'icons/icon-192.png',
  'fonts/caveat-latin-500-normal.woff2', 'fonts/caveat-latin-700-normal.woff2', 'fonts/dm-sans-latin-400-normal.woff2', 'fonts/dm-sans-latin-500-normal.woff2', 'fonts/dm-sans-latin-700-normal.woff2'];
self.addEventListener('install', e => { e.waitUntil(caches.open(V).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);
  if (e.request.method !== 'GET' || u.origin !== location.origin) return;
  // rede primeiro (pega versão nova), cache se estiver sem internet
  e.respondWith(fetch(e.request).then(r => { const c = r.clone(); caches.open(V).then(x => x.put(e.request, c)); return r; }).catch(() => caches.match(e.request)));
});

/* notificações */
self.addEventListener('push', e => {
  let d = {}; try { d = e.data ? e.data.json() : {}; } catch (_) { d = { title: 'Bilhete', body: e.data && e.data.text() }; }
  e.waitUntil((async () => {
    await self.registration.showNotification(d.title || 'Bilhete', { body: d.body || '', tag: d.tag || 'bilhete', renotify: true, icon: 'icons/icon-192.png', badge: 'icons/icon-192.png', data: { url: d.url || './' } });
    try { if (self.navigator && self.navigator.setAppBadge) await self.navigator.setAppBadge(); } catch (_) {}
  })());
});
self.addEventListener('notificationclick', e => {
  e.notification.close();
  e.waitUntil((async () => {
    const all = await self.clients.matchAll({ type: 'window', includeUncontrolled: true });
    for (const c of all) { if ('focus' in c) return c.focus(); }
    return self.clients.openWindow(new URL(e.notification.data && e.notification.data.url || './', self.registration.scope).href);
  })());
});
