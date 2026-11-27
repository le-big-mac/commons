# Deeper trees: every multiset of m elements on Z_(2^K) up to the symmetries of the 2-tree (swapping the two
# halves of a class, with all that lies below them), one representative each; rho_2 by brute force over all
# signings of the representative.  The bound, where it is attained, the referee's criterion for equality,
# and the least rho_2 over sets.
# usage: run_trees.py K M_FROM M_TO          (counts the trees first; "count" as 4th argument only counts)
#        run_trees.py check K M              (checks on ALL multisets of 1..M elements on Z_(2^K) that rho_2 is the
#                                             same for a multiset and for its representative)
import sys, itertools, time
from fractions import Fraction
from collections import Counter
from functools import lru_cache
from ref_lib import p, Fast


@lru_cache(maxsize=None)
def trees(d, m):
    """One representative (a tuple of elements of Z_(2^d)) of every class of multisets of m elements on Z_(2^d)
    under the tree symmetries: the even elements (halved) and the odd elements (halved) are representatives
    at depth d - 1, the smaller part first; equal sizes: the earlier in the list first."""
    if d == 0:
        return ((0,) * m,)
    out = []
    for a in range(0, m // 2 + 1):
        b = m - a
        TL = trees(d - 1, a); TR = trees(d - 1, b)
        if a < b:
            for L in TL:
                for R in TR:
                    out.append(tuple(2 * x for x in L) + tuple(2 * x + 1 for x in R))
        else:
            for i, L in enumerate(TL):
                for R in TR[i:]:
                    out.append(tuple(2 * x for x in L) + tuple(2 * x + 1 for x in R))
    return tuple(out)


@lru_cache(maxsize=None)
def ntrees(d, m):
    if d == 0:
        return 1
    tot = 0
    for a in range(0, m // 2 + 1):
        b = m - a
        if a < b:
            tot += ntrees(d - 1, a) * ntrees(d - 1, b)
        else:
            x = ntrees(d - 1, a)
            tot += x * (x + 1) // 2
    return tot


def elems(t, d):
    return list(t)


def canon(B, d):
    """a canonical representative of the class of the multiset B on Z_(2^d), independent of trees()"""
    if d == 0:
        return (0,) * len(B)
    L = canon([x >> 1 for x in B if x % 2 == 0], d - 1)
    R = canon([x >> 1 for x in B if x % 2 == 1], d - 1)
    if (len(L), L) > (len(R), R):
        L, R = R, L
    return tuple(2 * x for x in L) + tuple(2 * x + 1 for x in R)


def criterion(B, K):
    if 1 not in Counter(B).values():
        return False
    for j in range(1, K + 1):
        cl = {}
        for b in B:
            cl.setdefault(b % (1 << (j - 1)), []).append(b)
        split = sum(1 for c in cl.values() if len({b % (1 << j) for b in c}) == 2)
        if split >= 2 and not any(len(c) == 1 for c in cl.values()):
            return False
    return True


if sys.argv[1] == "check":
    K = int(sys.argv[2]); M = int(sys.argv[3])
    bad = 0; tot = 0; reps = set()
    for m in range(1, M + 1):
        f = Fast(m)
        seen = {}
        for B in itertools.combinations_with_replacement(range(1 << K), m):
            c = canon(list(B), K)
            g = f.count_good(B, K)
            tot += 1
            if c not in seen:
                rep = tuple(sorted(elems(c, K)))
                assert canon(list(rep), K) == c
                seen[c] = f.count_good(rep, K)
            if seen[c] != g:
                bad += 1
        print(f"Z_{1 << K}, m = {m}: {len(seen)} classes of multisets under the tree symmetries "
              f"(formula: {ntrees(K, m)})", flush=True)
        assert len(seen) == ntrees(K, m)
        # the enumeration used in the main mode gives exactly one representative of each class
        enum = [canon(elems(t, K), K) for t in trees(K, m)]
        assert len(enum) == len(set(enum)) and set(enum) == set(seen)
    print(f"all {tot} multisets of 1..{M} elements on Z_{1 << K}: rho_2 differs from the representative's in {bad} cases")
    sys.exit()

K = int(sys.argv[1]); M0 = int(sys.argv[2]); M1 = int(sys.argv[3])
print(f"Z_{1 << K}: trees of depth {K}; numbers of representatives:",
      {m: ntrees(K, m) for m in range(M0, M1 + 1)}, flush=True)
if len(sys.argv) > 4:
    sys.exit()
t0 = time.time()
fails = Counter()
for m in range(M0, M1 + 1):
    f = Fast(m)
    bound = int(p(m - 1) * (1 << m))
    tot = eq = 0; least = None; arg = None
    nsets = 0; leastset = None; argset = None; eqsets = 0
    for t in trees(K, m):
        B = elems(t, K)
        g = f.count_good(B, K)
        tot += 1
        if g < bound:
            fails["below the bound"] += 1
            print("  BELOW:", sorted(B))
        e = (g == bound)
        eq += e
        if criterion(B, K) != e:
            fails["criterion for equality"] += 1
            if fails["criterion for equality"] <= 5:
                print("  criterion mismatch:", sorted(B), Fraction(g, 1 << m))
        if least is None or g < least:
            least = g; arg = sorted(B)
        if len(set(B)) == m:
            nsets += 1; eqsets += e
            if leastset is None or g < leastset:
                leastset = g; argset = sorted(B)
    line = (f"m = {m}: {tot} representatives, least rho_2 = {Fraction(least, 1 << m)} (p_(m-1) = {p(m - 1)}), "
            f"equal to the bound at {eq}; ")
    if nsets:
        line += f"sets: {nsets}, least rho_2 over sets = {Fraction(leastset, 1 << m)} at {argset}, equal to the bound at {eqsets}"
    else:
        line += "no sets"
    print(line + f"   [{time.time() - t0:.0f} s]", flush=True)
print("failures:", dict(fails) if fails else "none")
