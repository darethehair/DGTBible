const APP_VERSION='v0.8';
const state={book:'John',chapter:1,verse:1,data:null,mode:localStorage.getItem('dgt-mode')||'study'};
const $=id=>document.getElementById(id);
const layerDefaults={greek:true,translit:false,literal:false,dgt:true,notes:false};
const layers={...layerDefaults,...JSON.parse(localStorage.getItem('dgt-layers')||'{}')};

function transliterateGreek(s){
  const map={'α':'a','β':'b','γ':'g','δ':'d','ε':'e','ζ':'z','η':'ē','θ':'th','ι':'i','κ':'k','λ':'l','μ':'m','ν':'n','ξ':'x','ο':'o','π':'p','ρ':'r','σ':'s','ς':'s','τ':'t','υ':'y','φ':'ph','χ':'ch','ψ':'ps','ω':'ō','Α':'A','Β':'B','Γ':'G','Δ':'D','Ε':'E','Ζ':'Z','Η':'Ē','Θ':'Th','Ι':'I','Κ':'K','Λ':'L','Μ':'M','Ν':'N','Ξ':'X','Ο':'O','Π':'P','Ρ':'R','Σ':'S','Τ':'T','Υ':'Y','Φ':'Ph','Χ':'Ch','Ψ':'Ps','Ω':'Ō'};
  return s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').split('').map(c=>map[c]??c).join('');
}
async function loadChapter(ch){const r=await fetch(`data/john/${String(ch).padStart(2,'0')}.json`);if(!r.ok)throw new Error(`John ${ch} is not loaded yet.`);return r.json()}
function parseRef(s){const m=s.trim().match(/^(?:john|jn|joh)?\s*(\d+)\s*[:.]\s*(\d+)$/i);return m?{chapter:+m[1],verse:+m[2]}:null}
function setMode(mode){state.mode=mode;localStorage.setItem('dgt-mode',mode);$('studyView').hidden=mode!=='study';$('chapterView').hidden=mode!=='chapter';document.querySelectorAll('[data-mode]').forEach(b=>b.classList.toggle('active',b.dataset.mode===mode));if(state.data) mode==='chapter'?renderChapter():renderStudy()}
function saveLayers(){localStorage.setItem('dgt-layers',JSON.stringify(layers));renderChapter()}
function renderLayerControls(){document.querySelectorAll('[data-layer]').forEach(cb=>{cb.checked=!!layers[cb.dataset.layer];cb.onchange=()=>{layers[cb.dataset.layer]=cb.checked;saveLayers()}})}
function clearAlignment(){
  document.querySelectorAll('.align-token.active').forEach(el=>el.classList.remove('active'));
}
function highlightAlignment(ids){
  clearAlignment();
  if(!ids?.length)return;
  document.querySelectorAll('.align-token').forEach(el=>{
    const mine=(el.dataset.ids||'').split(',');
    if(mine.some(id=>ids.includes(id))) el.classList.add('active');
  });
}
function renderAligned(container,key,verse,fallback){
  const items=verse.alignment?.[key];
  if(!items){container.textContent=fallback;return}
  container.innerHTML=items.map(item=>{
    const ids=(item.ids||[]).join(',');
    return `<span class="align-token" tabindex="0" data-ids="${ids}">${esc(item.text)}</span>${esc(item.after||'')}`;
  }).join('');
  container.querySelectorAll('.align-token').forEach(el=>{
    const go=()=>highlightAlignment((el.dataset.ids||'').split(',').filter(Boolean));
    el.addEventListener('click',go);
    el.addEventListener('mouseenter',go);
    el.addEventListener('focus',go);
  });
}
function renderStudy(){
  const verse=state.data.verses.find(x=>x.v===state.verse); if(!verse)return;
  $('verseCard').hidden=false;$('reference').textContent=`John ${state.chapter}:${state.verse}`;
  renderAligned($('greek'),'greek',verse,verse.greek);
  renderAligned($('translit'),'translit',verse,transliterateGreek(verse.greek));
  renderAligned($('literal'),'literal',verse,verse.literal);
  renderAligned($('english'),'dgt',verse,verse.dgt);
  const notes=verse.notes||[];$('notesWrap').hidden=!notes.length;$('notes').innerHTML=notes.map(n=>`<p>${n}</p>`).join('');
  $('prevVerse').disabled=state.chapter===1&&state.verse===1;$('nextVerse').disabled=state.chapter===2&&state.verse===25;
  $('studyPosition').textContent=`John ${state.chapter}:${state.verse}`;
}
function renderGrid(){const g=$('verseGrid');g.innerHTML='';for(const x of state.data.verses){const b=document.createElement('button');b.textContent=x.v;b.className=x.v===state.verse?'active':'';b.onclick=()=>show(state.chapter,x.v);g.appendChild(b)}}
function esc(s){return s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function renderChapter(){
  if(!state.data)return;
  $('chapterHeading').textContent=`John ${state.chapter}`;
  $('chapterReading').innerHTML=state.data.verses.map(v=>`<article class="chapter-verse" id="v${v.v}">
    <button class="verse-number" title="Study John ${state.chapter}:${v.v}" data-study="${v.v}">${v.v}</button>
    ${layers.greek?`<div class="cv-greek">${esc(v.greek)}</div>`:''}
    ${layers.translit?`<div class="cv-translit">${esc(transliterateGreek(v.greek))}</div>`:''}
    ${layers.literal?`<div class="cv-literal">${esc(v.literal)}</div>`:''}
    ${layers.dgt?`<div class="cv-dgt">${esc(v.dgt)}</div>`:''}
    ${layers.notes&&v.notes?.length?`<div class="cv-notes">${v.notes.map(n=>`<p>${esc(n)}</p>`).join('')}</div>`:''}
  </article>`).join('');
  document.querySelectorAll('[data-study]').forEach(b=>b.onclick=()=>{state.verse=+b.dataset.study;setMode('study');show(state.chapter,state.verse)});
}
async function show(ch,v,push=true,scroll=true){
  try{
    state.data=await loadChapter(ch);
    const verse=state.data.verses.find(x=>x.v===v); if(!verse)throw new Error(`John ${ch}:${v} is not loaded.`);
    Object.assign(state,{chapter:ch,verse:v});$('status').textContent='';$('ref').value=`John ${ch}:${v}`;$('chapter').value=String(ch);$('chapterTitle').textContent=`John ${ch}`;renderGrid();
    if(state.mode==='study')renderStudy(); else renderChapter();
    if(push)location.hash=`John.${ch}.${v}`;
    if(scroll&&state.mode==='study')$('verseCard').scrollIntoView({behavior:'smooth',block:'start'});
  }catch(e){$('status').textContent=e.message}
}
async function moveVerse(delta){
  let ch=state.chapter,v=state.verse+delta;
  if(v<1&&ch>1){ch--;const d=await loadChapter(ch);v=d.verses.at(-1).v}
  else if(state.data&&v>state.data.verses.at(-1).v&&ch<2){ch++;v=1}
  else if(v<1||v>(state.data?.verses.at(-1).v||1))return;
  await show(ch,v);
}
$('refForm').addEventListener('submit',e=>{e.preventDefault();const r=parseRef($('ref').value);if(!r){$('status').textContent='Try a reference such as John 1:18.';return}setMode('study');show(r.chapter,r.verse)});
$('chapter').addEventListener('change',async e=>show(+e.target.value,1,true,false));
$('copyLink').onclick=async()=>{await navigator.clipboard.writeText(location.href);$('copyLink').textContent='Copied';setTimeout(()=>$('copyLink').textContent='Copy link',1200)};
$('verseCard').addEventListener('mouseleave',clearAlignment);
$('verseCard').addEventListener('click',e=>{if(!e.target.closest('.align-token'))clearAlignment()});
$('prevVerse').onclick=()=>moveVerse(-1);$('nextVerse').onclick=()=>moveVerse(1);
document.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>setMode(b.dataset.mode));
document.addEventListener('keydown',e=>{if(state.mode!=='study'||['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName))return;if(e.key==='ArrowLeft')moveVerse(-1);if(e.key==='ArrowRight')moveVerse(1)});
let touchX=null;$('studyView').addEventListener('touchstart',e=>touchX=e.changedTouches[0].clientX,{passive:true});$('studyView').addEventListener('touchend',e=>{if(touchX==null)return;const dx=e.changedTouches[0].clientX-touchX;touchX=null;if(Math.abs(dx)>70)moveVerse(dx>0?-1:1)},{passive:true});
window.addEventListener('hashchange',()=>{const m=location.hash.match(/^#John\.(\d+)\.(\d+)$/i);if(m)show(+m[1],+m[2],false,false)});
(async()=>{$('appVersion').textContent=APP_VERSION;if('serviceWorker'in navigator)navigator.serviceWorker.register('sw.js');renderLayerControls();setMode(state.mode);const m=location.hash.match(/^#John\.(\d+)\.(\d+)$/i);await show(m?+m[1]:1,m?+m[2]:1,false,false)})();