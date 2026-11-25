#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(ROOT/'scripts'/'master-nt-review.py')], check=True, stdout=subprocess.DEVNULL)
rows=[]
with (ROOT/'master-review'/'ranked-review.jsonl').open(encoding='utf8') as f:
    for line in f:
        r=json.loads(line)
        if r.get('book')=='Acts':
            rows.append(r)
print(f"ACTS_MASTER_TAIL_COUNT={len(rows)}")
for r in rows:
    print(json.dumps(r,ensure_ascii=False,sort_keys=True))
