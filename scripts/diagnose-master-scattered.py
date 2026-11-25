#!/usr/bin/env python3
import json,collections,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
catalog=json.loads((DATA/'books.json').read_text(encoding='utf8'))['books']
allow_path=DATA/'master-review-allowlist.json'
allow=set(json.loads(allow_path.read_text(encoding='utf8')).get('interactions',[])) if allow_path.exists() else set()
rows=[]
for book in catalog:
    slug,name=book['slug'],book['name']
    mp=DATA/slug/'manifest.json'
    if not mp.exists(): continue
    manifest=json.loads(mp.read_text(encoding='utf8'))
    for ch in manifest.get('chapters',[]):
        p=DATA/slug/ch['file']; d=json.loads(p.read_text(encoding='utf8'))
        for v in d.get('verses',[]):
            A=v.get('alignment',{}); G=A.get('greek',[]); D=A.get('dgt',[])
            if not G or not D: continue
            used=collections.defaultdict(list)
            for i,x in enumerate(D):
                for wid in x.get('ids',[]): used[wid].append(i)
            gby={wid:g for g in G for wid in g.get('ids',[])}
            for wid,pos in used.items():
                if len(pos)<2: continue
                groups=1
                for a,z in zip(pos,pos[1:]):
                    if z!=a+1: groups+=1
                span=(pos[-1]-pos[0]+1)/max(1,len(D))
                if groups<2 or (span<0.35 and len(pos)<5): continue
                key=f"precise-scattered|{slug}|{ch['chapter']}|{v['v']}|{wid}"
                fan=f"precise-fanout|{slug}|{ch['chapter']}|{v['v']}|{wid}"
                if key in allow or fan in allow: continue
                # Severity strongly favors more activated tokens and more runs.
                score=min(99, 40 + len(pos)*8 + (groups-1)*7 + int(span*15))
                rows.append((score,name,slug,ch['chapter'],v['v'],wid,pos,groups,span,gby.get(wid,{}),v,D,G))
rows.sort(key=lambda r:(-r[0],-len(r[6]),-r[8],r[1],r[3],r[4]))
print('SCATTERED_DIAGNOSTIC',len(rows))
print('BY ACTIVATED COUNT',dict(sorted(collections.Counter(len(r[6]) for r in rows).items())))
print('TOP',min(120,len(rows)))
for r in rows[:120]:
    score,name,slug,ch,vnum,wid,pos,groups,span,g,v,D,G=r
    print('===',name,f'{ch}:{vnum}','id',wid,'score',score,'activated',len(pos),'groups',groups,'span',f'{span:.3f}','===')
    print('SOURCE',json.dumps({'text':g.get('text'),'gloss':g.get('gloss'),'id':wid},ensure_ascii=False))
    print('GREEK_TEXT',v.get('greek',''))
    print('DGT_TEXT',v.get('dgt',''))
    print('GREEK',json.dumps([{'id':(x.get('ids') or [''])[0],'text':x.get('text'),'gloss':x.get('gloss')} for x in G],ensure_ascii=False))
    print('DGT',json.dumps([{'i':i,'text':x.get('text'),'ids':x.get('ids',[]),'confidence':x.get('confidence')} for i,x in enumerate(D)],ensure_ascii=False))
