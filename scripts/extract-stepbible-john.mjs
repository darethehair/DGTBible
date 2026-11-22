import fs from 'node:fs/promises';
import path from 'node:path';

const upstreamSha='5de0a47f35f0fc13dfe1430d104e5db8a4285f9c';
const file='Translators Amalgamated OT+NT/TAGNT Mat-Jhn - Translators Amalgamated Greek NT - STEPBible.org CC-BY.txt';
const url='https://raw.githubusercontent.com/STEPBible/STEPBible-Data/'+upstreamSha+'/'+file.split('/').map(encodeURIComponent).join('/');
const sblgntSha='d7f35adca9ec410e1d1499c63b4dd989d76c8d4d';
const sblgntUrl='https://raw.githubusercontent.com/Faithlife/SBLGNT/'+sblgntSha+'/data/sblgnt/text/John.txt';
const start=Number(process.env.START_CHAPTER||4);
const end=Number(process.env.END_CHAPTER||10);

const res=await fetch(url);
if(!res.ok) throw new Error('STEPBible download failed: '+res.status+' '+res.statusText);
const text=await res.text();
const lines=text.split(/\r?\n/);

const patterns=[
  /(?:^|\t)(?:Jhn|John|Jn)[ ._-]?(\d+)[.:](\d+)/i,
  /(?:^|\t)(?:JHN|JOH)\s+(\d+):(\d+)/,
  /(?:^|\t)(?:Jhn|John|Jn)\.(\d+)\.(\d+)/i
];

const matched=[];
const diagnostics=[];
for(const line of lines){
  let m=null;
  for(const p of patterns){ m=line.match(p); if(m) break; }
  if(m){
    const ch=Number(m[1]);
    if(ch>=start&&ch<=end) matched.push(line);
  } else if(diagnostics.length<50 && /Jhn|John|\bJHN\b|\bJOH\b/i.test(line)){
    diagnostics.push(line);
  }
}

await fs.mkdir('authoring',{recursive:true});
await fs.writeFile('authoring/step-john-'+String(start).padStart(2,'0')+'-'+String(end).padStart(2,'0')+'.tsv',
  [
    '# STEPBible TAGNT extraction',
    '# source: STEPBible/STEPBible-Data@'+upstreamSha,
    '# range: John '+start+'-'+end,
    ...matched
  ].join('\n')+'\n');
await fs.writeFile('authoring/step-john-diagnostics.txt',diagnostics.join('\n')+'\n');

const sblRes=await fetch(sblgntUrl);
if(!sblRes.ok) throw new Error('SBLGNT download failed: '+sblRes.status+' '+sblRes.statusText);
const sblText=await sblRes.text();
const sblLines=sblText.split(/\r?\n/).filter(line=>{
  const m=line.match(/^John (\d+):(\d+)\t/);
  return m && Number(m[1])>=start && Number(m[1])<=end;
});
await fs.writeFile(
  'authoring/sblgnt-john-'+String(start).padStart(2,'0')+'-'+String(end).padStart(2,'0')+'.txt',
  ['# SBLGNT extraction','# source: Faithlife/SBLGNT@'+sblgntSha,'# range: John '+start+'-'+end,...sblLines].join('\n')+'\n'
);
console.log('Matched',sblLines.length,'SBLGNT verses for John',start+'-'+end);

console.log('Downloaded',text.length,'characters /',lines.length,'lines');
console.log('Matched',matched.length,'lines for John',start+'-'+end);
if(matched.length<100){
  console.log('Diagnostic John-like lines:', diagnostics.slice(0,10));
  throw new Error('Too few John lines matched; inspect diagnostics artifact before trusting parser.');
}
