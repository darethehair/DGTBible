#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data'/'acts'/'21.json'
d=json.loads(path.read_text(encoding='utf8'))

EDITS=[
 (2,6,'to',['w5'],False,"Renders εἰς, not supplied glue"),
 (2,8,'we',['w7'],False,"Subject of 'we went aboard' carried by participle ἐπιβάντες, not later ἀνήχθημεν"),
 (2,9,'went',['w7'],False,"Renders ἐπιβάντες without unrelated phrase span"),
 (5,8,'the',['w6'],False,"Article with days without unrelated phrase span"),
 (5,10,'we',['w8'],False,"Subject of 'we departed' carried by ἐξελθόντες"),
 (5,11,'departed',['w8'],False,"Renders ἐξελθόντες"),
 (5,12,'and',[],True,"English coordination between departed and continued is supplied"),
 (5,13,'continued',['w9'],False,"Renders ἐπορευόμεθα"),
 (5,14,'on',[],True,"English aspectual particle in 'continued on' is supplied"),
 (5,15,'our',['w9'],False,"English possessive support in 'our way' tied to first-person verb"),
 (5,16,'way,',['w9'],False,"Contextual rendering of ἐπορευόμεθα"),
 (5,20,'them,',['w12'],False,"Renders πάντων/everyone context as 'all of them'"),
 (5,22,'women',['w14'],False,"Renders γυναιξὶ"),
 (5,25,'escorted',['w10'],False,"Renders προπεμπόντων"),
 (5,27,'until',['w17'],False,"Renders ἕως"),
 (5,31,'the',['w19'],False,"Article with city, not later τὰ w23"),
 (5,34,'kneeling',['w22','w24'],False,"Contextual rendering of θέντες τὰ γόνατα ('kneeling')"),
 (5,36,'the',['w26'],False,"Article with shore without unrelated phrase span"),
 (5,37,'beach,',['w27'],False,"Renders αἰγιαλὸν"),
 (6,7,'we',['w4'],False,"Subject of 'we went aboard' without unrelated phrase span"),
 (6,10,'the',['w6'],False,"Article with ship without unrelated phrase span"),
 (7,1,'we',['w1'],False,"Opening subject Ἡμεῖς without unrelated phrase span"),
 (7,4,'the',['w3'],False,"Article with voyage without unrelated phrase span"),
 (7,8,'we',['w8'],False,"Subject of 'we arrived' carried by κατηντήσαμεν, not later ἐμείναμεν"),
 (7,10,'at',['w9'],False,"Destination preposition εἰς rendered idiomatically as 'at'"),
 (7,13,'the',['w13'],False,"Article with brothers without unrelated phrase span"),
 (14,11,'“Let',['w11'],False,"Imperatival rendering of γινέσθω"),
 (14,12,'the',['w9'],False,"Article with will, not genitive Τοῦ"),
 (14,14,'of',['w7'],False,"Genitive article in 'of the Lord'"),
 (14,15,'the',['w7'],False,"Article in 'of the Lord', not τὸ w9"),
 (15,3,'we',['w6'],False,"Subject of 'we prepared' carried by participle ἐπισκευασάμενοι, not later ἀνεβαίνομεν"),
 (16,9,'with',['w8'],False,"Renders σύν without unrelated phrase span"),
 (16,15,'of',['w16'],False,"English genitive rendering of Κυπρίῳ ('of Cyprus'), not earlier τῶν"),
 (16,16,'Cyprus,',['w16'],False,"Renders Κυπρίῳ"),
 (16,23,'were',['w13'],False,"Modal/passive support for ξενισθῶμεν"),
 (16,24,'to',['w13'],False,"Infinitival rendering support for ξενισθῶμεν"),
 (16,25,'stay.',['w13'],False,"Contextual rendering of ξενισθῶμεν"),
 (24,4,'yourself',['w3'],False,"Reflexive English rendering of middle/passive imperative ἁγνίσθητι, not αὐτὸς w27"),
 (24,6,'them,',['w5'],False,"Renders αὐτοῖς without unrelated phrase span"),
 (24,7,'and',['w6'],False,"Renders καί without unrelated phrase span"),
 (24,8,'pay',['w7'],False,"Renders δαπάνησον"),
 (24,9,'their',['w9'],False,"Renders αὐτοῖς without unrelated phrase span"),
 (24,12,'that',['w10'],False,"Renders ἵνα without unrelated phrase span"),
 (24,13,'they',['w11'],False,"Subject of ξυρήσονται without unrelated phrase span"),
 (24,16,'their',['w12'],False,"Article with κεφαλήν rendered possessively, not ξυρήσονται"),
 (24,18,'and',['w14'],False,"Renders καί without unrelated phrase span"),
 (24,20,'will',['w15'],False,"Future auxiliary carried by γνώσονται without unrelated phrase span"),
 (24,22,'that',['w17'],False,"Renders ὅτι without unrelated phrase span"),
 (24,23,'there',['w23'],False,"English existential support for ἐστιν"),
 (24,25,'nothing',['w22'],False,"Renders οὐδέν"),
 (24,27,'the',[],True,"English article supplied in 'the things'"),
 (24,28,'things',['w18'],False,"Renders relative ὧν as substantival 'things'"),
 (24,29,'they',['w19'],False,"Subject of passive κατήχηνται"),
 (24,32,'told',['w19'],False,"Renders κατήχηνται"),
 (24,34,'you,',['w21'],False,"Renders σοῦ without unrelated phrase span"),
 (24,36,'that',[],True,"English complementizer after but is supplied"),
 (24,37,'you',['w25'],False,"Subject of στοιχεῖς without unrelated phrase span"),
 (24,43,'the',['w29'],False,"Article with law without unrelated phrase span"),
 (32,0,'He',['w1'],False,"Relative ὃς carried as English subject 'He'"),
 (32,1,'immediately',['w2'],False,"Renders ἐξαυτῆς"),
 (32,3,'soldiers',['w4'],False,"Renders στρατιώτας without unrelated phrase span"),
 (32,6,'and',['w5'],False,"First-clause coordination belongs to καὶ w5, not δὲ w11"),
 (32,12,'they',['w12'],False,"Subject of 'they saw' carried by participle ἰδόντες, not later ἐπαύσαντο"),
 (32,14,'the',['w13'],False,"Article with commander without unrelated phrase span"),
 (32,17,'the',['w16'],False,"Article with soldiers without unrelated phrase span"),
 (32,18,'soldiers,',['w17'],False,"Renders στρατιώτας without unrelated phrase span"),
]

count=0
for vn,idx,expected,ids,supplied,reason in EDITS:
    verse=next(v for v in d['verses'] if v['v']==vn)
    x=verse['alignment']['dgt'][idx]
    if x.get('text') != expected:
        raise SystemExit(f"Acts 21:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids)
    if supplied:
        x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 42: '+reason
    count+=1

path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-42 corrections in Acts 21')
