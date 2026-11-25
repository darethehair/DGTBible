#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

# Exact, human-reviewed master-pass corrections.
# Each edit verifies the expected displayed token before changing ids.
FIXES={
 ('1corinthians',11,32): {
   2:('we',['w1']), 3:('are',['w1'])
 },
 ('1corinthians',12,2): {
   6:('Gentiles,',['w4']),
   7:('you',[]), 8:('were',[]), 9:('being',['w14']), 10:('led',['w14']), 11:('away',['w14'])
 },
 ('1corinthians',14,27): {
   3:('in',['w2']), 20:('let',['w16'])
 },
 ('1corinthians',15,48): {
   0:('As',['w1']), 1:('the',['w2']), 2:('one',['w2']),
   7:('so',['w4']), 8:('also',['w5']), 10:('those',['w6']),
   11:('made',['w7']), 12:('of',['w7']), 13:('dust;',['w7']),
   15:('as',['w9']),16:('the',['w10']),
   20:('so',['w12']), 22:('are',[]), 23:('those',['w14']),24:('who',[]),25:('are',[]),
   26:('heavenly.',['w15'])
 },
 ('1corinthians',15,56): {
   0:('Now',['w2']), 5:('is',[]), 7:('and',['w9']),
   10:('of',['w12']), 12:('is',[]), 13:('the',['w13'])
 },
 ('1corinthians',16,10): {
   6:('he',['w8']), 7:('is',['w8'])
 },
 ('2corinthians',10,3): {
   2:('we',['w4'])
 },
 ('2corinthians',11,17): {
   4:('I',['w6']), 5:('am',['w6'])
 },
}

changed={}
for (slug,ch,vnum),edits in FIXES.items():
    path=ROOT/'data'/slug/f'{ch:02}.json'
    d=json.loads(path.read_text(encoding='utf8'))
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
        D[idx]['reason']='Human-reviewed full-NT master pass'
    changed[path]=d

for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

print(f'Applied {sum(len(x) for x in FIXES.values())} reviewed token corrections across {len(FIXES)} verses / {len(changed)} chapter files')
for key,edits in FIXES.items():
    print(key, len(edits))
