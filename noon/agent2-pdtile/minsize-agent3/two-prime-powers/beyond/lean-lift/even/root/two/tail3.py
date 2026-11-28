# Tail conditions of section 3 of result.md, in the sharper form of Remark 3.1: the claim e_3(m) <= a_par/sqrt(m) is
# made only for m > R1 = R0/2; sizes up to R0 are taken from the exact table.  Reads table3-M0.txt (made by rec3.py).
# usage: tail3.py M0 R0 a_even a_odd [a_even a_odd ...]
import sys, math
from math import comb
M0 = int(sys.argv[1]); R0 = int(sys.argv[2]); R1 = R0 // 2
PAIRS = [(float(sys.argv[i]), float(sys.argv[i + 1])) for i in range(3, len(sys.argv) - 1, 2)]
E = [0] * (M0 + 1)
for line in open(f"table3-{M0}.txt"):
    w = line.split(); E[int(w[0])] = int(w[1], 16)
c = [comb(r, r // 2) if r % 2 == 0 else 0 for r in range(M0 + 1)]
U = [c[r] + E[r] for r in range(M0 + 1)]
def fr(x, r): return x / (1 << r)
e = [fr(E[r], r) for r in range(M0 + 1)]; u = [fr(U[r], r) for r in range(M0 + 1)]; cf = [fr(c[r], r) for r in range(M0 + 1)]
assert [E[r] for r in range(1, 8)] == [0, 0, 2, 0, 6, 2, 20]
kap = math.sqrt(2 / math.pi)
def sig(s): return math.sqrt((M0 + 1) / (M0 + 1 - s))
print(f"M0={M0} R0={R0} R1={R1}; table: max E*sqrt(r) over {R1} < r <= {M0}: even {max(e[r]*math.sqrt(r) for r in range(R1+1, M0+1) if r%2==0):.6f}, odd {max(e[r]*math.sqrt(r) for r in range(R1+1, M0+1) if r%2==1):.6f};"
      f" max u(r) over 2 < r <= {M0}: {max(u[3:]):.6f}; kappa/2 = {kap/2:.6f}, 7 kappa/6 = {7*kap/6:.6f}")
for (a_ev, a_od) in PAIRS:
    a = (a_ev, a_od); amax = max(a); amin = min(a); ok = True
    w = max(e[r] * math.sqrt(r) / a[r % 2] for r in range(R1 + 1, M0 + 1))
    print(f"(T0') max over R1 < r <= M0 of E(r)*sqrt(r)/a_par(r) = {w:.6f}"); ok &= (w <= 1)
    worst = 0; wa = None
    for r2 in range(1, R0 + 1):
        for p1 in (0, 1):
            pm = (p1 + r2) % 2
            val = sig(r2) * (a[p1] * u[r2] + (kap if p1 == 0 else 0.0) * e[r2]) / a[pm]
            if val > worst: worst = val; wa = (r2, p1)
    print(f"(T2s) worst ratio = {worst:.6f} at (r2, parity of r1) = {wa}"); ok &= (worst <= 1)
    val = math.sqrt(2) * amax * (2 * kap + amax) / math.sqrt(R0) / amin
    print(f"(T2l) ratio <= {val:.6f}"); ok &= (val <= 1)
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
    den = min(2 * M0 / 9, R0 * (1 - R0 / M0))
    val = (kap * kap / math.sqrt(den) + math.sqrt(3) * (amax + kap) ** 2 / math.sqrt(R0 / 2) / 2) / amin
    print(f"(T3l) ratio <= {val:.6f}"); ok &= (val <= 1)
    print("TAIL CONDITIONS", "ALL HOLD" if ok else "FAIL", f"for M0={M0} R0={R0} R1={R1} a_even={a_ev} a_odd={a_od}; kappa+a_even = {kap+a_ev:.6f}")
