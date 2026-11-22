import re,unicodedata,collections

G=[
['amen','truly'],['answer','answered','responded'],['say','said','says','saying','speak','spoke','speaking'],
['see','seen','saw','behold'],['come','came','coming'],['go','went','going'],['remain','remains','stay','stayed','abide'],
['believe','believed','believing'],['testify','testified','testimony','witness'],['receive','received'],['give','gave','given','gives'],
['born','birth'],['judge','judged','judging','judgment','condemn','condemned','condemning'],['save','saved','salvation'],
['love','loved'],['do','did','done','does'],['know','knew','known','understand','understood'],['send','sent'],
['baptize','baptized','baptizing'],['rise','raise','raised'],['perish','perished'],['have','has','had'],
['be','is','am','are','was','were','been','being'],['not','no','cannot'],['man','person','people'],['spirit','wind'],
['voice','sound'],['earth','earthly'],['heaven','heavenly'],['one','someone','everyone','anyone'],['from','of'],
['into','in'],['with','among'],['work','works','deeds'],['evil','wicked'],['life','live','living'],['die','died','death'],
['eat','ate','eating'],['drink','drank','drinking'],['hear','heard','listen'],['walk','walking'],['teach','teacher','teaching'],
['seek','seeking','look','looking'],['true','truth'],['glory','glorify','glorified'],['free','freedom'],['slave','enslaved'],
['light','shining'],['dark','darkness'],['heal','healed','well'],['open','opened'],['blind','blindness'],['follow','following'],
['sheep','flock'],['stone','stoned','stoning'],['sin','sinned','sinner','sinful'],['because','for','since'],['so','therefore','then'],
['but','however','yet'],['sir','lord'],['want','wish','willing'],['great','large'],['little','small'],['bring','brought'],
['leave','left'],['lie','lies','lay','lying','lain'],['sick','ailing','ill','infirmity'],['multitude','number','many','crowd'],
['old','elder','older'],['write','wrote','written','writing'],['take','took','taken','receive','received'],['make','made','become','became'],
['tell','told','report','reported'],['ask','asked','request','requested'],['fear','afraid'],['rejoice','rejoiced','glad'],
['find','found'],['call','called'],['lead','led'],['kill','killed','murder','murderer'],['hold','held','seize','seized'],
['keep','kept','observe'],['break','broken']
]
S={}
for g in G:
 for w in g:S.setdefault(w,set()).update(g)

def n(s):
 s=unicodedata.normalize('NFD',str(s)).lower()
 s=''.join(x for x in s if unicodedata.category(x)!='Mn')
 return re.sub(r'[^a-z0-9]','',s)

def stems(w):
 w=n(w);out={w}
 for suf,repl in [('ies','y'),('ied','y'),('ing',''),('ed',''),('es',''),('s',''),('ly','')]:
  if len(w)>len(suf)+2 and w.endswith(suf):
   x=w[:-len(suf)]+repl;out.add(x)
   if suf=='ing' and len(x)>2:
    out.add(x+'e')
    if len(x)>2 and len(x)>=2 and x[-1]==x[-2]:out.add(x[:-1])
   if suf=='ed' and len(x)>2:out.add(x+'e')
 return out

def atom_sim(a,b):
 a,b=n(a),n(b)
 if not a or not b:return 0
 if a==b:return 12
 if b in S.get(a,set()) or a in S.get(b,set()):return 9
 common=stems(a)&stems(b)
 if common and max(map(len,common))>=3:return 8
 if len(a)>=4 and len(b)>=4 and a[:4]==b[:4]:return 5
 return 0

def parts(s):return [x for x in re.split(r'[^A-Za-z0-9]+',str(s)) if x]
def sim(a,b):
 aa=parts(a) or [a];bb=parts(b) or [b]
 return max(atom_sim(x,y) for x in aa for y in bb)

def words(g):return [x for x in re.split(r'\s+',re.sub(r'[^A-Za-z0-9 ]',' ',g or '')) if x]

def split(raw):
 m=re.match(r'^([“‘"(\[]*)(.*?)([.,;:!?…”’")\]]*)$',raw)
 return m.groups() if m else ('',raw,'')

PRON={'i','me','my','mine','you','your','yours','he','him','his','she','her','hers','it','its','we','us','our','ours','they','them','their','theirs','who','whom','whose'}
ART={'the','a','an'}
CONJ={'and','but','or','so','therefore','then','yet','however','for','because','since'}
PREP={'of','to','from','in','into','on','at','with','among','by','through','before','after','about','against','under','over'}
NEG={'not','no','never','neither','nor'}
AUX={'is','am','are','was','were','be','been','being','has','have','had','do','does','did','will','would','shall','should','may','might','can','could','must'}

def morph_bonus(word,s):
 w=n(word);m=(s.get('morph') or '').upper();g=' '.join(words(s.get('gloss',''))).lower()
 if w in PRON and (m.startswith('P-') or 'PRON' in m):return 6
 if w in ART and (m.startswith('T-') or 'ART' in m):return 5
 if w in CONJ and ('CONJ' in m or m.startswith('ADV')):return 4
 if w in PREP and 'PREP' in m:return 6
 if w in NEG and ('-N' in m or re.search(r'\b(no|not|never|neither)\b',g)):return 7
 if w in AUX and m.startswith('V-'):return 4
 return 0

def align(text,src):
 rs=re.findall(r'\S+',text);out=[]
 for i,raw in enumerate(rs):
  a,b,c=split(raw);best=None
  for j,s in enumerate(src):
   z=max([sim(b,w) for w in words(s.get('gloss',''))] or [0])
   mb=morph_bonus(b,s)
   p=abs(i/max(1,len(rs)-1)-j/max(1,len(src)-1))
   q=z*10+mb*6+(2 if p<=0.18 else 0)-p*8
   if best is None or q>best[0]:best=(q,z,mb,p,s['id'])
  ids=[];conf='unlinked';reason='No high-confidence lexical anchor'
  if best and (best[1]>=5 or (best[2]>=5 and best[3]<=0.18)):
   ids=[best[4]];conf='auto-high';reason=None
  if n(b)=='cannot':
   ap=round(i*(len(src)-1)/max(1,len(rs)-1));neg=[];able=[]
   for j,s in enumerate(src):
    g=' '.join(words(s.get('gloss',''))).lower()
    if re.search(r'\b(not|no|unless)\b',g):neg.append((abs(j-ap),s['id']))
    if re.search(r'\b(able|can)\b',g):able.append((abs(j-ap),s['id']))
   if neg and able:
    ids=list(dict.fromkeys([min(neg)[1],min(able)[1]]))[:2];conf='auto-high';reason=None
  x={'text':a+b+c,'ids':ids,'after':' ' if i<len(rs)-1 else '','confidence':conf}
  if reason:x['reason']=reason
  out.append(x)
 return fill_contextual(prune(out,src),src)

def fill_contextual(items,src):
 pos={s['id']:i for i,s in enumerate(src)}
 def cat(w):
  w=n(w)
  if w in PRON or w in {'who','whom','whose','what','which'}:return 'pron'
  if w in ART:return 'art'
  if w in PREP:return 'prep'
  if w in CONJ or w in {'that','when','while','where','as'}:return 'conj'
  if w in NEG:return 'neg'
  if w in AUX:return 'aux'
  return None
 def compatible(kind,s):
  m=(s.get('morph') or '').upper();g=' '.join(words(s.get('gloss',''))).lower()
  if kind=='pron':return m.startswith(('P-','R-','D-','X-'))
  if kind=='art':return m.startswith('T-')
  if kind=='prep':return 'PREP' in m
  if kind=='conj':return 'CONJ' in m or m.startswith('ADV') or m.startswith('R-')
  if kind=='neg':return '-N' in m or bool(re.search(r'\\b(no|not|never|neither)\\b',g))
  return False

 # Auxiliaries may share a nearby already-linked Greek verb.
 for i,x in enumerate(items):
  if x['ids'] or cat(x['text'])!='aux':continue
  candidates=[]
  for j in range(max(0,i-2),min(len(items),i+3)):
   if j==i:continue
   for id in items[j]['ids']:
    s=src[pos[id]]
    if (s.get('morph') or '').upper().startswith('V-'):candidates.append(id)
  candidates=list(dict.fromkeys(candidates))
  if len(candidates)==1:
   x['ids']=[candidates[0]];x['confidence']='auto-high';x.pop('reason',None)

 # Finite Greek verb morphology can directly support an explicit English subject pronoun.
 subject_person={'i':{'1S'},'we':{'1P'},'you':{'2S','2P'},'he':{'3S'},'she':{'3S'},'it':{'3S'},'they':{'3P'}}
 for i,x in enumerate(items):
  w=n(x['text'])
  if x['ids'] or w not in subject_person:continue
  candidates=[]
  for j in range(max(0,i-2),min(len(items),i+4)):
   if j==i:continue
   for id in items[j]['ids']:
    s=src[pos[id]];m=(s.get('morph') or '').upper()
    if not m.startswith('V-'):continue
    pm=re.search(r'-(1S|2S|3S|1P|2P|3P)$',m)
    if pm and pm.group(1) in subject_person[w]:candidates.append(id)
  candidates=list(dict.fromkeys(candidates))
  if len(candidates)==1:
   x['ids']=[candidates[0]];x['confidence']='auto-high';x.pop('reason',None)

 # Fill grammatical words only in a narrow interval bounded by trusted links.
 for i,x in enumerate(items):
  if x['ids']:continue
  kind=cat(x['text'])
  if kind not in {'pron','art','prep','conj','neg'}:continue
  left=right=None
  for j in range(i-1,-1,-1):
   if items[j]['ids']:
    left=max(pos[id] for id in items[j]['ids'] if id in pos);break
  for j in range(i+1,len(items)):
   if items[j]['ids']:
    right=min(pos[id] for id in items[j]['ids'] if id in pos);break
  if left is None and right is None:continue
  lo=0 if left is None else max(0,left-1)
  hi=len(src)-1 if right is None else min(len(src)-1,right+1)
  if hi-lo>7:continue
  cs=[s for k,s in enumerate(src) if lo<=k<=hi and compatible(kind,s)]
  used={id for y in items[max(0,i-3):min(len(items),i+4)] for id in y['ids']}
  free=[s for s in cs if s['id'] not in used]
  if len(free)==1:
   x['ids']=[free[0]['id']];x['confidence']='auto-high';x.pop('reason',None)
 return prune(items,src)

def prune(items,src):
 g={s['id']:s for s in src}
 for _ in range(5):
  p=collections.defaultdict(list)
  for i,x in enumerate(items):
   for id in x['ids']:p[id].append(i)
  changed=False
  for id,ps in p.items():
   if len(ps)<2 or all(ps[k]==ps[k-1]+1 for k in range(1,len(ps))):continue
   gw=words(g[id].get('gloss',''));si=next((j for j,s in enumerate(src) if s['id']==id),0)
   tp=si/max(1,len(src)-1)*max(1,len(items)-1)
   anchor=max(ps,key=lambda i:(max([sim(items[i]['text'],w) for w in gw] or [0]),-abs(i-tp)))
   keep={anchor}
   for d in (-1,1):
    k=anchor+d
    while k in ps and max([sim(items[k]['text'],w) for w in gw] or [0])>0:
     keep.add(k);k+=d
   for i in ps:
    if i in keep:continue
    items[i]['ids']=[x for x in items[i]['ids'] if x!=id]
    if not items[i]['ids']:
     items[i]['confidence']='unlinked'
     items[i]['reason']='Ambiguous noncontiguous helper-word alignment withheld'
    changed=True
  if not changed:break
 return items
