#!/usr/bin/env python3
"""W(no 3) = sum over the integers e* > 1 with all prime factors >= 5 of 2^(-mu(e*)), mu(e*) = max_q v_q(e*) (q - 1);
and the numbers p_r and the arithmetic of Corollary 3.  A reader's recomputation, exact fractions.

A(t) = #{e* >= 1, prime factors >= 5, mu(e*) <= t} = prod over primes 5 <= p <= t + 1 of (1 + floor(t / (p - 1))).
W(no 3) = sum over even t >= 4 of (A(t) - A(t - 2)) 2^(-t).
Tail: A(t) 2^(-t) <= (u + 1) x^u, u = t / 2, x = exp(2K/3)/4, K = sum_k ln(1 + 1/k)/k  (the bound of Lemma W of
sign-four-result.md for all odd d, which contains these e*); checked here term by term up to t = 400 as well.
"""
from fractions import Fraction
from math import log, exp


def primes_upto(n):
    s = [True] * (n + 1)
    s[0:2] = [False, False]
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            for j in range(i * i, n + 1, i):
                s[j] = False
    return [i for i in range(n + 1) if s[i]]


PR = primes_upto(2000)


def A(t):
    out = 1
    for p in PR:
        if p < 5:
            continue
        if p > t + 1:
            break
        out *= 1 + t // (p - 1)
    return out


def partial(tmax):
    s = Fraction(0)
    for t in range(4, tmax + 1, 2):
        s += Fraction(A(t) - A(t - 2), 2 ** t)
    return s


def main():
    # 1. the product formula against a direct list: every e <= N with prime factors >= 5, mu from its factorisation
    N = 2_000_000
    spf = list(range(N + 1))
    for i in range(2, int(N ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, N + 1, i):
                if spf[j] == j:
                    spf[j] = i
    count = {}
    direct = Fraction(0)
    for e in range(5, N + 1):
        if e % 2 == 0 or e % 3 == 0:
            continue
        x = e
        mu = 0
        while x > 1:
            p = spf[x]
            v = 0
            while x % p == 0:
                x //= p
                v += 1
            mu = max(mu, v * (p - 1))
        count[mu] = count.get(mu, 0) + 1
        direct += Fraction(1, 2 ** mu) if mu <= 60 else 0
    # all e* with mu <= 12 are below 5^3 7^2 11 13 = 875875 < N
    for t in range(4, 13, 2):
        listed = 1 + sum(c for mu, c in count.items() if mu <= t)
        assert listed == A(t), (t, listed, A(t))
    print("product formula A(t) against a list of all e <= %d: equal for t = 4, ..., 12: %s"
          % (N, [A(t) for t in range(4, 13, 2)]))
    print("sum of 2^(-mu(e)) over the e <= %d listed (a lower bound): %.10f" % (N, float(direct)))
    # 2. partial sums
    for tmax in (40, 60, 100, 400):
        print("partial sum up to t = %3d: %.12f" % (tmax, float(partial(tmax))))
    s60 = partial(60)
    # 3. the tail after t = 60
    Kpart = sum(log(1 + 1 / k) / k for k in range(1, 2000))
    K = Kpart + 1 / 1999 + 1e-9
    x = exp(2 * K / 3) / 4 * (1 + 1e-12)
    tail = x ** 31 * (32 - 31 * x) / (1 - x) ** 2
    print("K < %.7f, x < %.6f, tail after t = 60 below %.3e" % (K, x, tail))
    worst = max(A(t) / 2 ** t / ((t // 2 + 1) * x ** (t // 2)) for t in range(4, 401, 2))
    print("A(t) 2^(-t) / ((u+1) x^u), largest over t <= 400: %.4f (must be <= 1)" % worst)
    assert worst <= 1
    upper = float(s60) + tail
    print("W(no 3) < %.9f ; claimed < 0.118569: %s" % (upper, upper < 0.118569))
    assert s60 < Fraction(118564699, 10 ** 9)
    assert upper < 0.118569
    assert 2 * upper < 0.2372
    # 4. the numbers p_r and the arithmetic of Corollary 3
    p = [Fraction(1)]
    for r in range(60):
        p.append((1 - p[-1]) / 2)
    assert p[:8] == [1, 0, Fraction(1, 2), Fraction(1, 4), Fraction(3, 8), Fraction(5, 16), Fraction(11, 32),
                     Fraction(21, 64)]
    for r in range(60):
        assert p[r] - Fraction(1, 3) == Fraction(2, 3) * Fraction(-1, 2) ** r
    assert 2 * p[3] == Fraction(1, 2) and 2 * p[4] == Fraction(3, 4)
    assert all(p[m] <= Fraction(11, 32) for m in range(5, 60))
    assert all(p[m - 1] >= Fraction(5, 16) for m in range(5, 60))
    assert all(2 * p[m] == 1 - p[m - 1] for m in range(1, 60))
    assert 2 * Fraction(11, 32) + Fraction(2372, 10000) < Fraction(925, 1000)
    assert Fraction(5, 16) - Fraction(2372, 10000) > Fraction(75, 1000)
    print("2 (11/32) + 0.2372 = %s < 0.925 ; 5/16 - 0.2372 = %s > 0.075"
          % (float(2 * Fraction(11, 32) + Fraction(2372, 10000)), float(Fraction(5, 16) - Fraction(2372, 10000))))
    print("p_r, 2 p_3 = 1/2, 2 p_4 = 3/4, p_m <= 11/32 and p_(m-1) >= 5/16 for 5 <= m < 60, 2 p_m = 1 - p_(m-1): right")


if __name__ == "__main__":
    main()
