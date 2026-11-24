// Full-book Mark authoring extractor.
import fs from 'node:fs/promises';

const upstreamSha='5de0a47f35f0fc13dfe1430d104e5db8a4285f9c';
const stepFile='Translators Amalgamated OT+NT/TAGNT Mat-Jhn - Translators Amalgamated Greek NT - STEPBible.org CC-BY.txt';
const stepUrl='https://raw.githubusercontent.com/STEPBible/STEPBible-Data/'+upstreamSha+'/'+stepFile.split('/').map(encodeURIComponent).join('/');
const sblgntSha='d7f35adca9ec410e1d1499c63b4dd989d76c8d4d';
const sblUrl='https://raw.githubusercontent.com/Faithlife/SBLGNT/'+sblgntSha+'/data/sblgnt/text/Mark.txt';

const stepRes=await fetch(stepUrl);
if(!stepRes.ok)throw new Error('STEPBible download failed: '+stepRes.status);
const stepLines=(await stepRes.text()).split(/\r?\n/);
await fs.mkdir('authoring',{recursive:true});
const sblRes=await fetch(sblUrl);
if(!sblRes.ok)throw new Error('Mark SBLGNT download failed: '+sblRes.status);
const patterns=[
  /(?:^|\t)(?:Mrk|Mar|Mark|Mk)[ ._-]?(\d+)[.:](\d+)/i,
  /(?:^|\t)(?:MRK|MAR)\s+(\d+):(\d+)/,
  /(?:^|\t)(?:Mrk|Mar|Mark|Mk)\\.(\d+)\\.(\d+)/i
];
const matched=[];
const diagnostics=[];
for(const line of stepLines){
  let m=null;
  for(const p of patterns){ m=line.match(p); if(m) break; }
  if(m) matched.push(line);
  else if(diagnostics.length<50 && /Mrk|Mar|Mark|\bMRK\b|\bMAR\b/i.test(line)) diagnostics.push(line);
}
await fs.writeFile('authoring/step-mark.tsv',['# STEPBible TAGNT extraction','# source: STEPBible/STEPBible-Data@'+upstreamSha,'# book: Mark',...matched].join('\n')+'\n');
const sblLines=(await sblRes.text()).split(/\r?\n/).filter(line=>/^Mark \d+:\d+\t/.test(line));
await fs.writeFile('authoring/sblgnt-mark.txt',['# SBLGNT extraction','# source: Faithlife/SBLGNT@'+sblgntSha,'# book: Mark',...sblLines].join('\n')+'\n');
console.log('Matched',sblLines.length,'SBLGNT verses and',matched.length,'TAGNT lines for Mark');
if(sblLines.length!==673)throw new Error('Unexpected SBLGNT verse count for Mark: '+sblLines.length);
if(matched.length<5000){
  console.log('Diagnostic Mark-like lines:', diagnostics.slice(0,10));
  console.log('Sample Mrk.001.001 rows:', stepLines.filter(line=>line.includes('Mrk.001.001')).slice(0,12));
  console.log('Sample Mark opening Greek rows:', stepLines.filter(line=>/Ἀρχὴ|ἀρχὴ|Αρχη/.test(line)).slice(0,12));
  throw new Error('Too few TAGNT lines for Mark');
}
