# Referee's exact checks of the intermediate inequalities of sections 3 and 4 of two/result.md on ranges of sizes.
#  (1) top term (section 4): m g(r_1..r_p)^2 <= tau_p^2 = p 4^(1-p) for all sizes r_1 >= ... >= r_p >= 1, sum m <= M.
#  (2) section 3: g(r1,r2,r3) <= q(r1) (c(r2+r3) - c(r2)c(r3)) for all r1 >= r2 >= r3 >= 1 with sum <= M3
#      (the text then uses q(r1) <= kappa/sqrt(r1)).
#  (3) q(r+2)/q(r) = (r+2)/(r+3) for odd r; c(r) + a_p/sqrt(r) < 3/8 for the sizes named in my report (Theorem 2
#      without Theorem Q).
import sys, math
from fractions import Fraction as F
from math import comb
def P(r, v): return F(comb(r, (r + v) // 2), 1 << r) if (r - v) % 2 == 0 and abs(v) <= r else F(0)
def c(r): return P(r, 0)
def q(r): return F(comb(r, r // 2), 1 << r)
def g(rs):
    if len({r % 2 for r in rs}) > 1: return F(0)
    lo = min(rs); t = F(0)
    for v in range(-lo, lo + 1):
        if v and (v - lo) % 2 == 0:
            x = F(1)
            for r in rs: x *= P(r, v)
            t += x
    return t
def parts(m, k, lo=1):
    if k == 1:
        if m >= lo: yield (m,)
        return
    for x in range(lo, m // k + 1):
        for rest in parts(m - x, k - 1, x): yield (x,) + rest
for p, M in ((5, int(sys.argv[1])), (7, int(sys.argv[2])), (11, int(sys.argv[3]))):
    tau2 = F(p, 4 ** (p - 1)); n = 0; worst = (F(0), None); second = (F(0), None); eq = []
    for m in range(p, M + 1):
        for rs in parts(m, p):
            gg = g(rs); n += 1
            if not gg: continue
            val = gg * gg * m / tau2
            assert val <= 1, ("TOP TERM FAILS", p, rs)
            if val == 1: eq.append(rs)
            elif val > second[0]: second = (val, rs)
    print(f"(1) p = {p}: {n} size patterns with sum <= {M}: sqrt(m) g <= tau_p every time; equality at {eq}; next largest sqrt(m) g / tau_p = {math.sqrt(float(second[0])):.4f} at {second[1]}")
M3 = int(sys.argv[4]); n = 0; worst = (F(0), None)
for m in range(3, M3 + 1):
    for (r3, r2, r1) in parts(m, 3):
        gg = g((r1, r2, r3)); n += 1
        bound = q(r1) * (c(r2 + r3) - c(r2) * c(r3))
        assert gg <= bound, ("SECTION 3 g-BOUND FAILS", r1, r2, r3)
        if bound and gg / bound > worst[0]: worst = (gg / bound, (r1, r2, r3))
print(f"(2) p = 3: {n} triples with sum <= {M3}: g <= q(r1)(c(r2+r3) - c(r2)c(r3)) every time; largest ratio {float(worst[0]):.4f} at {worst[1]}")
print("(3) q(r+2)/q(r) = (r+2)/(r+3) for odd r <= 999:", all(q(r + 2) / q(r) == F(r + 2, r + 3) for r in range(1, 1000, 2)))
def a_p(p):
    tau = math.sqrt(p) * 2.0 ** (1 - p); return tau / (1 - 0.8165 * math.sqrt(p) * 2.0 ** (2 - p))
for p in (5, 7, 11, 13):
    ev = [(float(c(r)) + a_p(p) / math.sqrt(r), r) for r in range(p + 1, 400, 2)]
    od = [(a_p(p) / math.sqrt(r), r) for r in range(p, 400, 2)]
    bad = [r for v, r in ev + od if v >= 0.375]
    print(f"    p = {p}: max over even r >= {p+1} of c(r) + a_p/sqrt(r) = {max(ev)[0]:.4f} at r = {max(ev)[1]}; over odd r >= p: {max(od)[0]:.4f}; sizes with value >= 3/8: {bad}")
