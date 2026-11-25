#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('luke',1,35): {
   4:('“The',['w7']),
   12:('the',[]),
   22:('the',['w19'])
 },
 ('acts',2,39): {
   5:('you',['w1']),
   13:('who',['w12']),
   15:('far',['w14']),
   16:('away,',['w14']),
   22:('our',['w21'])
 },
 ('acts',4,9): {
   12:('a',[]),
   18:('this',['w11'])
 },
 ('2corinthians',2,5): {
   0:('But',['w2']),
   7:('has',['w7']),
   8:('not',['w5'])
 },
 ('philippians',1,10): {
   0:('so',['w1']),
   1:('that',['w2']),
   7:('that',['w6']),
   8:('matter,',['w6']),
   14:('sincere',['w9']),
   17:('for',['w12'])
 },
 ('philippians',2,17): {
   8:('upon',['w5']),
   9:('the',['w6']),
   14:('your',['w12']),
   16:('I',['w13']),
   17:('rejoice',['w13']),
   20:('together',['w15'])
 },
 ('philippians',3,5): {
   0:('circumcised',['w1']),
   5:('from',['w3']),
   6:('the',['w4']),
   7:('people',['w4']),
   10:('of',['w6']),
   13:('of',['w7'])
 },
 ('titus',3,12): {
   14:('at',['w12']),
   24:('there.',['w14'])
 },
 ('revelation',11,3): {
   6:('my',['w6'])
 },
 ('revelation',14,18): {
   8:('the',['w8']),
   26:('the',['w20']),
   36:('the',['w33']),
   38:('of',['w35']),
   39:('the',['w35'])
 },
}

LEGITIMATE=[
 'precise-fanout|acts|5|41|w11',
 'precise-fanout|luke|10|15|s11',
 'precise-fanout|romans|9|33|w19',
 'precise-fanout|romans|10|18|w5',
 'precise-scattered|romans|10|18|w5',
 'precise-fanout|romans|11|32|w12',
 'precise-fanout|2corinthians|2|5|w7',
 'precise-scattered|2corinthians|2|5|w7',
 'precise-fanout|philippians|2|17|w4',
 'precise-fanout|philippians|4|12|w12',
 'precise-fanout|titus|2|3|w12',
 'precise-fanout|philemon|1|15|w5',
 'precise-fanout|philemon|1|22|w14',
 'precise-fanout|revelation|12|15|w17',
 'precise-fanout|revelation|18|8|w18',
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 9'

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
