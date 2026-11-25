#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('1peter',4,2): {
   2:('to',['w13']),
   12:('for',['w4']),
   17:('the',['w7'])
 },
 ('1peter',4,12): {
   11:('that',['w11']),
   12:('is',['w11']),
   13:('happening',['w11'])
 },
 ('1peter',5,4): {
   5:('is',['w2']),
   10:('the',['w6'])
 },
 ('1thessalonians',2,2): {
   2:('we',['w3']),
   3:('had',['w3']),
   16:('boldly',['w10']),
   24:('the',['w18']),
   31:('struggle.',['w24'])
 },
 ('1thessalonians',2,19): {
   12:('our',['w17']),
   18:('Is',[])
 },
 ('1thessalonians',3,1): {
   2:('we',['w3']),
   7:('it,',['w3']),
   8:('we',['w4']),
   9:('were',['w4']),
   10:('pleased',['w4'])
 },
 ('1thessalonians',3,3): {
   0:('so',['w1']),
   1:('that',['w1']),
   4:('would',['w3']),
   6:('shaken',['w3']),
   17:('appointed',['w14'])
 },
 ('1thessalonians',3,4): {
   0:('For',['w2']),
   1:('even',['w1']),
   14:('were',['w10']),
   15:('going',['w10']),
   17:('be',['w11']),
   18:('afflicted,',['w11']),
   19:('just',['w12']),
   23:('happened',['w14'])
 },
 ('1thessalonians',3,10): {
   3:('praying',['w5']),
   4:('exceedingly',['w4']),
   11:('complete',['w13']),
   16:('your',['w18'])
 },
 ('1thessalonians',4,7): {
   2:('did',['w3']),
   6:('for',['w7']),
   9:('in',['w10'])
 },
 ('1thessalonians',4,15): {
   3:('say',['w4']),
   6:('by',['w5']),
   10:('the',['w7']),
   13:('who',['w10']),
   16:('who',['w12']),
   18:('until',['w14']),
   19:('the',['w15']),
   24:('will',['w21']),
   29:('who',['w23']),
   30:('have',['w23'])
 },
 ('1thessalonians',5,2): {
   15:('like',['w9']),
   18:('in',['w11'])
 },
 ('1thessalonians',5,18): {
   9:('for',['w11'])
 },
}

LEGITIMATE=[
 'precise-fanout|1john|3|16|w3',
 'precise-scattered|1peter|5|4|w2',
 'precise-scattered|1thessalonians|2|2|w10',
 'precise-scattered|1thessalonians|5|19|w4',
 'precise-scattered|1thessalonians|5|20|w3',
 'precise-scattered|1thessalonians|5|26|w6',
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 20'
for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=DATA/'master-review-allowlist.json'
obj=json.loads(allow_path.read_text(encoding='utf8')) if allow_path.exists() else {'interactions':[]}
items=set(obj.get('interactions',[])); items.update(LEGITIMATE)
obj['interactions']=sorted(items)
allow_path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {sum(len(x) for x in FIXES.values())} reviewed token corrections across {len(FIXES)} verses')
print(f'Recorded {len(LEGITIMATE)} reviewed legitimate master interactions')
