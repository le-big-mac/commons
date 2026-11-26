"""Remark 15 of the PDF ("one condition instead of four").

(1) host level  <=>  x = 0, for every pattern with k' >= 1 (pure combinatorics of the statement).
(2) "x = 0 iff some least multiset for the pattern (E u G, F), which has q p^(e+k') elements, contains a
    nonempty class of depth < min G all of whose subclasses are balanced": decided exactly by dp2.c
    (all multisets of the given size), compared with x from Theorem 1(c).
(3) the word "least" cannot be dropped: patterns with x = 1 for which a LARGER multiset with pattern
    (E u G, F) has such a class.
(4) dp2.c's extra quantity checked against plain enumeration on two small groups.
usage: t9_remark.py
"""
import subprocess, itertools, os
import numpy as np
from lib import subsets, class_vectors, class_pattern, is_constant, theorem_value


def rule(p, n, E, F):
    full = set(range(1, n + 1))
    a0 = min(full - F)
    G = {a for a in F - E if a > a0}
    kp = len(G)
    c = (kp == 0, any(a < a0 for a in E), (a0 in E) and p >= 3,
         (a0 in E) and p == 2 and kp > 0 and any(a0 < a < min(G) for a in E - F))
    return a0, G, kp, (0 if any(c) else 1)


# (1)
tested = bad = 0
for p in (2, 3, 5):
    for n in range(1, 9):
        full = set(range(1, n + 1))
        for E in subsets(n):
            for F in subsets(n):
                E_, F_ = set(E), set(F)
                if F_ == full:
                    continue
                a0, G, kp, x = rule(p, n, E_, F_)
                if kp == 0:
                    continue
                g1 = min(G)
                host = any(b < g1 and (b < a0 or (b == a0 and p >= 3) or (b > a0 and b not in F_ and a0 in E_)) for b in E_)
                tested += 1
                if host != (x == 0):
                    bad += 1
print(f"(1) host level <=> x = 0: patterns with k' >= 1, n <= 8, p in 2,3,5: tested {tested}, disagreements {bad}")


def run_dp2(p, q, n, B):
    fn = f"dpout/dp2-{p}-{q}-{n}-B{B}.txt"
    if not os.path.exists(fn):
        with open(fn, "w") as f:
            subprocess.run(["./dp2", str(p), str(q), str(n), str(B)], stdout=f, stderr=subprocess.DEVNULL, check=True)
    mu = {}
    for line in open(fn):
        j, e, f_, t, m = map(int, line.split())
        E = frozenset(l for l in range(1, j + 1) if e >> (l - 1) & 1)
        F = frozenset(l for l in range(1, j + 1) if f_ >> (l - 1) & 1)
        mu[(j, E, F, t)] = m
    return mu


# (4) plain enumeration against dp2
def multisets(M, S):
    cur = [0] * M

    def rec(pos, left):
        if pos == M:
            yield tuple(cur)
            return
        for x in range(left + 1):
            cur[pos] = x
            yield from rec(pos + 1, left - x)
        cur[pos] = 0
    yield from rec(0, S)


for (p, q, n, S) in [(2, 3, 2, 9), (3, 2, 2, 6), (2, 3, 3, 6)]:
    best = {}
    cnt = 0
    for a in multisets(p ** n * q, S):
        if sum(a) == 0 or sum(a) % q:
            continue
        A = np.array(a, dtype=np.int64).reshape(p ** n, q)
        vec = {d: class_vectors(A, p, n, d) for d in range(n + 1)}
        if not is_constant(vec[0][0]):
            continue
        cnt += 1
        E, F = class_pattern(A, p, n, 0, 0)
        m = 255
        for d in range(n + 1):
            for c in range(p ** d):
                if vec[d][c].sum() == 0:
                    continue
                if all(is_constant(vec[dd][cc]) for dd in range(d, n + 1) for cc in range(c, p ** dd, p ** d)):
                    m = min(m, d)
        key = (n, E, F, sum(a))
        best[key] = min(best.get(key, 255), m)
    mu = run_dp2(p, q, n, S)
    mine = {k: v for k, v in mu.items() if k[0] == n}
    print(f"(4) p={p} q={q} n={n}: {cnt} balanced multisets of size <= {S} enumerated; (pattern, size) pairs {len(best)}; "
          f"least depth of a fibre class equals dp2.c's in all: {best == mine}")

# (2), (3)
for (p, q, n, B) in [(2, 3, 2, 24), (3, 2, 2, 36), (2, 5, 2, 20), (5, 2, 2, 50), (2, 3, 3, 48), (3, 2, 3, 54),
                     (2, 3, 4, 48), (3, 2, 4, 162), (5, 3, 2, 75), (2, 5, 3, 20), (5, 2, 3, 250), (7, 2, 2, 98)]:
    mu = run_dp2(p, q, n, B)
    for j in range(2, n + 1):
        full = set(range(1, j + 1))
        t0 = t1 = b0 = b1 = skipped = larger = 0
        ex = None
        for E in subsets(j):
            for F in subsets(j):
                E_, F_ = set(E), set(F)
                if F_ == full:
                    continue
                a0, G, kp, x = rule(p, j, E_, F_)
                if kp == 0:
                    continue
                size = q * p ** (len(E_) + kp)
                if size > B:
                    skipped += 1
                    continue
                Eplus = frozenset(E_ | G)
                assert theorem_value(p, q, j, Eplus, F_, True) == size
                m = mu.get((j, Eplus, F, size))
                assert m is not None, "pattern (E u G, F) not found at its least size"
                has = m <= min(G) - 1
                if x == 0:
                    t0 += 1
                    b0 += (not has)
                else:
                    t1 += 1
                    b1 += has
                    # (3): a larger multiset with pattern (E u G, F) and a fibre class of depth < min G
                    for t in range(size + q, B + 1, q):
                        m2 = mu.get((j, Eplus, F, t))
                        if m2 is not None and m2 <= min(G) - 1:
                            larger += 1
                            if ex is None or t < ex[2]:
                                ex = (sorted(E_), sorted(F_), t, size)
                            break
        print(f"(2) p={p} q={q} n={j} (sizes <= {B}): patterns with k'>=1 and x=0: {t0}, of which without such a class {b0}; "
              f"with x=1: {t1}, of which WITH such a class {b1}; beyond the bound, not decided: {skipped}")
        if ex:
            print(f"    (3) x=1 patterns for which a larger multiset with pattern (E u G, F) has such a class: {larger}; "
                  f"smallest example E={ex[0]} F={ex[1]}: size {ex[2]} (least size {ex[3]})")
