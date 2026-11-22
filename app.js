const APP_VERSION='v0.22';
const state={book:'John',slug:'john',chapter:1,verse:1,data:null,mode:localStorage.getItem('dgt-mode')||'study'};
let books=[],availableChapters=[],paragraphStarts={},editorialNotes={};
const $=id=>document.getElementById(id);
const layerDefaults={greek:true,translit:false,literal:false,dgt:true,notes:false};
const layers={...layerDefaults,...JSON.parse(localStorage.getItem('dgt-layers')||'{}')};

function esc(s){return String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function transliterateGreek(s){
 const map={'α':'a','β':'b','γ':'g','δ':'d','ε':'e','ζ':'z','η':'ē','θ':'th','ι':'i','κ':'k','λ':'l','μ':'m','ν':'n','ξ':'x','ο':'o','π':'p','ρ':'r','σ':'s','ς':'s','τ':'t','υ':'y','φ':'ph','χ':'ch','ψ':'ps','ω':'ō','Α':'A','Β':'B','Γ':'G','Δ':'D','Ε':'E','Ζ':'Z','Η':'Ē','Θ':'Th','Ι':'I','Κ':'K','Λ':'L','Μ':'M','Ν':'N','Ξ':'X','Ο':'O','Π':'P','Ρ':'R','Σ':'S','Τ':'T','Υ':'Y','Φ':'Ph','Χ':'Ch','Ψ':'Ps','Ω':'Ō'};
 return s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').split('').map(c=>map[c]??c).join('');
}
function hashRef(){return '#'+state.slug+'.'+state.chapter+'.'+state.verse}
function parseHash(){
 const m=location.hash.match(/^#([^.]+)\.(\d+)\.(\d+)$/i);if(!m)return null;
 const slug=m[1].toLowerCase();return books.some(b=>b.slug===slug)?{slug,chapter:+m[2],verse:+m[3]}:null;
}
function parseRef(s){
 const raw=s.trim().toLowerCase().replace(/\s+/g,' ');
 for(const b of books){
  for(const name of [b.name,...(b.aliases||[])]){
   const n=name.toLowerCase().replace(/\s+/g,' ');
   if(raw.startsWith(n)){
    const rest=raw.slice(n.length).trim(),m=rest.match(/^(\d+)\s*[:.]\s*(\d+)$/);
    if(m)return{slug:b.slug,chapter:+m[1],verse:+m[2]};
   }
  }
 }
 const m=raw.match(/^(\d+)\s*[:.]\s*(\d+)$/);return m?{slug:state.slug,chapter:+m[1],verse:+m[2]}:null;
}
async function loadCatalog(){
 const r=await fetch('data/books.json');if(!r.ok)throw new Error('Book catalog unavailable');
 books=(await r.json()).books||[];$('book').innerHTML=books.map(b=>`<option value="${esc(b.slug)}">${esc(b.name)}</option>`).join('');
}
async function loadBookResources(slug){
 const b=books.find(x=>x.slug===slug);if(!b)throw new Error('Unknown book');
 state.slug=b.slug;state.book=b.name;$('book').value=b.slug;const base=`data/${b.slug}`;
 const [mr,pr,nr]=await Promise.all([fetch(base+'/manifest.json'),fetch(base+'/paragraphs.json'),fetch(base+'/editorial-notes.json')]);
 if(!mr.ok)throw new Error(b.name+' manifest unavailable');
 const manifest=await mr.json();availableChapters=(manifest.chapters||[]).map(x=>Number(x.chapter)).filter(Number.isInteger).sort((a,b)=>a-b);
 paragraphStarts=pr.ok?((await pr.json()).chapters||{}):{};editorialNotes=nr.ok?((await nr.json()).notes||{}):{};
 $('chapter').innerHTML=availableChapters.map(ch=>`<option value="${ch}">${ch}</option>`).join('');
}
async function loadChapter(ch){
 const r=await fetch(`data/${state.slug}/${String(ch).padStart(2,'0')}.json`);if(!r.ok)throw new Error(`${state.book} ${ch} is not loaded yet.`);
 const data=await r.json();for(const v of data.verses||[]){const extra=editorialNotes[`${ch}:${v.v}`]||[];if(extra.length)v.notes=[...(v.notes||[]),...extra.filter(n=>!(v.notes||[]).includes(n))]}return data;
}
function scrollTo(id,toolbarClass,behavior='smooth'){const target=$(id);if(!target)return;const h=document.querySelector(toolbarClass)?.getBoundingClientRect().height||0;window.scrollTo({top:Math.max(0,window.scrollY+target.getBoundingClientRect().top-h-12),behavior})}
function setMode(mode){
 state.mode=mode;localStorage.setItem('dgt-mode',mode);$('studyView').hidden=mode!=='study';$('chapterView').hidden=mode!=='chapter';$('compactView').hidden=mode!=='compact';
 document.querySelectorAll('[data-mode]').forEach(b=>b.classList.toggle('active',b.dataset.mode===mode));
 if(state.data){if(mode==='chapter'){renderChapter();requestAnimationFrame(()=>scrollTo('v'+state.verse,'.chapter-toolbar'))}else if(mode==='compact'){renderCompact();requestAnimationFrame(()=>scrollTo('compact-v'+state.verse,'.compact-toolbar'))}else renderStudy()}
}
function saveLayers(){localStorage.setItem('dgt-layers',JSON.stringify(layers));renderChapter()}
function renderLayerControls(){document.querySelectorAll('[data-layer]').forEach(cb=>{cb.checked=!!layers[cb.dataset.layer];cb.onchange=()=>{layers[cb.dataset.layer]=cb.checked;saveLayers()}})}
function clearAlignment(){document.querySelectorAll('.align-token.active').forEach(el=>el.classList.remove('active'))}
function highlightAlignment(ids){clearAlignment();if(!ids?.length)return;document.querySelectorAll('.align-token').forEach(el=>{const mine=(el.dataset.ids||'').split(',');if(mine.some(id=>ids.includes(id)))el.classList.add('active')})}
function renderAligned(container,key,verse,fallback){
 const items=verse.alignment?.[key];if(!items){container.textContent=fallback;return}
 container.innerHTML=items.map(item=>{const ids=(item.ids||[]).join(',');return ids?`<span class="align-token" tabindex="0" data-ids="${ids}">${esc(item.text)}</span>${esc(item.after||'')}`:`<span class="unaligned-token" title="No high-confidence automatic Greek link">${esc(item.text)}</span>${esc(item.after||'')}`}).join('');
 const activate=e=>{
  const el=e.target.closest?.('.align-token');
  if(!el||!container.contains(el))return;
  highlightAlignment((el.dataset.ids||'').split(',').filter(Boolean));
 };
 container.onmouseover=activate;
 container.onclick=activate;
 container.onfocusin=activate;
}
function refText(v=state.verse){return `${state.book} ${state.chapter}:${v}`}
function renderStudy(){
 const verse=state.data.verses.find(x=>x.v===state.verse);if(!verse)return;$('verseCard').hidden=false;$('reference').textContent=refText();
 renderAligned($('greek'),'greek',verse,verse.greek);renderAligned($('translit'),'translit',verse,transliterateGreek(verse.greek));renderAligned($('literal'),'literal',verse,verse.literal);renderAligned($('english'),'dgt',verse,verse.dgt);
 const notes=verse.notes||[];$('notesWrap').hidden=!notes.length;$('notes').innerHTML=notes.map(n=>`<p>${esc(n)}</p>`).join('');
 const ai=$('alignmentNotice');ai.hidden=!!verse.alignment;ai.textContent=verse.alignment?'':'Word alignment for this verse has not yet been manually curated.';
 const ci=availableChapters.indexOf(state.chapter),first=state.data.verses[0].v,last=state.data.verses.at(-1).v;$('prevVerse').disabled=ci===0&&state.verse===first;$('nextVerse').disabled=ci===availableChapters.length-1&&state.verse===last;$('studyPosition').textContent=refText();
}
function renderGrid(){const g=$('verseGrid');g.innerHTML='';for(const x of state.data.verses){const b=document.createElement('button');b.textContent=x.v;b.className=x.v===state.verse?'active':'';b.onclick=()=>show(state.chapter,x.v,true,true);g.appendChild(b)}}
function updateChapterNav(){
 const i=availableChapters.indexOf(state.chapter),pd=i<=0,nd=i<0||i>=availableChapters.length-1;
 for(const id of ['prevChapterTop','prevChapterBottom','prevCompactChapterTop','prevCompactChapterBottom']){const el=$(id);if(el)el.disabled=pd}
 for(const id of ['nextChapterTop','nextChapterBottom','nextCompactChapterTop','nextCompactChapterBottom']){const el=$(id);if(el)el.disabled=nd}
 for(const id of ['chapterPositionTop','chapterPositionBottom','compactPositionTop','compactPositionBottom']){const el=$(id);if(el)el.textContent=`${state.book} ${state.chapter}`}
}
async function moveChapter(delta){const i=availableChapters.indexOf(state.chapter),next=i+delta;if(next<0||next>=availableChapters.length)return;const ch=availableChapters[next],d=await loadChapter(ch);await show(ch,d.verses[0].v,true,false);window.scrollTo({top:0,behavior:'smooth'})}
function renderCompact(){
 if(!state.data)return;$('compactHeading').textContent=`${state.book} ${state.chapter}`;updateChapterNav();const starts=new Set((paragraphStarts[String(state.chapter)]||[state.data.verses[0]?.v]).map(Number));let html='',open=false;
 for(const v of state.data.verses){if(starts.has(v.v)||!open){if(open)html+='</p>';html+='<p class="compact-paragraph">';open=true}else html+=' ';html+=`<span class="compact-verse" id="compact-v${v.v}"><button class="compact-number" data-compact-study="${v.v}" title="Study ${esc(refText(v.v))}">${v.v}</button><span class="compact-text">${esc(v.dgt)}</span></span>`}
 if(open)html+='</p>';$('compactReading').innerHTML=html;document.querySelectorAll('[data-compact-study]').forEach(b=>b.onclick=()=>{state.verse=+b.dataset.compactStudy;setMode('study');show(state.chapter,state.verse)});
}
function renderChapter(){
 if(!state.data)return;$('chapterHeading').textContent=`${state.book} ${state.chapter}`;updateChapterNav();
 $('chapterReading').innerHTML=state.data.verses.map(v=>`<article class="chapter-verse" id="v${v.v}"><button class="verse-number" title="Study ${esc(refText(v.v))}" data-study="${v.v}">${v.v}</button>${layers.greek?`<div class="cv-greek">${esc(v.greek)}</div>`:''}${layers.translit?`<div class="cv-translit">${esc(transliterateGreek(v.greek))}</div>`:''}${layers.literal?`<div class="cv-literal">${esc(v.literal)}</div>`:''}${layers.dgt?`<div class="cv-dgt">${esc(v.dgt)}</div>`:''}${layers.notes&&v.notes?.length?`<div class="cv-notes">${v.notes.map(n=>`<p>${esc(n)}</p>`).join('')}</div>`:''}</article>`).join('');
 document.querySelectorAll('[data-study]').forEach(b=>b.onclick=()=>{state.verse=+b.dataset.study;setMode('study');show(state.chapter,state.verse)});
}
async function show(ch,v,push=true,scroll=true){
 try{state.data=await loadChapter(ch);const verse=state.data.verses.find(x=>x.v===v);if(!verse)throw new Error(`${state.book} ${ch}:${v} is not loaded.`);
 Object.assign(state,{chapter:ch,verse:v});$('status').textContent='';$('ref').value=refText();$('chapter').value=String(ch);$('chapterTitle').textContent=`${state.book} ${ch}`;renderGrid();if(state.mode==='study')renderStudy();else if(state.mode==='chapter')renderChapter();else renderCompact();if(push)location.hash=hashRef();
 if(scroll){if(state.mode==='study')$('verseCard').scrollIntoView({behavior:'smooth',block:'start'});else if(state.mode==='chapter')requestAnimationFrame(()=>scrollTo('v'+state.verse,'.chapter-toolbar'));else requestAnimationFrame(()=>scrollTo('compact-v'+state.verse,'.compact-toolbar'))}}catch(e){$('status').textContent=e.message}
}
async function selectBook(slug,ch=1,v=1,push=true){await loadBookResources(slug);const targetCh=availableChapters.includes(ch)?ch:availableChapters[0],d=await loadChapter(targetCh);await show(targetCh,d.verses.some(x=>x.v===v)?v:d.verses[0].v,push,false)}
async function moveVerse(delta){
 let ch=state.chapter;const ci=availableChapters.indexOf(ch),verses=state.data?.verses||[],vi=verses.findIndex(x=>x.v===state.verse);if(vi<0)return;const ni=vi+delta;
 if(ni>=0&&ni<verses.length){await show(ch,verses[ni].v);return}if(ni<0&&ci>0){ch=availableChapters[ci-1];const d=await loadChapter(ch);await show(ch,d.verses.at(-1).v);return}if(ni>=verses.length&&ci>=0&&ci<availableChapters.length-1){ch=availableChapters[ci+1];const d=await loadChapter(ch);await show(ch,d.verses[0].v)}
}
$('refForm').addEventListener('submit',async e=>{e.preventDefault();const r=parseRef($('ref').value);if(!r){$('status').textContent='Try a reference such as John 1:18 or 1 John 5:20.';return}setMode('study');if(r.slug!==state.slug)await selectBook(r.slug,r.chapter,r.verse);else show(r.chapter,r.verse)});
$('book').addEventListener('change',async e=>selectBook(e.target.value));$('chapter').addEventListener('change',async e=>{const ch=+e.target.value,d=await loadChapter(ch);show(ch,d.verses[0].v,true,false)});
$('copyLink').onclick=async()=>{await navigator.clipboard.writeText(location.href);$('copyLink').textContent='Copied';setTimeout(()=>$('copyLink').textContent='Copy link',1200)};
const verseCard=$('verseCard');
verseCard.addEventListener('mouseleave',clearAlignment);
verseCard.addEventListener('click',e=>{if(!e.target.closest('.align-token'))clearAlignment()});
$('prevVerse').onclick=()=>moveVerse(-1);$('nextVerse').onclick=()=>moveVerse(1);
for(const id of ['prevChapterTop','prevChapterBottom','prevCompactChapterTop','prevCompactChapterBottom']){const el=$(id);if(el)el.onclick=()=>moveChapter(-1)}for(const id of ['nextChapterTop','nextChapterBottom','nextCompactChapterTop','nextCompactChapterBottom']){const el=$(id);if(el)el.onclick=()=>moveChapter(1)}
document.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>setMode(b.dataset.mode));document.addEventListener('keydown',e=>{if(state.mode!=='study'||['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName))return;if(e.key==='ArrowLeft')moveVerse(-1);if(e.key==='ArrowRight')moveVerse(1)});
let touchX=null;$('studyView').addEventListener('touchstart',e=>touchX=e.changedTouches[0].clientX,{passive:true});$('studyView').addEventListener('touchend',e=>{if(touchX==null)return;const dx=e.changedTouches[0].clientX-touchX;touchX=null;if(Math.abs(dx)>70)moveVerse(dx>0?-1:1)},{passive:true});
window.addEventListener('hashchange',async()=>{const h=parseHash();if(!h)return;if(h.slug!==state.slug)await selectBook(h.slug,h.chapter,h.verse,false);else show(h.chapter,h.verse,false,false)});
(async()=>{$('appVersion').textContent=APP_VERSION;if('serviceWorker'in navigator)navigator.serviceWorker.register('sw.js');await loadCatalog();renderLayerControls();const h=parseHash();await loadBookResources(h?.slug||'john');setMode(state.mode);await show(h?.chapter||availableChapters[0],h?.verse||1,false,false)})();
