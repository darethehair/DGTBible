#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
files={}

def get(ch):
    if ch not in files:
        p=ROOT/'data'/'james'/f'{ch:02}.json'
        files[ch]=(p,json.loads(p.read_text(encoding='utf8')))
    return files[ch][1]

def edit(ch,vn,idx,expected,ids,supplied,reason):
    d=get(ch)
    verse=next(v for v in d['verses'] if v['v']==vn)
    x=verse['alignment']['dgt'][idx]
    if x.get('text') != expected:
        raise SystemExit(f"James {ch}:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids)
    if supplied:
        x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 61: '+reason

# James 1:8
edit(1,8,0,'a',[],True,"English article before 'double-minded person' is supplied; ἀνήρ supplies 'person'")
edit(1,8,2,'person,',['w1'],False,"Renders ἀνήρ")

# James 2:6
edit(2,6,5,'person.',['w5'],False,"Substantival πτωχόν supplies 'poor person'; do not borrow interrogative οὐχ")
edit(2,6,6,'Is',[],True,"English interrogative auxiliary in 'Is it not...' is supplied")
edit(2,6,7,'it',[],True,"English expletive subject in the interrogative is supplied")
edit(2,6,8,'not',['w6'],False,"Renders οὐχ")
edit(2,6,11,'who',['w7'],False,"Substantival article οἱ introduces 'the rich who...'")

# James 3:3
edit(3,3,2,'we',['w10'],False,"Subject of βάλλομεν ('we put')")
edit(3,3,8,'so',['w11'],False,"Purpose/result εἰς rendered idiomatically as 'so that'")
edit(3,3,9,'that',['w12','w13'],False,"Article + infinitive construction supplies 'that they obey'")
edit(3,3,13,'we',['w21'],False,"Second 'we' belongs to μετάγομεν ('we guide/turn'), not βάλλομεν")
edit(3,3,14,'also',['w16'],False,"Renders καί adverbially as 'also'")
edit(3,3,15,'guide',['w21'],False,"Contextual rendering of μετάγομεν")

# James 3:5
edit(3,5,10,'great',['w9'],False,"First 'great' belongs to μεγάλα ('great things'), not ἡλίκον")
edit(3,5,14,'small',['w12'],False,"Second 'small' belongs to comparative/exclamatory ἡλίκον describing the fire")
edit(3,5,17,'sets',['w16'],False,"Renders ἀνάπτει")
edit(3,5,18,'ablaze',['w16'],False,"Completes contextual rendering of ἀνάπτει")

# James 3:8
edit(3,8,2,'human',['w7'],False,"Genitive ἀνθρώπων supplies 'human'")
edit(3,8,3,'being',[],True,"English noun completion 'human being' is supplied")
edit(3,8,4,'is',['w6'],False,"Copular/modal support with δύναται ('is able')")
edit(3,8,7,'tame',['w5'],False,"Renders δαμάσαι")
edit(3,8,11,'is',[],True,"Second-clause copula in 'It is a restless evil' is supplied")
edit(3,8,12,'a',[],True,"English article before 'restless evil' is supplied")
edit(3,8,13,'restless',['w8'],False,"Renders ἀκατάστατον, not ἀνθρώπων")

# James 5:20
edit(5,20,0,'let',['w1'],False,"Imperatival force of γινωσκέτω")
edit(5,20,2,'person',[],True,"English explicit subject 'that person' is supplied from the imperative context")
edit(5,20,4,'that',[],True,"Second English complementizer introducing the one-who-turns clause is supplied")
edit(5,20,5,'whoever',['w3'],False,"Substantival article ὁ before ἐπιστρέψας supplies 'whoever/the one who'")
edit(5,20,6,'turns',['w4'],False,"Renders ἐπιστρέψας")
edit(5,20,11,'the',[],True,"Greek πλάνης lacks an article; English 'the error' article is supplied")
edit(5,20,13,'of',['w8'],False,"Genitive ὁδοῦ supplies relation in 'error of their way'")
edit(5,20,18,'a',[],True,"English article before 'soul' is supplied")
edit(5,20,26,'of',[],True,"English genitive glue in 'multitude of sins' is supplied")

for p,d in files.values():
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

print('Applied reviewed James master-alignment corrections')
