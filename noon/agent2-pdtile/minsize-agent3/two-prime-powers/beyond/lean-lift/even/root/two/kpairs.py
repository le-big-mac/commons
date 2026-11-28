# Supplementary data (not used in any proof): the constant K_same of the brief for decorations made of PAIRS, computed
# by my own route: for every configuration of the pair sums (each -2, 0, 2 with weights 1, 2, 1) the integer values
# among Q(zeta_d), d | n, are found by integer long division by Phi_d; K = expected number of distinct such values.
# usage: kpairs.py [pp] n r1 r2 ...   (each residue stands for a pair; with pp: only d = 1 and prime powers)
import sys, itertools
from fractions import Fraction
import numpy as np
PP = (sys.argv[1] == 'pp')          # 'pp' as first argument: only d = 1 and the prime powers d | n
if PP: del sys.argv[1]
n = int(sys.argv[1]); res = [int(x) % n for x in sys.argv[2:]]; r = len(res)
def is_pp(d):
    f = [q for q in range(2, d + 1) if d % q == 0 and all(q % t for t in range(2, q))]
    return len(f) <= 1
def polydiv_exact(num, den):
    num = num[:]; q = [0] * (len(num) - len(den) + 1)
    for i in range(len(num) - len(den), -1, -1):
        q[i] = num[i + len(den) - 1]
        for j, dj in enumerate(den): num[i + j] -= q[i] * dj
    assert all(v == 0 for v in num); return q
PHI = {}
def phi(d):
    if d not in PHI:
        num = [-1] + [0] * (d - 1) + [1]
        for e in range(1, d):
            if d % e == 0: num = polydiv_exact(num, phi(e))
        PHI[d] = num
    return PHI[d]
N = 3 ** r
idx = np.indices((3,) * r).reshape(r, N)                 # 0,1,2 -> sums -2,0,2
W = np.ones(N, dtype=np.int64)
V = np.zeros((N, n), dtype=np.int64)
for i, b in enumerate(res):
    V[:, b] += 2 * (idx[i] - 1); W *= np.where(idx[i] == 1, 2, 1)
vals = []
for d in [d for d in range(1, n + 1) if n % d == 0 and (not PP or is_pp(d))]:
    Vd = np.zeros((N, d), dtype=np.int64)
    for c in range(n): Vd[:, c % d] += V[:, c]
    ph = np.array(phi(d), dtype=np.int64); k = len(ph) - 1
    for deg in range(d - 1, k - 1, -1):
        co = Vd[:, deg].copy(); Vd[:, deg - k:deg + 1] -= co[:, None] * ph[None, :]
    isint = ~Vd[:, 1:k].any(axis=1) if k > 1 else np.ones(N, dtype=bool)
    vals.append(np.where(isint, Vd[:, 0], 10 ** 6))
M = np.sort(np.array(vals), axis=0)
distinct = np.ones_like(M, dtype=bool); distinct[1:] = M[1:] != M[:-1]
cnt = ((M != 10 ** 6) & distinct).sum(axis=0)
K = Fraction(int((cnt * W).sum()), 4 ** r)
print(("prime-power divisors only: " if PP else "") + f"Z_{n}, pairs at {sorted(res)}: K_same = {K} = {float(K):.6f}; times sqrt(2/pi): {float(K) * 0.7978845608:.6f}")
