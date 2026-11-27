"""Two additions to ref_gamma.py (same recursion, exact fractions).
(1) A certificate for Gamma(n'_36 / 3^17) > 0 that can be followed by hand: an order of the trees and, at each step,
    G', L', the two terms of Lemma 3T (and of Lemma 3' when a = 1) and the value taken.
(2) The shapes of the author's first, weaker reduction, n_m = product over odd primes p <= m of p^(m-1): for which m is
    Gamma > 0 for some choice of q (small_cover.out stops with an error at m = 17).
usage: ref_gamma_extra.py MMAX"""
import sys
from fractions import Fraction as Fr
from ref_gamma import lam, single, shape, primes_upto

def gamma_table(trees):
    k = len(trees); G = {}; how = {}
    for mask in range(1, 1 << k):
        idx = [i for i in range(k) if mask >> i & 1]
        if len(idx) == 1:
            G[mask] = single(*trees[idx[0]]); how[mask] = None; continue
        best = None
        for i in idx:
            rest = mask & ~(1 << i); g1 = G[rest]
            if g1 <= 0: continue
            p, a = trees[i]; L = 1
            for j in idx:
                if j != i: L *= trees[j][1] + 1
            t1 = single(p, a) * g1; t2 = Fr(3, 4) * g1 - L * lam(p, a)
            cand = min(t1, t2); rec = (i, g1, L, t1, t2, None, None)
            if a == 1:
                u1 = g1 / 2; u2 = g1 - Fr(L, 2 ** (p - 1))
                if min(u1, u2) > cand:
                    cand = min(u1, u2)
                rec = (i, g1, L, t1, t2, u1, u2)
            if best is None or cand > best[0]:
                best = (cand, rec)
        G[mask] = best[0] if best else Fr(-1); how[mask] = best[1] if best else None
    return G, how

if __name__ == '__main__':
    M = int(sys.argv[1])
    f = [(p, a) for p, a in shape(36) if p != 3]
    G, how = gamma_table(f)
    mask = (1 << len(f)) - 1
    chain = []
    while how[mask] is not None:
        chain.append((mask, how[mask])); mask &= ~(1 << how[mask][0])
    print('(1) n\'_36 = ' + ' * '.join(f'{p}^{a}' if a > 1 else str(p) for p, a in shape(36)) + '; q = 3; trees in the order taken:')
    (i0,) = [i for i in range(len(f)) if mask >> i & 1]
    print(f'    first tree {f[i0][0]}^{f[i0][1]}: Gamma = single = {G[mask]}')
    for mask, (i, g1, L, t1, t2, u1, u2) in reversed(chain):
        p, a = f[i]
        line = f'    add {p}^{a}: G\' = {g1}, L\' = {L}, lambda = {lam(p, a)}: single*G\' = {t1}, 3/4 G\' - L\' lambda = {t2}'
        if u1 is not None:
            line += f'; (a = 1) G\'/2 = {u1}, G\' - L\' 2^(1-p) = {u2}'
        line += f'  ->  Gamma = {G[mask]} (~{float(G[mask]):.6g})'
        print(line)
    print('(2) first reduction, n_m = product of p^(m-1) over odd primes p <= m:')
    for m in range(7, M + 1):
        f = [(p, m - 1) for p in primes_upto(m) if p >= 3]
        pos = []
        for q in [None] + [p for p, _ in f]:
            rest = [(p, a) for p, a in f if p != q]
            g = gamma_table(rest)[0][(1 << len(rest)) - 1]
            if g > 0: pos.append((q, g))
        print(f'    m={m}: ' + ('Gamma > 0 for q = ' + ', '.join(f'{q} ({float(g):.3g})' for q, g in pos) if pos else 'Gamma <= 0 for every q and for no q'))
