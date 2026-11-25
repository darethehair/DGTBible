#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('acts',12,21): {
   1:('an',[])
 },
 ('mark',8,3): {
   8:('their',['w8']),
   23:('far',['w17']),
   24:('away.”',['w17'])
 },
 ('luke',20,11): {
   1:('sent',['w4']),
   5:('they',['w6']),
   6:('beat',['w9']),
   9:('that',['w8']),
   10:('one',['w8']),
   11:('also',['w8']),
   16:('empty-handed.',['w13'])
 },
 ('luke',4,12): {
   13:('your',['w14']),
   15:('to',['w10'])
 },
 ('acts',27,13): {
   7:('they',['w7']),
   10:('their',[])
 },
 ('luke',8,17): {
   12:('will',['w14']),
   14:('become',['w14'])
 },
 ('luke',15,22): {
   5:('his',['w8']),
   14:('put',['w16']),
   16:('on',['w16']),
   22:('his',['w24'])
 },
 ('2corinthians',11,1): {
   13:('with',['w10'])
 },
 ('mark',8,2): {
   1:('have',['w1']),
   7:('they',['w9']),
   8:('have',['w9']),
   10:('remained',['w9'])
 },
 ('luke',21,19): {
   1:('your',['w4']),
   6:('your',['w8']),
   7:('lives.',['w7'])
 },
 ('mark',9,36): {
   1:('taking',['w2']),
   5:('stood',['w4']),
   7:('child',['w5']),
   12:('embracing',['w10']),
   14:('child,',['w11'])
 },
 ('luke',1,5): {
   6:('of',['w9']),
   21:('was',[]),
   30:('was',[])
 },
}

LEGITIMATE=[
 'precise-scattered|luke|4|12|w10',
 'precise-scattered|acts|27|13|w10',
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 10'
for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=DATA/'master-review-allowlist.json'
obj=json.loads(allow_path.read_text(encoding='utf8')) if allow_path.exists() else {'interactions':[]}
items=set(obj.get('interactions',[])); items.update(LEGITIMATE)
obj['interactions']=sorted(items)
allow_path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

print(f'Applied {sum(len(x) for x in FIXES.values())} reviewed token corrections across {len(FIXES)} verses')
print(f'Recorded {len(LEGITIMATE)} reviewed legitimate master interactions')
