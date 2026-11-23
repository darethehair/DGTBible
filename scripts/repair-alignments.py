# context-aware corpus repair
# rerun exact lexical pass
import json,re,unicodedata,collections,sys
from pathlib import Path

BOOKS=['john','1john','2john','3john','jude','1peter','2peter','james','hebrews']
GLUE=set('a an the and but or so for because since if then than as of to from in into on at with by through before after about against under over is am are was were be been being has have had do does did will would shall should may might can could must he she it they we you i me him her them us my his their our your who whom whose which that this these those there here'.split())
GROUPS=[
 ['imprint','expression','character','stamp','representation'],
 ['substance','being','reality','nature','essence'],
 ['word','declaration','saying','message','speech'],
 ['make','made','making','do','did','done','produce','produced','create','created'],
 ['time','times','portion','portions','part','parts'],
 ['way','ways','manner','manners'],
 ['save','saved','salvation','rescue','rescued','deliver','delivered'],
 ['perfect','perfected','complete','completed','mature','maturity'],
 ['share','shared','sharer','sharers','partake','partook','participant','participants','partner','partners'],
 ['test','tested','testing','trial','trials','tempt','tempted','temptation'],
 ['hold','held','holding','keep','kept','retain','retained','grasp'],
 ['fall','fell','fallen','falling','stumble','stumbled'],
 ['rest','rested','resting','sabbathrest'],
 ['priest','priesthood','priestly'],
 ['covenant','testament'],
 ['offering','offer','offered','sacrifice','sacrifices'],
 ['holy','holiness','sanctify','sanctified','sanctification','saint','saints'],
 ['faith','faithful','believe','believed','believing'],
 ['righteous','righteousness','just','justify','justified'],
 ['lawless','lawlessness','unrighteous','unrighteousness','wicked','wickedness'],
 ['speak','spoke','spoken','speaking','say','said','says','saying','tell','told'],
 ['see','seen','saw','look','looked','behold','observe','observed'],
 ['know','knew','known','knowledge','understand','understood','recognize','recognized'],
 ['glory','glorious','glorify','glorified'],
 ['power','powerful','strength','strong','mighty','authority'],
 ['death','die','died','dead'],
 ['life','live','lived','living'],
 ['eternal','forever','everlasting'],
 ['give','gave','given','gives','grant','granted'],
 ['come','came','coming','arrive','arrived'],
 ['go','went','going','leave','left','depart','departed'],
 ['raise','raised','rise','risen','resurrection'],
 ['judge','judged','judgment','condemn','condemned','condemnation'],
 ['love','loved','loving','affection'],
 ['fear','feared','afraid','reverence','reverent'],
 ['good','better','best','excellent','excellence'],
 ['great','greater','large'],
 ['little','small','least'],
 ['body','flesh'],
 ['brother','brothers','sister','sisters','siblings'],
 ['child','children','son','sons','offspring'],
 ['work','works','deed','deeds','labor','labored'],
 ['truth','true','truly'],
 ['sin','sins','sinned','sinner','sinners','sinful'],
 ['worship','serve','served','service','minister','ministry'],
 ['clean','cleanse','cleansed','cleansing','purify','purified','purification'],
 ['promise','promised','promises'],
 ['inherit','inherited','inheritance','heir','heirs'],
 ['endure','endured','endurance','patient','patience'],
 ['call','called','calling','name','named'],
 ['write','wrote','written','writing'],
 ['hear','heard','hearing','listen','listened'],
 ['eat','ate','eating','food'],
 ['drink','drank','drinking'],
 ['king','kingdom','royal'],
 ['law','command','commandment','commandments'],
 ['free','freedom','liberty'],
 ['slave','slavery','enslave','enslaved'],
 ['light','lights','shining'],
 ['dark','darkness','gloom'],
 ['heal','healed','healing','well'],
 ['open','opened'],
 ['blind','blindness'],
 ['follow','followed','following','imitate','imitated'],
 ['sheep','flock'],
 ['stone','rock'],
 ['desire','desires','desired','lust','lusts','passion','pleasure','pleasures'],
 ['mercy','merciful','compassion','compassionate'],
 ['rebellion','rebel','rebelled','disobedience','disobey','disobeyed'],
 ['proud','pride','arrogant','boast','boasted','boasting'],
 ['humble','humbled','humility','lowly'],
 ['glad','joy','joyful','rejoice','rejoiced'],
 ['anger','angry','wrath'],
 ['house','household'],
 ['city','town'],
 ['earth','world','earthly'],
 ['heaven','heavens','heavenly'],
 ['angel','angels'],
 ['spirit','spirits'],
 ['heart','hearts'],
 ['mind','minds','thought','thoughts'],
 ['remember','remembered','remembrance','memory'],
 ['forget','forgot','forgotten'],
 ['teach','taught','teacher','teachers','teaching'],
 ['seek','sought','seeking'],
 ['find','found'],
 ['receive','received','obtain','obtained'],
 ['bring','brought','lead','led'],
 ['kill','killed','murder','murdered'],
 ['one','someone','anyone','everyone','person','people','man','human'],
]
S={}
for g in GROUPS:
 for w in g:S.setdefault(w,set()).update(g)

def norm(s):
 s=unicodedata.normalize('NFD',str(s)).lower()
 s=''.join(x for x in s if unicodedata.category(x)!='Mn')
 return re.sub(r'[^a-z0-9]','',s)

def atoms(s): return [norm(x) for x in re.findall(r"[A-Za-z0-9]+",str(s)) if norm(x)]
def stems(w):
 w=norm(w);out={w}
 for suf,repl in [('ies','y'),('ied','y'),('ing',''),('ed',''),('es',''),('s',''),('ly','')]:
  if len(w)>len(suf)+2 and w.endswith(suf):
   x=w[:-len(suf)]+repl;out.add(x)
   if suf=='ing' and len(x)>2:out.add(x+'e')
   if suf=='ed' and len(x)>2:out.add(x+'e')
 return out
def sim(a,b):
 a,b=norm(a),norm(b)
 if not a or not b:return 0
 if a==b:return 12
 if b in S.get(a,set()) or a in S.get(b,set()):return 9
 if stems(a)&stems(b):return 8
 if len(a)>=5 and len(b)>=5 and a[:5]==b[:5]:return 6
 return 0

def gloss_atoms(g):
 vals=atoms(g.get('gloss',''))
 if not vals: vals=atoms(g.get('text',''))
 return vals

def source_map(G):
 src={};pos={}
 for i,g in enumerate(G):
  for id in g.get('ids',[]):
   src[id]=g;pos[id]=i
 return src,pos

def semantic(token,g):
 return max([sim(token,a) for a in gloss_atoms(g)] or [0])

def bounds(D,i,pos,skip_current=True):
 left=right=None
 for j in range(i-1,-1,-1):
  ids=[id for id in D[j].get('ids',[]) if id in pos]
  if ids:
   left=max(pos[id] for id in ids);break
 for j in range(i+1,len(D)):
  ids=[id for id in D[j].get('ids',[]) if id in pos]
  if ids:
   right=min(pos[id] for id in ids);break
 return left,right

def candidate_score(i,D,G,src,pos,id,z):
 rel=i/max(1,len(D)-1); sp=pos[id]/max(1,len(G)-1)
 score=z*10-abs(rel-sp)*18
 left,right=bounds(D,i,pos)
 p=pos[id]
 if left is not None and right is not None:
  lo=min(left,right)-2;hi=max(left,right)+2
  if lo<=p<=hi:score+=22
  else:score-=20
 elif left is not None:
  if abs(p-left)<=3:score+=10
 elif right is not None:
  if abs(p-right)<=3:score+=10
 # Strong preference for sharing a Greek source with an adjacent English phrase.
 for j in (i-1,i+1):
  if 0<=j<len(D) and id in D[j].get('ids',[]):score+=16
 return score

def repair_verse(D,G):
 src,pos=source_map(G);changes=[]
 if not src:return changes
 # Pass 1: repair clearly misplaced content links when a strong in-context alternative exists.
 for i,x in enumerate(D):
  w=norm(x.get('text',''))
  contentish = w not in GLUE or (w=='being' and i>0 and norm(D[i-1].get('text','')) in {'my','your','his','her','our','their'})
  if not w or not contentish or not x.get('ids'):continue
  cur=[id for id in x['ids'] if id in src]
  if not cur:continue
  curz=max(semantic(w,src[id]) for id in cur)
  left,right=bounds(D,i,pos)
  cur_in=True
  if left is not None and right is not None:
   lo=min(left,right)-4;hi=max(left,right)+4
   cur_in=any(lo<=pos[id]<=hi for id in cur)
  candidates=[]
  for id,g in src.items():
   z=semantic(w,g)
   if z>=8:candidates.append((candidate_score(i,D,G,src,pos,id,z),z,id))
  if not candidates:continue
  candidates.sort(reverse=True);score,z,best=candidates[0]
  curscore=max(candidate_score(i,D,G,src,pos,id,semantic(w,src[id])) for id in cur)
  if best not in cur and (not cur_in) and score>=curscore+8:
   old=list(x['ids']);x['ids']=[best];x['confidence']='context-repaired';x.pop('reason',None)
   changes.append(('relink',x['text'],old,best))
 # Pass 2: fill lexical misses conservatively.
 for i,x in enumerate(D):
  if x.get('ids'):continue
  w=norm(x.get('text',''))
  if not w or w in GLUE:continue
  candidates=[]
  for id,g in src.items():
   z=semantic(w,g)
   if z>=8:candidates.append((candidate_score(i,D,G,src,pos,id,z),z,id))
  if not candidates:continue
  candidates.sort(reverse=True)
  best=candidates[0]
  margin=best[0]-(candidates[1][0] if len(candidates)>1 else -999)
  left,right=bounds(D,i,pos);p=pos[best[2]]
  in_context=True
  if left is not None and right is not None:
   in_context=min(left,right)-4<=p<=max(left,right)+4
  elif left is not None:in_context=abs(p-left)<=5
  elif right is not None:in_context=abs(p-right)<=5
  # Exact matches can tolerate a smaller margin; synonym/stem matches require contextual clarity.
  if in_context and ((best[1]>=12 and margin>=2) or (best[1]>=8 and margin>=8)):
   x['ids']=[best[2]];x['confidence']='context-repaired';x.pop('reason',None)
   changes.append(('link',x['text'],best[2]))
 # Pass 3: unique exact lexical matches missed only because word order is unusual.
 exact_exclude=GLUE|{'one','someone','anyone','everyone','there','here','what','where','whether','others','other','though','once','having','thing','things'}
 for i,x in enumerate(D):
  if x.get('ids'):continue
  w=norm(x.get('text',''))
  if not w or w in exact_exclude:continue
  exact=[id for id,g in src.items() if semantic(w,g)>=12]
  if len(exact)==1:
   id=exact[0]
   rel=i/max(1,len(D)-1);sp=pos[id]/max(1,len(G)-1)
   if abs(rel-sp)<=0.48:
    x['ids']=[id];x['confidence']='context-repaired';x.pop('reason',None)
    changes.append(('exact-link',x['text'],id))
 return changes

summary=collections.Counter();examples=[]
targets=sys.argv[1:] or BOOKS
for slug in targets:
 for path in sorted((Path('data')/slug).glob('[0-9][0-9].json')):
  d=json.loads(path.read_text(encoding='utf8'));dirty=False
  for v in d.get('verses',[]):
   A=v.get('alignment',{});D=A.get('dgt',[]);G=A.get('greek',[])
   if not D or not G:continue
   changes=repair_verse(D,G)
   if changes:
    dirty=True;summary[slug]+=len(changes)
    for ch in changes[:5]:
     if len(examples)<100:examples.append((slug,path.stem,v['v'],ch))
  if dirty:path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
for slug in targets:print(f'{slug}: {summary[slug]} alignment repairs')
print('TOTAL',sum(summary.values()))
for x in examples:print(x)
