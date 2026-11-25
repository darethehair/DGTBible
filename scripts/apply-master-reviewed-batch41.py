#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data'/'acts'/'22.json'
d=json.loads(path.read_text(encoding='utf8'))

EDITS=[
 (2,1,'they',['w1'],False,"Subject of 'they heard' is carried by participle Ἀκούσαντες, not later παρέσχον"),
 (2,18,'he',['w13'],False,"Subject of 'he said' carried by φησίν without unrelated phrase span"),
 (10,1,'I',['w1'],False,"Subject of first 'I said' without unrelated phrase span"),
 (10,2,'said,',['w1'],False,"Renders εἶπον without unrelated phrase span"),
 (10,5,'I',['w4'],False,"Subject carried by ποιήσω without unrelated phrase span"),
 (10,6,'do,',['w4'],False,"Renders ποιήσω without unrelated phrase span"),
 (10,8,'And',['w7'],False,"Renders δὲ in second clause without unrelated phrase span"),
 (10,9,'the',['w6'],False,"Article with Lord without unrelated phrase span"),
 (10,11,'said',['w9'],False,"Renders εἶπεν without unrelated phrase span"),
 (10,12,'to',['w10'],False,"Renders πρός without unrelated phrase span"),
 (10,14,'‘Get',['w12'],False,"Imperatival rendering of Ἀναστὰς"),
 (10,26,'you',['w17'],False,"Renders σοι without unrelated phrase span"),
 (10,29,'the',[],True,"English article supplied in 'all the things'"),
 (10,36,'you',['w23'],False,"Renders second σοι without unrelated phrase span"),
 (10,37,'to',['w24'],False,"Infinitival marker with ποιῆσαι without unrelated phrase span"),
 (10,38,'do.’',['w24'],False,"Renders ποιῆσαι without unrelated phrase span"),
 (11,2,'I',['w4'],False,"Subject of ἐνέβλεπον without unrelated phrase span"),
 (11,7,'of',['w5'],False,"Part of 'because of' rendering without unrelated phrase span"),
 (11,9,'glory',['w7'],False,"Renders δόξης"),
 (11,10,'of',['w8'],False,"Genitive article relation without unrelated phrase span"),
 (11,13,'I',['w11'],False,"Subject of passive participle χειραγωγούμενος in English clause, not later ἦλθον"),
 (11,14,'was',['w11'],False,"Passive auxiliary with χειραγωγούμενος"),
 (11,16,'by',['w11'],False,"Part of idiom 'led by the hand' without unrelated phrase span"),
 (11,17,'the',['w11'],False,"Part of idiom 'by the hand' for χειραγωγούμενος"),
 (11,19,'by',['w12'],False,"Renders ὑπό without unrelated phrase span"),
 (11,21,'who',['w14'],False,"Relative English support for συνόντων ('those who were with')"),
 (13,1,'to',['w2'],False,"Renders πρός without unrelated phrase span"),
 (13,2,'me',['w3'],False,"Renders ἐμέ without unrelated phrase span"),
 (13,3,'and',['w4'],False,"Renders first καί without unrelated phrase span"),
 (13,6,'me',['w5'],False,"Part of contextual rendering ἐπιστὰς ('stood by me')"),
 (13,7,'and',['w4'],False,"Renders coordination into said-clause without unrelated phrase span"),
 (13,9,'to',['w7'],False,"Dative 'to me' without unrelated phrase span"),
 (13,10,'me,',['w7'],False,"Renders μοι without unrelated phrase span"),
 (13,13,'see',['w10'],False,"Renders ἀνάβλεψον, not later ἀνέβλεψα"),
 (13,14,'again!’',['w10'],False,"Second part of 'see again' rendering of ἀνάβλεψον"),
 (13,15,'And',['w11'],False,"Renders κἀγώ without unrelated phrase span"),
 (13,16,'at',['w12'],False,"Temporal preposition supplied by αὐτῇ in context"),
 (13,17,'that',['w12'],False,"Renders demonstrative force of αὐτῇ"),
 (13,18,'very',['w12'],False,"Intensifying rendering of αὐτῇ"),
 (16,0,'And',['w1'],False,"Renders καί without unrelated phrase span"),
 (16,3,'do',['w4'],False,"English auxiliary in 'do you delay?' belongs with μέλλεις, not βάπτισαι"),
 (16,4,'you',['w4'],False,"Subject carried by μέλλεις without unrelated phrase span"),
 (16,6,'Get',['w5'],False,"Imperatival rendering of ἀναστὰς without unrelated phrase span"),
 (16,7,'up,',['w5'],False,"Part of ἀναστὰς rendering without unrelated phrase span"),
 (16,10,'and',['w7'],False,"Renders καί without unrelated phrase span"),
 (16,13,'your',['w11'],False,"Renders σου without unrelated phrase span"),
 (16,17,'his',['w15'],False,"Renders αὐτοῦ without unrelated phrase span"),
 (19,0,'And',['w1'],False,"Renders κἀγώ without unrelated phrase span"),
 (19,1,'I',['w1'],False,"Renders κἀγώ without unrelated phrase span"),
 (19,9,'every',['w12','w13','w14'],False,"Contextual rendering of κατὰ τὰς συναγωγὰς ('in every synagogue')"),
 (19,16,'those',['w15'],False,"Renders τοὺς"),
 (19,17,'who',['w15'],False,"English relative support for substantival τοὺς"),
 (19,19,'in',['w17'],False,"Renders ἐπί, not earlier κατά"),
]

count=0
for vn,idx,expected,ids,supplied,reason in EDITS:
    verse=next(v for v in d['verses'] if v['v']==vn)
    x=verse['alignment']['dgt'][idx]
    if x.get('text') != expected:
        raise SystemExit(f"Acts 22:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids)
    if supplied:
        x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 41: '+reason
    count+=1

path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-41 corrections in Acts 22')
