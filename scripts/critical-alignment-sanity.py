# post-review critical rescan
# full corpus critical scan
import json,collections,sys
from pathlib import Path
from alignment_repair import BOOKS,atoms,norm,GLUE,sim,literal_terms_by_id,semantic_terms,source_map

LOW=GLUE|{'very','also','even','still','now','then','only','indeed','surely','therefore','thus','yet'}

def cwords(text):
 return [w for w in atoms(text) if w and w not in LOW]

def sscore(words,g,id,litmap):
 terms=semantic_terms(g,id,litmap)
 return max((sim(w,t) for w in words for t in terms),default=0)

stats=collections.defaultdict(collections.Counter)
examples=[]
allow_path=Path('data/alignment-quality-allowlist.json')
allow=json.loads(allow_path.read_text(encoding='utf8')) if allow_path.exists() else {}
for slug in BOOKS:
 for path in sorted((Path('data')/slug).glob('[0-9][0-9].json')):
  d=json.loads(path.read_text(encoding='utf8'))
  for v in d.get('verses',[]):
   A=v.get('alignment',{}); G=A.get('greek',[]); D=A.get('dgt',[]); L=A.get('literal',[])
   if not G or not D: continue
   src,pos=source_map(G); litmap=literal_terms_by_id(L)
   for i,x in enumerate(D):
    words=cwords(x.get('text',''))
    if not words: continue
    linked=[id for id in x.get('ids',[]) if id in src]
    current=max((sscore(words,src[id],id,litmap) for id in linked),default=0)
    candidates=[]
    for id,g in src.items():
     z=sscore(words,g,id,litmap)
     if z>=8:
      rel=i/max(1,len(D)-1); sp=pos[id]/max(1,len(G)-1)
      candidates.append((z,abs(rel-sp),id,g.get('text',''),g.get('gloss','')))
    if not candidates: continue
    bestz=max(z for z,_,_,_,_ in candidates)
    top=[c for c in candidates if c[0]==bestz]
    if len(top)!=1: continue
    z,dist,best,gt,gl=top[0]
    if best in linked: continue
    if not linked:
     if dist<=0.35:
      key=f"{slug}.{path.stem}.{v['v']}|{x.get('text','')}"
      if key in allow:
       stats[slug]['reviewed_unlinked']+=1
      else:
       stats[slug]['unique_unlinked']+=1
       examples.append((slug,path.stem,v['v'],'UNLINKED',x.get('text',''),best,gt,gl,z,round(dist,3)))
    elif current<8 and dist<=0.35 and x.get('confidence') not in {'phrase-repaired','quality-scan','authored'}:
     stats[slug]['unique_wrong_link']+=1
     examples.append((slug,path.stem,v['v'],'WRONG_LINK',x.get('text',''),linked,best,gt,gl,z,round(dist,3)))

for slug in BOOKS: print(slug,dict(stats[slug]))
print('TOTALS',dict(sum((stats[s] for s in BOOKS),collections.Counter())))
print('CANDIDATES')
for e in examples: print(e)
unreviewed=sum(stats[s]['unique_unlinked']+stats[s]['unique_wrong_link'] for s in BOOKS)
if unreviewed:
 print(f'CRITICAL SANITY FAILED: {unreviewed} unreviewed candidate(s)')
 sys.exit(1)
print('CRITICAL SANITY CLEAN')
