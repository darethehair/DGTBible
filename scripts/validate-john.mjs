import fs from 'node:fs';
import path from 'node:path';

const root=process.cwd();
const fail=[];
const warn=[];
const readJson=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const reconstruct=items=>items.map(x=>(x.text||'')+(x.after||'')).join('');
const manifest=readJson('data/john/manifest.json');
const overrides=readJson('data/john/curated-overrides.json');
const verseMap=new Map();

for(const entry of manifest.chapters){
  const file='data/john/'+entry.file;
  const chapter=readJson(file);
  if(chapter.book!==manifest.book) fail.push(`${file}: book must be ${manifest.book}`);
  if(chapter.chapter!==entry.chapter) fail.push(`${file}: chapter metadata mismatch`);
  if(chapter.verses.length!==entry.verses) fail.push(`${file}: expected ${entry.verses} verses, found ${chapter.verses.length}`);

  chapter.verses.forEach((v,i)=>{
    const ref=`John.${entry.chapter}.${v.v}`;
    verseMap.set(ref,v);
    if(v.v!==i+1) fail.push(`${ref}: verses must be sequential; position ${i+1} contains ${v.v}`);
    for(const field of ['greek','literal','dgt']){
      if(typeof v[field]!=='string'||!v[field].length) fail.push(`${ref}: missing ${field} text`);
    }
    if(v.notes!==undefined&&!Array.isArray(v.notes)) fail.push(`${ref}: notes must be an array`);
    if(!v.alignment){fail.push(`${ref}: missing alignment`);return}

    const greekIds=new Set();
    for(const layer of ['greek','translit','literal','dgt']){
      const items=v.alignment[layer];
      if(!Array.isArray(items)||!items.length){fail.push(`${ref}: alignment.${layer} missing or empty`);continue}
      for(const item of items){
        if(typeof item.text!=='string') fail.push(`${ref}: alignment.${layer} item missing text`);
        if(item.after!==undefined&&typeof item.after!=='string') fail.push(`${ref}: alignment.${layer} after must be a string`);
        if(!Array.isArray(item.ids)||!item.ids.length) fail.push(`${ref}: alignment.${layer} item has no ids`);
        if(layer==='dgt' && Array.isArray(item.ids) && item.ids.length>2 && !overrides[ref]) fail.push(`${ref}: DGT alignment item spans too many Greek IDs (${item.ids.join(', ')}) — split to token-level mapping`);
      }
    }
    for(const item of v.alignment.greek||[]){
      for(const id of item.ids||[]){
        if(greekIds.has(id)) fail.push(`${ref}: duplicate Greek alignment id ${id}`);
        greekIds.add(id);
      }
    }
    for(const layer of ['translit','literal','dgt']){
      for(const item of v.alignment[layer]||[]) for(const id of item.ids||[]){
        if(!greekIds.has(id)) fail.push(`${ref}: alignment.${layer} references unknown Greek id ${id}`);
      }
    }
    for(const [layer,field] of [['greek','greek'],['literal','literal'],['dgt','dgt']]){
      if(reconstruct(v.alignment[layer]||[])!==v[field]) fail.push(`${ref}: alignment.${layer} does not reconstruct ${field} exactly`);
    }
  });
}

for(const [ref,override] of Object.entries(overrides)){
  const verse=verseMap.get(ref);
  if(!verse) fail.push(`${ref}: curated override has no loaded verse`);
  else if(JSON.stringify(verse.alignment)!==JSON.stringify(override.alignment)) fail.push(`${ref}: generated alignment no longer matches curated override`);
}

const sourceDir=path.join(root,'data/sources');
const sourceFiles=fs.readdirSync(sourceDir).filter(n=>/^step-john-.*\.json$/.test(n)).sort();
const sourceRefs=new Map();
let sourceMeta=null;
for(const name of sourceFiles){
  const data=readJson('data/sources/'+name);
  const meta={source:data.source,upstream:data.upstream,mirror:data.mirror,license:data.license};
  if(!sourceMeta) sourceMeta=meta;
  else if(JSON.stringify(meta)!==JSON.stringify(sourceMeta)) fail.push(`data/sources/${name}: STEPBible source metadata differs from other chunks`);
  if(data.license!=='CC BY 4.0') fail.push(`data/sources/${name}: expected CC BY 4.0`);
  for(const v of data.verses||[]){
    const ref=`John.${Number(v.chapter)}.${Number(v.verse)}`;
    if(sourceRefs.has(ref)) fail.push(`${ref}: duplicated across STEPBible source chunks`);
    sourceRefs.set(ref,v);
    if(!Array.isArray(v.words)||!v.words.length) fail.push(`${ref}: STEPBible source verse has no words`);
  }
}
for(const ref of verseMap.keys()) if(!sourceRefs.has(ref)) fail.push(`${ref}: no preserved STEPBible source verse`);
for(const ref of sourceRefs.keys()) if(!verseMap.has(ref)) warn.push(`${ref}: STEPBible source preserved but chapter is not yet in manifest`);

if(warn.length){
  console.log('Warnings:');
  for(const x of warn) console.log(' - '+x);
}
if(fail.length){
  console.error(`Validation failed with ${fail.length} problem(s):`);
  for(const x of fail) console.error(' - '+x);
  process.exit(1);
}
console.log(`Validated ${verseMap.size} John verses across ${manifest.chapters.length} chapter(s), ${sourceRefs.size} preserved STEPBible source verses, and ${Object.keys(overrides).length} curated override(s).`);
