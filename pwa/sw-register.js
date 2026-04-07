if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    const swPath = (window.rootPath || '') + 'sw.js';
    navigator.serviceWorker.register(swPath).then(registration => {
      console.log('SW registered: ', registration);
    }).catch(registrationError => {
      console.log('SW registration failed: ', registrationError);
    });
  });
}
