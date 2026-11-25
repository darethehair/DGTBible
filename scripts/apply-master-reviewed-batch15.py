#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('1john',5,1): {
   20:('gave',['w18']),
   26:('born',['w22'])
 },
 ('mark',3,26): {
   9:('is',['w9']),
   15:('has',['w15'])
 },
 ('1corinthians',15,8): {
   5:('to',['w5']),
   8:('born,',['w6'])
 },
 ('1thessalonians',2,7): {
   1:('we',['w1']),
   2:('could',['w1']),
   3:('have',['w4']),
   4:('been',['w4']),
   5:('a',['w3']),
   6:('burden',['w3'])
 },
 ('luke',1,3): {
   7:('followed',['w3']),
   12:('start,',['w4']),
   13:('to',['w9']),
   15:('it',['w9']),
   20:('orderly',['w7']),
   21:('sequence,',['w7'])
 },
 ('mark',4,30): {
   7:('compare',['w4']),
   13:('with',['w10']),
   14:('what',['w11']),
   16:('shall',['w14']),
   17:('we',['w14']),
   18:('set',['w14']),
   20:('forth?',['w14'])
 },
 ('luke',19,15): {
   2:('he',['w6']),
   8:('he',['w11']),
   9:('ordered',['w11']),
   11:('those',['w14']),
   12:('slaves',['w15']),
   22:('to',['w13']),
   24:('so',['w21']),
   26:('he',['w22']),
   33:('in',['w25']),
   34:('business.',['w25'])
 },
 ('mark',3,21): {
   6:('they',['w6']),
   12:('of',['w7']),
   20:('out',['w12']),
   21:('of',['w12']),
   22:('his',['w12']),
   23:('mind.”',['w12'])
 },
 ('luke',19,33): {
   2:('were',['w1']),
   6:('its',['w9']),
   7:('owners',['w8']),
   12:('are',['w13']),
   14:('untying',['w13'])
 },
 ('colossians',3,21): {
   4:('your',['w7']),
   6:('so',['w8']),
   9:('do',['w10'])
 },
}

LEGITIMATE=[
 'precise-fanout|philippians|3|12|w16',
 'precise-scattered|1corinthians|15|8|w8',
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 15'
for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=DATA/'master-review-allowlist.json'
obj=json.loads(allow_path.read_text(encoding='utf8')) if allow_path.exists() else {'interactions':[]}
items=set(obj.get('interactions',[])); items.update(LEGITIMATE)
obj['interactions']=sorted(items)
allow_path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {sum(len(x) for x in FIXES.values())} reviewed token corrections across {len(FIXES)} verses')
print(f'Recorded {len(LEGITIMATE)} reviewed legitimate master interactions')
