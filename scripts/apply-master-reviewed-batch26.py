#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

# High-confidence removals from the ranked precise-scattered queue.
# Remove only the erroneous precise ID; preserve any other IDs and authored phrase span.
REMOVALS={
 ('acts',14,13): {7:('was','w22')},
 ('acts',14,3): {15:('to','w23')},
 ('acts',15,22): {18:('among','w32')},
 ('acts',15,25): {13:('and','w15')},
 ('acts',15,27): {11:('report','w9')},
 ('acts',15,36): {27:('to','w6')},
 ('acts',15,38): {5:('to','w14')},
 ('acts',15,39): {0:('And','w10')},
 ('acts',15,41): {0:('And','w5')},
 ('acts',16,13): {7:('the','w4')},
 ('acts',16,15): {10:('us,','w25')},
 ('acts',16,18): {0:('And','w11')},
 ('acts',16,25): {8:('and','w6'),13:('and','w6')},
 ('acts',16,26): {0:('And','w18')},
 ('acts',16,27): {15:('and','w6')},
 ('acts',16,29): {0:('And','w5')},
 ('acts',16,3): {14:('him','w28')},
 ('acts',16,30): {1:('he','w5')},
}

changed={}
count=0
for (slug,ch,vnum),edits in REMOVALS.items():
    path=DATA/slug/f'{ch:02}.json'
    d=changed.get(path)
    if d is None:
        d=json.loads(path.read_text(encoding='utf8')); changed[path]=d
    verse=next((v for v in d['verses'] if v['v']==vnum),None)
    if verse is None:
        raise SystemExit(f'missing verse {slug} {ch}:{vnum}')
    D=verse['alignment']['dgt']
    for idx,(expected,bad_id) in edits.items():
        if idx>=len(D) or D[idx].get('text')!=expected:
            got=D[idx].get('text') if idx<len(D) else '<missing>'
            raise SystemExit(f'{slug} {ch}:{vnum} token {idx}: expected {expected!r}, got {got!r}')
        ids=list(D[idx].get('ids',[]))
        if bad_id not in ids:
            raise SystemExit(f'{slug} {ch}:{vnum} token {idx}: expected precise id {bad_id} in {ids}')
        D[idx]['ids']=[x for x in ids if x!=bad_id]
        D[idx]['confidence']='reviewed-master-narrowed'
        D[idx]['reason']='Human-reviewed full-NT master pass batch 26: removed unrelated precise source link'
        count+=1

for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

print(f'Applied {count} reviewed precise-link removals across {len(REMOVALS)} verses')
