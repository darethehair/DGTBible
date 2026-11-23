import json,os
from pathlib import Path
start=int(os.environ.get('START_CHAPTER','1'));end=int(os.environ.get('END_CHAPTER','1'))
linked=unlinked=count=0
for ch in range(start,end+1):
 d=json.loads((Path('data')/'galatians'/f'{ch:02}.json').read_text(encoding='utf8'))
 count+=len(d['verses'])
 for v in d['verses']:
  assert v['greek'] and v['dgt'] and v['literal']
  ids={x['ids'][0] for x in v['alignment']['greek']}
  for x in v['alignment']['dgt']:
   if x.get('ids') or x.get('phraseIds'):linked+=1
   else:unlinked+=1
   assert all(i in ids for i in (x.get('ids',[])+x.get('phraseIds',[]))),f'dangling alignment Galatians {ch}:{v["v"]}'
pct=linked/(linked+unlinked)*100
assert pct>=75,pct
print(f'Galatians {start}-{end} audit clean: {count} verses; {pct:.1f}% authored DGT token coverage.')
