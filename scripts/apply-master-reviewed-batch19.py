#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('1john',2,4): {
   8:('does',['w11']),
   22:('that',['w16']),
   23:('person.',['w16'])
 },
 ('1john',2,27): {
   18:('for',['w16']),
   20:('to',['w18']),
   40:('just',['w37'])
 },
 ('1john',3,16): {
   4:('come',['w3']),
   5:('to',['w3']),
   20:('down',['w22']),
   21:('our',['w21'])
 },
 ('1john',4,3): {
   4:('does',['w6']),
   8:('is',['w17']),
   10:('from',['w10']),
   14:('is',['w20']),
   15:('the',['w21']),
   16:('spirit',['w21'])
 },
 ('1john',5,18): {
   5:('has',['w5']),
   6:('been',['w5']),
   14:('rather,',['w11']),
   17:('born',['w13']),
   21:('him,',['w18']),
   26:('does',['w23'])
 },
}

LEGITIMATE=[
 'precise-fanout|1corinthians|4|8|w12',
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 19'
for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=DATA/'master-review-allowlist.json'
obj=json.loads(allow_path.read_text(encoding='utf8')) if allow_path.exists() else {'interactions':[]}
items=set(obj.get('interactions',[])); items.update(LEGITIMATE)
obj['interactions']=sorted(items)
allow_path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {sum(len(x) for x in FIXES.values())} reviewed token corrections across {len(FIXES)} verses')
print(f'Recorded {len(LEGITIMATE)} reviewed legitimate master interactions')
