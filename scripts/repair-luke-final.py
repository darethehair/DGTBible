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

changed=0
for path in sorted(Path('data/luke').glob('[0-9][0-9].json')):
 d=json.loads(path.read_text(encoding='utf8'))
 file_changed=0
 for v in d.get('verses',[]):
  A=v.get('alignment',{});D=A.get('dgt',[]);G=A.get('greek',[]);L=A.get('literal',[])
  file_changed+=exact_fixed_point(D,L)
  file_changed+=semantic_pass(D,G,L)
  file_changed+=exact_fixed_point(D,L)
 if file_changed:
  path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
  changed+=file_changed
print(f'Luke post-override deterministic repairs: {changed}')

