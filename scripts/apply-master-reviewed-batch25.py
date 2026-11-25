#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('acts',11,5): {
   19:('coming',['w12'])
 },
 ('acts',13,24): {
   15:('of',[])
 },
 ('acts',13,28): {
   2:('they',['w5']),
   12:('have',['w8'])
 },
 ('acts',13,29): {
   10:('they',['w9'])
 },
 ('acts',13,38): {
   3:('be',['w3'])
 },
 ('acts',13,41): {
   27:('in',[])
 },
 ('acts',13,42): {
   2:('were',['w1'])
 },
 ('acts',13,43): {
   0:('And',['w2']),
   13:('devout',['w11']),
   14:('proselytes',['w12']),
   23:('and',[])
 },
 ('acts',13,51): {
   1:('they',['w3'])
 },
 ('acts',14,1): {
   14:('in',['w17']),
   15:('such',['w17']),
   16:('a',['w17'])
 },
 ('acts',14,6): {
   0:('they',['w1']),
   4:('it',[])
 },
 ('acts',14,14): {
   9:('it,',[]),
   10:('they',[]),
   14:('and',[])
 },
}

LEGITIMATE=[
 'precise-scattered|2corinthians|3|8|w8',
 'precise-scattered|acts|13|32|w4',
]

changed={}
for (slug,ch,vnum),edits in FIXES.items():
    path=DATA/slug/f'{ch:02}.json'
    d=changed.get(path)
    if d is None:
        d=json.loads(path.read_text(encoding='utf8')); changed[path]=d
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 25'
for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=DATA/'master-review-allowlist.json'
obj=json.loads(allow_path.read_text(encoding='utf8')) if allow_path.exists() else {'interactions':[]}
items=set(obj.get('interactions',[])); items.update(LEGITIMATE)
obj['interactions']=sorted(items)
allow_path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {sum(len(x) for x in FIXES.values())} reviewed token corrections across {len(FIXES)} verses')
print(f'Recorded {len(LEGITIMATE)} reviewed legitimate master interactions')
