#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data'/'acts'/'08.json'
d=json.loads(path.read_text(encoding='utf8'))

EDITS=[
 (4,10,'news',['w6'],False,"'announcing the good news' is the rendering of εὐαγγελιζόμενοι; λόγον remains 'word'"),
 (4,12,'the',['w7'],False,"Article with λόγον without unrelated phrase span"),

 (6,0,'And',['w2'],False,"Opening connective renders δὲ, leaving καί w15 for heard-and-saw"),
 (6,1,'the',['w3'],False,"Article with crowds"),
 (6,7,'paying',['w1'],False,"Renders προσεῖχον ('were paying attention')"),
 (6,8,'attention',['w1'],False,"Completes rendering of προσεῖχον"),
 (6,10,'the',['w5'],False,"Article within 'the things' belongs to τοῖς, not τοῦ w8"),
 (6,16,'they',['w14'],False,"Renders αὐτοὺς without unrelated phrase span"),
 (6,20,'the',['w17'],False,"Article with signs without unrelated phrase span"),
 (6,24,'doing.',['w20'],False,"Renders ἐποίει"),

 (13,0,'And',['w2'],False,"Opening connective renders δὲ without unrelated phrase span"),
 (13,5,'and',['w7'],False,"Renders καί without unrelated phrase span"),
 (13,7,'being',['w8'],False,"Passive participial rendering belongs to βαπτισθεὶς, not γινομένας"),
 (13,9,'he',['w9'],False,"Subject with ἦν without unrelated phrase span"),
 (13,10,'was',['w9'],False,"Renders ἦν without unrelated phrase span"),
 (13,11,'continually',['w10'],False,"Renders προσκαρτερῶν"),
 (13,15,'seeing',['w13'],False,"Renders θεωρῶν"),
 (13,17,'and',['w16'],False,"Renders καί without unrelated phrase span"),
 (13,19,'powerful',['w17'],False,"Renders δυνάμεις as 'powerful works/miracles'"),
 (13,20,'works',['w17'],False,"Completes rendering of δυνάμεις"),
 (13,21,'happening,',['w19'],False,"Renders γινομένας"),
 (13,22,'he',['w20'],False,"Subject of ἐξίστατο without unrelated phrase span"),
 (13,23,'was',['w20'],False,"Auxiliary with ἐξίστατο without unrelated phrase span"),

 (20,0,'But',['w2'],False,"Opening connective renders δὲ"),
 (20,3,'to',['w4'],False,"Renders πρός without unrelated phrase span"),
 (20,5,'“May',['w11'],False,"Optative force of εἴη, not earlier εἶπεν"),
 (20,6,'your',['w8'],False,"Renders σου"),
 (20,8,'go',['w11'],False,"English support for optative εἴη in 'may ... go/be to destruction'"),
 (20,10,'you',['w10'],False,"Renders σοὶ, not σου"),
 (20,11,'to',['w12'],False,"Renders εἰς without unrelated phrase span"),
 (20,14,'you',['w19'],False,"Subject carried by ἐνόμισας, not σοὶ w10"),
 (20,17,'could',['w19'],False,"English modal support for ἐνόμισας + infinitive"),
 (20,19,'the',['w15'],False,"Article with gift, not genitive τοῦ w17"),
 (20,21,'of',['w17'],False,"Genitive article relation in 'of God' without unrelated span"),
 (20,23,'with',['w20'],False,"Renders διά as means 'with/by money', not earlier σύν"),

 (22,2,'from',['w3'],False,"Renders ἀπό rather than supplied glue"),
 (22,5,'of',[],True,"English genitival glue in 'wickedness of yours' is supplied; ἀπό already renders 'from'"),
 (22,10,'the',['w10'],False,"Article/dative in 'to the Lord' without unrelated phrase span"),
 (22,12,'that,',[],True,"English complementizer before conditional clause is supplied"),
 (22,14,'possible,',['w13'],False,"Contextual rendering of ἄρα ('if perhaps/possible')"),
 (22,15,'the',['w16'],False,"Article with intention"),
 (22,16,'intention',['w17'],False,"Renders ἐπίνοια"),
 (22,18,'your',['w20'],False,"Possessive 'your heart' renders second σου, not first σου w6"),
 (22,20,'may',['w14'],False,"Future/passive force of ἀφεθήσεται rendered modally"),
 (22,23,'you.',['w15'],False,"Renders dative σοι, not possessive σου w20"),

 (25,2,'solemnly',['w4'],False,"Adverbial rendering within διαμαρτυράμενοι"),
 (25,6,'the',['w7'],False,"Article with word without unrelated phrase span"),
 (25,8,'of',['w9'],False,"Genitive article relation without unrelated phrase span"),
 (25,9,'the',['w9'],False,"Article in 'of the Lord' without unrelated phrase span"),
 (25,11,'they',['w1'],False,"Opening subject Οἱ for 'they returned'"),
 (25,12,'returned',['w11'],False,"Renders ὑπέστρεφον"),
 (25,13,'to',['w12'],False,"Renders εἰς without unrelated phrase span"),
 (25,15,'and',['w15'],False,"Connective τε introduces second clause, not earlier καί w5"),
 (25,17,'were',['w19'],False,"Auxiliary with εὐηγγελίζοντο, not ὑπέστρεφον"),
 (25,19,'good',['w19'],False,"Part of 'announcing good news' rendering of εὐηγγελίζοντο"),
 (25,20,'news',['w19'],False,"Part of 'announcing good news' rendering of εὐηγγελίζοντο"),
 (25,21,'to',['w14'],False,"Dative-like contextual rendering of πολλάς in 'to many villages' without unrelated span"),
 (25,24,'of',['w17'],False,"Genitive article relation without unrelated phrase span"),
 (25,25,'the',['w17'],False,"Article with Samaritans without unrelated phrase span"),

 (30,1,'ran',['w1'],False,"Renders προσδραμὼν"),
 (30,3,'and',['w2'],False,"First clause connective renders δὲ, leaving καί w11 before 'said'"),
 (30,5,'him',['w6'],False,"Renders αὐτοῦ without unrelated phrase span"),
 (30,6,'reading',['w7'],False,"Renders ἀναγινώσκοντος without unrelated phrase span"),
 (30,8,'the',['w9'],False,"Article with prophet without unrelated phrase span"),
 (30,12,'“Do',[],True,"English interrogative auxiliary is supplied"),
 (30,13,'you',['w15'],False,"Subject carried by γινώσκεις without unrelated phrase span"),
 (30,16,'you',['w17'],False,"Subject carried by ἀναγινώσκεις without unrelated phrase span"),
 (30,18,'reading?”',['w17'],False,"Renders ἀναγινώσκεις without unrelated phrase span"),

 (31,0,'He',['w1'],False,"Article/substantival subject ὁ carried as 'He', not εἶπεν"),
 (31,9,'And',['w14'],False,"Second-clause connective renders τε, not earlier δὲ"),
 (31,10,'he',['w13'],False,"Subject of παρεκάλεσεν without unrelated phrase span"),
 (31,16,'and',[],True,"English coordination between 'come up' and 'sit' is supplied"),

 (40,0,'But',['w2'],False,"Opening connective renders δὲ"),
 (40,2,'was',['w3'],False,"Passive auxiliary with εὑρέθη, not later εὐηγγελίζετο"),
 (40,10,'was',['w8'],False,"Auxiliary with εὐηγγελίζετο without unrelated phrase span"),
 (40,12,'good',['w8'],False,"Part of 'announcing good news' rendering of εὐηγγελίζετο"),
 (40,13,'news',['w8'],False,"Part of 'announcing good news' rendering of εὐηγγελίζετο"),
 (40,14,'to',['w9'],False,"Dative/article force before cities without unrelated phrase span"),
 (40,16,'the',['w9'],False,"Article with cities, not genitive τοῦ w13"),
 (40,17,'cities',['w10'],False,"Renders πόλεις"),
 (40,21,'to',['w16'],False,"Renders εἰς without unrelated phrase span"),
]

count=0
for vn,idx,expected,ids,supplied,reason in EDITS:
    verse=next(v for v in d['verses'] if v['v']==vn)
    x=verse['alignment']['dgt'][idx]
    if x.get('text') != expected:
        raise SystemExit(f"Acts 8:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids)
    if supplied:
        x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 47: '+reason
    count+=1

path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-47 corrections in Acts 8')
