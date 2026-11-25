#!/usr/bin/env python3
import json, re
from pathlib import Path

ROOT=Path("data/matthew")
ARTICLE=re.compile(r"^(?:ὁ|ἡ|τό|τοῦ|τῆς|τοῖς|ταῖς|τῶν|τόν|τήν|τούς|τάς|τὸ|τῇ|τῷ|οἱ|αἱ|τὰ|τὰς|τοὺς|τὴν|τὸν)[,.;·]?$")
SOFT_GLOSSES={"and","now","then","however","indeed","maybe","if","only","that","for","also","the","when"}

total_phrase=total_unlinked=total_missing=0
rows=[]
for ch in range(1,29):
    p=ROOT/f"{ch:02}.json"
    d=json.loads(p.read_text())
    for v in d.get("verses",[]):
        G=v.get("alignment",{}).get("greek",[])
        D=v.get("alignment",{}).get("dgt",[])
        used={i for t in D for i in (t.get("ids") or [])}
        phrase=[(i,t.get("text",""),len(t.get("phraseIds") or [])) for i,t in enumerate(D)
                if not (t.get("ids") or []) and not t.get("supplied") and len(t.get("phraseIds") or [])>=2]
        unlinked=[(i,t.get("text","")) for i,t in enumerate(D)
                  if not (t.get("ids") or []) and not t.get("supplied") and not (t.get("phraseIds") or [])]
        missing=[]
        for g in G:
            ids=g.get("ids") or []
            if ids and not any(i in used for i in ids):
                txt=g.get("text","")
                gloss=(g.get("gloss") or "").lower().strip(" .,:;!?")
                if not ARTICLE.match(txt) and gloss not in SOFT_GLOSSES:
                    missing.append((ids[0],txt,g.get("gloss","")))
        if phrase or unlinked or missing:
            rows.append((ch,v.get("v"),phrase,unlinked,missing))
            total_phrase+=len(phrase); total_unlinked+=len(unlinked); total_missing+=len(missing)

print(f"MATTHEW_BILINGUAL_RESIDUAL phrase_only={total_phrase} unlinked_english={total_unlinked} meaningful_unused_greek={total_missing} verses={len(rows)}")
for ch,v,phrase,unlinked,missing in rows:
    parts=[]
    if phrase: parts.append("phrase="+",".join(f"{i}:{t}[{n}]" for i,t,n in phrase))
    if unlinked: parts.append("unlinked="+",".join(f"{i}:{t}" for i,t in unlinked))
    if missing: parts.append("greek="+",".join(f"{i}:{t}<{g}>" for i,t,g in missing))
    print(f"M{ch}:{v} "+" | ".join(parts))


# Detailed candidate spans for oversized chapters 13 and 26
for ch in (13,26):
    p=ROOT/f"{ch:02}.json"
    d=json.loads(p.read_text())
    print(f"DETAIL_CHAPTER_{ch}")
    for v in d.get("verses",[]):
        G=v.get("alignment",{}).get("greek",[])
        byid={i:g for g in G for i in (g.get("ids") or [])}
        D=v.get("alignment",{}).get("dgt",[])
        for i,t in enumerate(D):
            ids=t.get("ids") or []
            phrase=t.get("phraseIds") or []
            if not ids and not t.get("supplied") and len(phrase)>=2:
                cand=[(x,byid.get(x,{}).get("text",""),byid.get(x,{}).get("gloss","")) for x in phrase]
                print(f"M{ch}:{v.get('v')} TOKEN {i} {t.get('text')!r} CAND {cand}")
            elif not ids and not t.get("supplied") and not phrase:
                print(f"M{ch}:{v.get('v')} TOKEN {i} {t.get('text')!r} UNLINKED")

# audit trigger after oversized repair

# final Matthew audit/deploy trigger

# post Greek recovery audit/deploy trigger
