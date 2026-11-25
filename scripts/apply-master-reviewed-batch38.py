#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data'/'acts'/'25.json'
d=json.loads(path.read_text(encoding='utf8'))

EDITS=[
 (5,3,'“let',[],True,"English imperative support for the participial/imperatival construction"),
 (5,4,'the',['w1'],False,"Opening article refers to the powerful men (Οἱ ... δυνατοὶ), not the later τῷ"),
 (5,6,'men',['w1','w6'],False,"Renders the substantival Οἱ ... δυνατοὶ ('the powerful [men]')"),
 (5,9,'come',['w7'],False,"Renders συγκαταβάντες without unrelated phrase span"),
 (5,19,'in',['w11'],False,"Renders ἐν without unrelated phrase span"),
 (5,22,'let',[],True,"English imperative support for κατηγορείτωσαν"),
 (5,23,'them',['w15'],False,"Subject of 'let them accuse' carried by κατηγορείτωσαν"),
 (16,2,'them',['w2'],False,"Renders relative οὓς without unrelated phrase span"),
 (16,7,'the',['w7'],False,"Article supplied within 'the custom' rendering without unrelated span"),
 (16,9,'of',['w8'],False,"English genitival rendering of dative Ῥωμαίοις ('of Romans'), not ἀπολογίας"),
 (16,11,'to',['w9'],False,"Infinitival marker with χαρίζεσθαι"),
 (16,12,'hand',['w9'],False,"Part of contextual rendering 'hand over' for χαρίζεσθαι"),
 (16,17,'the',['w16'],False,"Article with accused without unrelated phrase span"),
 (16,20,'his',['w20'],False,"Possessive in 'has his accusers' carried by ἔχοι context without unrelated phrase span"),
 (16,26,'receives',['w26'],False,"Renders λάβοι ('receives/has')"),
 (16,32,'the',['w28'],False,"Article with charge without unrelated phrase span"),
 (16,33,'charge.',['w29'],False,"Renders ἐγκλήματος"),
 (17,3,'came',['w1'],False,"Part of συνελθόντων ('came together')"),
 (17,4,'together',['w1'],False,"Part of συνελθόντων ('came together')"),
 (17,6,'I',['w7'],False,"Subject of 'I made no delay' is carried by ποιησάμενος, not later ἐκέλευσα"),
 (17,11,'on',['w8'],False,"Renders τῇ in temporal phrase without unrelated span"),
 (17,12,'the',['w8'],False,"Renders τῇ in 'on the next day' without unrelated span"),
 (17,16,'on',['w11'],False,"Renders ἐπὶ without unrelated span"),
 (17,17,'the',['w12'],False,"Article with judgment seat without unrelated span"),
 (17,22,'the',['w16'],False,"Article with man without unrelated span"),
 (18,5,'him,',['w2'],False,"Renders relative οὗ ('whom/him') without unrelated span"),
 (18,6,'they',['w5'],False,"Subject of 'they brought' is the accusers, not participle σταθέντες"),
 (18,11,'the',['w9'],False,"English article in 'the evil things' tied to relative ὧν, not earlier οἱ"),
 (26,1,'him',['w2'],False,"'Concerning him' renders περὶ οὗ; not the later αὐτόν"),
 (26,2,'I',['w9'],False,"Subject of 'I have nothing' carried by ἔχω"),
 (26,3,'have',['w9'],False,"Renders ἔχω, not γράψαι"),
 (26,4,'nothing',['w8','w4'],False,"Renders οὐκ + τι in context"),
 (26,5,'certain',['w3'],False,"Renders ἀσφαλές"),
 (26,12,'I',['w11'],False,"Subject of 'I brought' carried by προήγαγον without unrelated span"),
 (26,15,'before',['w13'],False,"Renders ἐφʼ without unrelated span"),
 (26,16,'you',['w14'],False,"Renders ὑμῶν without unrelated span"),
 (26,20,'before',['w17'],False,"Renders ἐπί without unrelated span"),
 (26,21,'you,',['w18'],False,"Renders σοῦ without unrelated span"),
 (26,27,'the',['w22'],False,"Article/temporal marker with examination without unrelated span"),
 (26,29,'I',['w25'],False,"Subject of σχῶ without unrelated span"),
 (26,30,'may',['w25'],False,"Subjunctive/modal rendering of σχῶ"),
 (26,31,'have',['w25'],False,"Renders σχῶ without unrelated span"),
]

count=0
for vn,idx,expected,ids,supplied,reason in EDITS:
    verse=next(v for v in d['verses'] if v['v']==vn)
    x=verse['alignment']['dgt'][idx]
    if x.get('text') != expected:
        raise SystemExit(f"Acts 25:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids)
    if supplied:
        x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 38: '+reason
    count+=1

path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-38 corrections in Acts 25')
