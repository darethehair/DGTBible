#!/usr/bin/env python3
import json,re,unicodedata,collections
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/'data/books.json').read_text(encoding='utf8'))['books']
GLUE=set('a an the and but or so for because since if then than as of to from in into on at with by through before after about against under over is am are was were be been being has have had do does did will would shall should may might can could must he she it they we you i me him her them us my his their our your who whom whose which that this these those there here not no never none nothing one thing things its'.split())

def norm(s):
    s=unicodedata.normalize('NFD',str(s)).lower()
    s=''.join(c for c in s if unicodedata.category(c)!='Mn')
    return re.sub(r'[^a-z0-9]','',s)

def atoms(s):
    return [norm(x) for x in re.findall(r"[A-Za-z0-9]+",str(s)) if norm(x)]

def stemset(w):
    w=norm(w); out={w}
    for suf,repl in [('ies','y'),('ied','y'),('ing',''),('ed',''),('es',''),('s','')]:
        if len(w)>len(suf)+3 and w.endswith(suf):
            out.add(w[:-len(suf)]+repl)
    return out

def exactish(a,b):
    return bool(stemset(a)&stemset(b))

repairs=[]
by_book=collections.Counter()
changed_files=0

for book in catalog:
    slug=book['slug']
    manifest=ROOT/'data'/slug/'manifest.json'
    if not manifest.exists(): continue
    m=json.loads(manifest.read_text(encoding='utf8'))
    for ch in m.get('chapters',[]):
        path=ROOT/'data'/slug/ch['file']
        if not path.exists(): continue
        d=json.loads(path.read_text(encoding='utf8'))
        dirty=False
        for v in d.get('verses',[]):
            A=v.get('alignment',{}); G=A.get('greek',[]); D=A.get('dgt',[]); L=A.get('literal',[])
            if not G or not D: continue
            src={wid:g for g in G for wid in g.get('ids',[])}
            gpos={wid:i for i,g in enumerate(G) for wid in g.get('ids',[])}
            lit=collections.defaultdict(set)
            for x in L:
                for wid in x.get('ids',[]): lit[wid].update(atoms(x.get('text','')))
            used={wid for x in D for wid in x.get('ids',[])}
            for i,x in enumerate(D):
                if x.get('ids') or x.get('phraseIds') or x.get('supplied'): continue
                words=[w for w in atoms(x.get('text','')) if w not in GLUE and len(w)>2]
                if not words: continue
                candidates=[]
                rel=i/max(1,len(D)-1)
                for wid,g in src.items():
                    if wid in used: continue
                    terms=set(atoms(g.get('gloss','')))|lit.get(wid,set())
                    if not terms: continue
                    matches=[(w,t) for w in words for t in terms if exactish(w,t)]
                    if not matches: continue
                    dist=abs(rel-gpos.get(wid,0)/max(1,len(G)-1))
                    if dist<=0.25: candidates.append((wid,g,dist,matches))
                if len(candidates)!=1: continue
                wid,g,dist,matches=candidates[0]
                x['ids']=[wid]
                x['confidence']='master-exact-precise'
                x['reason']='Master review: unique unused Greek source with exact lexical/stem match'
                used.add(wid)
                dirty=True
                by_book[book['name']]+=1
                repairs.append({
                    'book':book['name'],'chapter':ch['chapter'],'verse':v['v'],
                    'english':x.get('text',''),'greek':g.get('text',''),'gloss':g.get('gloss',''),
                    'id':wid,'distance':round(dist,3),'matches':matches
                })
        if dirty:
            path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
            changed_files+=1

print(f'REPAIRED {len(repairs)} unique exact unlinked content tokens in {changed_files} chapter files')
for book,n in by_book.most_common(): print(f'{book}\t{n}')
print('DETAILS')
for r in repairs: print(json.dumps(r,ensure_ascii=False))
