#!/usr/bin/env python3
import json,re,collections
from pathlib import Path
from alignment_repair import norm,sim,semantic_terms,source_map

FAMILIES=[
 {'must','necessary','behooves','behoove','ought','needs','need','needed'},
 {'generation','generations'},
 {'humble','humbles','humbled','humbling','lowly'},
]

def atoms(s):
 return [norm(t) for t in re.findall(r"[A-Za-z0-9]+",str(s)) if norm(t)]

def fscore(a,b):
 a=norm(a);b=norm(b)
 z=sim(a,b)
 for g in FAMILIES:
  if a in g and b in g:z=max(z,12)
 if a in {'caesars','gods'} and b==a[:-1]:z=max(z,12)
 return z

def exact_fixed_point(D,L):
 total=0
 while True:
  changed=0
  byword=collections.defaultdict(list)
  used=collections.defaultdict(set)
  for i,x in enumerate(D):
   w=norm(x.get('text',''))
   if not w:continue
   if x.get('ids'):used[w].update(x.get('ids',[]))
   else:byword[w].append(i)
  lids=collections.defaultdict(list)
  for y in L:
   for w in atoms(y.get('text','')):
    for id in y.get('ids',[]):
     if id not in lids[w]:lids[w].append(id)
  for w,idxs in byword.items():
   allowed=set()
   for i in idxs:allowed.update(D[i].get('phraseIds',[]))
   cand=[id for id in lids.get(w,[]) if id not in used[w] and (not allowed or id in allowed)]
   if cand and len(cand)==len(idxs):
    for i,id in zip(idxs,cand):
     D[i]['ids']=[id];D[i]['phraseIds']=[id]
     D[i]['confidence']='luke-postoverride-exact'
     D[i].pop('reason',None)
     used[w].add(id);changed+=1
  total+=changed
  if not changed:return total

def semantic_pass(D,G,L):
 src,pos=source_map(G);changes=0
 for i,x in enumerate(D):
  if x.get('ids'):continue
  w=norm(x.get('text',''))
  if not w:continue
  allowed=set(x.get('phraseIds',[]))
  scored=[]
  for id,g in src.items():
   if allowed and id not in allowed:continue
   terms=set(semantic_terms(g,id,None))
   z=max((fscore(w,t) for t in terms),default=0)
   if z>=8:scored.append((z,id,g))
  if not scored:continue
  best=max(z for z,_,_ in scored)
  tops=[(id,g) for z,id,g in scored if z==best]
  chosen=None
  if len(tops)==1 and best>=9:
   chosen=tops[0][0]
  elif best>=12:
   # Possessive forms prefer a matching genitive gloss ("of Caesar/God").
   if w in {'caesars','gods'}:
    poss=[id for id,g in tops if any(t=='of' for t in atoms(g.get('gloss','')))]
    if len(poss)==1:chosen=poss[0]
   if chosen is None:
    erel=i/max(1,len(D)-1)
    ranked=sorted((abs(erel-pos[id]/max(1,len(G)-1)),id) for id,_ in tops)
    if len(ranked)>=2 and ranked[1][0]-ranked[0][0]>=0.08:chosen=ranked[0][1]
  if chosen:
   x['ids']=[chosen];x['phraseIds']=[chosen]
   x['confidence']='luke-postoverride-semantic'
   x.pop('reason',None);changes+=1
 return changes



CONTENT_STOP={
 'a','an','the','and','or','but','so','for','of','to','in','on','at','by','from','with','as',
 'that','this','these','those','who','whom','whose','which','what','when','where','why','how',
 'i','me','my','mine','we','us','our','ours','you','your','yours','he','him','his','she','her',
 'they','them','their','it','its','be','am','is','are','was','were','been','being','do','does',
 'did','have','has','had','will','would','shall','should','may','might','can','could','must',
 'not','no','nor','if','then','than','also','even','only','very','more','most','all','any',
 'some','one','ones','there','here','into','out','up','down','over','under','again','away'
}

def global_unique_content_recover(D,G,L):
 changes=0
 # Build literal word -> unique source IDs for the entire verse.
 lids=collections.defaultdict(list)
 for y in L:
  for w in atoms(y.get('text','')):
   for id in y.get('ids',[]):
    if id not in lids[w]:lids[w].append(id)

 for x in D:
  if x.get('ids'):continue
  w=norm(x.get('text',''))
  if not w or w in CONTENT_STOP:continue
  cand=lids.get(w,[])
  if len(cand)==1:
   x['ids']=[cand[0]];x['phraseIds']=[cand[0]]
   x['confidence']='luke-global-unique-content-exact'
   x.pop('reason',None);changes+=1
   continue

  # If literal wording differs, accept only one uniquely best Greek/TAGNT
  # semantic candidate across the whole verse, with a strong score.
  scored=[]
  for g in G:
   for id in g.get('ids',[]):
    z=max((fscore(w,t) for t in semantic_terms(g,id,None)),default=0)
    if z>=9:scored.append((z,id))
  if scored:
   best=max(z for z,_ in scored)
   tops=list(dict.fromkeys(id for z,id in scored if z==best))
   second=max((z for z,_ in scored if z<best),default=0)
   if len(tops)==1 and (best>=12 or best-second>=2):
    x['ids']=[tops[0]];x['phraseIds']=[tops[0]]
    x['confidence']='luke-global-unique-content-semantic'
    x.pop('reason',None);changes+=1
 return changes

def family_fixed_point(D,G):
 src,pos=source_map(G);total=0
 def fkey(w):
  w=norm(w)
  for n,g in enumerate(FAMILIES):
   if w in g:return n
  return None
 while True:
  changed=0
  byfam=collections.defaultdict(list);used=collections.defaultdict(set)
  for i,x in enumerate(D):
   k=fkey(x.get('text',''))
   if k is None:continue
   if x.get('ids'):used[k].update(x.get('ids',[]))
   else:byfam[k].append(i)
  for k,idxs in byfam.items():
   allowed=set()
   for i in idxs:allowed.update(D[i].get('phraseIds',[]))
   cand=[]
   for id,g in src.items():
    if id in used[k] or (allowed and id not in allowed):continue
    if any(fkey(t)==k for t in semantic_terms(g,id,None)):
     cand.append(id)
   cand.sort(key=lambda id:pos.get(id,10**9))
   if cand and len(cand)==len(idxs):
    for i,id in zip(idxs,cand):
     D[i]['ids']=[id];D[i]['phraseIds']=[id]
     D[i]['confidence']='luke-postoverride-family'
     D[i].pop('reason',None);used[k].add(id);changed+=1
  total+=changed
  if not changed:return total

def pronoun_key(w):
 w=norm(w)
 groups={
  'he':{'he','him','his','himself'},
  'she':{'she','her','hers','herself'},
  'they':{'they','them','their','theirs','themselves'},
  'we':{'we','us','our','ours','ourselves'},
  'you':{'you','your','yours','yourself','yourselves'},
  'i':{'i','me','my','mine','myself'},
  'it':{'it','its','itself'},
 }
 if w in {'who','whom','whose','which'}:return 'relative'
 for k,g in groups.items():
  if w in g:return k
 return None

def relative_bridge(D,L):
 used={id for x in D for id in x.get('ids',[])}
 relids=[]
 for y in L:
  if 'relative' in {pronoun_key(t) for t in re.findall(r"[A-Za-z0-9]+",y.get('text','')) if pronoun_key(t)}:
   for id in y.get('ids',[]):
    if id not in used and id not in relids:relids.append(id)
 changes=0
 for i,x in enumerate(D):
  if x.get('ids') or pronoun_key(x.get('text','')) not in {'he','she','they','it'}:continue
  allowed=set(x.get('phraseIds',[]))
  cand=[id for id in relids if not allowed or id in allowed]
  if len(cand)==1:
   id=cand[0];x['ids']=[id];x['phraseIds']=[id]
   x['confidence']='luke-postoverride-relative'
   x.pop('reason',None);used.add(id);relids.remove(id);changes+=1
 return changes



def apply_reviewed_precision_fixes(D,ch,vn):
 fixes={
  # Luke 22:55: English auxiliary "had" belongs with περιάψαντων
  # ("having kindled"), and the final "sat" belongs with ἐκάθητο
  # ("was sitting"), not συγκαθισάντων ("having sat down together").
  (10,15):[
   ('you',1,['w2']),
   ('capernaum',1,['w3']),
   ('will',1,['w8']),
   ('you',2,['w8']),
   ('be',1,['w8']),
   ('exalted',1,['w8']),
  ],
  (10,4):[
   ('carry',1,['w2']),
   ('no',1,['w1']),
   ('money',1,['w3']),
   ('bag',1,['w3']),
   ('no',2,['w4']),
   ('travelers',1,['w5']),
   ('bag',2,['w5']),
   ('and',1,['w8']),
   ('no',3,['w6']),
   ('sandals',1,['w7']),
   ('and',2,['w8']),
   ('greet',1,['w13']),
   ('no',4,['w9']),
   ('one',1,['w9']),
   ('along',1,['w10']),
   ('the',1,['w11']),
   ('road',1,['w12']),
  ],
  (6,37):[
   ('do',1,['w3']),
   ('not',1,['w2']),
   ('judge',1,['w3']),
   ('and',1,['w4']),
   ('you',1,['w7']),
   ('will',1,['w7']),
   ('certainly',1,['w5']),
   ('not',2,['w6']),
   ('be',1,['w7']),
   ('judged',1,['w7']),
   ('do',2,['w10']),
   ('not',3,['w9']),
   ('condemn',1,['w10']),
   ('and',2,['w11']),
   ('you',2,['w14']),
   ('will',2,['w14']),
   ('certainly',2,['w12']),
   ('not',4,['w13']),
   ('be',2,['w14']),
   ('condemned',1,['w14']),
   ('release',1,['w15']),
   ('others',1,['w15']),
   ('and',3,['w16']),
   ('you',3,['w17']),
   ('will',3,['w17']),
   ('be',3,['w17']),
   ('released',1,['w17']),
  ],
  (6,33):[
   ('you',1,['w4']),
   ('do',1,['w4']),
   ('good',1,['w4']),
   ('to',1,['w5']),
   ('those',1,['w5']),
   ('who',1,['w6']),
   ('do',2,['w6']),
   ('good',2,['w6']),
   ('to',2,['w6']),
   ('you',2,['w7']),
   ('what',1,['w8']),
   ('credit',1,['w10']),
   ('is',1,['w11']),
   ('that',1,['w11']),
   ('to',3,['w9']),
   ('you',3,['w9']),
   ('even',1,['w12']),
   ('sinners',1,['w15']),
   ('do',3,['w18']),
   ('the',1,['w16']),
   ('same',1,['w17']),
  ],
  (22,55):[
   ('had',1,['w1']),
   ('sat',2,['w11']),
  ],
 }
 changes=0
 for word,occ,ids in fixes.get((ch,vn),[]):
  matches=[x for x in D if norm(x.get('text',''))==word]
  if occ<1 or occ>len(matches):
   raise SystemExit(f'Luke {ch}:{vn}: reviewed precision target {word!r} occurrence {occ} not found')
  x=matches[occ-1]
  if x.get('ids')!=ids or x.get('phraseIds')!=ids:
   x['ids']=ids[:];x['phraseIds']=ids[:]
   x['confidence']='luke-reviewed-precision'
   x.pop('reason',None);changes+=1
 return changes

REVIEWED_SYNTHETICS={
 (2,48,'s21'):('and',2),(2,48,'s22'):('i',1),
 (5,13,'s7'):('saying',1),(5,36,'s20'):('otherwise',1),(5,37,'s11'):('otherwise',1),
 (6,3,'s14'):('when',1),
 (10,6,'s15'):('otherwise',1),(10,15,'s11'):('brought',1),(10,39,'s14'):('jesus',1),
 (11,33,'s19'):('light',1),
 (13,9,'s10'):('not',1),(13,21,'s7'):('hid',1),
 (14,32,'s3'):('not',1),
 (15,16,'s3'):('fill',1),(15,16,'s7'):('with',1),
 (20,24,'s9'):('answered',1),(20,26,'s5'):('saying',1),
 (22,61,'s13'):('word',1),
 (23,42,'s8'):('into',1),
 (24,47,'s8'):('and',2),
 (24,49,'s4'):('sending',1),
}

def reviewed_synthetic_links(D,G,ch,vn):
 source={id for g in G for id in g.get('ids',[])}
 changes=0
 for (mc,mv,sid),(word,occ) in REVIEWED_SYNTHETICS.items():
  if (mc,mv)!=(ch,vn) or sid not in source:continue
  if any(sid in x.get('ids',[]) for x in D):continue
  matches=[i for i,x in enumerate(D) if norm(x.get('text',''))==word]
  if occ<1 or occ>len(matches):
   raise SystemExit(f'Luke {ch}:{vn}: reviewed synthetic {sid} target {word!r} occurrence {occ} not found')
  x=D[matches[occ-1]]
  x['ids']=list(dict.fromkeys(x.get('ids',[])+[sid]))
  x['phraseIds']=list(dict.fromkeys(x.get('phraseIds',[])+[sid]))
  x['confidence']='luke-reviewed-synthetic'
  x.pop('reason',None);changes+=1
 return changes

changed=0
for path in sorted(Path('data/luke').glob('[0-9][0-9].json')):
 d=json.loads(path.read_text(encoding='utf8'))
 file_changed=0
 for v in d.get('verses',[]):
  A=v.get('alignment',{});D=A.get('dgt',[]);G=A.get('greek',[]);L=A.get('literal',[])
  file_changed+=reviewed_synthetic_links(D,G,int(path.stem),v['v'])
  file_changed+=apply_reviewed_precision_fixes(D,int(path.stem),v['v'])
  file_changed+=global_unique_content_recover(D,G,L)
  file_changed+=exact_fixed_point(D,L)
  file_changed+=family_fixed_point(D,G)
  file_changed+=semantic_pass(D,G,L)
  file_changed+=relative_bridge(D,L)
  file_changed+=exact_fixed_point(D,L)
  file_changed+=family_fixed_point(D,G)
 if file_changed:
  path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
  changed+=file_changed
print(f'Luke post-override deterministic repairs: {changed}')


