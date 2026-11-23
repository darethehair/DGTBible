import json
from pathlib import Path
d=json.loads((Path('data')/'jude'/'01.json').read_text(encoding='utf8'))
linked=unlinked=0
assert len(d['verses'])==25,len(d['verses'])
for v in d['verses']:
 assert v['greek'] and v['dgt'] and v['literal']
 ids={x['ids'][0] for x in v['alignment']['greek']}
 for x in v['alignment']['dgt']:
  if x.get('ids'):linked+=1
  else:unlinked+=1
  assert all(i in ids for i in x.get('ids',[])),f"dangling alignment Jude 1:{v['v']}"
pct=linked/(linked+unlinked)*100
assert pct>=75,pct
print(f'Jude audit clean: 25 verses; {pct:.1f}% high-confidence DGT token coverage.')
