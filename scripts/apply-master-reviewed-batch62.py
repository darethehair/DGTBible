#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
files={}

def get(ch):
    if ch not in files:
        p=ROOT/'data'/'john'/f'{ch:02}.json'
        files[ch]=(p,json.loads(p.read_text(encoding='utf8')))
    return files[ch][1]

def edit(ch,vn,idx,expected,ids,supplied,reason):
    d=get(ch)
    verse=next(v for v in d['verses'] if v['v']==vn)
    x=verse['alignment']['dgt'][idx]
    if x.get('text') != expected:
        raise SystemExit(f"John {ch}:{vn} token {idx}: expected {expected!r}, got {x.get('text')!r}")
    x['ids']=list(ids); x['phraseIds']=list(ids)
    if supplied:
        x['supplied']=True; x['confidence']='reviewed-master-supplied'
    else:
        x.pop('supplied',None); x['confidence']='reviewed-master-precise'
    x['reason']='Human-reviewed full-NT master pass batch 62: '+reason

# John 1
edit(1,16,9,'in',['w11'],False,"ἀντί rendered idiomatically as 'in place of'")
edit(1,16,10,'place',['w11'],False,"Part of 'in place of' rendering of ἀντί")
edit(1,16,11,'of',['w11'],False,"Completes 'in place of' rendering; do not reuse αὐτοῦ")
edit(1,18,5,'God',['w1'],False,"First God renders θεόν; second God renders w6")
edit(1,18,6,'The',[],True,"English article before 'one and only God' is supplied")
edit(1,18,7,'one',['w5'],False,"Renders μονογενής as 'one and only'")
edit(1,18,8,'and',['w5'],False,"Part of idiomatic 'one and only' rendering")
edit(1,18,9,'only',['w5'],False,"Completes μονογενής rendering")
edit(1,22,16,'who',['w9'],False,"Substantival τοῖς before πέμψασιν supplies relative 'who'")
edit(1,27,5,'whose',['w5'],False,"Relative οὗ supplies 'whose'")
edit(1,27,12,'to',['w9'],False,"Purpose ἵνα supplies infinitival 'to untie'")
edit(1,31,7,'I',['w13'],False,"Second 'I' belongs to explicit ἐγώ in 'I came', not opening κἀγώ")
edit(1,31,12,'so',['w6'],False,"Purpose ἵνα rendered as 'so that'")

# John 10
edit(10,14,10,'my',['w15'],False,"Second 'my own' belongs to second ἐμά")
edit(10,14,11,'own',['w15'],False,"Second 'own' renders second ἐμά, not first ἐμά")

# John 11
edit(11,37,5,'“Could',['w7'],False,"Modal 'Could' renders ἐδύνατο, not εἶπαν")
edit(11,37,6,'not',['w6'],False,"First negation οὐκ supplies 'not'; later μή is absorbed by 'kept ... from dying'")
edit(11,37,13,'of',['w13'],False,"Genitive article before blind man")
edit(11,37,16,'man,',['w14'],False,"Second 'man' belongs to τυφλοῦ ('blind man'), not οὗτος")
edit(11,37,18,'kept',['w15','w19'],False,"Contextual rendering of ποιῆσαι ... μή as 'kept ... from'")
edit(11,37,22,'from',['w15','w19'],False,"Part of contextual negative prevention construction")

# John 13
edit(13,19,8,'it',['w7'],False,"First 'it happens' belongs to γενέσθαι")
edit(13,19,9,'happens,',['w7'],False,"First 'happens' renders γενέσθαι, not later γένηται")
edit(13,19,13,'it',['w11'],False,"Second 'it happens' belongs to γένηται")
edit(13,19,16,'may',['w9'],False,"Modal force belongs to πιστεύσητε, not γένηται")

# John 14
edit(14,29,7,'it',['w6'],False,"First 'it happens' belongs to γενέσθαι")
edit(14,29,8,'happens,',['w6'],False,"First 'happens' renders γενέσθαι, not later γένηται")
edit(14,29,9,'so',['w7'],False,"Purpose ἵνα rendered as 'so that'")
edit(14,29,12,'it',['w9'],False,"Second 'it happens' belongs to γένηται")
edit(14,29,14,'you',['w10'],False,"Subject carried by πιστεύσητε")
edit(14,29,15,'may',['w10'],False,"Modal force of πιστεύσητε")

# John 16
edit(16,21,17,'given',['w14'],False,"Second birth clause renders γεννήσῃ, not earlier τίκτῃ")
edit(16,21,18,'birth',['w14'],False,"Completes second γεννήσῃ rendering")
edit(16,21,19,'to',[],True,"English dative/idiomatic support in 'give birth to the child' is supplied")
edit(16,21,22,'she',['w18'],False,"Subject of 'she no longer remembers' carried by μνημονεύει")
edit(16,21,28,'because',['w21'],False,"Causal διά rendered as 'because of'")
edit(16,21,35,'being',['w26'],False,"ἄνθρωπος supplies the noun phrase 'human being'; birth verb remains w25")

# John 18
edit(18,23,6,'wrongly,',['w6'],False,"Renders κακῶς")
edit(18,23,15,'do',[],True,"English interrogative auxiliary in 'why do you hit me?' is supplied")
edit(18,23,17,'hit',['w17'],False,"Renders δέρεις")
edit(18,26,6,'a',[],True,"English article before 'relative' is supplied")
edit(18,26,8,'of',['w9'],False,"Part of participial relation ὢν ('being a relative of')")
edit(18,26,10,'man',['w10'],False,"Relative οὗ supplies referent 'man whose ear...'")
edit(18,26,11,'whose',['w10'],False,"Renders relative οὗ")
edit(18,26,18,'“Did',[],True,"English interrogative auxiliary is supplied")

# John 19
edit(19,31,6,'the',[],True,"English article in 'the day of preparation' is supplied")
edit(19,31,7,'day',['w5'],False,"Preparation παρασκευή is rendered idiomatically as 'day of preparation'; later ἡμέρα is the Sabbath day")
edit(19,31,8,'of',[],True,"English genitive glue in 'day of preparation' is supplied")
edit(19,31,12,'the',['w13'],False,"Article with bodies belongs to τὰ, not cross article")
edit(19,31,14,'would',['w9'],False,"Subjunctive/modal force of μείνῃ")
edit(19,31,17,'on',['w10'],False,"First 'on' belongs to cross phrase ἐπὶ τοῦ σταυροῦ")
edit(19,31,18,'the',['w11'],False,"Article with cross")
edit(19,31,20,'on',['w15'],False,"Second 'on' belongs to Sabbath phrase ἐν τῷ σαββάτῳ")
edit(19,31,21,'the',['w16'],False,"Article with first Sabbath")
edit(19,31,22,'Sabbath—for',['w17','w19'],False,"Punctuation-bound token carries σαββάτῳ and causal γάρ")
edit(19,31,24,'Sabbath',['w25'],False,"Second Sabbath renders σαββάτου, not first σαββάτῳ")
edit(19,31,28,'great',['w20'],False,"Renders μεγάλη, not second Sabbath")
edit(19,31,29,'one—asked',['w26'],False,"English 'one' is supplied by the preceding day phrase; lexical content here is 'asked'")
edit(19,31,38,'they',[],True,"English subject of final passive clause is supplied")

for p,d in files.values():
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

allow_path=ROOT/'data'/'master-review-allowlist.json'
a=json.loads(allow_path.read_text(encoding='utf8'))
items=set(a.get('interactions',[]))
items.add('precise-scattered|john|1|27|w10')
a['interactions']=sorted(items)
allow_path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

print('Applied reviewed John master-alignment corrections and reviewed one legitimate split rendering')
