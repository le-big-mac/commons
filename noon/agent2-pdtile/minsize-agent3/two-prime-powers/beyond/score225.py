"""Score the sheet expectations-z225.md from out225/z225-*.jsonl.  Written before the run.   usage: score225.py"""
import json, glob, collections
P = json.load(open('predictions-225.json'))
R = {}
for f in sorted(glob.glob('out225/z225-*.jsonl')):
    for l in open(f):
        if l.startswith('{'): r = json.loads(l); R[','.join(map(str, r['D']))] = r
M = 225
print(len(R), 'of', len(P), 'patterns run;', collections.Counter(r['status'] for r in R.values()))
bad = [k for k, r in R.items() if r['exact_pattern_ok'] is False]; print('multisets failing the exact check:', bad)
dec = {k: r for k, r in R.items() if r['status'] == 'optimal'}           # decided: least size proved
# an 'infeasible' with a prediction as upper bound decides only that the least size is above the prediction
above = [k for k, r in R.items() if r['status'] == 'infeasible' and r['predicted'] is not None]
def ep(D): return len(set(D) & {3, 9}), len(set(D) & {5, 25})
divs = [d for d in range(1, M + 1) if M % d == 0]
def lbP(D):
    U = [d for d in D if all(e in D for e in divs if e % d == 0)]; comp = [c for c in divs if c not in U]
    return sum(M // c for c in comp if not any(e != c and e % c == 0 for e in comp))
def is_up(D): return all(e in D for d in D for e in divs if e % d == 0)
w0 = []
for k, r in dec.items():
    D = r['D']; a, b = ep(D)
    if r['size'] % (3 ** a * 5 ** b): w0.append((k, 'divisibility'))
    if r['size'] < lbP(D): w0.append((k, 'below Corollary P'))
    if r['size'] == lbP(D) and not is_up(D): w0.append((k, 'non-up-set at the bound'))
    if P[k]['cls'].startswith('theorem') and r['size'] != P[k]['predicted']: w0.append((k, 'theorem', r['size'], P[k]['predicted']))
w0 += [(k, 'theorem value infeasible') for k in above if P[k]['cls'].startswith('theorem')]
print('W0 (checks) failures:', w0)
for cls in ('theorem-upset', 'theorem-m1'):
    ks = [k for k in P if P[k]['cls'] == cls]; print(f'   {cls}: {len(ks)} patterns, decided {sum(1 for k in ks if k in dec)}, equal {sum(1 for k in ks if k in dec and dec[k]["size"] == P[k]["predicted"])}')
print(f'W1: decided {len(dec)} of 256 (expected: at least 128)  ->', len(dec) >= 128)
fit = [k for k in P if P[k]['cls'] == 'fit']
fd = [k for k in fit if k in dec]; fa = [k for k in fit if k in above]
eq = [k for k in fd if dec[k]['size'] == P[k]['predicted']]
settled = len(fd) + len(fa)                                               # for a fit pattern, 'above the prediction' also settles that the prediction is wrong
print(f'W2/W3: fit patterns {len(fit)}; settled {settled} (least size proved {len(fd)}, proved above the prediction {len(fa)}); equal to the prediction {len(eq)}'
      f' = {100 * len(eq) / max(settled, 1):.1f}% of the settled  -> W2 (at least 90%):', len(eq) >= 0.9 * settled, '; W3 (all):', len(eq) == settled)
print('   fit patterns below the prediction:', [(P[k]['S'], P[k]['how'], P[k]['predicted'], dec[k]['size']) for k in fd if dec[k]['size'] < P[k]['predicted']])
print('   fit patterns above the prediction:', [(P[k]['S'], P[k]['how'], P[k]['predicted']) for k in fa])
show = lambda S: ' '.join(f'{u}{v}' for u, v in S)
W4 = [('01 02 21', 25), ('10 12 20', 18), ('01 12 20', 75), ('02 10 21', 90), ('02 11 20', 105), ('02 11 20', 90), ('01 02 20 22', 150), ('02 10 20 22', 90),
      ('01 02 10 12 21 22', 225), ('01 10 12 20 21 22', 225), ('12 21', 30), ('11 22', 30), ('02 20 22', 30)]
byS = {show(o['S']): k for k, o in P.items()}
for S, val in W4:
    k = byS[S]; r = R.get(k)
    print(f'W4/W5: {S}: expected {val}; run: {None if r is None else (r["status"], r["size"])}')
print('the patterns with no prediction that were decided:', [(show(P[k]['S']), P[k]['values_23_32_25_52'], dec[k]['size']) for k in P if P[k]['cls'] == 'none' and k in dec])
vals = collections.Counter(r['size'] for r in dec.values()); print('distinct decided values:', len(vals), sorted(vals.items()))
