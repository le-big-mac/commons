"""Odd m, exact fractions: B3(m) = B(m) - (the terms of the patterns 3^j) + min(those terms, c_(m-2)/2), with B(m) of
Theorem 2 in full (every N <= m), and the test m B3(m)^2 < 1.   usage: mixed_exact.py MMIN MMAX"""
import sys, math
from fractions import Fraction
sys.path.insert(0, '/home/agent3/lean/lift-check/even/root/one')
from bound import c_frac, cnt_table, gamma_exact
lo, hi = int(sys.argv[1]), int(sys.argv[2])
c = c_frac(hi); cnt = cnt_table(hi); allok = True
for m in range(lo | 1, hi + 1, 2):
    g = {N: gamma_exact(c, m, N) for N in range(3, m + 1, 2)}
    B = sum(cnt[N] * Fraction(1, 2 ** (N - 2)) * g[N] for N in g)
    own3 = sum(Fraction(1, 2 ** (N - 2)) * g[N] for N in g)          # N(3^j) = 2j + 1: one pattern for every odd N
    B3 = B - own3 + min(own3, c[m - 2] / 2)
    ok = m * B3 * B3 < 1; allok &= ok
    print(f"m = {m}  B(m) = {float(B):.9f}  powers of 3: own {float(own3):.9f}, c_(m-2)/2 = {float(c[m - 2] / 2):.9f}  "
          f"B3(m) = {float(B3):.9f}  sqrt(m) B3(m) = {math.sqrt(m) * float(B3):.6f}  m B3^2 < 1 (exact): {ok}")
print("all below 1:", allok)
