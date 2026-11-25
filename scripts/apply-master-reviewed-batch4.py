#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('1thessalonians',5,2): {
   4:('accurately',['w3']),
   6:('the',[]),
   19:('the',[])
 },
 ('1timothy',5,12): {
   7:('their',[])
 },
 ('2corinthians',11,6): {
   7:('I',[]),
   8:('am',[]),
   13:('in',['w12'])
 },
 ('2corinthians',12,1): {
   0:('I',['w2']),
   1:('must',['w2'])
 },
 ('2corinthians',12,19): {
   0:('All',['w1']),
   1:('this',['w1']),
   2:('time',['w1']),
   18:('we',['w11']),
   19:('are',['w11']),
   25:('are',[])
 },
 ('2corinthians',3,17): {
   1:('the',['w1']),
   3:('is',['w6']),
   4:('the',['w4']),
   8:('the',['w9'])
 },
}

LEGITIMATE=[
 'precise-fanout|2corinthians|5|12|w15',
 'precise-fanout|2corinthians|7|14|w9',
 'precise-fanout|2corinthians|9|4|w12',
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
        D[idx]['confidence']='reviewed-master-precise' if new_ids else 'reviewed-master-unaligned'
        D[idx]['reason']='Human-reviewed full-NT master pass batch 4'

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
