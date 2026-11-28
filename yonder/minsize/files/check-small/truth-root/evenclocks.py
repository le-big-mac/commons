"""Exact share of bad ways for every marking (containing hour 0) of m marks on small clocks,
against 3.12/sqrt(m) (every m) and 2/sqrt(m) (odd m).  A marking is a vector of multiplicities.
A way of choosing signs is bad if the signed marks balance at some divisor d of n (1 included):
sum_j v_j zeta_d^j = 0, v_j the signed count at hour j.  Shares are exact (integer weights);
the test "= 0" is in floating point with integer coefficients of size <= m (tolerance 1e-9).
usage: evenclocks.py n mmin mmax [seconds]"""
import sys, time
from math import comb, sqrt, pi, cos, sin
import numpy as np
from fractions import Fraction as F

n = int(sys.argv[1]); mmin = int(sys.argv[2]); mmax = int(sys.argv[3])
limit = float(sys.argv[4]) if len(sys.argv) > 4 else 150.0
t0 = time.time()
divs = [d for d in range(1, n + 1) if n % d == 0]
zeta = {d: [complex(cos(2 * pi * j / d), sin(2 * pi * j / d)) for j in range(n)] for d in divs}

def comps(total, parts):
    if parts == 1:
        yield (total,)
        return
    for a in range(total + 1):
        for rest in comps(total - a, parts - 1):
            yield (a,) + rest

def bad_count(a):
    # returns number of bad sign choices out of 2^m
    vals = [np.arange(-x, x + 1, 2) for x in a]
    wts = [np.array([comb(x, k) for k in range(x + 1)], dtype=object) for x in a]
    W = np.array([1], dtype=object)
    S = {d: np.zeros(1, dtype=complex) for d in divs}
    for j in range(n):
        if a[j] == 0:
            continue
        W = np.multiply.outer(W, wts[j]).ravel()
        for d in divs:
            S[d] = np.add.outer(S[d], vals[j] * zeta[d][j]).ravel()
    bad = np.zeros(len(W), dtype=bool)
    for d in divs:
        bad |= np.abs(S[d]) < 1e-9
    return int(sum(W[bad]))

for m in range(mmin, mmax + 1):
    worst = (-1, None); cnt = 0; done = True
    for rest in comps(m - 1, n):
        a = (rest[0] + 1,) + rest[1:]
        b = bad_count(a)
        cnt += 1
        if b > worst[0]:
            worst = (b, a)
        if time.time() - t0 > limit:
            done = False
            break
    share = F(worst[0], 2 ** m)
    bound = 3.12 / sqrt(m)
    line = "n=%d m=%d markings=%d%s largest bad share %s = %.5f (times sqrt m: %.4f) at %s; 3.12/sqrt(m)=%.4f %s" % (
        n, m, cnt, "" if done else " (STOPPED EARLY)", share, float(share), float(share) * sqrt(m), worst[1],
        bound, "ok" if float(share) <= bound else "VIOLATION")
    if m % 2 == 1:
        line += "; 2/sqrt(m)=%.4f %s" % (2 / sqrt(m), "ok" if float(share) < 2 / sqrt(m) else "VIOLATION")
    print(line, flush=True)
    if not done:
        break
print("seconds: %.1f" % (time.time() - t0))
