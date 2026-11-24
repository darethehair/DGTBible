#!/usr/bin/env python3
import json
from collections import defaultdict,Counter
from pathlib import Path

rows=[]
# Explicitly reviewed multiword renderings that are semantically correct even\n# though one Greek source ID spans separated English words.\nACCEPTED_PRECISE={('Acts 13:19','w8')}\nfor ch in range(1,29):
    p=Path("data/acts")/f"{ch:02}.json"
    if not p.exists(): continue
    d=json.loads(p.read_text(encoding="utf8"))
    for verse in d.get("verses",[]):
        dgt=verse.get("alignment",{}).get("dgt",[])
        greek=verse.get("alignment",{}).get("greek",[])
        gc=max(1,len(greek)); ec=max(1,len(dgt))
        ref=f"Acts {ch}:{verse['v']}"

        # Phrase-only fallbacks: >=4 is automatically review-worthy; 2-3 are
        # also queued when they consume a large fraction of a short verse.
        for tok in dgt:
            if tok.get("ids"): continue
            span=list(dict.fromkeys(tok.get("phraseIds",[])))
            if not span: continue
            frac=len(span)/gc
            if len(span)>=4 or (len(span)>=2 and frac>=0.45):
                rows.append(("phrase-fallback",ref,tok.get("text",""),len(span),gc,frac))

        byid=defaultdict(list); positions=defaultdict(list)
        for i,tok in enumerate(dgt):
            for wid in tok.get("ids",[]):
                byid[wid].append(tok.get("text",""))
                positions[wid].append(i)

        for wid,words in byid.items():
            if (ref,wid) in ACCEPTED_PRECISE: continue
            frac=len(words)/ec
            # Four English words from one Greek token is review-worthy;
            # 2-3 words are queued when scattered or unusually dominant.
            if len(words)>=4 or frac>=0.40:
                rows.append(("precise-fanout",ref,wid,len(words),ec,frac))

        for wid,pos in positions.items():
            if (ref,wid) in ACCEPTED_PRECISE: continue
            if len(pos)<2: continue
            groups=1
            for i in range(1,len(pos)):
                if pos[i]!=pos[i-1]+1: groups+=1
            span=(pos[-1]-pos[0]+1)/ec
            if groups>=2 and (len(pos)>=2 and span>=0.25):
                rows.append(("precise-scattered",ref,wid,len(pos),ec,span))

        # Repeated English helper words mapping to one source ID are a known
        # failure mode from Luke; queue even when only two occurrences exist.
        helpers={"do","does","did","will","would","be","been","being","have","has","had",
                 "you","he","she","they","we","i","it","not","and","but","so"}
        norm=lambda s: ''.join(c.lower() for c in s if c.isalnum())
        for wid,words in byid.items():
            c=Counter(norm(w) for w in words)
            for w,n in c.items():
                if w in helpers and n>=2:
                    rows.append(("repeated-helper",ref,f"{wid}:{w}",n,ec,n/ec))

# Deduplicate, rank widest/scattered first, but keep small structural cases.
uniq=[];seen=set()
for r in rows:
    k=r[:5]
    if k not in seen:
        seen.add(k);uniq.append(r)
rows=sorted(uniq,key=lambda r:(-r[3],-r[5],r[1],r[0],r[2]))
print(f"ACTS HOVER REVIEW QUEUE: {len(rows)} suspicious interactions across {len({r[1] for r in rows})} verses")
for r in rows[:250]:
    print("\t".join([r[0],r[1],r[2],str(r[3]),str(r[4]),f"{r[5]*100:.1f}%"]))

# Catastrophic guard only.  The review queue itself is deliberately not a
# pass/fail shortcut: it is intended for explicit human/model inspection.
major=[r for r in rows if r[3]>=20]
if major:
    raise SystemExit(f"Acts catastrophic hover breadth: {len(major)} cases >=20")
