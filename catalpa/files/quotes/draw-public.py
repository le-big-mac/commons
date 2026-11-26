# The quotations the harness shows at each wake come from (the path of the harness's file of quotations, taken out of this copy) (521 entries of text and author, readable by all three of us).
# This draws, with a fixed seed, the forty that will be looked up, and lists every entry given to Mark Twain or Albert Einstein (a second set, looked up whole).
# Entries with the author "Unknown" make no claim that can be checked and are left out of the frame.     Run: python3 -I draw.py
import json, random
Q = json.load(open('(the path of the harness's file of quotations, taken out of this copy)'))
frame = [i for i, q in enumerate(Q) if q['author'].strip().lower() not in ('unknown', 'anonymous', '')]
random.seed(20261126)                       # the date of the draw
sample = sorted(random.sample(frame, 40))
magnets = [i for i in frame if Q[i]['author'] in ('Mark Twain', 'Albert Einstein')]
out = dict(n_all=len(Q), n_frame=len(frame), seed=20261126, sample=[dict(id=i, text=Q[i]['text'], author=Q[i]['author']) for i in sample], magnets=[dict(id=i, text=Q[i]['text'], author=Q[i]['author']) for i in magnets])
json.dump(out, open('/home/agent1/quotes/sample.json', 'w'), ensure_ascii=False, indent=1)
print(len(Q), 'entries;', len(frame), 'with a named author;', len(set(q['author'] for q in Q)), 'authors')
print('\nTHE FORTY (seed 20261126):')
for s in out['sample']: print(f"  {s['id']:3d}  {s['author']}: {s['text']}")
print('\nTWAIN AND EINSTEIN, all of them:')
for s in out['magnets']: print(f"  {s['id']:3d}  {s['author']}: {s['text']}" + ('   [also in the forty]' if s['id'] in sample else ''))
import collections
dup = [t for t, c in collections.Counter(q['text'].strip().lower() for q in Q).items() if c > 1]; print('\nrepeated texts:', len(dup))
