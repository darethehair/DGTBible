#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('2corinthians',13,1): {
   2:('the',[])
 },
 ('2corinthians',13,5): {
   0:('Test',['w2']),
   5:('you',['w4'])
 },
 ('2corinthians',1,6): {
   13:('we',['w11'])
 },
 ('2corinthians',1,9): {
   9:('ourselves,',['w4'])
 },
 ('2corinthians',1,18): {
   8:('is',['w13'])
 },
 ('2corinthians',1,23): {
   1:('I',['w1']),
   10:('to',['w12']),
   13:('I',['w15']),
   14:('did',['w15']),
   15:('not',['w14'])
 },
 ('2corinthians',2,1): {
   4:('for',['w3'])
 },
 ('2corinthians',2,4): {
   19:('you',['w15'])
 },
 ('2corinthians',2,12): {
   4:('to',['w3']),
   7:('the',['w7']),
   11:('and',['w11']),
   14:('was',['w14']),
   16:('for',['w13'])
 },
 ('2corinthians',2,16): {
   0:('to',['w1']),1:('the',['w1']),2:('one',['w1']),
   5:('from',['w4']),7:('to',['w6']),
   9:('and',['w9']),
   10:('to',['w8']),11:('the',['w8']),12:('other',['w8']),
   13:('an',['w10']),15:('from',['w11']),17:('to',['w13'])
 },
 ('2corinthians',4,4): {
   2:('the',['w3']),
   3:('god',['w4']),
   4:('of',['w5']),
   9:('the',['w9']),
   11:('of',['w11']),12:('the',['w11']),
   15:('that',['w13']),
   16:('the',['w14']),
   18:('of',['w20']),19:('the',['w20']),
   21:('of',['w22']),22:('the',['w22'])
 },
 ('2corinthians',4,18): {
   3:('not',['w1']),
   5:('the',['w4']),6:('things',['w4']),
   9:('at',['w2']),
   10:('the',['w7']),11:('things',['w7']),12:('not',['w8']),
   15:('the',['w10']),16:('things',['w10']),
   20:('but',['w15']),
   21:('the',['w14']),22:('things',['w14']),23:('not',['w16'])
 },
 ('2corinthians',5,17): {
   19:('things',['w13']),
   20:('have',['w12'])
 },
 ('2corinthians',6,14): {
   10:('does',['w7']),
   13:('with',['w9']),
   18:('does',['w13']),
   20:('have',['w13']),
   21:('with',['w15'])
 },
 ('2corinthians',7,3): {
   0:('I',['w4']),1:('do',['w4']),3:('say',['w4']),4:('this',['w4']),
   5:('to',['w1']),
   7:('you,',[]),
   8:('for',['w6']),
   21:('together',['w15']),
   24:('together.',['w17'])
 },
 ('2corinthians',8,15): {
   4:('“The',['w3']),5:('one',['w3']),6:('who',['w3']),7:('gathered',['w7']),
   10:('not',['w6']),11:('have',['w7']),12:('too',['w7']),
   15:('the',['w9']),16:('one',['w9']),17:('who',['w9']),18:('gathered',['w13']),
   20:('did',['w13']),21:('not',['w12']),22:('have',['w13']),23:('too',['w13'])
 },
 ('2corinthians',8,23): {
   0:('As',['w2']),1:('for',['w2']),
   5:('my',['w5']),
   12:('as',['w10']),13:('for',['w10'])
 },
}

LEGITIMATE=[
 'precise-fanout|2corinthians|12|17|w9',
 'precise-scattered|2corinthians|3|8|w5',
 'precise-scattered|2corinthians|5|3|w7',
 'precise-scattered|2corinthians|5|9|w3',
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 22'
for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=DATA/'master-review-allowlist.json'
obj=json.loads(allow_path.read_text(encoding='utf8')) if allow_path.exists() else {'interactions':[]}
items=set(obj.get('interactions',[])); items.update(LEGITIMATE)
obj['interactions']=sorted(items)
allow_path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {sum(len(x) for x in FIXES.values())} reviewed token corrections across {len(FIXES)} verses')
print(f'Recorded {len(LEGITIMATE)} reviewed legitimate master interactions')
