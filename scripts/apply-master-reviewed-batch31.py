#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'acts'

EDITS=[
 (21,18,0,'And',['w2'],False,"Opening connective renders δέ, not later τε"),
 (21,2,11,'and',[],True,"English coordination before 'set sail' has no separate Greek conjunction"),
 (21,40,17,'When',['w18'],False,"Second temporal 'When' belongs to γενομένης ('having taken place')"),
 (21,6,0,'and',[],True,"Verse-opening English continuation has no separate Greek conjunction"),
 (21,6,3,'to',['w2'],False,"'to one another' belongs with ἀλλήλους, not later εἰς"),
 (21,6,12,'and',['w9'],False,"Connective before 'they returned' renders δέ"),
 (22,10,0,'And',['w2'],False,"First connective renders δέ, not the later δέ before 'the Lord said'"),
 (22,10,32,'have',['w22'],False,"Perfect auxiliary in 'have been appointed' belongs with τέτακται"),
 (22,17,0,'“And',['w2'],False,"Opening connective renders δέ, not later καί"),
 (22,17,4,'I',['w3'],False,"First-person participant in 'when I returned' is represented by μοι ('to me')"),
 (22,23,0,'And',['w2'],False,"Opening connective renders τε, not later καί"),
 (22,23,7,'throwing',['w5'],False,"First action 'throwing off' renders ῥιπτούντων, not later βαλλόντων"),
 (22,23,9,'their',[],True,"Possessive 'their garments' is contextual English; αὐτῶν is the subject of shouting"),
 (22,26,4,'this,',[],True,"Object 'this' in 'heard this' is supplied by English context, not later οὗτος"),
 (22,26,6,'went',['w5'],False,"'went to the commander' renders προσελθών ('having gone/come near')"),
 (22,27,4,'and',['w2'],False,"Coordination between 'came' and 'said' renders δέ"),
 (22,27,15,'said,',['w15'],False,"Second 'said' renders ἔφη, not the earlier εἶπεν"),
 (22,5,24,'and',[],True,"English coordination before 'was traveling' has no separate Greek καί"),
 (22,7,0,'And',['w2'],False,"Opening connective renders τε, not the later καί"),
 (23,18,4,'and',[],True,"English coordination between 'took' and 'brought' has no separate Greek καί"),
 (23,18,17,'and',[],True,"English coordination before 'asked' has no separate Greek καί"),
 (23,18,20,'to',['w21'],False,"Infinitive marker before 'bring' belongs to ἀγαγεῖν"),
 (23,18,21,'bring',['w21'],False,"Second 'bring' renders ἀγαγεῖν, not earlier ἤγαγεν"),
 (23,18,28,'he',['w24'],False,"Subject of 'he has something' is carried by ἔχοντα ('having')"),
 (23,18,29,'has',['w24'],False,"'has something' renders ἔχοντα ('having')"),
 (23,27,19,'them',[],True,"Object in 'came upon them' is supplied by English; no second αὐτῶν"),
 (23,27,23,'and',[],True,"English coordination before 'rescued' has no separate Greek καί"),
 (23,27,25,'him,',[],True,"Object of 'rescued him' is the continuing man; μαθών belongs to the following 'having learned'"),
 (23,9,0,'And',['w2'],False,"Opening connective renders δέ, not later καί"),
 (23,9,18,'and',[],True,"English coordination between 'stood up' and 'began arguing' has no separate Greek καί"),
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
    x=D[idx]
    target=list(ids)
    already=(x.get('ids',[])==target and bool(x.get('supplied'))==supplied and str(x.get('confidence','')).startswith('reviewed-master-'))
    if already:
        continue
    x['ids']=target
    x['phraseIds']=target.copy()
    if supplied:
        x['supplied']=True
        x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None)
        x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 31: '+reason
    count+=1

for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-31 corrections across {len(changed)} Acts chapter files')
