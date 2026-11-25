#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data'/'acts'/'27.json'
allow_path=ROOT/'data'/'master-review-allowlist.json'
d=json.loads(path.read_text(encoding='utf8'))

EDITS=[
 (2,3,'Adramyttian',['w4'],False,"Renders Ἀδραμυττηνῷ directly"),
 (2,5,'that',[],True,"Relative connector supplied in English"),
 (2,6,'was',['w5'],False,"Auxiliary in 'was about to sail' belongs to μέλλοντι, not later ὄντος"),
 (2,8,'to',['w6'],False,"Infinitival marker with πλεῖν"),
 (2,9,'sail',['w6'],False,"Renders πλεῖν"),
 (2,10,'to',['w7'],False,"Destination preposition before places renders εἰς"),
 (2,14,'coast',[],True,"English expansion of 'places along Asia'; no separate Greek lexical item"),
 (2,15,'of',[],True,"English glue in 'coast of Asia'"),
 (2,18,'put',['w13'],False,"Part of 'put to sea' rendering of ἀνήχθημεν"),
 (2,19,'to',['w13'],False,"Part of idiomatic 'put to sea' rendering of ἀνήχθημεν"),
 (2,20,'sea,',['w13'],False,"Part of idiomatic 'put to sea' rendering of ἀνήχθημεν"),
 (15,2,'the',['w3'],False,"Article with ship without unrelated phrase span"),
 (15,8,'to',['w8'],False,"Infinitival marker with ἀντοφθαλμεῖν"),
 (15,11,'the',['w9'],False,"Article/preposition element with wind without unrelated phrase span"),
 (15,13,'we',['w11'],False,"Subject of 'we gave way' is carried by participle ἐπιδόντες, leaving ἐφερόμεθα for 'were driven along'"),
 (29,2,'that',[],True,"English complementizer supplied for μή-clause"),
 (29,3,'we',['w8'],False,"Subject carried by ἐκπέσωμεν"),
 (29,4,'might',['w8'],False,"Modal force of subjunctive ἐκπέσωμεν"),
 (29,5,'run',['w8'],False,"Part of contextual rendering of ἐκπέσωμεν"),
 (29,6,'aground',['w8'],False,"Part of contextual rendering of ἐκπέσωμεν"),
 (29,7,'somewhere',['w4'],False,"Renders που"),
 (29,11,'they',['w11'],False,"Subject of 'they threw' is carried by participle ῥίψαντες, not later ηὔχοντο"),
 (29,12,'threw',['w11'],False,"Renders ῥίψαντες without unrelated phrase span"),
 (36,1,'they',['w3'],False,"Subject of 'they became encouraged' is carried by γενόμενοι"),
 (36,3,'became',['w3'],False,"Renders γενόμενοι, while εὔθυμοι supplies 'encouraged'"),
]

count=0
for vn,idx,expected,ids,supplied,reason in EDITS:
    verse=next(v for v in d['verses'] if v['v']==vn)
    x=verse['alignment']['dgt'][idx]
    if x.get('text') != expected:
        raise SystemExit(f"Acts 27:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids)
    if supplied:
        x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 36: '+reason
    count+=1

path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

a=json.loads(allow_path.read_text(encoding='utf8'))
items=set(a.get('interactions',[]))
for key in [
    'precise-scattered|acts|27|4|w1',
    'precise-scattered|acts|27|19|w9',
]:
    items.add(key)
a['interactions']=sorted(items)
allow_path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-36 corrections and reviewed 2 legitimate scattered renderings')
