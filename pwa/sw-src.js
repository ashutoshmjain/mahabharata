import { precacheAndRoute } from 'workbox-precaching';
import { registerRoute, NavigationRoute } from 'workbox-routing';
import { NetworkFirst } from 'workbox-strategies';

// Precache all assets
precacheAndRoute(self.__WB_MANIFEST);

// Handle navigation requests with a NetworkFirst strategy
// This ensures the PWA works offline but stays updated online
const navigationHandler = new NetworkFirst({
  cacheName: 'navigations',
});

const navigationRoute = new NavigationRoute(navigationHandler);
registerRoute(navigationRoute);

// Simple fetch handler to satisfy Chrome's PWA requirement
self.addEventListener('fetch', (event) => {
  // Pass-through for non-navigation requests handled by precache
});
