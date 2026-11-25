#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('luke',19,22): {
   14:('You',['w12']),16:('did',['w12']),17:('you,',['w12']),30:('put',['w21'])
 },
 ('galatians',5,11): {
   4:('I',['w7'])
 },
 ('luke',14,12): {
   20:('invite',['w13']),21:('your',['w16']),27:('or',['w25']),29:('neighbors,',['w26'])
 },
 ('acts',27,20): {
   14:('was',['w14']),15:('pressing',['w14']),16:('upon',['w14']),
   22:('would',['w20']),23:('be',['w20']),26:('finally',['w15']),
   27:('being',['w16']),28:('taken',['w16']),29:('away.',['w16'])
 },
 ('galatians',4,15): {
   3:('your',['w6']),13:('you',['w16']),14:('would',['w16']),15:('have',['w16']),
   18:('your',['w15'])
 },
 ('mark',9,45): {
   16:('to',['w13']),21:('to',['w22']),22:('have',['w22']),29:('Gehenna.',['w26'])
 },
 ('mark',14,12): {
   25:('to',['w18']),31:('to',['w21'])
 },
 ('mark',14,31): {
   7:('I',['w8']),8:('must',['w7']),23:('the',['w15'])
 },
 ('acts',18,4): {
   0:('And',['w2']),8:('and',['w10'])
 },
 ('galatians',6,11): {
   1:('with',['w4'])
 },
 ('luke',22,55): {
   0:('When',['w1'])
 },
}

LEGITIMATE=[
 'precise-fanout|galatians|4|13|w8',
 'precise-fanout|mark|15|42|w10',
 'precise-scattered|luke|19|22|w21',
 'precise-scattered|galatians|5|11|w10',
 'precise-scattered|luke|14|12|w31',
 'precise-scattered|mark|14|31|w14',
 'precise-scattered|1corinthians|4|15|w5',
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 12'
for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=DATA/'master-review-allowlist.json'
obj=json.loads(allow_path.read_text(encoding='utf8')) if allow_path.exists() else {'interactions':[]}
items=set(obj.get('interactions',[])); items.update(LEGITIMATE)
obj['interactions']=sorted(items)
allow_path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {sum(len(x) for x in FIXES.values())} reviewed token corrections across {len(FIXES)} verses')
print(f'Recorded {len(LEGITIMATE)} reviewed legitimate master interactions')
