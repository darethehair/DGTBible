#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('mark',14,14): {
   11:('‘The',['w9']),
   14:('Where',['w12'])
 },
 ('mark',14,28): {
   2:('I',['w5']),
   3:('am',['w4'])
 },
 ('mark',3,5): {
   29:('his',['w26'])
 },
 ('mark',8,23): {
   25:('him,',['w21']),
   29:('him,',['w23'])
 },
 ('mark',8,7): {
   13:('them',[])
 },
 ('mark',9,33): {
   7:('he',['w9']),
   8:('was',['w9'])
 },
 ('mark',10,38): {
   11:('are',['w9']),
   13:('Are',['w10']),
   14:('you',['w10']),
   15:('able',['w10']),
   16:('to',['w11']),
   17:('drink',['w11']),
   26:('baptized',['w23']),
   30:('with',['w20']),
   34:('baptized?”',['w22'])
 },
 ('mark',10,39): {
   13:('“The',['w11']),
   25:('with',['w21'])
 },
 ('mark',10,40): {
   8:('my',['w6']),
   16:('it',[]),
   17:('is',[])
 },
 ('matthew',3,12): {
   12:('his',['w12'])
 },
 ('matthew',20,11): {
   0:('And',['w2']),
   4:('it,',[])
 },
 ('matthew',20,23): {
   25:('it',[])
 },
 ('matthew',28,17): {
   2:('they',['w2'])
 },
}

LEGITIMATE=[
 'precise-fanout|mark|10|39|w24',
 'precise-scattered|mark|10|39|w24',
 'precise-fanout|mark|12|4|w10',
 'precise-fanout|matthew|1|19|w12',
 'precise-fanout|matthew|7|10|w8',
 'precise-scattered|matthew|7|10|w8',
 'precise-fanout|matthew|10|25|w19',
 'precise-fanout|matthew|12|11|w23',
 'precise-fanout|matthew|21|5|w20',
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 8'

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
