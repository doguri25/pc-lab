/* Bundled-shell worker: no cross-version asset mixing, no automatic reload,
 * no catch-all HTML fallback, no deleting unrelated caches or any user saves. */
'use strict';
const VERSION='__RELEASE_VERSION__',BUILD='__BUILD_ID__';
function hash(s){let h=2166136261;for(const c of s){h^=c.charCodeAt(0);h=Math.imul(h,16777619);}return (h>>>0).toString(36);}
const SCOPE=self.registration.scope,PREFIX='pc-lab:cache:'+hash(SCOPE)+':',CACHE=PREFIX+BUILD;
const INDEX=new URL('index.html',SCOPE).href,ASSETS=['index.html','assets/icon.svg','manifest.webmanifest'].map(x=>new URL(x,SCOPE).href);
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(async c=>{for(const url of ASSETS){const r=await fetch(new Request(url,{cache:'reload'}));if(!r.ok)throw Error('Asset unavailable');await c.put(url,r);}})));
// A new release waits naturally for old controlled tabs to close. No skipWaiting.
self.addEventListener('activate',e=>e.waitUntil(Promise.resolve()));
self.addEventListener('fetch',e=>{
 const u=new URL(e.request.url);if(e.request.method!=='GET'||u.origin!==self.location.origin||!u.href.startsWith(SCOPE))return;
 if(u.searchParams.has('fresh'))return; // explicit diagnostic requests bypass this cache.
 const relative=u.pathname.slice(new URL(SCOPE).pathname.length);
 if(e.request.mode==='navigate'&&(relative===''||relative==='index.html')){
  e.respondWith((async()=>{const c=await caches.open(CACHE);try{const r=await fetch(new Request(e.request,{cache:'no-store'}));if(r.ok){const text=await r.clone().text();if(text.includes('name="pc-lab-version"'))await c.put(INDEX,r.clone());}return r;}catch{return await c.match(INDEX)||Response.error();}})());return;
 }
 if(ASSETS.includes(u.href)&&relative!=='index.html')e.respondWith((async()=>{const c=await caches.open(CACHE);return await c.match(u.href)||fetch(e.request);})());
 // Missing/versioned HTML requests are left alone (404 offline), never sent to an old home page.
});
