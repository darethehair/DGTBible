# precise-fanout review marker 2026-11-24
# diagnostic rerun marker: conservative cleanup wave 2026-11-24
#!/usr/bin/env python3
import json
from pathlib import Path
from collections import defaultdict

catalog=json.loads(Path("data/books.json").read_text(encoding="utf8"))["books"]
rows=[]
for book in catalog:
    slug=book["slug"]
    manifest=Path("data")/slug/"manifest.json"
    if not manifest.exists():
        continue
    m=json.loads(manifest.read_text(encoding="utf8"))
    for chinfo in m.get("chapters",[]):
        p=Path("data")/slug/chinfo["file"]
        if not p.exists():
            continue
        d=json.loads(p.read_text(encoding="utf8"))
        for verse in d.get("verses",[]):
            dgt=verse.get("alignment",{}).get("dgt",[])
            greek=verse.get("alignment",{}).get("greek",[])
            gcount=max(1,len(greek)); ecount=max(1,len(dgt))
            ref=f'{book["name"]} {chinfo["chapter"]}:{verse["v"]}'

            # English phrase fallback that would light an implausibly large Greek span.
            for tok in dgt:
                if tok.get("ids"): continue
                span=list(dict.fromkeys(tok.get("phraseIds",[])))
                if not span: continue
                frac=len(span)/gcount
                if len(span)>=6 and frac>=0.50:
                    rows.append(("broad-phrase",ref,tok.get("text",""),len(span),gcount,frac,",".join(span)))

            # One precise Greek ID fanning out across too many DGT tokens.
            byid=defaultdict(list)
            for tok in dgt:
                for wid in tok.get("ids",[]):
                    byid[wid].append(tok.get("text",""))
            gtext={}
            for tok in greek:
                for wid in tok.get("ids",[]): gtext[wid]=tok.get("text","")
            for wid,words in byid.items():
                frac=len(words)/ecount
                if len(words)>=5 or frac>=0.35:
                    rows.append(("precise-fanout",ref,gtext.get(wid,wid),len(words),ecount,frac," ".join(words)))

rows.sort(key=lambda r:(-r[5],-r[3],r[1],r[2]))
from collections import Counter
book_interactions=Counter()
book_verses={}
for r in rows:
    ref=r[1]
    book=next((b["name"] for b in catalog if ref.startswith(b["name"]+" ")), ref.split(" ")[0])
    book_interactions[book]+=1
    book_verses.setdefault(book,set()).add(ref)
print(f"HOVER BREADTH SANITY: {len(rows)} suspicious interactions")
print("BY BOOK")
for book,count in sorted(book_interactions.items(), key=lambda kv:(-kv[1],kv[0])):
    print(f"{book}\t{count}\t{len(book_verses[book])} verses")
print("kind\tref\tsource/token\tactivated\ttotal\tshare\tdetail")
for r in rows:
    print(f"{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]}\t{r[5]*100:.1f}%\t{r[6]}")

# Diagnostic threshold: keep this non-failing initially so we can establish
# a baseline, fix the worst cases, then promote an agreed threshold to CI.
