const state={book:'John',chapter:1,verse:1,data:null};
const $=id=>document.getElementById(id);
function transliterateGreek(s){
  const map={
    'α':'a','β':'b','γ':'g','δ':'d','ε':'e','ζ':'z','η':'ē','θ':'th','ι':'i','κ':'k','λ':'l','μ':'m','ν':'n','ξ':'x','ο':'o','π':'p','ρ':'r','σ':'s','ς':'s','τ':'t','υ':'y','φ':'ph','χ':'ch','ψ':'ps','ω':'ō',
    'Α':'A','Β':'B','Γ':'G','Δ':'D','Ε':'E','Ζ':'Z','Η':'Ē','Θ':'Th','Ι':'I','Κ':'K','Λ':'L','Μ':'M','Ν':'N','Ξ':'X','Ο':'O','Π':'P','Ρ':'R','Σ':'S','Τ':'T','Υ':'Y','Φ':'Ph','Χ':'Ch','Ψ':'Ps','Ω':'Ō'
  };
  return s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').split('').map(c=>map[c]??c).join('');
}
async function loadChapter(ch){const p=`data/john/${String(ch).padStart(2,'0')}.json`;const r=await fetch(p);if(!r.ok)throw new Error(`John ${ch} is not loaded yet.`);return r.json()}
function parseRef(s){const m=s.trim().match(/^(?:john|jn|joh)?\s*(\d+)\s*[:.]\s*(\d+)$/i);if(!m)return null;return {chapter:+m[1],verse:+m[2]}}
async function show(ch,v,push=true){try{state.data=await loadChapter(ch);const verse=state.data.verses.find(x=>x.v===v);if(!verse)throw new Error(`John ${ch}:${v} is not in this prototype.`);Object.assign(state,{chapter:ch,verse:v});$('status').textContent='';$('verseCard').hidden=false;$('reference').textContent=`John ${ch}:${v}`;$('greek').textContent=verse.greek;$('translit').textContent=transliterateGreek(verse.greek);$('literal').textContent=verse.literal||'Literal line not yet added.';$('english').textContent=verse.dgt;const notes=verse.notes||[];$('notesWrap').hidden=!notes.length;$('notes').innerHTML=notes.map(n=>`<p>${n}</p>`).join('');$('ref').value=`John ${ch}:${v}`;$('chapter').value=String(ch);$('chapterTitle').textContent=`John ${ch}`;renderGrid();if(push)location.hash=`John.${ch}.${v}`;document.querySelector('.verse-card').scrollIntoView({behavior:'smooth',block:'start'});}catch(e){$('status').textContent=e.message}}
function renderGrid(){const g=$('verseGrid');g.innerHTML='';for(const x of state.data.verses){const b=document.createElement('button');b.textContent=x.v;b.className=x.v===state.verse?'active':'';b.onclick=()=>show(state.chapter,x.v);g.appendChild(b)}}
$('refForm').addEventListener('submit',e=>{e.preventDefault();const r=parseRef($('ref').value);if(!r){$('status').textContent='Try a reference such as John 1:18.';return}show(r.chapter,r.verse)});
$('chapter').addEventListener('change',async e=>show(+e.target.value,1));
$('copyLink').onclick=async()=>{await navigator.clipboard.writeText(location.href);$('copyLink').textContent='Copied';setTimeout(()=>$('copyLink').textContent='Copy link',1200)};
window.addEventListener('hashchange',()=>{const m=location.hash.match(/^#John\.(\d+)\.(\d+)$/i);if(m)show(+m[1],+m[2],false)});
(async()=>{if('serviceWorker'in navigator)navigator.serviceWorker.register('sw.js');const m=location.hash.match(/^#John\.(\d+)\.(\d+)$/i);await show(m?+m[1]:1,m?+m[2]:1,false)})();
