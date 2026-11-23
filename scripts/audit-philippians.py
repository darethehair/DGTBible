import json,os,re,unicodedata,collections
from pathlib import Path
start=int(os.environ.get('START_CHAPTER','1'));end=int(os.environ.get('END_CHAPTER','1'))
def n(s):
 s=unicodedata.normalize('NFD',str(s)).lower()
 s=''.join(x for x in s if unicodedata.category(x)!='Mn')
 return re.sub(r'[^a-z0-9]','',s)
def atoms(s): return [n(x) for x in re.findall(r"[A-Za-z0-9]+",str(s)) if n(x)]
def pk(w):
 groups={
  'he':{'he','him','his','himself'},
  'she':{'she','her','hers','herself'},
  'they':{'they','them','their','theirs','themselves'},
  'we':{'we','us','our','ours','ourselves'},
  'you':{'you','your','yours','yourself','yourselves'},
  'i':{'i','me','my','mine','myself'},
  'it':{'it','its','itself'},
 }
 w=n(w)
 if w in {'who','whom','whose','which'}:return 'relative'
 for k,vals in groups.items():
  if w in vals:return k
 return None

linked=unlinked=count=0
recoverable=[]
collisions=[]
synthetic_unlinked=[]
out_of_span=[]
recoverable_pronouns=[]
recoverable_relative_pronouns=[]
recoverable_context_relative=[]
recoverable_bundled_pronouns=[]
recoverable_positional=[]
EVANGEL_WORDS={'proclaim','proclaimed','preach','preached','good','news','gospel','evangelize','evangelized','evangelised'}
for ch in range(start,end+1):
 d=json.loads((Path('data')/'philippians'/f'{ch:02}.json').read_text(encoding='utf8'))
 count+=len(d['verses'])
 for v in d['verses']:
  assert v['greek'] and v['dgt'] and v['literal']
  ids={x['ids'][0] for x in v['alignment']['greek']}
  D=v['alignment']['dgt']; L=v['alignment']['literal']
  for x in D:
   if x.get('ids') or x.get('phraseIds'):linked+=1
   else:unlinked+=1
   if x.get('phraseIds') and any(i not in set(x.get('phraseIds',[])) for i in x.get('ids',[])):
    out_of_span.append((ch,v['v'],x.get('text',''),x.get('ids',[]),x.get('phraseIds',[]),x.get('confidence','')))
   assert all(i in ids for i in (x.get('ids',[])+x.get('phraseIds',[]))),f'dangling alignment Philippians {ch}:{v["v"]}'
  used_precise={i for x in D for i in x.get('ids',[])}
  for g in v['alignment']['greek']:
   gid=(g.get('ids') or [None])[0]
   if gid and gid.startswith('s') and gid not in used_precise:
    synthetic_unlinked.append((ch,v['v'],gid,g.get('text','')))
  # If an unlinked DGT word occurs N times and the literal layer contains exactly
  # N source-linked occurrences of the same word, ordered pairing is deterministic.
  byword=collections.defaultdict(list)
  for i,x in enumerate(D):
   if not x.get('ids'):
    w=n(x.get('text',''))
    if w: byword[w].append(i)
  # Same deterministic check for English pronoun-family variants.
  pd=collections.defaultdict(list)
  for i,x in enumerate(D):
   if not x.get('ids'):
    k=pk(x.get('text',''))
    if k:pd[k].append(i)
  usedp=collections.defaultdict(set)
  for x in D:
   k=pk(x.get('text',''))
   if k and x.get('ids'):
    usedp[k].update(x.get('ids',[]))
  for k,idxs in pd.items():
   if k=='relative':continue
   lids=[]
   for y in L:
    if k in {pk(t) for t in re.findall(r"[A-Za-z0-9]+",y.get('text','')) if pk(t)}:
     for id in y.get('ids',[]):
      if id not in usedp[k]:lids.append(id)
   lids=list(dict.fromkeys(lids))
   if lids and len(lids)==len(idxs):
    recoverable_pronouns.append((ch,v['v'],k,len(idxs),lids))
  # Contextual "in whom" -> "in him" style bridge: if a literal relative
  # pronoun follows a precisely aligned preposition and DGT has an unlinked
  # personal pronoun immediately after the same source-aligned preposition,
  # that bridge is deterministically recoverable.
  usedids={id for x in D for id in x.get('ids',[])}
  for li,y in enumerate(L):
   ykeys=[pk(t) for t in re.findall(r"[A-Za-z0-9]+",y.get('text','')) if pk(t)]
   if 'relative' not in ykeys or li==0:continue
   relids=[id for id in y.get('ids',[]) if id not in usedids]
   if len(relids)!=1:continue
   prev=set(L[li-1].get('ids',[]))
   for i in range(1,len(D)):
    if D[i].get('ids') or pk(D[i].get('text','')) not in {'he','she','they','it'}:continue
    if prev & set(D[i-1].get('ids',[])):
     recoverable_context_relative.append((ch,v['v'],D[i].get('text',''),relids[0]))
     break

  lit_terms=collections.defaultdict(set)
  for y in L:
   terms=[n(t) for t in re.findall(r"[A-Za-z0-9]+",y.get('text',''))]
   for id in y.get('ids',[]):
    lit_terms[id].update(terms)
  for i,x in enumerate(D):
   if x.get('ids'):continue
   k=pk(x.get('text',''))
   if not k or k=='relative':continue
   candidates=[]
   for j in (i-1,i+1,i-2,i+2):
    if not (0<=j<len(D)):continue
    for id in D[j].get('ids',[]):
     if any(pk(t)==k for t in lit_terms.get(id,set())):
      candidates.append(id)
   unique=list(dict.fromkeys(candidates))
   if len(unique)==1:
    recoverable_bundled_pronouns.append((ch,v['v'],x.get('text',''),unique[0]))

  personal_idxs=[i for i,x in enumerate(D) if not x.get('ids') and pk(x.get('text','')) in {'he','she','they','it'}]
  usedids={id for x in D for id in x.get('ids',[])}
  relids=[]
  for y in L:
   if 'relative' in {pk(t) for t in re.findall(r"[A-Za-z0-9]+",y.get('text','')) if pk(t)}:
    for id in y.get('ids',[]):
     if id not in usedids and id not in relids:relids.append(id)
  if personal_idxs and len(personal_idxs)==len(relids):
   recoverable_relative_pronouns.append((ch,v['v'],[D[i].get('text','') for i in personal_idxs],relids))
  used_exact=collections.defaultdict(set)
  for x in D:
   w=n(x.get('text',''))
   if w and x.get('ids'):
    used_exact[w].update(x.get('ids',[]))
  lpos={}
  for li,y in enumerate(L):
   for id in y.get('ids',[]):
    lpos[id]=li
  for w,idxs in byword.items():
   lids=[]
   allowed=set()
   for i in idxs: allowed.update(D[i].get('phraseIds',[]))
   for y in L:
    if w in atoms(y.get('text','')):
     for id in y.get('ids',[]):
      if id not in used_exact[w] and (not allowed or id in allowed):lids.append(id)
   lids=list(dict.fromkeys(lids))
   if lids and len(lids)==len(idxs):
    recoverable.append((ch,v['v'],w,len(idxs),lids))
   elif len(idxs)==1 and len(lids)>1:
    i=idxs[0]
    erel=i/max(1,len(D)-1)
    ranked=sorted((abs(erel-lpos[id]/max(1,len(L)-1)),id) for id in lids if id in lpos)
    if len(ranked)>=2 and ranked[1][0]-ranked[0][0]>=0.12:
     recoverable_positional.append((ch,v['v'],w,ranked[0][1],ranked[:3]))
  # Catastrophic-collision guard: several explicitly authored precise English
  # content words must not collapse onto one Greek ID unless the literal layer
  # for that ID itself contains those lexical words. This catches resolver bugs
  # such as unrelated Paul/apostle/Christ/God tokens all becoming w1.
  lit_by_id=collections.defaultdict(set)
  for y in L:
   for id in y.get('ids',[]):
    lit_by_id[id].update(atoms(y.get('text','')))
  precise_by_id=collections.defaultdict(list)
  for x in D:
   if x.get('confidence')=='authored-precise':
    for id in x.get('ids',[]):
     precise_by_id[id].append(n(x.get('text','')))
  for id,ws in precise_by_id.items():
   uniq=list(dict.fromkeys(w for w in ws if w))
   unrelated=[w for w in uniq if w not in lit_by_id.get(id,set())]
   litwords=lit_by_id.get(id,set())
   evangel_ok=bool(litwords & {'evangelised','evangelized','gospel','evangelize'}) and set(uniq).issubset(EVANGEL_WORDS)
   if len(uniq)>=3 and len(unrelated)>=2 and not evangel_ok:
    collisions.append((ch,v['v'],id,uniq,sorted(litwords)))
pct=linked/(linked+unlinked)*100
assert pct>=75,pct
assert not recoverable, f'recoverable exact DGT links left unlinked: {recoverable[:20]}'
assert not recoverable_pronouns, f'recoverable pronoun-family DGT links left unlinked: {recoverable_pronouns[:20]}'
assert not recoverable_relative_pronouns, f'recoverable relative-to-personal pronoun links left unlinked: {recoverable_relative_pronouns[:20]}'
assert not recoverable_context_relative, f'recoverable contextual relative-pronoun links left unlinked: {recoverable_context_relative[:20]}'
assert not recoverable_bundled_pronouns, f'recoverable neighboring bundled-pronoun links left unlinked: {recoverable_bundled_pronouns[:20]}'
assert not recoverable_positional, f'recoverable positional exact links left unlinked: {recoverable_positional[:20]}'
assert not collisions, f'suspicious authored-precise Greek ID collisions: {collisions[:20]}'
assert not out_of_span, f'precise DGT links escaped authored phrase spans: {out_of_span[:20]}'
assert not synthetic_unlinked, f'unreviewed synthetic Greek tokens left without precise DGT links: {synthetic_unlinked[:20]}'
print(f'Philippians {start}-{end} audit clean: {count} verses; {pct:.1f}% authored DGT token coverage; 0 recoverable exact links left unlinked; 0 recoverable pronoun-family links left unlinked; 0 recoverable relative-pronoun bridges left unlinked; 0 suspicious authored-precise collisions; 0 unreviewed synthetic Greek tokens.')
