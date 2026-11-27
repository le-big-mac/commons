"""The sharper bound for the level d = 3 (used for even m only), exact fractions.

Classes modulo 3 of sizes k0 >= k1 >= k2 >= 1, independent uniform signs, s_j = sum of the signs in class j.
P(s0 = s1 = s2) <= c_{k0} * c_{k1} <= c_{ceil(m/3)} / 2, with c_k = C(k, floor(k/2)) / 2^k = max_b P(sum of k signs = b).
Checked for every (k0, k1, k2) with m = k0 + k1 + k2 <= mmax; also that c_k is nonincreasing.
usage: level3.py [mmax=60]
"""
import sys
from fractions import Fraction as Fr
from math import comb

mmax = int(sys.argv[1]) if len(sys.argv) > 1 else 60


def dist(k):
    return {2 * j - k: Fr(comb(k, j), 2 ** k) for j in range(k + 1)}


def c(k):
    return Fr(comb(k, k // 2), 2 ** k)


D = {k: dist(k) for k in range(1, mmax + 1)}
for k in range(1, mmax + 1):
    assert c(k) == max(D[k].values())
    if k > 1:
        assert c(k) <= c(k - 1)
cnt = 0
worst = Fr(0)
worst2 = Fr(0)
for m in range(3, mmax + 1):
    for k2 in range(1, m // 3 + 1):
        for k1 in range(k2, (m - k2) // 2 + 1):
            k0 = m - k1 - k2
            P = sum(D[k0].get(b, 0) * D[k1].get(b, 0) * v for b, v in D[k2].items())
            assert P <= c(k0) * c(k1) <= c(-(-m // 3)) / 2, (k0, k1, k2)
            assert P <= Fr(1, 4)
            cnt += 1
            worst = max(worst, P / (c(k0) * c(k1)))
            if m % 2 == 0 and m >= 14:
                worst2 = max(worst2, P)
print(f"level 3: {cnt} triples (k0, k1, k2) with m <= {mmax}: P(s0 = s1 = s2) <= c_k0 c_k1 <= c_ceil(m/3)/2 in every case; "
      f"largest P/(c_k0 c_k1) = {float(worst):.4f}; largest P for even m >= 14: {worst2} = {float(worst2):.5f} (bound used: 5/32 = 0.15625)")
