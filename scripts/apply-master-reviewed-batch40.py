#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data'/'acts'/'23.json'
d=json.loads(path.read_text(encoding='utf8'))

EDITS=[
 (5,2,'said,',['w1'],False,"Renders ἔφη without unrelated phrase span"),
 (5,5,'not',['w5'],False,"Renders οὐκ without unrelated phrase span"),
 (5,8,'that',['w8'],False,"Renders ὅτι without unrelated phrase span"),
 (5,10,'was',['w9'],False,"Copular rendering of ἐστὶν, not earlier ἔφη"),
 (5,15,'is',['w11'],False,"Passive auxiliary in 'it is written' belongs with γέγραπται, not earlier ἐστὶν"),
 (5,17,'‘You',['w19'],False,"Subject carried by future verb ἐρεῖς, not possessive σου"),
 (5,18,'shall',['w19'],False,"Future/modal force of ἐρεῖς"),
 (5,22,'of',['w14','w15','w16'],False,"Genitival relation in 'ruler of the people' belongs to Ἄρχοντα τοῦ λαοῦ"),
 (5,25,'of',['w15'],False,"Genitive article τοῦ in 'of your people', not σου"),
 (5,26,'your',['w17'],False,"Renders σου without unrelated phrase span"),
 (12,2,'came,',['w1'],False,"Renders γενομένης in 'when day came'"),
 (12,5,'formed',['w4'],False,"Renders ποιήσαντες"),
 (12,9,'bound',['w8'],False,"Renders ἀνεθεμάτισαν"),
 (12,12,'a',['w8'],False,"English support within 'bound themselves with a curse'"),
 (12,13,'curse,',['w8'],False,"Contextual rendering of ἀνεθεμάτισαν ('put under a curse/oath')"),
 (12,14,'saying',['w10'],False,"Renders λέγοντες"),
 (12,17,'would',['w12','w14'],False,"English modal support for infinitival oath construction, not a separate Greek lexical item"),
 (16,2,'the',['w3'],False,"Article with son, not genitive article τῆς"),
 (16,4,'of',['w5'],False,"Genitive article linking sister"),
 (16,5,'Paul’s',['w7'],False,"Renders Παύλου without unrelated phrase span"),
 (16,9,'the',['w8'],False,"Article with ambush without unrelated phrase span"),
 (16,11,'he',['w10'],False,"Subject of 'he came' is carried by participle παραγενόμενος, not later ἀπήγγειλεν"),
 (16,15,'the',['w14'],False,"Article with barracks without unrelated phrase span"),
 (16,17,'and',['w11'],False,"Renders καί coordinating entered/reported"),
 (16,20,'to',['w17'],False,"Dative/article before Paul, not Παύλῳ itself"),
 (16,21,'Paul.',['w18'],False,"Renders Παύλῳ without unrelated phrase span"),
 (21,6,'them,',['w5'],False,"Renders αὐτοῖς without unrelated phrase span"),
 (21,12,'from',['w9'],False,"Renders ἐξ, not later ἀπό"),
 (21,13,'among',['w9'],False,"Part of 'from among' rendering of ἐξ"),
 (21,14,'them',['w10'],False,"Renders αὐτῶν without unrelated phrase span"),
 (21,15,'are',['w6'],False,"Finite verb supplied by ἐνεδρεύουσιν"),
 (21,16,'lying',['w6'],False,"Renders ἐνεδρεύουσιν ('lying in wait')"),
 (21,17,'in',['w6'],False,"Part of idiom 'lying in ambush' for ἐνεδρεύουσιν"),
 (21,18,'ambush',['w6'],False,"Part of idiom 'lying in ambush' for ἐνεδρεύουσιν"),
 (21,22,'have',['w15'],False,"Perfect auxiliary in 'have bound themselves' belongs with ἀνεθεμάτισαν"),
 (21,23,'bound',['w15'],False,"Renders ἀνεθεμάτισαν"),
 (21,27,'curse',['w15'],False,"Contextual rendering of ἀνεθεμάτισαν"),
 (21,29,'to',['w18'],False,"Infinitival marker with φαγεῖν, not πιεῖν"),
 (21,37,'him,',['w24'],False,"Renders second αὐτόν, not earlier αὐτὸν w8"),
 (21,43,'waiting',['w29'],False,"Renders προσδεχόμενοι, not ἐνεδρεύουσιν"),
 (21,45,'your',['w32'],False,"Renders σοῦ without unrelated phrase span"),
 (23,0,'And',['w1'],False,"Renders Καί without unrelated phrase span"),
 (23,2,'two',['w3'],False,"Renders δύο without unrelated phrase span"),
 (23,3,'of',['w5'],False,"Genitive article with centurions without unrelated phrase span"),
 (23,4,'the',['w5'],False,"Article with centurions without unrelated phrase span"),
 (23,9,'two',['w10'],False,"Part of διακοσίους without unrelated phrase span"),
 (23,10,'hundred',['w10'],False,"Part of διακοσίους without unrelated phrase span"),
 (23,12,'to',['w12'],False,"Infinitival marker with πορευθῶσιν, not προσκαλεσάμενος"),
 (23,18,'and',['w15'],False,"Renders first καί without unrelated phrase span"),
 (23,21,'and',['w18'],False,"Renders second καί without unrelated phrase span"),
 (23,22,'two',['w20'],False,"Part of second διακοσίους without unrelated phrase span"),
 (23,23,'hundred',['w20'],False,"Part of second διακοσίους without unrelated phrase span"),
 (23,26,'the',['w22'],False,"Article-like support with third hour without unrelated phrase span"),
 (23,29,'of',['w24'],False,"Genitive article with night without unrelated phrase span"),
 (23,30,'the',['w24'],False,"Article with night without unrelated phrase span"),
 (32,1,'the',['w1'],False,"Article in 'on the next day' without unrelated phrase span"),
 (32,4,'they',['w4'],False,"Subject of 'they allowed' carried by participle ἐάσαντες, not later ὑπέστρεψαν"),
 (32,6,'the',['w5'],False,"Article with horsemen without unrelated phrase span"),
 (32,8,'to',['w7'],False,"Infinitival marker with ἀπέρχεσθαι without unrelated phrase span"),
 (32,10,'on',[],True,"English aspectual particle in 'go on' is supplied"),
 (32,15,'to',['w11'],False,"Renders εἰς without unrelated phrase span"),
 (32,16,'the',['w12'],False,"Article with barracks without unrelated phrase span"),
 (35,5,'you',['w2'],False,"Renders σου ('you')"),
 (35,8,'your',['w8'],False,"Renders σου without unrelated phrase span"),
 (35,13,'he',['w10'],False,"Subject of 'he commanded' carried by participle κελεύσας, not earlier ἔφη"),
]

count=0
for vn,idx,expected,ids,supplied,reason in EDITS:
    verse=next(v for v in d['verses'] if v['v']==vn)
    x=verse['alignment']['dgt'][idx]
    if x.get('text') != expected:
        raise SystemExit(f"Acts 23:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids)
    if supplied:
        x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 40: '+reason
    count+=1

path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-40 corrections in Acts 23')
