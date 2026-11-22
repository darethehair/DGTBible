import re,json,glob,collections,unicodedata
from pathlib import Path
from john_batch_common import map_words,clean
from john_batch_dgt import align
R=Path('.');A=R/'authoring';J=R/'data/john';S=R/'data/sources'
sbl={}
for line in (A/'sblgnt-john-04-10.txt').read_text(encoding='utf8').splitlines():
 m=re.match(r'^John (\d+):(\d+)\t(.*)$',line)
 if m:sbl[(int(m[1]),int(m[2]))]=m[3].strip().replace('⸀','').replace('⸂','').replace('⸃','')
step=collections.defaultdict(list)
for line in (A/'step-john-04-10.tsv').read_text(encoding='utf8').splitlines():
 m=re.match(r'^Jhn\.(\d+)\.(\d+)#(\d+)=([^\t]*)\t([^\t]*)\t([^\t]*)\t([^\t]*)\t([^\t]*)\t([^\t]*)',line)
 if not m:continue
 f=m[5];q=re.match(r'(.+?)\s+\(([^()]*)\)\s*$',f);o=(q.group(1) if q else f).strip();t=(q.group(2) if q else '')
 tag=m[7];a,b=(tag.split('=',1)+[''])[:2] if '=' in tag else (tag,'')
 step[(int(m[1]),int(m[2]))].append(dict(idx=int(m[3]),original=o,translit=t,gloss=m[6],strongs=a,morph=b))
for k in step:step[k].sort(key=lambda x:x['idx'])
dgt={}
for ch in range(4,11):
 for p in sorted(glob.glob(f'data/authoring/john-{ch:02}*-dgt.tsv')):
  for line in Path(p).read_text(encoding='utf8').splitlines():
   if line.strip():
    v,t=line.split('\t',1);dgt[(ch,int(v))]=t
notes={(5,2):['SBLGNT and TAGNT have different place-name spellings here; the displayed Greek follows SBLGNT.'],(7,53):['John 7:53–8:11 is bracketed in SBLGNT because of its well-known textual history. It is retained because it is present in the SBLGNT source.'],(8,1):['John 7:53–8:11 is bracketed in SBLGNT because of its well-known textual history. DGT follows the displayed SBLGNT text.'],(8,3):['SBLGNT and TAGNT differ in wording form here; the alignment follows SBLGNT.'],(8,8):['SBLGNT uses two words for “stooping down” where TAGNT has a compound form; the alignment follows SBLGNT.'],(8,9):['SBLGNT and TAGNT differ in wording near the end of this verse; DGT follows SBLGNT.'],(8,11):['SBLGNT has a shorter wording here than the TAGNT variant data; DGT follows SBLGNT.']}
total=linked=unlinked=0
for ch in range(4,11):
 vs=[];sv=[]
 for v in sorted(x for c,x in sbl if c==ch):
  if (ch,v) not in dgt:raise SystemExit(f'missing DGT John {ch}:{v}')
  greek=sbl[(ch,v)];src=map_words(ch,v,greek,step[(ch,v)]);ga=[];ta=[];la=[]
  for i,x in enumerate(src):
   af='' if i==len(src)-1 else ' ';g={'text':x['text'],'after':af,'ids':[x['id']]}
   for k in ['gloss','strongs','morph']:
    if x[k]:g[k]=x[k]
   ga.append(g);ta.append({'text':x['translit'],'after':af,'ids':[x['id']]});la.append({'text':x['gloss'] or x['text'],'after':af,'ids':[x['id']]})
  lit=''.join(x['text']+x['after'] for x in la);da=align(dgt[(ch,v)],src)
  linked+=sum(bool(x['ids']) for x in da);unlinked+=sum(not x['ids'] for x in da);total+=1
  vs.append({'v':v,'greek':greek,'literal':lit,'dgt':dgt[(ch,v)],'notes':notes.get((ch,v),[]),'alignment':{'greek':ga,'translit':ta,'literal':la,'dgt':da}})
  sv.append({'ref':f'Jhn.{ch}.{v}','book':'JHN','chapter':str(ch),'verse':str(v),'testament':'NT','words':[{'original':x['text'],'translit':x['translit'],'strongs':x['strongs'],'morph':x['morph'],'gloss':x['gloss'],'synthetic':x.get('synthetic',False)} for x in src]})
 (J/f'{ch:02}.json').write_text(json.dumps({'book':'John','chapter':ch,'greekSource':'SBLGNT','verses':vs},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 (S/f'step-john-{ch:02}.json').write_text(json.dumps({'source':'STEPBible TAGNT aligned to SBLGNT','upstream':'STEPBible/STEPBible-Data@5de0a47f35f0fc13dfe1430d104e5db8a4285f9c','mirror':'direct pinned upstream extraction','license':'CC BY 4.0','sblgnt':'Faithlife/SBLGNT@d7f35adca9ec410e1d1499c63b4dd989d76c8d4d','verses':sv},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
if total!=366:raise SystemExit(f'expected 366 verses, got {total}')
pct=linked/(linked+unlinked)*100
if pct<80:raise SystemExit(f'high-confidence link coverage too low: {pct:.1f}%')
print(f'Generated {total} verses; high-confidence DGT link coverage {pct:.1f}% ({linked} linked, {unlinked} deliberately unlinked).')
