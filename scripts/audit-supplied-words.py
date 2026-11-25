#!/usr/bin/env python3
"""Recover falsely supplied definite articles using an unused adjacent Greek article.

Conservative: a linked following English word must identify a single Greek
word; the immediately preceding Greek word must be an unused article.
Ambiguous candidates are reported, never silently linked.
"""
import argparse
import collections
import json
import re
from pathlib import Path

def norm(s):
    return re.sub(r"[^a-z]", "", s.lower())

def inspect(v):
    a=v["alignment"]
    d,g=a["dgt"],a["greek"]
    used={i for t in d for i in t.get("ids",[])}
    direct=[]
    other=[]
    for i,t in enumerate(d):
        if not t.get("supplied") or t.get("ids"):
            continue
        n=norm(t["text"])
        if n=="the":
            nxt=d[i+1] if i+1<len(d) else {}
            ids=nxt.get("ids",[])
            if len(ids)!=1:
                continue
            j=next((j for j,x in enumerate(g) if ids[0] in x.get("ids",[])), -1)
            if j<1:
                continue
            x=g[j-1]
            if len(x.get("ids",[]))==1 and x["ids"][0] not in used and x.get("morph","").startswith("T-") and x.get("gloss","").lower() in ("the","of the"):
                direct.append((i,x["ids"][0],nxt["text"]))
        elif n:
            matches=[x["ids"][0] for x in g if len(x.get("ids",[]))==1 and x["ids"][0] not in used and norm(x.get("gloss",""))==n]
            if matches:
                other.append((i,t["text"],matches))
    counts=collections.Counter(x[1] for x in direct)
    return [x for x in direct if counts[x[1]]==1], [x for x in direct if counts[x[1]]>1],other

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--apply",action="store_true")
    p.add_argument("--strict",action="store_true",help="fail if clear article candidates remain")
    p.add_argument("--book",default="matthew")
    args=p.parse_args()
    paths=sorted((Path("data")/args.book).glob("[0-9][0-9].json"))
    if args.book=="matthew" and len(paths)!=28:
        raise SystemExit("Expected all 28 Matthew chapters")
    total=ambiguous=other_total=0
    for path in paths:
        data=json.loads(path.read_text(encoding="utf8"))
        dirty=False
        count=0
        for v in data["verses"]:
            direct,amb,other=inspect(v)
            count+=len(direct)
            ambiguous+=len(amb)
            other_total+=len(other)
            for i,id_,nxt in direct:
                print(f"{args.book} {path.stem}:{v['v']} token {i}: the {nxt} -> {id_}")
                if args.apply:
                    t=v["alignment"]["dgt"][i]
                    t.pop("supplied",None)
                    t.update(ids=[id_],phraseIds=[id_],confidence="reviewed-bilingual-article",reason="Unused Greek article directly precedes the uniquely linked following English word")
                    dirty=True
            for row in amb:
                print(f"REVIEW duplicate article {path.stem}:{v['v']} {row}")
            for row in other:
                print(f"REVIEW other supplied {path.stem}:{v['v']} {row}")
        total+=count
        if dirty:
            path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
        print(f"CHAPTER {path.stem}: {count} clear article candidates")
    print(f"SUMMARY chapters={len(paths)} clear_articles={total} ambiguous_articles={ambiguous} other_exact_candidates={other_total}")
    if args.strict and total and not args.apply:
        raise SystemExit(1)
    if args.book=="matthew" and (args.apply or args.strict):
        v=json.loads(Path("data/matthew/19.json").read_text(encoding="utf8"))["verses"][0]
        d=v["alignment"]["dgt"]
        for noun,expected in (("region","w17"),("Jordan","w22")):
            i=next(i for i,t in enumerate(d) if norm(t["text"])==norm(noun))
            assert d[i-1]["ids"]==[expected] and not d[i-1].get("supplied"), (noun,d[i-1])
        print("PASS Matthew 19:1 regression")
if __name__=="__main__":
    main()
