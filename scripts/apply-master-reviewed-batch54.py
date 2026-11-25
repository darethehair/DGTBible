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
    x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 54: '+reason

edit(10,2,20,'continually.',['w22'],"Renders διὰ παντός idiomatically as 'continually'")
edit(10,26,9,'myself',['w10'],"Renders emphatic αὐτός")
edit(10,29,10,'So',['w7'],"Second discourse connective renders οὖν")
edit(10,3,3,'hour',['w7'],"Renders ὥραν")
edit(10,33,0,'So',['w2'],"Opening οὖν rendered as 'So'")
edit(13,8,3,'magician—for',['w6'],"Renders μάγος within punctuation-bound English token")
edit(14,4,15,'others',['w14'],"Second substantival οἱ in οἱ δὲ rendered as 'others'")
edit(16,12,9,'city',['w11'],"Renders πόλις; πρώτη supplies 'leading'")
edit(16,26,23,'everyone’s',['w19'],"Renders πάντων in 'everyone’s chains'")
edit(16,36,19,'go',['w20'],"Renders πορεύεσθε, not earlier release verb")
edit(16,40,2,'coming',['w1'],"Renders ἐξελθόντες in 'after coming out'")
edit(16,9,11,'Macedonian',['w10'],"Renders Μακεδών")
edit(17,13,18,'also,',['w10'],"Renders καί modifying 'in Berea also'; κἀκεῖ supplies later 'there too'")
edit(17,21,19,'something',['w14','w17'],"Single English 'something' serves both coordinated Greek τι objects")
edit(17,28,10,'even',['w10'],"Renders καί adverbially as 'even'")
edit(17,31,0,'because',['w1'],"Renders καθότι contextually as causal 'because'")
edit(19,27,32,'even',['w25'],"Renders emphatic καί before καθαιρεῖσθαι")
edit(19,33,5,'instructed',['w5'],"Contextual rendering of συνεβίβασαν")
edit(19,34,10,'voice',['w6'],"Renders φωνή")
edit(19,35,11,'Ephesus,',['w9'],"Vocative Ἐφέσιοι rendered idiomatically as 'of Ephesus'")

for p,d in files.values():
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=ROOT/'data'/'master-review-allowlist.json'
a=json.loads(allow_path.read_text(encoding='utf8'))
items=set(a.get('interactions',[]))
items.add('unused-greek-with-rendering|acts|15|17|w20')
items.add('unused-greek-with-rendering|acts|17|27|w6')
a['interactions']=sorted(items)
allow_path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Applied 20 reviewed unused-Greek repairs and reviewed 2 legitimate omissions in Acts 10-19')
