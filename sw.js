const CACHE='dgtbible-v026';
const ASSETS=['./','index.html','style.css','app.js','manifest.webmanifest','data/john/manifest.json','data/john/paragraphs.json','data/john/editorial-notes.json','icons/icon.svg','data/john/01.json','data/john/02.json','data/john/03.json','data/john/04.json','data/john/05.json','data/john/06.json','data/john/07.json','data/john/08.json','data/john/09.json','data/john/10.json','data/john/11.json','data/john/12.json','data/john/13.json','data/john/14.json','data/john/15.json','data/john/16.json','data/john/17.json','data/john/18.json','data/john/19.json','data/john/20.json','data/john/21.json'];

self.addEventListener('install',event=>{
  self.skipWaiting();
  event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(ASSETS)));
});

self.addEventListener('activate',event=>{
  event.waitUntil(
    caches.keys()
      .then(keys=>Promise.all(keys.filter(key=>key!==CACHE).map(key=>caches.delete(key))))
      .then(()=>self.clients.claim())
  );
});

self.addEventListener('fetch',event=>{
  if(event.request.method!=='GET') return;
  const url=new URL(event.request.url);
  if(url.origin!==self.location.origin) return;

  event.respondWith(
    fetch(event.request)
      .then(response=>{
        if(response && response.ok){
          const copy=response.clone();
          caches.open(CACHE).then(cache=>cache.put(event.request,copy));
        }
        return response;
      })
      .catch(()=>caches.match(event.request).then(cached=>cached||caches.match('./')))
  );
});