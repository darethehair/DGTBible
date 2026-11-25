#!/usr/bin/env python3
import json, runpy
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

# Recover reviewed Acts 22 work from the canceled batch-41 run.
runpy.run_path(str(ROOT/'scripts'/'apply-master-reviewed-batch41.py'), run_name='__main__')

path=ROOT/'data'/'acts'/'20.json'
d=json.loads(path.read_text(encoding='utf8'))

EDITS=[
 (4,0,'And',[],True,"Opening English connective is supplied; δὲ later marks continuation"),
 (4,6,'Berea',['w9'],False,"Renders Βεροιαῖος"),
 (4,9,'and',['w11'],False,"Clause connective before Aristarchus/Secundus belongs to δὲ w11, not καί w13"),
 (4,20,'and',['w18'],False,"Renders καί joining Gaius and Timothy without unrelated phrase span"),
 (4,22,'and',['w21'],False,"Clause connective before the Asia group belongs to δὲ w21, not previous καί w18"),
 (4,24,'Asia',['w20'],False,"Renders Ἀσιανοὶ ('from Asia/Asians')"),
 (4,26,'and',['w23'],False,"Renders καί joining Tychicus and Trophimus without unrelated phrase span"),
 (7,1,'on',['w1'],False,"Temporal preposition comes from Ἐν, not later τῇ w19"),
 (7,2,'the',['w3'],False,"Article with first day without unrelated phrase span"),
 (7,4,'day',['w4'],False,"Part of μιᾷ rendering without unrelated phrase span"),
 (7,5,'of',['w5'],False,"Genitive article relation without unrelated phrase span"),
 (7,6,'the',['w5'],False,"Article in 'of the week' without unrelated phrase span"),
 (7,10,'were',['w7'],False,"Passive auxiliary with συνηγμένων, not κλάσαι"),
 (7,11,'gathered',['w7'],False,"Renders συνηγμένων"),
 (7,12,'to',['w11'],False,"Infinitival marker with κλάσαι, not αὐτοῖς"),
 (7,16,'began',['w15'],False,"Aspectual English rendering of διελέγετο"),
 (7,17,'speaking',['w15'],False,"Renders διελέγετο"),
 (7,18,'to',['w16'],False,"Dative 'to them' without unrelated phrase span"),
 (7,20,'intending',['w17'],False,"Renders μέλλων"),
 (7,21,'to',['w18'],False,"Infinitival marker with ἐξιέναι without unrelated phrase span"),
 (7,23,'the',['w19'],False,"Article in 'the next day' without unrelated phrase span"),
 (7,25,'day,',['w20'],False,"Renders ἐπαύριον without unrelated phrase span"),
 (7,28,'extended',['w21'],False,"Renders παρέτεινεν"),
 (7,29,'his',['w24'],False,"English possessive with λόγον in 'his message'"),
 (7,30,'message',['w24'],False,"Renders λόγον"),
 (9,0,'And',[],True,"Opening English connective is supplied from discourse δέ"),
 (9,9,'the',['w8'],False,"Article with window without unrelated phrase span"),
 (9,12,'sinking',['w10'],False,"Contextual rendering of καταφερόμενος"),
 (9,16,'sleep',['w11'],False,"Renders ὕπνῳ without unrelated phrase span"),
 (9,19,'kept',['w13'],False,"Aspectual English support for διαλεγομένου"),
 (9,20,'speaking',['w13'],False,"Renders διαλεγομένου"),
 (9,23,'long',['w17'],False,"Renders πλεῖον ('longer/long time')"),
 (9,24,'time.',['w17'],False,"Contextual completion of πλεῖον"),
 (9,25,'Overcome',['w18'],False,"Renders κατενεχθεὶς"),
 (9,26,'by',['w19'],False,"Renders ἀπό in 'by sleep' without unrelated phrase span"),
 (9,27,'sleep,',['w21'],False,"Renders ὕπνου without unrelated phrase span"),
 (9,32,'the',['w24'],False,"Article with third floor without unrelated phrase span"),
 (9,34,'floor',['w25'],False,"Renders τριστέγου ('third story/floor')"),
 (12,0,'And',['w2'],False,"Renders δὲ without unrelated phrase span"),
 (14,7,'we',['w8'],False,"Subject of 'we took him aboard' carried by ἀναλαβόντες, not later ἤλθομεν"),
 (16,0,'For',['w2'],False,"Renders γὰρ without unrelated phrase span"),
 (16,4,'to',['w5'],False,"Infinitival marker with παραπλεῦσαι without unrelated phrase span"),
 (16,6,'past',['w5'],False,"Renders compound sense of παραπλεῦσαι ('sail past')"),
 (16,10,'he',['w10','w11'],False,"Subject/support of 'he would not spend time' belongs to γένηται αὐτῷ, not later ἔσπευδεν"),
 (16,11,'would',['w10'],False,"Modal/subjunctive force of γένηται, not εἴη in later clause"),
 (16,15,'in',['w13'],False,"Renders ἐν without unrelated phrase span"),
 (16,20,'hurrying,',['w16'],False,"Renders ἔσπευδεν"),
 (16,24,'be',['w26'],False,"Infinitival rendering of γενέσθαι, not εἴη"),
 (16,28,'the',['w22'],False,"Article in 'on the day' belongs with τὴν w22, not genitive τῆς w24"),
 (20,2,'held',['w3'],False,"Renders ὑπεστειλάμην"),
 (20,4,'nothing',['w2'],False,"Renders οὐδέν"),
 (20,7,'was',['w5'],False,"Copular English support for συμφερόντων ('what was beneficial'), not ἀναγγεῖλαι"),
 (20,8,'beneficial',['w5'],False,"Renders συμφερόντων"),
 (20,9,'from',[],True,"English complement in 'held back ... from declaring' is supplied"),
 (20,12,'to',['w8'],False,"Infinitival marker with ἀναγγεῖλαι without unrelated phrase span"),
 (20,13,'you',['w9'],False,"Renders ὑμῖν without unrelated phrase span"),
 (20,14,'and',['w10'],False,"Renders καί without unrelated phrase span"),
 (20,16,'you',['w12'],False,"Renders ὑμᾶς without unrelated phrase span"),
 (20,18,'and',['w14'],False,"Renders second καί without unrelated phrase span"),
 (20,21,'to',['w16'],False,"Part of idiom 'house to house' for οἴκους, not broad span"),
 (25,2,'look,',['w3'],False,"Renders ἰδοὺ without unrelated phrase span"),
 (25,3,'I',['w4'],False,"Renders ἐγὼ without unrelated phrase span"),
 (25,6,'none',['w7','w12','w13'],False,"Contextual rendering of οὐκέτι + ὑμεῖς πάντες ('none of you ... again')"),
 (25,7,'of',[],True,"English partitive glue in 'none of you'"),
 (25,8,'you',['w12','w13'],False,"Renders ὑμεῖς πάντες, not ὄψεσθε"),
 (25,17,'will',['w8'],False,"Future auxiliary carried by ὄψεσθε"),
 (25,18,'see',['w8'],False,"Renders ὄψεσθε"),
 (25,21,'again.',['w7'],False,"Renders οὐκέτι ('no longer/again')"),
 (36,5,'he',['w4'],False,"Subject of 'he knelt down' carried by participle θεὶς, not later προσηύξατο"),
 (36,6,'knelt',['w4','w6'],False,"Contextual rendering of θεὶς τὰ γόνατα"),
 (36,10,'of',[],True,"English partitive glue in 'all of them'"),
 (38,0,'being',['w1'],False,"Participial rendering of ὀδυνώμενοι"),
 (38,2,'grieved',['w1'],False,"Renders ὀδυνώμενοι"),
 (38,4,'the',['w4'],False,"Article with word without unrelated phrase span"),
 (38,10,'they',['w10'],False,"Subject carried by μέλλουσιν without unrelated phrase span"),
 (38,11,'were',['w10'],False,"Auxiliary in 'were about to' belongs to μέλλουσιν, not later προέπεμπον"),
 (38,15,'his',['w13'],False,"Renders αὐτοῦ without unrelated phrase span"),
 (38,18,'more.',['w9'],False,"Completes οὐκέτι ('no more')"),
 (38,20,'they',['w15'],False,"Subject of 'they accompanied' carried by προέπεμπον without unrelated phrase span"),
 (38,22,'him',['w17'],False,"Renders αὐτὸν without unrelated phrase span"),
 (38,23,'to',['w18'],False,"Renders εἰς without unrelated phrase span"),
 (38,24,'the',['w19'],False,"Article with ship without unrelated phrase span"),
]

count=0
for vn,idx,expected,ids,supplied,reason in EDITS:
    verse=next(v for v in d['verses'] if v['v']==vn)
    x=verse['alignment']['dgt'][idx]
    if x.get('text') != expected:
        raise SystemExit(f"Acts 20:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids)
    if supplied:
        x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 43: '+reason
    count+=1

path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-43 corrections in Acts 20, plus recovered Acts 22 batch 41')
