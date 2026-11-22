import fs from 'node:fs';
import path from 'node:path';

const root=process.cwd();
const overrides=JSON.parse(fs.readFileSync(path.join(root,'data/john/curated-overrides.json'),'utf8'));
const byChapter=new Map();

for(const [ref,override] of Object.entries(overrides)){
  const m=ref.match(/^John\.(\d+)\.(\d+)$/);
  if(!m) throw new Error('Unsupported override reference: '+ref);
  const ch=Number(m[1]), v=Number(m[2]);
  if(!byChapter.has(ch)) byChapter.set(ch,[]);
  byChapter.get(ch).push({v,override});
}

for(const [ch,items] of byChapter){
  const file=path.join(root,'data/john',String(ch).padStart(2,'0')+'.json');
  const data=JSON.parse(fs.readFileSync(file,'utf8'));
  for(const {v,override} of items){
    const verse=data.verses.find(x=>x.v===v);
    if(!verse) throw new Error(`John ${ch}:${v} not found in ${file}`);
    verse.alignment=override.alignment;
  }
  fs.writeFileSync(file,JSON.stringify(data,null,2)+'\n');
  console.log(`Applied ${items.length} curated override(s) to John ${ch}`);
}
