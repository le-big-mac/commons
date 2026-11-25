"""Referee check of the Corollary's reading of the two tables of [KLMS, Thm 1.6].

Tables transcribed by the referee directly from Final_version.tex lines 833-877 (not from the document
under review). Rows alpha = 0..4 (M/p^alpha), columns beta = 0..2 (M/q^beta); entry = value on the
step class R_{M/(p^alpha q^beta)}, i.e. on the elements of order p^alpha q^beta.

Checks, for each admissible prime pair p < q < p^2:
  * f, g >= 0, f(0) = g(0) = 1;
  * f^ = p^2 q f and g^ = p^2 q g (exactly, with Fractions, transform computed class by class from
    Ramanujan sums; and for small M also by a brute-force numpy FFT over the whole group);
  * the list of orders d on which each vanishes; that the two lists partition the divisors > 1 of M;
  * the two lists contain the hypotheses of Lemma A and Lemma B respectively.
"""
from fractions import Fraction as Fr
import math
import sys

import numpy as np


def tables(p, q):
    php, phq, phq2 = p - 1, q - 1, q * (q - 1)
    f = [
        [Fr(1), Fr(0), Fr(q - p, phq2)],
        [Fr(0), Fr(1, phq), Fr(q - p, phq2)],
        [Fr(q * q - p * q + p * p - q, p * phq2), Fr(p * p - q, p * phq2), Fr(0)],
        [Fr(q - p, p * phq), Fr(0), Fr(0)],
        [Fr(0), Fr(0), Fr(1, p * p * phq)],
    ]
    d = 2 * p * q - p * p - q
    g = [
        [Fr(1), Fr(p * (q - p), d), Fr(0)],
        [Fr(q * php, d), Fr(0), Fr(0)],
        [Fr(0), Fr(0), Fr(1, d)],
        [Fr(0), Fr(q, p * d), Fr(php, p * d)],
        [Fr(q - p, p * d), Fr(q - p, p * d), Fr(0)],
    ]
    return f, g


def ram(p, n, a, a2):
    """sum over x in Z_{p^n} of order p^a of exp(2 pi i x xi / p^n), xi of order p^a2.
    = Ramanujan sum c_{p^a}(p^(n-a2))."""
    if a == 0:
        return 1
    k = n - a2  # xi = p^k * unit
    if a <= k:
        return (p - 1) * p ** (a - 1)
    if a == k + 1:
        return -p ** (a - 1)
    return 0


def ram_bruteforce(p, n, a, a2):
    N = p ** n
    xi = p ** (n - a2)
    s = 0
    for x in range(N):
        if N // math.gcd(x, N) == p ** a:
            s += np.exp(2j * np.pi * x * xi / N)
    return s


def transform(tab, p, q):
    out = [[Fr(0)] * 3 for _ in range(5)]
    for a2 in range(5):
        for b2 in range(3):
            s = Fr(0)
            for a in range(5):
                for b in range(3):
                    s += tab[a][b] * ram(p, 4, a, a2) * ram(q, 2, b, b2)
            out[a2][b2] = s
    return out


def zero_orders(tab, p, q):
    return sorted(p ** a * q ** b for a in range(5) for b in range(3) if tab[a][b] == 0)


def fft_check(tab, p, q):
    M = p ** 4 * q ** 2
    v = np.zeros(M)
    for x in range(M):
        o = M // math.gcd(x, M)
        a = 0
        while o % p == 0:
            o //= p
            a += 1
        b = 0
        while o % q == 0:
            o //= q
            b += 1
        v[x] = float(tab[a][b])
    F = np.fft.fft(v)
    return float(np.max(np.abs(F - p * p * q * v)))


def main():
    # Ramanujan-sum formula against brute force
    for (p, n) in ((2, 4), (3, 2), (3, 4), (5, 2)):
        for a in range(n + 1):
            for a2 in range(n + 1):
                assert abs(ram_bruteforce(p, n, a, a2) - ram(p, n, a, a2)) < 1e-8, (p, n, a, a2)
    print("Ramanujan-sum formula agrees with brute force")

    primes = [x for x in range(2, 60) if all(x % k for k in range(2, x))]
    pairs = [(p, q) for p in primes for q in primes if p < q < p * p]
    allok = True
    for (p, q) in pairs:
        f, g = tables(p, q)
        M = p ** 4 * q ** 2
        ev = p * p * q
        ok = f[0][0] == 1 and g[0][0] == 1
        ok &= all(v >= 0 for row in f for v in row) and all(v >= 0 for row in g for v in row)
        fh, gh = transform(f, p, q), transform(g, p, q)
        ok &= all(fh[a][b] == ev * f[a][b] for a in range(5) for b in range(3))
        ok &= all(gh[a][b] == ev * g[a][b] for a in range(5) for b in range(3))
        zf, zg = zero_orders(f, p, q), zero_orders(g, p, q)
        listA = sorted([p, q, p ** 4, p ** 3 * q, p ** 4 * q, p ** 2 * q ** 2, p ** 3 * q ** 2])
        listB = sorted([p ** 2, p ** 3, q ** 2, p * q, p ** 2 * q, p * q ** 2, p ** 4 * q ** 2])
        ok &= zf == listA and zg == listB
        alld = sorted(p ** a * q ** b for a in range(5) for b in range(3) if (a, b) != (0, 0))
        ok &= sorted(zf + zg) == alld
        lemA = {q, p ** 4, p ** 4 * q, p ** 3 * q, p ** 3 * q ** 2, p ** 2 * q ** 2}
        lemB = {p ** 2, p ** 3, q ** 2, p * q, p * q ** 2, p ** 2 * q}
        ok &= lemA <= set(zf) and lemB <= set(zg)
        extra = ""
        if M <= 40000:
            e1, e2 = fft_check(f, p, q), fft_check(g, p, q)
            ok &= e1 < 1e-7 and e2 < 1e-7
            extra = f" FFT residuals {e1:.1e}, {e2:.1e}"
        allok &= ok
        if (p, q) in ((2, 3), (3, 5), (3, 7), (5, 7)) or not ok:
            print(f"(p,q)=({p},{q}) M={M}: ok={ok} zeros(f)={zf} zeros(g)={zg}{extra}")
    print(f"{len(pairs)} prime pairs with p<q<p^2, p,q<60: all checks pass = {allok}")

    # outside the range p<q<p^2 the tables should break (sanity of the 'exactly' in the Corollary)
    for (p, q) in ((2, 5), (2, 7), (3, 11), (3, 2)):
        f, g = tables(p, q)
        neg = any(v < 0 for row in f for v in row) or any(v < 0 for row in g for v in row)
        fh = transform(f, p, q)
        eig = all(fh[a][b] == p * p * q * f[a][b] for a in range(5) for b in range(3))
        print(f"outside range ({p},{q}): some entry negative = {neg}; f still an eigenfunction = {eig}; "
              f"zeros(f) = {zero_orders(f, p, q)}")


if __name__ == "__main__":
    main()
