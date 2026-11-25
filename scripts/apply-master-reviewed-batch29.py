#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'acts'

EDITS=[
 (19,17,0,'And',['w2'],False,"Opening connective renders δέ, not later καί"),
 (19,17,8,'and',['w8'],False,"Conjunction between Jews and Greeks renders καί w8"),
 (19,18,0,'And',['w2'],False,"Opening connective renders τε, not later καί"),
 (19,22,0,'And',['w2'],False,"Opening connective renders δέ, not conjunction between Timothy and Erastus"),
 (19,25,21,'have',['w20'],False,"Idiomatic 'we have' is carried by ἐστιν ('is') with ἡμῖν ('to us')"),
 (19,27,0,'And',['w3'],False,"Opening connective renders δέ, not later τε"),
 (19,27,9,'of',[],True,"Possessive phrasing 'trade of ours' is natural English for ἡμῖν; no separate genitive token"),
 (19,27,35,'is',['w23'],False,"'is about to' is carried by μέλλειν, not earlier κινδυνεύει"),
 (19,31,6,'were',['w6'],False,"Copular 'were' in 'were his friends' renders ὄντες ('being')"),
 (19,32,7,'and',[],True,"Coordination in 'one thing and some another' is English rendering of the contrast; later καί belongs to next clause"),
 (19,33,0,'And',['w2'],False,"Opening connective renders first δέ"),
 (19,35,2,'city',['w4'],False,"'city clerk' renders γραμματεύς ('town clerk'), not later πόλιν"),
 (19,35,7,'and',[],True,"English coordination before 'said' has no separate Greek καί"),
 (19,35,20,'that',[],True,"English complementizer before 'the city' has no separate Greek source token"),
 (19,8,0,'And',['w2'],False,"Opening connective renders δέ, not later καί"),
 (19,9,20,'and',[],True,"English coordination between withdrawing and separating has no separate Greek καί"),
 (20,1,12,'and',[],True,"English coordination before the farewell participle has no separate Greek καί"),
 (20,1,13,'after',[],True,"Temporal 'after' before the farewell participle is supplied English"),
 (20,12,0,'And',['w2'],False,"Opening connective renders δέ, not later καί"),
 (20,2,0,'And',['w2'],False,"Opening connective renders δέ, not later καί"),
 (20,24,26,'to',['w28'],False,"Infinitive marker before 'testify' belongs to διαμαρτύρασθαι, not τελειῶσαι"),
 (20,25,11,'I',['w16'],False,"First-person subject of 'I went about' is carried by διῆλθον"),
 (20,25,19,'my',['w11'],False,"Possessive before 'face' renders μου ('of me')"),
 (20,31,12,'did',['w10'],False,"Past auxiliary in 'did not stop' belongs with ἐπαυσάμην ('I ceased')"),
 (20,32,19,'you',[],True,"Object in 'build you up' is supplied by English context; no separate ὑμᾶς here"),
 (20,32,23,'you',[],True,"Recipient in 'give you the inheritance' is supplied by English context"),
 (20,36,12,'and',[],True,"English coordination before 'prayed' has no separate Greek καί"),
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
    x['reason']='Human-reviewed full-NT master pass batch 29: '+reason
    count+=1

for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-29 corrections across {len(changed)} Acts chapter files')
