# post-cleanup baseline
import json
from pathlib import Path
BOOKS=['john','1john','2john','3john','jude','1peter','2peter','james','hebrews']
for slug in BOOKS:
 linked=unlinked=verses=0
 for path in sorted((Path('data')/slug).glob('[0-9][0-9].json')):
  d=json.loads(path.read_text(encoding='utf8'))
  verses+=len(d.get('verses',[]))
  for v in d.get('verses',[]):
   for x in v.get('alignment',{}).get('dgt',[]):
    if x.get('ids'):linked+=1
    else:unlinked+=1
 total=linked+unlinked
 pct=100*linked/total if total else 0
 print(f'{slug}\t{verses}\t{linked}\t{unlinked}\t{pct:.1f}%')
