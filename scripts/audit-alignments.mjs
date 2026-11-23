import fs from 'node:fs';
import path from 'node:path';

const root=process.cwd();
const manifest=JSON.parse(fs.readFileSync(path.join(root,'data/john/manifest.json'),'utf8'));
const allowPath=path.join(root,'data/john/semantic-audit-allowlist.json');
const allow=fs.existsSync(allowPath)?JSON.parse(fs.readFileSync(allowPath,'utf8')):{};
const generic=new Set(['the','a','an','of','to','and','or','in','on','at','for','with','from','by','that','this','one','he','she','it','they','we','you','i','me','him','her','his','their','our','your','my','is','was','were','be','been','being','has','have','had','do','did','does','not','no','are','am','will','would','should','could']);

const norm=s=>String(s||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^\p{L}\p{N}\s]/gu,' ').replace(/\s+/g,' ').trim();
const words=s=>norm(s).split(' ').filter(Boolean);


const semanticGroups=[
  ['say','said','says','saying','speak','spoke','spoken','tell','told'],
  ['see','seen','saw','behold','look','looked'],
  ['know','knew','known','understand','understood','recognize','recognized'],
  ['fear','feared','afraid'],
  ['hope','hoped','hoping'],
  ['believe','believed','believing'],
  ['seek','sought','seeking'],
  ['give','gave','given','gives'],
  ['go','went','going','depart','departed','leave','left'],
  ['come','comes','came','coming'],
  ['command','commands','commandment','commandments'],
  ['stone','stoned','stoning'],
  ['die','died','dies','death'],
  ['do','did','does','done','make','made'],
  ['hear','heard','hearing'],
  ['hold','held','holding'],
  ['free','freedom'],
  ['great','greater','large'],
  ['clay','mud'],
  ['take','took','taken','pick','picked'],
  ['bring','brings','brought','bringing'],
  ['write','writes','wrote','written','writing'],
  ['stumble','stumbles','stumbled','stumbling'],
  ['judge','judged','judging','condemn','condemned'],
];
const sem=new Map();
for(const g of semanticGroups) for(const w of g) sem.set(w,new Set(g));
const stem=w=>{
  let x=w;
  for(const suf of ['ing','ed','es','s']){
    if(x.length>suf.length+2 && x.endsWith(suf)) return x.slice(0,-suf.length);
  }
  return x;
};
const equiv=(a,b)=>a===b || stem(a)===stem(b) || sem.get(a)?.has(b) || sem.get(b)?.has(a);

const findings=[];
for(const entry of manifest.chapters){
  const ch=JSON.parse(fs.readFileSync(path.join(root,'data/john',entry.file),'utf8'));
  for(const v of ch.verses){
    const greekById={};
    for(const item of v.alignment?.greek||[]) for(const id of item.ids||[]) greekById[id]=item;
    for(const layer of ['literal','dgt']){
      const items=v.alignment?.[layer]||[];
      const positions={};
      items.forEach((item,i)=>(item.ids||[]).forEach(id=>(positions[id]??=[]).push(i)));
      for(const [id,pos] of Object.entries(positions)){
        const g=greekById[id];
        if(!g) continue;
        const separated=pos.some((p,i)=>i>0&&p!==pos[i-1]+1);
        const phrase=pos.map(i=>items[i].text).join(' ');
        const pwords=words(phrase).filter(w=>!generic.has(w));
        const gwords=words(g.gloss||'').filter(w=>!generic.has(w));
        const overlap=pwords.some(w=>gwords.some(gw=>equiv(w,gw)));
        let score=0;
        const reasons=[];
        if(separated){score+=2;reasons.push('noncontiguous')}
        if(gwords.length&&pwords.length&&!overlap){score+=1;reasons.push('no-gloss-overlap')}
        const splitOnlyByNegation=separated && pos.every((p,i)=>i===0 || (()=> {
          const start=pos[i-1]+1, end=p;
          const between=items.slice(start,end);
          return between.length>0 && between.every(x=>{
            const text=String(x.text||'').toLowerCase().replace(/[^a-z]/g,'');
            if(text==='not'||text==='no') return true;
            return (x.ids||[]).some(otherId=>{
              const other=greekById[otherId];
              const gloss=String(other?.gloss||'').toLowerCase();
              const morph=String(other?.morph||'');
              return morph.includes('PRT-N') || /\bnot\b|\bno\b|\bunless\b/.test(gloss);
            });
          });
        })());
        if(splitOnlyByNegation){
          score=Math.max(0,score-2);
          reasons.push('negation-split');
        }
        if(score>=3){
          const key=`John.${entry.chapter}.${v.v}|${layer}|${id}`;
          findings.push({key,ref:`John ${entry.chapter}:${v.v}`,layer,id,greek:g.text,gloss:g.gloss||'',phrase,positions:pos,score,reasons,allowed:Boolean(allow[key])});
        }
      }
    }
  }
}

const unexpected=findings.filter(x=>!x.allowed);
const stale=Object.keys(allow).filter(key=>!findings.some(x=>x.key===key));

if(findings.length){
  console.log('Semantic alignment audit findings:');
  for(const f of findings) console.log(` - ${f.allowed?'ALLOW':'CHECK'} ${f.key}: ${f.greek} [${f.gloss}] -> "${f.phrase}" (${f.reasons.join(', ')})`);
}
if(stale.length){
  console.error('Stale semantic-audit allowlist entries:');
  for(const key of stale) console.error(' - '+key);
}
if(unexpected.length||stale.length){
  console.error(`Semantic audit failed: ${unexpected.length} unexpected high-risk mapping(s), ${stale.length} stale allowlist entr${stale.length===1?'y':'ies'}.`);
  process.exit(1);
}
console.log(`Semantic audit passed: ${findings.length} high-risk pattern(s), all explicitly reviewed and allowed.`);
