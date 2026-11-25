#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def edit(path, vn, idx, expected, ids, supplied, reason):
    d=json.loads(path.read_text(encoding='utf8'))
    verse=next(v for v in d['verses'] if v['v']==vn)
    x=verse['alignment']['dgt'][idx]
    if x.get('text') != expected:
        raise SystemExit(f"{path.name} {vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids)
    if supplied:
        x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 45: '+reason
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

# Acts 10:43: English complementizer "that" is supplied; ἄφεσιν belongs to forgiveness.
edit(ROOT/'data'/'acts'/'10.json',43,8,'that',[],True,"English complementizer after 'bear witness' is supplied; ἄφεσιν renders 'forgiveness'")

# Acts 17:4: "of" belongs to the genitive Greek phrase for devout Greeks, not γυναικῶν.
edit(ROOT/'data'/'acts'/'17.json',4,16,'of',['w13'],False,"Genitive article τῶν introduces 'of devout Greeks'; γυναικῶν belongs only to 'women'")
edit(ROOT/'data'/'acts'/'17.json',4,17,'devout',['w15'],False,"Renders σεβομένων")

# Acts 21:6: first connective belongs to καί before 'we went aboard'; δὲ belongs to 'and they returned'.
edit(ROOT/'data'/'acts'/'21.json',6,6,'Then',['w3'],False,"Connective before 'we went aboard' renders καί w3, not later δὲ w9")

# Acts 23:12: first 'they' belongs to the oath/eating clause, not the later kill verb.
edit(ROOT/'data'/'acts'/'23.json',12,16,'they',['w10'],False,"Subject of the reported oath is carried by λέγοντες/context, leaving ἀποκτείνωσιν for the later 'they had killed'")

allow_path=ROOT/'data'/'master-review-allowlist.json'
a=json.loads(allow_path.read_text(encoding='utf8'))
items=set(a.get('interactions',[]))
for key in [
  'precise-scattered|acts|20|12|w1',
  'precise-scattered|acts|20|25|w7',
  'precise-scattered|acts|21|14|w11',
  'precise-fanout|acts|22|11|w11',
]:
    items.add(key)
a['interactions']=sorted(items)
allow_path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Applied reviewed residual fixes in Acts 10, 17, 21, 23 and reviewed 4 legitimate interactions')
