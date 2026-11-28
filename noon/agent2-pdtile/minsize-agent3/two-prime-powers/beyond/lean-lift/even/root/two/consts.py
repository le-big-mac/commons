# The constants of section 3 of result.md (primes p >= 5), recomputed; and the recursion tables for p = 5, 7 as a check.
import math, sys
from math import comb
from fractions import Fraction
import recp
kap = math.sqrt(2 / math.pi)
print(f"kappa = sqrt(2/pi) = {kap:.6f}; kappa/sqrt(5) = {kap/math.sqrt(5):.6f}")
# two classes: theta = sqrt(m/r1) * [u(r2) + kappa*1(r2>=p)/sqrt(r2)]
print("two classes:")
print(f"  r2=2: (1/2)sqrt(7/5) = {0.5*math.sqrt(7/5):.4f};  r2 in (3,4): (3/8)sqrt(9/5) = {0.375*math.sqrt(9/5):.4f};  5<=r2<p: (3/8)sqrt2 = {0.375*math.sqrt(2):.4f}")
print(f"  r2>=p odd: sqrt2*(1/4+kappa/sqrt5) = {math.sqrt(2)*(0.25+kap/math.sqrt(5)):.4f};  r2>=p even (>=6): sqrt2*(3/8+kappa/sqrt6) = {math.sqrt(2)*(0.375+kap/math.sqrt(6)):.4f}")
# k >= 3 classes: psi(k,j)
def psi(k, j):
    return 0.5 ** (k - 1) if j == 0 else 0.5 ** (k - 1 - j) * 0.375 ** (j - 1) * (0.375 + j * kap / math.sqrt(5))
w = max(0.75 ** (j - 1) * (0.375 + j * kap / math.sqrt(5)) for j in range(1, 200))
print(f"max over j>=1 of (3/4)^(j-1) (3/8 + j kappa/sqrt5) = {w:.5f}  (used: 0.8165)"); assert w <= 0.8165
for k in range(3, 14):
    mx = max(psi(k, j) for j in range(0, k)); assert mx <= 0.8165 * 2.0 ** (2 - k) + 1e-15
    print(f"  k={k}: max_j psi(k,j) = {mx:.5f}; times sqrt(k) = {mx*math.sqrt(k):.5f}; 0.8165*sqrt(k)*2^(2-k) = {0.8165*math.sqrt(k)*2.0**(2-k):.5f}")
# top term and a_p
tot_tau = 0; tot_a = 0
for p in [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]:
    tau = math.sqrt(p) * 2.0 ** (1 - p); th = 0.8165 * math.sqrt(p) * 2.0 ** (2 - p); a = tau / (1 - th); tot_tau += tau; tot_a += a
    if p <= 19: print(f"p={p}: tau_p = sqrt(p) 2^(1-p) = {tau:.7f}, theta_p = {th:.5f}, a_p = {a:.7f}, kappa + a_p = {kap + a:.5f}")
    # checks of the top term: odd sizes rho>=3 all equal, and even sizes
    assert kap * 0.375 ** (p - 2) <= 2.0 ** (1 - p) and kap * 4.0 ** (2 - p) <= 2.0 ** (1 - p)
tail = sum(math.sqrt(p) * 2.0 ** (1 - p) / 0.99 for p in range(61, 4000, 2))   # every odd number >= 61, far more than the primes
print(f"sum of a_p over primes 5 <= p <= 59 = {tot_a:.7f}; over all odd numbers >= 61 at most {tail:.3e}; TOTAL A5 <= {tot_a + tail:.6f}")
print("P(S_r = 2) <= 1/4 for even 2 <= r <= 2000:", all(4 * comb(r, r // 2 + 1) <= 2 ** r for r in range(2, 2001, 2)))
print("q(r) sqrt(r) <= kappa for 1 <= r <= 2000:", all(comb(r, r // 2) / 2 ** r * math.sqrt(r) <= kap for r in range(1, 2001)))
print("odd step: (r+4)(r+2) <= (r+3)^2 (always); check sup of sqrt(m)*prod_{t<p} q(r_t) over odd sizes <= 9, p = 5:")
best = 0
import itertools
for rs in itertools.combinations_with_replacement([1, 3, 5, 7, 9], 5):
    v = math.sqrt(sum(rs)) * math.prod(comb(r, (r + 1) // 2) / 2 ** r for r in sorted(rs)[1:])
    best = max(best, v)
print(f"   {best:.6f}  (sqrt5/16 = {math.sqrt(5)/16:.6f})")
# recursion tables as a check of the analytic constants
for p, M in ((5, int(sys.argv[1])), (7, int(sys.argv[2]))):
    E, U, c, arg = recp.table(p, M); a = math.sqrt(p) * 2.0 ** (1 - p) / (1 - 0.8165 * math.sqrt(p) * 2.0 ** (2 - p))
    for par in (0, 1):
        ms = [m for m in range(p, M + 1) if m % 2 == par]; me = max(ms, key=lambda m: E[m] / (1 << m) * math.sqrt(m))
        print(f"p={p}, parity {par}: max over m <= {M} of E_p(m) sqrt(m) = {E[me] / (1 << me) * math.sqrt(me):.6f} at m={me} split {arg[me]}; last m={ms[-1]}: {E[ms[-1]] / (1 << ms[-1]) * math.sqrt(ms[-1]):.6f} split {arg[ms[-1]]}")
    print(f"   all below a_p = {a:.6f}:", all(E[m] / (1 << m) * math.sqrt(m) <= a for m in range(1, M + 1)),
          f"; max (c+E_p)(m) sqrt(m) = {max(U[m] / (1 << m) * math.sqrt(m) for m in range(1, M + 1)):.6f}")
