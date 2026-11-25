#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data'/'acts'/'24.json'
d=json.loads(path.read_text(encoding='utf8'))

EDITS=[
 (12,3,'not',['w2'],False,"Negative force of οὔτε in the first clause"),
 (12,9,'disputing',['w10'],False,"Renders διαλεγόμενον"),
 (12,13,'causing',['w13'],False,"Renders ποιοῦντα in 'causing a crowd to gather'"),
 (12,17,'gather,',['w12','w13'],False,"Contextual rendering of ἐπίστασιν ποιοῦντα ('causing a gathering')"),
 (12,18,'either',['w15'],False,"Renders second οὔτε in the correlative sequence"),
 (12,19,'in',['w16'],False,"Renders ἐν without unrelated phrase span"),
 (12,20,'the',['w17'],False,"Article with synagogues without unrelated phrase span"),
 (12,22,'or',['w19'],False,"Renders third οὔτε, not earlier ἢ"),
 (12,23,'throughout',['w20'],False,"Renders κατά in the city phrase"),
 (12,24,'the',['w21'],False,"Article with city without unrelated phrase span"),
 (14,1,'I',['w1'],False,"Subject of ὁμολογῶ without unrelated phrase span"),
 (14,4,'to',['w4'],False,"Dative 'to you' without unrelated phrase span"),
 (14,6,'that',['w5'],False,"Renders ὅτι without unrelated phrase span"),
 (14,8,'to',['w6'],False,"Part of κατὰ rendering 'according to' without unrelated phrase span"),
 (14,16,'in',['w12'],False,"Renders οὕτως ('in this way'), not πᾶσι"),
 (14,17,'this',['w12'],False,"Part of 'in this way' rendering of οὕτως"),
 (14,18,'way',['w12'],False,"Part of 'in this way' rendering of οὕτως, not ὁδόν"),
 (14,19,'I',['w13'],False,"Subject of λατρεύω without unrelated phrase span"),
 (14,24,'our',['w15'],False,"Renders ancestral/πατρῴῳ as 'our fathers'"),
 (14,25,'fathers,',['w15'],False,"Renders πατρῴῳ ('ancestral/fathers')"),
 (14,30,'according',['w20'],False,"Second 'according' renders second κατά, not earlier w6"),
 (14,36,'in',['w25'],False,"Renders ἐν without unrelated phrase span"),
 (22,2,'having',['w9'],False,"Participial support for εἰδὼς ('having knowledge')"),
 (22,5,'accurate',['w8'],False,"Renders ἀκριβέστερον"),
 (22,6,'knowledge',['w9'],False,"Renders εἰδὼς/knowing as noun phrase"),
 (22,8,'the',['w12'],False,"Article with Way, not τὰ w10"),
 (22,10,'postponed',['w3'],False,"Renders Ἀνεβάλετο"),
 (22,15,'the',['w17'],False,"Article with commander without unrelated phrase span"),
 (22,21,'decide',['w20'],False,"Renders διαγνώσομαι"),
 (22,22,'your',['w23'],False,"Renders ὑμᾶς in 'your case' without unrelated phrase span"),
 (22,23,'case.”',['w21','w22','w23'],False,"Contextual rendering of τὰ καθʼ ὑμᾶς ('your case')"),
]

count=0
for vn,idx,expected,ids,supplied,reason in EDITS:
    verse=next(v for v in d['verses'] if v['v']==vn)
    x=verse['alignment']['dgt'][idx]
    if x.get('text') != expected:
        raise SystemExit(f"Acts 24:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids)
    if supplied:
        x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 39: '+reason
    count+=1

path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-39 corrections in Acts 24')
