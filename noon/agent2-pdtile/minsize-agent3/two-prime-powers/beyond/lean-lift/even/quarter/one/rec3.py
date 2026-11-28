"""The bounding recursion of result.md, section 3, for the prime 3 (exact fractions).

xi(m) is an upper bound, proved in result.md (Lemmas 1, 2), for
    X(B) = share of signings of B that are bad at some 3^i, i >= 1, and have sum of signs != 0,
for every multiset B of m elements on every Z_(3^a).  (For odd m this is the share of bad signings.)

xi(0) = xi(1) = 0;  xi(m) = max over r0 >= r1 >= r2 >= 0, r0 + r1 + r2 = m, r1 >= 1 of  A(r0,r1,r2) + S(r0,r1,r2),
  A = sum over v != 0 of P(sum of r0 signs = v) P(sum of r1 signs = v) P(sum of r2 signs = v)
  S = the least of the rules that apply:
      (a) g(r0) g(r1) g(r2),   g(r) = [r even] c_r + xi(r),  g(0) = 1
      (b) all r_t even:  prod (c_(r_t) + xi(r_t)) - prod c_(r_t)
      (c) r2 = 0, r0 and r1 odd and <= 7:  xi(r0) xi(r1) / 2

usage: rec3.py M      prints the table and the checks C1..C5 used in result.md
"""
import sys
from fractions import Fraction as F
from math import comb

M = int(sys.argv[1])
NV = [[0] * (M + 2) for _ in range(M + 1)]          # NV[r][v] = number of sign vectors of length r with sum v >= 0
for r in range(M + 1):
    for v in range(r % 2, r + 1, 2):
        NV[r][v] = comb(r, (r + v) // 2)


def c(r):
    return F(comb(r, r // 2), 2 ** r)


xi = {0: F(0)}
arg = {}


def g(r):
    return (c(r) if r % 2 == 0 else F(0)) + xi[r]


def A_int(r0, r1, r2):
    a, b, cc = NV[r0], NV[r1], NV[r2]
    tot = 0
    for v in range(1, r2 + 1):
        if cc[v]:
            tot += a[v] * b[v] * cc[v]
    return 2 * tot                                   # v and -v


for m in range(1, M + 1):
    best = F(0); bestarg = None
    for r2 in range(0, m // 3 + 1):
        for r1 in range(max(r2, 1), (m - r2) // 2 + 1):
            r0 = m - r1 - r2
            if r0 < r1:
                continue
            A = F(A_int(r0, r1, r2), 2 ** m)
            S = g(r0) * g(r1) * g(r2); rule = 'a'
            if r0 % 2 == 0 and r1 % 2 == 0 and r2 % 2 == 0:
                Sb = (c(r0) + xi[r0]) * (c(r1) + xi[r1]) * (c(r2) + xi[r2]) - c(r0) * c(r1) * c(r2)
                if Sb < S:
                    S = Sb; rule = 'b'
            if r2 == 0 and r0 % 2 == 1 and r1 % 2 == 1 and r0 <= 7:
                Sc = xi[r0] * xi[r1] / 2
                if Sc < S:
                    S = Sc; rule = 'c'
            val = A + S
            if val > best:
                best = val; bestarg = (r0, r1, r2, rule, A, S)
    xi[m] = best; arg[m] = bestarg

print("m, xi(m), float, attained at (r0, r1, r2), rule, A, S;  for even m also c_m + xi(m)")
for m in range(1, M + 1):
    if m <= 40 or m % 20 == 0 or m >= M - 1:
        a = arg[m]
        extra = '' if m % 2 else f"   c_m + xi = {c(m) + xi[m]} = {float(c(m) + xi[m]):.6f}"
        if m > 24:
            print(f"m = {m:3d}  xi = {float(xi[m]):.8f}  at {a[:4] if a else None}{'' if m % 2 else f'   c_m + xi = {float(c(m) + xi[m]):.6f}'}")
        else:
            print(f"m = {m:3d}  xi = {str(xi[m]):>22s} = {float(xi[m]):.8f}  at {a[:4] if a else None}  A = {a[4] if a else 0}  S = {a[5] if a else 0}{extra}")

# ---- checks used in result.md
ok1 = all(xi[m] == c(m - 2) / 2 for m in range(3, M + 1, 2)) and xi[1] == 0
print(f"C1  odd m, 3 <= m <= {M}: xi(m) = c_(m-2)/2 exactly: {ok1}")
ok2 = all(xi[m] <= F(5, 128) for m in range(2, M + 1, 2))
mx = max((xi[m], m) for m in range(2, M + 1, 2))
print(f"C2  even m <= {M}: xi(m) <= 5/128: {ok2};  largest xi(m) = {mx[0]} = {float(mx[0]):.8f} at m = {mx[1]};  xi(2) = {xi[2]}, xi(4) = {xi[4]}, xi(6) = {xi[6]}, xi(8) = {xi[8]}, xi(10) = {xi[10]}")
ok3 = all(xi[m] <= c(m) / 2 for m in range(2, M + 1, 2))
rat = max((xi[m] / c(m), m) for m in range(2, M + 1, 2))
print(f"C3  even m <= {M}: xi(m) <= c_m/2: {ok3};  largest xi(m)/c_m = {float(rat[0]):.6f} at m = {rat[1]};  xi({M - M % 2})/c = {float(xi[M - M % 2] / c(M - M % 2)):.6f}")
m0 = min([m for m in range(2, M + 1, 2) if c(m) / 2 <= F(5, 128)] or [10 ** 9])
print(f"C4  c_m/2 <= 5/128 from m = {m0} on (c_m decreases over the even m); M = {M} >= {m0}: {M >= m0}")
# Psi(r1, r2) = c_(r1+r2) - 2 c_r1 c_r2 + (3/2) g(r1) g(r2), even r1 >= 2, even r2 >= 0, r1 + r2 <= 60
worst = (F(-1), None)
if M >= 60:
    for r1 in range(2, 61, 2):
        for r2 in range(0, min(r1, 60 - r1) + 1, 2):
            psi = c(r1 + r2) - 2 * c(r1) * c(r2) + F(3, 2) * g(r1) * g(r2)
            if psi > worst[0]:
                worst = (psi, (r1, r2))
    print(f"C5  Psi(r1, r2) <= 1/4 for all even r1 >= r2 >= 0, r1 >= 2, r1 + r2 <= 60: {worst[0] <= F(1, 4)};  largest = {worst[0]} at {worst[1]}")
    tail = c(62) + F(3, 2) * F(5, 128) * (F(3, 2) + F(5, 128))
    print(f"    for r1 + r2 >= 62: Psi <= c_62 + (3/2)(5/128)(3/2 + 5/128) = {float(tail):.6f} <= 1/4: {tail <= F(1, 4)}")
# bounds for the share of bad signings on Z_(3^a)
print("t_m <= [m even] c_m + xi(m):")
for m in range(3, min(M, 30) + 1):
    t = (c(m) if m % 2 == 0 else 0) + xi[m]
    print(f"  m = {m:2d}  t_m <= {t} = {float(t):.6f}   <= 3/8: {t <= F(3, 8)}")
okq = all(((c(m) if m % 2 == 0 else 0) + xi[m]) <= F(3, 8) for m in range(3, M + 1))
print(f"t_m <= 3/8 for 3 <= m <= {M}: {okq}")
okw = all(((c(m) if m % 2 == 0 else 0) + xi[m]) + F(118569, 10 ** 6) <= F(3, 8) for m in range(27, M + 1))
print(f"t_m + 0.118569 <= 3/8 for 27 <= m <= {M}: {okw}")

# ---- a numerical look at Proposition T (the tail): continue the same recursion beyond M with the tail values
#      xi*(m) = c_(m-2)/2 (m odd), c_m/2 (m even) in place of the maximum, and check that the maximum stays below them
if len(sys.argv) > 2:
    M2 = int(sys.argv[2])
    NV = [[0] * (M2 + 2) for _ in range(M2 + 1)]
    for r in range(M2 + 1):
        for v in range(r % 2, r + 1, 2):
            NV[r][v] = comb(r, (r + v) // 2)
    okt = True; slack = None
    for m in range(M + 1, M2 + 1):
        target = c(m - 2) / 2 if m % 2 else c(m) / 2
        best = F(0)
        for r2 in range(0, m // 3 + 1):
            for r1 in range(max(r2, 1), (m - r2) // 2 + 1):
                r0 = m - r1 - r2
                if r0 < r1:
                    continue
                A = F(A_int(r0, r1, r2), 2 ** m)
                S = g(r0) * g(r1) * g(r2)
                if r0 % 2 == 0 and r1 % 2 == 0 and r2 % 2 == 0:
                    S = min(S, (c(r0) + xi[r0]) * (c(r1) + xi[r1]) * (c(r2) + xi[r2]) - c(r0) * c(r1) * c(r2))
                best = max(best, A + S)
        okt &= best <= target
        if m % 2 == 0:
            r_ = best / target
            slack = r_ if slack is None else max(slack, r_)
        xi[m] = target
    print(f"Proposition T, numerically: for {M} < m <= {M2} the recursion with the tail values stays <= the tail values: {okt}; "
          f"largest (bound)/(c_m/2) over the even m: {float(slack):.4f}; for odd m the bound equals c_(m-2)/2")
