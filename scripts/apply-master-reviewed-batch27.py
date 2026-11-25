#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'acts'

# Human-reviewed corrections from the full-NT precise-scattered queue.
# Each edit is keyed by chapter, verse, DGT token index, expected token text.
# ids=[] with supplied=True means natural English with no distinct Greek token.
EDITS=[
 (16,13,28,'the',['w19'],False,"Article in 'the women' belongs to ταῖς / 'to those'"),
 (16,37,32,'them',['w25'],False,"Subject of 'Let them come' is carried by plural ἐλθόντες"),
 (16,37,35,'and',[],True,"English coordination before 'bring us out' has no separate Greek καί"),
 (16,38,6,'the',['w3'],False,"Article in 'to the magistrates' belongs to τοῖς"),
 (16,40,0,'And',['w2'],False,"Opening connective renders δέ ('then/and'), not later καί"),
 (17,4,19,'and',['w20'],False,"Coordination before women renders τε, not earlier καί"),
 (17,8,0,'And',['w2'],False,"Opening connective renders δέ, not later καί"),
 (17,11,27,'were',['w22'],False,"Second 'were' renders ἔχοι ('would be'), not earlier ἦσαν"),
 (17,15,4,'him',['w5'],False,"First 'him' resumes Paul (Παῦλον), not later αὐτόν"),
 (17,16,17,'he',['w15'],False,"Subject of 'he observed' is carried by θεωροῦντος"),
 (17,16,22,'of',[],True,"'full of idols' is idiomatic English for κατείδωλον; no separate Greek 'of'"),
 (17,23,2,'I',['w1'],False,"Subject of 'I was passing through' is carried by διερχόμενος"),
 (17,26,0,'And',['w2'],False,"Opening connective renders τε, not later καί"),
 (17,26,28,'dwelling,',['w22'],False,"Nominal 'dwelling' renders κατοικίας ('habitation')"),
 (18,1,3,'he',['w4'],False,"Subject of 'he departed' is carried by χωρισθείς"),
 (18,1,7,'and',[],True,"English coordination before 'came' has no separate Greek conjunction"),
 (18,10,15,'I',['w16'],False,"Idiomatic 'I have' renders μοι ('to me') with ἐστί"),
 (18,14,3,'was',['w1'],False,"'Paul was about to' is carried by μέλλοντος, not later ἦν"),
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
    x['reason']='Human-reviewed full-NT master pass batch 27: '+reason
    count+=1

for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-27 corrections across {len(changed)} Acts chapter files')
