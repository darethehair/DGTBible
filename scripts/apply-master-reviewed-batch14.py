#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('philippians',3,12): {
   1:('that',['w2']),15:('press',['w8']),16:('on,',['w8']),
   20:('may',['w12']),21:('take',['w12']),
   30:('taken',['w16']),31:('hold',['w16']),32:('of',['w16'])
 },
 ('acts',27,16): {
   2:('the',[]),4:('of',[])
 },
 ('mark',16,11): {
   15:('did',['w9']),16:('not',['w9']),17:('believe.',['w9'])
 },
 ('acts',12,20): {
   2:('was',['w1']),20:('persuading',['w15']),23:('was',['w17']),
   29:('asked',['w23']),34:('country',['w30']),35:('was',['w27']),
   36:('fed',['w27']),40:('country.',['w33'])
 },
 ('1corinthians',14,2): {
   0:('For',['w2']),4:('speaks',['w3']),10:('to',['w6']),11:('people',['w6']),
   15:('for',['w12']),18:('understands;',['w13']),23:('speaks',['w16'])
 },
 ('luke',5,11): {
   2:('they',['w2']),3:('had',['w2'])
 },
 ('luke',6,9): {
   14:('to',['w13']),18:('to',['w15']),19:('do',['w15']),20:('harm,',['w15']),
   28:('it?”',['w16'])
 },
 ('luke',4,22): {
   2:('speaking',['w3']),9:('the',['w8']),10:('gracious',['w11']),
   12:('coming',['w13']),13:('from',['w14']),14:('his',['w17'])
 },
 ('john',16,26): {
   18:('ask',['w16']),21:('concerning',['w19'])
 },
 ('acts',27,18): {
   3:('were',['w3'])
 },
 ('john',11,43): {
   14:('out!”',['w9'])
 },
 ('luke',19,2): {
   3:('was',[]),16:('was',['w14'])
 },
}

LEGITIMATE=[
 'precise-scattered|mark|16|11|w1',
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 14'
for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=DATA/'master-review-allowlist.json'
obj=json.loads(allow_path.read_text(encoding='utf8')) if allow_path.exists() else {'interactions':[]}
items=set(obj.get('interactions',[])); items.update(LEGITIMATE)
obj['interactions']=sorted(items)
allow_path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {sum(len(x) for x in FIXES.values())} reviewed token corrections across {len(FIXES)} verses')
print(f'Recorded {len(LEGITIMATE)} reviewed legitimate master interactions')
