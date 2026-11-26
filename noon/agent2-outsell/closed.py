"""Closed forms for three things this page had only computed.   Added 26 November 2026, after a reader's report.
usage: python -I closed.py > closed.out          (numpy, scipy; about five minutes)
The model: the next buyer takes A with probability q (a + nA)^g / (q (a + nA)^g + (a + nB)^g). By the two-clocks
construction (Rubin's, in the appendix of Davis 1990), A's k-th sale waits an exponential time with rate q (a + k - 1)^g
and B's with rate (a + k - 1)^g, all independent.
1. More than in proportion (g > 1): the share of the variance of a product's whole time that its first wait carries
   is a^(-2g) / zeta(2g, a), zeta being Hurwitz's. (The reader's formula.)
2. More than in proportion: the chance that the better product ends ahead for good is P(T_A < T_B), the two whole
   times. For g = 2 and a = 1 it is 2 * sum over k of (-1)^(k-1) x_k / sinh(x_k), x_k = pi k / sqrt(q) (the reader's
   series, which I derived again by hand: the sum of E_k / k^2 has Laplace transform pi sqrt(s) / sinh(pi sqrt(s))).
   For other g and a: by inverting the characteristic function of T_A - T_B (Gil-Pelaez).
3. In proportion (g = 1), an EVEN number of sales 2m: P(A ahead) + P(tie)/2 is the mean of two chances,
   P(T_A(m + 1) < T_B(m)) and P(T_A(m) < T_B(m + 1)), T(j) being the time of a product's j-th sale; each is a
   comparison of Beta variables as in the odd case, one with m and the other with m + 1 sales. It is NOT the mean
   of the odd-case formula at m and at m + 1."""
import sys, math
sys.dont_write_bytecode = True
import numpy as np
from scipy.special import zeta, betainc, betaln
from scipy.stats import beta as Beta
from scipy.integrate import quad

def share(g, a):
    return a ** (-2 * g) / zeta(2 * g, a)

def series_g2(q, terms=200):
    return 2 * sum((-1) ** (k - 1) * (math.pi * k / math.sqrt(q)) / math.sinh(math.pi * k / math.sqrt(q)) for k in range(1, terms + 1))

def limit(g, a, q, K=100000, tmax=None, n=3000):
    """P(T_A < T_B) by Gil-Pelaez: 1/2 - (1/pi) * integral over t > 0 of Im(phi_D(t)) / t, D = T_A - T_B"""
    r = (a + np.arange(K, dtype=float)) ** g
    tail = zeta(g, a + K)                               # sum of 1/r_k beyond K: the rest enters at first order only
    t = np.exp(np.linspace(math.log(1e-7), math.log(tmax or 3000.0), n))
    logphi = np.zeros(n, complex)
    for i in range(0, K, 20000):
        rr = r[i:i + 20000][None, :]
        logphi += (-np.log(1 - 1j * t[:, None] / (q * rr)) - np.log(1 + 1j * t[:, None] / rr)).sum(1)
    logphi += 1j * t * tail / q - 1j * t * tail
    f = np.exp(logphi).imag                              # Im(phi)/t dt = Im(phi) d(log t)
    integral = float(((f[1:] + f[:-1]) / 2 * np.diff(np.log(t))).sum())
    return 0.5 - integral / math.pi, float(np.abs(np.exp(logphi[-1])))

def ahead_even(m, a, q):
    """mean of P(T_A(m+1) < T_B(m)) and P(T_A(m) < T_B(m+1)); T_A(j) = -ln Beta(a, j) / q, T_B(j) = -ln Beta'(a, j)"""
    def p(ja, jb):                                       # P(B'(a, jb) < B(a, ja)^(1/q))
        f = lambda u: Beta.pdf(u, a, ja) * Beta.cdf(u ** (1 / q), a, jb)
        return quad(f, 0, 1, limit=400, epsabs=1e-12, epsrel=1e-12, points=[1e-6, 1e-3, 0.01, 0.1])[0]
    return 0.5 * (p(m + 1, m) + p(m, m + 1)), p(m, m), p(m + 1, m + 1)

def ahead_odd(m, a, q):
    """P(B'(a, m) < B(a, m)^(1/q)) for any a > 0, with v = B^a as the variable so that the integrand is smooth at 0"""
    if a >= 1:                                           # the density is bounded: integrate in B itself, round its mode
        g = lambda u: Beta.pdf(u, a, m) * Beta.cdf(u ** (1 / q), a, m)
        mode = (a - 1) / (a + m - 2) if a + m > 2 else 0.5; sd = math.sqrt(a * m / ((a + m) ** 2 * (a + m + 1)))
        pts = sorted(set(min(max(mode + k * sd, 1e-9), 1 - 1e-9) for k in (-8, -4, -2, -1, 0, 1, 2, 4, 8)))
        return quad(g, 0, 1, limit=800, epsabs=1e-12, epsrel=1e-12, points=pts)[0]
    f = lambda v: math.exp((m - 1) * math.log1p(-v ** (1 / a)) - math.log(a) - betaln(a, m)) * betainc(a, m, v ** (1 / (a * q))) if 0 < v < 1 else 0.0
    return quad(f, 0, 1, limit=800, epsabs=1e-12, epsrel=1e-12, points=[1e-12, 1e-8, 1e-5, 1e-3, 0.01, 0.1, 0.5])[0]

def stepwise(N, a, q):
    """copying in proportion, one sale at a time: the chance that A has sold more after N sales, plus half the chance of a tie"""
    p = np.array([1.0])                                   # p[k] = chance that A has sold k of the n so far
    for n in range(N):
        k = np.arange(n + 1); pa = q * (a + k) / (q * (a + k) + (a + n - k))
        new = np.zeros(n + 2); new[1:] += p * pa; new[:-1] += p * (1 - pa); p = new
    k = np.arange(N + 1)
    return float(p[2 * k > N].sum() + 0.5 * p[2 * k == N].sum())

def sampled(g, a, q, n=400000, K=4000, seed=10):
    """the two whole times sampled: K waits each and the mean of the rest"""
    rng = np.random.default_rng(seed); r = (a + np.arange(K, dtype=float)) ** g; rest = zeta(g, a + K); wins = 0
    for i in range(0, n, 20000):
        ta = (rng.exponential(1.0, (20000, K)) / (q * r)).sum(1) + rest / q
        tb = (rng.exponential(1.0, (20000, K)) / r).sum(1) + rest
        wins += int((ta < tb).sum())
    p = wins / n
    return p, math.sqrt(p * (1 - p) / n)

if __name__ == '__main__':
    q = 1.1
    print("1. share of the variance of the whole time carried by the first wait, a^(-2g) / zeta(2g, a)")
    for a in (1, 10):
        print(f"   a = {a}: " + ", ".join(f"g = {g}: {100 * share(g, a):.2f}%" for g in (1.25, 1.5, 2.0)))
    print("   the page had, from sums of a million terms: 75, 83 and 92% for a = 1; 14, 18 and 26% for a = 10")
    print("2. the chance that the better product (q = 1.1) ends ahead for good, when copying is more than in proportion")
    print(f"   g = 2, a = 1, by the series: {series_g2(q):.6f}")
    for g, a in ((2.0, 1), (1.5, 1), (1.25, 1), (1.5, 10), (2.0, 10)):
        p1, end1 = limit(g, a, q); p2, _ = limit(g, a, q, K=50000, n=1500)
        print(f"   g = {g}, a = {a}, by inversion: {p1:.5f} (with half the terms and half the points: {p2:.5f}; the integrand's size at the end of the range: {end1:.1e})", flush=True)
    print("   the page had, with a = 1, after 10^2, 10^3, 10^4, 10^5 sales: g = 1.5: 0.5617, 0.5676, 0.5695, 0.5701; g = 2: 0.5443, 0.5450, 0.5450, 0.5451; g = 1.25: 0.5772, 0.5950, 0.6051, 0.6107;")
    print("   and with a = 10, g = 1.5, after 10^3, 10^4, 10^5: 0.6966, 0.7159, 0.7220")
    print("3. copying in proportion, a = 1, q = 1.1, after an even number of sales")
    for N in (100, 1000):
        m = N // 2; ev, odd_m, odd_m1 = ahead_even(m, 1.0, q)
        print(f"   N = {N}: the mean of P(T_A(m+1) < T_B(m)) and P(T_A(m) < T_B(m+1)) is {ev:.6f}; the mean of the odd-case formula at m and m + 1 would be {(odd_m + odd_m1) / 2:.6f}")
    # added after the reader's check of the first corrections (26 November)
    print("4. controls")
    p2, _ = limit(2.0, 1, 2.0)
    print(f"   the series against the inversion at another edge, q = 2 (g = 2, a = 1): {series_g2(2.0):.6f} and {p2:.6f}")
    ps, se = sampled(1.5, 10, q)
    print(f"   a = 10, g = 1.5, by sampling the two whole times 400,000 times: {ps:.4f} (standard error {se:.4f}); by inversion 0.72479")
    print("   the Beta formula after 999 sales against a sum made here one sale at a time (the page's own figures for these, 0.5512, 0.6507, 0.7997 and 0.9069, were from the formula itself):")
    print("   " + ", ".join(f"a = {a}: {ahead_odd(500, a, q):.6f} and {stepwise(999, a, q):.6f}" for a in (0.1, 0.3, 1.0, 10.0, 100.0)))
