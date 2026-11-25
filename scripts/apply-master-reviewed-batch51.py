#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data'/'acts'/'03.json'
d=json.loads(path.read_text(encoding='utf8'))
EDITS=[
 (5,0,'And',['w2'],False,"Opening connective renders δὲ"),
 (5,1,'he',['w3'],False,"Subject of ἐπεῖχεν"),
 (5,2,'gave',['w3'],False,"Part of idiom ἐπεῖχεν 'gave attention'"),
 (5,3,'them',['w4'],False,"Renders αὐτοῖς without unrelated phrase span"),
 (5,4,'his',[],True,"English possessive in 'his attention' is supplied"),
 (5,5,'attention,',['w3'],False,"Completes rendering of ἐπεῖχεν"),
 (5,7,'to',['w9'],False,"Infinitival marker with λαβεῖν, not αὐτοῖς"),
 (5,11,'them.',['w8'],False,"Renders αὐτῶν without unrelated phrase span"),

 (6,0,'But',['w2'],False,"Opening connective renders δὲ"),
 (6,6,'I',['w9'],False,"Dative μοι underlies English first-person possession in 'I do not have'"),
 (6,7,'do',[],True,"English auxiliary in 'do not have' is supplied"),
 (6,8,'not',['w7'],False,"Renders οὐχ"),
 (6,10,'but',['w11'],False,"Second-clause connective renders δὲ"),
 (6,15,'I',['w15'],False,"Subject carried by δίδωμι without unrelated span"),
 (6,19,'the',['w17'],False,"Article with name without unrelated phrase span"),
 (6,21,'of',['w19'],False,"Genitival English relation with Jesus"),
 (6,24,'the',['w21'],False,"Article with Nazarene without unrelated phrase span"),
 (6,25,'Nazarene,',['w22'],False,"Renders Ναζωραίου"),
 (6,26,'walk!”',['w25'],False,"Renders περιπάτει"),
 
 (10,0,'and',['w2'],False,"Opening connective renders δὲ, leaving καί w18 for second clause"),
 (10,1,'they',['w1'],False,"Subject of ἐπεγίνωσκον without unrelated span"),
 (10,3,'him',['w3'],False,"Renders αὐτόν without unrelated span"),
 (10,5,'the',['w7'],False,"Article with 'one' without unrelated span"),
 (10,7,'who',['w7'],False,"Substantival article supplies relative English 'who'"),
 (10,8,'used',['w6','w11'],False,"Past habitual support from ἦν + καθήμενος"),
 (10,9,'to',['w11'],False,"Part of habitual 'used to sit' rendering of καθήμενος"),
 (10,13,'at',['w12'],False,"Renders ἐπί without unrelated span"),
 (10,14,'the',['w13'],False,"Article with Beautiful Gate"),
 (10,18,'the',['w16'],False,"Genitive article in 'of the temple'"),
 (10,20,'and',['w18'],False,"Renders καί without unrelated span"),
 (10,21,'they',['w19'],False,"Subject of ἐπλήσθησαν without unrelated span"),
 (10,22,'were',['w19'],False,"Passive auxiliary with ἐπλήσθησαν"),
 (10,26,'and',['w21'],False,"Renders second καί without unrelated span"),
 (10,27,'astonishment',['w22'],False,"Renders ἐκστάσεως"),
 (10,28,'at',['w23'],False,"Renders ἐπί without unrelated span"),
 (10,29,'what',['w24','w25'],False,"Relative/article phrase τῷ συμβεβηκότι rendered as 'what had happened'"),

 (12,0,'When',['w1'],False,"Temporal English rendering of participle ἰδών"),
 (12,2,'saw',['w1'],False,"Renders ἰδών without unrelated span"),
 (12,3,'this,',['w14'],False,"Renders τούτῳ as discourse demonstrative"),
 (12,4,'he',['w5'],False,"Subject of ἀπεκρίνατο"),
 (12,6,'to',['w6'],False,"Renders πρός without unrelated span"),
 (12,7,'the',['w7'],False,"Article with people"),
 (12,11,'Israel,',['w10'],False,"Renders Ἰσραηλῖται"),
 (12,12,'why',['w11'],False,"Renders first τί without unrelated span"),
 (12,14,'you',['w12'],False,"Subject of θαυμάζετε without unrelated span"),
 (12,15,'marvel',['w12'],False,"Renders θαυμάζετε"),
 (12,18,'or',['w15'],False,"Renders ἢ without unrelated span"),
 (12,21,'you',['w18'],False,"Subject of ἀτενίζετε without unrelated span"),
 (12,22,'stare',['w18'],False,"Renders ἀτενίζετε"),
 (12,23,'at',['w16'],False,"Dative ἡμῖν rendered as 'at us', not earlier ἐπί"),
 (12,24,'us',['w16'],False,"Renders ἡμῖν"),
 (12,31,'or',['w22'],False,"Renders second ἢ without unrelated span"),
 
 (26,0,'For',[],True,"English discourse connective is supplied"),
 (26,1,'you',['w1'],False,"Renders ὑμῖν without unrelated span"),
 (26,7,'his',['w8'],False,"Renders αὐτοῦ without unrelated span"),
 (26,10,'him',['w11'],False,"Renders αὐτόν without unrelated span"),
 (26,11,'to',['w12'],False,"Infinitival English support with εὐλογοῦντα, not ὑμῖν"),
 (26,13,'you',['w13'],False,"Renders ὑμᾶς without unrelated span"),
 (26,14,'by',['w14','w15'],False,"Contextual rendering of ἐν τῷ with verbal infinitive"),
 (26,17,'of',[],True,"English partitive glue in 'each of you' is supplied"),
 (26,18,'you',['w21'],False,"Possessive/plural reference ὑμῶν rendered in partitive phrase"),
 (26,20,'from',['w18'],False,"Renders ἀπό"),
 (26,21,'your',['w21'],False,"Renders ὑμῶν without unrelated span"),
 (26,22,'wicked',['w20'],False,"Renders πονηριῶν"),
 (26,23,'ways.”',['w20'],False,"Contextual nominal rendering of πονηριῶν"),
]
count=0
for vn,idx,expected,ids,supplied,reason in EDITS:
    verse=next(v for v in d['verses'] if v['v']==vn); x=verse['alignment']['dgt'][idx]
    if x.get('text')!=expected: raise SystemExit(f"Acts 3:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids)
    if supplied: x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else: x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 51: '+reason; count+=1
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-51 corrections in Acts 3')
