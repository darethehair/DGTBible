#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('acts',10,6): {
   1:('is',['w2'])
 },
 ('acts',10,43): {
   8:('that',[])
 },
 ('acts',11,7): {
   0:('And',['w2'])
 },
 ('acts',11,8): {
   0:('But',['w2']),
   6:('because',['w5'])
 },
 ('acts',11,30): {
   0:('And',['w2'])
 },
 ('acts',12,4): {
   0:('After',[])
 },
 ('acts',12,8): {
   16:('Then',['w16']),
   18:('said',['w17']),
   22:('your',['w22'])
 },
 ('acts',12,12): {
   0:('And',['w2'])
 },
 ('acts',12,14): {
   2:('Peter’s',['w6']),
   5:('of',[]),
   15:('ran',['w14']),
   17:('and',[])
 },
 ('acts',12,15): {
   7:('of',[]),
   12:('kept',['w9']),
   16:('was',['w11'])
 },
 ('acts',12,16): {
   4:('and',['w7'])
 },
 ('acts',13,5): {
   4:('in',['w3']),
   8:('the',['w6']),
   13:('the',['w11']),
   23:('an',['w19']),
   24:('assistant.',['w19'])
 },
 ('acts',13,10): {
   0:('and',[]),
   5:('every',['w4']),
   8:('every',['w7']),
   9:('villainy,',['w8']),
   15:('of',['w12']),
   21:('stop',['w15']),
   22:('making',['w16']),
   23:('crooked',['w16']),
   25:('straight',['w22']),
   27:('of',['w20'])
 },
}

LEGITIMATE=[
 'precise-fanout|2peter|1|15|w1',
 'precise-scattered|acts|11|8|w10',
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 24'
for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=DATA/'master-review-allowlist.json'
obj=json.loads(allow_path.read_text(encoding='utf8')) if allow_path.exists() else {'interactions':[]}
items=set(obj.get('interactions',[])); items.update(LEGITIMATE)
obj['interactions']=sorted(items)
allow_path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {sum(len(x) for x in FIXES.values())} reviewed token corrections across {len(FIXES)} verses')
print(f'Recorded {len(LEGITIMATE)} reviewed legitimate master interactions')
