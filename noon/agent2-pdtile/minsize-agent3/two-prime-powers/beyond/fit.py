"""First look for formulas: each pattern of Z_{p^2 q^2} as a set of exponent pairs; its least sizes at (p,q) = (2,3), (3,2), (2,5), (5,2)
(from the Z_36 and Z_100 tables and their transposes); which sums of monomials p^i q^j (i, j <= 2..3, coefficients small) fit all four.
usage: fit.py"""
import json, itertools, collections
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
show = lambda S: ' '.join(f'{u}{v}' for u, v in sorted(S)) or '-'
PTS = [(2, 3), (3, 2), (2, 5), (5, 2)]
def vals(S):
    return (E36[S]['size'], E36[tr(S)]['size'], E100[S]['size'], E100[tr(S)]['size']), (True, True, bool(E100[S]['by']), bool(E100[tr(S)]['by']))
MON = [(i, j) for i in range(4) for j in range(4) if i + j <= 4]
def monval(c, pt): return sum(k * pt[0] ** i * pt[1] ** j for (i, j), k in c)
# all sums of at most 3 monomials with coefficients 1..2 (coefficient 3 for a single monomial too)
cands = {}
for r in (1, 2, 3):
    for ms in itertools.combinations(MON, r):
        for ks in itertools.product((1, 2), repeat=r):
            c = tuple(zip(ms, ks)); v = tuple(monval(c, pt) for pt in PTS); cands.setdefault(v, []).append(c)
def fmt(c):
    def m(i, j, k):
        s = ('' if k == 1 else str(k)) + ('p' + ('' if i == 1 else f'^{i}') if i else '') + ('q' + ('' if j == 1 else f'^{j}') if j else '')
        return s if (i or j) else str(k)
    return ' + '.join(m(i, j, k) for (i, j), k in c)
def weight(c): return (len(c), sum(k for _, k in c), sum(i + j for (i, j), _ in c))
groups = collections.defaultdict(list)
for S in E36: groups[vals(S)].append(S)
nofit = []
print(len(groups), 'distinct quadruples of values (with their decided flags) among', len(E36), 'patterns')
for (v, dec), Ss in sorted(groups.items(), key=lambda t: t[0][0]):
    fits = sorted(cands.get(v, []), key=weight)[:3]
    flag = '' if all(dec) else '  [not all decided: ' + ''.join('.' if d else '?' for d in dec) + ']'
    print(v, len(Ss), 'patterns;', 'fits:', ' | '.join(fmt(c) for c in fits) if fits else 'NONE', flag, '  e.g.', show(Ss[0]))
    if not fits: nofit.append((v, dec, Ss))
print(len(nofit), 'quadruples without a fit;', sum(len(t[2]) for t in nofit), 'patterns')
