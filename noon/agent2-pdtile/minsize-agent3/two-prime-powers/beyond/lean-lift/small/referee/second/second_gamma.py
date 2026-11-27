"""Second look, three checks of what the note now says about Gamma (exact fractions throughout).
(1) 'the same fractions': the referee's recursion (../ref_gamma.py, written from section 5 of sign-all-result.md)
    against the third result's own function coverage2.Gamma, for every m from 7 to MMAX, every prime of n'_m taken out
    as q, and none.
(2) the certificate printed in section 4 of the note (order 5^8, 7^5, 11^3, 13^2, 17^2, 19, 31, 23, 29): the value, and
    at which steps the candidate of Lemma 3' (the step taken from the second result) is the one that gives the value.
(3) a certificate that uses Lemma 3T only (no Lemma 3'): best order and value for n'_36 / 3^17.
usage: second_gamma.py MMAX"""
import sys
from fractions import Fraction as Fr
sys.path.insert(0, '/home/agent3/lean/lift-check/small/referee')
sys.path.insert(0, '/home/agent3/lean/lift-check/general2')
from ref_gamma import gamma_all, shape, lam, single
from coverage2 import Gamma as GammaAuthor

MMAX = int(sys.argv[1])
ncmp = 0; npos = 0; nneg = 0; ndiff = 0
for m in range(7, MMAX + 1):
    f = shape(m)
    for q in [None] + [p for p, _ in f]:
        rest = [(p, a) for p, a in f if p != q]
        mine = gamma_all(rest); theirs = GammaAuthor(tuple(sorted(rest)))
        # where Gamma <= 0 the two programs may print different non-positive numbers: the text takes the maximum of
        # the candidates (it can be below -1), coverage2.py starts its maximum at -1.  Only Gamma > 0 carries meaning.
        if mine > 0 or theirs > 0:
            assert mine == theirs, (m, q, mine, theirs)
            npos += 1
        else:
            nneg += 1; ndiff += (mine != theirs)
        ncmp += 1
print(f'(1) referee\'s Gamma against coverage2.Gamma, exact fractions, m = 7..{MMAX}, every q and none: {ncmp} values; '
      f'{npos} positive, equal in every case; {nneg} not positive in both programs (of these {ndiff} are different non-positive numbers)')

def step(p, a, g1, L, use3p):
    t1 = single(p, a) * g1; t2 = Fr(3, 4) * g1 - L * lam(p, a)
    c3T = min(t1, t2)
    if a == 1 and use3p:
        c3p = min(g1 / 2, g1 - Fr(L, 2 ** (p - 1)))
        return max(c3T, c3p), c3T, c3p
    return c3T, c3T, None

order = [(5, 8), (7, 5), (11, 3), (13, 2), (17, 2), (19, 1), (31, 1), (23, 1), (29, 1)]
g = single(*order[0]); L = order[0][1] + 1
print('(2) the order of the note, full recursion:')
for p, a in order[1:]:
    val, c3T, c3p = step(p, a, g, L, True)
    need = (c3p is not None and c3p > c3T)
    print(f'    add {p}^{a}: L\' = {L}: Lemma 3T gives {c3T} (~{float(c3T):.6g})' + (f', Lemma 3\' gives {c3p} (~{float(c3p):.6g})' if c3p is not None else '')
          + f' -> {val}' + ('   [the value is that of Lemma 3\']' if need else ''))
    g = val; L *= a + 1
print(f'    Gamma = {g} (~{float(g):.6g})')

# (3) best order with Lemma 3T only
trees = order
k = len(trees); G = {}; how = {}
for mask in range(1, 1 << k):
    idx = [i for i in range(k) if mask >> i & 1]
    if len(idx) == 1:
        G[mask] = single(*trees[idx[0]]); how[mask] = None; continue
    best = None
    for i in idx:
        g1 = G[mask & ~(1 << i)]
        if g1 <= 0: continue
        p, a = trees[i]; L = 1
        for j in idx:
            if j != i: L *= trees[j][1] + 1
        val = step(p, a, g1, L, False)[0]
        if best is None or val > best[0]: best = (val, i, g1, L)
    G[mask] = best[0] if best else Fr(-1); how[mask] = best
mask = (1 << k) - 1; chain = []
while how[mask] is not None:
    chain.append((mask, how[mask])); mask &= ~(1 << how[mask][1])
(i0,) = [i for i in range(k) if mask >> i & 1]
print('(3) Lemma 3T only (no step from the second result), best order:')
print(f'    first tree {trees[i0][0]}^{trees[i0][1]}: single = {G[mask]}')
for mask, (val, i, g1, L) in reversed(chain):
    p, a = trees[i]
    print(f'    add {p}^{a}: G\' = {g1}, L\' = {L}, lambda = {lam(p, a)}: min( single*G\' = {single(p, a) * g1} , 3/4 G\' - L\' lambda = {Fr(3, 4) * g1 - L * lam(p, a)} ) = {val} (~{float(val):.6g})')
print(f'    Gamma without Lemma 3\' = {G[(1 << k) - 1]} (~{float(G[(1 << k) - 1]):.6g})')
