#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('2corinthians',10,4): {
   1:('the',['w1']),
   11:('through',['w12']),
   13:('for',['w13']),
   15:('tearing',['w14']),
   19:('tearing',['w17']),
   20:('down',['w17'])
 },
 ('2corinthians',10,13): {
   6:('measure,',['w6']),
   10:('the',['w10']),
   11:('measure',['w11'])
 },
 ('2corinthians',11,21): {
   3:('I',['w3']),
   4:('say',['w3']),
   7:('were',['w7']),
   8:('too',['w7']),
   17:('to',['w13']),
   18:('boast',['w13']),
   21:('I',['w16'])
 },
 ('2corinthians',11,29): {
   0:('Who',['w1']),
   8:('Who',['w6']),
   9:('is',['w7']),
   10:('made',['w7']),
   11:('to',['w7']),
   14:('I',['w10']),
   16:('not',['w9'])
 },
 ('2corinthians',11,30): {
   1:('I',['w3']),
   12:('my',['w7'])
 },
 ('2corinthians',11,32): {
   2:('the',['w3']),
   9:('the',['w9']),
   14:('in',['w12']),
   15:('order',['w12'])
 },
 ('2corinthians',12,4): {
   11:('that',['w10']),
   12:('a',['w13']),
   14:('is',['w12'])
 },
 ('2corinthians',12,13): {
   4:('you',['w5']),
   9:('the',['w7']),
   17:('myself',['w13'])
 },
 ('2corinthians',12,17): {
   2:('take',['w9']),
   4:('of',['w9']),
   7:('anyone',['w2'])
 },
 ('2corinthians',12,18): {
   5:('the',['w5']),
   10:('did',['w8']),
   11:('not',['w7']),
   12:('take',['w8']),
   14:('of',['w8']),
   16:('did',['w7']),
   17:('he?',['w7']),
   20:('not',['w11']),
   22:('in',['w12']),
   23:('the',['w12']),
   24:('same',['w13']),
   26:('and',[]),
   27:('in',['w17']),
   28:('the',['w17'])
 },
 ('2corinthians',12,19): {
   3:('you',['w2']),
   11:('ourselves',['w5']),
   21:('And',['w13']),
   25:('are',['w19']),
   29:('up.',['w19'])
 },
}

LEGITIMATE=[
 'precise-scattered|1thessalonians|3|1|w3',
 'precise-scattered|1timothy|2|11|w4',
 'precise-scattered|1timothy|5|15|w4',
 'precise-scattered|1timothy|5|17|w7',
 'precise-scattered|2corinthians|10|18|w7',
 'precise-scattered|2corinthians|11|19|w3',
 'precise-scattered|2corinthians|11|28|w11',
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 21'
for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=DATA/'master-review-allowlist.json'
obj=json.loads(allow_path.read_text(encoding='utf8')) if allow_path.exists() else {'interactions':[]}
items=set(obj.get('interactions',[])); items.update(LEGITIMATE)
obj['interactions']=sorted(items)
allow_path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {sum(len(x) for x in FIXES.values())} reviewed token corrections across {len(FIXES)} verses')
print(f'Recorded {len(LEGITIMATE)} reviewed legitimate master interactions')
