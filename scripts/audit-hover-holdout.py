#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter

# Holdout lexical targets: intentionally NOT present in authoring precision overrides.
CASES=[
 (5,1,"reported",1,["w2"]),(5,5,"Satan",1,["w5"]),(5,5,"flesh,",1,["w9"]),(5,5,"Lord.",1,["w18"]),
 (5,7,"leaven",1,["w5"]),(5,11,"reviler",1,["w18"]),(5,11,"drunkard",1,["w20"]),
 (6,9,"immoral,",1,["w13"]),(6,11,"Lord",1,["w15"]),(6,11,"Jesus",1,["w17"]),(6,11,"God.",1,["w24"]),
 (6,12,"beneficial.",1,["w7"]),(6,16,"joins",1,["w6"]),(6,19,"Spirit",1,["w13"]),
 (7,1,"woman.”",1,["w8"]),(7,5,"tempt",1,["w26"]),(7,14,"unclean,",1,["w24"]),(7,14,"holy.",1,["w28"]),
 (7,21,"slave?",1,["w1"]),(7,22,"slave",1,["w6"]),(7,22,"Lord’s",1,["w8"]),(7,32,"unmarried",1,["w7"]),
 (7,32,"please",1,["w13"]),(7,36,"prime",1,["w12"]),(7,36,"sinning.",1,["w21"]),
 (8,1,"puffs",1,["w12"]),(8,1,"builds",1,["w16"]),(8,4,"nothing",1,["w9"]),(8,4,"world",1,["w12"]),
 (8,7,"conscience,",1,["w20"]),(8,7,"weak,",1,["w22"]),(8,10,"sees",1,["w4"]),(8,10,"eat",2,["w23"])
]
def verse(ch,v):
 d=json.loads((Path("data/1corinthians")/f"{ch:02}.json").read_text(encoding="utf8"))
 return next(x for x in d["verses"] if x["v"]==v)
def nth(items,text,n):
 xs=[x for x in items if x.get("text")==text]
 return xs[n-1] if len(xs)>=n else None
C=Counter(); rows=[]
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
print(f"HOVER HOLDOUT AUDIT: {total} unseen lexical targets")
for k in ["exact","over-broad","missing","partial/wrong","wrong"]:
 n=C[k];print(f"{k:13} {n:3}  {n/total*100:5.1f}%")
print("\nDETAIL")
for ch,v,text,e,a,s in rows:
 print(f"1Cor {ch}:{v:<2} {text:<16} expected={','.join(e):<10} actual={','.join(a):<40} {s}")
