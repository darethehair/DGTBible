#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('acts',23,6): {
   7:('was',['w9']),
   9:('and',['w12']),
   17:('the',['w17']),
   20:('and',[]),
   23:('am',['w23']),
   31:('am',['w32']),
   32:('being',['w32'])
 },
 ('2corinthians',11,2): {
   7:('a',['w5'])
 },
 ('2corinthians',3,5): {
   1:('that',['w2']),
   11:('from',['w10']),
   17:('from',['w16'])
 },
 ('2corinthians',8,8): {
   14:('I',['w16']),
   15:('am',['w16'])
 },
 ('acts',21,1): {
   0:('And',['w2']),
   5:('we',['w5']),
   7:('torn',['w6']),
   12:('and',[]),
   13:('set',['w4']),
   16:('ran',['w9']),
   18:('straight',['w9']),
   19:('course',['w9']),
   20:('to',['w11']),
   22:('and',['w15'])
 },
 ('acts',23,15): {
   7:('notify',['w4']),
   10:('to',['w12']),
   18:('you',['w17']),
   19:('were',['w17']),
   20:('going',['w17']),
   22:('determine',['w18']),
   24:('accurately',['w19']),
   27:('concerning',['w21']),
   30:('we',['w23']),
   35:('him',['w33']),
   37:('he',['w28']),
   38:('comes',['w27']),
   39:('near.”',['w27'])
 },
 ('mark',16,20): {
   0:('And',['w2']),
   4:('and',[])
 },
 ('luke',6,23): {
   16:('Their',['w26']),
   20:('do',['w21']),
   22:('same',['w19']),
   25:('the',['w22'])
 },
 ('acts',10,29): {
   17:('summoned',['w10'])
 },
 ('luke',19,19): {
   9:('to',['w8'])
 },
}

LEGITIMATE=[
 'precise-fanout|luke|19|15|w25',
 'precise-fanout|mark|3|21|w12',
 'precise-scattered|2corinthians|11|2|w11',
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 16'
for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=DATA/'master-review-allowlist.json'
obj=json.loads(allow_path.read_text(encoding='utf8')) if allow_path.exists() else {'interactions':[]}
items=set(obj.get('interactions',[])); items.update(LEGITIMATE)
obj['interactions']=sorted(items)
allow_path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {sum(len(x) for x in FIXES.values())} reviewed token corrections across {len(FIXES)} verses')
print(f'Recorded {len(LEGITIMATE)} reviewed legitimate master interactions')
