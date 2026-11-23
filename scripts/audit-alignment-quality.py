import json,re,unicodedata,collections
from pathlib import Path

BOOKS=['john','1john','2john','3john','jude','1peter','2peter','james','hebrews']
GLUE=set('a an the and but or so for because since if then than as of to from in into on at with by through before after about against under over is am are was were be been being has have had do does did will would shall should may might can could must he she it they we you i me him her them us my his their our your who whom whose which that this these those'.split())

def norm(s):
 s=unicodedata.normalize('NFD',str(s)).lower()
 s=''.join(x for x in s if unicodedata.category(x)!='Mn')
 return re.sub(r'[^a-z0-9]','',s)

def atoms(s):
 return [norm(x) for x in re.findall(r"[A-Za-z0-9]+",str(s)) if norm(x)]

groups=[
 ['imprint','expression','character','stamp','representation'],
 ['substance','being','reality','nature','essence'],
 ['word','declaration','saying','message'],
 ['make','made','making','do','did','done','produce','produced'],
 ['time','times','portion','portions','part','parts'],
 ['way','ways','manner','manners'],
 ['save','saved','salvation','rescue','rescued'],
 ['perfect','perfected','complete','completed','mature','maturity'],
 ['share','shared','sharer','sharers','partake','partook','participant','participants'],
 ['test','tested','testing','trial','trials','tempt','tempted','temptation'],
 ['hold','held','holding','keep','kept','retain','retained'],
 ['fall','fell','fallen','falling','stumble','stumbled'],
 ['rest','rested','resting','sabbathrest'],
 ['priest','priesthood','priestly'],
 ['covenant','testament'],
 ['offering','offer','offered','sacrifice','sacrifices'],
 ['holy','holiness','sanctify','sanctified','sanctification','saint','saints'],
 ['faith','faithful','believe','believed','believing'],
 ['righteous','righteousness','just','justify','justified'],
 ['lawless','lawlessness','unrighteous','unrighteousness','wicked','wickedness'],
 ['speak','spoke','spoken','say','said','saying','tell','told'],
 ['see','seen','saw','look','looked','behold'],
 ['know','knew','known','knowledge','understand','understood'],
 ['glory','glorious','glorify','glorified'],
 ['power','powerful','strength','strong','mighty'],
 ['death','die','died','dead'],
 ['life','live','lived','living'],
 ['eternal','forever','everlasting'],
]
S={}
for g in groups:
 for w in g:S.setdefault(w,set()).update(g)

def stem(w):
 w=norm(w); out={w}
 for suf,repl in [('ies','y'),('ied','y'),('ing',''),('ed',''),('es',''),('s',''),('ly','')]:
  if len(w)>len(suf)+2 and w.endswith(suf):out.add(w[:-len(suf)]+repl)
 return out

def sim(a,b):
 a,b=norm(a),norm(b)
 if not a or not b:return 0
 if a==b:return 12
 if b in S.get(a,set()) or a in S.get(b,set()):return 9
 if stem(a)&stem(b):return 8
 return 0

def src_words(g):
 out=[]
 for x in atoms(g.get('gloss','')):out.append(x)
 # literal alignment text can be more useful than gloss for old John
 return out

stats=collections.defaultdict(lambda:collections.Counter())
examples=[]
for slug in BOOKS:
 for path in sorted((Path('data')/slug).glob('[0-9][0-9].json')):
  d=json.loads(path.read_text(encoding='utf8'))
  for v in d['verses']:
   G=v.get('alignment',{}).get('greek',[]); D=v.get('alignment',{}).get('dgt',[])
   if not G or not D:continue
   pos={id:i for i,g in enumerate(G) for id in g.get('ids',[])}
   src={id:g for g in G for id in g.get('ids',[])}
   used={id for x in D for id in x.get('ids',[])}
   for i,x in enumerate(D):
    w=norm(x.get('text',''))
    if not w:continue
    if not x.get('ids') and w not in GLUE:
     candidates=[]
     for id,g in src.items():
      z=max([sim(w,a) for a in src_words(g)] or [0])
      if z>=8:candidates.append((z,id,g.get('text',''),g.get('gloss','')))
     if candidates:
      stats[slug]['probable_unlinked']+=1
      if len(examples)<100:examples.append((slug,v['v'],'UNLINKED',x['text'],sorted(candidates,reverse=True)[:3]))
    elif x.get('ids'):
     # flag links whose lexical fit is zero and which are far from relative position
     bestcur=max([max([sim(w,a) for a in src_words(src[id])] or [0]) for id in x['ids'] if id in src] or [0])
     rel=i/max(1,len(D)-1)
     dist=min([abs(rel-pos[id]/max(1,len(G)-1)) for id in x['ids'] if id in pos] or [0])
     if bestcur==0 and w not in GLUE and dist>.22:
      stats[slug]['suspicious_link']+=1
      if len(examples)<100:examples.append((slug,v['v'],'SUSPICIOUS',x['text'],[(id,src[id].get('text',''),src[id].get('gloss','')) for id in x['ids'] if id in src]))
for slug in BOOKS: print(slug,dict(stats[slug]))
print('EXAMPLES')
for e in examples:print(e)
