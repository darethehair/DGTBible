#!/usr/bin/env python3
import json,re,collections
from pathlib import Path
from alignment_repair import norm,sim,semantic_terms,source_map

# Explicit reviewed mappings are added here as the Acts hover-review queue is
# inspected.  They intentionally fail fast when a later wording change makes
# a reviewed target disappear.
REVIEWED_PRECISION={
 (5,40):[
  ('and',1,['w1']),('after',1,['w2']),('calling',1,['w2']),('the',1,['w3']),('apostles',1,['w4']),
  ('they',1,['w5']),('beat',1,['w5']),('them',1,['w5']),
  ('commanded',1,['w6']),('them',2,['w6']),('not',1,['w7']),('to',1,['w8']),('speak',1,['w8']),
  ('in',2,['w9']),('the',2,['w10']),('name',1,['w11']),('of',1,['w12']),('jesus',1,['w13']),
  ('and',3,['w14']),('released',1,['w15']),('them',3,['w15']),
 ],
 (7,2):[
  ('he',1,['w3']),('said',1,['w3']),('he',2,['w18']),('was',1,['w18']),
  ('he',3,['w25']),('lived',1,['w24']),
 ],
 (8,33):[
  ('was',1,['w8']),('taken',1,['w8']),('away',1,['w8']),
  ('taken',2,['w16']),('away',2,['w16']),
 ],
 (16,34):[
  ('and',1,['w2']),('his',2,['w12']),('whole',1,['w12']),('household',1,['w12']),
  ('he',1,['w8']),('set',1,['w8']),('he',2,['w11']),('rejoiced',1,['w11']),
 ],
 (16,38):[
  ('the',1,['w5']),('officers',1,['w6']),('they',1,['w11']),('became',1,['w11']),('afraid',1,['w11']),
  ('they',2,['w13']),('heard',1,['w13']),('they',3,['w16']),('were',1,['w16']),('romans',1,['w15']),
 ],
 (20,10):[('his',1,['w15'])],
 (21,20):[
  ('they',1,['w3']),('heard',1,['w3']),('they',2,['w4']),('began',1,['w4']),('glorifying',1,['w4']),
  ('and',1,['w8']),('they',3,['w7']),('said',1,['w7']),
  ('and',2,['w20']),('they',4,['w25']),('are',2,['w25']),('all',1,['w21']),
 ],
 (23,24):[
  ('they',1,['w5']),('may',1,['w5']),('put',1,['w5']),('paul',1,['w7']),
  ('on',1,['w5']),('them',1,['w5']),('bring',1,['w8']),('him',1,['w8']),('safely',1,['w8']),
 ],
 (26,16):[
  ('and',1,['w3']),('and',2,['w17']),('and',3,['w24']),
  ('things',1,['w19']),('in',1,['w19']),('which',1,['w19']),
  ('things',2,['w23']),('in',2,['w23']),('which',2,['w23']),
 ],
 (27,7):[
  ('we',1,['w5']),('sailed',1,['w5']),('slowly',1,['w5']),
  ('we',2,['w17']),('sailed',2,['w17']),('under',1,['w17']),
 ],
 (27,21):[
  ('and',1,['w2']),('and',4,['w25']),('and',5,['w29']),
 ],
 (7,47):[('but',1,['w2']),('solomon',1,['w1']),('built',1,['w3']),('for',1,['w4']),('him',1,['w4']),('house',1,['w5'])],
 (7,50):[('did',1,['w5']),('not',1,['w1']),('make',1,['w5'])],
 (11,4):[('but',1,['w2']),('began',1,['w1']),('peter',1,['w4']),('explained',1,['w5']),('it',1,['w5']),('to',1,['w6']),('them',1,['w6']),('saying',1,['w8'])],
 (11,25):[('search',1,['w7']),('for',1,['w7']),('saul',1,['w8'])],
 (13,39):[('in',1,['w12']),('this',1,['w13']),('one',1,['w13']),('everyone',1,['w14']),('who',1,['w15']),('believes',1,['w16']),('is',1,['w17']),('justified',1,['w17'])],
 (15,31):[('and',1,['w2']),('when',1,['w1']),('they',1,['w1']),('read',1,['w1']),('it',1,['w1']),('rejoiced',1,['w3'])],
 (16,8):[('so',1,['w2']),('passing',1,['w1']),('by',1,['w1']),('mysia',1,['w4'])],
 (18,16):[('away',1,['w2'])],
 (20,5):[('on',1,['w3']),('and',1,['w2']),('waiting',1,['w4']),('for',1,['w4'])],
 (21,9):[('had',1,['w3']),('who',1,['w7']),('prophesied',1,['w7'])],
 (21,22):[('to',1,['w3']),('be',1,['w3']),('done',1,['w3'])],
 (23,25):[('he',1,['w1']),('wrote',1,['w1'])],
 (27,26):[('but',1,['w3']),('we',1,['w6']),('must',1,['w5']),('run',1,['w7']),('aground',1,['w7']),('on',1,['w1']),('some',1,['w4']),('island',1,['w2'])],
 (28,12):[('after',1,['w2']),('landing',1,['w2'])],
 (1,2):[('he',1,['w12']),('was',1,['w12']),('taken',1,['w12']),('up',1,['w12']),('he',2,['w11']),('had',1,['w11']),('chosen',1,['w11'])],
 (2,18):[('i',1,['w16']),('will',1,['w16']),('pour',1,['w16']),('out',1,['w16']),('my',2,['w20'])],
 (2,39):[('for',1,['w2']),('for',2,['w1']),('for',3,['w7']),('for',4,['w11'])],
 (3,2):[('to',1,['w12']),('to',2,['w24']),('ask',1,['w24']),('for',1,['w24'])],
 (3,6):[('i',1,['w9']),('have',1,['w8']),('i',2,['w12']),('have',2,['w12'])],
 (4,9):[('to',1,['w7']),('man',1,['w7']),('man',2,['w11'])],
 (4,24):[('one',1,['w4']),('one',2,['w14'])],
 (5,4):[
  ('did',1,['w4']),('did',2,['w14']),('you',1,['w14']),('did',3,['w23']),
  ('not',1,['w1']),('not',2,['w1']),('not',3,['w22'])
 ],
 (5,10):[
  ('they',1,['w14']),('her',2,['w15']),('her',3,['w18']),('buried',1,['w19']),('her',4,['w19'])
 ],
 (5,39):[('you',1,['w7']),('you',2,['w13']),('will',1,['w7']),('be',1,['w7']),('able',1,['w7']),('be',2,['w13']),('found',1,['w13'])],
 (6,1):[('were',1,['w6']),('were',2,['w17']),('being',1,['w17']),('overlooked',1,['w17'])],
 (7,57):[('with',1,['w3']),('with',2,['w11']),('one',1,['w11']),('accord',1,['w11'])],
 (9,19):[('he',1,['w4']),('was',1,['w4']),('he',2,['w5']),('was',2,['w5'])],
 (9,40):[('up',1,['w19']),('she',2,['w30']),('sat',1,['w30']),('up',2,['w30'])],
 (10,23):[('and',2,['w6']),('and',4,['w14'])],
 (10,31):[('has',1,['w4']),('been',1,['w4']),('heard',1,['w4']),('have',1,['w12']),('been',2,['w12']),('remembered',1,['w12'])],
 (10,45):[('had',1,['w8']),('come',1,['w8']),('with',1,['w8']),('had',2,['w22']),('been',1,['w22']),('poured',1,['w22']),('out',1,['w22'])],
 (11,9):[('a',1,['w4']),('a',2,['w6']),('second',1,['w6']),('time',1,['w6'])],
 (12,9):[('he',1,['w3']),('followed',1,['w3']),('he',2,['w7']),('did',1,['w7']),('not',1,['w6']),('know',1,['w7']),('was',1,['w10'])],
 (13,21):[('they',1,['w2']),('asked',1,['w2']),('for',1,['w2'])],
 (13,36):[('his',1,['w4']),('own',1,['w4']),('his',2,['w17'])],
 (14,23):[('entrusted',1,['w10']),('they',2,['w16']),('had',1,['w16']),('believed',1,['w16'])],
 (1,3):[('to',1,['w1']),('them',1,['w1']),('to',2,['w17']),('them',2,['w17'])],
 (1,11):[('looking',1,['s8']),('you',3,['w26']),('saw',1,['w26'])],
 (2,12):[('they',1,['w1','w5']),('were',1,['w1','w5']),('astonished',1,['w1']),('perplexed',1,['w5'])],
 (2,23):[('by',1,['w2']),('the',1,['w2']),('by',2,['w14']),('of',1,['w8']),('god',1,['w8']),('of',2,['w13'])],
 (2,27):[('to',1,['w7']),('to',2,['w14']),('see',1,['w14'])],
 (3,10):[('to',1,['w11']),('to',2,['w26']),('him',2,['w26'])],
 (3,12):[('do',1,['w12']),('do',2,['w18']),('made',1,['w24'])],
 (3,15):[('of',1,['w5']),('life',1,['w5']),('of',2,['w13'])],
 (4,14):[('had',1,['w9']),('they',1,['w11']),('had',2,['w11'])],
 (4,32):[('was',1,['w6']),('was',2,['w20']),('was',3,['w22'])],
 (4,34):[('there',1,['w5']),('was',1,['w5']),('was',2,['w20'])],
 (5,2):[('he',1,['w2']),('kept',1,['w2']),('back',1,['w2']),('part',1,['w2']),('a',1,['w13']),('part',2,['w13'])],
 (5,13):[('of',1,['w1']),('the',1,['w1']),('of',2,['w10'])],
 (5,31):[('to',1,['w8']),('to',2,['w12']),('give',1,['w12'])],
 (5,33):[('they',1,['w3']),('heard',1,['w3']),('they',2,['w4']),('were',1,['w4']),('cut',1,['w4'])],
 (5,36):[('was',1,['w9']),('was',2,['w19']),('killed',1,['w19'])],
 (7,25):[('he',1,['w1']),('thought',1,['w1']),('was',1,['w13'])],
 (7,54):[('they',1,['w1']),('heard',1,['w1']),('they',2,['w4']),('were',1,['w4']),('cut',1,['w4'])],
 (8,1):[('and',1,['w2']),('and',2,['w23']),('and',3,['w30'])],
 (8,10):[('of',2,['w14']),('god',1,['w14'])],
 (8,40):[('he',1,['w8']),('was',1,['w8']),('he',2,['w15']),('came',1,['w14'])],
 (9,4):[('to',1,['w3']),('to',2,['w9']),('him',1,['w9'])],
 (9,18):[('his',1,['w4']),('he',1,['w10']),('saw',1,['w10']),('he',2,['w14'])],
 (9,26):[('he',1,['w1']),('arrived',1,['w1']),('he',2,['w7']),('tried',1,['w7']),('he',3,['w18']),('was',1,['w18'])],
 (10,12):[('of',2,['w13']),('of',3,['w18'])],
 (10,15):[('a',1,['w2']),('voice',1,['w2']),('a',2,['w5'])],
 (10,22):[('they',1,['w3']),('said',1,['w3']),('spoken',1,['w12'])],
 (10,26):[('raised',1,['w4']),('up',1,['w4']),('stand',1,['w7']),('up',2,['w7'])],
 (12,5):[('being',1,['w5']),('being',2,['w13']),('made',1,['w13'])],
 (12,8):[('on',1,['w9']),('your',1,['w12']),('put',1,['w19'])],
 (12,20):[('who',1,['w17']),('was',1,['w17']),('was',2,['w27'])],
 (13,6):[('they',1,['w1']),('they',2,['w8']),('found',1,['w8'])],
 (13,14):[('on',2,['w17']),('the',2,['w17'])],
 (13,38):[('be',1,['w3']),('be',2,['s23']),('of',1,['w12']),('of',2,['s22'])],
 (14,6):[('of',2,['w7']),('lycaonia',1,['w7'])],
 (14,9):[('to',1,['w4']),('to',2,['w15']),('be',1,['w15'])],
 (15,7):[('and',1,['w2']),('and',4,['w34'])],
 (16,10):[('had',1,['w5']),('had',2,['w14'])],
 (17,25):[('is',1,['w5']),('he',1,['w5']),('served',1,['w5']),('he',2,['w8'])],
 (18,17):[('of',1,['w15'])],
 (18,19):[('and',1,['w2']),('and',2,['w5']),('them',1,['w5'])],
 (18,22):[('he',1,['w5']),('went',1,['w5']),('went',2,['w10']),('down',1,['w10'])],
 (19,28):[('they',1,['w1']),('heard',1,['w1']),('they',2,['w7']),('crying',1,['w7']),('out',1,['w7'])],
 (20,9):[('was',1,['w10']),('was',2,['w28']),('picked',1,['w28']),('up',1,['w28'])],
 (20,11):[('going',1,['w1']),('he',1,['w12']),('talked',1,['w12']),('he',2,['w16']),('departed',1,['w16'])],
 (21,5):[('we',1,['w4']),('we',2,['w8']),('we',4,['w28']),('prayed',1,['w28']),('our',1,['w9'])],
 (21,37):[('was',1,['w1']),('he',1,['w9']),('said',1,['w9']),('he',2,['w21']),('said',2,['w21'])],
 (22,28):[('with',1,['w6']),('a',1,['w6']),('large',1,['w6'])],
 (23,14):[('we',1,['w10']),('have',1,['w10']),('bound',1,['w10']),('have',2,['w16']),('killed',1,['w16'])],
 (23,21):[
  ('for',2,['w8']),('him',2,['w8']),('for',3,['w29']),
  ('are',1,['w6']),('they',1,['w14']),('they',2,['w23']),('they',3,['w27']),('are',2,['w27'])
 ],
 (26,2):[('i',1,['w4']),('am',1,['w4']),('accused',1,['w4']),('am',2,['w14'])],
 (27,17):[('they',1,['w4']),('used',1,['w4']),('they',3,['w19']),('were',1,['w19']),('driven',1,['w19']),('along',1,['w19'])],
 (28,10):[('they',1,['w5']),('honored',1,['w5']),('they',2,['w9']),('put',1,['w9']),('on',1,['w9'])],
 (28,19):[('i',1,['w5']),('was',1,['w5']),('compelled',1,['w5']),('i',2,['w13'])],
 (15,29):[('you',1,['w11']),('keep',1,['w11']),('yourselves',1,['w12']),('you',2,['w14']),('will',1,['w14']),('do',1,['w14'])],
 (15,38):[('take',1,['w18']),('along',1,['w18']),('to',2,['w14'])],
 (16,9):[('to',1,['w7']),('paul',1,['w7']),('to',2,['w20'])],
 (19,1):[('it',1,['w1']),('happened',1,['w1']),('came',1,['s15'])],
 (19,2):[('he',1,['w1']),('said',1,['w1']),('you',1,['w8']),('you',2,['w9'])],
 (19,15):[('i',1,['w12']),('know',1,['w12']),('i',2,['w16']),('recognize',1,['w16'])],
 (20,13):[('went',1,['w3']),('to',4,['w22']),('go',1,['w22'])],
 (21,14):[('be',1,['w2']),('be',2,['w11']),('done',1,['w11'])],
 (21,29):[('had',1,['w3']),('had',2,['w18']),('brought',1,['w18'])],
 (23,20):[
  ('to',1,['w8']),('ask',1,['w8']),
  ('to',2,['w14']),('bring',1,['w14']),('down',1,['w14']),
  ('to',3,['w15']),('to',4,['w22']),('inquire',1,['w22'])
 ],
 (24,10):[('a',1,['w15'])],
 (25,22):[('he',1,['w16']),('said',2,['w16']),('hear',1,['w12']),('you',1,['w17']),('will',1,['w17']),('hear',2,['w17'])],
 (25,26):[
  ('to',1,['w5']),('write',1,['w5']),
  ('to',2,['w7']),('my',1,['w7']),('lord',1,['w7']),
  ('to',3,['w27']),('write',2,['w27'])
 ],
 (26,28):[('a',1,['w9']),('you',1,['w11']),('persuading',1,['w11']),('to',2,['w13']),('a',2,['w12']),('christian',1,['w12'])],
 (27,11):[('was',1,['w10']),('persuaded',1,['w10']),('was',2,['w16']),('saying',1,['w16'])],
 (27,15):[('and',1,['w2']),('and',2,['w5'])],
 (27,6):[('and',1,['w1']),('there',1,['w1'])],
 (28,13):[('came',1,['w3']),('and',2,['w6']),('we',2,['w13']),('came',2,['w13'])],
}
REVIEWED_SUPPLIED={
 (8,10):[('them',1)],
 (16,34):[('his',1)],
 (27,21):[('and',2),('and',3)],
 (7,47):[('a',1)],
 (11,4):[('and',1)],
 (23,25):[('and',1)],
 (10,23):[('and',1),('and',3)],
 (13,21):[('for',2)],
 (4,16):[('it',1)],
 (5,2):[('his',1)],
 (7,25):[('his',1)],
 (8,10):[('of',1)],
 (10,10):[('food',1)],
 (10,12):[('of',1)],
 (13,14):[('on',1)],
 (14,6):[('of',1)],
 (15,7):[('and',2),('and',3)],
 (16,14):[('a',2)],
 (18,7):[('a',2)],
 (18,19):[('and',3)],
 (20,9):[('a',2),('a',3)],
 (21,5):[('we',3),('were',1)],
 (22,28):[('a',2),('citizen',1)],
 (23,21):[('for',1)],
 (28,10):[('we',2)],
 (15,29):[('if',1)],
 (19,2):[('said',2)],
 (25,22):[('said',1)],
 (27,15):[('and',3)],
 (27,6):[('and',2)],
 (28,13):[('and',1),('and',3)],
}
REVIEWED_SYNTHETICS={
 (1,11):[('s8','looking',1)],
 (1,15):[('s20','about',1)],
 (2,5):[('s3','in',1)],
 (3,19):[('s5','so',1)],
 (4,37):[('s10','at',1)],
 (5,19):[('s6','opened',1)],
 (5,26):[('s8','brought',1)],
 (7,34):[('s14','their',1)],
 (7,46):[('s12','god',2)],
 (9,21):[('s13','in',1)],
 (13,38):[
  ('s14','and',2),
  ('s15','from',1),
  ('s16','all',1),
  ('s17','which',1),
  ('s18','not',1),
  ('s19','you',3),('s19','could',1),
  ('s20','by',1),
  ('s21','law',1),
  ('s22','moses',1),
  ('s23','be',1),('s23','justified',1),
 ],
 (15,4):[('s4','jerusalem',1)],
 (16,11):[('s2','so',1)],
 (18,23):[('s13','strengthening',1)],
 (19,1):[('s15','came',1)],
 (19,40):[
  ('s22','and',1),
  ('s23','these',1),
  ('s24','saying',1),
  ('s25','dismissed',1),
  ('s26','assembly',1),('s27','assembly',1),
 ],
 (20,6):[('s21','where',1)],
 (23,7):[('s4','said',1)],
 (23,17):[('s12','bring',1)],
 (23,18):[('s20','young',1),('s20','man',1)],
 (26,1):[('s9','for',1)],
 (28,23):[('s5','came',1)],
}

FAMILIES=[
 {'must','necessary','behooves','behoove','ought','needs','need','needed'},
 {'generation','generations'},
 {'humble','humbles','humbled','humbling','lowly'},
 {'assembly','assemblies','church','churches','congregation','congregations'},
 {'servant','servants','slave','slaves','minister','ministers'},
 {'announce','announces','announced','proclaim','proclaims','proclaimed','preach','preached'},
 {'rise','rises','rose','risen','raise','raises','raised','arise','arose','arisen'},
 {'send','sends','sent','sending'},
 {'answer','answered','reply','replied'},
 {'say','says','said','saying','speak','speaks','spoke','spoken','speaking'},
 {'see','sees','saw','seen','look','looks','looked','looking'},
 {'receive','receives','received','take','takes','took','taken'},
 {'go','goes','went','gone','going','depart','departed','leave','left'},
 {'come','comes','came','coming','arrive','arrived','approach','approached'},
 {'believe','believes','believed','faith','faithful'},
 {'save','saves','saved','salvation'},
]

def atoms(s):
 return [norm(t) for t in re.findall(r"[A-Za-z0-9]+",str(s)) if norm(t)]

def fkey(w):
 w=norm(w)
 for i,g in enumerate(FAMILIES):
  if w in g:return i
 return None

def fscore(a,b):
 a=norm(a);b=norm(b);z=sim(a,b)
 ka,kb=fkey(a),fkey(b)
 if ka is not None and ka==kb:z=max(z,12)
 return z

def target(D,word,occ,ref):
 matches=[x for x in D if norm(x.get('text',''))==norm(word)]
 if occ<1 or occ>len(matches):
  raise SystemExit(f'{ref}: reviewed target {word!r} occurrence {occ} not found')
 return matches[occ-1]

def apply_reviewed(D,G,ch,vn):
 ref=f'Acts {ch}:{vn}';changes=0
 source={id for g in G for id in g.get('ids',[])}
 for word,occ,ids in REVIEWED_PRECISION.get((ch,vn),[]):
  x=target(D,word,occ,ref)
  for id in ids:
   if id not in source:raise SystemExit(f'{ref}: reviewed precision unknown source {id}')
  if x.get('ids')!=ids or x.get('phraseIds')!=ids:
   x['ids']=ids[:];x['phraseIds']=ids[:];x['confidence']='acts-reviewed-precision'
   x.pop('supplied',None);x.pop('reason',None);changes+=1
 for word,occ in REVIEWED_SUPPLIED.get((ch,vn),[]):
  x=target(D,word,occ,ref)
  if x.get('ids') or x.get('phraseIds') or not x.get('supplied'):
   x['ids']=[];x['phraseIds']=[];x['supplied']=True
   x['confidence']='acts-reviewed-supplied'
   x['reason']='English supplied for natural rendering; no separate Greek token'
   changes+=1
 for sid,word,occ in REVIEWED_SYNTHETICS.get((ch,vn),[]):
  if sid not in source:raise SystemExit(f'{ref}: reviewed synthetic {sid} missing')
  x=target(D,word,occ,ref)
  ids=list(dict.fromkeys(x.get('ids',[])+[sid]))
  if x.get('ids')!=ids:
   x['ids']=ids;x['phraseIds']=list(dict.fromkeys(x.get('phraseIds',[])+[sid]))
   x['confidence']='acts-reviewed-synthetic';x.pop('reason',None);changes+=1
 return changes


def reconcile_repeated_exact(D,L):
 # Repair a common auto-alignment failure: repeated English helper/content
 # words collapsing onto one source occurrence.  Only act when the literal
 # layer provides exactly the same number of source-linked exact occurrences,
 # making ordered pairing deterministic.  Explicit reviewed mappings win.
 byword=collections.defaultdict(list)
 for i,x in enumerate(D):
  if x.get('supplied'):continue
  w=norm(x.get('text',''))
  if w:byword[w].append(i)
 lids=collections.defaultdict(list)
 for y in L:
  for w in atoms(y.get('text','')):
   for id in y.get('ids',[]):
    if id not in lids[w]:lids[w].append(id)
 changes=0
 for w,idxs in byword.items():
  if len(idxs)<2:continue
  cand=lids.get(w,[])
  if len(cand)!=len(idxs):continue
  current=[tuple(D[i].get('ids',[])) for i in idxs]
  if all(cur==(cand[j],) for j,cur in enumerate(current)):continue
  # Never override an explicit reviewed decision.
  if any(str(D[i].get('confidence','')).startswith('acts-reviewed-') for i in idxs):continue
  # Only repair actual collapse/mis-order, not a purposeful multi-ID phrase.
  flat=[id for cur in current for id in cur]
  if len(set(flat))>=len(cand) and all(cur for cur in current):continue
  for j,i in enumerate(idxs):
   D[i]['ids']=[cand[j]];D[i]['phraseIds']=[cand[j]]
   D[i]['confidence']='acts-final-repeated-exact'
   D[i].pop('reason',None);changes+=1
 return changes


HELPERS=set('i you he she it we they me him her us them my your his our their mine yours hers ours theirs am is are was were be been being have has had do does did will would shall should may might can could must'.split())
SUPPLIED_GLUE=set('a an the and but or so for because since if then than as of to from in into on at by with through before after about against under over until when while where why how what whether though although toward'.split())

def reviewed_token(x):
 return str(x.get('confidence','')).startswith('acts-reviewed-')

def boundary_between(D,a,b):
 lo=min(a,b);hi=max(a,b)
 for k in range(lo,hi):
  t=str(D[k].get('text',''))
  if any(c in t for c in '.;:?!'):
   return True
 return False

def helper_verb_recover(D,G):
 # English subject pronouns and auxiliaries often unpack person/tense/voice
 # encoded inside one Greek verb.  Attach a still-unlinked helper only to a
 # nearby, already-precise verbal source ID inside its authored phrase span.
 # Never cross strong punctuation and never override reviewed decisions.
 byid={id:g for g in G for id in g.get('ids',[])}
 changes=0
 for i,x in enumerate(D):
  if x.get('ids') or x.get('supplied') or reviewed_token(x):continue
  w=norm(x.get('text',''))
  if w not in HELPERS:continue
  allowed=set(x.get('phraseIds',[]))
  cand=[]
  # Prefer the next verbal English token for subjects/auxiliaries, then prior.
  order=[1,2,3,-1,-2,-3]
  for off in order:
   j=i+off
   if not (0<=j<len(D)) or boundary_between(D,i,j):continue
   for id in D[j].get('ids',[]):
    if allowed and id not in allowed:continue
    g=byid.get(id,{})
    if str(g.get('morph','')).startswith('V-'):
     cand.append((abs(off),0 if off>0 else 1,id))
  if not cand:continue
  cand.sort()
  best=cand[0]
  # Require a unique nearest verbal ID; ambiguity stays for review.
  same=[c for c in cand if c[:2]==best[:2]]
  ids=list(dict.fromkeys(c[2] for c in same))
  if len(ids)!=1:continue
  id=ids[0]
  x['ids']=[id];x['phraseIds']=[id];x['confidence']='acts-final-helper-verb'
  x.pop('reason',None);changes+=1
 return changes

def mark_unresolved_glue_supplied(D):
 # If a pure English glue word still has no defensible precise source after
 # exact/family/helper recovery, leaving a 4-5-token hover is more misleading
 # than explicitly recording it as supplied English.  Content words are never
 # handled here.
 changes=0
 for x in D:
  if x.get('ids') or x.get('supplied') or reviewed_token(x):continue
  w=norm(x.get('text',''))
  if w in SUPPLIED_GLUE and len(x.get('phraseIds',[]))>=4:
   x['ids']=[];x['phraseIds']=[];x['supplied']=True
   x['confidence']='acts-final-supplied-glue'
   x['reason']='English connective/article/preposition supplied for natural rendering; no safe separate Greek hover target'
   changes+=1
 return changes

def exact_fixed_point(D,L):
 total=0
 while True:
  changed=0;byword=collections.defaultdict(list);used=collections.defaultdict(set)
  for i,x in enumerate(D):
   if x.get('supplied'):continue
   w=norm(x.get('text',''))
   if not w:continue
   if x.get('ids'):used[w].update(x.get('ids',[]))
   else:byword[w].append(i)
  lids=collections.defaultdict(list)
  for y in L:
   for w in atoms(y.get('text','')):
    for id in y.get('ids',[]):
     if id not in lids[w]:lids[w].append(id)
  for w,idxs in byword.items():
   allowed=set()
   for i in idxs:allowed.update(D[i].get('phraseIds',[]))
   cand=[id for id in lids.get(w,[]) if id not in used[w] and (not allowed or id in allowed)]
   if cand and len(cand)==len(idxs):
    for i,id in zip(idxs,cand):
     D[i]['ids']=[id];D[i]['phraseIds']=[id];D[i]['confidence']='acts-final-exact'
     D[i].pop('reason',None);used[w].add(id);changed+=1
  total+=changed
  if not changed:return total

def family_fixed_point(D,G):
 src,pos=source_map(G);total=0
 while True:
  changed=0;byfam=collections.defaultdict(list);used=collections.defaultdict(set)
  for i,x in enumerate(D):
   if x.get('supplied'):continue
   k=fkey(x.get('text',''))
   if k is None:continue
   if x.get('ids'):used[k].update(x.get('ids',[]))
   else:byfam[k].append(i)
  for k,idxs in byfam.items():
   allowed=set()
   for i in idxs:allowed.update(D[i].get('phraseIds',[]))
   cand=[]
   for id,g in src.items():
    if id in used[k] or (allowed and id not in allowed):continue
    if any(fkey(t)==k for t in semantic_terms(g,id,None)):cand.append(id)
   cand.sort(key=lambda id:pos.get(id,10**9))
   if cand and len(cand)==len(idxs):
    for i,id in zip(idxs,cand):
     D[i]['ids']=[id];D[i]['phraseIds']=[id];D[i]['confidence']='acts-final-family'
     D[i].pop('reason',None);used[k].add(id);changed+=1
  total+=changed
  if not changed:return total

changed=0
for path in sorted(Path('data/acts').glob('[0-9][0-9].json')):
 d=json.loads(path.read_text(encoding='utf8'));file_changed=0;ch=int(path.stem)
 for v in d.get('verses',[]):
  A=v.get('alignment',{});D=A.get('dgt',[]);G=A.get('greek',[]);L=A.get('literal',[])
  file_changed+=apply_reviewed(D,G,ch,v['v'])
  file_changed+=reconcile_repeated_exact(D,L)
  file_changed+=exact_fixed_point(D,L)
  file_changed+=family_fixed_point(D,G)
  file_changed+=helper_verb_recover(D,G)
  file_changed+=exact_fixed_point(D,L)
  file_changed+=mark_unresolved_glue_supplied(D)
 if file_changed:
  path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
  changed+=file_changed
print(f'Acts final deterministic/reviewed repairs: {changed}')
