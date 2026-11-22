import re,unicodedata
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
 return out
def clean(g):return re.sub(r'\s+',' ',re.sub(r'[<>\[\]]','',g or '').replace('¶','')).strip(' ,;')
def translit(s):
 mp={'α':'a','β':'b','γ':'g','δ':'d','ε':'e','ζ':'z','η':'ē','θ':'th','ι':'i','κ':'k','λ':'l','μ':'m','ν':'n','ξ':'x','ο':'o','π':'p','ρ':'r','σ':'s','ς':'s','τ':'t','υ':'y','φ':'ph','χ':'ch','ψ':'ps','ω':'ō'}
 t=unicodedata.normalize('NFD',s);return ''.join(mp.get(x.lower(),x) for x in t if unicodedata.category(x)!='Mn')
def map_words(greek,rows):
 ts=greek.split();ps=pairs(ts,[r['original'] for r in rows]);by={i:j for i,j in ps}
 used={j for _,j in ps};out=[];seen=set()
 # Resolve remaining near-equivalent words conservatively by relative position.
 for i in range(len(ts)):
  if i in by:continue
  cs=[j for j in range(len(rows)) if j not in used and equiv(ts[i],rows[j]['original'])]
  if cs:
   j=min(cs,key=lambda x:abs(i/max(1,len(ts)-1)-x/max(1,len(rows)-1)));by[i]=j;used.add(j)
 for i,t in enumerate(ts):
  if i in by:
   r=rows[by[i]];base=f'w{r["idx"]}';wid=base if base not in seen else base+'a';seen.add(wid)
   out.append(dict(id=wid,text=t,translit=r['translit'] or translit(t),gloss=clean(r['gloss']),strongs=r['strongs'],morph=r['morph'],synthetic=wid!=base))
  else:
   out.append(dict(id=f's{i+1}',text=t,translit=translit(t),gloss='',strongs='',morph='',synthetic=True))
 return out
