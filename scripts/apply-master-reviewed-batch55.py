#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
files={}
def get(ch):
    if ch not in files:
        p=ROOT/'data'/'acts'/f'{ch:02}.json'
        files[ch]=(p,json.loads(p.read_text(encoding='utf8')))
    return files[ch][1]
def edit(ch,vn,idx,expected,ids,reason):
    d=get(ch); verse=next(v for v in d['verses'] if v['v']==vn); x=verse['alignment']['dgt'][idx]
    if x.get('text')!=expected:
        raise SystemExit(f"Acts {ch}:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids); x.pop('supplied',None)
    x['confidence']='reviewed-master-precise'; x['reason']='Human-reviewed full-NT master pass batch 55: '+reason

edit(20,13,24,'himself',['w21'],"Renders emphatic αὐτός, not earlier διατεταγμένος")
edit(21,26,29,'offering',['w32'],"Renders προσφορά; προσηνέχθη supplies 'was presented'")
edit(22,5,1,'even',['w2'],"Renders first καί adverbially as 'even'")
edit(24,15,5,'these',['w9'],"Renders demonstrative οὗτοι; αὐτοὶ supplies 'themselves'")
edit(24,25,7,'self-control',['w7'],"Renders ἐγκρατείας")
edit(25,2,6,'leading',['w8'],"Renders πρῶτοι as 'leading'")
edit(25,2,7,'men',['w8'],"Nominal completion of substantival πρῶτοι")
edit(25,20,3,'about',['w6'],"Renders first περὶ in 'about the investigation'")
edit(26,22,24,'and',['w22','w28'],"English 'and' carries Greek correlative τε ... καί joining prophets and Moses")
edit(26,9,1,'myself',['w5'],"Renders reflexive ἐμαυτῷ; Ἐγώ remains English 'I'")
edit(27,27,16,'around',['w11'],"Renders κατά in the phrase 'around midnight'")
edit(27,27,17,'midnight',['w12','w14'],"Compresses μέσον τῆς νυκτός ('middle of the night') as 'midnight'")
edit(27,27,18,'the',['w16'],"Article belongs with sailors, not μέσον")
edit(27,33,26,'taking',['w21'],"Renders participle προσλαβόμενοι")
edit(27,44,7,'others',['w8'],"Second relative οὓς in correlative 'some ... others'")
edit(28,25,10,'said',['w7'],"Renders participle εἰπόντος in temporal clause")

for p,d in files.values():
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=ROOT/'data'/'master-review-allowlist.json'
a=json.loads(allow_path.read_text(encoding='utf8')); items=set(a.get('interactions',[]))
for key in [
 'unused-greek-with-rendering|acts|22|5|w23',
 'unused-greek-with-rendering|acts|24|26|w16',
 'unused-greek-with-rendering|acts|26|29|w28',
]:
    items.add(key)
a['interactions']=sorted(items)
allow_path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Applied 16 reviewed unused-Greek repairs and reviewed 3 legitimate omissions in Acts 20-28')
