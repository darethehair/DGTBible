#!/usr/bin/env python3
import json,re,unicodedata,collections
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
OUT=ROOT/'master-review'
OUT.mkdir(exist_ok=True)

catalog=json.loads((DATA/'books.json').read_text(encoding='utf8'))['books']
allow_path=DATA/'master-review-allowlist.json'
allow=set((json.loads(allow_path.read_text(encoding='utf8')).get('interactions',[])) if allow_path.exists() else [])

GLUE=set('a an the and but or so for because since if then than as of to from in into on at with by through before after about against under over is am are was were be been being has have had do does did will would shall should may might can could must he she it they we you i me him her them us my his their our your who whom whose which that this these those there here not no never none nothing one thing things its'.split())

def norm(s):
    s=unicodedata.normalize('NFD',str(s)).lower()
    s=''.join(c for c in s if unicodedata.category(c)!='Mn')
    return re.sub(r'[^a-z0-9]','',s)

def atoms(s):
    return [norm(x) for x in re.findall(r"[A-Za-z0-9]+",str(s)) if norm(x)]

def content_words(s):
    return [w for w in atoms(s) if w not in GLUE and len(w)>1]

# Lightweight semantic families drawn from recurring DGT alignment review cases.
FAMILIES=[
 {'say','said','saying','speak','spoke','spoken','speaking','tell','told'},
 {'see','saw','seen','seeing','look','looked','looking','behold','observe','observed'},
 {'know','knew','known','knowledge','understand','understood','understanding','intelligent','intelligence','recognize','recognized'},
 {'go','went','gone','going','depart','departed','leave','left'},
 {'come','came','coming','arrive','arrived','approach','approached'},
 {'give','gave','given','grant','granted'},
 {'take','took','taken','receive','received'},
 {'make','made','making','do','did','done'},
 {'save','saved','salvation','rescue','rescued','deliver','delivered'},
 {'believe','believed','believing','faith','faithful'},
 {'righteous','righteousness','just','justify','justified'},
 {'announce','announced','announcing','preach','preached','preaching','proclaim','proclaimed','good','news','gospel'},
 {'servant','servants','slave','slaves','minister','ministers'},
 {'assembly','assemblies','church','churches','congregation','congregations'},
 {'rise','rose','risen','raise','raised','arise','arose','resurrection'},
 {'ask','asked','request','requested','beg','begged','urge','urged'},
 {'kill','killed','destroy','destroyed','slay','slain'},
 {'write','wrote','written','writing'},
 {'hear','heard','hearing','listen','listened','listening'},
 {'great','greater','much','many','large'},
 {'small','little','least'},
 {'house','home','dwelling','household'},
 {'ship','boat','vessel'},
 {'fear','feared','afraid','terrified'},
 {'rejoice','rejoiced','joy','glad','gladness'},
 {'power','powerful','strength','strong','mighty','authority'},
 {'holy','holiness','sanctify','sanctified','saint','saints'},
 {'death','die','died','dead'},
 {'life','live','lived','living'},
 {'eternal','everlasting','forever'},
 {'covenant','testament'},
 {'offering','offer','offered','sacrifice','sacrifices'},
]
FAM={}
for i,g in enumerate(FAMILIES):
    for w in g:FAM[w]=i

def stemset(w):
    w=norm(w); out={w}
    for suf,repl in [('ies','y'),('ied','y'),('ing',''),('ed',''),('es',''),('s',''),('ly','')]:
        if len(w)>len(suf)+2 and w.endswith(suf):
            out.add(w[:-len(suf)]+repl)
    return out

def sim(a,b):
    a,b=norm(a),norm(b)
    if not a or not b:return 0
    if a==b:return 12
    if FAM.get(a) is not None and FAM.get(a)==FAM.get(b):return 9
    if stemset(a)&stemset(b):return 8
    return 0

def src_terms(g,literal_by_id,wid):
    vals=[]
    vals += atoms(g.get('gloss',''))
    vals += list(literal_by_id.get(wid,set()))
    return set(vals)

rows=[]
stats=collections.defaultdict(collections.Counter)
verses_seen=0
tokens_seen=0

for book in catalog:
    slug,name=book['slug'],book['name']
    manifest=DATA/slug/'manifest.json'
    if not manifest.exists():
        rows.append({'severity':100,'kind':'missing-manifest','book':name,'ref':name,'detail':str(manifest)})
        stats[name]['missing_manifest']+=1
        continue
    m=json.loads(manifest.read_text(encoding='utf8'))
    for chinfo in m.get('chapters',[]):
        path=DATA/slug/chinfo['file']
        if not path.exists():
            rows.append({'severity':100,'kind':'missing-chapter','book':name,'ref':f"{name} {chinfo['chapter']}",'detail':str(path)})
            stats[name]['missing_chapter']+=1
            continue
        d=json.loads(path.read_text(encoding='utf8'))
        for v in d.get('verses',[]):
            verses_seen+=1
            ref=f"{name} {chinfo['chapter']}:{v['v']}"
            A=v.get('alignment',{})
            G=A.get('greek',[]); D=A.get('dgt',[]); L=A.get('literal',[])
            if not G or not D:
                rows.append({'severity':95,'kind':'missing-alignment','book':name,'ref':ref,'detail':'Greek or DGT alignment absent'})
                stats[name]['missing_alignment']+=1
                continue
            tokens_seen+=len(D)
            src={wid:g for g in G for wid in g.get('ids',[])}
            gpos={wid:i for i,g in enumerate(G) for wid in g.get('ids',[])}
            gtext={wid:g.get('text','') for wid,g in src.items()}
            literal_by_id=collections.defaultdict(set)
            for x in L:
                terms=atoms(x.get('text',''))
                for wid in x.get('ids',[]):
                    literal_by_id[wid].update(terms)
            used=collections.defaultdict(list)
            for i,x in enumerate(D):
                for wid in x.get('ids',[]):used[wid].append(i)

            # Over-broad phrase fallback.
            for i,x in enumerate(D):
                if x.get('ids'):continue
                span=list(dict.fromkeys(x.get('phraseIds',[])))
                if span:
                    frac=len(span)/max(1,len(G))
                    if len(span)>=6 and frac>=0.50:
                        sev=80+min(19,int(frac*10))
                        rows.append({'severity':sev,'kind':'broad-phrase','book':name,'ref':ref,'token':x.get('text',''),'activated':len(span),'total':len(G),'share':round(frac,3),'detail':span})
                        stats[name]['broad_phrase']+=1

            # Precise fanout and scattered reuse.
            for wid,pos in used.items():
                # Fan-out is about a single Greek source lighting an unusually
                # long English rendering. A large percentage of a very short
                # verse is not, by itself, suspicious.
                if len(pos)>=5:
                    akey=f"precise-fanout|{slug}|{chinfo['chapter']}|{v['v']}|{wid}"
                    if akey not in allow:
                        rows.append({'severity':88,'kind':'precise-fanout','book':name,'ref':ref,'token':gtext.get(wid,wid),'activated':len(pos),'total':len(D),'share':round(len(pos)/max(1,len(D)),3),'detail':[D[i].get('text','') for i in pos]})
                        stats[name]['precise_fanout']+=1
                if len(pos)>=2:
                    groups=1
                    for a,b in zip(pos,pos[1:]):
                        if b!=a+1:groups+=1
                    span=(pos[-1]-pos[0]+1)/max(1,len(D))
                    if groups>=2 and (span>=0.35 or len(pos)>=5):
                        akey=f"precise-scattered|{slug}|{chinfo['chapter']}|{v['v']}|{wid}"
                        fanout_key=f"precise-fanout|{slug}|{chinfo['chapter']}|{v['v']}|{wid}"
                        # A reviewed legitimate fan-out is the same complete
                        # interaction pattern; do not re-report it merely
                        # because its words form multiple English runs.
                        if akey not in allow and fanout_key not in allow:
                            rows.append({'severity':84,'kind':'precise-scattered','book':name,'ref':ref,'token':gtext.get(wid,wid),'activated':len(pos),'total':len(D),'share':round(span,3),'detail':[D[i].get('text','') for i in pos]})
                            stats[name]['precise_scattered']+=1

            # Unlinked meaningful English with a unique plausible unused Greek candidate.
            already=set(used)
            for i,x in enumerate(D):
                if x.get('ids') or x.get('phraseIds') or x.get('supplied'):continue
                words=content_words(x.get('text',''))
                if not words:continue
                candidates=[]
                rel=i/max(1,len(D)-1)
                for wid,g in src.items():
                    terms=src_terms(g,literal_by_id,wid)
                    z=max((sim(w,t) for w in words for t in terms),default=0)
                    if z>=8:
                        dist=abs(rel-gpos.get(wid,0)/max(1,len(G)-1))
                        candidates.append((z,dist,wid,g.get('text',''),g.get('gloss','')))
                if candidates:
                    bestz=max(z for z,_,_,_,_ in candidates)
                    top=[c for c in candidates if c[0]==bestz]
                    if len(top)==1 and top[0][1]<=0.35:
                        z,dist,wid,gt,gl=top[0]
                        sev=78 if wid not in already else 72
                        rows.append({'severity':sev,'kind':'unique-unlinked-content','book':name,'ref':ref,'token':x.get('text',''),'detail':{'greek_id':wid,'greek':gt,'gloss':gl,'score':z,'distance':round(dist,3),'greek_already_used':wid in already}})
                        stats[name]['unique_unlinked_content']+=1
                    else:
                        stats[name]['ambiguous_unlinked_content']+=1
                else:
                    stats[name]['unlinked_content_no_candidate']+=1

            # Greek lexical source apparently unrepresented in precise DGT links.
            for wid,g in src.items():
                terms=[t for t in src_terms(g,literal_by_id,wid) if t not in GLUE]
                if not terms or wid in used:continue
                # Only elevate when a plausible English content word exists somewhere in verse.
                best=[]
                for i,x in enumerate(D):
                    words=content_words(x.get('text',''))
                    if not words:continue
                    z=max((sim(w,t) for w in words for t in terms),default=0)
                    if z>=8:best.append((z,i,x.get('text','')))
                if best:
                    best.sort(reverse=True)
                    z,i,et=best[0]
                    rows.append({'severity':74,'kind':'unused-greek-with-rendering','book':name,'ref':ref,'token':g.get('text',''),'detail':{'greek_id':wid,'gloss':g.get('gloss',''),'possible_english':et,'score':z}})
                    stats[name]['unused_greek_with_rendering']+=1

rows.sort(key=lambda r:(-r.get('severity',0),r.get('book',''),r.get('ref',''),r.get('kind','')))
summary={
 'books_expected':len(catalog),
 'books_scanned':sum(1 for b in catalog if (DATA/b['slug']/'manifest.json').exists()),
 'verses_scanned':verses_seen,
 'dgt_tokens_scanned':tokens_seen,
 'suspicious_interactions':len(rows),
 'by_kind':dict(collections.Counter(r['kind'] for r in rows)),
 'by_book':{k:dict(v) for k,v in stats.items()},
}
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
with (OUT/'ranked-review.jsonl').open('w',encoding='utf8') as f:
    for r in rows:f.write(json.dumps(r,ensure_ascii=False)+'\n')
with (OUT/'ranked-review.tsv').open('w',encoding='utf8') as f:
    f.write('severity\tkind\tbook\tref\ttoken\tdetail\n')
    for r in rows:
        f.write(f"{r.get('severity','')}\t{r.get('kind','')}\t{r.get('book','')}\t{r.get('ref','')}\t{r.get('token','')}\t{json.dumps(r.get('detail',''),ensure_ascii=False)}\n")
report=[
 'DGTBible FULL NEW TESTAMENT MASTER REVIEW',
 f"Books scanned: {summary['books_scanned']}/{summary['books_expected']}",
 f"Verses scanned: {summary['verses_scanned']}",
 f"DGT alignment tokens scanned: {summary['dgt_tokens_scanned']}",
 f"Ranked suspicious interactions: {summary['suspicious_interactions']}",
 '',
 'BY KIND',
]
for k,n in sorted(summary['by_kind'].items(),key=lambda kv:(-kv[1],kv[0])):
    report.append(f"{k}\t{n}")
report += ['','TOP 250']
for r in rows[:250]:
    report.append(f"{r['severity']}\t{r['kind']}\t{r['ref']}\t{r.get('token','')}\t{json.dumps(r.get('detail',''),ensure_ascii=False)}")
(OUT/'master-review.txt').write_text('\n'.join(report)+'\n',encoding='utf8')
print('\n'.join(report))
