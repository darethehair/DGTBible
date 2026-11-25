#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('galatians',4,31): {
   14:('woman.',['w9'])
 },
 ('galatians',5,4): {
   7:('have',['w1']),
   8:('been',['w1'])
 },
 ('hebrews',9,26): {
   2:('would',['w2']),
   3:('have',['w2']),
   4:('had',['w2']),
   7:('many',['w4']),
   8:('times',['w4']),
   9:('since',['w6']),
   10:('the',['w7']),
   19:('appeared',['w24']),
   21:('at',['w12']),
   22:('the',['w13']),
   23:('culmination',['w13']),
   24:('of',['w14']),
   25:('the',['w14']),
   27:('to',['w16'])
 },
 ('james',1,15): {
   13:('gives',['w11']),
   14:('birth',['w11']),
   15:('to',['w11'])
 },
 ('john',1,12): {
   0:('But',['w2']),
   1:('to',['w6']),
   2:('all',['w1']),
   3:('who',['w1']),
   4:('did',['w3']),
   5:('receive',['w3']),
   6:('him',['w4']),
   7:('who',['w11']),
   8:('believed',['w12']),
   9:('in',['w13']),
   10:('his',['w16']),
   11:('name',['w15']),
   12:('he',['w5']),
   13:('gave',['w5']),
   14:('the',[]),
   15:('right',['w7']),
   16:('to',['w10']),
   17:('become',['w10']),
   18:('children',['w8']),
   19:('of',['w9']),
   20:('God',['w9'])
 },
 ('john',2,8): {
   10:('take',['w7']),
   11:('it',['w7']),
   18:('So',['w11']),
   20:('took',['w12']),
   21:('it',['w12'])
 },
 ('john',3,33): {
   3:('has',['w2']),
   5:('his',['w3'])
 },
 ('john',11,12): {
   12:('he',['w9']),
   14:('recover.”',['w9'])
 },
 ('john',19,22): {
   6:('I',['w6']),
   7:('have',['w6'])
 },
}

LEGITIMATE=[
 'precise-fanout|john|1|24|w2',
 'precise-fanout|acts|26|25|w5',
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 6'

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
