"""Brier scores of the two Z_225 sheets, from out225/score225.txt and score225b.txt as written by the scoring programs, with the
odds as sealed.  A line is scored only if the run settles it.   usage: brier225.py"""
import json, glob
R = {}
for f in sorted(glob.glob('out225/z225-*.jsonl')):
    for l in open(f):
        if l.startswith('{'): r = json.loads(l); R[tuple(r['D'])] = r
P = json.load(open('predictions-225.json')); B = json.load(open('bounds-225.json'))
dec = {k: R[tuple(int(t) for t in k.split(',') if t)]['size'] for k in P if R[tuple(int(t) for t in k.split(',') if t)]['status'] == 'optimal'}
show = lambda S: ' '.join(f'{u}{v}' for u, v in S); byS = {show(o['S']): k for k, o in P.items()}
lines = []
lines.append(('W1 at least 128 decided', 0.7, len(dec) >= 128))
fit = [k for k in P if P[k]['cls'] == 'fit' and k in dec]
eq = sum(1 for k in fit if dec[k] == P[k]['predicted'])
lines.append(('W2 at least 90% of settled fit patterns as predicted', 0.6, eq >= 0.9 * len(fit)))
lines.append(('W3 every settled fit pattern as predicted', 0.12, eq == len(fit)))
for S, val, pr in [('01 02 21', 25, 0.6), ('10 12 20', 18, 0.6), ('01 12 20', 75, 0.5), ('02 10 21', 90, 0.5), ('02 11 20', 105, 0.35), ('02 11 20', 90, 0.35), ('01 02 20 22', 150, 0.4), ('02 10 20 22', 90, 0.4),
                   ('01 02 10 12 21 22', 225, 0.6), ('01 10 12 20 21 22', 225, 0.6), ('12 21', 30, 0.45), ('11 22', 30, 0.6), ('02 20 22', 30, 0.6)]:
    k = byS[S]
    if k in dec: lines.append((f'W4/W5 {{{S}}} is {val}', pr, dec[k] == val))
    else: lines.append((f'W4/W5 {{{S}}} is {val}', pr, None))
def brier(ls):
    s = [(p - (1 if o else 0)) ** 2 for _, p, o in ls if o is not None]; return sum(s) / len(s), len(s)
print('FIRST SHEET')
for name, p, o in lines: print(f'  {name}: odds {p}; ' + ('not settled by the run' if o is None else 'held' if o else 'did not hold'))
b, n = brier(lines); print(f'  Brier score over the {n} lines the run settled: {b:.3f}  (0.25 is what saying one half every time gets)')
l2 = []
eqU = sum(1 for k, v in dec.items() if v == B[k]['U'])
l2.append(('V1 at least 85% of decided have least = U', 0.7, eqU >= 0.85 * len(dec)))
none = [k for k in dec if P[k]['cls'] == 'none']
l2.append(('V2 at least half of the decided no-prediction patterns have least = U', 0.5, 2 * sum(1 for k in none if dec[k] == B[k]['U']) >= len(none)))
l2.append(('V3 at least 10 decided with least < U', 0.75, sum(1 for k, v in dec.items() if v < B[k]['U']) >= 10))
print('SECOND SHEET')
for name, p, o in l2: print(f'  {name}: odds {p}; ' + ('held' if o else 'did not hold'))
b, n = brier(l2); print(f'  Brier score over the {n} lines: {b:.3f}')
