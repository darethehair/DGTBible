#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('luke',10,15): {
   9:('You',['s11']), 10:('will',['s11']), 11:('be',['s11']), 13:('down',['s11'])
 },
 ('luke',10,31): {
   11:('he',['w12'])
 },
 ('luke',11,19): {
   17:('they',['w17'])
 },
 ('luke',12,46): {
   19:('does',['w17']),
   30:('assign',['w28']),
   32:('a',['w23']),
   36:('unfaithful.',['w27'])
 },
 ('luke',15,6): {
   1:('he',['w2']),
   3:('home,',['w5']),
   7:('his',[]),
   10:('neighbors,',['w11']),
   17:('because',['w16']),
   20:('my',['w20'])
 },
 ('luke',17,2): {
   22:('for',['w17'])
 },
 ('luke',17,10): {
   11:('‘We',['w14']),
   15:('we',['w19']),
   22:('have',['w17']),
   23:('done.’”',['w18'])
 },
 ('luke',19,30): {
   6:('you.',[]),
   8:('you',['w9'])
 },
 ('luke',22,54): {
   3:('him,',['w3']),
   5:('him',['w3']),
   12:('house',['w10']),
   22:('distance.',['w17'])
 },
 ('luke',23,25): {
   10:('for',['w5']),
   11:('uprising',['w6']),
   12:('and',['w7']),
   23:('over',['w18'])
 },
 ('luke',6,4): {
   4:('of',['w6']),
   6:('took',['w13']),
   7:('the',['w9']),
   8:('bread',['w10']),
   9:('of',['w11']),
   10:('the',['w11']),
   11:('Presence,',['w12']),
   13:('it,',['w10']),
   14:('and',['w16']),
   31:('to',['w25']),
   33:('it.”',['w22'])
 },
 ('luke',6,21): {
   2:('you',['w2']),
   10:('satisfied.',['w6']),
   13:('you',['w8'])
 },
 ('luke',6,38): {
   16:('be',['w12']),
   17:('poured',['w12']),
   19:('your',['w16']),
   25:('you',['w22']),
   26:('use,',['w22'])
 },
 ('luke',6,39): {
   7:('a',['w8']),
   10:('guide',['w10']),
   11:('a',['w9']),
   12:('blind',['w9']),
   13:('person?',['w9'])
 },
 ('luke',6,42): {
   4:('to',['w5']),
   7:('‘Brother,',['w8']),
   10:('take',['w10']),
   15:('your',['w17']),
   18:('you',['w18']),
   22:('see',['w26']),
   31:('take',['w28']),
   46:('remove',['w48']),
   47:('the',['w39']),
   48:('speck',['w40'])
 },
 ('luke',8,10): {
   10:('the',['w7']),
   21:('they',['w8']),
   22:('are',['w5'])
 },
 ('luke',8,50): {
   8:('be',['w9'])
 },
}

LEGITIMATE=[
 'precise-fanout|luke|10|42|w15',
 'precise-fanout|luke|12|46|w19',
 'precise-fanout|luke|17|2|w18',
 'precise-fanout|luke|21|16|w13',
 'precise-scattered|luke|21|16|w13',
 'precise-fanout|luke|8|10|w5',
 'precise-scattered|luke|8|10|w5',
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 7'

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
