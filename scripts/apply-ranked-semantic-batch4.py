import json
from pathlib import Path

# Fourth curated semantic batch: manually reviewed orphan-English -> Greek source links.
FIXES=[
 ('romans',5,3,12,'affliction',['w13']),
 ('romans',10,14,32,'proclaiming?',['w18']),
 ('romans',11,28,23,'fathers,',['w15']),
 ('romans',11,33,0,'Oh,',['w1']),
 ('romans',13,7,0,'Give',['w1']),
 ('romans',13,7,16,'fear',['w18']),
 ('romans',14,1,14,'opinions.',['w10']),
 ('romans',16,18,25,'unsuspecting.',['w25']),
 ('1corinthians',4,10,25,'dishonored.',['w19']),
 ('john',20,1,24,'taken',['w21']),
 ('john',20,1,25,'away',['w21']),
 ('john',16,7,23,'Advocate',['w18']),
 ('romans',1,21,23,'undiscerning',['w20']),
 ('romans',12,16,8,'lofty',['w8']),
 ('james',4,14,6,'tomorrow',['w6']),
 ('john',13,27,3,'piece',['w4']),
 ('hebrews',10,25,1,'abandoning',['w2']),
 ('2peter',2,16,9,'speechless',['w7']),
 ('1john',3,5,6,'revealed',['w5']),
 ('1john',4,12,22,'completion',['w19']),
 ('romans',13,1,22,'appointed',['w21']),
 ('romans',16,11,3,'relative.',['w4']),
 ('hebrews',2,2,8,'firm,',['w9']),
 ('james',1,11,8,'dried',['w9']),
 ('3john',1,7,9,'receiving',['w7']),
 ('2peter',1,8,7,'increasing,',['w6']),
 ('1peter',2,19,12,'sorrows',['w10']),
 ('hebrews',9,23,6,'copies',['w5']),
 ('john',19,17,1,'carrying',['w2']),
 ('james',1,13,15,'untemptable',['w12']),
 ('john',19,38,13,'secretly',['w16']),
 ('john',16,21,7,'sorrow',['w5']),
 ('hebrews',11,37,22,'afflicted,',['w15']),
 ('romans',9,3,21,'relatives',['w15']),
 ('1peter',3,20,1,'formerly',['w2']),
 ('romans',14,14,20,'considers',['w15']),
 ('hebrews',12,17,8,'wanted',['w6']),
 ('james',3,7,7,'reptile',['w8']),
]
op=Path('data/alignment-quality-overrides.json')
over=json.loads(op.read_text(encoding='utf8'))
changed=0
for slug,ch,vnum,idx,expected,ids in FIXES:
 path=Path('data')/slug/f'{ch:02}.json'
 d=json.loads(path.read_text(encoding='utf8'))
 verse=next(v for v in d['verses'] if int(v['v'])==vnum)
 arr=verse['alignment']['dgt']
 x=arr[idx]
 if x.get('text')!=expected:
  raise SystemExit(f'token mismatch {slug} {ch}:{vnum} index {idx}: {x.get("text")!r} != {expected!r}')
 valid={i for g in verse['alignment']['greek'] for i in g.get('ids',[])}
 if any(i not in valid for i in ids):
  raise SystemExit(f'bad source id {slug} {ch}:{vnum} {ids}')
 if x.get('ids')!=ids or x.get('confidence')!='quality-scan':
  x['ids']=ids; x['confidence']='quality-scan'; x.pop('reason',None); changed+=1
 key=f'{slug}.{ch}.{vnum}.{idx}'
 over[key]={'text':expected,'ids':ids}
 path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
op.write_text(json.dumps(over,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {changed} reviewed semantic fixes; persisted {len(FIXES)} overrides.')
