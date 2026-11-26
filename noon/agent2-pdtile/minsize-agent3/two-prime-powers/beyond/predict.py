"""Predictions for Z_225 = 3^2 5^2 from what is known on Z_36 and Z_100, for a sealed sheet.
A pattern is a set S of exponent pairs (u, v) != (0, 0), 0 <= u, v <= 2, meaning Phi_{p^u q^v} divides.  For each S the tables give
f_S(2,3), f_S(3,2), f_S(2,5), f_S(5,2) (a pattern of Z_36 read with p = 2 or with p = 3, and the same for Z_100).  Prediction of f_S(3,5):
  'theorem-upset'   S is an up-set: the corner sum (Theorem S)
  'theorem-m1'      S uses only pairs with v <= 1, or only pairs with u <= 1: the theorem for Z_{p^n q} (rule below)
  'fit'             all four values decided and a sum of at most three monomials p^i q^j (coefficients 1 or 2, i + j <= 4) passes through them:
                    the simplest such sum, evaluated at (3, 5); 'fit-ambiguous' if the simplest sums give different values at (3, 5)
  'none'            otherwise
Writes predictions-225.json: for each divisor set D of 225 the class and the predicted value.   usage: predict.py"""
import json, itertools
R36 = {frozenset(r['D']): r for r in json.load(open('/home/agent3/pq2/note/rows-36.json'))}
R100 = {frozenset(r['D']): r for r in json.load(open('/home/agent3/pq2/note/rows-100.json'))}
def exps(D, p, q):
    out = []
    for d in D:
        u = 0
        while d % p == 0: d //= p; u += 1
        v = 0
        while d % q == 0: d //= q; v += 1
        out.append((u, v))
    return frozenset(out)
E36 = {exps(D, 2, 3): r for D, r in R36.items()}; E100 = {exps(D, 2, 5): r for D, r in R100.items()}
tr = lambda S: frozenset((v, u) for u, v in S)
PTS = [(2, 3), (3, 2), (2, 5), (5, 2)]
def vals(S): return (E36[S]['size'], E36[tr(S)]['size'], E100[S]['size'], E100[tr(S)]['size']), (True, True, bool(E100[S]['by']), bool(E100[tr(S)]['by']))
def rule(p, q, n, E, F):                                       # the theorem for Z_{p^n q}, as in score100.py
    e = len(E)
    if 0 not in F:
        k = len([a for a in F if a not in E]); return p ** e * (p ** k + q) if k else p ** e
    if set(F) == set(range(n + 1)): return q * p ** e
    a0 = min(a for a in range(1, n + 1) if a not in F); G = sorted(a for a in F if a > a0 and a not in E)
    x = 0 if (not G or any(a in E for a in range(1, a0)) or (a0 in E and p >= 3) or (a0 in E and p == 2 and any(a in E and a not in F for a in range(a0 + 1, G[0])))) else 1
    return q * p ** e * (p ** len(G) + x)
def m1(S, p, q):
    if all(v <= 1 for u, v in S): return rule(p, q, 2, [u for u, v in S if v == 0], [u for u, v in S if v == 1])
    if all(u <= 1 for u, v in S): return rule(q, p, 2, [v for u, v in S if u == 0], [v for u, v in S if u == 1])
    return None
ALL = [(u, v) for u in range(3) for v in range(3) if (u, v) != (0, 0)]
def is_up(S): return all((a, b) in S for (u, v) in S for (a, b) in ALL if a >= u and b >= v)
def corner_sum(S, p, q):
    L = [(u, v) for u in range(3) for v in range(3) if (u, v) not in S]
    C = [(u, v) for (u, v) in L if not any((a, b) != (u, v) and a >= u and b >= v for (a, b) in L)]
    return sum(p ** (2 - u) * q ** (2 - v) for u, v in C)
MON = [(i, j) for i in range(5) for j in range(5) if i + j <= 4]
def mv(c, pt): return sum(k * pt[0] ** i * pt[1] ** j for (i, j), k in c)
cands = {}
for r in (1, 2, 3):
    for ms in itertools.combinations(MON, r):
        for ks in itertools.product((1, 2), repeat=r):
            c = tuple(zip(ms, ks)); cands.setdefault(tuple(mv(c, pt) for pt in PTS), []).append(c)
weight = lambda c: (len(c), sum(k for _, k in c), sum(i + j for (i, j), _ in c))
def fmt(c): return ' + '.join(('' if k == 1 else str(k)) + (('p' + ('' if i == 1 else f'^{i}')) if i else '') + (('q' + ('' if j == 1 else f'^{j}')) if j else '') or str(k) for (i, j), k in c)
# self-check of the two theorems on the tables themselves
for S in E36:
    v, dec = vals(S)
    for (p, q), x, d in zip(PTS, v, dec):
        SS = S if (p, q) in ((2, 3), (2, 5)) else S     # f_S(p,q): for (3,2),(5,2) the table entry is that of the transposed divisor set, already taken in vals
        if is_up(S) and d: assert x == corner_sum(S, p, q), (sorted(S), p, q, x)
        t = m1(S, p, q)
        if t is not None and d: assert x == t, (sorted(S), p, q, x, t)
out = {}; classes = {}
for S in sorted(E36, key=lambda S: (len(S), sorted(S))):
    D = sorted(3 ** u * 5 ** v for u, v in S)
    v, dec = vals(S)
    if is_up(S): cls, pred, how = 'theorem-upset', corner_sum(S, 3, 5), 'corner sum'
    elif m1(S, 3, 5) is not None: cls, pred, how = 'theorem-m1', m1(S, 3, 5), 'theorem for p^n q'
    elif all(dec) and v in cands:
        best = sorted(cands[v], key=weight); w0 = weight(best[0]); top = [c for c in best if weight(c) == w0]
        ps = sorted(set(mv(c, (3, 5)) for c in top))
        if len(ps) == 1: cls, pred, how = 'fit', ps[0], fmt(top[0])
        else: cls, pred, how = 'fit-ambiguous', None, ' | '.join(fmt(c) for c in top)
    else: cls, pred, how = 'none', None, ('not all four decided' if not all(dec) else 'no sum of at most three monomials')
    out[','.join(map(str, D))] = dict(S=sorted(S), values_23_32_25_52=v, decided=dec, cls=cls, predicted=pred, how=how)
    classes[cls] = classes.get(cls, 0) + 1
json.dump(out, open('predictions-225.json', 'w'), indent=0)
print(classes)
import collections
print('fit formulas used:', sorted(collections.Counter(o['how'] for o in out.values() if o['cls'] == 'fit').items(), key=lambda t: -t[1]))
print('ambiguous:', [(o['S'], o['how']) for o in out.values() if o['cls'] == 'fit-ambiguous'][:10])
print('none:', collections.Counter(o['how'] for o in out.values() if o['cls'] == 'none'))
