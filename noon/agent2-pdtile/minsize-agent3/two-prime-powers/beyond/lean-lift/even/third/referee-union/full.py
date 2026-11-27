# Referee's second look: full support (every residue of Z_n once, every coefficient a sign).
# Imports nothing of the author's and nothing of the search's.  Exact integers.
#   a(n)  = number of the 2^n signings bad on Z_n            (printed: OEIS A144926)
#   F(n)  = number bad for the reduction modulo the odd part of n
#   and, for every 2^m | n (m >= 1):
#   c(m)  = number of signings with Phi_(2^m) | S            (by remainders)
#   z(m)  = number of signings in which every class modulo 2^(m-1) has sign sum 0
#   f5(m) = 2^n * ( sum_k (C(N,k)/2^N)^2 )^(2^(m-1)),  N = n/2^m   (formula (5) of the 2024 preprint, p = 2, q = 1/2)
# usage: full.py n [n ...]   (n even)
import sys
from fractions import Fraction as Fr
from math import comb
import numpy as np
from cyc import divisors, v2, xpow_mod

def run(n):
    k = v2(n); n1 = n >> k
    dn, do = divisors(n), divisors(n1)
    b = np.arange(n)
    cols, lab = [], []
    for d in dn:
        cols.append(np.array(xpow_mod(d, n), dtype=np.int64).reshape(n, -1)); lab.append(("A", d))
    for e in do:
        r1 = np.array(xpow_mod(e, n1), dtype=np.int64).reshape(n1, -1)
        cols.append(r1[b % n1]); lab.append(("O", e))
    for m in range(1, k + 1):                      # class sums modulo 2^(m-1)
        cols.append((b[:, None] % 2 ** (m - 1) == np.arange(2 ** (m - 1))[None, :]).astype(np.int64)); lab.append(("Z", m))
    T = np.concatenate(cols, axis=1)
    starts = np.cumsum([0] + [c.shape[1] for c in cols])[:-1]
    iA = [i for i, l in enumerate(lab) if l[0] == "A"]
    iO = [i for i, l in enumerate(lab) if l[0] == "O"]
    half = 1 << (n - 1)                             # first sign +; every event is kept by the global sign
    a = F = 0
    c = {m: 0 for m in range(1, k + 1)}
    z = {m: 0 for m in range(1, k + 1)}
    step = 1 << 15
    for s0 in range(0, half, step):
        s = np.arange(s0, min(half, s0 + step), dtype=np.int64)
        sg = np.ones((len(s), n), dtype=np.int64)
        for i in range(n - 1):
            sg[:, i + 1] = 1 - 2 * ((s >> i) & 1)
        R = sg @ T
        Z = np.add.reduceat((R != 0).astype(np.int32), starts, axis=1) == 0
        a += int(Z[:, iA].any(axis=1).sum())
        F += int(Z[:, iO].any(axis=1).sum())
        for m in range(1, k + 1):
            c[m] += int(Z[:, lab.index(("A", 2 ** m))].sum())
            z[m] += int(Z[:, lab.index(("Z", m))].sum())
    out = f"n={n:2d}  a(n)={2*a}  F(n)={2*F}  a<=2F: {a <= 2*F}"
    for m in range(1, k + 1):
        N = n >> m
        f5 = 2 ** n * sum(Fr(comb(N, j), 2 ** N) ** 2 for j in range(N + 1)) ** (2 ** (m - 1))
        ok = (2 * c[m] == 2 * z[m] == f5)
        out += f"  | m={m}: Phi_{2**m} divides S in {2*c[m]}, every class mod {2**(m-1)} sums to 0 in {2*z[m]}, formula (5) gives {f5}: {'equal' if ok else 'DIFFER'}"
    print(out, flush=True)

# the identification needs q = 1/2: for signs + with probability q, n = 4, m = 1 (N = 2)
q = Fr(1, 3)
phi = lambda j, N: comb(N, j) * q ** j * (1 - q) ** (N - j)
print("q = 1/3, n = 4, m = 1: formula (5) =", sum(phi(j, 2) ** 2 for j in range(3)),
      "; P(the four signs sum to 0) =", comb(4, 2) * q ** 2 * (1 - q) ** 2, " (they differ: q = 1/2 is needed)")
for n in map(int, sys.argv[1:]):
    run(n)
