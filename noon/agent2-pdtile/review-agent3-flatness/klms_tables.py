"""Independent reading of the two tables in the proof of [KLMS, Theorem 1.6] (arXiv:2411.03854, TeX source),
typed in by agent3 / Yonder from Final_version.tex lines 834-876, and checked:
  * which orders the functions vanish on (compare with the two lists in flatness.md, Corollary);
  * f, g >= 0 for p < q < p^2;
  * f^ = p^2 q f and g^ = p^2 q g, (a) by a plain FFT over Z_M in floating point, (b) exactly, with the
    transform of a step class written as a Ramanujan sum evaluated by its definition-free divisor formula.
Row alpha, column beta of a table is the value on the elements of order p^alpha q^beta."""
import numpy as np
from fractions import Fraction as Fr
from math import gcd

def divisors(n): return [d for d in range(1, n + 1) if n % d == 0] if n < 10**6 else sorted({d for i in range(1, int(n**0.5) + 1) if n % i == 0 for d in (i, n // i)})
def mobius(n):
    m, k = 1, 2
    while k * k <= n:
        if n % k == 0:
            n //= k
            if n % k == 0: return 0
            m = -m
        k += 1
    return -m if n > 1 else m
def primerange(a, b): return [n for n in range(max(a, 2), b) if all(n % k for k in range(2, int(n**0.5) + 1))]

def tables(p, q):
    phi = lambda n, pr: n - n // pr                      # phi of a prime power n = pr^k (and phi(pr) for k = 1)
    fq, fq2, fp = q - 1, q * (q - 1), p - 1
    d = 2 * p * q - p * p - q
    f = [[1, 0, Fr(q - p, fq2)],
         [0, Fr(1, fq), Fr(q - p, fq2)],
         [Fr(q * q - p * q + p * p - q, p * fq2), Fr(p * p - q, p * fq2), 0],
         [Fr(q - p, p * fq), 0, 0],
         [0, 0, Fr(1, p * p * fq)]]
    g = [[1, Fr(p * (q - p), d), 0],
         [Fr(q * fp, d), 0, 0],
         [0, 0, Fr(1, d)],
         [0, Fr(q, p * d), Fr(fp, p * d)],
         [Fr(q - p, p * d), Fr(q - p, p * d), 0]]
    return f, g

def name(a, b):
    s = []
    if a: s.append("p" + (f"^{a}" if a > 1 else ""))
    if b: s.append("q" + (f"^{b}" if b > 1 else ""))
    return "".join(s) or "1"

def ramanujan(d, n):                                     # sum over elements z of order d of exp(-2 pi i z n / d ...)
    return sum(int(mobius(d // e)) * e for e in divisors(gcd(d, n)))

LIST_F = {(1, 0), (0, 1), (4, 0), (3, 1), (4, 1), (2, 2), (3, 2)}      # flatness.md: p, q, p^4, p^3q, p^4q, p^2q^2, p^3q^2
LIST_G = {(2, 0), (3, 0), (0, 2), (1, 1), (2, 1), (1, 2), (4, 2)}      # p^2, p^3, q^2, pq, p^2q, pq^2, p^4q^2
pairs = [(p, q) for p in primerange(2, 14) for q in primerange(p + 1, p * p)]
worst = 0.0
for p, q in pairs:
    M = p ** 4 * q ** 2
    f, g = tables(p, q)
    for T, L, nm in ((f, LIST_F, "f"), (g, LIST_G, "g")):
        assert all(T[a][b] >= 0 for a in range(5) for b in range(3)), (p, q, nm, "negative value")
        zeros = {(a, b) for a in range(5) for b in range(3) if T[a][b] == 0}
        assert zeros == L, (p, q, nm, zeros)
        # exact: value of the transform on the elements of order p^a' q^b'  (xi = M / order is one such element)
        tot = sum(T[a][b] * (p ** a - p ** a // p if a else 1) * (q ** b - q ** b // q if b else 1) for a in range(5) for b in range(3))
        assert tot == p * p * q, (p, q, nm, tot)
        for a2 in range(5):
            for b2 in range(3):
                xi = M // (p ** a2 * q ** b2)
                val = sum(T[a][b] * ramanujan(p ** a * q ** b, xi) for a in range(5) for b in range(3))
                assert val == p * p * q * T[a2][b2], (p, q, nm, a2, b2)
        if M <= 3_000_000:                               # plain FFT, no step-function formula
            z = np.arange(M); gp = np.gcd(z, p ** 4); gq = np.gcd(z, q ** 2)
            ia = np.round(np.log(p ** 4 // gp) / np.log(p)).astype(int); ib = np.round(np.log(q ** 2 // gq) / np.log(q)).astype(int)
            arr = np.array([[float(T[a][b]) for b in range(3)] for a in range(5)])[ia, ib]
            F = np.fft.fft(arr)
            worst = max(worst, np.abs(F - p * p * q * arr).max())
print(f"{len(pairs)} prime pairs p < q < p^2, p <= 13: both tables nonnegative; zero sets are exactly the two lists;")
print(f"total weight p^2 q; f^ = p^2 q f and g^ = p^2 q g exactly (Ramanujan sums); FFT check, largest error {worst:.1e}")
print("f zero orders:", sorted(name(a, b) for a, b in LIST_F)); print("g zero orders:", sorted(name(a, b) for a, b in LIST_G))
# the conditions are needed: outside p < q < p^2 something goes negative
for p, q in ((2, 5), (3, 2), (2, 7), (3, 11)):
    f, g = tables(p, q)
    print(p, q, "min f", min(min(r) for r in f), "min g", min(min(r) for r in g))
