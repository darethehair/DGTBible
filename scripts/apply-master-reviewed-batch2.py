#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('1corinthians',2,8): {
   15:('they',['w18'])
 },
 ('1corinthians',5,11): {
   33:('a',['w22'])
 },
 ('2corinthians',11,25): {
   0:('Three',['w1']),
   11:('three',['w5']),
   21:('I',['w11']),
   22:('spent',['w11'])
 },
}

LEGITIMATE=[
 'precise-fanout|1corinthians|10|13|w7',
 'precise-fanout|1corinthians|12|13|w25',
 'precise-fanout|1corinthians|13|12|w22',
 'precise-fanout|1corinthians|4|6|w27',
 'precise-fanout|1corinthians|9|17|w12',
 'precise-fanout|1john|2|3|w6',
 'precise-fanout|1peter|3|16|w16',
 'precise-fanout|1timothy|1|10|w2',
 'precise-fanout|1timothy|4|10|w9',
 'precise-fanout|2corinthians|11|25|w2',
 'precise-fanout|2corinthians|11|25|w7',
 'precise-scattered|acts|13|19|w8',
]

changed={}
for (slug,ch,vnum),edits in FIXES.items():
    path=DATA/slug/f'{ch:02}.json'
    d=changed.get(path)
    if d is None:
        d=json.loads(path.read_text(encoding='utf8'))
        changed[path]=d
    verse=next((v for v in d['verses'] if v['v']==vnum),None)
    if verse is None: raise SystemExit(f'missing verse {slug} {ch}:{vnum}')
    D=verse['alignment']['dgt']
    for idx,(expected,new_ids) in edits.items():
        if idx>=len(D) or D[idx].get('text')!=expected:
            got=D[idx].get('text') if idx<len(D) else '<missing>'
            raise SystemExit(f'{slug} {ch}:{vnum} token {idx}: expected {expected!r}, got {got!r}')
        D[idx]['ids']=list(new_ids)
        D[idx].pop('phraseIds',None)
        D[idx]['confidence']='reviewed-master-precise'
        D[idx]['reason']='Human-reviewed full-NT master pass batch 2'

for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=DATA/'master-review-allowlist.json'
obj=json.loads(allow_path.read_text(encoding='utf8')) if allow_path.exists() else {'interactions':[]}
items=set(obj.get('interactions',[]))
items.update(LEGITIMATE)
obj['interactions']=sorted(items)
allow_path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

print(f'Applied {sum(len(x) for x in FIXES.values())} reviewed token corrections across {len(FIXES)} verses')
print(f'Recorded {len(LEGITIMATE)} reviewed legitimate master interactions')
