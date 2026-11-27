# clause_check.py -- the clause added to "Mine (ii)" of the revised text: "mu(d) + 1, the least number of elements
# with which d can be a level after contraction".
#  1. Attained: for every odd d, 3 <= d <= DMAX, the multiset of mu(d) + 1 elements on Z_d built from the residues
#     0 and j*p^t (1 <= j < p, 0 <= t < v_p(d)) for each prime p of d (padded with 0, combined by the Chinese
#     remainder theorem) has a full group at every level of every tree, and no order of contracting changes it.
#  2. At least mu(d) + 1: in every output of exh_full.py here, every end n_flat of a contraction of a multiset of m
#     elements has mu(n_flat) + 1 <= m (hence mu(d) + 1 <= m for every d | n_flat); the first m at which each end
#     occurs.  (The runs also tested n_flat | n'_m, the same statement, for three orders of contracting.)
#  3. Another count, for comparison: the least number of elements with which some signing is BAD at d for a
#     multiset on Z_d that has a full group at every level of every tree ("a loss is possible at all" at the level d).
import sys, re, glob, itertools, random
import numpy as np
from rlib import factor, divisors, mu, crt, all_levels_full, contract_all, bad_at, signs

DMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 3001
rng = random.Random(3)
cnt = 0
for d in range(3, DMAX, 2):
    f = factor(d)
    m = mu(d) + 1
    cols = {}
    for p, a in f.items():
        col = [0] + [j * p ** t for t in range(a) for j in range(1, p)]
        assert len(col) == 1 + a * (p - 1) <= m
        cols[p] = col + [0] * (m - len(col))
    B = []
    for k in range(m):
        x, M = 0, 1
        for p, a in f.items():
            x = crt(x, M, cols[p][k], p ** a)
            M *= p ** a
        B.append(x)
    assert len(B) == m and all_levels_full(B, d), d
    for order in ("deep", "shallow", "random"):
        Bf, nf, steps = contract_all(B, d, order, rng)
        assert nf == d and not steps, d
    cnt += 1
print("1. attained: for each of the %d odd d with 3 <= d < %d the construction with mu(d) + 1 elements has every level of every tree full and is not contractible" % (cnt, DMAX))

first = {}
lines = 0
for fn in sorted(glob.glob("exh_*.out")):
    s = open(fn).read()
    n = int(re.search(r"Z_(\d+), multisets", s).group(1))
    for a in re.finditer(r"m = +(\d+): (\d+) multisets, .*?ends of the deepest-first contraction: (\{.*?\})", s):
        m = int(a.group(1))
        ends = eval(a.group(3))
        lines += 1
        for nf, c in ends.items():
            assert mu(nf) + 1 <= m, (fn, m, nf)
            if nf not in first or m < first[nf]:
                first[nf] = m
print("2. at least: %d lines (group, m) of the exhaustive outputs: every end n_flat has mu(n_flat) + 1 <= m" % lines)
print("   end n_flat: first m at which it occurs in these runs / mu(n_flat) + 1:", {nf: "%d / %d" % (first[nf], mu(nf) + 1) for nf in sorted(first)})

print("3. least number of elements with which some signing is bad at d, multisets on Z_d with every level of every tree full")
for d, mmax in ((3, 4), (5, 6), (7, 8), (9, 8), (15, 7), (21, 8)):
    found = None
    for m in range(mu(d) + 1, mmax + 1):
        E = signs(m)
        nfull = nbad = 0
        ex = None
        for tup in itertools.combinations_with_replacement(range(d), m - 1):
            B = [0] + list(tup)
            if not all_levels_full(B, d):
                continue
            nfull += 1
            k = int(bad_at(B, d, d, E).sum())
            if k:
                nbad += 1
                if ex is None:
                    ex = (B, k)
        print("   d = %2d, m = %d: %d multisets with 0 and every level full; with a signing bad at d: %d%s" % (d, m, nfull, nbad, "; for instance %s (%d of %d signings)" % (ex[0], ex[1], 1 << m) if ex else ""))
        if nbad:
            found = m
            break
    print("   d = %2d: mu(d) + 1 = %d; least m with a signing bad at d: %s" % (d, mu(d) + 1, found if found else "more than %d" % mmax))
