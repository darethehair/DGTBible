#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('1corinthians',10,26): {
   4:('the',['w1'])
 },
 ('1corinthians',11,2): {
   2:('praise',['w1']),
   4:('because',['w5']),
   12:('hold',['w15']),
   13:('firmly',['w15']),
   14:('to',[]),
   16:('traditions',['w14'])
 },
 ('1corinthians',14,12): {
   2:('you,',['w3']),
   6:('eager',['w5']),
   7:('for',['w7']),
   11:('to',['w15']),
   12:('abound',['w15']),
   14:('the',['w9']),
   17:('of',['w11']),
   18:('the',['w11']),
   19:('assembly.',['w12'])
 },
 ('1corinthians',14,18): {
   4:('I',['w9'])
 },
 ('1corinthians',14,20): {
   3:('do',['w4']),
   5:('become',['w4']),
   7:('in',['w5']),
   8:('your',['w6']),
   9:('thinking;',['w6']),
   10:('rather,',['w7']),
   11:('be',['w10']),
   12:('infants',['w10']),
   13:('in',['w8']),
   15:('but',['w12']),
   16:('become',['w15']),
   17:('mature',['w14']),
   18:('in',['w11']),
   19:('your',['w13'])
 },
 ('1corinthians',14,37): {
   2:('thinks',['w3']),
   3:('he',['w5']),
   4:('is',['w5']),
   9:('let',['w8']),
   10:('him',['w8']),
   19:('are',['w15']),
   20:('a',[]),
   23:('the',['w14'])
 },
 ('1corinthians',14,39): {
   2:('my',['w3']),
   4:('and',[]),
   6:('eagerly',['w4'])
 },
 ('1corinthians',15,18): {
   4:('have',['w4'])
 },
 ('1corinthians',15,25): {
   1:('he',['w3']),
   2:('must',['w1'])
 },
 ('1corinthians',15,34): {
   0:('Wake',['w1']),
   2:('to',['w2']),
   3:('righteousness',['w2']),
   18:('your',['w13'])
 },
}

LEGITIMATE=[
 'precise-scattered|1corinthians|10|22|w2',
 'precise-scattered|1corinthians|10|22|w8',
 'precise-scattered|1corinthians|11|31|w7',
 'precise-scattered|1corinthians|12|19|w9',
 'precise-scattered|1corinthians|14|7|w17',
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 17'
for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=DATA/'master-review-allowlist.json'
obj=json.loads(allow_path.read_text(encoding='utf8')) if allow_path.exists() else {'interactions':[]}
items=set(obj.get('interactions',[])); items.update(LEGITIMATE)
obj['interactions']=sorted(items)
allow_path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {sum(len(x) for x in FIXES.values())} reviewed token corrections across {len(FIXES)} verses')
print(f'Recorded {len(LEGITIMATE)} reviewed legitimate master interactions')
