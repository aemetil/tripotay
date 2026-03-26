importScripts('https://storage.googleapis.com/workbox-cdn/releases/7.0.0/workbox-sw.js');

const { registerRoute } = workbox.routing;
const { CacheFirst, NetworkFirst, StaleWhileRevalidate } = workbox.strategies;
const { ExpirationPlugin } = workbox.expiration;
const { BackgroundSyncPlugin } = workbox.backgroundSync;
const { precacheAndRoute } = workbox.precaching;

const CACHE_NAME = 'tripotay-v1';
const OFFLINE_URL = '/offline/';

// ── Précache de la page offline ──────────────────────────────
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll([OFFLINE_URL]))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(clients.claim());
});

// ── Static assets (CSS, JS, fonts) → Cache First ────────────
registerRoute(
  ({ request }) => ['style', 'script', 'font'].includes(request.destination),
  new CacheFirst({
    cacheName: 'static-assets',
    plugins: [
      new ExpirationPlugin({ maxEntries: 60, maxAgeSeconds: 30 * 24 * 60 * 60 }),
    ],
  })
);

// ── Images → Cache First 30 jours ───────────────────────────
registerRoute(
  ({ request }) => request.destination === 'image',
  new CacheFirst({
    cacheName: 'images',
    plugins: [
      new ExpirationPlugin({ maxEntries: 100, maxAgeSeconds: 30 * 24 * 60 * 60 }),
    ],
  })
);

// ── Pages HTML → Network First, fallback cache ───────────────
registerRoute(
  ({ request }) => request.destination === 'document',
  new NetworkFirst({
    cacheName: 'pages',
    plugins: [
      new ExpirationPlugin({ maxEntries: 50, maxAgeSeconds: 7 * 24 * 60 * 60 }),
    ],
    networkTimeoutSeconds: 4,
  })
);

// ── Background Sync — votes et commentaires offline ──────────
const bgSyncPlugin = new BackgroundSyncPlugin('offline-actions', {
  maxRetentionTime: 24 * 60, // 24h en minutes
});

// Intercepter les POST vers nos endpoints
registerRoute(
  ({ url }) => ['/vote/', '/komante/', '/rapote/'].some(p => url.pathname.includes(p)),
  new NetworkFirst({
    plugins: [bgSyncPlugin],
  }),
  'POST'
);

// ── Fallback offline pour les pages non cachées ──────────────
self.addEventListener('fetch', event => {
  if (event.request.destination === 'document') {
    event.respondWith(
      fetch(event.request).catch(() =>
        caches.match(OFFLINE_URL)
      )
    );
  }
});
