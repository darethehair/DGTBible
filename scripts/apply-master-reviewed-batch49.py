#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def apply(ch, edits):
    path=ROOT/'data'/'acts'/f'{ch:02}.json'
    d=json.loads(path.read_text(encoding='utf8'))
    count=0
    for vn,idx,expected,ids,supplied,reason in edits:
        verse=next(v for v in d['verses'] if v['v']==vn)
        x=verse['alignment']['dgt'][idx]
        if x.get('text') != expected:
            raise SystemExit(f"Acts {ch}:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
        x['ids']=list(ids); x['phraseIds']=list(ids)
        if supplied:
            x['supplied']=True; x['confidence']='reviewed-master-supplied'
        else:
            x.pop('supplied',None); x['confidence']='reviewed-master-precise'
        x['reason']='Human-reviewed full-NT master pass batch 49: '+reason
        count+=1
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return count

ed6=[
 (7,0,'And',['w1'],False,"Renders opening Καί without unrelated phrase span"),
 (7,1,'the',['w2'],False,"Article with word without unrelated phrase span"),
 (7,3,'of',['w4'],False,"Genitive article relation in 'of God', not θεοῦ itself"),
 (7,5,'kept',['w6'],False,"Aspectual English rendering of ηὔξανεν"),
 (7,6,'growing,',['w6'],False,"Renders ηὔξανεν"),
 (7,7,'and',['w7'],False,"Renders second καί without unrelated phrase span"),
 (7,8,'the',['w9'],False,"Article with number without unrelated phrase span"),
 (7,10,'of',['w11'],False,"Genitive article before disciples without unrelated phrase span"),
 (7,14,'was',['w8'],False,"Passive auxiliary with ἐπληθύνετο"),
 (7,16,'greatly,',['w15'],False,"Renders σφόδρα, not πολύς"),
 (7,17,'and',['w17'],False,"Third-clause connective renders τε, not earlier καί w7"),
 (7,18,'a',['w16'],False,"Article-like English support with πολύς"),
 (7,19,'large',['w16'],False,"Renders πολύς"),
 (7,20,'crowd',['w18'],False,"Renders ὄχλος"),
 (7,21,'of',['w19'],False,"Genitive article before priests without unrelated phrase span"),
 (7,27,'the',['w22'],False,"Article/dative in 'to the faith' without unrelated phrase span"),
 (13,0,'They',['w1'],False,"Subject carried by ἔστησαν"),
 (13,2,'put',['w1'],False,"Part of 'put forward' rendering of ἔστησαν, not τόπου"),
 (13,3,'forward',['w1'],False,"Completes contextual rendering of ἔστησαν"),
 (13,6,'who',['w5'],False,"Relative English support for participle λέγοντας"),
 (13,7,'said,',['w5'],False,"Renders λέγοντας without unrelated phrase span"),
 (13,14,'words',['w12'],False,"Renders ῥήματα"),
 (13,16,'this',['w15','w16'],False,"English demonstrative in 'this holy place' tied to the place phrase, not οὗτος w8"),
 (13,20,'the',['w21'],False,"Article with law without unrelated phrase span"),
]

ed5=[
 (2,0,'and',['w1'],False,"Renders opening καί without unrelated phrase span"),
 (2,4,'knowledge',['w6'],False,"Renders συνειδυίης"),
 (2,5,'he',['w2'],False,"Subject of ἐνοσφίσατο without unrelated phrase span"),
 (2,9,'of',['w4'],False,"Article/genitive relation in 'part of the price', not later τῶν w18"),
 (2,10,'the',['w4'],False,"Article with price, not wife article w8"),
 (2,11,'price',['w5'],False,"Renders τιμῆς"),
 (2,12,'and',['w11'],False,"Renders second καί without unrelated phrase span"),
 (2,17,'and',[],True,"English coordination before 'laid it' is supplied"),
 (2,21,'the',['w16'],False,"Article with feet, not genitive τῶν w18"),
 (6,0,'And',['w2'],False,"Opening connective renders δὲ, leaving καί w7 before carrying out"),
 (6,4,'got',['w1'],False,"Part of ἀναστάντες ('got up') without unrelated phrase span"),
 (6,7,'him',['w6'],False,"Renders αὐτόν without unrelated phrase span"),
 (6,10,'him',['w8'],False,"Object included in contextual rendering of ἐξενέγκαντες"),
 (6,12,'and',['w7'],False,"Renders καί"),
 (6,14,'him.',['w9'],False,"Object included in contextual rendering of ἔθαψαν"),
 (7,3,'of',[],True,"English connective in 'interval of about three hours' is supplied"),
 (7,8,'and',['w7'],False,"Renders καί before wife clause"),
 (7,9,'his',['w10'],False,"Renders αὐτοῦ without unrelated phrase span"),
 (7,17,'happened.',['w14'],False,"Renders γεγονὸς without unrelated phrase span"),
 (15,0,'so',['w1'],False,"Renders ὥστε"),
 (15,1,'that',[],True,"English complementizer completing 'so that' is supplied"),
 (15,2,'they',[],True,"English subject of infinitival construction is supplied by context"),
 (15,5,'the',['w7'],False,"Article with sick, not streets article w4"),
 (15,8,'the',['w4'],False,"Article with streets, not sick article w7"),
 (15,10,'and',['w9'],False,"Renders καί without unrelated phrase span"),
 (15,12,'them',['w10'],False,"Object included in τιθέναι"),
 (15,14,'beds',['w12'],False,"Renders κλιναρίων"),
 (15,15,'and',['w13'],False,"Renders καί without unrelated phrase span"),
 (15,17,'so',['w15'],False,"Second purpose clause belongs to ἵνα; do not reuse ὥστε"),
 (15,18,'that',['w15'],False,"Renders ἵνα"),
 (15,19,'when',['w16'],False,"Renders genitive participle ἐρχομένου"),
 (15,21,'came',['w16'],False,"Renders ἐρχομένου"),
 (15,25,'his',['w19'],False,"English possessive with σκιὰ tied to article/subject phrase"),
 (15,27,'might',['w21'],False,"Subjunctive/modal rendering of ἐπισκιάσῃ"),
 (15,28,'fall',['w21'],False,"Contextual rendering of ἐπισκιάσῃ"),
 (15,29,'on',['w21'],False,"Part of contextual rendering 'fall on' for ἐπισκιάσῃ"),
 (15,32,'them.',['w23'],False,"Renders αὐτῶν without unrelated phrase span"),
 (16,0,'The',['w4'],False,"Article with multitude without unrelated phrase span"),
 (16,3,'the',['w6'],False,"Genitive article in 'from the cities', not repeated w4"),
 (16,5,'around',['w7'],False,"Renders πέριξ without unrelated phrase span"),
 (16,7,'was',['w1'],False,"Auxiliary with συνήρχετο"),
 (16,9,'gathering,',['w1'],False,"Renders συνήρχετο"),
 (16,12,'people',[],True,"English noun completing 'sick people' is supplied"),
 (16,15,'troubled',['w14'],False,"Renders ὀχλουμένους"),
 (16,19,'and',[],True,"English connective before relative healing clause is supplied"),
 (16,20,'they',['w18'],False,"Relative οἵτινες rendered as English subject without unrelated span"),
 (16,21,'were',['w19'],False,"Passive auxiliary with ἐθεραπεύοντο without unrelated span"),
 (16,23,'being',['w19'],False,"Passive progressive support with ἐθεραπεύοντο, not ὀχλουμένους"),
 (33,0,'When',['w3'],False,"Temporal English rendering of participle ἀκούσαντες"),
 (33,1,'they',['w3'],False,"Subject carried by ἀκούσαντες"),
 (33,3,'this,',[],True,"English object of 'heard' is supplied from discourse context"),
 (33,7,'to',[],True,"English idiom 'cut to the heart' supplies preposition"),
 (33,8,'the',[],True,"English idiom 'to the heart' supplies article"),
 (33,10,'and',['w5'],False,"Renders καί without unrelated phrase span"),
 (33,13,'to',['w7'],False,"Infinitival marker with ἀνελεῖν"),
 (36,7,'saying',['w8'],False,"Renders λέγων"),
 (36,8,'that',[],True,"English complementizer after 'saying' is supplied"),
 (36,13,'and',[],True,"English coordination before joined-clause is supplied"),
 (36,22,'him.',['w12'],False,"Dative/relative ᾧ supplies 'him' in 'joined him', not later αὐτῷ"),
 (36,23,'He',['w18'],False,"Relative ὃς starts 'He was killed'"),
 (36,26,'and',['w20'],False,"Renders καί without unrelated phrase span"),
 (36,28,'who',['w22'],False,"Renders ὅσοι"),
 (36,29,'were',['w23'],False,"Passive auxiliary with ἐπείθοντο without unrelated span"),
 (36,33,'were',['w25'],False,"Passive auxiliary with διελύθησαν"),
 (36,34,'scattered',['w25'],False,"Renders διελύθησαν"),
 (36,35,'and',['w26'],False,"Renders second καί"),
 (36,37,'to',['w28'],False,"Renders εἰς without unrelated phrase span"),
 (36,38,'nothing.',['w29'],False,"Renders οὐδέν"),
 (37,0,'After',['w1'],False,"Renders μετά without unrelated phrase span"),
 (37,1,'him',['w2'],False,"Renders τοῦτον as prior referent, not later αὐτοῦ"),
 (37,12,'census',['w11'],False,"Renders ἀπογραφῆς"),
 (37,13,'and',['w12'],False,"Renders καί without unrelated phrase span"),
 (37,17,'after',['w16'],False,"Renders ὀπίσω without unrelated phrase span"),
 (37,18,'him.',['w17'],False,"Renders αὐτοῦ without unrelated phrase span"),
 (37,19,'That',['w18'],False,"Renders κἀκεῖνος ('and that one/he')"),
 (37,20,'man',['w18'],False,"Completes contextual rendering of κἀκεῖνος"),
 (37,21,'also',['w18'],False,"Conjunctive force within κἀκεῖνος"),
 (37,23,'and',['w20'],False,"Renders καί"),
 (37,25,'who',['w22'],False,"Renders ὅσοι"),
 (37,26,'were',['w23'],False,"Passive auxiliary with ἐπείθοντο without unrelated span"),
 (37,29,'him',['w24'],False,"Renders αὐτῷ without unrelated phrase span"),
 (37,30,'were',['w25'],False,"Passive auxiliary with διεσκορπίσθησαν without unrelated span"),
 (37,31,'dispersed.',['w25'],False,"Renders διεσκορπίσθησαν"),
 (40,0,'And',['w1'],False,"Renders opening καί"),
 (40,5,'in,',['w2'],False,"Completes 'calling ... in' rendering of προσκαλεσάμενοι without broad span"),
 (40,6,'they',['w5'],False,"Subject of 'they beat' carried by participle δείραντες"),
 (40,9,'and',[],True,"English coordination between beating and commanding is supplied"),
]

count=apply(6,ed6)+apply(5,ed5)
print(f'Applied {count} reviewed batch-49 corrections in Acts 5-6')
