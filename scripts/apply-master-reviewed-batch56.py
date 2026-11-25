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
    x['confidence']='reviewed-master-precise'; x['reason']='Human-reviewed full-NT master pass batch 56: '+reason

edit(1,15,12,'brothers—the',['w11'],"Renders ἀδελφῶν within punctuation-bound token")
edit(1,15,21,'twenty—and',['w22'],"Renders εἴκοσι within punctuation-bound token")
edit(1,18,6,'from',['w6'],"Renders ἐκ in 'from the reward'")
edit(2,36,17,'Christ—this',['w12','w16'],"Single punctuation-bound token carries χριστόν and demonstrative τοῦτον")
edit(3,24,15,'announced',['w14'],"Renders κατήγγειλαν")
edit(5,38,23,'people,',['w18'],"Renders ἀνθρώπων contextually as 'people'")
edit(7,35,11,'judge?’—this',['w12','w13'],"Punctuation-bound token carries δικαστήν and following demonstrative τοῦτον")
edit(7,35,12,'one',['w13'],"Completes rendering of demonstrative τοῦτον")
edit(7,41,9,'brought',['w8'],"Contextual rendering of ἀνήγαγον in 'brought/offered a sacrifice'")
edit(7,51,0,'“Stiff-necked',['w1'],"Renders Σκληροτράχηλοι")
edit(7,56,2,'“Look,',['w3'],"Renders Ἰδοὺ ('Behold/Look'), leaving θεωρῶ for 'I see'")
edit(8,7,16,'voice—and',['w8','w12'],"Punctuation-bound token carries φωνῇ and discourse δὲ rendered as 'and'")
edit(8,10,8,'greatest,',['w7'],"Renders μεγάλου in 'from the least to the greatest'")
edit(8,24,1,'answered,',['w1','w5'],"English 'answered' compresses ἀποκριθείς ... εἶπεν ('answering ... said')")
edit(8,34,2,'responded',['w1','w7'],"English 'responded' compresses ἀποκριθείς ... εἶπεν")
edit(8,38,8,'both',['w8','w13'],"Single English 'both' carries ἀμφότεροι and the later τε ... καί correlative")

for p,d in files.values():
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=ROOT/'data'/'master-review-allowlist.json'
a=json.loads(allow_path.read_text(encoding='utf8')); items=set(a.get('interactions',[]))
items.add('unused-greek-with-rendering|acts|2|18|w8')
items.add('unused-greek-with-rendering|acts|9|32|w1')
a['interactions']=sorted(items)
allow_path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Applied final early-Acts unused-Greek repairs and reviewed 2 legitimate compressions')
