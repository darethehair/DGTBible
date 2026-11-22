import fs from 'node:fs/promises';

const start=Number(process.env.START_CHAPTER||4);
const end=Number(process.env.END_CHAPTER||10);
const stepPath='authoring/step-john-'+String(start).padStart(2,'0')+'-'+String(end).padStart(2,'0')+'.tsv';
const sblPath='authoring/sblgnt-john-'+String(start).padStart(2,'0')+'-'+String(end).padStart(2,'0')+'.txt';

const norm=s=>String(s||'')
  .normalize('NFD').replace(/[\u0300-\u036f]/g,'')
  .toLowerCase().replace(/[ʼ᾽’']/g,'')
  .replace(/[^\p{L}\p{N}]/gu,'');

function editOne(a,b){
  if(Math.abs(a.length-b.length)>1)return false;
  if(a.length===b.length){
    let d=0;for(let i=0;i<a.length;i++)if(a[i]!==b[i]&&++d>1)return false;
    return d<=1;
  }
  const [long,short]=a.length>b.length?[a,b]:[b,a];
  for(let i=0;i<long.length;i++)if(long.slice(0,i)+long.slice(i+1)===short)return true;
  return false;
}
function equiv(a,b){
  a=norm(a);b=norm(b);
  if(!a||!b)return false;
  if(a===b)return true;
  if(a.endsWith('ν')&&a.slice(0,-1)===b)return true;
  if(b.endsWith('ν')&&b.slice(0,-1)===a)return true;
  if(a.endsWith('α')&&a.slice(0,-1)===b)return true;
  if(b.endsWith('α')&&b.slice(0,-1)===a)return true;
  return editOne(a,b);
}
function lcs(A,B){
  const m=A.length,n=B.length;
  const dp=Array.from({length:m+1},()=>Array(n+1).fill(0));
  for(let i=m-1;i>=0;i--)for(let j=n-1;j>=0;j--)
    dp[i][j]=equiv(A[i],B[j])?1+dp[i+1][j+1]:Math.max(dp[i+1][j],dp[i][j+1]);
  const pairs=[];let i=0,j=0;
  while(i<m&&j<n){
    if(equiv(A[i],B[j])&&dp[i][j]===1+dp[i+1][j+1]){pairs.push([i,j]);i++;j++}
    else if(dp[i+1][j]>=dp[i][j+1])i++;else j++;
  }
  return pairs;
}
function robustPairs(A,B){
  const pairs=lcs(A,B), usedA=new Set(pairs.map(x=>x[0])), usedB=new Set(pairs.map(x=>x[1]));
  for(let i=0;i<A.length;i++){
    if(usedA.has(i))continue;
    const candidates=[];
    for(let j=0;j<B.length;j++)if(!usedB.has(j)&&equiv(A[i],B[j]))candidates.push(j);
    if(!candidates.length)continue;
    const j=candidates.sort((x,y)=>Math.abs(i/A.length-x/B.length)-Math.abs(i/A.length-y/B.length))[0];
    pairs.push([i,j]);usedA.add(i);usedB.add(j);
  }
  return pairs.sort((a,b)=>a[0]-b[0]);
}

const stepText=await fs.readFile(stepPath,'utf8');
const sblText=await fs.readFile(sblPath,'utf8');
const step=new Map();
for(const line of stepText.split(/\r?\n/)){
  const m=line.match(/^Jhn\.(\d+)\.(\d+)#(\d+)=/);
  if(!m)continue;
  const cols=line.split('\t');
  const key=m[1]+':'+m[2];
  const original=(cols[1]||'').split(' (',1)[0];
  const row={index:Number(m[3]),original,gloss:cols[2]||'',tag:cols[3]||'',lemma:cols[4]||'',editions:cols[5]||''};
  if(!step.has(key))step.set(key,[]);
  step.get(key).push(row);
}
const verses=[];
for(const line of sblText.split(/\r?\n/)){
  const m=line.match(/^John (\d+):(\d+)\t(.*)$/);
  if(!m)continue;
  const ch=Number(m[1]),v=Number(m[2]);
  const greek=m[3].trim().replace(/[⸀⸂⸃]/g,'');
  const toks=greek.split(/\s+/);
  const rows=step.get(ch+':'+v)||[];
  const pairs=robustPairs(toks,rows.map(x=>x.original));
  const matched=new Set(pairs.map(x=>x[0]));
  const unmatchedSbl=toks.filter((_,i)=>!matched.has(i));
  const usedStep=new Set(pairs.map(x=>x[1]));
  const unmatchedTagnt=rows.filter((_,i)=>!usedStep.has(i)).map(x=>x.original);
  verses.push({ref:'John '+ch+':'+v,sblTokens:toks.length,tagntRows:rows.length,matched:pairs.length,unmatchedSbl,unmatchedTagnt});
}
const exceptions=verses.filter(v=>v.unmatchedSbl.length);
const summary={
  range:'John '+start+'-'+end,
  verses:verses.length,
  fullyMatched:verses.length-exceptions.length,
  exceptions:exceptions.length,
  exceptionRefs:exceptions.map(x=>x.ref)
};
await fs.writeFile('authoring/john-'+String(start).padStart(2,'0')+'-'+String(end).padStart(2,'0')+'-preflight.json',JSON.stringify({summary,exceptions},null,2)+'\n');
await fs.writeFile('authoring/john-'+String(start).padStart(2,'0')+'-'+String(end).padStart(2,'0')+'-preflight.md',
  '# John '+start+'–'+end+' source preflight\n\n'+
  '- Verses: '+summary.verses+'\n- Fully auto-matched: '+summary.fullyMatched+'\n- Exceptions: '+summary.exceptions+'\n\n'+
  exceptions.map(x=>'## '+x.ref+'\n\n- Unmatched SBLGNT: '+JSON.stringify(x.unmatchedSbl)+'\n- Unmatched TAGNT: '+JSON.stringify(x.unmatchedTagnt)+'\n').join('\n')
);
console.log(JSON.stringify(summary,null,2));
if(exceptions.length>Math.max(20,verses.length*0.1))throw new Error('Too many source alignment exceptions; batch matcher needs review.');
