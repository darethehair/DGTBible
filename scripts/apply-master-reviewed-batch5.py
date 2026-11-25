#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('2timothy',4,4): {
   4:('their',['w7'])
 },
 ('acts',12,19): {
   3:('searched',['w3']),
   16:('ordered',['w11']),
   23:('execution.',['w12']),
   25:('he',['w14'])
 },
 ('acts',13,11): {
   22:('time.”',['w17']),
   27:('fell',['w20']),
   32:('around,',['w27']),
   39:('him',['w29']),
   41:('the',['w29'])
 },
 ('acts',16,22): {
   13:('their',['w11']),
   17:('them',[])
 },
 ('acts',26,10): {
   9:('shut',['w14']),
   15:('ones',['w10']),
   35:('my',[])
 },
 ('colossians',2,20): {
   5:('to',['w7']),
   23:('regulations:',['w17'])
 },
 ('colossians',3,10): {
   6:('man,',[]),
   7:('who',['w5'])
 },
 ('colossians',4,4): {
   5:('it',['w3']),
   8:('I',['w6']),
   9:('ought',['w5'])
 },
}

LEGITIMATE=[
 'precise-fanout|2timothy|2|11|w8',
 'precise-fanout|2timothy|2|12|w4',
 'precise-fanout|2timothy|2|26|w2',
 'precise-fanout|acts|12|19|w12',
 'precise-fanout|acts|13|11|w29',
 'precise-fanout|acts|13|19|w8',
 'precise-fanout|acts|16|11|w6',
 'precise-fanout|acts|16|22|w15',
 'precise-fanout|acts|21|25|w19',
 'precise-fanout|acts|23|24|w5',
 'precise-fanout|acts|28|10|w8',
 'precise-fanout|colossians|1|9|w17',
 'precise-fanout|colossians|2|20|w17',
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 5'

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
