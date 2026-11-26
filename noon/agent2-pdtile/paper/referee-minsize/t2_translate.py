"""Lemma 3 (the tree and the divisors) and the recursion program dp.c, both checked by brute force.

For a small group and a size bound S, enumerate EVERY multiset with at most S elements.
For each one compute the pattern twice:
  (i)  by exact integer long division of sum_x A(x) X^x by Phi_d (d = p^a, p^a q, q);
  (ii) from the tree definitions of Section 2 (classes, totals, shapes).
They must agree (Lemma 3).  The set of all (E, F, balanced, size) found must equal what
dp.c reports for sizes <= S (so the recursion enumerates the same thing).
"""
import sys, subprocess, itertools
from multiprocessing import Pool
import numpy as np
from lib import root_pattern, cyclotomic, poly_divmod_monic

CASES = [(2, 3, 1, 12), (3, 2, 1, 12), (2, 5, 1, 9), (5, 2, 1, 9), (2, 3, 2, 8), (3, 2, 2, 6),
         (2, 5, 2, 5), (2, 3, 3, 5), (2, 3, 0, 12), (5, 3, 1, 6), (3, 5, 1, 6), (2, 7, 1, 7)]


def multisets(M, S):
    """all vectors in N^M with sum <= S"""
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


def run(case):
    p, q, n, S = case
    M = p ** n * q
    divs = [("E", l, cyclotomic(p ** l)) for l in range(1, n + 1)] + \
           [("F", l, cyclotomic(p ** l * q)) for l in range(1, n + 1)] + [("B", 0, cyclotomic(q))]
    found = set()
    count = 0
    mism = 0
    for a in multisets(M, S):
        count += 1
        E, F, bal = set(), set(), False
        for kind, l, phi in divs:
            _, rem = poly_divmod_monic(a, phi)
            if not any(rem):
                if kind == "E":
                    E.add(l)
                elif kind == "F":
                    F.add(l)
                else:
                    bal = True
        A = np.zeros((p ** n, q), dtype=np.int64)
        for x in range(M):
            A[x % p ** n, x % q] = a[x]
        tE, tF, tbal = root_pattern(A, p, n)
        if (frozenset(E), frozenset(F), bal) != (tE, tF, tbal):
            mism += 1
        found.add((frozenset(E), frozenset(F), bal, sum(a)))
    out = subprocess.run(["./dp", str(p), str(q), str(n), str(S)], capture_output=True, text=True).stdout
    dp = set()
    for line in out.splitlines():
        t = list(map(int, line.split()))
        if t[0] != n:
            continue
        E = frozenset(l for l in range(1, n + 1) if t[1] >> (l - 1) & 1)
        F = frozenset(l for l in range(1, n + 1) if t[2] >> (l - 1) & 1)
        for s in t[4:]:
            dp.add((E, F, bool(t[3]), s))
    npat = len({(e, f, b) for e, f, b, _ in found})
    return (case, M, count, mism, len(found), npat, found == dp)


if __name__ == "__main__":
    with Pool(8) as pool:
        for case, M, count, mism, nf, npat, same in pool.imap(run, CASES):
            p, q, n, S = case
            print(f"p={p} q={q} n={n} Z_{M}: all {count} multisets of size <= {S}: "
                  f"tree pattern != division pattern in {mism}; distinct (pattern,size) {nf}, patterns seen {npat} of {2**(2*n+1)}; "
                  f"dp.c gives the same set: {same}")
