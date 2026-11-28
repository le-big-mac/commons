"""Theorem 2 / Theorem 6 with the powers of 3 taken from the first text (quarter/one/result.md):
 odd m:  the share bad at some power of 3 is at most c_(m-2)/2  (its Theorem A);
 even m: the share bad at some 3^i, i >= 1, and not at 1 is at most 309/8192  (its Theorem B).
So  beta(m) <= B3(m) := [the bound of bound.py / bound_even.py without the terms d* = 3^j] + that number.
usage: mixed.py M0"""
import sys, math
sys.path.insert(0, '/home/agent3/lean/lift-check/even/root/one')
from bound_even import Even
from bound import NTOP
M0 = int(sys.argv[1]); E = Even(M0)
worst = {0: (0, 0), 1: (0, 0)}; bad_odd = []
for m in range(27, M0 + 1):
    E._lc = {}
    c = lambda x: float(E.c[x + E.OFF])
    tl = E.s2pi / math.sqrt(m) * E.tail if m > NTOP else 0.0
    if m % 2:
        own3 = sum(E.LC(m, N) for (p, j, N) in E.pp if p == 3 and N <= m)
        rest = sum(E.cnt[N] * E.LC(m, N) for N in E.cnt if N <= m) - own3 + tl
        three = min(own3, c(m - 2) / 2)
    else:
        own3 = sum(E.PPE(m, 3, j) for (p, j, N) in E.pp if p == 3 and N <= m)
        rest = E.BE(m) - own3
        three = min(own3, 309 / 8192)
    v = (rest + three) * math.sqrt(m)
    if m <= 110: print(f"m = {m:4d}  powers of 3: own {own3:.6f}, first text {three:.6f};  B3(m) = {rest + three:.6f}  sqrt(m) B3(m) = {v:.5f}")
    if m >= 47 and v > worst[m % 2][0]: worst[m % 2] = (v, m)
    if m % 2 and m >= 47 and v >= 1: bad_odd.append(m)
print(f"largest sqrt(m) B3(m) over even m in [47, {M0}]: {worst[0][0]:.6f} at m = {worst[0][1]}")
print(f"largest sqrt(m) B3(m) over odd  m in [47, {M0}]: {worst[1][0]:.6f} at m = {worst[1][1]};  odd m >= 47 with sqrt(m) B3(m) >= 1: {bad_odd}")
