import json,os,re,unicodedata,collections
from pathlib import Path
start=int(os.environ.get('START_CHAPTER','1'));end=int(os.environ.get('END_CHAPTER','1'))
def n(s):
 s=unicodedata.normalize('NFD',str(s)).lower()
 s=''.join(x for x in s if unicodedata.category(x)!='Mn')
 return re.sub(r'[^a-z0-9]','',s)
def atoms(s): return [n(x) for x in re.findall(r"[A-Za-z0-9]+",str(s)) if n(x)]

linked=unlinked=count=0
recoverable=[]
for ch in range(start,end+1):
 d=json.loads((Path('data')/'galatians'/f'{ch:02}.json').read_text(encoding='utf8'))
 count+=len(d['verses'])
 for v in d['verses']:
  assert v['greek'] and v['dgt'] and v['literal']
  ids={x['ids'][0] for x in v['alignment']['greek']}
  D=v['alignment']['dgt']; L=v['alignment']['literal']
  for x in D:
   if x.get('ids') or x.get('phraseIds'):linked+=1
   else:unlinked+=1
   assert all(i in ids for i in (x.get('ids',[])+x.get('phraseIds',[]))),f'dangling alignment Galatians {ch}:{v["v"]}'
  # If an unlinked DGT word occurs N times and the literal layer contains exactly
  # N source-linked occurrences of the same word, ordered pairing is deterministic.
  byword=collections.defaultdict(list)
  for i,x in enumerate(D):
   if not x.get('ids'):
    w=n(x.get('text',''))
    if w: byword[w].append(i)
  for w,idxs in byword.items():
   lids=[]
   for y in L:
    if w in atoms(y.get('text','')):
     lids.extend(y.get('ids',[]))
   lids=list(dict.fromkeys(lids))
   if lids and len(lids)==len(idxs):
    recoverable.append((ch,v['v'],w,len(idxs),lids))
pct=linked/(linked+unlinked)*100
assert pct>=75,pct
assert not recoverable, f'recoverable exact DGT links left unlinked: {recoverable[:20]}'
print(f'Galatians {start}-{end} audit clean: {count} verses; {pct:.1f}% authored DGT token coverage; 0 recoverable exact links left unlinked.')
