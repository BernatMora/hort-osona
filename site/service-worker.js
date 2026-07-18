// service-worker.js — Service Worker per a Hort Osona PWA
// Cache-first per a l'HTML i assets, network-first per a Open-Meteo

const CACHE_VERSION = 'hort-osona-v3';
const STATIC_CACHE = CACHE_VERSION + '-static';
const RUNTIME_CACHE = CACHE_VERSION + '-runtime';

const STATIC_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon.svg',
  './icon-192.png',
  './icon-512.png',
  './checklist-data.json',
];

// Instal·lació: pre-cache dels assets estàtics
self.addEventListener('install', event => {
  console.log('[SW] Instal·lant...');
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => cache.addAll(STATIC_ASSETS))
      .then(() => self.skipWaiting())
  );
});

// Activació: netejar caches antigues
self.addEventListener('activate', event => {
  console.log('[SW] Activant...');
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys
          .filter(key => key !== STATIC_CACHE && key !== RUNTIME_CACHE)
          .map(key => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

// Fetch: cache-first per a assets locals, network-first per a Open-Meteo
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Network-first per a Open-Meteo (dades meteorològiques)
  if (url.hostname === 'api.open-meteo.com') {
    event.respondWith(
      fetch(request)
        .then(response => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(RUNTIME_CACHE).then(cache => cache.put(request, clone));
          }
          return response;
        })
        .catch(() => caches.match(request))
    );
    return;
  }

  // Cache-first per a la resta (incloent l'HTML i JSON)
  if (request.method === 'GET') {
    event.respondWith(
      caches.match(request)
        .then(cached => {
          if (cached) return cached;
          return fetch(request)
            .then(response => {
              if (response.ok && (url.origin === location.origin)) {
                const clone = response.clone();
                caches.open(RUNTIME_CACHE).then(cache => cache.put(request, clone));
              }
              return response;
            })
            .catch(() => {
              // Fallback: si és una navegació i no tenim caché, retorna l'index
              if (request.mode === 'navigate') {
                return caches.match('./index.html');
              }
            });
        })
    );
  }
});

// Escoltar missatges del client (per actualitzar el SW manualment)
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
