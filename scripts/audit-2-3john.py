import json
from pathlib import Path
for slug,name,expected in [('2john','2 John',13),('3john','3 John',15)]:
 d=json.loads((Path('data')/slug/'01.json').read_text(encoding='utf8'))
 linked=unlinked=0
 assert len(d['verses'])==expected,(name,len(d['verses']))
 for v in d['verses']:
  assert v['greek'] and v['dgt'] and v['literal']
  ids={x['ids'][0] for x in v['alignment']['greek']}
  for x in v['alignment']['dgt']:
   if x.get('ids'): linked+=1
   else: unlinked+=1
   assert all(i in ids for i in x.get('ids',[])),f"dangling alignment {name} 1:{v['v']}"
 pct=linked/(linked+unlinked)*100
 assert pct>=80,pct
 print(f'{name} audit clean: {expected} verses; {pct:.1f}% high-confidence DGT token coverage.')
