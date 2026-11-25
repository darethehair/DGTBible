#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
files={}

def get(ch):
    if ch not in files:
        p=ROOT/'data'/'colossians'/f'{ch:02}.json'
        files[ch]=(p,json.loads(p.read_text(encoding='utf8')))
    return files[ch][1]

def edit(ch,vn,idx,expected,ids,supplied,reason):
    d=get(ch)
    verse=next(v for v in d['verses'] if v['v']==vn)
    x=verse['alignment']['dgt'][idx]
    if x.get('text')!=expected:
        raise SystemExit(f"Colossians {ch}:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids)
    x['phraseIds']=list(ids)
    if supplied:
        x['supplied']=True
        x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None)
        x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 57: '+reason

# Colossians 1
edit(1,2,1,'the',['w1'],False,"Opening dative article τοῖς supplies 'to the saints'; do not borrow πατρός")
edit(1,15,10,'of',['w9'],False,"Genitive 'of all creation' belongs with πάσης, not the earlier τοῦ before God")

# Colossians 2
edit(2,1,0,'For',['w2'],False,"Renders γάρ")
edit(2,1,11,'have',['w7'],False,"First 'I have' renders ἔχω; the later 'have seen' belongs to ἑόρακαν")
edit(2,13,10,'of',['w11'],False,"Genitive article before flesh")
edit(2,13,11,'your',['w13'],False,"Renders ὑμῶν")
edit(2,13,19,'graciously',['w18'],False,"Adverbial force of χαρισάμενος")
edit(2,13,20,'forgiving',['w18'],False,"Renders χαρισάμενος")
edit(2,13,23,'trespasses,',['w22'],False,"Second 'trespasses' renders the later παραπτώματα")
edit(2,14,1,'erased',['w1'],False,"Renders ἐξαλείψας")
edit(2,14,2,'the',['w2'],False,"Article with χειρόγραφον")
edit(2,14,3,'record',['w5'],False,"Renders χειρόγραφον")
edit(2,14,4,'of',[],True,"English genitive glue in 'record of debt'; do not link it to later ἐκ 'out of'")
edit(2,14,5,'debt',['w5'],False,"Contextual rendering of χειρόγραφον as a record of debt")
edit(2,14,12,'hostile',['w10'],False,"Renders ὑπεναντίον")
edit(2,14,22,'the',['w16'],False,"Article in 'out of the way' belongs to τοῦ")

# Colossians 3
edit(3,4,4,'is',['w4'],False,"Passive auxiliary with first φανερωθῇ")
edit(3,4,10,'be',['w13'],False,"Second passive auxiliary belongs to φανερωθήσεσθε")
edit(3,4,11,'revealed',['w13'],False,"Second 'revealed' renders φανερωθήσεσθε, not earlier φανερωθῇ")

# Colossians 4
edit(4,7,1,'the',['w8'],False,"Article with 'beloved brother'")
edit(4,7,11,'the',[],True,"Greek ἐν κυρίῳ has no article; English article is supplied")
edit(4,7,19,'the',['w1'],False,"Article within 'all the things' belongs with Τὰ")
edit(4,7,20,'things',['w1'],False,"Renders Τὰ as substantival 'things'")
edit(4,10,22,'receive',['w20'],False,"Imperative 'receive' renders δέξασθε, not earlier ἐλάβετε")
edit(4,11,15,'from',['w8'],False,"Renders ἐκ in 'from the circumcision'")
edit(4,11,16,'the',[],True,"Greek περιτομῆς has no article here; English article is supplied")
edit(4,11,19,'the',['w14'],False,"Article with kingdom")
edit(4,11,23,'and',[],True,"English coordination before final relative clause is supplied")
edit(4,11,26,'become',['w19'],False,"Renders ἐγενήθησάν")

for p,d in files.values():
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=ROOT/'data'/'master-review-allowlist.json'
a=json.loads(allow_path.read_text(encoding='utf8'))
items=set(a.get('interactions',[]))
for key in [
    'precise-scattered|colossians|2|1|w17',
    'precise-scattered|colossians|3|21|w10',
    'precise-scattered|colossians|4|4|w2',
    'precise-scattered|colossians|4|11|w1',
]:
    items.add(key)
a['interactions']=sorted(items)
allow_path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Applied reviewed Colossians master-alignment corrections and reviewed 4 legitimate split renderings')
