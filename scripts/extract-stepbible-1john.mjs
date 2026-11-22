import fs from 'node:fs/promises';

const upstreamSha='5de0a47f35f0fc13dfe1430d104e5db8a4285f9c';
const stepFile='Translators Amalgamated OT+NT/TAGNT Act-Rev - Translators Amalgamated Greek NT - STEPBible.org CC-BY.txt';
const stepUrl='https://raw.githubusercontent.com/STEPBible/STEPBible-Data/'+upstreamSha+'/'+stepFile.split('/').map(encodeURIComponent).join('/');
const sblgntSha='d7f35adca9ec410e1d1499c63b4dd989d76c8d4d';
const sblgntUrl='https://raw.githubusercontent.com/Faithlife/SBLGNT/'+sblgntSha+'/data/sblgnt/text/1John.txt';

const [stepRes,sblRes]=await Promise.all([fetch(stepUrl),fetch(sblgntUrl)]);
if(!stepRes.ok) throw new Error('STEPBible download failed: '+stepRes.status);
if(!sblRes.ok) throw new Error('SBLGNT download failed: '+sblRes.status);
const stepText=await stepRes.text();
const stepLines=stepText.split(/\r?\n/);
const patterns=[
 /(?:^|\t)(?:1Jn|1John|1Jo)[ ._-]?(\d+)[.:](\d+)/i,
 /(?:^|\t)(?:1JN|1JO)\s+(\d+):(\d+)/,
 /(?:^|\t)(?:1Jn|1John|1Jo)\.(\d+)\.(\d+)/i
];
const matched=[];
for(const line of stepLines){
 let m=null;
 for(const p of patterns){m=line.match(p);if(m)break;}
 if(m)matched.push(line);
}
await fs.mkdir('authoring',{recursive:true});
await fs.writeFile('authoring/step-1john.tsv',[
 '# STEPBible TAGNT extraction',
 '# source: STEPBible/STEPBible-Data@'+upstreamSha,
 '# book: 1 John',
 ...matched
].join('\n')+'\n');

const sblLines=(await sblRes.text()).split(/\r?\n/).filter(line=>/^1John \d+:\d+\t/.test(line));
await fs.writeFile('authoring/sblgnt-1john.txt',[
 '# SBLGNT extraction',
 '# source: Faithlife/SBLGNT@'+sblgntSha,
 '# book: 1 John',
 ...sblLines
].join('\n')+'\n');
console.log('Matched',sblLines.length,'SBLGNT verses and',matched.length,'TAGNT lines for 1 John');
if(sblLines.length!==105) throw new Error('Expected 105 SBLGNT verses for 1 John');
if(matched.length<1500) throw new Error('Too few TAGNT lines for 1 John; parser/source format needs review');
