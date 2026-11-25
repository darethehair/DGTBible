#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'acts'

EDITS=[
 (25,4,11,'that',[],True,"Second clause complementizer is supplied English; ἀπεκρίθη w5 supplies the first 'answered that'"),
 (25,6,11,'he',['w11'],False,"Subject of 'he went down' is carried by καταβάς"),
 (25,6,21,'he',['w16'],False,"Subject of 'he sat' is carried by καθίσας"),
 (25,24,24,'to',['w23'],False,"'appealed to me' belongs with μοι w23, not the later infinitive ζῆν"),
 (26,23,4,'to',['w2'],False,"Infinitival sense in 'was to suffer' belongs with παθητός"),
 (26,23,14,'was',['w11'],False,"'was/about to proclaim' is carried by μέλλει"),
 (26,29,5,'to',['w7'],False,"Dative 'to God' belongs with τῷ w7, not γενέσθαι"),
 (27,14,8,'the',['w10'],False,"Article in 'called the Northeaster' belongs to ὁ w10"),
 (27,14,13,'the',[],True,"Article in 'from the island' is supplied by English for pronominal αὐτῆς"),
 (27,33,12,'take',['w11'],False,"First 'take food' renders μεταλαβεῖν, not later προσλαβόμενοι"),
 (27,33,21,'have',['w19'],False,"Perfect auxiliary in 'you have continued' belongs to διατελεῖτε"),
 (27,33,25,'food,',['w18'],False,"Second 'without food' renders ἄσιτοι, not the earlier τροφῆς"),
 (27,4,12,'of',[],True,"'shelter of Cyprus' is idiomatic English; διὰ w6 belongs to 'because'"),
 (27,9,9,'was',['w6'],False,"Copula in 'voyage was dangerous' renders ὄντος"),
 (27,9,16,'had',['w17'],False,"Perfect auxiliary in 'the Fast had passed' belongs to παρεληλυθέναι"),
 (27,9,18,'passed,',['w17'],False,"Second 'passed' renders παρεληλυθέναι, not earlier διαγενομένου"),
 (28,14,4,'and',[],True,"Coordination between finding brothers and being urged is supplied English"),
 (28,3,4,'a',['w6'],False,"Article-like 'a' in 'a bundle' belongs with τι ('some')"),
 (28,3,19,'of',['w14'],False,"'because of the heat' renders ἀπό w14 in context"),
 (28,3,22,'and',[],True,"Coordination between viper coming out and fastening is supplied English"),
 (28,30,0,'And',['w2'],False,"Opening connective renders δέ, not later καί"),
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
    x['reason']='Human-reviewed full-NT master pass batch 33: '+reason
    count+=1

for path,d in changed.items():
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-33 corrections across {len(changed)} Acts chapter files')
