# Referee's own recomputation of the table \hat E(m) (p = 3), 3 <= m <= M, written from the definitions of
# sections 2 and 3 of two/result.md (not from the author's code).
#   \hat E(m) = max over the size patterns of the first split of the bound of Lemma 2:
#     two classes  r1 >= r2 >= 1:        u(r1)u(r2) - c(r1)c(r2)          (u = c + \hat E)
#                  except r1, r2 in {3,5,7}:  \hat E(r1) \hat E(r2) / 2   (the text's (e))
#     three classes r1 >= r2 >= r3 >= 1: g(r1,r2,r3) + u(r1)u(r2)u(r3) - c(r1)c(r2)c(r3),
#                  g = sum over v != 0 of P(S_r1 = v) P(S_r2 = v) P(S_r3 = v).
# Method: every split is evaluated in float64 (all terms positive, relative error far below 1e-12); the splits
# within a relative 1e-9 of the float maximum are then evaluated in exact integers and the exact maximum is kept.
# So the float pass only discards splits that are certainly not maximal; the table itself is exact.
# usage: mytable3.py M [author's table file to compare with]
import sys, time
import numpy as np
from math import comb
from fractions import Fraction

M = int(sys.argv[1])
t0 = time.time()
B = [[1]]
for r in range(1, M + 1):
    prev = B[-1]
    B.append([1] + [prev[i] + prev[i + 1] for i in range(r - 1)] + [1])
Cx = [B[r][r // 2] if r % 2 == 0 else 0 for r in range(M + 1)]      # c(r) 2^r
Ex = [Fraction(0)] * (M + 1)                                          # \hat E(r) 2^r  (Fractions, to be safe)
Ux = [Fraction(Cx[r]) for r in range(M + 1)]
P = np.zeros((M + 1, M + 2))
for r in range(M + 1):
    two = 1 << r
    row = B[r]
    for v in range(r % 2, r + 1, 2):
        P[r, v] = row[(r + v) // 2] / two
cf = P[:, 0].copy(); ef = np.zeros(M + 1); uf = cf.copy()
EXC = (3, 5, 7)

def exact(split):
    m = sum(split)
    if len(split) == 2:
        r1, r2 = split
        if r1 in EXC and r2 in EXC:
            return Ex[r1] * Ex[r2] / 2
        return Ux[r1] * Ux[r2] - Cx[r1] * Cx[r2]
    r1, r2, r3 = split
    t = Ux[r1] * Ux[r2] * Ux[r3] - Cx[r1] * Cx[r2] * Cx[r3]
    if (r1 - r2) % 2 == 0 and (r2 - r3) % 2 == 0:
        g = 0
        for v in range(-r3, r3 + 1):
            if v != 0 and (v - r3) % 2 == 0:
                g += B[r1][(r1 + v) // 2] * B[r2][(r2 + v) // 2] * B[r3][(r3 + v) // 2]
        t += g
    return t

arg = [None] * (M + 1); ncand = 0; nsplit = 0
for m in range(3, M + 1):
    vals = []; sp = []
    r2 = np.arange(1, m // 2 + 1); r1 = m - r2
    v2 = uf[r1] * uf[r2] - cf[r1] * cf[r2]
    for i in range(len(r2)):
        if int(r1[i]) in EXC and int(r2[i]) in EXC:
            v2[i] = ef[r1[i]] * ef[r2[i]] / 2
    vals.append(v2); sp.append(np.stack([r1, r2, np.zeros_like(r2)], axis=1))
    for r3 in range(1, m // 3 + 1):
        r2 = np.arange(r3, (m - r3) // 2 + 1); r1 = m - r3 - r2
        v3 = uf[r1] * uf[r2] * uf[r3] - cf[r1] * cf[r2] * cf[r3]
        if (m - r3) % 2 == 0:
            idx = np.nonzero((r2 - r3) % 2 == 0)[0]
            if len(idx):
                vs = np.arange(2 - r3 % 2, r3 + 1, 2)
                A = P[r1[idx][:, None], vs[None, :]] * P[r2[idx][:, None], vs[None, :]]
                v3[idx] += 2.0 * (A @ P[r3, vs])
        vals.append(v3); sp.append(np.stack([r1, r2, np.full_like(r2, r3)], axis=1))
    vals = np.concatenate(vals); sp = np.concatenate(sp); nsplit += len(vals)
    fmax = vals.max()
    best = Fraction(0); ba = None
    if fmax > 0:
        for i in np.nonzero(vals >= fmax * (1 - 1e-9) - 1e-300)[0]:
            s = tuple(int(x) for x in sp[i] if x > 0)
            t = exact(s); ncand += 1
            if t > best: best = t; ba = s
    Ex[m] = best; Ux[m] = Cx[m] + best; arg[m] = ba
    ef[m] = float(best / (1 << m)); uf[m] = float(Ux[m] / (1 << m))
    assert abs(ef[m] - fmax) <= 1e-9 * max(fmax, 1e-300) + 1e-300, (m, ef[m], fmax)
print(f"table to M = {M}: {nsplit} splits evaluated in floats, {ncand} candidates evaluated exactly; {time.time()-t0:.0f} s")
assert all(x.denominator == 1 for x in Ex)
E = [int(x) for x in Ex]; U = [int(x) for x in Ux]
with open(f"mytable3-{M}.txt", "w") as f:
    for m in range(1, M + 1): f.write(f"{m} {E[m]:x} {arg[m]}\n")
print("E(3..16):", [str(Fraction(E[r], 1 << r)) for r in range(3, min(M, 16) + 1)])
# exact statements of section 3
def sq_le(m, num, den):       # (U[m]/2^m)^2 * m <= (num/den)^2 ?
    return U[m] * U[m] * m * den * den <= num * num * (1 << (2 * m))
print("exact: (c+E)^2 m <= 0.9487^2 for every even m <= M:", all(sq_le(m, 9487, 10000) for m in range(2, M + 1, 2)))
print("exact: (c+E)^2 m <= 0.948695^2 for every even m <= M:", all(sq_le(m, 948695, 1000000) for m in range(2, M + 1, 2)))
print("exact: (c+E)^2 m <= 0.948694^2 for every even m <= M:", all(sq_le(m, 948694, 1000000) for m in range(2, M + 1, 2)))
print("exact: (c+E)^2 m <= 0.4331^2 for every odd m <= M:", all(sq_le(m, 4331, 10000) for m in range(1, M + 1, 2)))
print("exact: (c+E)^2 m <= 1 for every m <= M:", all(sq_le(m, 1, 1) for m in range(1, M + 1)))
print("exact: u(r) = c(r)+E(r) <= 1/2 for every r <= M:", all(2 * U[r] <= (1 << r) for r in range(1, M + 1)),
      "; u(r) <= 3/8 for 3 <= r <= M:", all(8 * U[r] <= 3 * (1 << r) for r in range(3, M + 1)))
odd_ok = [m for m in range(5, M + 1, 2) if E[m] != 2 * B[m - 2][(m - 1) // 2]]
print("odd 5 <= m <= M with E(m) != (1/2) q(m-2):", odd_ok)
import math
def f(x, r): return x / (1 << r)
for par, name in ((0, "even"), (1, "odd")):
    ms = [m for m in range(1, M + 1) if m % 2 == par]
    mt = max(ms, key=lambda m: Fraction(U[m] * U[m] * m, 1 << (2 * m)))
    me = max(ms, key=lambda m: Fraction(E[m] * E[m] * m, 1 << (2 * m)))
    print(f"{name} m <= {M}: max (c+E) sqrt(m) = {f(U[mt], mt)*math.sqrt(mt):.6f} at m = {mt} (split {arg[mt]}); max E sqrt(m) = {f(E[me], me)*math.sqrt(me):.6f} at m = {me} (split {arg[me]})")
    ms2 = [m for m in ms if m > 200]
    if ms2:
        me = max(ms2, key=lambda m: Fraction(E[m] * E[m] * m, 1 << (2 * m)))
        print(f"   200 < m <= {M}: max E sqrt(m) = {f(E[me], me)*math.sqrt(me):.6f} at m = {me}")
for m in (100, 200, 500, 1000):
    if m <= M: print(f"   m = {m}: (c+E) sqrt(m) = {f(U[m], m)*math.sqrt(m):.4f}, E sqrt(m) = {f(E[m], m)*math.sqrt(m):.6f}, split {arg[m]}")
if len(sys.argv) > 2:
    diff = []; n = 0
    for line in open(sys.argv[2]):
        w = line.split(); m = int(w[0])
        if m <= M:
            n += 1
            if int(w[1], 16) != E[m]: diff.append(m)
    print(f"compared with the author's table on {n} values of m: differing m = {diff}")
