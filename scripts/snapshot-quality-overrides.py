# capture current reviewed corpus mappings
import json
from pathlib import Path

BOOKS=['john','1john','2john','3john','jude','1peter','2peter','james','hebrews','romans','1corinthians']
out={}
for slug in BOOKS:
 for path in sorted((Path('data')/slug).glob('[0-9][0-9].json')):
  d=json.loads(path.read_text(encoding='utf8'))
  ch=int(path.stem)
  for v in d.get('verses',[]):
   for i,x in enumerate(v.get('alignment',{}).get('dgt',[])):
    if x.get('confidence')=='quality-scan':
     key=f'{slug}.{ch}.{v["v"]}.{i}'
     out[key]={'text':x.get('text',''),'ids':x.get('ids',[])}
Path('data/alignment-quality-overrides.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Snapshotted {len(out)} reviewed quality-scan token overrides.')
