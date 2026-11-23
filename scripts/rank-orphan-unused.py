# refreshed after second ranked semantic pass — Rank non-lexical orphan English tokens against unused meaningful Greek tokens.
import json,collections
from pathlib import Path
from alignment_repair import BOOKS,atoms,GLUE,source_map,literal_terms_by_id,semantic_terms

LOW=GLUE|{'very','also','even','still','now','then','only','indeed','surely','therefore','thus','yet'}
allow_path=Path('data/alignment-quality-allowlist.json')
allow=json.loads(allow_path.read_text(encoding='utf8')) if allow_path.exists() else {}
rows=[]
for slug in BOOKS:
 for path in sorted((Path('data')/slug).glob('[0-9][0-9].json')):
  d=json.loads(path.read_text(encoding='utf8'))
  for v in d.get('verses',[]):
   A=v.get('alignment',{});G=A.get('greek',[]);D=A.get('dgt',[]);L=A.get('literal',[])
   if not G or not D:continue
   src,pos=source_map(G);litmap=literal_terms_by_id(L)
   used={id for x in D for id in x.get('ids',[])}
   unused=[]
   for id,g in src.items():
    if id in used:continue
    terms=[w for w in semantic_terms(g,id,litmap) if w not in LOW]
    if terms:unused.append((id,g,pos[id],terms))
   if not unused:continue
   for i,x in enumerate(D):
    if x.get('ids'):continue
    words=[w for w in atoms(x.get('text','')) if w not in LOW]
    if not words:continue
    key=f"{slug}.{path.stem}.{v['v']}|{x.get('text','')}"
    if key in allow:continue
    rel=i/max(1,len(D)-1)
    cand=[]
    for id,g,p,terms in unused:
      dist=abs(rel-p/max(1,len(G)-1))
      cand.append((dist,id,g.get('text',''),g.get('gloss',''),terms))
    cand.sort()
    if not cand:continue
    dist,id,gt,gl,terms=cand[0]
    rows.append((dist,{
      'book':slug,'chapter':int(path.stem),'verse':v['v'],'index':i,
      'token':x.get('text',''),'reason':x.get('reason',''),
      'nearest_unused':{'id':id,'greek':gt,'gloss':gl,'terms':terms,'distance':round(dist,4)},
      'dgt':v.get('dgt',''),'greek_text':v.get('greek','')
    }))
rows.sort(key=lambda z:z[0])
print('RANKED ORPHAN-UNUSED PAIRS',len(rows))
for _,r in rows:print(json.dumps(r,ensure_ascii=False))
