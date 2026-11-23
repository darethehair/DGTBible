import re,json,collections
from pathlib import Path
from epistle_common import map_words
from john_batch_dgt import align

R=Path('.'); A=R/'authoring'; S=R/'data/sources'; S.mkdir(parents=True,exist_ok=True)
raw={}
for path in sorted((R/'data/authoring').glob('james-*-dgt.tsv')):
 for line in path.read_text(encoding='utf8').splitlines():
  if not line.strip():continue
  _,ref,t=line.split('\t',2);ch,v=map(int,ref.split(':'));raw[(ch,v)]=t
D=R/'data/james';D.mkdir(parents=True,exist_ok=True)
sbl={}
for line in (A/'sblgnt-james.txt').read_text(encoding='utf8').splitlines():
 m=re.match(r'^Jas (\d+):(\d+)\t(.*)$',line)
 if m:sbl[(int(m[1]),int(m[2]))]=m[3].strip().replace('⸀','').replace('⸂','').replace('⸃','')
if len(sbl)!=108:raise SystemExit(f'James: expected 108 verses, got {len(sbl)}')
step=collections.defaultdict(list)
for line in (A/'step-james.tsv').read_text(encoding='utf8').splitlines():
 m=re.match(r'^Jas\.(\d+)\.(\d+)(?:\[[^\]]+\])?#(\d+)=([^\t]*)\t([^\t]*)\t([^\t]*)\t([^\t]*)\t([^\t]*)\t([^\t]*)',line)
 if not m:continue
 f=m[5];q=re.match(r'(.+?)\s+\(([^()]*)\)\s*$',f);o=(q.group(1) if q else f).strip();t=(q.group(2) if q else '')
 tag=m[7];a,b=(tag.split('=',1)+[''])[:2] if '=' in tag else (tag,'')
 step[(int(m[1]),int(m[2]))].append(dict(idx=int(m[3]),original=o,translit=t,gloss=m[6],strongs=a,morph=b))
for k in step:step[k].sort(key=lambda x:x['idx'])
manifests=[];linked=unlinked=synthetic=0
for ch in range(1,6):
 vs=[];sv=[]
 for (cnum,v),greek in sorted(sbl.items()):
  if cnum!=ch:continue
  src=map_words(greek,step[(ch,v)]);synthetic+=sum(bool(x.get('synthetic')) for x in src)
  ga=[];ta=[];la=[]
  for i,x in enumerate(src):
   af='' if i==len(src)-1 else ' ';g={'text':x['text'],'after':af,'ids':[x['id']]}
   for k in ['gloss','strongs','morph']:
    if x[k]:g[k]=x[k]
   ga.append(g);ta.append({'text':x['translit'],'after':af,'ids':[x['id']]});la.append({'text':x['gloss'] or x['text'],'after':af,'ids':[x['id']]})
  dgt=raw[(ch,v)];da=align(dgt,src);linked+=sum(bool(x['ids']) for x in da);unlinked+=sum(not x['ids'] for x in da)
  lit=''.join(x['text']+x['after'] for x in la)
  vs.append({'v':v,'greek':greek,'literal':lit,'dgt':dgt,'notes':[],'alignment':{'greek':ga,'translit':ta,'literal':la,'dgt':da}})
  sv.append({'ref':f'Jas.{ch}.{v}','book':'JAS','chapter':str(ch),'verse':str(v),'testament':'NT','words':[{'original':x['text'],'translit':x['translit'],'strongs':x['strongs'],'morph':x['morph'],'gloss':x['gloss'],'synthetic':x.get('synthetic',False)} for x in src]})
 (D/f'{ch:02}.json').write_text(json.dumps({'book':'James','chapter':ch,'greekSource':'SBLGNT','verses':vs},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 (S/f'step-james-{ch:02}.json').write_text(json.dumps({'source':'STEPBible TAGNT aligned to SBLGNT','upstream':'STEPBible/STEPBible-Data@5de0a47f35f0fc13dfe1430d104e5db8a4285f9c','license':'CC BY 4.0','sblgnt':'Faithlife/SBLGNT@d7f35adca9ec410e1d1499c63b4dd989d76c8d4d','verses':sv},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 manifests.append({'chapter':ch,'file':f'{ch:02}.json','verses':len(vs)})
(D/'manifest.json').write_text(json.dumps({'book':'James','slug':'james','chapters':manifests},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
pct=linked/(linked+unlinked)*100
if pct<75:raise SystemExit(f'James: coverage too low {pct:.1f}%')
if synthetic>20:raise SystemExit(f'James: too many synthetic source tokens {synthetic}')
print(f'Generated James: 108 verses; {pct:.1f}% DGT token coverage ({linked} linked, {unlinked} deliberately unlinked); {synthetic} synthetic source tokens.')
