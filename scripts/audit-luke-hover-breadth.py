import json
from collections import defaultdict
from pathlib import Path

rows=[]  # Luke-only CI diagnostic
for ch in range(1,25):
    p=Path("data/luke")/f"{ch:02}.json"
    d=json.loads(p.read_text(encoding="utf8"))
    for verse in d.get("verses",[]):
        dgt=verse.get("alignment",{}).get("dgt",[])
        greek=verse.get("alignment",{}).get("greek",[])
        gc=max(1,len(greek)); ec=max(1,len(dgt))
        ref=f"Luke {ch}:{verse['v']}"

        for tok in dgt:
            if tok.get("ids"): continue
            span=list(dict.fromkeys(tok.get("phraseIds",[])))
            if not span: continue
            frac=len(span)/gc
            if len(span)>=5 and frac>=0.35:
                rows.append(("broad-phrase",ref,tok.get("text",""),len(span),gc,frac))

        byid=defaultdict(list)
        positions=defaultdict(list)
        for i,tok in enumerate(dgt):
            for wid in tok.get("ids",[]):
                byid[wid].append(tok.get("text",""))
                positions[wid].append(i)
        for wid,words in byid.items():
            frac=len(words)/ec
            if len(words)>=5 or frac>=0.35:
                rows.append(("precise-fanout",ref,wid,len(words),ec,frac))
        for wid,pos in positions.items():
            if len(pos)<2: continue
            groups=1
            for i in range(1,len(pos)):
                if pos[i]!=pos[i-1]+1: groups+=1
            span=(pos[-1]-pos[0]+1)/ec
            if groups>=2 and (span>=0.35 or len(pos)>=5):
                rows.append(("precise-scattered",ref,wid,len(pos),ec,span))

rows.sort(key=lambda r:(-r[3],-r[5],r[1]))
major=[r for r in rows if (r[0]=='broad-phrase' and r[3]>=5 and r[5]>=0.35) or r[3]>=20]
maxsize=max((r[3] for r in rows),default=0)
print(f"LUKE HOVER BREADTH: {len(rows)} suspicious interactions; {len({r[1] for r in rows})} verses; major cases={len(major)}; worst={maxsize}")
for r in rows[:40]:
    print("\t".join([r[0],r[1],r[2],str(r[3]),str(r[4]),f"{r[5]*100:.1f}%"]))
if major:
    raise SystemExit(f"Luke hover breadth major cutoff failed: {len(major)} broad/20+ cases")
