module.exports = {
  globDirectory: 'book/',
  globPatterns: [
    '**/*.{html,js,css,png,jpg,svg,gif,json,woff,woff2,ttf,eot}'
  ],
  swDest: 'book/sw.js',
  swSrc: 'pwa/sw-src.js',
  maximumFileSizeToCacheInBytes: 60 * 1024 * 1024 // 60MB
};
