#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('1corinthians',16,23): {
   0:('The',['w1'])
 },
 ('1corinthians',16,24): {
   5:('of',['w6'])
 },
 ('1corinthians',2,7): {
   0:('Rather,',['w1']),
   8:('the',['w7']),
   13:('predestined',['w10'])
 },
 ('1corinthians',2,13): {
   1:('things',['w1']),
   2:('we',['w3']),
   9:('by',['w6']),
   16:('by',['w12']),
   19:('interpreting',['w17']),
   21:('things',['w16']),
   22:('with',['w15']),
   24:('words.',['w15'])
 },
 ('1corinthians',2,15): {
   1:('the',['w1']),
   3:('person',['w1']),
   4:('discerns',['w4']),
   9:('discerned',['w11'])
 },
 ('1corinthians',3,10): {
   7:('to',['w8']),
   9:('like',['w9']),
   10:('a',['w10']),
   16:('a',['w12']),
   18:('and',['w15']),
   20:('builds',['w16']),
   21:('on',['w16']),
   22:('it.',['w16']),
   23:('But',['w18']),
   24:('let',['w19']),
   27:('watch',['w19']),
   29:('they',['w21']),
   31:('on',['w21'])
 },
 ('1corinthians',4,8): {
   5:('you',['w5']),
   6:('became',['w5']),
   11:('began',['w8']),
   12:('to',['w8']),
   15:('I',['w10']),
   17:('indeed',['w11']),
   19:('you',['w12']),
   20:('had',['w12']),
   21:('begun',['w12']),
   22:('to',['w12'])
 },
 ('1corinthians',4,18): {
   2:('became',['w8']),
   8:('were',['w3'])
 },
 ('1corinthians',7,17): {
   2:('each',['w8']),
   3:('person',['w8']),
   17:('one.',['w8']),
   19:('so',['w16']),
   21:('direct',['w21']),
   25:('assemblies.',['w19'])
 },
 ('1corinthians',7,40): {
   0:('But',['w2']),
   3:('happier',['w1']),
   7:('as',['w5']),
   8:('she',['w5']),
   9:('is,',['w5']),
   13:('opinion;',['w10']),
   14:('and',['w12']),
   18:('I',['w13']),
   19:('too',['w13'])
 },
 ('1corinthians',5,11): {
   3:('have',['w3']),
   12:('called',['w10']),
   17:('who',['w11']),
   18:('is',['w11']),
   34:('swindler—not',['w22','w25'])
 },
}

LEGITIMATE=[
 'precise-scattered|1corinthians|15|30|w4',
 'precise-scattered|1corinthians|15|45|w4',
 'precise-scattered|1corinthians|2|7|w4',
 'precise-scattered|1corinthians|2|9|w4',
 'precise-scattered|1corinthians|7|17|w8',
 'precise-scattered|1corinthians|8|13|w20',
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 18'
for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=DATA/'master-review-allowlist.json'
obj=json.loads(allow_path.read_text(encoding='utf8')) if allow_path.exists() else {'interactions':[]}
items=set(obj.get('interactions',[])); items.update(LEGITIMATE)
obj['interactions']=sorted(items)
allow_path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {sum(len(x) for x in FIXES.values())} reviewed token corrections across {len(FIXES)} verses')
print(f'Recorded {len(LEGITIMATE)} reviewed legitimate master interactions')
