#!/usr/bin/env python3
import json
from pathlib import Path

CASES=[
 (16,1,"assemblies",1,["w12"]),
 (16,22,"accursed.",1,["w10"]),
]

for ch,v,text,n,expected in CASES:
 d=json.loads((Path("data/1corinthians")/f"{ch:02}.json").read_text(encoding="utf8"))
 verse=next(x for x in d["verses"] if x["v"]==v)
 xs=[x for x in verse["alignment"]["dgt"] if x.get("text")==text]
 if len(xs)<n: raise SystemExit(f"1Cor {ch}:{v} missing DGT token {text!r} occurrence {n}")
 actual=xs[n-1].get("ids",[])
 if actual!=expected:
  raise SystemExit(f"1Cor {ch}:{v} {text!r}: expected {expected}, got {actual}")
 print(f"1Cor {ch}:{v} {text}: exact {actual}")
