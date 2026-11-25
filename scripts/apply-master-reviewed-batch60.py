#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
files={}

def get(ch):
    if ch not in files:
        p=ROOT/'data'/'hebrews'/f'{ch:02}.json'
        files[ch]=(p,json.loads(p.read_text(encoding='utf8')))
    return files[ch][1]

def edit(ch,vn,idx,expected,ids,supplied,reason):
    d=get(ch)
    verse=next(v for v in d['verses'] if v['v']==vn)
    x=verse['alignment']['dgt'][idx]
    if x.get('text') != expected:
        raise SystemExit(f"Hebrews {ch}:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids)
    if supplied:
        x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 60: '+reason

# Hebrews 1
edit(1,1,2,'at',[],True,"English preposition in 'at many times' is supplied")
edit(1,1,3,'many',['w1'],False,"First 'many' belongs with Πολυμερῶς ('many portions/times'), not πολυτρόπως")
edit(1,1,14,'through',['w10'],False,"Greek ἐν is rendered idiomatically as 'through' the prophets")
edit(1,9,0,'You',['w1'],False,"Opening subject is carried by ἠγάπησας, not later σε")

# Hebrews 2
# 2:7 ἠλάττωσας legitimately renders split 'You made ... lower'.
edit(2,17,1,'he',['w2'],False,"Subject/support of ὤφειλεν ('he had to')")
edit(2,17,2,'had',['w2'],False,"Past modal rendering of ὤφειλεν")
edit(2,17,3,'to',['w2'],False,"Infinitival support governed by ὤφειλεν")
edit(2,17,4,'become',['w7'],False,"First 'become like' renders ὁμοιωθῆναι, not later γένηται")
edit(2,17,8,'and',[],True,"English coordination in 'brothers and sisters' is supplied")
edit(2,17,9,'sisters',['w6'],False,"Inclusive English rendering of ἀδελφοῖς")
edit(2,17,11,'every',['w4'],False,"Renders πάντα in 'every way'")
edit(2,17,12,'way,',['w4'],False,"Completes πάντα contextual rendering")
edit(2,17,25,'matters',['w14'],False,"Substantival τὰ in τὰ πρὸς τὸν θεόν rendered as 'matters'")
edit(2,17,29,'to',['w18'],False,"Purpose εἰς rendered as 'to/in order to'")
edit(2,17,32,'for',['w20'],False,"Part of ἱλάσκεσθαι contextual rendering 'make atonement for'")

# Hebrews 3
edit(3,9,1,'your',['w6'],False,"Renders ὑμῶν")
edit(3,9,3,'tested',['w2'],False,"Verb 'tested' renders ἐπείρασαν, not δοκιμασίᾳ")
edit(3,9,4,'me',[],True,"Object 'me' is supplied by the quotation context")
# 3:11 εἰσελεύσονται legitimately spans 'They will ... enter' around negation.

# Hebrews 4
edit(4,1,1,'let',['w1'],False,"Hortatory/subjunctive force of Φοβηθῶμεν")
edit(4,1,2,'us',['w1'],False,"First-person plural carried by Φοβηθῶμεν")
edit(4,1,6,'a',[],True,"English article before promise is supplied")
edit(4,1,8,'of',[],True,"English genitive/infinitival glue in 'promise of entering' is supplied")
edit(4,1,16,'should',['w11'],False,"Subjunctive/modal force of δοκῇ")
# 4:1 καταλειπομένης legitimately spans 'while ... remains'.
# 4:5 εἰσελεύσονται legitimately spans around negation.
edit(4,8,3,'had',['w5'],False,"Past-perfect auxiliary belongs with κατέπαυσεν ('had given rest')")
edit(4,8,11,'have',['w10'],False,"Perfect English support in 'would not ... have spoken' belongs with ἐλάλει")
# 4:8 ἐλάλει legitimately supplies split 'he ... spoken'.

# Hebrews 8
edit(8,5,1,'serve',['w5'],False,"Renders λατρεύουσιν")
edit(8,5,9,'things,',['w7'],False,"First 'things' belongs with τῶν ἐπουρανίων, not later πάντα")
edit(8,5,10,'just',['w8'],False,"καθὼς rendered as 'just as'")
edit(8,5,13,'was',['w9'],False,"Perfect/passive support with κεχρημάτισται")
edit(8,5,14,'warned',['w9'],False,"Contextual rendering of κεχρημάτισται")
edit(8,5,15,'when',['w11'],False,"Participial μέλλων supplies temporal 'when'")
edit(8,5,16,'he',['w11'],False,"Subject carried by μέλλων")
edit(8,5,19,'to',['w12'],False,"Infinitival marker with ἐπιτελεῖν")
edit(8,5,35,'to',[],True,"English dative preposition before 'you' is supplied")
edit(8,7,4,'covenant',[],True,"English noun completing substantival 'first' is supplied from context")
edit(8,7,14,'for',['w10'],False,"Genitive/contextual δευτέρας rendered as 'for a second'")
edit(8,7,15,'a',[],True,"English article in 'for a second [covenant]' is supplied, not τόπος")
edit(8,13,8,'old;',['w5'],False,"First 'old' belongs to πεπαλαίωκεν ('made obsolete/old'), not later παλαιούμενον")
edit(8,13,9,'and',['w11'],False,"Renders καί")
edit(8,13,10,'what',['w8'],False,"Substantival article τὸ supplies 'what'")
edit(8,13,11,'is',['w10'],False,"Copular support with παλαιούμενον")
edit(8,13,12,'becoming',['w10'],False,"Renders παλαιούμενον")

# Hebrews 9
edit(9,8,5,'indicates',['w2'],False,"Renders δηλοῦντος")
edit(9,8,6,'that',[],True,"English complementizer after 'indicates' is supplied; μήπω means 'not yet'")
edit(9,8,13,'has',['w8'],False,"Perfect auxiliary with πεφανερῶσθαι")
edit(9,8,14,'not',['w7'],False,"Negative force of μήπω")
edit(9,8,15,'yet',['w7'],False,"Temporal force of μήπω")
edit(9,8,22,'is',['w17'],False,"Copular support with ἐχούσης")
edit(9,12,9,'not',['w1'],False,"Renders οὐδὲ")
edit(9,12,10,'through',['w2'],False,"First 'through' belongs to διʼ before goat blood, not later διὰ")
edit(9,12,11,'the',[],True,"English article before blood is supplied")
edit(9,12,12,'blood',['w3'],False,"First blood renders αἵματος, not later own-blood αἵματος")
edit(9,12,18,'through',['w7'],False,"Second 'through' renders later διὰ")
edit(9,12,19,'his',['w10'],False,"Possessive force of ἰδίου")
edit(9,14,4,'the',['w3'],False,"Article with blood, not article before God")
edit(9,14,10,'the',[],True,"Greek πνεύματος has no article; English 'the eternal Spirit' article is supplied")
edit(9,14,15,'without',['w13'],False,"Contextual rendering of ἄμωμον as 'without blemish'")
edit(9,14,16,'blemish',['w13'],False,"Completes ἄμωμον rendering")
# 9:14 καθαριεῖ legitimately spans subject clause: 'will ... cleanse'.

# Hebrews 10
edit(10,15,0,'And',['w2'],False,"δὲ rendered as connective 'And'")
edit(10,15,6,'to',['w3'],False,"Dative 'to us' belongs with ἡμῖν, not εἰρηκέναι")

# Hebrews 11
edit(11,26,0,'considering',['w3'],False,"Renders ἡγησάμενος")
edit(11,26,1,'the',['w8'],False,"Article with reproach")
edit(11,26,3,'of',['w10'],False,"Genitive article before Christ")
edit(11,26,8,'the',[],True,"English article before treasures is supplied")
edit(11,26,10,'of',['w6'],False,"Genitive Egypt belongs with Αἰγύπτου, not Χριστοῦ")
edit(11,39,2,'these,',[],True,"English demonstrative is supplied from discourse context")
edit(11,39,3,'though',['w4'],False,"Concessive English rendering of participle μαρτυρηθέντες")
edit(11,39,5,'received',['w4'],False,"First 'received testimony' renders μαρτυρηθέντες, not ἐκομίσαντο")
edit(11,39,6,'testimony',['w4'],False,"Contextual rendering of μαρτυρηθέντες")
edit(11,39,9,'did',['w9'],False,"English auxiliary with ἐκομίσαντο")

# Hebrews 12
edit(12,29,3,'is',[],True,"English copula in 'God is a consuming fire' is supplied")
edit(12,29,4,'a',[],True,"English article before 'consuming fire' is supplied")

# Hebrews 13
edit(13,17,4,'yield',['w6'],False,"Renders ὑπείκετε")
edit(13,17,6,'them,',['w2','w3'],False,"Contextual object 'them' refers to leaders")
edit(13,17,9,'keep',[],True,"English aspectual support in 'keep watch' is supplied")
edit(13,17,12,'your',['w13'],False,"Renders ὑμῶν")
edit(13,17,15,'those',['w7'],False,"Emphatic/substantival αὐτοί supplies 'those'")
edit(13,17,16,'who',[],True,"English relative pronoun is supplied")
edit(13,17,17,'will',['w16'],False,"Future/participial sense of ἀποδώσοντες")
edit(13,17,21,'so',['w17'],False,"Purpose ἵνα rendered as 'so that'")
edit(13,17,31,'with',[],True,"English preposition in 'with groaning' is supplied")
edit(13,17,33,'for',['w26'],False,"γάρ rendered as causal 'for'")
edit(13,17,34,'that',['w28'],False,"Demonstrative τοῦτο supplies 'that'")
edit(13,17,35,'would',['w25'],False,"English modal/copular support with ἀλυσιτελές, not ἀποδώσοντες")
edit(13,17,36,'be',['w25'],False,"Copular support with ἀλυσιτελές")
edit(13,17,38,'for',['w27'],False,"Dative ὑμῖν rendered as 'for you'")

for p,d in files.values():
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=ROOT/'data'/'master-review-allowlist.json'
a=json.loads(allow_path.read_text(encoding='utf8'))
items=set(a.get('interactions',[]))
for key in [
 'precise-scattered|hebrews|2|7|w1',
 'precise-scattered|hebrews|3|11|w8',
 'precise-scattered|hebrews|4|1|w4',
 'precise-scattered|hebrews|4|5|w6',
 'precise-scattered|hebrews|4|8|w10',
 'precise-scattered|hebrews|9|14|w16',
]:
    items.add(key)
a['interactions']=sorted(items)
allow_path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Applied reviewed Hebrews master-alignment corrections and reviewed 6 legitimate split renderings')
