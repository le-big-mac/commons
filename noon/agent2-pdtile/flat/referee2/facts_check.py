"""Exact linear-algebra verification of Fact 1 and Fact 2.

For n = p^a q^b the condition  Phi_n | A(X)  depends only on the count function N on Z_n
(A(X) mod X^n - 1 = sum_x N(x) X^x and Phi_n | X^n - 1) and is LINEAR in N:
    sum_x N(x) * (X^x mod Phi_n) = 0        (phi(n) rational linear equations).
Fact 1 / Fact 2 state another system of linear equations in N.  The two statements are
equivalent for all real N (hence for all count functions) iff the two systems have the same
row space.  We test rank(R) = rank(D) = rank([R; D]) exactly over GF(P) for two large primes
AND over Q by fraction-free elimination on the small cases.
"""
import sys
from fractions import Fraction
from common import residues, euler_phi, selftest


def rank_mod(rows, P):
    rows = [[x % P for x in r] for r in rows]
    rank = 0
    ncol = len(rows[0]) if rows else 0
    for col in range(ncol):
        piv = None
        for i in range(rank, len(rows)):
            if rows[i][col]:
                piv = i
                break
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        inv = pow(rows[rank][col], P - 2, P)
        rows[rank] = [(x * inv) % P for x in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][col]:
                f = rows[i][col]
                rows[i] = [(x - f * y) % P for x, y in zip(rows[i], rows[rank])]
        rank += 1
    return rank


def rank_Q(rows):
    rows = [[Fraction(x) for x in r] for r in rows]
    rank = 0
    ncol = len(rows[0]) if rows else 0
    for col in range(ncol):
        piv = None
        for i in range(rank, len(rows)):
            if rows[i][col]:
                piv = i
                break
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        pv = rows[rank][col]
        rows[rank] = [x / pv for x in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][col]:
                f = rows[i][col]
                rows[i] = [x - f * y for x, y in zip(rows[i], rows[rank])]
        rank += 1
    return rank


def crt_index(pa, qb):
    """index[(r, t)] = the x in Z_{pa*qb} with x = r mod pa, x = t mod qb."""
    n = pa * qb
    idx = {}
    for x in range(n):
        idx[(x % pa, x % qb)] = x
    assert len(idx) == n
    return idx


def fact_rows(p, a, q, b):
    """Rows of the linear system asserted by Fact 1 (b == 0) or Fact 2 (a, b >= 1), literally
    as written in the text, in CRT coordinates."""
    pa, qb = p ** a, q ** b
    n = pa * qb
    idx = crt_index(pa, qb)
    rows = []
    if b == 0:
        # Fact 1: N(r + i p^{a-1}) = N(r) for all r, i
        for r in range(pa):
            for i in range(1, p):
                row = [0] * n
                row[idx[((r + i * p ** (a - 1)) % pa, 0)]] += 1
                row[idx[(r, 0)]] -= 1
                rows.append(row)
        return rows
    # Fact 2: for all r, t, i the difference N(r + i p^{a-1}, t') - N(r, t') is the same for all
    # t' in t + q^{b-1} Z.   <=>  for all r, t, i, s:  [diff at t + s q^{b-1}] - [diff at t] = 0
    for r in range(pa):
        for t in range(qb):
            for i in range(1, p):
                for s in range(1, q):
                    row = [0] * n
                    r2 = (r + i * p ** (a - 1)) % pa
                    t2 = (t + s * q ** (b - 1)) % qb
                    row[idx[(r2, t2)]] += 1
                    row[idx[(r, t2)]] -= 1
                    row[idx[(r2, t)]] -= 1
                    row[idx[(r, t)]] += 1
                    rows.append(row)
    return rows


def cyclo_rows(n):
    R = residues(n)  # n rows of length phi(n)
    ph = euler_phi(n)
    return [[R[x][k] for x in range(n)] for k in range(ph)]


def check(p, a, q, b, exact_Q):
    n = p ** a * q ** b
    C = cyclo_rows(n)
    D = fact_rows(p, a, q, b)
    ph = euler_phi(n)
    ok = True
    for P in (2305843009213693951, 1000000007):
        rc, rd, rb = rank_mod(C, P), rank_mod(D, P), rank_mod(C + D, P)
        ok = ok and (rc == rd == rb == ph)
    extra = ""
    if exact_Q:
        rc, rd, rb = rank_Q(C), rank_Q(D), rank_Q(C + D)
        ok = ok and (rc == rd == rb == ph)
        extra = " (also exact over Q)"
    name = f"Phi_{{{p}^{a}}}" if b == 0 else f"Phi_{{{p}^{a} {q}^{b}}}"
    print(f"  {name:16s} n={n:4d} phi(n)={ph:3d}  rank(cyclo)={rc} rank(Fact)={rd} rank(both)={rb}"
          f"  -> {'EQUIVALENT' if ok else 'NOT EQUIVALENT'}{extra}")
    return ok


if __name__ == "__main__":
    selftest()
    allok = True
    print("Fact 1 (one prime):")
    for p, a in [(2, 1), (2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (3, 3), (3, 4), (5, 1), (5, 2), (7, 1), (7, 2)]:
        allok &= check(p, a, 2 if p != 2 else 3, 0, exact_Q=True)
    print("Fact 2 (two primes), as literally stated, CRT coordinates:")
    cases = [(2, 1, 3, 1), (2, 2, 3, 1), (2, 3, 3, 1), (2, 4, 3, 1), (2, 1, 3, 2), (2, 2, 3, 2),
             (2, 3, 3, 2), (2, 4, 3, 2),
             (3, 1, 2, 1), (3, 2, 2, 1), (3, 1, 2, 2), (3, 2, 2, 2), (3, 3, 2, 2), (3, 3, 2, 1),
             (2, 1, 5, 1), (2, 2, 5, 1), (2, 3, 5, 2), (2, 2, 5, 2), (5, 1, 2, 1), (5, 2, 2, 2), (5, 1, 3, 1),
             (3, 1, 5, 1), (3, 2, 5, 1), (5, 2, 3, 1), (3, 1, 7, 1), (7, 1, 3, 2)]
    for (p, a, q, b) in cases:
        allok &= check(p, a, q, b, exact_Q=True)
    print("ALL FACT CHECKS PASS" if allok else "SOME FACT CHECK FAILED")
    sys.exit(0 if allok else 1)
