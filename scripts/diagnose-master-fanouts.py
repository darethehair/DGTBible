#!/usr/bin/env python3
import json,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
catalog=json.loads((DATA/'books.json').read_text(encoding='utf8'))['books']
allow_path=DATA/'master-review-allowlist.json'
allow=set(json.loads(allow_path.read_text(encoding='utf8')).get('interactions',[])) if allow_path.exists() else set()
for book in catalog:
    slug,name=book['slug'],book['name']
    mp=DATA/slug/'manifest.json'
    if not mp.exists(): continue
    manifest=json.loads(mp.read_text(encoding='utf8'))
    for ch in manifest.get('chapters',[]):
        p=DATA/slug/ch['file']
        d=json.loads(p.read_text(encoding='utf8'))
        for v in d.get('verses',[]):
            G=v.get('alignment',{}).get('greek',[])
            D=v.get('alignment',{}).get('dgt',[])
            used=collections.defaultdict(list)
            for i,x in enumerate(D):
                for wid in x.get('ids',[]): used[wid].append(i)
            gby={wid:g for g in G for wid in g.get('ids',[])}
            bad=[]
            for wid,pos in used.items():
                key=f"precise-fanout|{slug}|{ch['chapter']}|{v['v']}|{wid}"
                if len(pos)>=5 and key not in allow:
                    bad.append((wid,pos))
            if not bad: continue
            print('===',name,f"{ch['chapter']}:{v['v']}",'===')
            print('GREEK_TEXT',v.get('greek',''))
            print('DGT_TEXT',v.get('dgt',''))
            print('FLAGGED',json.dumps([{'id':wid,'positions':pos,'greek':gby.get(wid,{}).get('text'),'gloss':gby.get(wid,{}).get('gloss')} for wid,pos in bad],ensure_ascii=False))
            print('GREEK',json.dumps([{'id':(g.get('ids') or [''])[0],'text':g.get('text'),'gloss':g.get('gloss')} for g in G],ensure_ascii=False))
            print('DGT',json.dumps([{'i':i,'text':x.get('text'),'ids':x.get('ids',[]),'confidence':x.get('confidence')} for i,x in enumerate(D)],ensure_ascii=False))
