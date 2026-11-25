#!/usr/bin/env python3
import json,collections
from pathlib import Path

root=Path(__file__).resolve().parents[1]
catalog=json.loads((root/'data/books.json').read_text(encoding='utf8'))['books']
changed_files=0
removed=0
by_book=collections.Counter()

for book in catalog:
    slug=book['slug']
    manifest=root/'data'/slug/'manifest.json'
    if not manifest.exists(): continue
    m=json.loads(manifest.read_text(encoding='utf8'))
    for ch in m.get('chapters',[]):
        path=root/'data'/slug/ch['file']
        if not path.exists(): continue
        d=json.loads(path.read_text(encoding='utf8'))
        dirty=False
        for v in d.get('verses',[]):
            A=v.get('alignment',{})
            G=A.get('greek',[])
            D=A.get('dgt',[])
            gcount=max(1,len(G))
            for tok in D:
                if tok.get('ids'): continue
                span=list(dict.fromkeys(tok.get('phraseIds',[])))
                if not span: continue
                # This is exactly the class the UI suppresses as unsafe:
                # a fallback phrase covering most of a verse.
                if len(span)>=6 and len(span)/gcount>=0.50:
                    tok.pop('phraseIds',None)
                    tok['confidence']='reviewed-unaligned'
                    tok['reason']='Legacy over-broad fallback removed; no safe lexical hover target'
                    dirty=True
                    removed+=1
                    by_book[book['name']]+=1
        if dirty:
            path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
            changed_files+=1

print(f'REMOVED {removed} legacy over-broad fallback spans from {changed_files} chapter files')
for book,n in by_book.most_common():
    print(f'{book}\t{n}')
