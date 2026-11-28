# Recursion for the tree of 3 (exact integers) and the check of the tail conditions of result.md, section 2.
# usage: rec3.py M0 R0 a_even a_odd [a_even a_odd ...]
# E[m]/2^m = \hat E_3(m): upper bound for the share of signings bad at some 3^i (i>=1) and not at 1.
import sys, math
from math import comb
from fractions import Fraction
M0 = int(sys.argv[1]); R0 = int(sys.argv[2])
PAIRS = [(float(sys.argv[i]), float(sys.argv[i + 1])) for i in range(3, len(sys.argv) - 1, 2)]
binom = [[comb(r, j) for j in range(r + 1)] for r in range(M0 + 1)]
c = [binom[r][r // 2] if r % 2 == 0 else 0 for r in range(M0 + 1)]   # c(r)*2^r
E = [0] * (M0 + 1); U = [0] * (M0 + 1); arg = [None] * (M0 + 1)
U[1] = c[1]; U[2] = c[2]
EXC = (3, 5, 7)   # Remarks 3.2, 3.3 of quarter/three/result.md
for m in range(3, M0 + 1):
    best = 0; ba = None
    for r2 in range(1, m // 2 + 1):
        r1 = m - r2
        if r1 in EXC and r2 in EXC:
            t = E[r1] * E[r2] // 2
        else:
            t = U[r1] * U[r2] - c[r1] * c[r2]
        if t > best: best = t; ba = (r1, r2)
    for r3 in range(1, m // 3 + 1):
        b3 = binom[r3]; U3 = U[r3]; c3 = c[r3]
        for r2 in range(r3, (m - r3) // 2 + 1):
            r1 = m - r2 - r3
            t = U[r1] * U[r2] * U3 - c[r1] * c[r2] * c3
            if (r1 - r2) % 2 == 0 and (r2 - r3) % 2 == 0:
                b1 = binom[r1]; b2 = binom[r2]; g = 0
                for v in range(2 - r3 % 2, r3 + 1, 2):
                    g += b1[(r1 + v) // 2] * b2[(r2 + v) // 2] * b3[(r3 + v) // 2]
                t += 2 * g
            if t > best: best = t; ba = (r1, r2, r3)
    E[m] = best; U[m] = c[m] + best; arg[m] = ba
def fr(x, r):  # x/2^r as a float (integer true division, correctly rounded)
    return x / (1 << r)
e = [fr(E[r], r) for r in range(M0 + 1)]; u = [fr(U[r], r) for r in range(M0 + 1)]; cf = [fr(c[r], r) for r in range(M0 + 1)]
print("first values E(3..16):", [str(Fraction(E[r], 1 << r)) for r in range(3, 17)])
for par, name in ((0, "even"), (1, "odd")):
    ms = [m for m in range(1, M0 + 1) if m % 2 == par]
    mt = max(ms, key=lambda m: u[m] * math.sqrt(m)); me = max(ms, key=lambda m: e[m] * math.sqrt(m))
    print(f"m {name} <= {M0}: max (c+E)*sqrt(m) = {u[mt]*math.sqrt(mt):.6f} at m={mt} (argmax split {arg[mt]});"
          f" max E*sqrt(m) = {e[me]*math.sqrt(me):.6f} at m={me} (split {arg[me]})")
    big = [m for m in ms if m > M0 // 2]
    print(f"   over {M0//2} < m <= {M0}: max E*sqrt(m) = {max(e[m]*math.sqrt(m) for m in big):.6f};"
          f" max (c+E)*sqrt(m) = {max(u[m]*math.sqrt(m) for m in big):.6f}")
# exact: is (c+E)(m) <= 1/sqrt(m), i.e. U[m]^2 * m <= 4^m, for every m <= M0 ?
print(f"exact check (c+E)(m)^2 * m <= 1 for every 1 <= m <= {M0}:", all(U[m] * U[m] * m <= (1 << (2 * m)) for m in range(1, M0 + 1)))
print(f"exact check (c+E)(m)^2 * m <= 0.95^2 for every 1 <= m <= {M0}:", all(U[m] * U[m] * m * 10000 <= 9025 * (1 << (2 * m)) for m in range(1, M0 + 1)))
for m in (4, 6, 8, 10, 12, 20, 30, 50, 100, 101, 200, 201, 500, 501, M0 - 1, M0):
    if m <= M0: print(f"   m={m}: E*sqrt(m)={e[m]*math.sqrt(m):.6f} (c+E)*sqrt(m)={u[m]*math.sqrt(m):.6f} split {arg[m]}")
oddok = all(E[m] == 2 * binom[m - 2][(m - 1) // 2] for m in range(5, M0 + 1, 2))
print(f"odd 5 <= m <= {M0}: E(m) = (1/2)*C(m-2,(m-1)/2)/2^(m-2) exactly, every time: {oddok}")
with open(f"table3-{M0}.txt", "w") as f:
    for m in range(1, M0 + 1): f.write(f"{m} {E[m]:x} {arg[m]}\n")
# ---- tail conditions ----
kap = math.sqrt(2 / math.pi)
wq = max(fr(binom[r][r // 2], r) * math.sqrt(r) / kap for r in range(1, M0 + 1))
print(f"max q(r)sqrt(r)/kappa on the table = {wq:.6f}")
def sig(s): return math.sqrt((M0 + 1) / (M0 + 1 - s))
for (a_ev, a_od) in PAIRS:
    a = (a_ev, a_od); amax = max(a); amin = min(a); ok = True
    # (T0) table
    w = max(e[r] * math.sqrt(r) / a[r % 2] for r in range(1, M0 + 1))
    print(f"(T0) max over r<=M0 of E(r)*sqrt(r)/a_par(r) = {w:.6f}"); ok &= (w <= 1)
    # (T2s) two classes, small second class
    worst = 0; wa = None
    for r2 in range(1, R0 + 1):
        for p1 in (0, 1):
            pm = (p1 + r2) % 2
            val = sig(r2) * (a[p1] * u[r2] + (kap if p1 == 0 else 0.0) * e[r2]) / a[pm]
            if val > worst: worst = val; wa = (r2, p1)
    print(f"(T2s) worst ratio = {worst:.6f} at (r2, parity of r1) = {wa}"); ok &= (worst <= 1)
    # (T2l) two classes, r2 > R0
    val = math.sqrt(2) * amax * (2 * kap + amax) / math.sqrt(R0) / amin
    print(f"(T2l) ratio <= {val:.6f}"); ok &= (val <= 1)
    # (T3s) three classes, r2 + r3 <= R0
    worst = 0; wa = None
    for r3 in range(1, R0 // 2 + 1):
        for r2 in range(r3, R0 - r3 + 1):
            for p1 in (0, 1):
                pm = (p1 + r2 + r3) % 2
                flag = 1.0 if ((r2 - r3) % 2 == 0 and (r2 - p1) % 2 == 0) else 0.0
                val = kap * flag * (cf[r2 + r3] - cf[r2] * cf[r3]) + a[p1] * u[r2] * u[r3] + (kap if p1 == 0 else 0.0) * (u[r2] * u[r3] - cf[r2] * cf[r3])
                val = sig(r2 + r3) * val / a[pm]
                if val > worst: worst = val; wa = (r2, r3, p1)
    print(f"(T3s) worst ratio = {worst:.6f} at (r2, r3, parity of r1) = {wa}"); ok &= (worst <= 1)
    # (T3l) three classes, r2 + r3 > R0
    den = min(2 * M0 / 9, R0 * (1 - R0 / M0))
    val = (kap * kap / math.sqrt(den) + math.sqrt(3) * (amax + kap) ** 2 / math.sqrt(R0 / 2) / 2) / amin
    print(f"(T3l) ratio <= {val:.6f}"); ok &= (val <= 1)
    print("TAIL CONDITIONS", "ALL HOLD" if ok else "FAIL", f"for M0={M0} R0={R0} a_even={a_ev} a_odd={a_od}; kappa+a_even = {kap+a_ev:.6f}")
