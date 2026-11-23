# post-repair corpus rescan
# full-corpus bidirectional lexical sanity
import json,collections
from pathlib import Path
from alignment_repair import BOOKS,norm,atoms,GLUE,sim,literal_terms_by_id,semantic_terms

MEANINGLESS=GLUE|{'very','also','even','still','now','then','only','indeed','surely','therefore','thus','yet','one','thing','things'}

def content_atoms(text):
 return [w for w in atoms(text) if w and w not in MEANINGLESS]

def source_score(word,g,id,litmap):
 return max([sim(word,s) for s in semantic_terms(g,id,litmap)] or [0])

stats=collections.defaultdict(collections.Counter)
examples=[]

for slug in BOOKS:
 for path in sorted((Path('data')/slug).glob('[0-9][0-9].json')):
  d=json.loads(path.read_text(encoding='utf8'))
  for v in d.get('verses',[]):
   A=v.get('alignment',{})
   G=A.get('greek',[]); D=A.get('dgt',[]); L=A.get('literal',[])
   if not G or not D: continue
   src={id:g for g in G for id in g.get('ids',[])}
   litmap=literal_terms_by_id(L)
   back=collections.defaultdict(list)
   for x in D:
    for id in x.get('ids',[]): back[id].append(x)

   # English -> Greek: every meaningful English phrase should have a plausible source.
   for x in D:
    words=content_atoms(x.get('text',''))
    if not words: continue
    ids=[id for id in x.get('ids',[]) if id in src]
    if not ids:
     stats[slug]['unlinked_content_item']+=1
     if len(examples)<350: examples.append((slug,path.stem,v['v'],'UNLINKED_CONTENT',x.get('text','')))
     continue
    # A multiword DGT item may legitimately distribute its meaning across several linked Greek IDs.
    matched=[w for w in words if max([source_score(w,src[id],id,litmap) for id in ids] or [0])>=8]
    phrase_ok=x.get('confidence')=='phrase-repaired'
    if not matched and not phrase_ok:
     stats[slug]['implausible_link_item']+=1
     if len(examples)<350:
      examples.append((slug,path.stem,v['v'],'IMPLAUSIBLE_LINK',x.get('text',''),[(id,src[id].get('text'),src[id].get('gloss'),sorted(litmap.get(id,set()))) for id in ids]))

   # Greek -> English: every source lexical concept should have a meaningful realization.
   for id,g in src.items():
    terms={w for w in semantic_terms(g,id,litmap) if w}
    lexical_terms={w for w in terms if w not in MEANINGLESS}
    if not lexical_terms: continue
    eng=back.get(id,[])
    if not eng:
     stats[slug]['greek_unrepresented']+=1
     if len(examples)<350: examples.append((slug,path.stem,v['v'],'GREEK_UNREPRESENTED',g.get('text'),g.get('gloss'),sorted(lexical_terms)))
     continue
    ewords=[]
    for x in eng: ewords.extend(content_atoms(x.get('text','')))
    if not ewords:
     stats[slug]['greek_only_stopwords']+=1
     if len(examples)<350:
      examples.append((slug,path.stem,v['v'],'GREEK_ONLY_STOPWORDS',g.get('text'),g.get('gloss'),[x.get('text') for x in eng],sorted(lexical_terms)))
     continue
    best=max((sim(e,s) for e in ewords for s in lexical_terms),default=0)
    phrase_ok=any(x.get('confidence')=='phrase-repaired' for x in eng)
    if best<8 and not phrase_ok:
     stats[slug]['greek_weak_realization']+=1
     if len(examples)<350:
      examples.append((slug,path.stem,v['v'],'GREEK_WEAK_REALIZATION',g.get('text'),g.get('gloss'),[x.get('text') for x in eng],sorted(lexical_terms)))

for slug in BOOKS:
 print(slug,dict(stats[slug]))
print('TOTALS',dict(sum((stats[s] for s in BOOKS),collections.Counter())))
print('EXAMPLES')
for e in examples: print(e)
