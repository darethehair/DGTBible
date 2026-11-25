#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('acts',1,6): {
   6:('they',['w5'])
 },
 ('acts',10,17): {
   16:('might',['w10']),
   17:('mean,',['w10']),
   18:('look,',['w16'])
 },
 ('acts',19,40): {
   11:('concerning',['w6']),
   12:('today,',['w8']),
   25:('give',['w16']),
   27:('account',['w17']),
   30:('gathering.”',['w20'])
 },
 ('acts',26,25): {
   7:('of',['w5'])
 },
 ('2corinthians',1,10): {
   0:('He',['w1'])
 },
 ('2corinthians',1,24): {
   9:('we',['w9'])
 },
 ('2corinthians',5,6): {
   8:('we',['w7']),
   9:('are',['w7'])
 },
 ('ephesians',2,8): {
   11:('is',[]),
   13:('from',['w12']),
   17:('the',['w15'])
 },
}

LEGITIMATE=[
 'precise-fanout|acts|19|40|w3',
 'precise-fanout|galatians|2|19|w11',
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 3'

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
