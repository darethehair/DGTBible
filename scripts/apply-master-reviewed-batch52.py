#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data'/'acts'/'02.json'
d=json.loads(path.read_text(encoding='utf8'))
EDITS=[
 (4,0,'And',['w1'],False,"Renders opening καί without unrelated phrase span"),
 (4,6,'the',[],True,"First 'the Holy Spirit' has no Greek article; English article is supplied"),
 (4,8,'Spirit',['w4'],False,"First Spirit renders πνεύματος without unrelated phrase span"),
 (4,9,'and',['w6'],False,"Renders second καί without unrelated phrase span"),
 (4,11,'to',['w8'],False,"Infinitival marker with λαλεῖν without unrelated phrase span"),
 (4,16,'just',['w11'],False,"Renders καθὼς ('just as')"),
 (4,18,'the',['w12'],False,"Article with second Spirit"),
 (4,19,'Spirit',['w13'],False,"Second Spirit renders πνεῦμα without unrelated phrase span"),
 (4,23,'utterance.',['w15'],False,"Renders ἀποφθέγγεσθαι"),

 (6,0,'And',['w2'],False,"Opening discourse connective renders δὲ, not later καί"),
 (6,4,'occurred,',['w1'],False,"Renders γενομένης"),
 (6,5,'the',['w7'],False,"Article with multitude"),
 (6,9,'and',['w9'],False,"Renders καί"),
 (6,10,'was',['w10'],False,"Passive auxiliary with συνεχύθη without unrelated phrase span"),
 (6,11,'confused,',['w10'],False,"Renders συνεχύθη"),
 (6,15,'was',['w12'],False,"Auxiliary with ἤκουον without unrelated phrase span"),
 (6,20,'his',['w16'],False,"Possessive force in 'his own language' belongs to ἰδίᾳ, not λαλούντων"),
 (6,21,'own',['w16'],False,"Renders ἰδίᾳ"),

 (11,2,'and',['w3'],False,"Renders first καί without unrelated phrase span"),
 (11,3,'proselytes,',['w4'],False,"Renders προσήλυτοι"),
 (11,5,'and',['w6'],False,"Renders second καί without unrelated phrase span"),
 (11,6,'Arabs—we',['w7','w8'],False,"Renders Ἄραβες plus English clause boundary into first-person verb"),
 (11,15,'mighty',['w15'],False,"Renders μεγαλεῖα ('great/mighty things')"),
 (11,16,'works',['w15'],False,"Contextual rendering of μεγαλεῖα, not ἀκούομεν"),
 (11,17,'of',['w16'],False,"Genitive article in 'of God'"),

 (12,0,'And',['w2'],False,"Opening connective renders δὲ, not later καί"),
 (12,1,'they',['w1'],False,"Subject of first clause carried by ἐξίσταντο"),
 (12,2,'were',['w1'],False,"Auxiliary with ἐξίσταντο"),
 (12,5,'and',['w4'],False,"Renders καί"),
 (12,6,'perplexed,',['w5'],False,"Renders διηπόρουν without shared subject span"),
 (12,8,'to',['w7'],False,"Renders πρός without unrelated phrase span"),

 (23,0,'this',['w1'],False,"Renders τοῦτον"),
 (23,1,'man,',['w1'],False,"Contextual rendering of τοῦτον"),
 (23,16,'him',['w1'],False,"Same demonstrative/object referent legitimately carries English 'him' in reordered crucifixion clause"),
 (23,21,'the',[],True,"English article in 'through the hands' is supplied"),
 
 (24,2,'him',['w1'],False,"First object 'him' renders relative ὃν, not later αὐτόν"),
 (24,4,'releasing',['w5'],False,"Renders λύσας"),
 (24,5,'the',['w6'],False,"Article with pains without unrelated phrase span"),
 (24,6,'pains',['w7'],False,"Renders ὠδῖνας"),
 (24,7,'of',['w8'],False,"Genitive article in 'of death'"),
 (24,9,'because',['w10'],False,"Renders καθότι"),
 
 (29,2,'is',['w3'],False,"Copular support from ἐξόν without unrelated phrase span"),
 (29,4,'to',['w4'],False,"Infinitival marker with εἰπεῖν"),
 (29,6,'boldly',['w6'],False,"Adverbial rendering of μετὰ παρρησίας"),
 (29,7,'to',['w7'],False,"Renders πρός without unrelated phrase span"),
 (29,10,'the',['w10'],False,"Article with patriarch without unrelated phrase span"),
 (29,17,'and',['w16'],False,"Renders second καί without unrelated phrase span"),
 (29,20,'and',['w18'],False,"Renders third καί without unrelated phrase span"),
 (29,21,'his',['w21'],False,"Renders αὐτοῦ without unrelated phrase span"),
 (29,23,'is',['w22'],False,"Renders ἔστιν without unrelated phrase span"),
 (29,24,'with',['w23'],False,"Renders ἐν idiomatically as 'with us', not earlier μετὰ"),
 (29,25,'us',['w24'],False,"Renders ἡμῖν"),
 (29,26,'to',['w25'],False,"Renders ἄχρι ('to/until') rather than πρός"),
 
 (30,8,'had',['w8'],False,"Past-perfect auxiliary belongs to ὤμοσεν, not εἰδὼς"),
 (30,9,'sworn',['w8'],False,"Renders ὤμοσεν"),
 (30,10,'to',['w9'],False,"Dative 'to him' without unrelated phrase span"),
 (30,11,'him',['w9'],False,"Renders αὐτῷ"),
 (30,15,'that',['w6'],False,"Second English complementizer still belongs to the single Greek ὅτι governing the oath content"),
 (30,16,'one',[],True,"English nominal subject introduced by restructuring is supplied"),
 (30,17,'from',['w12'],False,"Renders ἐκ"),
 (30,18,'the',['w14'],False,"Genitive article in 'of his body' participates in noun phrase"),
 (30,20,'of',['w14'],False,"Genitive article relation"),
 (30,21,'his',['w16'],False,"Renders αὐτοῦ"),
 (30,22,'body',['w15'],False,"Contextual rendering of ὀσφύος ('loins/body')"),
 (30,23,'would',['w23'],False,"English modal support for infinitive καθίσαι"),
 (30,24,'sit',['w23'],False,"Renders καθίσαι"),
 (30,25,'on',['w24'],False,"Renders ἐπί"),
 (30,26,'his',['w27'],False,"Renders final αὐτοῦ without unrelated phrase span"),

 (34,2,'did',[],True,"English past-tense auxiliary in 'did not ascend' is supplied; Κάθου belongs only to quoted 'Sit'"),
 (34,6,'the',['w6'],False,"Article with heavens without unrelated phrase span"),
 (34,8,'but',['w9'],False,"Renders δὲ"),
 (34,12,'‘The',['w12'],False,"Article with Lord without unrelated phrase span"),
 (34,13,'Lord',['w13'],False,"Renders κύριος without unrelated phrase span"),
 (34,16,'my',['w16'],False,"Renders μου without unrelated phrase span"),
 (34,17,'Lord,',['w15'],False,"Renders κυρίῳ without unrelated phrase span"),
 (34,20,'my',['w20'],False,"Renders second μου without unrelated phrase span"),

 (42,0,'And',['w2'],False,"Opening connective renders δὲ, not later καί"),
 (42,3,'continually',['w3'],False,"Aspectual rendering of προσκαρτεροῦντες"),
 (42,4,'devoting',['w3'],False,"Renders προσκαρτεροῦντες"),
 (42,5,'themselves',['w3'],False,"Reflexive English support for προσκαρτεροῦντες"),
 (42,7,'the',['w4'],False,"Article/dative in 'to the teaching'"),
 (42,9,'of',['w6'],False,"Genitive article before apostles"),
 (42,10,'the',['w6'],False,"Article in 'of the apostles'"),
 (42,12,'and',['w8'],False,"Renders καί without unrelated phrase span"),
 (42,16,'the',['w12'],False,"Article/dative with breaking, not genitive τοῦ w14"),
 (42,18,'of',['w14'],False,"Genitive article before bread"),
 (42,20,'and',['w16'],False,"Renders second καί without unrelated phrase span"),

 (44,0,'And',['w2'],False,"Opening connective renders δὲ, not later καί"),
 (44,1,'all',['w1'],False,"Renders πάντες without unrelated phrase span"),
 (44,4,'were',['w5'],False,"Renders ἦσαν without unrelated phrase span"),
 (44,6,'and',['w9'],False,"Renders καί"),

 (46,0,'And',['w3'],False,"Opening connective renders first τε"),
 (46,5,'with',['w5'],False,"Renders ὁμοθυμαδὸν phrase without unrelated span"),
 (46,11,'and',['w10'],False,"Second connective before breaking renders second τε, not first τε"),
 (46,20,'sharing',['w14'],False,"Contextual rendering of μετελάμβανον"),
 (46,22,'with',['w16'],False,"Renders ἐν idiomatically as 'with' without unrelated span"),
 (46,24,'and',['w18'],False,"Renders καί without unrelated phrase span"),
 (46,26,'of',['w20'],False,"Genitive relation with καρδίας without unrelated span"),
]
count=0
for vn,idx,expected,ids,supplied,reason in EDITS:
    verse=next(v for v in d['verses'] if v['v']==vn); x=verse['alignment']['dgt'][idx]
    if x.get('text')!=expected: raise SystemExit(f"Acts 2:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids)
    if supplied: x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else: x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 52: '+reason; count+=1
path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'Applied {count} reviewed batch-52 corrections in Acts 2')
