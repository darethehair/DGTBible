import json,collections
from pathlib import Path
from alignment_repair import norm,GLUE,token_semantic_score,semantic_tokens_for_greek

BOOKS=['john','1john','2john','3john','jude','1peter','2peter','james','hebrews','romans']
MEANINGLESS=GLUE|{'very','also','even','still','now','then','only','indeed','surely','therefore','thus','yet'}

stats=collections.defaultdict(collections.Counter)
examples=[]

for slug in BOOKS:
 for path in sorted((Path('data')/slug).glob('[0-9][0-9].json')):
  d=json.loads(path.read_text(encoding='utf8'))
  for v in d.get('verses',[]):
   A=v.get('alignment',{})
   G=A.get('greek',[]); D=A.get('dgt',[])
   if not G or not D: continue
   src={id:g for g in G for id in g.get('ids',[])}
   back=collections.defaultdict(list)
   for x in D:
    for id in x.get('ids',[]): back[id].append(x)

   # English -> Greek sanity.
   for x in D:
    w=norm(x.get('text',''))
    if not w or w in MEANINGLESS: continue
    ids=[id for id in x.get('ids',[]) if id in src]
    if not ids:
     stats[slug]['unlinked_content']+=1
     if len(examples)<250: examples.append((slug,path.stem,v['v'],'UNLINKED_CONTENT',x.get('text','')))
     continue
    best=max(token_semantic_score(w,src[id]) for id in ids)
    # Phrase-repaired tokens are allowed to be individually non-similar if sibling words share same id.
    phrase_ok=x.get('confidence')=='phrase-repaired'
    if best==0 and not phrase_ok:
     stats[slug]['lexically_implausible_link']+=1
     if len(examples)<250:
      examples.append((slug,path.stem,v['v'],'IMPLAUSIBLE_LINK',x.get('text',''),[(id,src[id].get('text'),src[id].get('gloss')) for id in ids]))

   # Greek -> English sanity.
   for id,g in src.items():
    # Skip source items whose gloss is only function-word material.
    gwords={norm(z) for z in semantic_tokens_for_greek(g) if norm(z)}
    lexical=any(z not in MEANINGLESS for z in gwords)
    if not lexical: continue
    eng=back.get(id,[])
    if not eng:
     stats[slug]['greek_unrepresented']+=1
     if len(examples)<250: examples.append((slug,path.stem,v['v'],'GREEK_UNREPRESENTED',g.get('text'),g.get('gloss')))
     continue
    meaningful=[x for x in eng if norm(x.get('text','')) not in MEANINGLESS]
    if not meaningful:
     stats[slug]['greek_only_stopwords']+=1
     if len(examples)<250:
      examples.append((slug,path.stem,v['v'],'GREEK_ONLY_STOPWORDS',g.get('text'),g.get('gloss'),[x.get('text') for x in eng]))
     continue
    best=max(token_semantic_score(norm(x.get('text','')),g) for x in meaningful)
    phrase_ok=any(x.get('confidence')=='phrase-repaired' for x in meaningful)
    if best==0 and not phrase_ok:
     stats[slug]['greek_weak_realization']+=1
     if len(examples)<250:
      examples.append((slug,path.stem,v['v'],'GREEK_WEAK_REALIZATION',g.get('text'),g.get('gloss'),[x.get('text') for x in meaningful]))

for slug in BOOKS:
 print(slug,dict(stats[slug]))
print('TOTALS',dict(sum((stats[s] for s in BOOKS),collections.Counter())))
print('EXAMPLES')
for e in examples: print(e)
