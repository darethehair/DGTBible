#!/usr/bin/env python3
import json
from pathlib import Path

FIXES = {
13: {
  (1,0):["w1"],(1,6):None,(1,7):None,(1,9):None,(1,10):["w12"],(1,11):["w13"],
  (2,10):["w9"],(2,13):None,(2,16):["w21"],
  (3,12):["w11"],
  (4,1):["w2"],(4,3):["w4"],(4,6):None,(4,8):["w9"],(4,17):["w18"],
  (5,0):["w2"],(5,2):None,(5,4):["w4"],(5,9):["w9"],(5,11):["w9"],(5,19):["w15"],(5,20):None,(5,21):["w18"],(5,22):["w17"],
  (6,0):["w2"],(6,5):None,(6,6):["w4"],(6,9):["w6"],(6,10):None,(6,11):["w9"],(6,12):["w8"],
  (7,0):["w2"],(7,2):None,(7,4):["w4"],(7,7):None,(7,12):None,(7,14):["w13"],
  (8,0):["w2"],(8,2):None,(8,4):["w4"],(8,5):["w5"],(8,9):["w10"],(8,15):["w17"],(8,16):["w19"],(8,18):["w20"],
  (9,2):["w1"],(9,3):["w2"],(9,5):["w5"],
  (10,9):None,
  (11,23):["w17"],
  (12,3):None,(12,12):["w7"],(12,13):["w7"],(12,14):["w9"],(12,16):["w11"],(12,18):["w11"],
  (13,0):["w1","w2"],
  (14,1):["w4"],(14,9):["w8"],(14,14):["w10"],
  (15,16):["w11"],(15,22):["w18"],(15,24):None,(15,40):["w31"],(15,43):["w33"],
  (16,0):None,
  (17,11):["w10"],(17,18):["w16"],(17,21):None,(17,29):["w23"],(17,32):None,
  (18,7):["w7"],
  (19,0):["w2"],(19,9):["w9"],(19,12):None,(19,13):["w11"],(19,20):["w15"],(19,21):["w16"],(19,31):["w24"],(19,32):["w25"],(19,33):["w26"],
  (20,0):["w2"],(20,2):["w1"],(20,4):["w3"],(20,11):["w9"],
  (21,0):["w3"],(21,10):["w11"],(21,15):["w10"],(21,16):["w15"],(21,22):["w19"],
  (22,0):["w2"],(22,2):["w1"],(22,10):["w9"],(22,12):["w10"],(22,14):["w13"],(22,16):["w15"],(22,21):["w20"],(22,22):["w21"],(22,24):["w23"],(22,26):["w25"],
  (23,0):["w2"],(23,2):["w1"],(23,7):["w6"],(23,11):["w11"],(23,17):None,(23,20):["w19"],(23,28):["w27"],(23,29):["w29"],(23,31):["w30"],
  (24,12):["w6"],(24,13):["w6"],(24,14):["w6"],(24,15):["w6"],(24,18):["w12"],(24,19):["w12"],
  (25,0):["w2"],(25,1):["w1"],(25,4):["w4"],(25,13):None,
  (27,0):["w2"],(27,10):None,(27,14):["w9"],(27,17):["w10"],(27,24):["w18"],(27,25):["w18"],(27,27):["w20"],(27,29):["w20"],
  (28,0):["w2"],(28,20):None,(28,22):None,
  (29,0):["w2"],(29,5):["w5"],
  (30,9):["w8"],(30,17):["w15"],(30,30):["w30"],
  (31,16):["w12"],(31,17):["w14"],(31,20):["w15"],(31,21):None,
  (32,2):["w2"],(32,3):["w5"],(32,7):["w9"],(32,10):["w10"],(32,14):["w11"],(32,25):["w20"],(32,28):["w27"],(32,32):["w25"],
  (33,14):["w12"],(33,17):["w13"],(33,18):None,
  (34,13):["w13"],
  (35,2):["w3"],(35,3):["w4"],(35,8):["w2"],
  (36,5):None,
  (37,12):None,
  (38,15):["w18"],(38,19):["w21"],
  (39,3):["w4"],(39,4):["w5"],(39,7):["w8"],(39,13):["w13"],(39,14):["w15"],(39,15):None,(39,18):["w17"],(39,19):["w19"],
  (40,1):None,(40,5):None,(40,9):None,(40,15):["w11"],(40,17):["w13"],
  (41,0):["w2"],(41,13):["w11"],(41,19):["w17"],(41,22):["w19"],
  (43,1):None,(43,6):None,(43,9):None,(43,16):["w14"],(43,17):["w15"],(43,19):["w18"],
  (44,16):None,(44,19):["w18"],(44,25):["w23"],
  (46,0):["w3"],(46,1):["w2"],(46,2):["w2"],(46,5):["w5"],(46,9):None,(46,13):["w11"],
  (47,16):None,
  (48,3):["w3"],(48,5):["w4"],(48,14):["w10"],(48,17):None,(48,19):["w14"],(48,20):["w16"],(48,24):["w19"],
  (49,4):["w3"],(49,6):["w5"],(49,17):["w17"],
  (51,0):["w5"],
  (52,0):["w2"],(52,5):["w5","w6"],(52,8):["w9"],(52,9):["w9"],(52,12):None,(52,22):None,(52,28):["w20"],(52,30):["w21"],
  (53,9):["w10"],
  (54,4):["w5"],(54,14):["w14"],(54,20):None,(54,23):None,(54,27):["w22"],(54,28):["w25"],(54,29):["w25"],
  (55,2):["w1"],(55,3):["w4"],(55,7):["w8"],
  (56,2):["w5"],(56,11):None,(56,14):None,
  (57,3):["w3"],(57,4):["w4"],(57,23):["w24"],(57,24):None,
},
26: {
  (14,10):["w2"],
  (18,29):None,
  (37,13):["w11"],
  (63,12):["w11"],
  (63,14):["w11"],
}
}

for ch, fixes in FIXES.items():
    p=Path(f"data/matthew/{ch:02}.json")
    d=json.loads(p.read_text())
    byv={v["v"]:v for v in d["verses"]}
    changed=0
    for (vn,idx),ids in fixes.items():
        t=byv[vn]["alignment"]["dgt"][idx]
        if ids is None:
            t["ids"]=[]
            t.pop("phraseIds",None)
            t["supplied"]=True
            t["confidence"]="reviewed-bilingual-supplied"
            t["reason"]="Matthew bilingual audit: supplied English required by idiomatic rendering"
        else:
            t["ids"]=ids
            t["phraseIds"]=ids
            t.pop("supplied",None)
            t["confidence"]="reviewed-bilingual-precise"
            t["reason"]="Matthew bilingual audit: narrowed to direct Greek correspondence"
        changed+=1
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
    print(f"Matthew {ch}: {changed} oversized-file mappings repaired")


# Add high-confidence Greek source IDs to already-correct English tokens.
EXTRA_ADD = {
  13: {(2,10): "w12"},
  26: {(2,17): "w15", (18,30): "w22"},
}
for ch, adds in EXTRA_ADD.items():
    p=Path(f"data/matthew/{ch:02}.json")
    d=json.loads(p.read_text())
    byv={v["v"]:v for v in d["verses"]}
    for (vn,idx),gid in adds.items():
        t=byv[vn]["alignment"]["dgt"][idx]
        ids=list(dict.fromkeys((t.get("ids") or [])+[gid]))
        t["ids"]=ids
        t["phraseIds"]=ids
        t.pop("supplied",None)
        t["confidence"]="reviewed-bilingual-precise"
        t["reason"]="Matthew Greek coverage audit: added directly represented Greek source token"
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
    print(f"Matthew {ch}: added {len(adds)} high-confidence Greek coverage IDs")


# FINAL_MATTHEW_26_CERTIFICATION
M26_FINAL = {
  (1,12): (["w14"], "Bilingual certification: 'his disciples' renders μαθηταῖς αὐτοῦ"),
  (4,4): (["w3"], "Bilingual certification: purpose 'to seize' renders ἵνα"),
  (6,3): (["w4"], "Bilingual certification: 'was' in 'when Jesus was' renders γενομένου"),
  (8,10): (["w8","w9"], "Bilingual certification: 'Why' renders Εἰς τί"),
  (9,2): (["w1"], "Bilingual certification: modal 'could' renders ἐδύνατο"),
  (10,22): (["w16"], "Bilingual certification: 'for me' renders εἰς ἐμέ"),
  (11,7): (["w7"], "Bilingual certification: 'with you' includes ἑαυτῶν"),
  (12,2): (["w3"], "Bilingual certification: 'she' renders αὕτη"),
  (12,4): (["w6"], "Bilingual certification: demonstrative 'this perfume' renders τοῦτο"),
  (13,14): (["w16"], "Bilingual certification: relative 'what' renders ὃ"),
  (13,15): (["w18"], "Bilingual certification: 'she/this woman' renders αὕτη"),
  (16,2): (["w3"], "Bilingual certification: 'then' renders τότε"),
  (18,7): (["w8"], "Bilingual certification: 'to a certain man' renders πρὸς"),
  (23,18): (["w14"], "Bilingual certification: resumptive 'one' renders οὗτος"),
  (24,30): (["w24"], "Bilingual certification: 'been' renders ἦν in 'would have been good'"),
  (24,32): (["w25"], "Bilingual certification: 'for' renders αὐτῷ"),
  (24,33): (["w31"], "Bilingual certification: 'that' renders ἐκεῖνος"),
  (24,34): (["w30"], "Bilingual certification: 'man' renders ἄνθρωπος"),
  (27,14): (["w11"], "Bilingual certification: 'from it' renders ἐξ αὐτοῦ"),
  (31,13): (["w11","w14"], "Bilingual certification: 'this night' carries ἐν ... ταύτῃ"),
  (34,9): (["w9","w10"], "Bilingual certification: 'this night' carries ἐν ταύτῃ"),
  (36,18): (["w17","w18"], "Bilingual certification: 'while' renders ἕως οὗ"),
  (38,10): (["w11"], "Bilingual certification: 'to ... death' renders ἕως"),
  (39,7): (["w5"], "Bilingual certification: 'on his face' renders ἐπὶ"),
  (39,8): (["w7"], "Bilingual certification: 'his face' renders πρόσωπον αὐτοῦ"),
  (39,29): (["w26"], "Bilingual certification: 'I will/wish' renders θέλω"),
  (42,15): (["w10","w11"], "Bilingual certification: 'cannot' jointly renders οὐ δύναται"),
  (43,11): (["w12"], "Bilingual certification: 'heavy' renders βεβαρημένοι"),
  (45,12): (["w12"], "Bilingual certification: 'still' carries λοιπὸν"),
  (47,4): (["w2"], "Bilingual certification: 'still' renders ἔτι"),
  (48,12): (["w9"], "Bilingual certification: 'one' in 'the one I kiss' renders Ὃν"),
  (52,8): (["w10"], "Bilingual certification: 'to its place' renders εἰς"),
  (55,24): (["w20"], "Bilingual certification: 'day after day' carries καθʼ"),
  (58,9): (["w8"], "Bilingual certification: 'as far as' renders ἕως"),
  (61,4): (["w3"], "Bilingual certification: second 'said' renders ἔφη, not εἶπαν"),
  (64,1): (["w1"], "Bilingual certification: Jesus 'said' renders λέγει"),
  (64,30): (["w24"], "Bilingual certification: 'on the clouds' renders ἐπὶ"),
  (65,10): (["w11"], "Bilingual certification: interrogative 'What/why' renders τί"),
}
p=Path("data/matthew/26.json")
d=json.loads(p.read_text())
byv={v["v"]:v for v in d["verses"]}
for (vn,idx),(ids,reason) in M26_FINAL.items():
    t=byv[vn]["alignment"]["dgt"][idx]
    t["ids"]=ids
    t["phraseIds"]=ids
    t.pop("supplied",None)
    t["confidence"]="reviewed-bilingual-precise" if len(ids)==1 else "reviewed-bilingual-semantic"
    t["reason"]=reason
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
print(f"Matthew 26: applied {len(M26_FINAL)} final certification repairs")


# FINAL_MATTHEW_13_CERTIFICATION
M13_FINAL = {
  (10,8): (["w7","w8"], "Bilingual certification: 'Why' renders Διὰ τί"),
  (15,20): (["w16"], "Bilingual certification: 'their eyes' renders ὀφθαλμοὺς αὐτῶν"),
  (20,2): (["w1","w7"], "Bilingual certification: English 'the one' carries resumptive οὗτός"),
  (22,2): (["w1","w7"], "Bilingual certification: English 'the one' carries resumptive οὗτός"),
  (23,2): (["w1","w9"], "Bilingual certification: English 'the one' carries resumptive οὗτός"),
  (25,12): (["w14","w15"], "Bilingual certification: 'among' renders ἀνὰ μέσον"),
  (28,6): (["w5","w6"], "Bilingual certification: 'enemy' compresses Ἐχθρὸς ἄνθρωπος"),
  (30,27): (["w25","w27"], "Bilingual certification: purpose 'to burn' carries πρὸς ... κατακαῦσαι"),
  (35,15): (["w14"], "Bilingual certification: 'my mouth' renders στόμα μου"),
  (36,2): (["w2"], "Bilingual certification: 'left the crowds' renders ἀφεὶς"),
  (38,8): (["w10","w11"], "Bilingual certification: 'good seed' carries resumptive οὗτοί"),
  (44,27): (["w25","w26"], "Bilingual certification: 'everything' carries πάντα ὅσα"),
  (45,8): (["w8","w9"], "Bilingual certification: 'a merchant/man' carries ἀνθρώπῳ ἐμπόρῳ"),
  (46,11): (["w9","w10"], "Bilingual certification: 'everything' carries πάντα ὅσα"),
  (48,24): (["w18","w19"], "Bilingual certification: 'away/out' carries ἔξω ἔβαλον"),
  (54,3): (["w6"], "Bilingual certification: 'his hometown' renders πατρίδα αὐτοῦ"),
}
p=Path("data/matthew/13.json")
d=json.loads(p.read_text())
byv={v["v"]:v for v in d["verses"]}
for (vn,idx),(ids,reason) in M13_FINAL.items():
    t=byv[vn]["alignment"]["dgt"][idx]
    t["ids"]=ids
    t["phraseIds"]=ids
    t.pop("supplied",None)
    t["confidence"]="reviewed-bilingual-precise" if len(ids)==1 else "reviewed-bilingual-semantic"
    t["reason"]=reason
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
print(f"Matthew 13: applied {len(M13_FINAL)} final certification repairs")
