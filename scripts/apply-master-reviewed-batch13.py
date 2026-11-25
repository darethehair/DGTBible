#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('luke',4,41): {
   30:('he',['w29']),31:('was',['w30'])
 },
 ('luke',8,13): {
   17:('they',['w15']),21:('They',['w19']),28:('a',['w25'])
 },
 ('luke',6,44): {
   17:('do',['w19']),18:('they',['w19']),19:('pick',['w19'])
 },
 ('romans',7,1): {
   4:('know,',['w2'])
 },
 ('acts',28,23): {
   0:('And',['w2']),7:('even',['w11']),12:('him',['w7']),
   19:('explained,',['w13']),27:('and',['w20']),29:('to',['w19'])
 },
 ('2corinthians',11,2): {
   7:('a',['w5']),20:('to',['w13']),22:('you',['w8']),23:('as',[])
 },
 ('luke',8,2): {
   5:('had',['w5']),6:('been',['w5']),7:('healed',['w6'])
 },
 ('luke',12,48): {
   31:('the',['w21']),32:('one',['w21']),41:('be',['w25']),42:('demanded.',['w25'])
 },
}

LEGITIMATE=[
 'precise-fanout|galatians|4|15|w16',
 'precise-scattered|1peter|3|8|w7',
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 13'
for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=DATA/'master-review-allowlist.json'
obj=json.loads(allow_path.read_text(encoding='utf8')) if allow_path.exists() else {'interactions':[]}
items=set(obj.get('interactions',[])); items.update(LEGITIMATE)
obj['interactions']=sorted(items)
allow_path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {sum(len(x) for x in FIXES.values())} reviewed token corrections across {len(FIXES)} verses')
print(f'Recorded {len(LEGITIMATE)} reviewed legitimate master interactions')
