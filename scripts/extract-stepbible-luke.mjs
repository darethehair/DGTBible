// Full-book Luke authoring extractor.
import fs from 'node:fs/promises';

const upstreamSha='5de0a47f35f0fc13dfe1430d104e5db8a4285f9c';
const stepFile='Translators Amalgamated OT+NT/TAGNT Mat-Jhn - Translators Amalgamated Greek NT - STEPBible.org CC-BY.txt';
const stepUrl='https://raw.githubusercontent.com/STEPBible/STEPBible-Data/'+upstreamSha+'/'+stepFile.split('/').map(encodeURIComponent).join('/');
const sblgntSha='d7f35adca9ec410e1d1499c63b4dd989d76c8d4d';
const sblUrl='https://raw.githubusercontent.com/Faithlife/SBLGNT/'+sblgntSha+'/data/sblgnt/text/Luke.txt';

const stepRes=await fetch(stepUrl);
if(!stepRes.ok)throw new Error('STEPBible download failed: '+stepRes.status);
const stepLines=(await stepRes.text()).split(/\r?\n/);
await fs.mkdir('authoring',{recursive:true});
const sblRes=await fetch(sblUrl);
if(!sblRes.ok)throw new Error('Luke SBLGNT download failed: '+sblRes.status);
const pattern=/(?:^|\t)(?:Luk|Luke|Lk)[ ._-]?(\d+)[.:](\d+)/i;
const matched=stepLines.filter(line=>pattern.test(line));
await fs.writeFile('authoring/step-luke.tsv',['# STEPBible TAGNT extraction','# source: STEPBible/STEPBible-Data@'+upstreamSha,'# book: Luke',...matched].join('\n')+'\n');
const sblLines=(await sblRes.text()).split(/\r?\n/).filter(line=>/^Luke \d+:\d+\t/.test(line));
await fs.writeFile('authoring/sblgnt-luke.txt',['# SBLGNT extraction','# source: Faithlife/SBLGNT@'+sblgntSha,'# book: Luke',...sblLines].join('\n')+'\n');
console.log('Matched',sblLines.length,'SBLGNT verses and',matched.length,'TAGNT lines for Luke');
if(sblLines.length!==1149)throw new Error('Unexpected SBLGNT verse count for Luke: '+sblLines.length);
if(matched.length<10000)throw new Error('Too few TAGNT lines for Luke');
