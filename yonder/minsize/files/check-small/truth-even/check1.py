# Checks for the first new paragraph: signed sums at roots of unity, exactly (remainders modulo the cyclotomic
# polynomial, integer arithmetic) and, for the examples, numerically as well.
import cmath, itertools, sys
from math import gcd
from fractions import Fraction
import numpy as np


def polydivexact(a, b):
    a = a[:]
    q = [0] * (len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        c = a[i + len(b) - 1] // b[-1]
        q[i] = c
        for j, bj in enumerate(b):
            a[i + j] -= c * bj
    assert all(x == 0 for x in a)
    return q


_phi = {}


def cyclo(d):
    if d in _phi:
        return _phi[d]
    p = [-1] + [0] * (d - 1) + [1]
    for e in range(1, d):
        if d % e == 0:
            p = polydivexact(p, cyclo(e))
    _phi[d] = p
    return p


def rem_table(n, d):
    """row h: remainder of X^h modulo Phi_d, for h = 0..n-1"""
    ph = cyclo(d)
    deg = len(ph) - 1
    rows = []
    cur = [0] * deg
    if deg == 0:
        raise ValueError
    cur[0] = 1  # X^0
    for h in range(n):
        rows.append(cur[:])
        # multiply by X and reduce
        top = cur[-1]
        nxt = [0] + cur[:-1]
        if top:
            for j in range(deg):
                nxt[j] -= top * ph[j]
        cur = nxt
    return np.array(rows, dtype=np.int64)


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def signs_matrix(m):
    return np.array(list(itertools.product((1, -1), repeat=m)), dtype=np.int64)


def balance_divisors_numeric(n, marks, signs):
    out = []
    for d in divisors(n):
        z = cmath.exp(2j * cmath.pi / d)  # d steps to a full turn
        s = sum(e * z ** h for h, e in zip(marks, signs))
        if abs(s) < 1e-9:
            out.append(d)
    return out


def balance_divisors_exact(n, marks, signs, T):
    out = []
    for d in divisors(n):
        v = sum(e * T[d][h] for h, e in zip(marks, signs))
        if not v.any():
            out.append(d)
    return out


def run_checks():
    print("== examples, each choice of signs: divisors at which the signed marks balance (numeric | exact)")
    for n, marks in ((2, (0, 1)), (12, (0, 2)), (12, (0, 4)), (12, (0, 6)), (12, (0, 0)), (12, (0, 8)), (12, (3, 7)), (12, (1, 3))):
        T = {d: rem_table(n, d) for d in divisors(n)}
        for signs in itertools.product((1, -1), repeat=len(marks)):
            a = balance_divisors_numeric(n, marks, signs)
            b = balance_divisors_exact(n, marks, signs, T)
            assert a == b
            print(f"  clock {n:2d}, marks {marks}, signs {signs}: balances at {a if a else 'no divisor: GOOD'}")

    print("== pairs {0,b}: no good signs exactly when b is not a multiple of the largest power of 2 in n ?")
    ok = True
    for n in range(1, 61):
        k2 = 1
        while n % (2 * k2) == 0:
            k2 *= 2
        T = {d: rem_table(n, d) for d in divisors(n)}
        S = signs_matrix(2)
        nbad = 0
        for b in range(n):
            good = 0
            for signs in S:
                if not balance_divisors_exact(n, (0, b), signs, T):
                    good += 1
            predicted_exception = (b % k2 != 0)
            if (good == 0) != predicted_exception:
                ok = False
                print("  MISMATCH", n, b, good)
            nbad += (good == 0)
        if n in (2, 6, 12, 40, 56):
            print(f"  clock {n}: {nbad} of the {n} pairs (0,b) have no good signs; power of 2 in n is {k2}")
    print("  all clocks 1..60 agree with the description:", ok)

    print("== single marks: always good; share of good signs for 3, 4, 5, 6 marks (every multiset containing 0)")


    def shares(n, mmax):
        ds = divisors(n)
        T = {d: rem_table(n, d) for d in ds}
        res = {}
        for m in range(1, mmax + 1):
            S = signs_matrix(m)
            least = None
            arg = None
            cnt = 0
            nogood = 0
            for rest in itertools.combinations_with_replacement(range(n), m - 1):
                marks = (0,) + rest
                cnt += 1
                bad = np.zeros(len(S), dtype=bool)
                for d in ds:
                    v = S @ T[d][list(marks)]
                    bad |= ~v.any(axis=1)
                g = int((~bad).sum())
                if g == 0:
                    nogood += 1
                fr = Fraction(g, len(S))
                if least is None or fr < least:
                    least, arg = fr, marks
            res[m] = (cnt, nogood, least, arg)
        return res


    for n, mmax in ((12, 7), (2, 9), (4, 8), (6, 7), (20, 5), (24, 5), (36, 4), (30, 4), (60, 4), (9, 5), (15, 5)):
        r = shares(n, mmax)
        for m in sorted(r):
            cnt, nogood, least, arg = r[m]
            print(f"  clock {n:2d}, {m} marks: {cnt} markings with a mark at 0, {nogood} without good signs; least share of good signs {least} at {arg}")


if __name__ == "__main__":
    run_checks()
