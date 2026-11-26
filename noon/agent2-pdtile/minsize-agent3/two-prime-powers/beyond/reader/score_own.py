"""Reader's scoring of the two Z_225 sheets against the sheets' own words, from out225/z225-*.jsonl, predictions-225.json (sealed with
the first sheet), bounds-225.json (sealed with the second) and the reader's own LB / U3.  The odds are typed here from the sheets.
usage: score_own.py"""
import json, glob, itertools, collections, sys
sys.path.insert(0, '/home/agent3/pq2/rule/reader')
from bounds_own import theorem1, LB as myLB
R = '/home/agent3/pq2/rule/'
P = json.load(open(R + 'predictions-225.json')); B = json.load(open(R + 'bounds-225.json'))
OB = json.load(open(R + 'reader/own-bounds-2.json'))
runs = collections.defaultdict(list)
for f in sorted(glob.glob(R + 'out225/z225-*.jsonl')):
    for l in open(f):
        if l.startswith('{'):
            r = json.loads(l); runs[','.join(map(str, r['D']))].append((f.split('/')[-1], r))
assert set(runs) == set(P) and len(P) == 256
last = {k: v[-1][1] for k, v in runs.items()}
p, q, M = 3, 5, 225
show = lambda S: ' '.join(f'{u}{v}' for u, v in sorted(map(tuple, S)))

# --- the predictions file against the run's own record of what it was given, and against my own classification
mism = [k for k, v in runs.items() for f, r in v if 'predicted' in r and (r['predicted'] != P[k]['predicted'] or r.get('cls', P[k]['cls']) != P[k]['cls'])]
print('lines of the run whose recorded class or prediction differs from predictions-225.json:', mism)
ubs = [k for k, v in runs.items() for f, r in v if r.get('upper_bound_given') != (P[k]['predicted'] if P[k]['predicted'] is not None else 450)]
print('lines whose recorded upper bound is not the prediction (or 450 where there is none):', ubs)
ALLP = [(u, v) for u in range(3) for v in range(3) if (u, v) != (0, 0)]
def is_up(S): return all((x, y) in S for (u, v) in S for x in range(u, 3) for y in range(v, 3))
def corner_sum(S):
    low = [(u, v) for u in range(3) for v in range(3) if (u, v) not in S]
    return sum(p ** (2 - u) * q ** (2 - v) for (u, v) in low if not any((x, y) != (u, v) and x >= u and y >= v for (x, y) in low))
def inside(S):
    if all(v <= 1 for u, v in S): return theorem1(p, q, 2, {u for u, v in S if v == 0}, {u for u, v in S if v == 1 and u >= 1}, (0, 1) in S)
    if all(u <= 1 for u, v in S): return theorem1(q, p, 2, {v for u, v in S if u == 0}, {v for u, v in S if u == 1 and v >= 1}, (1, 0) in S)
    return None
# my own fit: sums of at most three monomials p^i q^j (i + j <= 4), coefficients 1 or 2, through the four stored values; simplest =
# fewest monomials, then least sum of coefficients, then least total degree (predict.py's order; the sheet says only "simplest")
PTS = [(2, 3), (3, 2), (2, 5), (5, 2)]; MON = [(i, j) for i in range(5) for j in range(5) if i + j <= 4]
cands = collections.defaultdict(list)
for r in (1, 2, 3):
    for ms in itertools.combinations(MON, r):
        for ks in itertools.product((1, 2), repeat=r):
            val = lambda pt: sum(k * pt[0] ** i * pt[1] ** j for (i, j), k in zip(ms, ks))
            cands[tuple(val(pt) for pt in PTS)].append(((r, sum(ks), sum(i + j for i, j in ms)), val((3, 5))))
cls = collections.Counter(); bad = []; amb = 0
for k, o in P.items():
    S = {tuple(t) for t in o['S']}
    assert sorted(p ** u * q ** v for u, v in S) == [int(t) for t in k.split(',') if t]
    if is_up(S): c, pred = 'theorem-upset', corner_sum(S)
    elif inside(S) is not None: c, pred = 'theorem-m1', inside(S)
    elif all(o['decided']) and tuple(o['values_23_32_25_52']) in cands:
        cs = cands[tuple(o['values_23_32_25_52'])]; w0 = min(w for w, _ in cs); vs = {v for w, v in cs if w == w0}
        allv = {v for w, v in cs}
        if len(allv) > 1: amb += 1
        c, pred = ('fit', vs.pop()) if len(vs) == 1 else ('fit-ambiguous', None)
    else: c, pred = 'none', None
    cls[c] += 1
    if (c, pred) != (o['cls'], o['predicted']): bad.append((k, c, pred, o['cls'], o['predicted']))
print('my classes:', dict(cls), '; differing from predictions-225.json:', bad)
print('fit patterns for which sums of different complexity give different values at (3, 5):', amb)
none_why = collections.Counter('not all four decided' if not all(o['decided']) else 'no sum' for o in P.values() if o['cls'] == 'none'); print('no prediction:', dict(none_why))
# the stored four values against the tables as they are now
R36 = {tuple(sorted(r['D'])): r for r in json.load(open('/home/agent3/pq2/note/rows-36.json'))}
R100 = {tuple(sorted(r['D'])): r for r in json.load(open('/home/agent3/pq2/note/rows-100.json'))}
chg = []; newdec = 0
for k, o in P.items():
    S = {tuple(t) for t in o['S']}; T = {(v, u) for u, v in S}
    now = [R36[tuple(sorted(2 ** u * 3 ** v for u, v in S))], R36[tuple(sorted(2 ** u * 3 ** v for u, v in T))], R100[tuple(sorted(2 ** u * 5 ** v for u, v in S))], R100[tuple(sorted(2 ** u * 5 ** v for u, v in T))]]
    nv = [r['size'] for r in now]; nd = [bool(r['by']) for r in now]
    if nv != o['values_23_32_25_52']: chg.append((show(S), o['values_23_32_25_52'], nv, o['decided'], nd, o['cls']))
    if all(nd) and not all(o['decided']): newdec += 1
print('patterns whose four values in the tables today differ from those sealed:', chg)
print('patterns with all four decided today but not when sealed:', newdec)

# --- first sheet
dec = {k: r['size'] for k, r in last.items() if r['status'] == 'optimal'}
inf = [k for k, r in last.items() if r['status'] == 'infeasible']
print('\nFIRST SHEET\nstatus:', dict(collections.Counter(r['status'] for r in last.values())), '; infeasible:', inf)
w0 = []
for k, v in dec.items():
    S = {tuple(t) for t in P[k]['S']}
    a = len(S & {(1, 0), (2, 0)}); b = len(S & {(0, 1), (0, 2)})
    upin = {(u, w) for (u, w) in S if all((x, y) in S for x in range(u, 3) for y in range(w, 3))}
    cp = corner_sum(upin)
    if is_up(S) and v != corner_sum(S): w0.append((k, 'up-set'))
    if not is_up(S) and inside(S) is not None and v != inside(S): w0.append((k, 'theorem'))
    if v % (3 ** a * 5 ** b): w0.append((k, 'divisibility'))
    if v < cp or (v == cp and not is_up(S)): w0.append((k, 'Corollary P'))
print('W0 failures:', w0)
ups = [k for k, o in P.items() if is_up({tuple(t) for t in o['S']})]
m1 = [k for k, o in P.items() if not is_up({tuple(t) for t in o['S']}) and inside({tuple(t) for t in o['S']}) is not None]
print(f'theorem patterns: {len(ups)} up-sets, decided {sum(k in dec for k in ups)}; {len(m1)} others, decided {sum(k in dec for k in m1)}; not decided:',
      [(show(P[k]["S"]), last[k]['status'], last[k]['size'], inside({tuple(t) for t in P[k]["S"]})) for k in m1 if k not in dec])
print('W1: decided', len(dec), '>= 128:', len(dec) >= 128)
fit = [k for k, o in P.items() if o['cls'] == 'fit']
fset = [k for k in fit if k in dec or k in inf]; feq = [k for k in fit if k in dec and dec[k] == P[k]['predicted']]
print(f'W2/W3: fit {len(fit)}; settled {len(fset)}; as predicted {len(feq)}; W2: {len(feq) >= 0.9 * len(fset)}; W3: {len(feq) == len(fset)}')
uns = [k for k in fit if k not in fset]
print('   fit patterns not settled:', len(uns), '; what the run found for them:', dict(collections.Counter(
      ('no multiset' if last[k]['size'] is None else 'a multiset of the predicted size' if last[k]['size'] == P[k]['predicted'] else 'a multiset BELOW the prediction' if last[k]['size'] < P[k]['predicted'] else 'above') for k in uns)))
print('   unsettled fit patterns where LB already equals the prediction (so the prediction is right by LB and the found multiset):',
      sum(1 for k in uns if last[k]['size'] == P[k]['predicted'] == OB['225|' + k]['LB']))
byS = {show(o['S']): k for k, o in P.items()}
lines = [('W1', 0.7, len(dec) >= 128), ('W2', 0.6, len(feq) >= 0.9 * len(fset)), ('W3', 0.12, len(feq) == len(fset))]
for S, val, pr in [('01 02 21', 25, 0.6), ('10 12 20', 18, 0.6), ('01 12 20', 75, 0.5), ('02 10 21', 90, 0.5), ('02 11 20', 105, 0.35), ('02 11 20', 90, 0.35), ('01 02 20 22', 150, 0.4),
                   ('02 10 20 22', 90, 0.4), ('01 02 10 12 21 22', 225, 0.6), ('01 10 12 20 21 22', 225, 0.6), ('12 21', 30, 0.45), ('11 22', 30, 0.6), ('02 20 22', 30, 0.6)]:
    k = byS[S]; lines.append((f'{{{S}}} is {val}', pr, (dec[k] == val) if k in dec else None))
    print(f'   {{{S}}} is {val}: odds {pr};', 'held' if k in dec and dec[k] == val else f'did not hold (it is {dec[k]})' if k in dec else f'not decided (status {last[k]["status"]}, found {last[k]["size"]}; class {P[k]["cls"]})')
sc = [(pr - (1 if o else 0)) ** 2 for _, pr, o in lines if o is not None]
print(f'Brier over {len(sc)} settled lines: {sum(sc) / len(sc):.4f}')
nofit10 = [show(o['S']) for o in P.values() if o['cls'] == 'none' and all(o['decided'])]; print('the patterns with all four decided and no sum (the sheet says ten):', len(nofit10), nofit10)

# --- second sheet
print('\nSECOND SHEET')
dB = [(k, B[k]['LB'], OB['225|' + k]['LB'], B[k]['U'], OB['225|' + k]['U3']) for k in B if B[k]['LB'] != OB['225|' + k]['LB'] or B[k]['U'] != OB['225|' + k]['U3']]
print('bounds-225.json against my own LB and three-move bound: differences:', dB, '; LB = U for', sum(1 for k in B if B[k]['LB'] == B[k]['U']))
print('V0 failures:', [(k, B[k]['LB'], v, B[k]['U']) for k, v in dec.items() if not B[k]['LB'] <= v <= B[k]['U']])
eq = sum(1 for k, v in dec.items() if v == B[k]['U']); lt = sum(1 for k, v in dec.items() if v < B[k]['U'])
none = [k for k in dec if P[k]['cls'] == 'none']; neq = sum(1 for k in none if dec[k] == B[k]['U'])
print(f'V1: least = U for {eq} of {len(dec)} = {100 * eq / len(dec):.1f}% ; at least 85%: {eq >= 0.85 * len(dec)}')
print(f'V2: no-prediction patterns: {sum(1 for o in P.values() if o["cls"] == "none")}; decided {len(none)}; least = U for {neq}; at least half: {2 * neq >= len(none)}')
print(f'V3: decided with least < U: {lt}; at least 10: {lt >= 10}')
s2 = [(0.7 - (eq >= 0.85 * len(dec))) ** 2, (0.5 - (2 * neq >= len(none))) ** 2, (0.75 - (lt >= 10)) ** 2]; print(f'Brier over 3 lines: {sum(s2) / 3:.4f}')
print('the second sheet says: U is the least size for 230 of 256 on Z_36 and 222 of the 236 decided on Z_100; LB = U for 145 in each; 144 on Z_225')

# --- the deviation: which results came from which file, and the seconds
print('\nTHE RUN, BY FILE')
for f in sorted({f for v in runs.values() for f, _ in v}):
    rs = [r for v in runs.values() for g, r in v if g == f]
    print(f'  {f}: {len(rs)} lines;', dict(collections.Counter(r['status'] for r in rs)), '; longest seconds', max(r['seconds'] for r in rs))
first = [(k, r) for k, v in runs.items() for f, r in v if f[5] in '012345']
fnp = [(k, r) for k, r in first if r['status'] == 'feasible-not-proved']
print('first run: lines', len(first), '; feasible-not-proved', len(fnp), '; unknown', sum(1 for k, r in first if r['status'] == 'unknown'), '; optimal', sum(1 for k, r in first if r['status'] == 'optimal'))
print('   seconds of the feasible-not-proved lines of the first run:', sorted(r['seconds'] for k, r in fnp))
print('   optimal lines of the first run that took more than 100 s:', sorted(r['seconds'] for k, r in first if r['status'] == 'optimal' and r['seconds'] > 100))
print('   classes of the 34:', dict(collections.Counter(P[k]['cls'] for k, r in fnp)))
