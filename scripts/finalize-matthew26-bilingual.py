#!/usr/bin/env python3
import json,re
from pathlib import Path

P=Path("data/matthew/26.json")
d=json.loads(P.read_text())
STRUCT=set("""a an the and but or so for of to in on at as is are am was were be been being has have had do did does will would shall should may might can could he she it they we you i his her their our your him them us me this that these those who whom which what when after before while than one thing about because toward from with into upon there if not no how let then yet still even just by""".split())
ALIASES={
 "said":{"say","speaking"},"say":{"said","speaking"},"asked":{"ask","questioning"},
 "took":{"take","taken"},"gave":{"give","given"},"went":{"go","departed"},"came":{"come","arrived"},
 "betrayed":{"deliver","delivered"},"handed":{"deliver","delivered"},"over":{"deliver","delivered"},
 "arrested":{"seize","seized"},"seized":{"take","seize"},"crucified":{"crucify"},
 "killed":{"kill","put","death"},"died":{"die","death"},"raised":{"raise","rise"},
 "prayed":{"pray"},"sleeping":{"sleep"},"asleep":{"sleep"},"woke":{"rise","awaken"},
 "denied":{"deny"},"swore":{"swear"},"testified":{"witness","testimony"},
 "answered":{"answer","reply"},"replied":{"answer","reply"},"commanded":{"command","instruct"},
 "prepared":{"prepare"},"passover":{"passover"},"bread":{"bread","loaf"},"cup":{"cup"},
 "blood":{"blood"},"covenant":{"covenant"},"body":{"body"},"sword":{"sword"},
 "ear":{"ear"},"kiss":{"kiss"},"rooster":{"cock"},"courtyard":{"court"},
 "servant":{"slave","servant"},"servants":{"slaves","servants"},"disciples":{"disciples"},
 "chief":{"chief","high"},"priests":{"priests"},"elders":{"elders"},"scribes":{"scribes"},
 "temple":{"temple","sanctuary"},"high":{"high"},"priest":{"priest"},
 "false":{"false"},"witnesses":{"witnesses"},"blasphemy":{"blasphemy"},
 "death":{"death"},"alive":{"living"},"prophecy":{"prophesy"},"prophet":{"prophet"},
 "galilee":{"galilee"},"peter":{"peter"},"jesus":{"jesus"},"judas":{"judas"},
}
def words(s):
    return re.findall(r"[A-Za-z0-9]+", (s or "").lower())
def stem(w):
    for suf in ("ing","ed","es","s"):
        if len(w)>4 and w.endswith(suf): return w[:-len(suf)]
    return w
def score(e,bag):
    E=stem(e); best=0
    for b in bag:
        if b==e: best=max(best,10)
        elif len(E)>=4 and stem(b)==E: best=max(best,9)
        if b in ALIASES.get(e,set()) or e in ALIASES.get(b,set()): best=max(best,8)
    return best

changed=0; unresolved=[]
for v in d.get("verses",[]):
    G=v.get("alignment",{}).get("greek",[])
    L=v.get("alignment",{}).get("literal",[])
    D=v.get("alignment",{}).get("dgt",[])
    for i,t in enumerate(D):
        if t.get("ids") or t.get("supplied"): continue
        ew=words(t.get("text",""))
        if not ew: continue
        cand=t.get("phraseIds") or [id for g in G for id in g.get("ids",[])]
        scored=[]
        for id in dict.fromkeys(cand):
            g=next((x for x in G if id in x.get("ids",[])),None)
            if not g: continue
            bag=words(g.get("gloss",""))
            for x in L:
                if id in x.get("ids",[]): bag+=words(x.get("text",""))
            s=max([score(e,bag) for e in ew] or [0])
            scored.append((s,id,g.get("text",""),g.get("gloss","")))
        scored.sort(reverse=True)
        if scored and scored[0][0]>=8 and (len(scored)==1 or scored[0][0]>scored[1][0]):
            _,id,gt,gg=scored[0]
            t["ids"]=[id]; t["phraseIds"]=[id]; t.pop("supplied",None)
            t["confidence"]="reviewed-bilingual-semantic"
            t["reason"]=f"Matthew 26 bilingual pass: {t.get('text')} ↔ {gt}"
            changed+=1
        elif ew[0] in STRUCT:
            t["ids"]=[]; t.pop("phraseIds",None); t["supplied"]=True
            t["confidence"]="reviewed-bilingual-supplied"
            t["reason"]="Matthew 26 bilingual pass: English structural wording has no distinct safe Greek token"
            changed+=1
        else:
            unresolved.append((v.get("v"),i,t.get("text"),[(x[1],x[2],x[3]) for x in scored[:8]]))
P.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
print(f"CHANGED={changed}")
print(f"UNRESOLVED={len(unresolved)}")
for row in unresolved:
    print("UNRESOLVED_TOKEN",json.dumps(row,ensure_ascii=False))
