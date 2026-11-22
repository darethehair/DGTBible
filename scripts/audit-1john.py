import json,re
from pathlib import Path
D=Path('data/1john')
total=linked=unlinked=0
for ch in range(1,6):
 d=json.loads((D/f'{ch:02}.json').read_text(encoding='utf8'))
 for v in d['verses']:
  total+=1
  assert v['greek'] and v['dgt'] and v['literal']
  for x in v['alignment']['dgt']:
   if x.get('ids'):linked+=1
   else:unlinked+=1
  ids={x['ids'][0] for x in v['alignment']['greek']}
  for x in v['alignment']['dgt']:
   assert all(i in ids for i in x.get('ids',[])),f"dangling alignment 1 John {ch}:{v['v']}"
assert total==105,total
pct=linked/(linked+unlinked)*100
assert pct>=80,pct
print(f'1 John audit clean: {total} verses; {pct:.1f}% high-confidence DGT token coverage.')
