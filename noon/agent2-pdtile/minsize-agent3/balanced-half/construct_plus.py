"""Proposition 13 of proof.md, the direction x = 0 => (*): the multiset A+ of its proof (the construction of section 6.3
in its host cases, with the fibres at the host level spread over the levels of G' as well) is built for every pattern
with k' >= 1 and x = 0 and checked to have exact pattern (E union G', F), exactly q p^(e+k') elements, and a nonempty
fibre class of depth h < g1 (the class with digit i0 at the host level h and 0 elsewhere).
The function below is construct() of construct_bal.py with those three lines changed (generated from it by text
replacement when this file was made)."""
import sys, itertools
sys.path.insert(0, "/home/agent3/minsize/prove")
from pat import tree_pattern
from claims import rule_value
from construct_bal import crt_index, digit_strings, all_balanced_patterns
from test_tree import analyse


def construct_plus(p, q, n, E, F):
    """returns (weights on Z_M, description).  0 in F is assumed."""
    E = set(E); F = set(F)
    assert 0 in F
    P = p ** n; M = P * q
    idx = crt_index(p, q, n)
    w = [0] * M
    lv = set(range(1, n + 1))

    def add_fibres(free, fixed, mult):
        for u, _ in digit_strings(p, n, free, fixed):
            for layer in range(q):
                w[idx[u][layer]] += mult

    # (a) F = all levels: fibres over the strings free at E
    if lv <= F:
        add_fibres(E, {}, 1)
        return w, 'all-F'

    a0 = min(a for a in lv if a not in F)
    above = {a for a in lv if a < a0}
    below = {a for a in lv if a > a0}
    G = sorted(a for a in below if a in F and a not in E)       # levels of F minus E deeper than a0
    k1 = len(G)
    T = {a for a in below if a in E or a in F}                  # free digits of the shape part below a0
    H = {a for a in below if a in E and a not in F}
    top_free = {a for a in above if a in E}
    Zq = [1] * q

    def rot(base, plus=(), minus=()):
        r = list(base)
        for i in plus: r[i % q] += 1
        for i in minus: r[i % q] -= 1
        assert min(r) >= 0
        return r

    R_uneq = {0: rot([0] * q, plus=[0]), 1: rot(Zq, minus=[0])}                      # a0 not in E
    R_eq = {i: rot(Zq) for i in range(p)}                                            # a0 in E
    R_eq[0] = rot(Zq, plus=[0], minus=[1]); R_eq[1] = rot(Zq, plus=[1], minus=[0])
    R_two = {0: R_eq[0], 1: R_eq[1]}                                                 # a0 in E, only two children carry shape

    def add_shape_part(top_free, T, H, R):
        """digits free at top_free (above a0) and at T (below a0), 0 elsewhere; digit i at a0 with the rotations R[i];
        tau(u) = 1 if H is not empty and every digit of u at a level of H is nonzero, else 0."""
        for i, Ri in R.items():
            for u, d in digit_strings(p, n, top_free | T, {a0: i}):
                tau = 1 if (H and all(d[a] != 0 for a in H)) else 0
                for r in range(q):
                    if Ri[r]:
                        w[idx[u][(tau + r) % q]] += Ri[r]

    R_std = R_eq if a0 in E else R_uneq
    if k1 == 0:
        add_shape_part(top_free, T, H, R_std)
        return w, 'k\'=0'
    g1 = G[0]
    # host level
    host = None
    cand = sorted(b for b in E if b < a0)
    if cand:
        host = cand[0]
    elif a0 in E and p >= 3:
        host = a0
    elif a0 in E:
        cand = sorted(b for b in E if a0 < b < g1 and b not in F)
        if cand:
            host = cand[0]
    if host is None:
        add_shape_part(top_free, T, H, R_std)
        add_fibres(E, {}, 1)
        return w, 'no host (x=1)'
    b = host
    if b < a0:
        add_shape_part(top_free - {b}, T, H, R_std)
        for i in range(1, p):
            add_fibres((E - {b}) | set(G), {b: i}, 1)
        return w, ('host above a0', b, 1)
    if b == a0:
        add_shape_part(top_free, T, H, R_two)
        for i in range(2, p):
            add_fibres((E - {b}) | set(G), {b: i}, 1)
        return w, ('host = a0', b, 2)
    add_shape_part(top_free, T - {b}, H - {b}, R_std)
    for i in range(1, p):
        add_fibres((E - {b}) | set(G), {b: i}, 1)
    return w, ('host below a0', b, 1)




def fibre_class_at(p, q, n, w, h, i0):
    """is the class of depth h with digit i0 at level h and 0 at the other levels <= h a nonempty fibre class?"""
    P = p ** n
    pref = i0 * p ** (h - 1)
    sub = [0] * len(w)
    for x, wt in enumerate(w):
        if wt and (x % P) % p ** h == pref: sub[x] = wt
    if not any(sub): return False
    # fibre class iff every leaf class inside is balanced
    for u in range(P):
        if u % p ** h != pref: continue
        vals = set(sub[x] for x in range(len(w)) if x % P == u)
        if len(vals) != 1: return False
    return True


if __name__ == '__main__':
    tot = bad = 0
    for (p, q, n) in [(2, 3, 2), (3, 2, 2), (2, 3, 3), (3, 2, 3), (2, 5, 3), (5, 2, 3), (3, 5, 3), (2, 3, 4), (3, 2, 4), (2, 7, 4), (5, 2, 4), (2, 3, 5), (3, 2, 5), (2, 3, 6)]:
        cnt = 0; b0 = bad
        for E, F in all_balanced_patterns(n):
            val, x, k1, a0 = rule_value(p, q, n, E, F[1:])
            if x is None or k1 == 0 or x == 1: continue
            w, info = construct_plus(p, q, n, E, F)
            kind, h, i0 = info
            G = sorted(a for a in F if a > a0 and a not in E); g1 = G[0]
            Eplus = tuple(sorted(set(E) | set(G)))
            ok = (sum(w) == q * p ** (len(E) + k1) and tree_pattern(p, q, n, w) == (Eplus, F) and h < g1 and fibre_class_at(p, q, n, w, h, i0))
            cnt += 1; tot += 1
            if not ok:
                bad += 1
                if bad <= 10: print('   BAD', (p, q, n), E, F, info)
        print(f'p={p} q={q} n={n}: {cnt} patterns with k\'>=1 and x=0, {bad - b0} wrong', flush=True)
    print('TOTAL:', tot, 'patterns,', bad, 'wrong')
