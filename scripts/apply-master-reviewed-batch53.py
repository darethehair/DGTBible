#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(ch):
    p=ROOT/'data'/'acts'/f'{ch:02}.json'
    return p,json.loads(p.read_text(encoding='utf8'))

def edit(d,vn,idx,expected,ids,supplied,reason):
    verse=next(v for v in d['verses'] if v['v']==vn)
    x=verse['alignment']['dgt'][idx]
    if x.get('text')!=expected:
        raise SystemExit(f"Acts {d['chapter']}:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids)
    if supplied:
        x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 53: '+reason

changed={}
for ch in [3,5,7,8]:
    p,d=load(ch); changed[ch]=(p,d)

# Acts 3
d=changed[3][1]
edit(d,12,3,'this,',[],True,"Object of 'saw' is supplied from the preceding healing; τούτῳ belongs to the later 'at this'")
# Acts 3:5 ἐπεῖχεν legitimately renders discontinuous 'he gave ... attention'.

# Acts 5
d=changed[5][1]
edit(d,17,18,'and',[],True,"English coordination before 'they were filled' is supplied; καί w5 joins the high priest with those around him")
edit(d,19,2,'the',[],True,"Greek διὰ νυκτὸς has no article; English 'the night' article is supplied")
edit(d,19,7,'the',[],True,"Greek 'angel of Lord' has no article before κυρίου; English article is supplied")
edit(d,19,8,'Lord',['w3'],False,"Renders κυρίου")
edit(d,20,8,'the',['w8'],False,"Second article belongs to τῷ before λαῷ, not the temple article")
edit(d,25,3,'and',[],True,"English coordination between 'came' and 'reported' is supplied; καί w21 belongs to standing-and-teaching")
# Acts 5:33 διεπρίοντο legitimately renders discontinuous 'they were cut ... heart'.

# Acts 7
d=changed[7][1]
edit(d,25,19,'understand.',['w19'],False,"Second 'understand' renders συνῆκαν, not earlier συνιέναι")
edit(d,27,3,'who',['w3'],False,"Relative English support for participle ἀδικῶν, not later interrogative Τίς")
edit(d,27,4,'was',['w3'],False,"Auxiliary with ἀδικῶν")
edit(d,27,5,'wronging',['w3'],False,"Renders ἀδικῶν")
edit(d,27,6,'his',[],True,"English possessive in 'his neighbor' is supplied")
edit(d,27,7,'neighbor',['w5'],False,"Renders πλησίον")
edit(d,31,0,'When',['w4'],False,"First temporal 'When Moses saw it' belongs to participle ἰδών, not later προσερχομένου")
edit(d,46,14,'God',['s12'],False,"Second God in 'God of Jacob' belongs to the synthetic/dative source for θεῷ, not earlier θεοῦ")
edit(d,59,5,'as',['w5'],False,"Temporal/subordinate English 'as he called out' belongs to participle ἐπικαλούμενον, not opening καί")
# Acts 7:50 ἐποίησεν legitimately renders discontinuous 'Did ... make'.

# Acts 8
d=changed[8][1]
edit(d,4,8,'the',[],True,"Article in 'announcing the good news' is supplied; τὸν w7 belongs to 'the word'")

for ch,(p,d) in changed.items():
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=ROOT/'data'/'master-review-allowlist.json'
a=json.loads(allow_path.read_text(encoding='utf8'))
items=set(a.get('interactions',[]))
for key in [
  'precise-scattered|acts|2|23|w1',
  'precise-scattered|acts|2|30|w6',
  'precise-scattered|acts|3|5|w3',
  'precise-scattered|acts|5|33|w4',
  'precise-scattered|acts|7|50|w5',
  'precise-fanout|acts|8|25|w19',
  'precise-fanout|acts|8|40|w8',
]:
    items.add(key)
a['interactions']=sorted(items)
allow_path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Applied batch-53 residual Acts interaction fixes and reviewed 7 legitimate interactions')
