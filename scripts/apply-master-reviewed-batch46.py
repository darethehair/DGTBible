#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data'/'acts'/'09.json'
d=json.loads(path.read_text(encoding='utf8'))

EDITS=[
 (2,0,'and',[],True,"Opening English continuation is supplied; this verse begins with ᾐτήσατο, not καί"),
 (2,5,'to',['w7'],False,"Renders πρός without unrelated phrase span"),
 (2,13,'he',['w13'],False,"Subject carried by εὕρῃ without unrelated phrase span"),
 (2,16,'who',['w16'],False,"Relative English support for ὄντας ('who belonged/being')"),
 (2,17,'belonged',['w16'],False,"Contextual rendering of ὄντας in 'belonged to the Way'"),
 (2,19,'the',['w14'],False,"Genitive article with Way without unrelated phrase span"),
 (2,25,'he',['w22'],False,"Subject of ἀγάγῃ without unrelated phrase span"),
 (2,30,'to',['w23'],False,"Renders εἰς without unrelated phrase span"),

 (12,0,'and',['w1'],False,"Renders καί without unrelated phrase span"),
 (12,1,'he',['w2'],False,"Subject of εἶδεν without unrelated phrase span"),
 (12,3,'seen',['w2'],False,"Renders εἶδεν without unrelated phrase span"),
 (12,5,'a',['w3'],False,"Article supplied within 'a man', tied to ἄνδρα rather than vision"),
 (12,7,'a',['w3'],False,"Second English article before 'man' belongs to ἄνδρα"),
 (12,12,'in',['w8'],False,"Part of contextual rendering εἰσελθόντα ('coming in'), not ἐν w4"),
 (12,13,'and',['w9'],False,"Renders καί without unrelated phrase span"),
 (12,20,'he',['w15'],False,"Subject of ἀναβλέψῃ without unrelated phrase span"),

 (18,0,'And',['w1'],False,"Renders opening καί without unrelated phrase span"),
 (18,9,'and',['w11'],False,"Connective with regained sight renders τε, leaving καί w13 for the next clause"),
 (18,15,'got',['w14'],False,"Contextual rendering of ἀναστὰς without unrelated phrase span"),
 (18,17,'and',['w13'],False,"Renders καί joining rising and baptism without unrelated phrase span"),

 (19,7,'And',['w6'],False,"Second-clause connective renders δὲ, not opening καί w1"),

 (24,1,'their',['w7'],False,"Possessive 'their plot' renders αὐτῶν, not ἐγνώσθη"),
 (24,7,'And',['w9'],False,"Second-clause connective renders δὲ, not τε w14"),
 (24,8,'they',['w8'],False,"Subject of παρετηροῦντο without unrelated phrase span"),
 (24,11,'the',['w11'],False,"Article with gates without unrelated phrase span"),
 (24,13,'both',['w10'],False,"Correlative English 'both' is supported by καὶ/τε sequence; attach to first connective"),
 (24,19,'they',['w19'],False,"Subject of ἀνέλωσιν without unrelated phrase span"),

 (25,1,'his',['w5'],False,"Possessive 'his disciples' renders αὐτοῦ, not λαβόντες"),
 (25,4,'him',['w11'],False,"Object 'him' is αὐτόν, not possessive αὐτοῦ"),
 (25,8,'lowered',['w10'],False,"First 'lowered him' renders καθῆκαν"),
 (25,11,'the',['w8'],False,"Article with wall without unrelated phrase span"),
 (25,13,'letting',['w12'],False,"Renders χαλάσαντες"),
 (25,14,'him',['w12'],False,"Object included in contextual rendering of χαλάσαντες"),
 (25,15,'down',['w12'],False,"Part of 'letting him down' rendering of χαλάσαντες"),

 (32,7,'the',[],True,"English article in 'all the regions' is supplied; τοὺς w10 belongs to holy ones"),
 (32,11,'came',['w7'],False,"Part of κατελθεῖν ('came down'), not Ἐγένετο"),
 (32,13,'to',['w9'],False,"Renders πρός without unrelated phrase span"),

 (41,0,'And',['w2'],False,"Opening connective renders δὲ, leaving καί w11 for saints and widows"),
 (41,1,'giving',['w1'],False,"Renders δοὺς"),
 (41,2,'her',['w3'],False,"Renders αὐτῇ without unrelated phrase span"),
 (41,5,'he',['w5'],False,"Subject of ἀνέστησεν without unrelated phrase span"),
 (41,7,'her',['w6'],False,"Renders αὐτήν without unrelated phrase span"),
 (41,9,'Then',['w8'],False,"Renders second δὲ without unrelated phrase span"),
 (41,11,'the',['w9'],False,"Article with holy ones without unrelated phrase span"),
 (41,13,'ones',['w10'],False,"Completes rendering of ἁγίους"),
 (41,15,'the',['w12'],False,"Article with widows without unrelated phrase span"),
 (41,17,'he',['w14'],False,"Subject of παρέστησεν without unrelated phrase span"),
 (41,19,'her',['w15'],False,"Renders αὐτὴν without unrelated phrase span"),
 (41,20,'alive.',['w16'],False,"Renders ζῶσαν"),

 (42,0,'And',['w2'],False,"Opening connective renders δὲ, leaving καί w8 for second clause"),
 (42,10,'in',['w11'],False,"Renders ἐπί idiomatically as 'in'"),
 (42,11,'the',['w12'],False,"Article with Lord without unrelated phrase span"),
]

count=0
for vn,idx,expected,ids,supplied,reason in EDITS:
    verse=next(v for v in d['verses'] if v['v']==vn)
    x=verse['alignment']['dgt'][idx]
    if x.get('text') != expected:
        raise SystemExit(f"Acts 9:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids)
    if supplied:
        x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 46: '+reason
    count+=1

path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-46 corrections in Acts 9')
