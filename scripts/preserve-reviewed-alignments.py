#!/usr/bin/env python3
"""Snapshot and restore human-reviewed DGT alignment decisions around book regeneration."""
import json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def reviewed(x):
    c=str(x.get("confidence",""))
    return c.startswith("reviewed")

def chapter_files(slug):
    return sorted((ROOT/"data"/slug).glob("[0-9][0-9].json"))

def save(slug, out_path):
    rows=[]
    for path in chapter_files(slug):
        d=json.loads(path.read_text(encoding="utf8"))
        for v in d.get("verses",[]):
            for i,x in enumerate(v.get("alignment",{}).get("dgt",[])):
                if not reviewed(x):
                    continue
                fields={}
                for k in ("ids","phraseIds","confidence","reason","supplied"):
                    if k in x:
                        fields[k]=x[k]
                rows.append({
                    "chapter": int(d["chapter"]),
                    "verse": int(v["v"]),
                    "index": i,
                    "text": x.get("text",""),
                    "fields": fields,
                })
    payload={"schema":1,"book":slug,"reviewed_tokens":rows}
    Path(out_path).write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(f"Saved {len(rows)} reviewed {slug} DGT tokens to {out_path}")

def restore(slug, in_path):
    payload=json.loads(Path(in_path).read_text(encoding="utf8"))
    if payload.get("book")!=slug:
        raise SystemExit(f"snapshot book mismatch: {payload.get('book')} != {slug}")
    by_ch={}
    for path in chapter_files(slug):
        d=json.loads(path.read_text(encoding="utf8"))
        by_ch[int(d["chapter"])]=(path,d)
    touched=set(); restored=0
    for row in payload.get("reviewed_tokens",[]):
        ch=int(row["chapter"]); vn=int(row["verse"]); idx=int(row["index"])
        if ch not in by_ch:
            raise SystemExit(f"missing regenerated {slug} chapter {ch}")
        path,d=by_ch[ch]
        verse=next((v for v in d.get("verses",[]) if int(v["v"])==vn),None)
        if verse is None:
            raise SystemExit(f"missing regenerated {slug} {ch}:{vn}")
        D=verse.get("alignment",{}).get("dgt",[])
        if idx>=len(D):
            raise SystemExit(f"reviewed token index drift at {slug} {ch}:{vn} index {idx}")
        x=D[idx]
        if x.get("text","")!=row.get("text",""):
            raise SystemExit(
                f"reviewed token text drift at {slug} {ch}:{vn} index {idx}: "
                f"{x.get('text')!r} != {row.get('text')!r}"
            )
        # Remove review-owned fields first, then restore exactly what was reviewed.
        for k in ("ids","phraseIds","confidence","reason","supplied"):
            x.pop(k,None)
        x.update(row.get("fields",{}))
        touched.add(path); restored+=1
    # Write from the chapter objects retained in by_ch.
    for ch,(path,d) in by_ch.items():
        if path in touched:
            path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(f"Restored {restored} reviewed {slug} DGT tokens across {len(touched)} chapter files")

def main():
    if len(sys.argv)!=4 or sys.argv[1] not in {"save","restore"}:
        raise SystemExit("usage: preserve-reviewed-alignments.py save|restore BOOK SNAPSHOT.json")
    mode,slug,snapshot=sys.argv[1:]
    (save if mode=="save" else restore)(slug,snapshot)

if __name__=="__main__":
    main()
