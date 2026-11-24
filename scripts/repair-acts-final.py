#!/usr/bin/env python3
import json,re,collections
from pathlib import Path
from alignment_repair import norm,sim,semantic_terms,source_map

# Explicit reviewed mappings are added here as the Acts hover-review queue is
# inspected.  They intentionally fail fast when a later wording change makes
# a reviewed target disappear.
REVIEWED_PRECISION={(20,10):[('his',1,['w15'])]}
REVIEWED_SUPPLIED={(8,10):[('them',1)]}
REVIEWED_SYNTHETICS={}

FAMILIES=[
 {'must','necessary','behooves','behoove','ought','needs','need','needed'},
 {'generation','generations'},
 {'humble','humbles','humbled','humbling','lowly'},
 {'assembly','assemblies','church','churches','congregation','congregations'},
 {'servant','servants','slave','slaves','minister','ministers'},
 {'announce','announces','announced','proclaim','proclaims','proclaimed','preach','preached'},
 {'rise','rises','rose','risen','raise','raises','raised','arise','arose','arisen'},
 {'send','sends','sent','sending'},
 {'answer','answered','reply','replied'},
 {'say','says','said','saying','speak','speaks','spoke','spoken','speaking'},
 {'see','sees','saw','seen','look','looks','looked','looking'},
 {'receive','receives','received','take','takes','took','taken'},
 {'go','goes','went','gone','going','depart','departed','leave','left'},
 {'come','comes','came','coming','arrive','arrived','approach','approached'},
 {'believe','believes','believed','faith','faithful'},
 {'save','saves','saved','salvation'},
]

def atoms(s):
 return [norm(t) for t in re.findall(r"[A-Za-z0-9]+",str(s)) if norm(t)]

def fkey(w):
 w=norm(w)
 for i,g in enumerate(FAMILIES):
  if w in g:return i
 return None

def fscore(a,b):
 a=norm(a);b=norm(b);z=sim(a,b)
 ka,kb=fkey(a),fkey(b)
 if ka is not None and ka==kb:z=max(z,12)
 return z

def target(D,word,occ,ref):
 matches=[x for x in D if norm(x.get('text',''))==norm(word)]
 if occ<1 or occ>len(matches):
  raise SystemExit(f'{ref}: reviewed target {word!r} occurrence {occ} not found')
 return matches[occ-1]

def apply_reviewed(D,G,ch,vn):
 ref=f'Acts {ch}:{vn}';changes=0
 source={id for g in G for id in g.get('ids',[])}
 for word,occ,ids in REVIEWED_PRECISION.get((ch,vn),[]):
  x=target(D,word,occ,ref)
  for id in ids:
   if id not in source:raise SystemExit(f'{ref}: reviewed precision unknown source {id}')
  if x.get('ids')!=ids or x.get('phraseIds')!=ids:
   x['ids']=ids[:];x['phraseIds']=ids[:];x['confidence']='acts-reviewed-precision'
   x.pop('supplied',None);x.pop('reason',None);changes+=1
 for word,occ in REVIEWED_SUPPLIED.get((ch,vn),[]):
  x=target(D,word,occ,ref)
  if x.get('ids') or x.get('phraseIds') or not x.get('supplied'):
   x['ids']=[];x['phraseIds']=[];x['supplied']=True
   x['confidence']='acts-reviewed-supplied'
   x['reason']='English supplied for natural rendering; no separate Greek token'
   changes+=1
 for sid,word,occ in REVIEWED_SYNTHETICS.get((ch,vn),[]):
  if sid not in source:raise SystemExit(f'{ref}: reviewed synthetic {sid} missing')
  x=target(D,word,occ,ref)
  ids=list(dict.fromkeys(x.get('ids',[])+[sid]))
  if x.get('ids')!=ids:
   x['ids']=ids;x['phraseIds']=list(dict.fromkeys(x.get('phraseIds',[])+[sid]))
   x['confidence']='acts-reviewed-synthetic';x.pop('reason',None);changes+=1
 return changes

def exact_fixed_point(D,L):
 total=0
 while True:
  changed=0;byword=collections.defaultdict(list);used=collections.defaultdict(set)
  for i,x in enumerate(D):
   if x.get('supplied'):continue
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
     D[i]['ids']=[id];D[i]['phraseIds']=[id];D[i]['confidence']='acts-final-exact'
     D[i].pop('reason',None);used[w].add(id);changed+=1
  total+=changed
  if not changed:return total

def family_fixed_point(D,G):
 src,pos=source_map(G);total=0
 while True:
  changed=0;byfam=collections.defaultdict(list);used=collections.defaultdict(set)
  for i,x in enumerate(D):
   if x.get('supplied'):continue
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
    if any(fkey(t)==k for t in semantic_terms(g,id,None)):cand.append(id)
   cand.sort(key=lambda id:pos.get(id,10**9))
   if cand and len(cand)==len(idxs):
    for i,id in zip(idxs,cand):
     D[i]['ids']=[id];D[i]['phraseIds']=[id];D[i]['confidence']='acts-final-family'
     D[i].pop('reason',None);used[k].add(id);changed+=1
  total+=changed
  if not changed:return total

changed=0
for path in sorted(Path('data/acts').glob('[0-9][0-9].json')):
 d=json.loads(path.read_text(encoding='utf8'));file_changed=0;ch=int(path.stem)
 for v in d.get('verses',[]):
  A=v.get('alignment',{});D=A.get('dgt',[]);G=A.get('greek',[]);L=A.get('literal',[])
  file_changed+=apply_reviewed(D,G,ch,v['v'])
  file_changed+=exact_fixed_point(D,L)
  file_changed+=family_fixed_point(D,G)
  file_changed+=exact_fixed_point(D,L)
 if file_changed:
  path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
  changed+=file_changed
print(f'Acts final deterministic/reviewed repairs: {changed}')
