const APP_VERSION='v0.14';
const state={book:'John',chapter:1,verse:1,data:null,mode:localStorage.getItem('dgt-mode')||'study'};
let availableChapters=[1,2];
const $=id=>document.getElementById(id);
const layerDefaults={greek:true,translit:false,literal:false,dgt:true,notes:false};
const layers={...layerDefaults,...JSON.parse(localStorage.getItem('dgt-layers')||'{}')};

function transliterateGreek(s){
  const map={'α':'a','β':'b','γ':'g','δ':'d','ε':'e','ζ':'z','η':'ē','θ':'th','ι':'i','κ':'k','λ':'l','μ':'m','ν':'n','ξ':'x','ο':'o','π':'p','ρ':'r','σ':'s','ς':'s','τ':'t','υ':'y','φ':'ph','χ':'ch','ψ':'ps','ω':'ō','Α':'A','Β':'B','Γ':'G','Δ':'D','Ε':'E','Ζ':'Z','Η':'Ē','Θ':'Th','Ι':'I','Κ':'K','Λ':'L','Μ':'M','Ν':'N','Ξ':'X','Ο':'O','Π':'P','Ρ':'R','Σ':'S','Τ':'T','Υ':'Y','Φ':'Ph','Χ':'Ch','Ψ':'Ps','Ω':'Ō'};
  return s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').split('').map(c=>map[c]??c).join('');
}
async function loadBookManifest(){
  try{
    const r=await fetch('data/john/manifest.json');
    if(!r.ok) throw new Error('manifest unavailable');
    const manifest=await r.json();
    const chapters=(manifest.chapters||[]).map(x=>Number(x.chapter)).filter(Number.isInteger).sort((a,b)=>a-b);
    if(chapters.length) availableChapters=chapters;
  }catch(_){}
  const select=$('chapter');
  select.innerHTML=availableChapters.map(ch=>`<option value="${ch}">${ch}</option>`).join('');
}
async function loadChapter(ch){const r=await fetch(`data/john/${String(ch).padStart(2,'0')}.json`);if(!r.ok)throw new Error(`John ${ch} is not loaded yet.`);return r.json()}
function parseRef(s){const m=s.trim().match(/^(?:john|jn|joh)?\s*(\d+)\s*[:.]\s*(\d+)$/i);return m?{chapter:+m[1],verse:+m[2]}:null}
function scrollToChapterVerse(verse=state.verse,behavior='smooth'){
  const target=$('v'+verse);
  if(!target)return;
  const toolbar=document.querySelector('.chapter-toolbar');
  const toolbarHeight=toolbar?.getBoundingClientRect().height||0;
  const extra=12;
  const top=window.scrollY+target.getBoundingClientRect().top-toolbarHeight-extra;
  window.scrollTo({top:Math.max(0,top),behavior});
}
function scrollToCompactVerse(verse=state.verse,behavior='smooth'){
  const target=$('compact-v'+verse);
  if(!target)return;
  const toolbar=document.querySelector('.compact-toolbar');
  const offset=(toolbar?.getBoundingClientRect().height||0)+12;
  const top=window.scrollY+target.getBoundingClientRect().top-offset;
  window.scrollTo({top:Math.max(0,top),behavior});
}
function setMode(mode){
  state.mode=mode;
  localStorage.setItem('dgt-mode',mode);
  $('studyView').hidden=mode!=='study';
  $('chapterView').hidden=mode!=='chapter';
  $('compactView').hidden=mode!=='compact';
  document.querySelectorAll('[data-mode]').forEach(b=>b.classList.toggle('active',b.dataset.mode===mode));
  if(state.data){
    if(mode==='chapter'){
      renderChapter();
      requestAnimationFrame(()=>scrollToChapterVerse(state.verse));
    }else if(mode==='compact'){
      renderCompact();
      requestAnimationFrame(()=>scrollToCompactVerse(state.verse));
    }else renderStudy();
  }
}
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
    if(!ids) return `<span class="unaligned-token" title="No high-confidence automatic Greek link">${esc(item.text)}</span>${esc(item.after||'')}`;
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
  const alignNotice=$('alignmentNotice');
  alignNotice.hidden=!!verse.alignment;
  alignNotice.textContent=verse.alignment?'':'Word alignment for this verse has not yet been manually curated.';
  const chapterIndex=availableChapters.indexOf(state.chapter);const firstVerse=state.data.verses[0].v;const lastVerse=state.data.verses.at(-1).v;
  $('prevVerse').disabled=chapterIndex===0&&state.verse===firstVerse;$('nextVerse').disabled=chapterIndex===availableChapters.length-1&&state.verse===lastVerse;
  $('studyPosition').textContent=`John ${state.chapter}:${state.verse}`;
}
function renderGrid(){
  const g=$('verseGrid');g.innerHTML='';
  for(const x of state.data.verses){
    const b=document.createElement('button');
    b.textContent=x.v;
    b.className=x.v===state.verse?'active':'';
    b.onclick=()=>{
      if(state.mode==='chapter') show(state.chapter,x.v,true,true);
      else if(state.mode==='compact') show(state.chapter,x.v,true,true);
      else show(state.chapter,x.v,true,true);
    };
    g.appendChild(b);
  }
}
function esc(s){return s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function renderCompact(){
  if(!state.data)return;
  $('compactHeading').textContent=`John ${state.chapter}`;
  $('compactReading').innerHTML=state.data.verses.map(v=>`<span class="compact-verse" id="compact-v${v.v}"><button class="compact-number" data-compact-study="${v.v}" title="Study John ${state.chapter}:${v.v}">${v.v}</button><span class="compact-text">${esc(v.dgt)}</span></span>`).join(' ');
  document.querySelectorAll('[data-compact-study]').forEach(b=>b.onclick=()=>{
    state.verse=+b.dataset.compactStudy;
    setMode('study');
    show(state.chapter,state.verse);
  });
}
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
    if(state.mode==='study') renderStudy();
    else if(state.mode==='chapter') renderChapter();
    else renderCompact();
    if(push)location.hash=`John.${ch}.${v}`;
    if(scroll){
      if(state.mode==='study') $('verseCard').scrollIntoView({behavior:'smooth',block:'start'});
      else if(state.mode==='chapter') requestAnimationFrame(()=>scrollToChapterVerse(state.verse));
      else requestAnimationFrame(()=>scrollToCompactVerse(state.verse));
    }
  }catch(e){$('status').textContent=e.message}
}
async function moveVerse(delta){
  let ch=state.chapter;
  const chapterIndex=availableChapters.indexOf(ch);
  const verses=state.data?.verses||[];
  const verseIndex=verses.findIndex(x=>x.v===state.verse);
  if(verseIndex<0)return;
  const nextIndex=verseIndex+delta;
  if(nextIndex>=0&&nextIndex<verses.length){
    await show(ch,verses[nextIndex].v);
    return;
  }
  if(nextIndex<0&&chapterIndex>0){
    ch=availableChapters[chapterIndex-1];
    const d=await loadChapter(ch);
    await show(ch,d.verses.at(-1).v);
    return;
  }
  if(nextIndex>=verses.length&&chapterIndex>=0&&chapterIndex<availableChapters.length-1){
    ch=availableChapters[chapterIndex+1];
    const d=await loadChapter(ch);
    await show(ch,d.verses[0].v);
  }
}
$('refForm').addEventListener('submit',e=>{e.preventDefault();const r=parseRef($('ref').value);if(!r){$('status').textContent='Try a reference such as John 1:18.';return}setMode('study');show(r.chapter,r.verse)});
$('chapter').addEventListener('change',async e=>{const ch=+e.target.value;const d=await loadChapter(ch);show(ch,d.verses[0].v,true,false)});
$('copyLink').onclick=async()=>{await navigator.clipboard.writeText(location.href);$('copyLink').textContent='Copied';setTimeout(()=>$('copyLink').textContent='Copy link',1200)};
$('verseCard').addEventListener('mouseleave',clearAlignment);
$('verseCard').addEventListener('click',e=>{if(!e.target.closest('.align-token'))clearAlignment()});
$('prevVerse').onclick=()=>moveVerse(-1);$('nextVerse').onclick=()=>moveVerse(1);
document.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>setMode(b.dataset.mode));
document.addEventListener('keydown',e=>{if(state.mode!=='study'||['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName))return;if(e.key==='ArrowLeft')moveVerse(-1);if(e.key==='ArrowRight')moveVerse(1)});
let touchX=null;$('studyView').addEventListener('touchstart',e=>touchX=e.changedTouches[0].clientX,{passive:true});$('studyView').addEventListener('touchend',e=>{if(touchX==null)return;const dx=e.changedTouches[0].clientX-touchX;touchX=null;if(Math.abs(dx)>70)moveVerse(dx>0?-1:1)},{passive:true});
window.addEventListener('hashchange',()=>{const m=location.hash.match(/^#John\.(\d+)\.(\d+)$/i);if(m)show(+m[1],+m[2],false,false)});
(async()=>{$('appVersion').textContent=APP_VERSION;if('serviceWorker'in navigator)navigator.serviceWorker.register('sw.js');await loadBookManifest();renderLayerControls();setMode(state.mode);const m=location.hash.match(/^#John\.(\d+)\.(\d+)$/i);await show(m?+m[1]:availableChapters[0],m?+m[2]:1,false,false)})();