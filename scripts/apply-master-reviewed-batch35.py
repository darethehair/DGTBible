#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data'/'acts'/'28.json'
d=json.loads(path.read_text(encoding='utf8'))

EDITS=[
 (5,1,'he',['w4'],False,"Subject of 'he shook off' is carried by participle ἀποτινάξας, not later ἔπαθεν"),
 (5,4,'the',['w5'],False,"Article with θηρίον; remove unrelated five-word phrase span"),
 (5,7,'the',['w8'],False,"Article with πῦρ; remove unrelated five-word phrase span"),
 (13,2,'we',['w3'],False,"Subject of first 'we came' is carried by κατηντήσαμεν"),
 (13,7,'to',['w4'],False,"First 'to' before Rhegium renders first εἰς, not the later εἰς before Puteoli"),
 (13,12,'day',['w9'],False,"Renders ἡμέραν without unrelated phrase span"),
 (13,18,'on',['w12'],False,"Part of 'on the second day' rendered by δευτεραῖοι"),
 (13,21,'day',['w12'],False,"Part of 'on the second day' rendered by δευτεραῖοι"),
 (22,2,'consider',['w1'],False,"Renders ἀξιοῦμεν ('consider/deem worthy'), not φρονεῖς"),
 (22,3,'it',['w1'],False,"Part of idiomatic rendering of ἀξιοῦμεν"),
 (22,4,'right',['w1'],False,"Part of idiomatic rendering of ἀξιοῦμεν ('deem it right')"),
 (22,5,'to',['w5'],False,"Infinitival marker with ἀκοῦσαι"),
 (22,19,'to',['w15'],False,"Dative 'to us' renders ἡμῖν without unrelated phrase span"),
 (22,23,'it',['w19'],False,"Subject supplied within passive rendering of ἀντιλέγεται"),
 (22,24,'is',['w19'],False,"Passive auxiliary within rendering of ἀντιλέγεται"),
]

count=0
for vn,idx,expected,ids,supplied,reason in EDITS:
    verse=next(v for v in d['verses'] if v['v']==vn)
    x=verse['alignment']['dgt'][idx]
    if x.get('text') != expected:
        raise SystemExit(f"Acts 28:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids)
    if supplied:
        x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 35: '+reason
    count+=1

path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-35 corrections in Acts 28')
