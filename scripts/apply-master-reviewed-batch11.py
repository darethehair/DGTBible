#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

FIXES={
 ('mark',6,46): {
   1:('after',['w2']),2:('saying',['w2']),3:('farewell',['w2']),
   4:('to',['w3']),9:('to',['w5'])
 },
 ('luke',24,30): {
   2:('he',['w6']),10:('took',['w9']),15:('broke',['w14']),16:('it,',['w14']),
   18:('began',['w15']),20:('it',['w15'])
 },
 ('galatians',6,3): {
   4:('he',['w5']),5:('is',['w5']),8:('he',['w8']),9:('is',['w8'])
 },
 ('mark',15,44): {
   2:('was',['w4']),3:('surprised',['w4']),6:('had',['w7']),14:('asked',['w12']),
   19:('been',['w16']),21:('for',['w15']),22:('some',['w15']),23:('time.',['w15'])
 },
 ('acts',25,10): {
   3:('“I',['w10']),16:('I',['w17'])
 },
 ('mark',7,33): {
   1:('taking',['w2']),8:('he',['w9']),10:('his',['w12']),12:('into',['w13']),
   14:('man’s',['w16']),20:('his',['w22'])
 },
 ('luke',11,2): {
   9:('may',['w13']),13:('made',['w13']),14:('holy.',['w13']),15:('May',['w17'])
 },
 ('mark',15,42): {
   10:('Day,',['w7']),13:('the',['w10']),14:('day',['w10']),16:('the',['w10'])
 },
 ('luke',23,22): {
   14:('I',['w15']),15:('have',['w15']),24:('I',['w21']),26:('punish',['w18']),
   30:('him.”',['w20'])
 },
 ('luke',16,31): {
   6:('they',['w10']),17:('they',['w17'])
 },
 ('john',3,29): {
   3:('has',['w2'])
 },
 ('philippians',4,6): {
   0:('Be',['w2'])
 },
 ('luke',5,9): {
   2:('had',['w3']),3:('seized',['w3'])
 },
 ('luke',19,1): {
   1:('he',['w2'])
 },
 ('luke',23,16): {
   7:('him.”',['w3'])
 },
 ('luke',11,8): {
   15:('he',['w11']),16:('is',['w11']),17:('his',['w13']),
   22:('his',['w18']),25:('he',['w20']),28:('up',['w19']),31:('him',['w21'])
 },
 ('mark',9,41): {
   11:('you',['w14']),12:('belong',['w14']),13:('to',['w13']),25:('his',['w24'])
 },
 ('galatians',4,13): {
   4:('because',['w4']),5:('of',['w4']),13:('the',['w8'])
 },
 ('mark',6,37): {
   10:('to',['w9']),13:('they',['w11']),14:('say',['w11']),15:('to',['w12']),
   16:('him,',['w12']),31:('to',['w20'])
 },
 ('luke',24,23): {
   2:('they',['w3']),10:('saying',['w8']),12:('they',['w12'])
 },
 ('mark',11,33): {
   11:('says',['w12']),12:('to',['w13']),13:('them,',['w13'])
 },
 ('matthew',13,58): {
   7:('works',['w5'])
 },
 ('2timothy',2,6): {
   4:('to',['w4'])
 },
 ('acts',23,34): {
   3:('he',['w6']),12:('he',['w12']),16:('was',['w15'])
 },
 ('luke',3,21): {
   9:('was',['w11']),14:('was',['w13'])
 },
 ('luke',15,5): {
   2:('he',['w2']),4:('it,',['w2']),5:('he',['w3']),6:('places',['w3'])
 },
 ('luke',7,9): {
   5:('he',['w6']),18:('tell',['w15'])
 },
 ('2corinthians',10,9): {
   8:('I',['w6']),9:('were',['w6'])
 },
 ('luke',18,4): {
   5:('unwilling,',['w3']),10:('to',['w10']),15:('do',['w17'])
 },
}

LEGITIMATE=[
 'precise-scattered|acts|25|10|w17',
 'precise-scattered|luke|23|22|w21',
 'precise-scattered|luke|23|16|w4',
 'precise-scattered|mark|9|41|w4',
 'precise-scattered|matthew|13|58|w3',
 'precise-scattered|2timothy|2|6|w8',
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
        D[idx]['reason']='Human-reviewed full-NT master pass batch 11'
for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=DATA/'master-review-allowlist.json'
obj=json.loads(allow_path.read_text(encoding='utf8')) if allow_path.exists() else {'interactions':[]}
items=set(obj.get('interactions',[])); items.update(LEGITIMATE)
obj['interactions']=sorted(items)
allow_path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {sum(len(x) for x in FIXES.values())} reviewed token corrections across {len(FIXES)} verses')
print(f'Recorded {len(LEGITIMATE)} reviewed legitimate master interactions')
