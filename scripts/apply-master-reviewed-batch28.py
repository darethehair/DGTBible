#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'acts'

EDITS=[
 (14,4,14,'and',['w15'],False,"Second connective renders δέ in οἱ δέ ('and others')"),
 (15,36,28,'see',[],True,"'to see' is natural English before πῶς ἔχουσιν ('how they are'); no separate source token"),
 (17,34,5,'and',[],True,"English coordination between 'joined him' and 'believed' has no separate Greek conjunction"),
 (18,17,8,'and',[],True,"English coordination before 'began beating' has no separate Greek conjunction"),
 (18,18,25,'he',['w21'],False,"Subject of the Cenchreae hair-cut clause is carried by κειράμενος"),
 (18,26,0,'And',['w2'],False,"Opening connective renders τε, not the later καί joining Priscilla and Aquila"),
 (18,27,21,'When',['w17'],False,"Second 'When' introduces παραγενόμενος ('having arrived'), not the opening βουλομένου"),
 (18,3,2,'he',['w5'],False,"Subject of 'he was of the same trade' is carried by εἶναι ('being')"),
 (18,3,3,'was',['w5'],False,"Copular 'was' renders εἶναι ('being'), not ἔμενεν ('stayed')"),
 (18,9,0,'And',['w2'],False,"Opening connective renders δέ, not the later καί"),
 (19,10,0,'And',['w2'],False,"Opening connective renders δέ, not the later καί between Jews and Greeks"),
 (19,16,5,'the',['w10'],False,"Article before 'evil spirit' belongs to τὸ w10, not article before 'man'"),
 (19,16,14,'of',['w16'],False,"'all of them' is rendered by ἀμφοτέρων, not later ἐκ ('out of')"),
 (19,16,16,'and',[],True,"English coordination before 'prevailed' has no separate Greek καί"),
 (19,19,0,'And',['w2'],False,"Opening connective renders δέ, not later καί"),
 (19,19,13,'and',[],True,"English coordination between bringing books and burning them has no separate Greek καί"),
 (19,2,0,'And',['w2'],False,"Opening connective renders τε in εἶπέν τε, not later δέ"),
 (19,2,20,'have',['w21'],False,"Perfect auxiliary in 'we have not heard' belongs with ἠκούσαμεν"),
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
    x['reason']='Human-reviewed full-NT master pass batch 28: '+reason
    count+=1

for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-28 corrections across {len(changed)} Acts chapter files')
