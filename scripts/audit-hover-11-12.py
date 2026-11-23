# rerun after generated 1 Corinthians 1-12 commit
# rerun after 11:3 precision fix
#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter

CASES=[
 (12,1,"unaware.",1,["w9"]),
 (11,3,"want",1,["w1"]),(11,3,"you",1,["w3"]),(11,3,"know",1,["w4"]),
 (11,3,"Christ",1,["w11"]),(11,3,"head",1,["w9"]),(11,3,"man,",1,["w7"]),
 (11,3,"man",1,["w17"]),(11,3,"God",1,["w23"]),
 (11,10,"authority",1,["w6"]),(11,10,"head",1,["w10"]),(11,10,"angels.",1,["w13"]),
 (11,23,"received",1,["w3"]),(11,23,"Lord",1,["w6"]),(11,23,"delivered",1,["w9"]),
 (11,23,"Jesus,",1,["w14"]),(11,23,"betrayed,",1,["w19"]),(11,23,"bread,",1,["w21"]),
 (11,24,"thanks,",1,["w2"]),(11,24,"my",1,["w9"]),(11,24,"body,",1,["w12"]),
 (11,24,"you.",1,["w15"]),(11,24,"remembrance",1,["w22"]),
 (11,25,"supper,",1,["w7"]),(11,25,"new",1,["w13"]),(11,25,"covenant",1,["w14"]),
 (11,25,"blood.",1,["w19"]),(11,25,"whenever",1,["w22"]),(11,25,"remembrance",1,["w28"]),
 (11,26,"bread",1,["w6"]),(11,26,"cup,",1,["w10"]),(11,26,"death",1,["w14"]),
 (11,26,"Lord",1,["w16"]),(11,26,"proclaim",1,["w17"]),
 (11,29,"judgment",1,["w7"]),(11,29,"themselves",1,["w8"]),(11,29,"discern",1,["w13"]),(11,29,"body.",1,["w15"]),
 (12,3,"can",1,["w15"]),(12,3,"Lord,”",1,["w17"]),(12,3,"Holy",1,["w23"]),(12,3,"Spirit.",1,["w22"]),
 (12,8,"wisdom,",1,["w9"]),(12,8,"knowledge",1,["w13"]),
 (12,10,"discernings",1,["w10"]),(12,10,"interpretation",1,["w18"]),
 (12,11,"distributing",1,["w11"]),(12,11,"one",2,["w13"]),
 (12,13,"one",1,["w4"]),(12,13,"one",2,["w9"]),(12,13,"baptized",1,["w11"]),
 (12,13,"made",1,["w25"]),(12,13,"drink",1,["w25"]),(12,13,"Spirit.",1,["w24"]),
 (12,28,"assembly:",1,["w9"]),(12,28,"administrations,",1,["w22"]),
 (12,31,"desire",1,["w1"]),(12,31,"excellent",1,["w10"]),(12,31,"way.",1,["w11"])
]

def verse(ch,v):
 d=json.loads((Path("data/1corinthians")/f"{ch:02}.json").read_text(encoding="utf8"))
 return next(x for x in d["verses"] if x["v"]==v)

def nth(items,text,n):
 xs=[x for x in items if x.get("text")==text]
 return xs[n-1] if len(xs)>=n else None

C=Counter();rows=[]
for ch,v,text,n,expected in CASES:
 x=nth(verse(ch,v)["alignment"]["dgt"],text,n)
 actual=[] if x is None else x.get("ids",[])
 A=set(actual);E=set(expected)
 if not actual:s="missing"
 elif A==E:s="exact"
 elif E<=A:s="over-broad"
 elif A&E:s="partial/wrong"
 else:s="wrong"
 C[s]+=1;rows.append((ch,v,text,expected,actual,s))

total=len(rows)
print(f"HOVER 11-12 AUDIT: {total} independently reviewed lexical targets")
for k in ["exact","over-broad","missing","partial/wrong","wrong"]:
 n=C[k];print(f"{k:13} {n:3}  {n/total*100:5.1f}%")
print("\nDETAIL")
for ch,v,text,e,a,s in rows:
 print(f"1Cor {ch}:{v:<2} {text:<16} expected={','.join(e):<10} actual={','.join(a):<30} {s}")
if any(C[k] for k in ["over-broad","missing","partial/wrong","wrong"]):
 raise SystemExit(f"HOVER 11-12 REGRESSION: exact={C['exact']}/{total}, over-broad={C['over-broad']}, missing={C['missing']}, wrong={C['wrong']}")
