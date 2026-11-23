# Report every unlinked meaningful DGT token, even when no lexical candidate is known.
import json,collections
from pathlib import Path
from alignment_repair import BOOKS,atoms,norm,GLUE,source_map,literal_terms_by_id,semantic_terms,sim

LOW=GLUE|{'very','also','even','still','now','then','only','indeed','surely','therefore','thus','yet'}
allow_path=Path('data/alignment-quality-allowlist.json')
allow=json.loads(allow_path.read_text(encoding='utf8')) if allow_path.exists() else {}

def content_words(text):
 return [w for w in atoms(text) if w and w not in LOW]

def score(words,g,id,litmap):
 terms=semantic_terms(g,id,litmap)
 return max((sim(w,t) for w in words for t in terms),default=0)

rows=[]
stats=collections.Counter()
for slug in BOOKS:
 for path in sorted((Path('data')/slug).glob('[0-9][0-9].json')):
  d=json.loads(path.read_text(encoding='utf8'))
  for v in d.get('verses',[]):
   A=v.get('alignment',{}); G=A.get('greek',[]); D=A.get('dgt',[]); L=A.get('literal',[])
   if not G or not D: continue
   src,pos=source_map(G); litmap=literal_terms_by_id(L)
   for i,x in enumerate(D):
    if x.get('ids'): continue
    words=content_words(x.get('text',''))
    if not words: continue
    key=f"{slug}.{path.stem}.{v['v']}|{x.get('text','')}"
    if key in allow:
     stats['allowlisted']+=1; continue
    rel=i/max(1,len(D)-1)
    candidates=[]
    for id,g in src.items():
     z=score(words,g,id,litmap)
     sp=pos[id]/max(1,len(G)-1)
     candidates.append((z,abs(rel-sp),id,g.get('text',''),g.get('gloss','')))
    candidates.sort(key=lambda c:(-c[0],c[1]))
    lexical=[c for c in candidates if c[0]>=8]
    nearby=sorted(candidates,key=lambda c:c[1])[:4]
    kind='LEXICAL' if lexical else 'ORPHAN'
    stats[kind.lower()]+=1
    rows.append({
      'book':slug,'chapter':int(path.stem),'verse':v['v'],'index':i,'token':x.get('text',''),
      'kind':kind,'reason':x.get('reason',''),'dgt':v.get('dgt',''),'greek':v.get('greek',''),
      'lexical':lexical[:4],'nearby':nearby
    })

print('UNLINKED CONTENT SUMMARY',dict(stats))
for r in rows:
 print(json.dumps(r,ensure_ascii=False))
print('TOTAL_UNREVIEWED',len(rows))
