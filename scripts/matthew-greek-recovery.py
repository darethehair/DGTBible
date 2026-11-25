#!/usr/bin/env python3
import json,re
from pathlib import Path

ROOT=Path("data/matthew")
STOP={"the","a","an","and","or","but","for","to","of","in","on","at","as","is","are","was","were","be","been","being","has","have","had","do","does","did","will","would","shall","should","may","might","can","could","he","she","it","they","we","you","i","his","her","their","our","your","him","them","us","this","that","these","those","who","whom","which","what","when","then","now","however","indeed","also","only","if","not"}

def words(s):
    return [x for x in re.sub(r"[^a-z0-9 ]+"," ",(s or "").lower()).split() if x]
def stem(w):
    for suf in ("ing","ed","es","s"):
        if len(w)>5 and w.endswith(suf): return w[:-len(suf)]
    return w

total=0; candidates=[]
for ch in range(1,29):
    p=ROOT/f"{ch:02}.json"
    d=json.loads(p.read_text())
    for v in d.get("verses",[]):
        A=v.get("alignment",{}); G=A.get("greek",[]); D=A.get("dgt",[]); L=A.get("literal",[])
        used={i for t in D for i in (t.get("ids") or [])}
        for g in G:
            ids=g.get("ids") or []
            if not ids or any(i in used for i in ids): continue
            gid=ids[0]
            source=[]
            source += words(g.get("gloss"))
            for t in L:
                if gid in (t.get("ids") or []): source += words(t.get("text"))
            key={stem(w) for w in source if w not in STOP and len(w)>2}
            if not key: continue
            hits=[]
            for idx,t in enumerate(D):
                tw={stem(w) for w in words(t.get("text")) if w not in STOP and len(w)>2}
                ov=key & tw
                if ov: hits.append((idx,t.get("text",""),sorted(ov)))
            if len(hits)==1:
                total+=1
                candidates.append((ch,v.get("v"),gid,g.get("text",""),g.get("gloss",""),hits[0]))
print(f"HIGH_CONFIDENCE_UNUSED_GREEK_CANDIDATES {total}")
for row in candidates:
    print("M%d:%s %s %s <%s> -> token %d %r overlap=%s"%(
        row[0],row[1],row[2],row[3],row[4],row[5][0],row[5][1],row[5][2]))
