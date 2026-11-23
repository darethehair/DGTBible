import json
from pathlib import Path
for slug,name,chapters,expected in [('1peter','1 Peter',5,105),('2peter','2 Peter',3,61)]:
 linked=unlinked=count=0
 for ch in range(1,chapters+1):
  d=json.loads((Path('data')/slug/f'{ch:02}.json').read_text(encoding='utf8'))
  count+=len(d['verses'])
  for v in d['verses']:
   assert v['greek'] and v['dgt'] and v['literal']
   ids={x['ids'][0] for x in v['alignment']['greek']}
   for x in v['alignment']['dgt']:
    if x.get('ids'):linked+=1
    else:unlinked+=1
    assert all(i in ids for i in x.get('ids',[])),f'dangling alignment {name} {ch}:{v["v"]}'
 assert count==expected,(name,count)
 pct=linked/(linked+unlinked)*100
 assert pct>=75,(name,pct)
 print(f'{name} audit clean: {expected} verses; {pct:.1f}% high-confidence DGT token coverage.')
