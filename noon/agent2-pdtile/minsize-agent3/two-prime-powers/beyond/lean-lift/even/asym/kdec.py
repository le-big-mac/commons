"""The limiting constant for one heavy residue.  A multiset on Z_n (n odd) made of h copies of 0 and a fixed
"decoration" D (r elements of Z_n, none 0).  A signing is bad iff S + Q(zeta) = 0 for some n-th root of unity zeta,
where S is the signed sum of the heavy copies and Q the signed mask of D.  As h grows, P(S = v) ~ sqrt(2/(pi h)) for
every v of the parity of h, so  P(bad) ~ K(D) * sqrt(2/(pi h)),  K(D) = E_signs #{ integers v of that parity : v = -Q(zeta)
for some zeta }.  K_same(D): h of the parity of r (m = h + r even);  K_other(D): the other parity (m odd).
This program computes K_same and K_other exactly for given decorations, and searches for large ones.
usage: kdec.py N R_MAX [SEED TRIES]"""
import sys, itertools, random
from fractions import Fraction
import numpy as np
sys.path.insert(0, '/home/agent3/lean/lift-check/even/shares')
from minshare import red_matrix
def K(R, blocks, D):
    r = len(D)
    if r == 0: return Fraction(1), Fraction(0)
    E = np.array(list(itertools.product((1, -1), repeat=r)), dtype=np.int64).T      # r x 2^r
    V = R[:, D] @ E                                                              # rows x 2^r
    vals = []                                                                    # per d: (is-integer mask, value)
    for (start, k, d) in blocks:
        blk = V[start:start + k]
        isint = ~np.any(blk[1:] != 0, axis=0) if k > 1 else np.ones(blk.shape[1], dtype=bool)
        vals.append((isint, blk[0]))
    same = 0; other = 0
    n2 = E.shape[1]
    # count distinct integer values per signing, by parity
    M = np.full((len(vals), n2), 10**6, dtype=np.int64)
    for i, (isint, v) in enumerate(vals): M[i, isint] = v[isint]
    M.sort(axis=0)
    distinct = np.ones_like(M, dtype=bool); distinct[1:] = M[1:] != M[:-1]
    valid = (M != 10**6) & distinct
    par = (M - r) % 2 == 0
    same = int((valid & par).sum()); other = int((valid & ~par).sum())
    return Fraction(same, n2), Fraction(other, n2)
if __name__ == '__main__':
    n = int(sys.argv[1]); rmax = int(sys.argv[2])
    R, blocks = red_matrix(n)
    if len(sys.argv) <= 3:
        for r in range(0, rmax + 1):
            best_s = (Fraction(-1), None); best_o = (Fraction(-1), None); cnt = 0
            for D in itertools.combinations_with_replacement(range(1, n), r):
                ks, ko = K(R, blocks, list(D)); cnt += 1
                if ks > best_s[0]: best_s = (ks, D)
                if ko > best_o[0]: best_o = (ko, D)
            print(f"n = {n}  r = {r}  decorations {cnt}:  K_same max {best_s[0]} = {float(best_s[0]):.4f} at {best_s[1]};  K_other max {best_o[0]} = {float(best_o[0]):.4f} at {best_o[1]}", flush=True)
    else:
        seed = int(sys.argv[3]); tries = int(sys.argv[4]); rng = random.Random(seed)
        for r in range(1, rmax + 1):
            for which in (0, 1):
                best = (Fraction(-1), None)
                for t in range(tries):
                    D = [rng.randrange(1, n) for _ in range(r)]; cur = K(R, blocks, D)[which]
                    for step in range(60 * r):
                        D2 = list(D); D2[rng.randrange(r)] = rng.randrange(1, n); c2 = K(R, blocks, D2)[which]
                        if c2 >= cur: D, cur = D2, c2
                    if cur > best[0]: best = (cur, sorted(D))
                print(f"n = {n}  r = {r}  {'K_same' if which == 0 else 'K_other'} found {best[0]} = {float(best[0]):.4f} at {best[1]}", flush=True)
