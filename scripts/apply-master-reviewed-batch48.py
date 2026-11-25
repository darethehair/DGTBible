#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data'/'acts'/'07.json'
d=json.loads(path.read_text(encoding='utf8'))

EDITS=[
 (3,2,'to',['w3'],False,"Renders πρός without unrelated phrase span"),
 (3,6,'from',['w6'],False,"Renders first ἐκ without unrelated phrase span"),
 (3,7,'your',['w9'],False,"Renders σου without unrelated phrase span"),
 (3,8,'land',['w8'],False,"First 'land' renders γῆς w8, not later γῆν w19"),
 (3,9,'and',['w10'],False,"Renders καί without unrelated phrase span"),
 (3,10,'from',['w11'],False,"Renders second ἐκ without unrelated phrase span"),
 (3,11,'your',['w14'],False,"Renders second σου without unrelated phrase span"),
 (3,12,'relatives',['w13'],False,"Renders συγγενείας"),
 (3,13,'and',['w15'],False,"Renders third καί without unrelated phrase span"),
 (3,16,'the',['w18'],False,"Article with second land without unrelated phrase span"),
 (3,18,'that',['w20'],False,"Relative pronoun ἣν rendered as 'that'"),
 (3,22,'you.’',['w22'],False,"Renders dative σοι without unrelated phrase span"),

 (6,0,'And',['w2'],False,"Opening connective renders δὲ, not later καί w15"),
 (6,3,'this',['w3'],False,"Part of οὕτως ('this way')"),
 (6,6,'his',['w10'],False,"Possessive 'his offspring' renders αὐτοῦ, not ἔσται"),
 (6,10,'foreigners',['w11'],False,"Contextual rendering of πάροικον"),
 (6,12,'a',['w13'],False,"English article with γῇ, not πάροικον"),
 (6,14,'belonging',['w14'],False,"Contextual rendering of ἀλλοτρίᾳ ('belonging to others/foreign')"),
 (6,16,'others,',['w14'],False,"Completes contextual rendering of ἀλλοτρίᾳ"),
 (6,17,'and',['w15'],False,"Renders καί without unrelated phrase span"),
 (6,18,'they',['w16'],False,"Subject carried by δουλώσουσιν without unrelated phrase span"),
 (6,21,'and',['w18'],False,"Renders second καί without unrelated phrase span"),
 (6,23,'them',['w17','w19'],False,"Object αὐτό carried through both coordinated verbs"),
 (6,27,'years.',['w20'],False,"Renders ἔτη"),

 (13,0,'And',['w1'],False,"Renders opening καί without unrelated phrase span"),
 (13,2,'the',['w3'],False,"Article with second visit without unrelated phrase span"),
 (13,4,'visit',['w4'],False,"Contextual rendering of δευτέρῳ ('second time/visit')"),
 (13,5,'Joseph',['w6'],False,"Renders Ἰωσὴφ without unrelated phrase span"),
 (13,7,'made',['w5'],False,"Part of passive rendering ἀνεγνωρίσθη ('was made known/recognized')"),
 (13,8,'known',['w5'],False,"First 'known' renders ἀνεγνωρίσθη, not later φανερόν"),
 (13,9,'to',['w7','w8'],False,"Dative relation to brothers"),
 (13,10,'his',['w9'],False,"Renders αὐτοῦ without unrelated phrase span"),
 (13,12,'and',['w10'],False,"Renders second καί without unrelated phrase span"),
 (13,13,'Joseph’s',['w18'],False,"Genitival English rendering of Ἰωσήφ"),
 (13,16,'known',['w11'],False,"Second 'known' renders φανερόν"),
 (13,17,'to',['w13'],False,"Dative/article before Pharaoh without unrelated phrase span"),

 (14,3,'and',[],True,"English coordination between sent and called is supplied"),
 (14,7,'his',['w8'],False,"Renders αὐτοῦ without unrelated phrase span"),
 (14,9,'and',['w9'],False,"Renders καί without unrelated phrase span"),
 (14,10,'all',['w10'],False,"Renders πᾶσαν without unrelated phrase span"),
 (14,11,'his',['w8'],False,"Possessive 'his relatives' carried by αὐτοῦ"),
 (14,12,'relatives,',['w12'],False,"Renders συγγένειαν"),
 (14,13,'seventy-five',['w16','w17'],False,"Renders ἑβδομήκοντα πέντε"),
 (14,16,'all.',['w14'],False,"Renders ἐν as 'in all' without unrelated phrase span"),

 (21,0,'And',['w2'],False,"Opening connective renders δὲ, leaving καί w9 for second clause"),
 (21,8,'him',['w5'],False,"Renders first αὐτόν without unrelated phrase span"),
 (21,9,'up',['w4'],False,"Completes 'took him up' rendering of ἀνείλατο, not later ἀνεθρέψατο"),
 (21,10,'and',['w9'],False,"Renders καί"),
 (21,12,'him',['w11'],False,"Renders second αὐτόν without unrelated phrase span"),
 (21,14,'her',['w12'],False,"Renders ἑαυτῇ without unrelated phrase span"),
 (21,15,'own',['w12'],False,"Part of reflexive rendering ἑαυτῇ without unrelated phrase span"),

 (22,0,'And',['w1'],False,"Renders opening καί without unrelated phrase span"),
 (22,2,'was',['w2'],False,"Passive auxiliary with ἐπαιδεύθη without unrelated phrase span"),
 (22,4,'in',[],True,"English preposition before 'all the wisdom' is supplied"),
 (22,6,'the',['w6'],False,"Article within 'the wisdom' tied to σοφίᾳ without unrelated span"),
 (22,8,'of',['w7'],False,"Genitival rendering of Αἰγυπτίων without unrelated phrase span"),
 (22,9,'the',['w7'],False,"English article with Egyptians tied to Αἰγυπτίων"),
 (22,11,'and',['w9'],False,"Second-clause connective renders δὲ, not καί w13"),

 (31,0,'When',['w8'],False,"Temporal clause belongs to προσερχομένου ('when approaching'), not first sight clause"),
 (31,2,'saw',['w4'],False,"Renders ἰδὼν without unrelated phrase span"),
 (31,3,'it,',['w7'],False,"Object 'it' refers to ὅραμα"),
 (31,9,'and',['w9'],False,"Connective before approach clause renders δὲ, not earlier δὲ w2"),
 (31,11,'he',['w10'],False,"Renders αὐτοῦ without unrelated phrase span"),
 (31,14,'look',['w11'],False,"Renders κατανοῆσαι without unrelated phrase span"),
 (31,17,'the',['w13'],False,"Article in English 'the voice' tied to φωνή"),
 (31,20,'the',[],True,"English article in 'of the Lord' is supplied"),

 (38,1,'is',['w2'],False,"Renders ἐστιν without unrelated phrase span"),
 (38,2,'the',['w3'],False,"Article with 'one' without unrelated phrase span"),
 (38,4,'who',['w4'],False,"Relative English support for substantival participle γενόμενος, not later τοῦ w14"),
 (38,5,'was',['w4'],False,"Renders γενόμενος"),
 (38,6,'in',['w5'],False,"Renders first ἐν without unrelated phrase span"),
 (38,7,'the',['w6'],False,"Article with assembly without unrelated phrase span"),
 (38,8,'assembly',['w7'],False,"Renders ἐκκλησίᾳ without unrelated phrase span"),
 (38,9,'in',['w8'],False,"Renders second ἐν without unrelated phrase span"),
 (38,10,'the',['w9'],False,"Article with wilderness without unrelated phrase span"),
 (38,13,'the',['w12'],False,"Article with angel without unrelated phrase span"),
 (38,15,'who',['w14'],False,"Relative article τοῦ introducing λαλοῦντος"),
 (38,17,'to',['w16'],False,"Dative 'to him' without unrelated phrase span"),
 (38,23,'with',['w22'],False,"Second 'with our fathers' is carried by the genitive coordination, not first μετὰ"),
 (38,24,'our',['w24'],False,"Renders ἡμῶν without unrelated phrase span"),
 (38,26,'who',['w25'],False,"Renders relative ὃς without unrelated phrase span"),
 (38,29,'words',['w27'],False,"Renders λόγια"),
 (38,30,'to',['w29'],False,"Infinitival marker with δοῦναι without unrelated phrase span"),
 (38,32,'to',['w30'],False,"Dative 'to us' without unrelated phrase span"),
 (38,33,'us.',['w30'],False,"Renders ἡμῖν without unrelated phrase span"),

 (40,1,'to',['w2'],False,"Dative/article before Aaron, not Aaron itself"),
 (40,5,'for',['w5'],False,"Dative ἡμῖν rendered as 'for us', not γὰρ w11"),
 (40,6,'us',['w5'],False,"Renders ἡμῖν without unrelated phrase span"),
 (40,7,'who',['w7'],False,"Renders relative οἳ without unrelated phrase span"),
 (40,11,'us,',['w9'],False,"Renders ἡμῶν without unrelated phrase span"),
 (40,15,'who',['w14'],False,"Renders relative ὃς without unrelated phrase span"),
 (40,17,'us',['w16'],False,"Renders ἡμᾶς without unrelated phrase span"),
 (40,20,'the',['w18'],False,"Article supplied within γῆς 'the land' without unrelated span"),
 (40,23,'Egypt—we',['w19'],False,"Renders Αἰγύπτου plus English clause boundary"),
 (40,24,'do',[],True,"English auxiliary in 'do not know' is supplied"),

 (46,13,'the',['w11'],False,"Article/dative in 'for the God' without unrelated phrase span"),

 (50,0,'Did',['w5'],False,"English interrogative auxiliary tied to ἐποίησεν"),
 (50,2,'my',['w4'],False,"Renders μου without unrelated phrase span"),

 (59,0,'And',['w1'],False,"Renders καί without unrelated phrase span"),
 (59,5,'as',['w1'],False,"English subordinate force of opening καί retained as 'as'"),
 (59,9,'and',['w6'],False,"Renders second καί without unrelated phrase span"),
 (59,14,'my',['w13'],False,"Renders μου without unrelated phrase span"),
]

count=0
for vn,idx,expected,ids,supplied,reason in EDITS:
    verse=next(v for v in d['verses'] if v['v']==vn)
    x=verse['alignment']['dgt'][idx]
    if x.get('text') != expected:
        raise SystemExit(f"Acts 7:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids)
    if supplied:
        x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 48: '+reason
    count+=1

path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-48 corrections in Acts 7')
