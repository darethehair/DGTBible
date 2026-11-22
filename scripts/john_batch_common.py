import re,unicodedata,collections
def norm(s):
 s=unicodedata.normalize('NFD',str(s)).replace('ʼ','').replace('᾽','').replace('’','').replace("'","")
 s=''.join(x for x in s if unicodedata.category(x)!='Mn').lower()
 return ''.join(x for x in s if x.isalnum())
def edit1(a,b):
 if abs(len(a)-len(b))>1:return False
 if len(a)==len(b):return sum(x!=y for x,y in zip(a,b))<=1
 L,S=(a,b) if len(a)>len(b) else (b,a)
 return any(L[:i]+L[i+1:]==S for i in range(len(L)))
def equiv(a,b):
 a,b=norm(a),norm(b)
 if not a or not b:return False
 if a==b:return True
 if a.endswith('ν') and a[:-1]==b:return True
 if b.endswith('ν') and b[:-1]==a:return True
 if a.endswith('α') and a[:-1]==b:return True
 if b.endswith('α') and b[:-1]==a:return True
 return edit1(a,b)
def pairs(A,B):
 m,n=len(A),len(B);d=[[0]*(n+1) for _ in range(m+1)]
 for i in range(m-1,-1,-1):
  for j in range(n-1,-1,-1):d[i][j]=1+d[i+1][j+1] if equiv(A[i],B[j]) else max(d[i+1][j],d[i][j+1])
 out=[];i=j=0
 while i<m and j<n:
  if equiv(A[i],B[j]) and d[i][j]==1+d[i+1][j+1]:out.append((i,j));i+=1;j+=1
  elif d[i+1][j]>=d[i][j+1]:i+=1
  else:j+=1
 ua={i for i,_ in out};ub={j for _,j in out}
 for i in range(m):
  if i in ua:continue
  cs=[j for j in range(n) if j not in ub and equiv(A[i],B[j])]
  if cs:
   j=min(cs,key=lambda x:abs(i/max(1,m-1)-x/max(1,n-1)));out.append((i,j));ub.add(j)
 return sorted(out)
def clean(g):return re.sub(r'\s+',' ',re.sub(r'[<>\[\]]','',g or '').replace('¶','')).strip(' ,;')
def translit(s):
 mp={'α':'a','β':'b','γ':'g','δ':'d','ε':'e','ζ':'z','η':'ē','θ':'th','ι':'i','κ':'k','λ':'l','μ':'m','ν':'n','ξ':'x','ο':'o','π':'p','ρ':'r','σ':'s','ς':'s','τ':'t','υ':'y','φ':'ph','χ':'ch','ψ':'ps','ω':'ō'}
 t=unicodedata.normalize('NFD',s);return ''.join(mp.get(x.lower(),x) for x in t if unicodedata.category(x)!='Mn')
S753=[('καὶ','kai','And','G2532','CONJ'),('ἐπορεύθη','eporeuthē','went','G4198','V-API-3S'),('ἕκαστος','hekastos','each','G1538','A-NSM'),('εἰς','eis','to','G1519','PREP'),('τὸν','ton','the','G3588','T-ASM'),('οἶκον','oikon','house','G3624','N-ASM'),('αὐτοῦ·','autou','his','G0846','P-GSM')]
def map_words(ch,v,greek,rows):
 ts=greek.split()
 if (ch,v)==(7,53):return [dict(id=f'w{i+1}',text=t,translit=S753[i][1],gloss=S753[i][2],strongs=S753[i][3],morph=S753[i][4],synthetic=True) for i,t in enumerate(ts)]
 ps=pairs(ts,[r['original'] for r in rows]);by={i:j for i,j in ps};used={j for _,j in ps}
 if (ch,v)==(5,2):
  a=[i for i in range(len(ts)) if i not in by];b=[j for j in range(len(rows)) if j not in used]
  if len(a)==len(b)==1:by[a[0]]=b[0];used.add(b[0])
 if (ch,v) in {(8,3),(8,8),(8,9),(8,11)}:
  a=[i for i in range(len(ts)) if i not in by];b=[j for j in range(len(rows)) if j not in used]
  for i in a:
   if not b:break
   j=min(b,key=lambda x:abs(i/max(1,len(ts)-1)-x/max(1,len(rows)-1)));by[i]=j;b.remove(j)
 out=[];seen=set()
 for i,t in enumerate(ts):
  if i in by:
   r=rows[by[i]];base=f'w{r["idx"]}';id=base if base not in seen else base+'a';seen.add(id)
   out.append(dict(id=id,text=t,translit=r['translit'] or translit(t),gloss=clean(r['gloss']),strongs=r['strongs'],morph=r['morph'],synthetic=id!=base))
  else:out.append(dict(id=f's{i+1}',text=t,translit=translit(t),gloss='',strongs='',morph='',synthetic=True))
 return out
