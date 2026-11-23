#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter

# Independently reviewed lexical targets for newly authored 1 Corinthians 9-10.
CASES=[
 (9,1,"free?",1,["w3"]),(9,1,"apostle?",1,["w6"]),(9,1,"Jesus",1,["w8"]),
 (9,1,"Lord?",1,["w11"]),(9,1,"our",1,["w12"]),(9,1,"work",1,["w16"]),(9,1,"my",1,["w17"]),
 (9,4,"we",1,["w3"]),(9,4,"have",1,["w3"]),(9,4,"right",1,["w4"]),(9,4,"eat",1,["w5"]),(9,4,"drink?",1,["w7"]),
 (9,12,"obstacle",1,["w22"]),(9,12,"gospel",1,["w25"]),(9,12,"Christ.",1,["w27"]),
 (9,24,"know",1,["w2"]),(9,24,"race",1,["w6"]),(9,24,"prize?",1,["w15"]),(9,24,"obtain",1,["w19"]),
 (9,27,"discipline",1,["w2"]),(9,27,"body",1,["w5"]),(9,27,"slavery,",1,["w7"]),
 (9,27,"preaching",1,["w11"]),(9,27,"disqualified.",1,["w13"]),
 (10,6,"examples",1,["w3"]),(10,6,"became",1,["w5"]),(10,6,"we",1,["w10"]),(10,6,"desire",1,["w11"]),
 (10,13,"temptation",1,["w1"]),(10,13,"you",1,["w2"]),(10,13,"you",2,["w15"]),
 (10,13,"temptation",2,["w24"]),(10,13,"way",1,["w27"]),(10,13,"out,",1,["w27"]),
 (10,16,"sharing",1,["w8"]),(10,16,"blood",1,["w11"]),(10,16,"sharing",2,["w19"]),(10,16,"body",1,["w21"]),
 (10,17,"bread,",1,["w3"]),(10,17,"body,",1,["w5"]),(10,17,"partake",1,["w16"]),(10,17,"bread.",1,["w15"]),
 (10,23,"beneficial.",1,["w7"]),(10,23,"permitted,”",2,["w10"]),(10,23,"build",1,["w14"]),(10,23,"up.",1,["w14"]),
 (10,31,"eat",1,["w3"]),(10,31,"drink",1,["w5"]),(10,31,"glory",1,["w11"]),(10,31,"God.",1,["w12"])
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
print(f"HOVER 9-10 AUDIT: {total} independently reviewed lexical targets")
for k in ["exact","over-broad","missing","partial/wrong","wrong"]:
 n=C[k]; print(f"{k:13} {n:3}  {n/total*100:5.1f}%")
print("\nDETAIL")
for ch,v,text,e,a,s in rows:
 print(f"1Cor {ch}:{v:<2} {text:<16} expected={','.join(e):<10} actual={','.join(a):<30} {s}")

if C["wrong"] or C["missing"] or C["over-broad"] or C["partial/wrong"]:
 raise SystemExit(f"HOVER 9-10 REGRESSION: exact={C['exact']}/{total}, over-broad={C['over-broad']}, missing={C['missing']}, wrong={C['wrong']}")
