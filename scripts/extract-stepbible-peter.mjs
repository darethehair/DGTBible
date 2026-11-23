import fs from 'node:fs/promises';

const upstreamSha='5de0a47f35f0fc13dfe1430d104e5db8a4285f9c';
const stepFile='Translators Amalgamated OT+NT/TAGNT Act-Rev - Translators Amalgamated Greek NT - STEPBible.org CC-BY.txt';
const stepUrl='https://raw.githubusercontent.com/STEPBible/STEPBible-Data/'+upstreamSha+'/'+stepFile.split('/').map(encodeURIComponent).join('/');
const sblgntSha='d7f35adca9ec410e1d1499c63b4dd989d76c8d4d';
const books=[
 {slug:'1peter',name:'1 Peter',step:'1Pe',sbl:'1Pet',chapters:5,verses:105},
 {slug:'2peter',name:'2 Peter',step:'2Pe',sbl:'2Pet',chapters:3,verses:61}
];
const stepRes=await fetch(stepUrl);
if(!stepRes.ok)throw new Error('STEPBible download failed: '+stepRes.status);
const stepLines=(await stepRes.text()).split(/\r?\n/);
await fs.mkdir('authoring',{recursive:true});
for(const b of books){
 const sblUrl='https://raw.githubusercontent.com/Faithlife/SBLGNT/'+sblgntSha+'/data/sblgnt/text/'+b.sbl+'.txt';
 const sblRes=await fetch(sblUrl);
 if(!sblRes.ok)throw new Error(b.name+' SBLGNT download failed: '+sblRes.status);
 const pattern=new RegExp('(?:^|\\t)'+b.step+'[ ._-]?(\\d+)[.:](\\d+)','i');
 const matched=stepLines.filter(line=>pattern.test(line));
 await fs.writeFile('authoring/step-'+b.slug+'.tsv',['# STEPBible TAGNT extraction','# source: STEPBible/STEPBible-Data@'+upstreamSha,'# book: '+b.name,...matched].join('\n')+'\n');
 const sblLines=(await sblRes.text()).split(/\r?\n/).filter(line=>new RegExp('^'+b.sbl+' \\d+:\\d+\\t').test(line));
 await fs.writeFile('authoring/sblgnt-'+b.slug+'.txt',['# SBLGNT extraction','# source: Faithlife/SBLGNT@'+sblgntSha,'# book: '+b.name,...sblLines].join('\n')+'\n');
 console.log('Matched',sblLines.length,'SBLGNT verses and',matched.length,'TAGNT lines for',b.name);
 if(sblLines.length!==b.verses)throw new Error('Unexpected SBLGNT verse count for '+b.name+': '+sblLines.length);
 if(matched.length<b.verses*8)throw new Error('Too few TAGNT lines for '+b.name);
}
