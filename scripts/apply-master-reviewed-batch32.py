#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'acts'

EDITS=[
 (24,2,0,'And',['w2'],False,"Opening connective renders δέ, not the later καί"),
 (24,9,5,'the',[],True,"Article in 'the attack' is supplied English; Greek article w4 belongs to 'The Jews'"),
 (24,10,5,'for',[],True,"Purpose 'for him to speak' is natural English around λέγειν; not ἐκ w10"),
 (24,23,0,'And',[],True,"Verse-opening English connective has no separate Greek conjunction"),
 (24,25,21,'when',['w25'],False,"Second temporal 'when I find' belongs to μεταλαβών ('having found')"),
 (24,26,5,'was',['w4'],False,"Auxiliary in 'was hoping' belongs to ἐλπίζων"),
 (24,26,18,'he',['w19'],False,"Subject of 'he was sending' is carried by μεταπεμπόμενος"),
 (24,26,19,'was',['w19'],False,"Auxiliary in 'was sending' belongs to μεταπεμπόμενος"),
 (24,26,26,'conversing',['w20'],False,"'conversing' directly renders ὡμίλει"),
 (25,13,13,'and',[],True,"Coordination before participial 'greeted' is supplied English"),
 (25,19,17,'had',['w15'],False,"Perfect auxiliary in 'had died' belongs to τεθνηκότος"),
 (25,20,0,'And',['w2'],False,"Opening connective renders δέ, not κἀκεῖ"),
 (25,20,8,'things,',['w7'],False,"First 'these things' belongs to τούτων w7, not later τούτων w18"),
 (25,20,13,'was',['w11'],False,"Auxiliary in 'was willing' belongs to βούλοιτο"),
 (26,10,0,'And',['w2'],False,"Opening connective renders initial καί w2"),
 (26,11,15,'And',['w12'],False,"Second clause connective renders τε w12, not opening καί"),
 (26,21,4,'the',[],True,"Article before 'Jews' is supplied English; Greek has bare Ἰουδαῖοι"),
 (26,21,16,'me.',[],True,"Object of 'kill me' is contextual English; no repeated Greek με"),
 (26,24,4,'saying',['w4'],False,"First 'saying' describes Paul's defense and belongs to ἀπολογουμένου"),
 (26,24,8,'his',['w3'],False,"Possessive subject in 'his defense' belongs to αὐτοῦ"),
 (26,24,25,'is',['w19'],False,"Progressive auxiliary in 'is driving' belongs to περιτρέπει"),
 (26,3,17,'you',[],True,"Object in 'I ask you to listen' is supplied; σε w4 belongs to 'you are an expert'"),
 (27,12,0,'And',['w2'],False,"Opening connective renders δέ, not later καί"),
 (27,30,8,'from',['w6'],False,"'from the ship' renders first ἐκ w6"),
 (27,30,21,'of',[],True,"'under pretense of intending' uses supplied English 'of', not ἐκ"),
 (28,1,2,'we',['w2'],False,"Subject of 'we had been brought safely through' is carried by διασωθέντες"),
]

changed={}
count=0
for ch,vn,idx,expected,ids,supplied,reason in EDITS:
    path=DATA/f'{ch:02}.json'
    d=changed.get(path)
    if d is None:
        d=json.loads(path.read_text(encoding='utf8')); changed[path]=d
    verse=next(v for v in d['verses'] if v['v']==vn)
    D=verse['alignment']['dgt']
    if idx>=len(D) or D[idx].get('text')!=expected:
        got=D[idx].get('text') if idx<len(D) else '<missing>'
        raise SystemExit(f'Acts {ch}:{vn} token {idx}: expected {expected!r}, got {got!r}')
    x=D[idx]; target=list(ids)
    already=(x.get('ids',[])==target and bool(x.get('supplied'))==supplied and str(x.get('confidence','')).startswith('reviewed-master-'))
    if already: continue
    x['ids']=target; x['phraseIds']=target.copy()
    if supplied:
        x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 32: '+reason
    count+=1

for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-32 corrections across {len(changed)} Acts chapter files')
