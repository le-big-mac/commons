# rho_2: the share of signings of a multiset on Z_{2^K} that are 3-bad at no 2^j (Lemma S3: sigma_B != 0 mod 3, and at
# every level j >= 1 some class C modulo 2^(j-1) has sigma_C' != sigma_C'' mod 3).
# rho_2 depends only on the 2-tree with its levels that are not live contracted (step-down, Lemma L3 (a) for q = 2),
# so m elements need at most m - 1 levels.  Here: every tree with m elements and at most m - 1 levels, by recursion
# (trees with levels that are not live are included; that does no harm); exact fractions.  Also a brute-force check against lib2.
import sys, itertools, random
from fractions import Fraction as Fr
from functools import lru_cache
sys.path.insert(0, '/home/agent3/lean/lift-check/even/prover2')

LMAX = 12
ALL = (1 << LMAX) - 1

@lru_cache(maxsize=None)
def leaf_dist(r):
    # r equal elements: distribution of (sigma mod 3, mask); mask = ALL if sigma != 0 (a witness at every deeper level), else 0
    d = {}
    for k in range(r + 1):           # k minus signs
        s = (r - 2 * k) % 3
        from math import comb
        key = (s, ALL if s else 0)
        d[key] = d.get(key, Fr(0)) + Fr(comb(r, k), 2 ** r)
    return tuple(sorted(d.items()))

@lru_cache(maxsize=None)
def trees(m, d):
    # trees with m elements and at most d levels: ('L', m) (all elements equal), ('U', child) (one child empty at this
    # level, the child not a leaf), ('N', left, right); returned with their depth
    out = [(('L', m), 0)]
    if d == 0: return tuple(out)
    for (t, dt) in trees(m, d - 1):
        if t[0] != 'L': out.append((('U', t), dt + 1))
    for a in range(1, m // 2 + 1):
        b = m - a
        for (ta, da) in trees(a, d - 1):
            for (tb, db) in trees(b, d - 1):
                if a == b and repr(ta) < repr(tb): continue
                out.append((('N', tb, ta), 1 + max(da, db)))
    return tuple(out)

@lru_cache(maxsize=None)
def dist(t):
    if t[0] == 'L': return leaf_dist(t[1])
    if t[0] == 'U':
        d = {}
        for (sc, mc), pc in dist(t[1]):
            key = (sc, (1 if sc else 0) | ((mc << 1) & ALL))
            d[key] = d.get(key, Fr(0)) + pc
        return tuple(sorted(d.items()))
    dl, dr = dist(t[1]), dist(t[2])
    d = {}
    for (sl, ml), pl in dl:
        for (sr, mr), pr in dr:
            mask = (1 if sl != sr else 0) | (((ml | mr) << 1) & ALL)
            key = ((sl + sr) % 3, mask)
            d[key] = d.get(key, Fr(0)) + pl * pr
    return tuple(sorted(d.items()))

def rho2(t, depth):
    need = (1 << depth) - 1
    return sum(p for (s, mask), p in dist(t) if s and (mask & need) == need)

def is_exceptional(t):
    return t[0] == 'N' and t[1] == ('L', 1) and t[2] == ('L', 1)

if __name__ == '__main__':
    # brute-force comparison on Z_8, Z_16 for small multisets
    from lib2 import all_signs, bad3_table, divisors
    import numpy as np
    def tree_of(B, K):
        if K == 0 or len(set(B)) == 1: return ('L', len(B)), 0
        E = [x // 2 for x in B if x % 2 == 0]; D = [x // 2 for x in B if x % 2 == 1]
        if not D or not E:
            t, d = tree_of(E or D, K - 1)
            return (t, d) if t[0] == 'L' else (('U', t), d + 1)
        (te, de), (td, dd) = tree_of(E, K - 1), tree_of(D, K - 1)
        return ('N', te, td), 1 + max(de, dd)
    rnd = random.Random(3); cmp = 0
    for K in (2, 3, 4):
        for _ in range(400):
            m = rnd.randint(1, 8); B = [rnd.randrange(1 << K) for _ in range(m)]
            S = all_signs(m, fix_first=False)
            bad3 = bad3_table(B, 1 << K, S)
            g = np.ones(S.shape[0], dtype=bool)
            for d in divisors(1 << K): g &= ~bad3[d]
            t, dep = tree_of(B, K)
            assert Fr(int(g.sum()), S.shape[0]) == rho2(t, dep), (B, K)
            cmp += 1
    print('recursion compared with all signings on', cmp, 'random multisets on Z_4, Z_8, Z_16: equal')
    for m in range(1, 9):
        best = None; cnt = 0
        for t, dep in trees(m, m - 1):
            if is_exceptional(t): continue
            r = rho2(t, dep); cnt += 1
            if best is None or r < best[0]: best = (r, t)
        print('m =', m, 'trees', cnt, 'least rho_2 =', best[0], '=%.4f' % float(best[0]), 'at', best[1], flush=True)
