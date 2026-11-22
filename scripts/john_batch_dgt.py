import re,unicodedata,collections
G=[['amen','truly'],['answer','answered','responded'],['say','said','says','saying','speak','spoke','speaking'],['see','seen','saw','behold'],['come','came','coming'],['go','went','going'],['remain','remains','stay','stayed','abide'],['believe','believed','believing'],['testify','testified','testimony','witness'],['receive','received'],['give','gave','given','gives'],['born','birth'],['judge','judged','judging','judgment','condemn','condemned','condemning'],['save','saved','salvation'],['love','loved'],['do','did','done','does'],['know','knew','known'],['send','sent'],['baptize','baptized','baptizing'],['rise','raise','raised'],['perish','perished'],['have','has','had'],['be','is','am','are','was','were','been','being'],['not','no','cannot'],['man','person','people'],['spirit','wind'],['voice','sound'],['earth','earthly'],['heaven','heavenly'],['one','someone','everyone','anyone'],['from','of'],['into','in'],['with','among'],['work','works','deeds'],['evil','wicked'],['life','live','living'],['die','died','death'],['eat','ate','eating'],['drink','drank','drinking'],['hear','heard','listen'],['walk','walking'],['teach','teacher','teaching'],['seek','seeking','look','looking'],['true','truth'],['glory','glorify','glorified'],['free','freedom'],['slave','enslaved'],['light','shining'],['dark','darkness'],['heal','healed','well'],['open','opened'],['blind','blindness'],['follow','following'],['sheep','flock'],['stone','stoned','stoning'],['sin','sinned','sinner','sinful'],['because','for','since'],['so','therefore','then'],['but','however','yet'],['sir','lord'],['want','wish','willing'],['great','large'],['little','small'],['bring','brought'],['leave','left']]
S={}
for g in G:
 for w in g:S.setdefault(w,set()).update(g)
def n(s):
 s=unicodedata.normalize('NFD',str(s)).lower();s=''.join(x for x in s if unicodedata.category(x)!='Mn');return re.sub(r'[^a-z0-9]','',s)
def st(w):
 w=n(w)
 for x in ['ing','ed','es','s','ly']:
  if len(w)>4 and w.endswith(x):return w[:-len(x)]
 return w
def sim(a,b):
 a,b=n(a),n(b)
 if not a or not b:return 0
 if a==b:return 12
 if b in S.get(a,set()) or a in S.get(b,set()):return 8
 if st(a)==st(b) and len(st(a))>=3:return 7
 if len(a)>=4 and len(b)>=4 and a[:4]==b[:4]:return 5
 return 0
def words(g):return [x for x in re.split(r'\s+',re.sub(r'[^A-Za-z0-9 ]',' ',g or '')) if x]
def split(raw):
 m=re.match(r'^([“‘"(\[]*)(.*?)([.,;:!?…”’")\]]*)$',raw);return m.groups() if m else ('',raw,'')
def align(text,src):
 rs=re.findall(r'\S+',text);out=[]
 for i,raw in enumerate(rs):
  a,b,c=split(raw);best=None
  for j,s in enumerate(src):
   z=max([sim(b,w) for w in words(s['gloss'])] or [0]);p=abs(i/max(1,len(rs)-1)-j/max(1,len(src)-1));q=z*10-p*4
   if best is None or q>best[0]:best=(q,z,s['id'])
  ids=[];conf='unlinked';reason='No high-confidence lexical anchor'
  if best and best[1]>=5:ids=[best[2]];conf='auto-high';reason=None
  if n(b)=='cannot':
   ap=round(i*(len(src)-1)/max(1,len(rs)-1));neg=[];able=[]
   for j,s in enumerate(src):
    g=' '.join(words(s['gloss'])).lower()
    if re.search(r'\b(not|no|unless)\b',g):neg.append((abs(j-ap),s['id']))
    if re.search(r'\b(able|can)\b',g):able.append((abs(j-ap),s['id']))
   if neg and able:ids=list(dict.fromkeys([min(neg)[1],min(able)[1]]))[:2];conf='auto-high';reason=None
  x={'text':a+b+c,'ids':ids,'after':' ' if i<len(rs)-1 else '','confidence':conf}
  if reason:x['reason']=reason
  out.append(x)
 return prune(out,src)
def prune(items,src):
 g={s['id']:s for s in src}
 for _ in range(5):
  p=collections.defaultdict(list)
  for i,x in enumerate(items):
   for id in x['ids']:p[id].append(i)
  changed=False
  for id,ps in p.items():
   if len(ps)<2 or all(ps[k]==ps[k-1]+1 for k in range(1,len(ps))):continue
   gw=words(g[id]['gloss']);si=next((j for j,s in enumerate(src) if s['id']==id),0);tp=si/max(1,len(src)-1)*max(1,len(items)-1)
   anchor=max(ps,key=lambda i:(max([sim(items[i]['text'],w) for w in gw] or [0]),-abs(i-tp)))
   keep={anchor}
   for d in (-1,1):
    k=anchor+d
    while k in ps and max([sim(items[k]['text'],w) for w in gw] or [0])>0:keep.add(k);k+=d
   for i in ps:
    if i in keep:continue
    items[i]['ids']=[x for x in items[i]['ids'] if x!=id]
    if not items[i]['ids']:items[i]['confidence']='unlinked';items[i]['reason']='Ambiguous noncontiguous helper-word alignment withheld'
    changed=True
  if not changed:break
 return items
