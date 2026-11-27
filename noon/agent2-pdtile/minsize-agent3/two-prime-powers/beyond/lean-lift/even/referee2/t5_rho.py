# t5_rho.py -- Lemma rho recomputed.
# rho_2(B) = share of the signings that are 3-bad at no 2^j, j = 0..k  (B a multiset on Z_{2^k}).
# usage:
#   t5_rho.py brute m K [with0]   every multiset of m elements on Z_{2^K}: rho_2 by all signings, from the DEFINITION of
#                                 "3-bad at d" (remainder of the mask modulo Phi_d divisible by 3); least value; and for
#                                 every multiset the value is compared with the tree recursion below; and the claim
#                                 "rho_2 depends only on the 2-tree with the levels that are not live removed" is checked
#                                 (all multisets with the same contracted tree have the same rho_2; the number of
#                                 contracted trees is printed)
#   t5_rho.py trees m             the least rho_2 over ALL trees with m elements: every tree of depth exactly m-1, and
#                                 separately every tree of depth <= m-1 all of whose levels are live
import sys
from itertools import combinations_with_replacement
from functools import lru_cache
from rlib import *

# ---- trees.  A tree of depth K: K = 0: ('L', r) (r >= 1 equal elements); K >= 1: ('N', A, B) with A, B trees of depth K-1
#      or () (empty), not both empty, in a canonical order (the larger first).
def tree_of(vals, K):
    # vals: list of residues modulo 2^K, nonempty
    if K == 0:
        return ('L', len(vals))
    E = [v // 2 for v in vals if v % 2 == 0]
    D = [v // 2 for v in vals if v % 2 == 1]
    a = tree_of(E, K - 1) if E else ()
    b = tree_of(D, K - 1) if D else ()
    return canon(a, b)

def key(t):
    return t          # the empty tree is (), below every other tuple

def canon(a, b):
    if key(a) < key(b):
        a, b = b, a
    return ('N', a, b)

def depth(t):
    if t[0] == 'L':
        return 0
    return 1 + depth(t[1])

def size(t):
    if t == ():
        return 0
    if t[0] == 'L':
        return t[1]
    return size(t[1]) + size(t[2])

def level_live(t, j):
    # is level j (1 = the split of the root) live in t: some class at depth j-1 has two nonempty children
    if t == () or t[0] == 'L':
        return False
    if j == 1:
        return t[1] != () and t[2] != ()
    return level_live(t[1], j - 1) or level_live(t[2], j - 1)

def remove_level(t, j):
    # remove the level j (not live): every class at depth j-1 is replaced by its only nonempty child
    if t == ():
        return ()
    if j == 1:
        assert t[0] == 'N' and (t[2] == ())
        return t[1]
    return canon(remove_level(t[1], j - 1), remove_level(t[2], j - 1))

def contract(t):
    K = depth(t)
    j = 1
    while j <= K:
        if level_live(t, j):
            j += 1
        else:
            t = remove_level(t, j)
            K -= 1
    return t

# ---- the recursion: for a tree, the number of signings with (sum mod 3, set of levels that have a witness)
P3 = {}
def leafdist(r):
    if r not in P3:
        d = {0: 1}
        for _ in range(r):
            nd = {}
            for s, c in d.items():
                for e in (1, 2):
                    nd[(s + e) % 3] = nd.get((s + e) % 3, 0) + c
            d = nd
        P3[r] = d
    return P3[r]

@lru_cache(None)
def dist(t):
    # dict {(s, mask): count}; mask bit (j-1) set iff level j below the root of t has a class whose two children have
    # sums of signs that differ modulo 3
    if t == ():
        return {(0, 0): 1}
    if t[0] == 'L':
        return {(s, 0): c for s, c in leafdist(t[1]).items()}
    da, db = dist(t[1]), dist(t[2])
    out = {}
    for (s1, w1), c1 in da.items():
        for (s2, w2), c2 in db.items():
            w = ((w1 | w2) << 1) | (1 if s1 != s2 else 0)
            k = ((s1 + s2) % 3, w)
            out[k] = out.get(k, 0) + c1 * c2
    return out

def rho_tree(t):
    K = depth(t)
    full = (1 << K) - 1
    d = dist(t)
    good = sum(c for (s, w), c in d.items() if s != 0 and w == full)
    return Fraction(good, 2 ** size(t))

# ---- enumeration of all trees
@lru_cache(None)
def all_trees(m, K):
    if K == 0:
        return (('L', m),)
    out = []
    # one child empty
    for a in all_trees(m, K - 1):
        out.append(canon(a, ()))
    for a in range(1, m):
        b = m - a
        if a < b:
            continue
        for ta in all_trees(a, K - 1):
            for tb in all_trees(b, K - 1):
                if a == b and key(ta) < key(tb):
                    continue
                out.append(canon(ta, tb))
    return tuple(out)

def all_live(t):
    return all(level_live(t, j) for j in range(1, depth(t) + 1))

def describe(t):
    if t == ():
        return '-'
    if t[0] == 'L':
        return str(t[1])
    return '(' + describe(t[1]) + ' ' + describe(t[2]) + ')'

mode = sys.argv[1]
if mode == 'brute':
    m, K = int(sys.argv[2]), int(sys.argv[3])
    with0 = len(sys.argv) > 4
    n = 2 ** K
    S = 1 << (m - 1)
    least = None
    cnt = 0
    by_contracted = {}
    mism = 0
    bs = max(500, 40_000_000 // (S * max(1, n // 2) * 2))
    for E in chunks(multisets(n, m, with0=with0), bs):
        good = np.ones((len(E), S), dtype=bool)
        for j in range(K + 1):
            good &= ~batch_bad3(E, 2 ** j)
        g = good.sum(axis=1)
        for row, gi in zip(E.tolist(), g.tolist()):
            t = tree_of(row, K)
            r = Fraction(gi, S)
            if rho_tree(t) != r:
                mism += 1
            c = contract(t)
            if c in by_contracted:
                if by_contracted[c] != r:
                    raise SystemExit(f"two multisets with the same contracted tree and different rho_2: {row}")
            else:
                by_contracted[c] = r
            if least is None or r < least[0]:
                least = (r, row)
            cnt += 1
    assert mism == 0, mism
    vals = sorted(set(by_contracted.values()))
    amin = [describe(c) for c, r in by_contracted.items() if r == vals[0]]
    print(f"m = {m}, Z_{n}: {'multisets with 0' if with0 else 'every multiset'}: {cnt}; rho_2 by all signings, from the definition; "
          f"least {least[0]} at {least[1]}; equal to the tree recursion for every multiset; "
          f"{len(by_contracted)} contracted trees, rho_2 constant on each; least values {', '.join(str(v) for v in vals[:4])}; "
          f"contracted trees with the least value: {len(amin)}, e.g. {amin[:3]}", flush=True)

elif mode == 'trees':
    for m in range(1, int(sys.argv[2]) + 1):
        K = m - 1
        ts = all_trees(m, K)
        vals = {}
        for t in ts:
            if m == 2 and t == canon(('L', 1), ('L', 1)):
                continue
            vals[t] = rho_tree(t)
        least = min(vals.values())
        arg = [describe(contract(t)) for t, v in vals.items() if v == least]
        # every tree of depth <= m-1 with all levels live
        livevals = {}
        for KK in range(0, m):
            for t in all_trees(m, KK):
                if all_live(t):
                    if m == 2 and KK == 1:
                        continue
                    livevals[t] = rho_tree(t)
        # consistency: contracting any tree of depth m-1 gives an all-live tree with the same value
        for t, v in vals.items():
            c = contract(t)
            assert all_live(c) and livevals[c] == v
        l2 = min(livevals.values())
        sv = sorted(set(livevals.values()))
        argl = [describe(t) for t, v in livevals.items() if v == l2]
        print(f"m = {m}: trees of depth exactly {K}: {len(vals)}; least rho_2 {least}; "
              f"trees of depth <= {K} with every level live: {len(livevals)}; least rho_2 {l2}, attained at {len(argl)} of them, e.g. {argl[:3]}; next values {', '.join(str(v) for v in sv[1:4])}", flush=True)
