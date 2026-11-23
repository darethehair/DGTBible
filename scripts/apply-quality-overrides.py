import json,sys
from pathlib import Path

p=Path('data/alignment-quality-overrides.json')
if not p.exists():
 print('No alignment quality overrides present.')
 raise SystemExit(0)
over=json.loads(p.read_text(encoding='utf8'))
changed=0
for key,val in over.items():
 slug,ch,vnum,idx=key.rsplit('.',3)
 path=Path('data')/slug/f'{int(ch):02}.json'
 if not path.exists():
  continue
 d=json.loads(path.read_text(encoding='utf8'))
 verse=next((v for v in d.get('verses',[]) if int(v.get('v'))==int(vnum)),None)
 if verse is None: raise SystemExit(f'Override verse missing: {key}')
 arr=verse.get('alignment',{}).get('dgt',[])
 i=int(idx)
 if i>=len(arr): raise SystemExit(f'Override token index missing: {key}')
 x=arr[i]
 if x.get('text')!=val['text']:
  raise SystemExit(f'Override token text changed: {key}: {x.get("text")!r} != {val["text"]!r}')
 if x.get('ids')!=val['ids'] or x.get('confidence')!='quality-scan':
  x['ids']=val['ids'];x['confidence']='quality-scan';x.pop('reason',None);changed+=1
  path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {changed} reviewed quality-scan token overrides.')
