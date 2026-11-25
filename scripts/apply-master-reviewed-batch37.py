#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data'/'acts'/'26.json'
d=json.loads(path.read_text(encoding='utf8'))

EDITS=[
 (13,1,'midday,',['w1','w2'],False,"Renders ἡμέρας μέσης ('midday')"),
 (13,4,'along',['w3'],False,"Renders κατά in 'along the road'"),
 (13,5,'the',['w4'],False,"Article with ὁδόν without unrelated phrase span"),
 (13,13,'brighter',['w9','w11'],False,"Comparative rendering of ὑπὲρ τὴν λαμπρότητα ('brighter than')"),
 (13,15,'the',['w12'],False,"Article with ἡλίου without unrelated phrase span"),
 (13,17,'shining',['w14'],False,"Renders περιλάμψαν, not φῶς"),
 (13,19,'me',['w15'],False,"Renders με without unrelated phrase span"),
 (13,22,'traveling',['w21'],False,"Renders πορευομένους"),
 (13,24,'me.',['w20'],False,"Renders ἐμοί without unrelated phrase span"),
 (23,1,'the',['w3'],False,"Article with Christ without unrelated phrase span"),
 (23,3,'was',['w2'],False,"English copular support for παθητός ('was to suffer')"),
 (23,6,'and,',[],True,"English coordination between the two εἰ clauses is supplied"),
 (23,7,'being',[],True,"English participial glue for the second clause"),
 (23,12,'the',['w9'],False,"Article in 'the dead' belongs with νεκρῶν phrase"),
 (23,15,'to',['w12'],False,"Infinitival marker with καταγγέλλειν"),
 (23,19,'to',['w14'],False,"Part of τε construction 'both to'"),
 (23,20,'the',['w13'],False,"Article with λαῷ"),
 (23,23,'to',['w17'],False,"Dative/article before Gentiles"),
 (23,24,'the',['w17'],False,"Article before Gentiles"),
 (25,0,'But',['w2'],False,"Renders δέ without unrelated phrase span"),
 (25,3,'“I',['w5'],False,"Subject carried by μαίνομαι without unrelated phrase span"),
 (25,13,'but',['w9'],False,"Renders ἀλλά without unrelated phrase span"),
]

count=0
for vn,idx,expected,ids,supplied,reason in EDITS:
    verse=next(v for v in d['verses'] if v['v']==vn)
    x=verse['alignment']['dgt'][idx]
    if x.get('text') != expected:
        raise SystemExit(f"Acts 26:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids)
    if supplied:
        x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 37: '+reason
    count+=1

path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-37 corrections in Acts 26')
