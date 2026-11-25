#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def apply(path, edits, label):
    d=json.loads(path.read_text(encoding='utf8'))
    count=0
    for vn,idx,expected,ids,supplied,reason in edits:
        verse=next(v for v in d['verses'] if v['v']==vn)
        x=verse['alignment']['dgt'][idx]
        if x.get('text') != expected:
            raise SystemExit(f"{label} {vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
        x['ids']=list(ids); x['phraseIds']=list(ids)
        if supplied:
            x['supplied']=True; x['confidence']='reviewed-master-supplied'
        else:
            x.pop('supplied',None); x['confidence']='reviewed-master-precise'
        x['reason']='Human-reviewed full-NT master pass batch 44: '+reason
        count+=1
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return count

ed19=[
 (11,6,'works',['w1'],False,"'powerful works/miracles' renders Δυνάμεις, not ἐποίει"),
 (11,8,'the',['w10'],False,"Article with hands without unrelated phrase span"),
 (25,0,'He',['w2'],False,"Subject of 'He gathered' is carried by participle συναθροίσας, not later εἶπεν"),
 (25,1,'gathered',['w2'],False,"Renders συναθροίσας"),
 (25,2,'these',['w1'],False,"Renders relative οὓς as 'these'"),
 (25,4,'along',[],True,"English connective in 'along with' is supplied"),
 (25,6,'the',['w4'],False,"Article with workers without unrelated phrase span"),
 (25,7,'workers',['w8'],False,"Renders ἐργάτας"),
 (25,9,'related',['w6','w7'],False,"Contextual rendering of τὰ τοιαῦτα ('such/related')"),
 (25,10,'trades,',['w5','w8'],False,"Contextual rendering of περὶ ... ἐργάτας ('workers in related trades')"),
 (25,20,'we',['w19'],False,"Dative ἡμῖν rendered idiomatically as first-person possession without unrelated span"),
 (25,22,'our',['w19'],False,"Possessive rendering of ἡμῖν without unrelated span"),
 (25,23,'prosperity.',['w18'],False,"Renders εὐπορία"),
]
ed18=[
 (4,8,'and',[],True,"English clause coordination before 'was trying to persuade' is supplied; τε supplies 'both'"),
 (4,9,'was',['w9'],False,"Auxiliary with ἔπειθεν without unrelated phrase span"),
 (9,1,'the',['w3'],False,"Article with Lord without unrelated phrase span"),
 (9,4,'to',['w9'],False,"Dative/article before Paul, not Παύλῳ itself"),
 (9,10,'the',['w5'],False,"Article in 'in the night' belongs with ἐν phrase, not τῷ before Paul"),
 (9,13,'not',['w11'],False,"Renders first μή without unrelated phrase span"),
 (9,14,'be',['w12'],False,"English support in 'be afraid' belongs with φοβοῦ, not σιωπήσῃς"),
 (9,17,'keep',['w14'],False,"Aspectual rendering of λάλλει ('keep speaking')"),
 (9,20,'do',['w17'],False,"English auxiliary in 'do not be silent' belongs with σιωπήσῃς"),
 (9,21,'not',['w16'],False,"Renders second μή without unrelated phrase span"),
 (17,1,'they',['w1'],False,"Subject of 'they seized' carried by participle ἐπιλαβόμενοι, not later ἔτυπτον"),
 (17,5,'the',['w7'],False,"Article with synagogue ruler, not noun ἀρχισυνάγωγον"),
 (17,13,'the',['w11'],False,"Article with judgment seat without unrelated phrase span"),
 (19,6,'he',['w6'],False,"Subject of 'he left them' carried by κατέλιπεν, not later διελέξατο"),
 (19,11,'he',['w8'],False,"Subject/emphasis of second clause belongs to αὐτὸς without unrelated phrase span"),
 (19,14,'the',['w12'],False,"Article with synagogue without unrelated phrase span"),
 (19,19,'the',['w15'],False,"Article/dative with Jews without unrelated phrase span"),
]
n=apply(ROOT/'data'/'acts'/'19.json',ed19,'Acts 19:')
n+=apply(ROOT/'data'/'acts'/'18.json',ed18,'Acts 18:')

allow_path=ROOT/'data'/'master-review-allowlist.json'
a=json.loads(allow_path.read_text(encoding='utf8'))
items=set(a.get('interactions',[]))
for key in [
 'precise-scattered|acts|18|16|w2',
 'precise-scattered|acts|18|17|w9',
]:
    items.add(key)
a['interactions']=sorted(items)
allow_path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {n} reviewed batch-44 corrections in Acts 18-19 and reviewed 2 legitimate scattered renderings')
