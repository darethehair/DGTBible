#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data'/'acts'/'28.json'
d=json.loads(path.read_text(encoding='utf8'))
verse=next(v for v in d['verses'] if v['v']==2)
D=verse['alignment']['dgt']

EDITS=[
 (0,'The',['w1'],False,"Article for the people"),
 (1,'local',['w3'],False,"Adjectival rendering within βάρβαροι ('local people')"),
 (2,'people',['w3'],False,"Nominal rendering of βάρβαροι ('people/natives')"),
 (3,'showed',['w4'],False,"Renders παρεῖχον"),
 (4,'us',['w9'],False,"Renders dative ἡμῖν"),
 (5,'extraordinary',['w5','w7'],False,"Renders the idiom οὐ ... τυχοῦσαν ('not ordinary')"),
 (6,'kindness,',['w8'],False,"Renders φιλανθρωπίαν"),
 (7,'for',['w11'],False,"Renders γὰρ"),
 (8,'because',['w16'],False,"First 'because of' renders first διά"),
 (10,'the',['w17'],False,"Article with first rain phrase"),
 (11,'rain',['w18'],False,"Renders ὑετόν"),
 (12,'that',['w19'],False,"Relative/article function of τόν introducing ἐφεστῶτα"),
 (13,'had',['w20'],False,"Perfect auxiliary carried by ἐφεστῶτα"),
 (14,'begun',['w20'],False,"Renders perfect participle ἐφεστῶτα in context"),
 (15,'and',['w21'],False,"Renders καί between the two causal phrases"),
 (16,'because',['w22'],False,"Second 'because of' renders second διά"),
 (17,'of',['w22'],False,"Second 'because of' renders second διά"),
 (18,'the',['w23'],False,"Article with cold"),
 (19,'cold,',['w24'],False,"Renders ψῦχος"),
 (20,'they',['w10'],False,"Plural subject carried by participle ἅψαντες in reordered clause"),
 (21,'kindled',['w10'],False,"Renders ἅψαντες"),
 (22,'a',['w12'],False,"Article supplied within 'a fire' rendering"),
 (23,'fire',['w12'],False,"Renders πυράν"),
 (24,'and',[],True,"Coordination between kindling and welcoming is supplied English"),
 (25,'welcomed',['w13'],False,"Renders προσελάβοντο"),
 (26,'us',['w15'],False,"Renders ἡμᾶς"),
 (27,'all.',['w14'],False,"Renders πάντας"),
]

count=0
for idx,expected,ids,supplied,reason in EDITS:
    x=D[idx]
    if x.get('text') != expected:
        raise SystemExit(f"Acts 28:2 token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids)
    x['phraseIds']=list(ids)
    if supplied:
        x['supplied']=True
        x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None)
        x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 34: '+reason
    count += 1

path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed Acts 28:2 alignment corrections')
