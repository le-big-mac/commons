"""Lemmas 4, 5, 6, 7, 8, 10 and statement (1) of the PDF on explicit multisets, straight from the
definitions of Section 2 (lib.py), independent of dp.c.

Multisets are sampled in two ways: uniformly with bounded multiplicities, and by a random recursive
builder that makes children equal, of equal shapes, of equal totals, or unrelated, so that patterns
with many levels occur.  Every class of every sampled multiset is tested, with every pair (E, F)
contained in its pattern.
usage: t5_sample.py seed
"""
import sys, itertools, random
import numpy as np
from lib import class_vectors, class_pattern, children, is_constant, equal_shapes, equal_totals, in_S, in_Sp, in_Q

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)


def subs(s):
    s = sorted(s)
    for r in range(len(s) + 1):
        for c in itertools.combinations(s, r):
            yield frozenset(c)


def build(p, q, j, maxm):
    """random array of shape (p^j, q)"""
    if j == 0:
        mode = rng.random()
        if mode < 0.25:
            return np.zeros((1, q), dtype=np.int64)
        if mode < 0.45:
            return np.full((1, q), rng.randint(0, maxm), dtype=np.int64)
        return np.array([[rng.randint(0, maxm) for _ in range(q)]], dtype=np.int64)
    mode = rng.random()
    if mode < 0.2:      # all children equal
        c = build(p, q, j - 1, maxm)
        kids = [c.copy() for _ in range(p)]
    elif mode < 0.45:   # equal shapes: a child, plus constants put on one string or spread evenly
        c = build(p, q, j - 1, maxm)
        kids = []
        for _ in range(p):
            k = c.copy()
            d = rng.choice([0, 0, 1, 1, 2, 3])
            if d:
                if rng.random() < 0.5:
                    k[rng.randrange(k.shape[0])] += d
                else:
                    k += d
            kids.append(k)
        rng.shuffle(kids)
    elif mode < 0.65:   # equal totals: the same child with its layers permuted (rotated or reversed)
        c = build(p, q, j - 1, maxm)
        kids = []
        for _ in range(p):
            r = rng.randrange(q)
            k = np.roll(c, r, axis=1)
            if rng.random() < 0.3:
                k = k[:, ::-1].copy()
            kids.append(k)
    elif mode < 0.8:    # one child, the others empty or fibres
        kids = []
        for i in range(p):
            if i == 0:
                kids.append(build(p, q, j - 1, maxm))
            elif rng.random() < 0.6:
                kids.append(np.zeros((p ** (j - 1), q), dtype=np.int64))
            else:
                k = np.zeros((p ** (j - 1), q), dtype=np.int64)
                k[rng.randrange(k.shape[0])] += rng.randint(1, 2)
                kids.append(k)
        rng.shuffle(kids)
    else:               # unrelated
        kids = [build(p, q, j - 1, maxm) for _ in range(p)]
    # child i holds the strings with digit i at the first level: u = i + p * (rest)
    out = np.zeros((p ** j, q), dtype=np.int64)
    for i, k in enumerate(kids):
        out[i::p] = k
    return out


stats = {}


def cnt(k, v=1):
    stats[k] = stats.get(k, 0) + v


def fail(name, info):
    cnt("FAIL " + name)
    print("FAIL", name, info)


def test(A, p, q, n):
    vec = {d: class_vectors(A, p, n, d) for d in range(n + 1)}
    pats = {}
    for d in range(n + 1):
        for c in range(p ** d):
            pats[(d, c)] = class_pattern(A, p, n, d, c)
    rootbal = is_constant(vec[0][0])
    EA, FA = pats[(0, 0)]
    for d in range(n + 1):
        for c in range(p ** d):
            g = vec[d][c]
            tot = int(g.sum())
            bal = is_constant(g)
            EN, FN = pats[(d, c)]
            j = n - d
            cnt("classes")
            # the vector of a class is the sum of the vectors of its children
            if j >= 1:
                kids = children(c, p, d)
                kv = [vec[d + 1][k] for k in kids]
                assert (sum(kv) == g).all()
                # statement (1): shifted pair is contained in the pattern of every child
                Em = {l - 1 for l in EN if l >= 2}
                Fm = {l - 1 for l in FN if l >= 2}
                for k in kids:
                    cnt("(1) shift")
                    if not (Em <= pats[(d + 1, k)][0] and Fm <= pats[(d + 1, k)][1]):
                        fail("shift", (p, q, n, d, c))
                # Lemma 4 (a), (b)
                if equal_shapes(kv):
                    cnt("L4 equal shapes")
                    assert 1 in FN
                    v = min(kv, key=lambda x: int(x.sum()))
                    ds = []
                    for x in kv:
                        diff = x - v
                        if not is_constant(diff) or diff[0] < 0:
                            fail("L4a", (p, q, n, d, c))
                        ds.append(int(diff[0]))
                    if tot != p * int(v.sum()) + q * sum(ds):
                        fail("L4a total", (p, q, n, d, c))
                    if equal_totals(kv) != (sum(ds) == 0):
                        fail("L4a equal totals", (p, q, n, d, c))
                    if bal != all(is_constant(x) for x in kv):
                        fail("L4b", (p, q, n, d, c))
                    if not bal:
                        cnt("L4b unbalanced")
                        if any(is_constant(x) or x.sum() == 0 for x in kv):
                            fail("L4b unbalanced child", (p, q, n, d, c))
                else:
                    assert 1 not in FN
                    if bal != all(is_constant(x) for x in kv):
                        cnt("L4b would fail without equal shapes")
            # Lemma 4 (c)
            if rootbal:
                a0 = min([l for l in range(1, n + 1) if l not in FA], default=n + 1)
                if d <= a0 - 1:
                    cnt("L4c")
                    if not bal:
                        fail("L4c", (p, q, n, d, c))
            # witnesses from the definition
            witness = set()
            for gl in range(1, j + 1):
                dd = d + gl - 1
                for cc in range(c, p ** dd, p ** d):
                    kv2 = [vec[dd + 1][k] for k in children(cc, p, dd)]
                    if not equal_totals(kv2):
                        witness.add(gl)
                        if vec[dd][cc].sum() == 0:
                            fail("witness class empty", (p, q, n, d, c))
                        if gl >= 2:
                            # it lies in one child, which has a witness at its own level gl-1
                            child = c + (cc // p ** d % p) * p ** d
                            if (gl - 1) in pats[(d + 1, child)][0]:
                                fail("witness in child", (p, q, n, d, c))
            if witness != set(range(1, j + 1)) - EN:
                fail("witness iff not in E(N)", (p, q, n, d, c))
            if tot == 0:
                continue
            for E in subs(EN):
                cnt("L5")
                if tot % p ** len(E) or (bal and tot % (q * p ** len(E))):
                    fail("L5", (p, q, n, d, c))
                for F in subs(FN):
                    u = len(E | F)
                    wit = [x for x in F if x in witness]
                    if not bal:
                        cnt("L6")
                        if not in_S(tot, p, q, u):
                            fail("L6", (p, q, n, d, c, sorted(E), sorted(F)))
                        if wit:
                            cnt("L7")
                            sp, qq = in_Sp(tot, p, q, u), in_Q(tot, p, q, u)
                            if not (sp or qq):
                                fail("L7", (p, q, n, d, c, sorted(E), sorted(F)))
                            if any(not any(l < x for l in E - F) for x in wit):
                                cnt("L8")
                                if not sp:
                                    fail("L8", (p, q, n, d, c, sorted(E), sorted(F)))
                            elif not sp:
                                cnt("L8 extra hypothesis false and conclusion false")
                    elif j >= 1 and 1 not in FN:
                        cnt("L10")
                        if tot < q * p ** u:
                            fail("L10", (p, q, n, d, c, sorted(E), sorted(F)))


def main():
    cases = [(p, q, n) for p in (2, 3, 5) for q in (2, 3, 5) if p != q for n in (1, 2, 3) if p ** n <= 27 or (p, n) == (5, 2)]
    for (p, q, n) in cases:
        nsamp = 4000 if p ** n <= 9 else 1500
        before = dict(stats)
        seen = set()
        for i in range(nsamp):
            if i % 4 == 0:
                A = np.array([[rng.choice([0, 0, 0, 1, 1, 2]) for _ in range(q)] for _ in range(p ** n)], dtype=np.int64)
            else:
                A = build(p, q, n, rng.choice([1, 2, 3]))
            test(A, p, q, n)
            seen.add(class_pattern(A, p, n, 0, 0) + (is_constant(class_vectors(A, p, n, 0)[0]),))
        d = {k: stats.get(k, 0) - before.get(k, 0) for k in stats}
        print(f"p={p} q={q} n={n}: {nsamp} multisets, root patterns seen {len(seen)} of {2**(2*n+1)}; " +
              ", ".join(f"{k}={d[k]}" for k in sorted(d) if d[k]))
    print("TOTAL:", ", ".join(f"{k}={stats[k]}" for k in sorted(stats)))


main()
