# corpus gate rerun after born-aligned 1 Corinthians 7-8
# post-structural-repair rescan: Find meaningful Greek source tokens that have no DGT token linked to them.
import json,collections
from pathlib import Path
from alignment_repair import BOOKS,atoms,norm,GLUE,source_map,literal_terms_by_id,semantic_terms

LOW=GLUE|{'very','also','even','still','now','then','only','indeed','surely','therefore','thus','yet'}
stats=collections.Counter(); rows=[]
for slug in BOOKS:
 for path in sorted((Path('data')/slug).glob('[0-9][0-9].json')):
  d=json.loads(path.read_text(encoding='utf8'))
  for v in d.get('verses',[]):
   A=v.get('alignment',{}); G=A.get('greek',[]); D=A.get('dgt',[]); L=A.get('literal',[])
   if not G or not D: continue
   src,pos=source_map(G); litmap=literal_terms_by_id(L)
   used={id for x in D for id in x.get('ids',[])}
   unlinked=[(i,x) for i,x in enumerate(D) if not x.get('ids') and any(w not in LOW for w in atoms(x.get('text','')))]
   for id,g in src.items():
    if id in used: continue
    terms=[w for w in semantic_terms(g,id,litmap) if w not in LOW]
    if not terms: continue
    p=pos[id]
    # nearest unlinked English content tokens by relative position
    cand=[]
    for i,x in unlinked:
     dist=abs(i/max(1,len(D)-1)-p/max(1,len(G)-1))
     cand.append((dist,i,x.get('text',''),x.get('reason','')))
    cand.sort()
    rows.append({
      'book':slug,'chapter':int(path.stem),'verse':v['v'],'source_id':id,
      'greek':g.get('text',''),'gloss':g.get('gloss',''),'terms':terms,
      'nearest_unlinked':cand[:5],'dgt':v.get('dgt','')
    })
    stats[slug]+=1
print('UNUSED MEANINGFUL GREEK SUMMARY',dict(stats),'TOTAL',sum(stats.values()))
for r in rows: print(json.dumps(r,ensure_ascii=False))
