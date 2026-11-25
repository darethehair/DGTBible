#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
files={}

def get(ch):
    if ch not in files:
        p=ROOT/'data'/'ephesians'/f'{ch:02}.json'
        files[ch]=(p,json.loads(p.read_text(encoding='utf8')))
    return files[ch][1]

def edit(ch,vn,idx,expected,ids,supplied,reason):
    d=get(ch)
    verse=next(v for v in d['verses'] if v['v']==vn)
    x=verse['alignment']['dgt'][idx]
    if x.get('text')!=expected:
        raise SystemExit(f"Ephesians {ch}:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids)
    if supplied:
        x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 58: '+reason

# Ephesians 1
edit(1,3,0,'Blessed',['w1'],False,"Opening adjective εὐλογητός supplies 'Blessed'; εὐλογήσας belongs to later 'blessed us'")
edit(1,3,6,'of',['w6'],False,"Genitive article τοῦ supplies 'of' before Lord")
edit(1,3,11,'who',['w11'],False,"Substantival article ὁ introducing εὐλογήσας supplies relative 'who'")
edit(1,3,19,'the',['w19'],False,"Article with heavenly places, not earlier τοῦ")
edit(1,3,21,'places',['w20'],False,"Contextual noun completion of ἐπουρανίοις")
# 1:16 ὑμῶν legitimately serves both 'for you' and 'mention of you'.

# Ephesians 2
edit(2,3,32,'also',['w28'],False,"Final 'also' renders the later καί before οἱ λοιποί")
edit(2,17,0,'And',['w1'],False,"Opening connective renders καί")
edit(2,17,11,'who',['w6'],False,"First relative 'who were far' belongs to τοῖς before μακράν, not later ἐγγύς")
edit(2,17,12,'were',[],True,"English copula in 'who were far away' is supplied")
edit(2,17,14,'away,',['w7'],False,"Completes rendering of μακράν")
edit(2,17,15,'and',['w8'],False,"Second connective renders καί")
edit(2,17,20,'were',[],True,"English copula in 'who were near' is supplied")
edit(2,19,11,'you',['w9'],False,"Second 'you are' belongs to the second ἐστὲ, not the first")
edit(2,19,15,'with',['w11'],False,"Genitive article τῶν is rendered idiomatically as 'with the saints'")
edit(2,19,16,'the',['w11'],False,"Article in 'with the saints'")
edit(2,19,19,'members',['w14'],False,"Contextual rendering of οἰκεῖοι as household members")
edit(2,19,23,'of',['w15'],False,"Genitive article before God")

# Ephesians 3
edit(3,1,0,'For',['w2'],False,"χάριν supplies causal 'For ... reason'; do not use later ὑπέρ")
edit(3,1,2,'reason',['w2'],False,"Completes 'For this reason' from χάριν")
edit(3,1,5,'the',['w5'],False,"Article with prisoner")
edit(3,1,7,'of',['w7'],False,"Genitive article before Christ, not Τούτου")
edit(3,1,10,'on',['w10'],False,"Part of idiomatic rendering of ὑπέρ as 'on behalf of'")
edit(3,1,11,'behalf',['w10'],False,"Part of idiomatic rendering of ὑπέρ")
edit(3,1,12,'of',['w10'],False,"Part of idiomatic rendering of ὑπέρ")
edit(3,1,14,'the',['w12'],False,"Article with nations/Gentiles")
edit(3,19,0,'and',['w2'],False,"Connective τε rendered as 'and'")
edit(3,19,3,'the',['w3'],False,"Article with love")
edit(3,19,7,'that',['w3'],False,"Relative/article force of τὴν introducing ὑπερβάλλουσαν")
edit(3,19,16,'to',['w12'],False,"Second 'to' renders εἰς, not earlier γνῶναί")
edit(3,19,18,'the',['w14'],False,"Article with fullness")
edit(3,20,4,'who',['w3'],False,"Participial δυναμένῳ supplies relative 'who'")
edit(3,20,5,'is',['w3'],False,"Copular support for δυναμένῳ ('who is able'), not later ἐνεργουμένην")
edit(3,20,9,'exceedingly',['w7'],False,"Renders ὑπερεκπερισσοῦ")
edit(3,20,10,'abundantly',['w7'],False,"Completes emphatic adverb ὑπερεκπερισσοῦ")
edit(3,20,11,'beyond',['w4'],False,"Renders ὑπέρ")

# Ephesians 4
edit(4,14,19,'by',['w12'],False,"Human trickery phrase is introduced by ἐν, not κλυδωνιζόμενοι")
edit(4,14,22,'by',['w17'],False,"Craftiness phrase is introduced by the later ἐν, not παντί")
edit(4,22,3,'according',['w3'],False,"First 'according to' renders the first κατά, not the later κατά")
edit(4,22,4,'to',['w3'],False,"Completes first κατά rendering")
edit(4,22,10,'the',['w7'],False,"Article with old man")
edit(4,22,13,'who',['w10'],False,"Article/relative before φθειρόμενον supplies 'who'")
edit(4,28,1,'the',['w1'],False,"Opening substantival article ὁ supplies 'the one'")
edit(4,28,2,'one',['w1'],False,"Completes substantival rendering of ὁ")
edit(4,28,8,'but',['w6'],False,"Contrastive δὲ renders 'but'")
edit(4,28,10,'let',[],True,"English imperative support before κοπιάτω is supplied")
edit(4,28,11,'him',['w7'],False,"Subject of κοπιάτω, not earlier κλεπτέτω")
edit(4,28,18,'his',['w10'],False,"Possessive force of ἰδίαις in 'his own hands'")
edit(4,28,29,'with',['w17'],False,"Dative article τῷ in 'share with the one', not earlier ἰδίαις")
edit(4,28,32,'in',['w18'],False,"English 'in need' belongs with χρείαν")
edit(4,29,0,'Let',['w9'],False,"Imperatival force of ἐκπορευέσθω supplies 'Let'")
edit(4,29,1,'no',['w8'],False,"Negation μή supplies 'no'")
edit(4,29,4,'come',['w9'],False,"Renders ἐκπορευέσθω")
edit(4,29,10,'only',['w11','w12'],False,"Contextual rendering of εἴ τις as restrictive 'only what'")
edit(4,29,11,'what',['w12'],False,"Substantival τις rendered as 'what'")
edit(4,29,12,'is',['w13'],False,"English copula with ἀγαθός")
edit(4,29,16,'up',['w15'],False,"Completes idiom 'building up' from οἰκοδομή")
edit(4,29,17,'according',['w16'],False,"Genitive article/need phrase rendered idiomatically as 'according to'")
edit(4,29,18,'to',['w16'],False,"Completes 'according to' phrase; do not borrow later τοῖς")
edit(4,29,24,'may',['w19'],False,"Subjunctive/modal force of δῷ")
edit(4,29,29,'who',['w21'],False,"Substantival article τοῖς before ἀκούουσιν supplies relative 'who'")

# Ephesians 5
edit(5,2,4,'just',['w5'],False,"Part of καθὼς rendered as 'just as'")
edit(5,2,21,'for',['w21'],False,"Final 'for a fragrant aroma' renders εἰς, not earlier ὑπέρ")
edit(5,8,5,'but',['w6'],False,"Contrastive δὲ renders 'but'")
edit(5,8,7,'you',[],True,"Second-clause subject is supplied in English; Greek has no repeated ὑμεῖς")
edit(5,8,8,'are',[],True,"Second-clause copula is supplied in English")
edit(5,24,1,'just',['w2'],False,"Part of ὡς rendered as 'just as'")
edit(5,24,3,'the',['w3'],False,"Article with assembly")
edit(5,24,11,'should',['w5'],False,"Elliptical second clause inherits the submit verb ὑποτάσσεται")
edit(5,24,12,'submit',['w5'],False,"Second-clause verbal sense is inherited from ὑποτάσσεται")
edit(5,24,13,'to',['w12'],False,"Dative article with husbands, not earlier Χριστῷ")
edit(5,24,14,'their',['w12'],False,"Possessive English rendering with husbands")

# Ephesians 6
edit(6,3,0,'“so',['w1'],False,"ἵνα supplies 'so that'")
edit(6,3,4,'go',['w4'],False,"Contextual rendering of γένηται in 'may go well'")
edit(6,3,10,'may',['w6'],False,"Second modal belongs to ἔσῃ, not earlier γένηται")
edit(6,3,13,'on',['w8'],False,"Renders ἐπί")

for p,d in files.values():
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=ROOT/'data'/'master-review-allowlist.json'
a=json.loads(allow_path.read_text(encoding='utf8'))
items=set(a.get('interactions',[]))
items.add('precise-scattered|ephesians|1|16|w5')
a['interactions']=sorted(items)
allow_path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Applied reviewed Ephesians master-alignment corrections and reviewed one legitimate repeated-pronoun rendering')
