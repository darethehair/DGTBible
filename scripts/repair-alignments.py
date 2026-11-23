# full-corpus quality repair
# corpus-wide context-aware alignment repair
import json,collections,sys
from pathlib import Path
from alignment_repair import BOOKS,repair_verse

summary=collections.Counter(); examples=[]
targets=sys.argv[1:] or BOOKS
for slug in targets:
 for path in sorted((Path('data')/slug).glob('[0-9][0-9].json')):
  d=json.loads(path.read_text(encoding='utf8')); dirty=False
  for v in d.get('verses',[]):
   A=v.get('alignment',{}); D=A.get('dgt',[]); G=A.get('greek',[]); L=A.get('literal',[])
   if not D or not G: continue
   changes=repair_verse(D,G,L)
   if changes:
    dirty=True; summary[slug]+=len(changes)
    for ch in changes[:5]:
     if len(examples)<160: examples.append((slug,path.stem,v['v'],ch))
  if dirty:
   path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
for slug in targets: print(f'{slug}: {summary[slug]} alignment repairs')
print('TOTAL',sum(summary.values()))
for x in examples: print(x)
