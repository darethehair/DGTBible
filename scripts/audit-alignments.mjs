import fs from 'node:fs';
import path from 'node:path';

const root=process.cwd();
const manifest=JSON.parse(fs.readFileSync(path.join(root,'data/john/manifest.json'),'utf8'));
const allowPath=path.join(root,'data/john/semantic-audit-allowlist.json');
const allow=fs.existsSync(allowPath)?JSON.parse(fs.readFileSync(allowPath,'utf8')):{};
const generic=new Set(['the','a','an','of','to','and','or','in','on','at','for','with','from','by','that','this','one','he','she','it','they','we','you','i','me','him','her','his','their','our','your','my','is','was','were','be','been','being','has','have','had','do','did','does','not','no','are','am','will','would','should','could']);

const norm=s=>String(s||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^\p{L}\p{N}\s]/gu,' ').replace(/\s+/g,' ').trim();
const words=s=>norm(s).split(' ').filter(Boolean);

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
        const overlap=pwords.some(w=>gwords.includes(w));
        let score=0;
        const reasons=[];
        if(separated){score+=2;reasons.push('noncontiguous')}
        if(gwords.length&&pwords.length&&!overlap){score+=1;reasons.push('no-gloss-overlap')}
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
