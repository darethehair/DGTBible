#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data'/'acts'/'04.json'
d=json.loads(path.read_text(encoding='utf8'))

EDITS=[
 (5,0,'And',['w2'],False,"Opening connective renders δὲ, not later καί w10"),
 (5,2,'the',['w4'],False,"Article with next day without unrelated phrase span"),
 (5,7,'and',['w10'],False,"Renders first καί"),
 (5,9,'and',['w13'],False,"Renders second καί"),
 (5,11,'gathered',['w6'],False,"Renders συναχθῆναι"),
 (5,12,'together',['w6'],False,"Completes contextual rendering of συναχθῆναι"),
 (5,13,'in',['w16'],False,"Renders ἐν without unrelated phrase span"),

 (6,0,'and',['w1'],False,"Renders opening καί"),
 (6,2,'the',['w3'],False,"Article with high priest"),
 (6,8,'and',['w11'],False,"Final list connective renders καί rather than supplied glue"),
 (6,13,'from',['w14'],False,"Renders ἐκ"),
 (6,14,'the',[],True,"English article in 'the high-priestly family' is supplied"),
 (6,15,'high-priestly',['w16'],False,"Renders ἀρχιερατικοῦ"),
 (6,16,'family.',['w15'],False,"Renders γένους"),

 (17,0,'But',['w1'],False,"Renders ἀλλʼ"),
 (17,2,'that',['w2'],False,"Renders ἵνα"),
 (17,6,'no',['w3'],False,"Negation 'no further' renders μή, not later μηδενί"),
 (17,9,'the',['w8'],False,"Article with people without unrelated phrase span"),
 (17,13,'threaten',['w11'],False,"Renders ἀπειλησώμεθα"),
 (17,15,'to',['w14'],False,"Infinitival marker with λαλεῖν"),
 (17,17,'no',['w13'],False,"Renders μηκέτι"),
 (17,19,'to',['w19'],False,"Dative 'to anyone' without unrelated phrase span"),
 (17,20,'anyone',['w19','w20'],False,"Renders μηδενὶ ἀνθρώπων"),
 
 (22,1,'the',['w6'],False,"Article with man"),
 (22,7,'of',['w14'],False,"Genitive article in 'of healing', not ἐτῶν"),
 (22,15,'years',['w1'],False,"Renders ἐτῶν"),
 (22,16,'old.',[],True,"English age idiom supplies 'old'"),

 (32,0,'Now',['w2'],False,"Opening discourse connective renders δὲ"),
 (32,1,'the',['w1'],False,"Article with multitude, not noun πλήθους"),
 (32,3,'of',['w1'],False,"Genitive article Τοῦ introduces 'of those who believed'"),
 (32,4,'those',['w4'],False,"Substantival article τῶν rendered as 'those'"),
 (32,5,'who',['w4'],False,"Relative English support from substantival article"),
 (32,10,'and',['w9'],False,"Renders first καί without unrelated phrase span"),
 (32,12,'and',['w13'],False,"Renders second καί without unrelated phrase span"),
 (32,14,'one',['w15'],False,"Renders εἷς without unrelated phrase span"),
 (32,15,'was',['w20'],False,"Auxiliary with ἔλεγεν"),
 (32,16,'saying',['w20'],False,"Renders ἔλεγεν"),
 (32,17,'that',[],True,"English complementizer before possession clause is supplied"),
 (32,18,'any',['w16'],False,"Renders τι"),
 (32,19,'of',['w17'],False,"Genitive article before possessions"),
 (32,20,'his',['w19'],False,"First possessive 'his possessions' renders αὐτῷ, not ἴδιον"),
 (32,22,'was',['w22'],False,"Infinitive/copular rendering of εἶναι"),
 (32,23,'his',['w21'],False,"Possessive adjective ἴδιον"),
 (32,24,'own,',['w21'],False,"Renders ἴδιον"),
 (32,26,'they',['w25'],False,"Dative plural αὐτοῖς supplies English subject in 'they had'"),
 (32,27,'had',['w24'],False,"Renders ἦν in idiomatic possessive construction"),
 (32,30,'in',['w27'],False,"Part of κοινά 'in common' without broad span"),

 (33,0,'And',['w1'],False,"Renders opening καί"),
 (33,4,'the',['w5'],False,"Article with testimony without unrelated phrase span"),
 (33,10,'the',['w9'],False,"Genitive article with resurrection without unrelated span"),
 (33,12,'of',['w11'],False,"Genitive article in 'of the Lord' without unrelated span"),
 (33,13,'the',['w11'],False,"Article in 'of the Lord' without unrelated span"),
 (33,16,'and',['w15'],False,"Second-clause connective renders τε, not opening καί"),
 (33,17,'great',['w16'],False,"Second 'great' renders μεγάλη w16, not μεγάλῃ w3"),

 (35,0,'and',['w1'],False,"Renders opening καί"),
 (35,4,'the',['w4'],False,"Article with feet"),
 (35,7,'and',['w9'],False,"Second-clause connective renders δὲ, not opening καί"),
 
 (36,0,'Now',['w2'],False,"Renders δὲ"),
 (36,3,'was',['w4'],False,"Passive auxiliary with ἐπικληθεὶς"),
 (36,4,'surnamed',['w4'],False,"Renders ἐπικληθεὶς"),
 (36,7,'the',['w7'],False,"Article with apostles without unrelated phrase span"),
 (36,8,'apostles—which',['w8','w9'],False,"Completes apostles and begins relative ὅ without broad span"),
 (36,13,'Encouragement—a',['w13','w14'],False,"Completes παρακλήσεως and English transition to Levite"),
 (36,17,'by',['w16'],False,"Dative/article in idiom 'by birth', not earlier ἀπό"),
]

count=0
for vn,idx,expected,ids,supplied,reason in EDITS:
    verse=next(v for v in d['verses'] if v['v']==vn)
    x=verse['alignment']['dgt'][idx]
    if x.get('text') != expected:
        raise SystemExit(f"Acts 4:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids)
    if supplied:
        x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 50: '+reason
    count+=1

path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-50 corrections in Acts 4')
