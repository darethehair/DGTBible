import json,re,unicodedata,collections,os
from pathlib import Path
B=Path('data/john');bad=[];risk=[];linked=unlinked=0;START=int(os.environ.get('START_CHAPTER','4'));END=int(os.environ.get('END_CHAPTER','10'))
GEN=set('the a an of to and or in on at for with from by that this one he she it they we you i me him her his their our your my is was were be been being has have had do did does not no are am will would should could may might can so but'.split())
def n(s):
 s=unicodedata.normalize('NFD',str(s)).lower();s=''.join(x for x in s if unicodedata.category(x)!='Mn');return re.sub(r'[^a-z0-9 ]',' ',s).strip()
def rec(a):return ''.join(x.get('text','')+x.get('after','') for x in a)
count=0
for ch in range(START,END+1):
 d=json.loads((B/f'{ch:02}.json').read_text(encoding='utf8'));prev=0
 for v in d['verses']:
  count+=1;ref=f'John {ch}:{v["v"]}'
  if v['v']<=prev:bad.append(ref+' verse order');prev=v['v']
  for L,F in [('greek','greek'),('literal','literal'),('dgt','dgt')]:
   if rec(v['alignment'][L])!=v[F]:bad.append(ref+' '+L+' reconstruction')
  ids=set()
  for x in v['alignment']['greek']:
   for i in x['ids']:
    if i in ids:bad.append(ref+' duplicate Greek '+i)
    ids.add(i)
  for L in ['translit','literal','dgt']:
   for x in v['alignment'][L]:
    if L=='dgt':
     if len(x['ids'])>2:bad.append(ref+' oversized DGT mapping')
     if not x['ids']:
      unlinked+=1
      if x.get('confidence')!='unlinked' or not x.get('reason'):bad.append(ref+' unsafe empty DGT mapping')
     else:linked+=1
    elif not x['ids']:bad.append(ref+' empty '+L+' mapping')
    for i in x['ids']:
     if i not in ids:bad.append(ref+' orphan '+L+' '+i)
  g={i:x for x in v['alignment']['greek'] for i in x['ids']};p=collections.defaultdict(list);items=v['alignment']['dgt']
  for j,x in enumerate(items):
   for i in x['ids']:p[i].append(j)
  for i,ps in p.items():
   sep=any(ps[k]!=ps[k-1]+1 for k in range(1,len(ps)))
   phrase=' '.join(items[j]['text'] for j in ps);pw=[w for w in n(phrase).split() if w not in GEN];gw=[w for w in n(g[i].get('gloss','')).split() if w not in GEN]
   if sep and gw and pw and not any(w in gw for w in pw):risk.append((ref,i,phrase))
expected=sum(1 for ch in range(START,END+1) for _ in json.loads((B/f'{ch:02}.json').read_text(encoding='utf8'))['verses'])
if count!=expected:bad.append(f'expected {expected} verses, got {count}')
pct=linked/(linked+unlinked)*100
if pct<80:bad.append(f'link coverage {pct:.1f}% below 80%')
if risk:bad.extend(f'{r}: high-risk {i} -> {p}' for r,i,p in risk)
if bad:
 print('Batch audit failed:');[print(' - '+x) for x in bad];raise SystemExit(1)
print(f'Batch audit passed for John {START}-{END}: {count} verses, {pct:.1f}% high-confidence DGT token coverage, {unlinked} safe unlinked tokens, zero high-risk mappings.')
