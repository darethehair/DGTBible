#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter

# Independently reviewed lexical hover targets for representative born-aligned
# 1 Corinthians 5-8 cases.  These are deliberately content words where a
# reasonably precise Greek target can be identified.  They are not generated
# from the authored segment ranges being tested.
CASES = [
 (5,1,"immorality",1,["w5"]),(5,1,"immorality",2,["w8"]),(5,1,"Gentiles:",1,["w13"]),
 (5,1,"father’s",1,["w19"]),(5,5,"destruction",1,["w7"]),(5,5,"spirit",1,["w12"]),
 (5,5,"saved",1,["w13"]),(5,7,"Passover,",1,["w16"]),(5,7,"Christ,",1,["w21"]),
 (5,7,"sacrificed.",1,["w20"]),(5,11,"greedy",1,["w14"]),(5,11,"idolater",1,["w16"]),
 (5,13,"God",1,["w5"]),(5,13,"wicked",1,["w10"]),
 (6,9,"unrighteous",1,["w5"]),(6,9,"idolaters,",1,["w15"]),(6,9,"adulterers,",1,["w17"]),
 (6,11,"washed,",1,["w6"]),(6,11,"sanctified,",1,["w8"]),(6,11,"justified",1,["w10"]),
 (6,11,"Spirit",1,["w22"]),(6,12,"permitted",1,["w3"]),(6,12,"mastered",1,["w14"]),
 (6,16,"prostitute",1,["w8"]),(6,16,"body",1,["w10"]),(6,16,"says,",1,["w14"]),
 (6,16,"two",1,["w16"]),(6,16,"flesh.”",1,["w18"]),(6,19,"body",1,["w6"]),
 (6,19,"temple",1,["w8"]),(6,19,"Holy",1,["w12"]),(6,19,"God,",1,["w18"]),
 (7,1,"wrote:",1,["w4"]),(7,1,"good",1,["w6"]),(7,1,"touch",1,["w10"]),
 (7,5,"deprive",1,["w2"]),(7,5,"agreement",1,["w8"]),(7,5,"prayer,",1,["w17"]),
 (7,5,"Satan",1,["w29"]),(7,5,"self-control.",1,["w32"]),
 (7,14,"sanctified",1,["w1"]),(7,14,"husband",1,["w4"]),(7,14,"wife,",1,["w9"]),
 (7,21,"concern",1,["w5"]),(7,21,"free,",1,["w10"]),(7,22,"freed",1,["w7"]),
 (7,22,"free",1,["w13"]),(7,32,"concern.",1,["w4"]),(7,32,"concerned",1,["w8"]),
 (7,36,"improperly",1,["w4"]),(7,36,"virgin,",1,["w7"]),(7,36,"marry.",1,["w22"]),
 (7,39,"bound",1,["w2"]),(7,39,"free",1,["w18"]),(7,39,"Lord.",1,["w25"]),
 (8,1,"knowledge.”",1,["w8"]),(8,1,"Knowledge",1,["w11"]),(8,1,"love",1,["w15"]),
 (8,4,"eating",1,["w3"]),(8,4,"idol",1,["w10"]),(8,4,"God",1,["w16"]),
 (8,6,"God,",1,["w4"]),(8,6,"Father,",1,["w6"]),(8,6,"Lord,",1,["w17"]),
 (8,6,"Jesus",1,["w18"]),(8,6,"Christ,",1,["w19"]),(8,7,"knowledge",1,["w6"]),
 (8,7,"familiarity",1,["w10"]),(8,7,"defiled.",1,["w24"]),(8,10,"knowledge,",1,["w8"]),
 (8,10,"temple,",1,["w10"]),(8,10,"conscience",1,["w14"]),(8,10,"weak,",1,["w16"]),
 (8,10,"built",1,["w18"]),(8,13,"food",1,["w3"]),(8,13,"stumble,",1,["w4"]),
 (8,13,"meat,",1,["w11"]),(8,13,"stumble.",1,["w20"]),
]

def load_verse(ch,v):
    d=json.loads((Path("data/1corinthians")/f"{ch:02}.json").read_text(encoding="utf8"))
    return next(x for x in d["verses"] if x["v"]==v)

def nth_token(items,text,n):
    found=[x for x in items if x.get("text")==text]
    return found[n-1] if len(found)>=n else None

counts=Counter()
rows=[]
for ch,v,text,n,expected in CASES:
    verse=load_verse(ch,v)
    item=nth_token(verse["alignment"]["dgt"],text,n)
    if item is None:
        status="missing"
        actual=[]
    else:
        actual=item.get("ids",[])
        A=set(actual); E=set(expected)
        if not actual:
            status="missing"
        elif A==E:
            status="exact"
        elif E <= A:
            status="over-broad"
        elif A & E:
            status="partial/wrong"
        else:
            status="wrong"
    counts[status]+=1
    rows.append((ch,v,text,expected,actual,status))

total=len(rows)
print(f"HOVER PRECISION AUDIT: {total} independently reviewed lexical targets")
for k in ["exact","over-broad","missing","partial/wrong","wrong"]:
    n=counts[k]
    print(f"{k:13} {n:3}  {n/total*100:5.1f}%")
print("\nDETAIL")
for ch,v,text,expected,actual,status in rows:
    print(f"1Cor {ch}:{v:<2} {text:<16} expected={','.join(expected):<12} actual={','.join(actual):<40} {status}")

# This audit is diagnostic for now.  It deliberately does not fail CI until
# we establish a baseline and improve the authored representation.
