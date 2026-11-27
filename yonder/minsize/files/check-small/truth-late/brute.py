# A fresh reader's brute-force test of the sentences of the plain page (27 Nov 2026, late evening).
# Exact integer arithmetic.  A signed marking "balances at d" when the cyclotomic polynomial Phi_d divides
# sum(+-X^hour); tested by the remainder of X^h modulo Phi_d (integer vectors).
# usage: brute.py MODE ...   (see the bottom)
import sys, itertools, math
from fractions import Fraction
import numpy as np


def polymul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] += x * y
    return r


def polydivexact(a, b):
    # a / b, both integer lists low degree first, b monic; exact
    a = a[:]
    q = [0] * (len(a) - len(b) + 1)
    for i in range(len(q) - 1, -1, -1):
        c = a[i + len(b) - 1]
        q[i] = c
        if c:
            for j, y in enumerate(b):
                a[i + j] -= c * y
    assert all(x == 0 for x in a), "not exact"
    return q


_phi = {}


def cyclo(d):
    if d not in _phi:
        p = [-1] + [0] * (d - 1) + [1]  # X^d - 1
        for e in range(1, d):
            if d % e == 0:
                p = polydivexact(p, cyclo(e))
        _phi[d] = p
    return _phi[d]


def rem_table(n, d):
    # rows: X^h mod Phi_d for h = 0..n-1, as integer vectors of length deg Phi_d
    phi = cyclo(d)
    deg = len(phi) - 1
    rows = []
    cur = [1] + [0] * (deg - 1) if deg >= 1 else []
    for h in range(n):
        rows.append(cur[:])
        # multiply by X and reduce
        top = cur[-1]
        cur = [0] + cur[:-1]
        if top:
            for j in range(deg):
                cur[j] -= top * phi[j]
    return np.array(rows, dtype=np.int64)


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def sign_matrix(m):
    # all 2^m sign vectors
    return np.array(list(itertools.product((1, -1), repeat=m)), dtype=np.int64)


def bad_sets(n, marks, tabs, S):
    # returns dict d -> boolean array over signings: balances at d
    out = {}
    idx = list(marks)
    for d, T in tabs.items():
        V = S @ T[idx]  # (2^m, deg)
        out[d] = ~V.any(axis=1)
    return out


def multisets(n, m, with_zero):
    if with_zero:
        if m == 0:
            return
        for rest in itertools.combinations_with_replacement(range(n), m - 1):
            yield (0,) + rest
    else:
        yield from itertools.combinations_with_replacement(range(n), m)


def pow2part(n):
    k = 1
    while n % (2 * k) == 0:
        k *= 2
    return k


def add_order(x, n):
    return n // math.gcd(n, x % n)


def run_union(n, m, with_zero):
    """the bold sentence: falls balancing at some divisor (1 included) <= 2 * falls balancing at some odd divisor
    (1 included); and the same with 1 left out on both sides, to see whether '1 included' is needed."""
    ds = divisors(n)
    tabs = {d: rem_table(n, d) for d in ds}
    S = sign_matrix(m)
    cnt = 0
    fail = 0
    fail_no1 = 0
    eq = 0
    ex_no1 = None
    none_odd_some_any = 0
    for marks in multisets(n, m, with_zero):
        cnt += 1
        b = bad_sets(n, marks, tabs, S)
        any_all = np.zeros(len(S), dtype=bool)
        any_odd = np.zeros(len(S), dtype=bool)
        any_all1 = np.zeros(len(S), dtype=bool)
        any_odd1 = np.zeros(len(S), dtype=bool)
        for d in ds:
            any_all |= b[d]
            if d % 2:
                any_odd |= b[d]
            if d > 1:
                any_all1 |= b[d]
                if d % 2:
                    any_odd1 |= b[d]
        A, O = int(any_all.sum()), int(any_odd.sum())
        if A > 2 * O:
            fail += 1
        if A == 2 * O and O > 0:
            eq += 1
        if O == 0 and A > 0:
            none_odd_some_any += 1
        A1, O1 = int(any_all1.sum()), int(any_odd1.sum())
        if A1 > 2 * O1:
            fail_no1 += 1
            if ex_no1 is None:
                ex_no1 = (marks, A1, O1)
    print(f"union n={n} m={m} zero={int(with_zero)}: markings {cnt}; 'at most twice' (1 included) fails {fail}; "
          f"equality with some bad {eq}; none at odd divisor but some elsewhere {none_odd_some_any}; "
          f"with 1 left out fails {fail_no1}" + (f" e.g. {ex_no1}" if ex_no1 else ""), flush=True)
    return fail


def run_final(n, m):
    """good signs exist exactly when the marking is not one of the pairs (both descriptions of the pairs)"""
    ds = divisors(n)
    tabs = {d: rem_table(n, d) for d in ds}
    S = sign_matrix(m)
    P = pow2part(n)
    cnt = mism = nogood = 0
    minshare = Fraction(1)
    arg = None
    for marks in multisets(n, m, False):
        cnt += 1
        b = bad_sets(n, marks, tabs, S)
        anyb = np.zeros(len(S), dtype=bool)
        for d in ds:
            anyb |= b[d]
        good = len(S) - int(anyb.sum())
        pair_page = (m == 2 and (marks[0] - marks[1]) % P != 0)
        pair_lean = (m == 2 and add_order(marks[0] - marks[1], n) % 2 == 0)
        assert pair_page == pair_lean, (n, marks)
        if (good == 0) != pair_page:
            mism += 1
        if good == 0:
            nogood += 1
        sh = Fraction(good, len(S))
        if sh < minshare:
            minshare, arg = sh, marks
    print(f"final n={n} m={m}: markings {cnt}; without good signs {nogood}; mismatches with 'is such a pair' {mism}; "
          f"least share of good signs {minshare} at {arg}", flush=True)
    return mism


def run_share(n, m, with_zero=True):
    ds = divisors(n)
    tabs = {d: rem_table(n, d) for d in ds}
    S = sign_matrix(m)
    cnt = 0
    minshare = Fraction(1)
    arg = None
    for marks in multisets(n, m, with_zero):
        cnt += 1
        b = bad_sets(n, marks, tabs, S)
        anyb = np.zeros(len(S), dtype=bool)
        for d in ds:
            anyb |= b[d]
        sh = Fraction(len(S) - int(anyb.sum()), len(S))
        if sh < minshare:
            minshare, arg = sh, marks
    print(f"share n={n} m={m}: markings with 0: {cnt}; least share of good signs {minshare} = {float(minshare):.4f} at {arg}",
          flush=True)


def run_random(n, m, N, seed):
    import random
    rnd = random.Random(seed)
    ds = divisors(n)
    tabs = {d: rem_table(n, d) for d in ds}
    S = sign_matrix(m)
    minshare = Fraction(1)
    arg = None
    fail = 0
    for t in range(N):
        kind = t % 3
        if kind == 0:
            marks = tuple(sorted(rnd.randrange(n) for _ in range(m)))
        elif kind == 1:
            # structured: few residues modulo small divisors
            base = [rnd.randrange(n) for _ in range(2)]
            steps = [n // d for d in ds if d > 1]
            marks = tuple(sorted((rnd.choice(base) + rnd.randrange(4) * rnd.choice(steps)) % n for _ in range(m)))
        else:
            step = rnd.choice([n // d for d in ds if d > 1])
            marks = tuple(sorted((rnd.randrange(2) + rnd.randrange(8) * step) % n for _ in range(m)))
        b = bad_sets(n, marks, tabs, S)
        any_all = np.zeros(len(S), dtype=bool)
        any_odd = np.zeros(len(S), dtype=bool)
        for d in ds:
            any_all |= b[d]
            if d % 2:
                any_odd |= b[d]
        A, O = int(any_all.sum()), int(any_odd.sum())
        if A > 2 * O:
            fail += 1
        sh = Fraction(len(S) - A, len(S))
        if sh < minshare:
            minshare, arg = sh, marks
    print(f"random n={n} m={m} N={N}: 'at most twice' fails {fail}; least share of good signs {minshare} = "
          f"{float(minshare):.4f} at {arg}", flush=True)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "union":
        tot = 0
        for spec in sys.argv[2:]:
            n, mmax, z = spec.split(":")
            for m in range(0, int(mmax) + 1):
                if int(z) and m == 0:
                    continue
                tot += run_union(int(n), m, bool(int(z)))
        print("total failures of 'at most twice' (1 included):", tot)
    elif mode == "final":
        tot = 0
        for spec in sys.argv[2:]:
            n, mmax = spec.split(":")
            for m in range(1, int(mmax) + 1):
                tot += run_final(int(n), m)
        print("total mismatches:", tot)
    elif mode == "share":
        for spec in sys.argv[2:]:
            n, m = spec.split(":")
            run_share(int(n), int(m))
    elif mode == "random":
        for spec in sys.argv[2:]:
            n, m, N = spec.split(":")
            run_random(int(n), int(m), int(N), 12345 + int(n) * 100 + int(m))
    elif mode == "order":
        bad = 0
        tot = 0
        for n in range(1, int(sys.argv[2]) + 1):
            P = pow2part(n)
            for x in range(n):
                tot += 1
                if (add_order(x, n) % 2 == 0) != (x % P != 0):
                    bad += 1
        print(f"'order of the difference is even' against 'not a multiple of the largest power of 2 in n': "
              f"{tot} cases, n up to {sys.argv[2]}, disagreements {bad}")
