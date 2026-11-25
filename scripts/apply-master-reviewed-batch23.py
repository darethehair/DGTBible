#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('2peter',1,15): {
   5:('every',['w1'])
 },
 ('2peter',2,2): {
   6:('ways,',['w6'])
 },
 ('2peter',2,5): {
   18:('he',['w15'])
 },
 ('2peter',2,6): {
   13:('to',['w7'])
 },
 ('2timothy',2,6): {
   6:('the',[])
 },
 ('acts',10,2): {
   2:('man',['w1'])
 },
 ('acts',10,21): {
   15:('are',['w19']),
   16:('looking',['w19']),
   17:('for.',['w19'])
 },
 ('acts',10,22): {
   5:('a',['w6']),
   15:('of',['w12']),
   26:('a',['w22']),
   30:('summon',['w24']),
   37:('words',['w32'])
 },
 ('acts',10,31): {
   9:('your',['w11'])
 },
 ('acts',10,43): {
   2:('one',['w1']),
   13:('him',['w17']),
   16:('of',['w7']),
   19:('his',['w12'])
 },
 ('acts',10,44): {
   6:('words,',['w6'])
 },
 ('acts',10,45): {
   12:('astonished',['w2']),
   14:('the',['w16']),
   17:('the',['w18']),
   21:('also',['w12']),
   26:('the',['w14'])
 },
 ('acts',11,11): {
   2:('at',['w3']),
   13:('we',['w12']),
   14:('were,',['w12']),
   15:('having',['w13'])
 },
 ('acts',11,12): {
   0:('And',['w2']),
   5:('to',['w6']),
   9:('without',['w9']),
   10:('making',['w9']),
   11:('any',['w9']),
   12:('distinction.',['w9']),
   23:('the',['w22'])
 },
 ('acts',11,13): {
   0:('And',['w2']),
   8:('the',['w6']),
   20:('summon',['w21']),
   24:('surnamed',['w24'])
 },
 ('acts',11,15): {
   1:('as',['w4']),
   3:('began',['w4'])
 },
 ('acts',11,20): {
   13:('to',['w12']),
   15:('and',['w15']),
   21:('Greeks,',['w18']),
   23:('the',['w19']),
   24:('good',['w19']),
   25:('news',['w19']),
   26:('of',[])
 },
 ('acts',11,21): {
   9:('and',['w8'])
 },
}

LEGITIMATE=[
 'precise-scattered|2timothy|2|19|w18',
 'precise-scattered|2timothy|4|4|w8',
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 23'
for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=DATA/'master-review-allowlist.json'
obj=json.loads(allow_path.read_text(encoding='utf8')) if allow_path.exists() else {'interactions':[]}
items=set(obj.get('interactions',[])); items.update(LEGITIMATE)
obj['interactions']=sorted(items)
allow_path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {sum(len(x) for x in FIXES.values())} reviewed token corrections across {len(FIXES)} verses')
print(f'Recorded {len(LEGITIMATE)} reviewed legitimate master interactions')
