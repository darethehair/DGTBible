#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'acts'

EDITS=[
 (1,4,23,'he',[],True,"Editorial 'he said' in the English quotation is supplied; it is not the earlier παρήγγειλεν"),
 (1,4,27,'from',['w17'],False,"'from me' belongs with μου, not the earlier ἀπό before Jerusalem"),
 (19,4,14,'in',['w12'],False,"First 'in' in 'believe in the one' renders the first εἰς w12"),
 (19,5,1,'they',['w1'],False,"Subject of 'they heard' is carried by plural participle ἀκούσαντες"),
 (19,38,25,'against',['w19'],False,"Second 'against' is part of ἐγκαλείτωσαν ('bring charges/accuse'), not earlier πρός"),
 (20,17,3,'he',['w5'],False,"Subject of 'he sent' is carried by πέμψας ('having sent'), not later summoned verb"),
 (20,35,25,'that',['w18'],False,"Second quotation-introducing 'that/how' belongs to the second ὅτι w18"),
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
    x['reason']='Human-reviewed full-NT master pass batch 30: '+reason
    count+=1

for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-30 corrections across {len(changed)} Acts chapter files')
