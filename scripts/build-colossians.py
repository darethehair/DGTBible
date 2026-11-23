import re,json,collections,os,unicodedata
from pathlib import Path
from epistle_common import map_words
from john_batch_dgt import align
from alignment_repair import repair_verse, GLUE, norm, sim, semantic_terms

R=Path('.'); A=R/'authoring'; S=R/'data/sources'; S.mkdir(parents=True,exist_ok=True)
raw={}; authored={}
for path in sorted((R/'data/authoring').glob('colossians-*-dgt.tsv')):
 for line in path.read_text(encoding='utf8').splitlines():
  if not line.strip():continue
  parts=line.split('\t',3)
  if len(parts)<3:raise SystemExit(f'bad Colossians authoring line in {path}: {line!r}')
  _,ref,t=parts[:3]; ch,v=map(int,ref.split(':')); raw[(ch,v)]=t
  if len(parts)==4 and parts[3].strip():
   try: authored[(ch,v)]=json.loads(parts[3])
   except json.JSONDecodeError as e:raise SystemExit(f'bad authored alignment JSON {ref} in {path}: {e}')

# Regenerate generated chapters whenever bundled-pronoun logic changes.
def authored_dgt(text,src,spec,ref,literal=None):
 def local_sim(a,b):
  extra=[
   {'assembly','assemblies','church','churches','congregation','congregations'},
   {'servant','servants','minister','ministers','deacon','deacons'},
   {'bond','bonds','chain','chains','imprisonment'},
   {'fellowship','participation','partnership'},
   {'confident','confidence','persuaded','persuasion','trusting','trust'},
   {'think','thinking','minded','minding','mind'},
   {'watch','beware','heed','look'},
   {'lordship','lordships','dominion','dominions'},
   {'affliction','afflictions','tribulation','tribulations'},
   {'warn','warning','warned','admonish','admonishing','admonition'},
   {'elemental','element','elements','principle','principles'},
   {'labor','labour','toil','toiling'},
   {'encourage','encouraging','exhort','exhorting','exhortation'},
   {'equal','equals','equality','equally'},
  ]
  a=norm(a);b=norm(b)
  z=sim(a,b)
  if z:return z
  for g in extra:
   if a in g and b in g:return 9
  return 0
 def pronoun_key(w):
  groups={
   'he':{'he','him','his','himself','who','whom','whose'},
   'she':{'she','her','hers','herself','who','whom','whose'},
   'they':{'they','them','their','theirs','themselves','who','whom','whose'},
   'we':{'we','us','our','ours','ourselves'},
   'you':{'you','your','yours','yourself','yourselves'},
   'i':{'i','me','my','mine','myself'},
   'it':{'it','its','itself','which'},
  }
  w=norm(w)
  # Relative pronouns are antecedent-dependent. Treat them as a special
  # canonical family first; resolve to the remaining personal-pronoun family
  # only when occurrence counts make the pairing deterministic.
  if w in {'who','whom','whose','which'}: return 'relative'
  for k,vals in groups.items():
   if w in vals:return k
  return None
 def greek_key(s):
  s=unicodedata.normalize('NFD',str(s)).replace('ʼ','').replace('᾽','').replace('’','').replace("'","")
  s=''.join(x for x in s if unicodedata.category(x)!='Mn').lower()
  return ''.join(x for x in s if x.isalnum())
 def resolve(refs):
  ids=[]
  for r in refs:
   if not isinstance(r,str):raise SystemExit(f'{ref}: authored source reference must be a string: {r!r}')
   if r.startswith('@'):
    q=r[1:]
    if q=='all':
     ns=range(1,len(src)+1)
    elif '-' in q:
     a,b=map(int,q.split('-',1));ns=range(a,b+1)
    else:ns=[int(q)]
    for n in ns:
     if n<1 or n>len(src):raise SystemExit(f'{ref}: authored Greek ordinal @{n} outside 1..{len(src)}')
     ids.append(src[n-1]['id'])
   elif r.startswith('%'):
    q=r[1:]; occurrence=1
    if '#' in q:
     q,n=q.rsplit('#',1)
     try: occurrence=int(n)
     except ValueError: raise SystemExit(f'{ref}: bad Greek surface occurrence in {r!r}')
    key=greek_key(q); matches=[x['id'] for x in src if greek_key(x.get('text',''))==key]
    if occurrence<1 or occurrence>len(matches):
     raise SystemExit(f'{ref}: cannot find Greek surface {q!r} occurrence {occurrence}')
    ids.append(matches[occurrence-1])
   else:ids.append(r)
  valid={x['id'] for x in src};bad=[x for x in ids if x not in valid]
  if bad:raise SystemExit(f'{ref}: unknown authored Greek source IDs: {bad}')
  return list(dict.fromkeys(ids))

 tokens=re.findall(r'\S+',text)
 precision={}
 if isinstance(spec,dict) and isinstance(spec.get('segments'),list):
  expanded=[];rebuilt=[]
  for seg in spec['segments']:
   if not isinstance(seg,list) or len(seg)!=2 or not isinstance(seg[0],str) or not isinstance(seg[1],list):
    raise SystemExit(f'{ref}: each authored segment must be [text,[source refs]]: {seg!r}')
   stoks=re.findall(r'\S+',seg[0]);ids=resolve(seg[1]);rebuilt.extend(stoks);expanded.extend([ids]*len(stoks))
  if rebuilt!=tokens:raise SystemExit(f'{ref}: authored segment text does not exactly reproduce DGT tokens')
  for p in spec.get('precision',[]):
   if not isinstance(p,list) or len(p)!=2 or not isinstance(p[0],int) or not isinstance(p[1],list):
    raise SystemExit(f'{ref}: each precision override must be [1-based-token-index,[source refs]]: {p!r}')
   if p[0]<1 or p[0]>len(tokens):raise SystemExit(f'{ref}: precision token index {p[0]} outside 1..{len(tokens)}')
   precision[p[0]-1]=resolve(p[1])
  # Human-readable born alignment: ["english-token", occurrence, [source refs]].
  # Matching ignores punctuation/case but the build fails if the requested token
  # occurrence does not exist, so lexical intent stays explicit and reviewable.
  for p in spec.get('precisionWords',[]):
   if not isinstance(p,list) or len(p)!=3 or not isinstance(p[0],str) or not isinstance(p[1],int) or not isinstance(p[2],list):
    raise SystemExit(f'{ref}: precisionWords entries must be [token,occurrence,[source refs]]: {p!r}')
   key=norm(p[0]);matches=[i for i,t in enumerate(tokens) if norm(t)==key]
   if p[1]<1 or p[1]>len(matches):raise SystemExit(f'{ref}: precisionWords cannot find {p[0]!r} occurrence {p[1]}')
   precision[matches[p[1]-1]]=resolve(p[2])
  spec=expanded
 if not isinstance(spec,list) or len(spec)!=len(tokens):
  raise SystemExit(f'{ref}: authored alignment must cover each DGT whitespace token ({len(tokens)} expected)')

 byid={x['id']:x for x in src}
 out=[]
 for i,(token,refs) in enumerate(zip(tokens,spec)):
  if not isinstance(refs,list):raise SystemExit(f'{ref}: bad authored source list at DGT token {i}: {refs!r}')
  phrase_ids=resolve(refs)
  ids=precision.get(i)
  confidence='authored-precise' if i in precision else 'authored-phrase-only'
  if i not in precision:
   w=norm(token)
   if w and phrase_ids:
    scored=[]
    for id in phrase_ids:
     g=byid.get(id)
     if not g:continue
     z=max((local_sim(w,t) for t in semantic_terms(g,id,None)),default=0)
     if z>=8:scored.append((z,id))
    if scored:
     best=max(z for z,_ in scored);tops=[id for z,id in scored if z==best]
     second=max((z for z,_ in scored if z<best),default=0)
     content_safe=w not in GLUE and (best>=12 or (best>=9 and best-second>=1) or (best>=8 and best-second>=2))
     glue_safe=w in GLUE and best>=12
     if len(tops)==1 and (content_safe or glue_safe):
      ids=[tops[0]];confidence='authored-auto-precise'
  if ids is None:ids=[]
  x={'text':token,'ids':ids,'after':' ' if i<len(tokens)-1 else '','confidence':confidence,'phraseIds':phrase_ids}
  if not ids:x['reason']='Covered by authored phrase span; no safe lexical hover target'
  out.append(x)

 # Multiword lexical aliases that correspond to a single Greek lexeme.
 # "good news" is our preferred DGT wording for gospel/evangelize language.
 for i in range(len(out)-1):
  if norm(out[i].get('text',''))!='good' or norm(out[i+1].get('text',''))!='news':continue
  candidates=[]
  for si,g in enumerate(src):
   terms=set(semantic_terms(g,g.get('id'),None))
   if terms & {'gospel','evangel','evangelize','evangelized','evangelised'}:
    rel=(i+0.5)/max(1,len(out)-1);sp=si/max(1,len(src)-1)
    candidates.append((abs(rel-sp),g['id']))
  if not candidates:continue
  candidates.sort()
  id=candidates[0][1]
  out[i]['ids']=[id];out[i]['confidence']='authored-auto-precise-good-news';out[i].pop('reason',None)
  out[i+1]['ids']=[id];out[i+1]['confidence']='authored-auto-precise-good-news';out[i+1].pop('reason',None)
  if i>0 and norm(out[i-1].get('text','')) in {'proclaim','proclaimed','preach','preached'}:
   out[i-1]['ids']=[id];out[i-1]['confidence']='authored-auto-precise-good-news';out[i-1].pop('reason',None)

 # Recover deterministic exact matches from the already source-aligned literal
 # layer. If N still-unlinked DGT occurrences of a word correspond to exactly N
 # literal source occurrences of that word, pair them left-to-right.
 byword=collections.defaultdict(list)
 for i,x in enumerate(out):
  if not x.get('ids'):
   w=norm(x.get('text',''))
   if w: byword[w].append(i)
 if literal:
  for w,idxs in byword.items():
   candidates=[]
   for y in literal:
    terms=[norm(t) for t in re.findall(r"[A-Za-z0-9]+",y.get('text',''))]
    if w in terms:
     for id in y.get('ids',[]):
      if id not in candidates:candidates.append(id)
   if len(candidates)==len(idxs) and candidates:
    for i,id in zip(idxs,candidates):
     out[i]['ids']=[id]
     out[i]['confidence']='authored-auto-precise-literal-ordered'
     out[i].pop('reason',None)

 # Fallback ordered exact recovery from TAGNT/source glosses.
 byword=collections.defaultdict(list)
 for i,x in enumerate(out):
  if not x.get('ids'):
   w=norm(x.get('text',''))
   if w: byword[w].append(i)
 for w,idxs in byword.items():
  candidates=[];seen_ids=set()
  for id in out[idxs[0]].get('phraseIds',[]):
   g=byid.get(id)
   if not g:continue
   if any(norm(t)==w for t in semantic_terms(g,id,None)) and id not in seen_ids:
    candidates.append(id);seen_ids.add(id)
  if len(candidates)==len(idxs) and candidates:
   for i,id in zip(idxs,candidates):
    out[i]['ids']=[id]
    out[i]['confidence']='authored-auto-precise-ordered'
    out[i].pop('reason',None)

 # Greek finite verbs often bundle an English subject pronoun with the verb.
 # For an ambiguous phrase-only glue word, look up to two English tokens away:
 # inherit a precise source only when its gloss explicitly contains that word
 # and the source remains inside the already-authored phrase span.
 subject_pronouns={'i','we','you','he','she','they','it'}
 for i,x in enumerate(out):
  if x.get('ids') or not x.get('phraseIds'):continue
  w=norm(x.get('text',''))
  if not w or w not in GLUE:continue
  candidates=[]
  for j in (i-1,i+1,i-2,i+2):
   if not (0<=j<len(out)):continue
   for id in out[j].get('ids',[]):
    if id not in x.get('phraseIds',[]):continue
    g=byid.get(id)
    if g and any(norm(t)==w for t in semantic_terms(g,id,None)):
     candidates.append((j-i,id))
  unique=list(dict.fromkeys(id for _,id in candidates))
  chosen=None
  if len(unique)==1:
   chosen=unique[0]
  elif w in subject_pronouns:
   following=sorted((d,id) for d,id in candidates if d>0)
   if following:
    nearest=following[0][0]
    tops=list(dict.fromkeys(id for d,id in following if d==nearest))
    if len(tops)==1:chosen=tops[0]
  if chosen:
   x['ids']=[chosen];x['confidence']='authored-auto-precise-bundled';x.pop('reason',None)

 # Recover pronouns bundled into a neighboring source gloss using the
 # already source-aligned literal layer. This safely handles cases such as
 # DGT "he himself" when one Greek pronoun is glossed "He himself".
 if literal:
  lit_terms=collections.defaultdict(set)
  for y in literal:
   terms=[norm(t) for t in re.findall(r"[A-Za-z0-9]+",y.get('text',''))]
   for id in y.get('ids',[]):
    lit_terms[id].update(terms)
  for i,x in enumerate(out):
   if x.get('ids'):continue
   w=norm(x.get('text',''));k=pronoun_key(w)
   if not k or k=='relative':continue
   candidates=[]
   for j in (i-1,i+1,i-2,i+2):
    if not (0<=j<len(out)):continue
    for id in out[j].get('ids',[]):
     terms=lit_terms.get(id,set())
     if any(pronoun_key(t)==k for t in terms):
      candidates.append(id)
   unique=list(dict.fromkeys(candidates))
   if len(unique)==1:
    x['ids']=[unique[0]]
    x['confidence']='authored-auto-precise-literal-bundled-pronoun'
    x.pop('reason',None)

 # Final fixed-point literal recovery. Earlier alignment passes can reduce an
 # ambiguous repeated word to a deterministic N-to-N match; keep resolving
 # those exact occurrence-ordered cases until no further safe links appear.
 if literal:
  changed=True
  while changed:
   changed=False
   byword=collections.defaultdict(list)
   for i,x in enumerate(out):
    if not x.get('ids'):
     w=norm(x.get('text',''))
     if w:byword[w].append(i)
   for w,idxs in byword.items():
    candidates=[]
    for y in literal:
     terms=[norm(t) for t in re.findall(r"[A-Za-z0-9]+",y.get('text',''))]
     if w in terms:
      for id in y.get('ids',[]):
       if id not in candidates:candidates.append(id)
    if len(candidates)==len(idxs) and candidates:
     for i,id in zip(idxs,candidates):
      out[i]['ids']=[id]
      out[i]['confidence']='authored-auto-precise-literal-ordered'
      out[i].pop('reason',None)
     changed=True
 # Contextual relative-pronoun bridge first. A literal phrase such as
 # "in whom" commonly becomes idiomatic DGT "in him". When the same preceding
 # preposition is already precisely aligned in both layers, link the immediately
 # following unlinked personal pronoun to the unused relative-pronoun source.
 if literal:
  used_ids={id for x in out for id in x.get('ids',[])}
  for li,y in enumerate(literal):
   ywords=[norm(t) for t in re.findall(r"[A-Za-z0-9]+",y.get('text',''))]
   if not any(pronoun_key(t)=='relative' for t in ywords): continue
   relids=[id for id in y.get('ids',[]) if id not in used_ids]
   if len(relids)!=1 or li==0: continue
   prev_ids=literal[li-1].get('ids',[])
   if not prev_ids: continue
   for i in range(1,len(out)):
    if out[i].get('ids') or pronoun_key(out[i].get('text','')) not in {'he','she','they','it'}: continue
    if set(out[i-1].get('ids',[])) & set(prev_ids):
     out[i]['ids']=[relids[0]]
     out[i]['confidence']='authored-auto-precise-relative-pronoun-context'
     out[i].pop('reason',None)
     used_ids.add(relids[0])
     break

 # Final deterministic pronoun-family recovery. English may express the same
 # Greek pronoun with case/possessive/reflexive forms (he/him/his/himself).
 if literal:
  dgroups=collections.defaultdict(list)
  for i,x in enumerate(out):
   if not x.get('ids'):
    k=pronoun_key(x.get('text',''))
    if k:dgroups[k].append(i)
  used_pronoun_ids=collections.defaultdict(set)
  for x in out:
   k=pronoun_key(x.get('text',''))
   if k and x.get('ids'):
    used_pronoun_ids[k].update(x.get('ids',[]))
  for k,idxs in list(dgroups.items()):
   if k=='relative': continue
   candidates=[]
   for y in literal:
    ykeys={pronoun_key(t) for t in re.findall(r"[A-Za-z0-9]+",y.get('text',''))}
    if k in ykeys:
     for id in y.get('ids',[]):
      if id not in used_pronoun_ids[k] and id not in candidates:candidates.append(id)
   if len(candidates)==len(idxs) and candidates:
    for i,id in zip(idxs,candidates):
     out[i]['ids']=[id]
     out[i]['confidence']='authored-auto-precise-pronoun-ordered'
     out[i].pop('reason',None)

  # Relative-pronoun bridge: literal "who/whom/whose/which" may become
  # a personal pronoun in idiomatic DGT English ("in whom" -> "in him").
  # Pair remaining occurrences left-to-right when N personal-pronoun tokens
  # correspond to exactly N unused relative-pronoun source candidates.
  personal_idxs=[i for i,x in enumerate(out) if not x.get('ids') and pronoun_key(x.get('text','')) in {'he','she','they','it'}]
  rel_candidates=[]
  used_ids={id for x in out for id in x.get('ids',[])}
  for y in literal:
   ykeys={pronoun_key(t) for t in re.findall(r"[A-Za-z0-9]+",y.get('text',''))}
   if 'relative' in ykeys:
    for id in y.get('ids',[]):
     if id not in used_ids and id not in rel_candidates: rel_candidates.append(id)
  if personal_idxs and len(personal_idxs)==len(rel_candidates):
   for i,id in zip(personal_idxs,rel_candidates):
    out[i]['ids']=[id]
    out[i]['confidence']='authored-auto-precise-relative-pronoun'
    out[i].pop('reason',None)

 # Final stabilization loop. Exact recovery can create a new neighboring
 # pronoun-bundle opportunity, and pronoun bundling can in turn make another
 # exact occurrence deterministic. Alternate both until no safe change remains.
 if literal:
  lit_terms=collections.defaultdict(set)
  for y in literal:
   terms=[norm(t) for t in re.findall(r"[A-Za-z0-9]+",y.get('text',''))]
   for id in y.get('ids',[]):
    lit_terms[id].update(terms)
  changed=True
  while changed:
   changed=False

   byword=collections.defaultdict(list)
   used_exact=collections.defaultdict(set)
   for i,x in enumerate(out):
    w=norm(x.get('text',''))
    if not w:continue
    if x.get('ids'):
     used_exact[w].update(x.get('ids',[]))
    else:
     byword[w].append(i)
   for w,idxs in byword.items():
    candidates=[]
    for y in literal:
     terms=[norm(t) for t in re.findall(r"[A-Za-z0-9]+",y.get('text',''))]
     if w in terms:
      for id in y.get('ids',[]):
       if id not in used_exact[w] and id not in candidates:candidates.append(id)
    if len(candidates)==len(idxs) and candidates:
     for i,id in zip(idxs,candidates):
      out[i]['ids']=[id]
      out[i]['confidence']='authored-auto-precise-final-ordered'
      out[i].pop('reason',None)
     changed=True

   for i,x in enumerate(out):
    if x.get('ids'):continue
    w=norm(x.get('text',''));k=pronoun_key(w)
    if not k or k=='relative':continue
    candidates=[]
    for j in (i-1,i+1,i-2,i+2):
     if not (0<=j<len(out)):continue
     for id in out[j].get('ids',[]):
      if any(pronoun_key(t)==k for t in lit_terms.get(id,set())):
       candidates.append(id)
    unique=list(dict.fromkeys(candidates))
    if len(unique)==1:
     x['ids']=[unique[0]]
     x['confidence']='authored-auto-precise-final-bundled-pronoun'
     x.pop('reason',None)
     changed=True
 return out

start=int(os.environ.get('START_CHAPTER','1')); end=int(os.environ.get('END_CHAPTER','1'))
D=R/'data/colossians';D.mkdir(parents=True,exist_ok=True)
sbl={}
for line in (A/'sblgnt-colossians.txt').read_text(encoding='utf8').splitlines():
 m=re.match(r'^Col (\d+):(\d+)\t(.*)$',line)
 if m:sbl[(int(m[1]),int(m[2]))]=m[3].strip().replace('⸀','').replace('⸂','').replace('⸃','')
expected=sum(1 for k in sbl if start<=k[0]<=end)
missing=[k for k in sorted(sbl) if start<=k[0]<=end and k not in raw]
if missing:raise SystemExit(f'Colossians missing DGT verses: {missing[:20]} (total {len(missing)})')

step=collections.defaultdict(list)
for line in (A/'step-colossians.tsv').read_text(encoding='utf8').splitlines():
 m=re.match(r'^Col\.(\d+)\.(\d+)(?:\[[^\]]+\])?#(\d+)=([^\t]*)\t([^\t]*)\t([^\t]*)\t([^\t]*)\t([^\t]*)\t([^\t]*)',line)
 if not m:continue
 f=m[5];q=re.match(r'(.+?)\s+\(([^()]*)\)\s*$',f);o=(q.group(1) if q else f).strip();t=(q.group(2) if q else '')
 tag=m[7];a,b=(tag.split('=',1)+[''])[:2] if '=' in tag else (tag,'')
 step[(int(m[1]),int(m[2]))].append(dict(idx=int(m[3]),original=o,translit=t,gloss=m[6],strongs=a,morph=b))
for k in step:step[k].sort(key=lambda x:x['idx'])

linked=unlinked=synthetic=repairs=authored_verses=0
for ch in range(start,end+1):
 vs=[];sv=[]
 for (cnum,v),greek in sorted(sbl.items()):
  if cnum!=ch:continue
  src=map_words(greek,step[(ch,v)]);synthetic+=sum(bool(x.get('synthetic')) for x in src)
  ga=[];ta=[];la=[]
  for i,x in enumerate(src):
   af='' if i==len(src)-1 else ' ';g={'text':x['text'],'after':af,'ids':[x['id']]}
   for k in ['gloss','strongs','morph']:
    if x[k]:g[k]=x[k]
   ga.append(g);ta.append({'text':x['translit'],'after':af,'ids':[x['id']]});la.append({'text':x['gloss'] or x['text'],'after':af,'ids':[x['id']]})
  dgt=raw[(ch,v)]
  spec=authored.get((ch,v))
  if spec is not None:
   da=authored_dgt(dgt,src,spec,f'Col {ch}:{v}',la);authored_verses+=1
  else:
   if ch>=1:raise SystemExit(f'Col {ch}:{v}: new translation requires authored Greek source IDs in the fourth TSV column')
   da=align(dgt,src);repairs+=len(repair_verse(da,ga))
  linked+=sum(bool(x.get('ids') or x.get('phraseIds')) for x in da);unlinked+=sum(not (x.get('ids') or x.get('phraseIds')) for x in da)
  lit=''.join(x['text']+x['after'] for x in la)
  vs.append({'v':v,'greek':greek,'literal':lit,'dgt':dgt,'notes':[],'alignment':{'greek':ga,'translit':ta,'literal':la,'dgt':da}})
  sv.append({'ref':f'Col.{ch}.{v}','book':'COL','chapter':str(ch),'verse':str(v),'testament':'NT','words':[{'original':x['text'],'translit':x['translit'],'strongs':x['strongs'],'morph':x['morph'],'gloss':x['gloss'],'synthetic':x.get('synthetic',False)} for x in src]})
 (D/f'{ch:02}.json').write_text(json.dumps({'book':'Colossians','chapter':ch,'greekSource':'SBLGNT','verses':vs},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 (S/f'step-colossians-{ch:02}.json').write_text(json.dumps({'source':'STEPBible TAGNT aligned to SBLGNT','upstream':'STEPBible/STEPBible-Data@5de0a47f35f0fc13dfe1430d104e5db8a4285f9c','license':'CC BY 4.0','sblgnt':'Faithlife/SBLGNT@d7f35adca9ec410e1d1499c63b4dd989d76c8d4d','verses':sv},ensure_ascii=False,indent=2)+'\n',encoding='utf8')

pct=linked/(linked+unlinked)*100
if pct<75:raise SystemExit(f'Colossians {start}-{end}: coverage too low {pct:.1f}%')
if synthetic>40:raise SystemExit(f'Colossians {start}-{end}: too many synthetic source tokens {synthetic}')
print(f'Generated Colossians {start}-{end}: {expected} verses; {pct:.1f}% DGT token coverage ({linked} linked, {unlinked} deliberately unlinked); {authored_verses} verses born aligned; {synthetic} synthetic source tokens; {repairs} legacy context repairs.')
