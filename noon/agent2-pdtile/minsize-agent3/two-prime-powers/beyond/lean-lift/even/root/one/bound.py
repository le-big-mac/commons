"""The explicit bound B(m) of result.md (Theorem 2) and the constants of Theorems 1, 3 and 4.

  c_r = C(r, floor(r/2)) / 2^r for r >= 1,  c_r = 1 for r <= 0.
  d* = prod p^(j_p) over a finite nonempty set of odd primes, j_p >= 1 (the ranks);
  G(d*) = max_p (1 + (j_p - 1)(p - 1)),  P(d*) = the largest prime,  N(d*) = G(d*) + P(d*) - 1  (odd, >= 3).
  cnt(N) = the number of d* with N(d*) = N.
  gamma(m, N) = max over 1 <= r <= (m-1)/2 of 2 c_r c_(max(m - 2r, r) - 2(N - 3)).
  B(m) = [m even] c_m + sum over odd N, 3 <= N <= m, of cnt(N) 2^-(N-2) gamma(m, N).

usage: bound.py counts NMAX          the table cnt(N), checked against a plain enumeration of the d* for N <= 19
       bound.py exact M              B(m) in exact fractions for m <= M (all N <= m)
       bound.py sup M0 NA            floating point: sup of sqrt(m) B(m) over m <= M0, the constants, the bound for m > M0
"""
import sys, math
from fractions import Fraction
from itertools import product

NTOP = 61                      # the terms N <= NTOP are taken exactly; beyond: the crude bound and the tail of Lemma W

def odd_primes(n):
    return [p for p in range(3, n + 1, 2) if all(p % q for q in range(3, int(p ** 0.5) + 1, 2))]

def J(q, g):                   # the number of ranks j >= 1 with 1 + (j-1)(q-1) <= g
    return 0 if g < 1 else 1 + (g - 1) // (q - 1)

def cnt_table(nmax):
    """cnt[N] for odd N <= nmax, by the closed formula: the d* with largest prime P and G(d*) <= g number
    J(P, g) * prod over the odd primes q < P of (1 + J(q, g))."""
    ps = odd_primes(nmax)
    def upto(P, g):
        if g < 1: return 0
        v = J(P, g)
        for q in ps:
            if q >= P: break
            v *= 1 + J(q, g)
        return v
    cnt = {N: 0 for N in range(3, nmax + 1, 2)}
    for P in ps:
        for g in range(1, nmax - P + 2, 2):
            cnt[g + P - 1] += upto(P, g) - upto(P, g - 2)
    return cnt

def cnt_plain(nmax):
    """the same by listing every d* with N(d*) <= nmax (exponent vectors over the odd primes <= nmax)."""
    ps = odd_primes(nmax)
    cnt = {N: 0 for N in range(3, nmax + 1, 2)}
    ranges = [range(0, 2 + (nmax - 1) // (p - 1)) for p in ps]
    for js in product(*ranges):
        if not any(js): continue
        G = max(1 + (j - 1) * (p - 1) for p, j in zip(ps, js) if j)
        P = max(p for p, j in zip(ps, js) if j)
        N = G + P - 1
        if N <= nmax: cnt[N] += 1
    return cnt

def c_frac(rmax):
    c = [Fraction(1)] * (rmax + 1)
    for r in range(1, rmax + 1):
        c[r] = Fraction(math.comb(r, r // 2), 2 ** r)
    return c

def gamma_exact(c, m, N):
    best = Fraction(0)
    for r in range(1, (m - 1) // 2 + 1):
        x = max(m - 2 * r, r) - 2 * (N - 3)
        v = 2 * c[r] * (c[x] if x >= 1 else 1)
        if v > best: best = v
    return best

def B_exact(m, c=None, cnt=None):
    """B(m) as a fraction, every N <= m."""
    if c is None: c = c_frac(m)
    if cnt is None: cnt = cnt_table(max(m, 3))
    tot = c[m] if m % 2 == 0 else Fraction(0)
    for N in range(3, m + 1, 2):
        tot += cnt[N] * Fraction(1, 2 ** (N - 2)) * gamma_exact(c, m, N)
    return tot

# ---- the tail of the weights (Lemma W of sign-four-result.md: A(t) 2^-t <= (u+1) x^u, u = t/2, x < 0.5783) ----
X_W = 0.5783
def tail_beyond(N2):
    """an upper bound for the sum over the d* with N(d*) > N2 (N2 odd) of sqrt(N(d*)) 2^-(N(d*)-2):
    the d* with N(d*) = N have mu(d*) <= N - 1, so they number at most A(N-1) <= 2^(N-1) (u+1) x^u, u = (N-1)/2;
    the term is at most 2 sqrt(2u+1) (u+1) x^u, and consecutive terms have ratio at most x (1 + 1/u2)^1.5."""
    u2 = (N2 + 1) // 2
    first = 2 * math.sqrt(2 * u2 + 1) * (u2 + 1) * X_W ** u2
    ratio = X_W * (1 + 1 / u2) ** 1.5
    assert ratio < 1
    return first / (1 - ratio)

def main():
    mode = sys.argv[1]
    if mode == 'counts':
        nmax = int(sys.argv[2]); cnt = cnt_table(nmax)
        plain = cnt_plain(19)
        ok = all(plain[N] == cnt[N] for N in plain)
        print("cnt(N) by the formula equals the plain enumeration for N <= 19:", ok)
        s2 = 0.0; s3 = 0.0
        for N in range(3, nmax + 1, 2):
            s2 += cnt[N] * 2.0 ** -(N - 2); s3 += cnt[N] * math.sqrt(N) * 2.0 ** -(N - 2)
            print(f"N = {N:3d}  cnt = {cnt[N]:>22d}  cnt 2^-(N-2) = {cnt[N] * 2.0 ** -(N - 2):.3e}  "
                  f"partial sum of cnt 2^-(N-2) = {s2:.9f}   of cnt sqrt(N) 2^-(N-2) = {s3:.9f}")
        t = tail_beyond(nmax)
        print(f"tail beyond N = {nmax} (bound): {t:.3e}")
        print(f"Sigma_1 := sum of cnt(N) 2^-(N-2) over all N: between {s2:.9f} and {s2 + t:.9f}")
        print(f"Sigma_h := sum of cnt(N) sqrt(N) 2^-(N-2) over all N: at most {s3 + t:.9f}")
        print(f"Theorem 1: C1 = sqrt(2/pi) (1 + Sigma_h) <= {math.sqrt(2 / math.pi) * (1 + s3 + t):.6f}")
        print(f"limits: sqrt(2/pi) Sigma_1 <= {math.sqrt(2 / math.pi) * (s2 + t):.6f},  sqrt(2/pi) (1 + Sigma_1) <= {math.sqrt(2 / math.pi) * (1 + s2 + t):.6f}")
    elif mode == 'exact':
        M = int(sys.argv[2]); c = c_frac(M); cnt = cnt_table(max(M, 3))
        for m in range(1, M + 1):
            b = B_exact(m, c, cnt)
            print(f"m = {m:3d}  B(m) = {b}  = {float(b):.6f}   sqrt(m) B(m) = {float(b) * math.sqrt(m):.4f}")
    elif mode == 'sup':
        import numpy as np
        M0 = int(sys.argv[2]); NA = int(sys.argv[3])
        cnt = cnt_table(NTOP)
        w = {N: cnt[N] * 2.0 ** -(N - 2) for N in cnt}
        tail = tail_beyond(NTOP)
        OFF = 2 * NTOP                                # c[x + OFF] = c_x, x >= -OFF
        c = np.ones(M0 + OFF + 1)
        c[1 + OFF] = 0.5
        # c_r: c_1 = 1/2, c_(2h) = c_(2h-1), c_(2h+1) = c_(2h) (2h+1)/(2h+2)
        for r in range(2, M0 + 1):
            c[r + OFF] = c[r - 1 + OFF] if r % 2 == 0 else c[r - 1 + OFF] * r / (r + 1)
        for r in (1, 2, 3, 4, 5, 6, 10, 11):
            assert abs(c[r + OFF] - math.comb(r, r // 2) / 2 ** r) < 1e-15
        s2pi = math.sqrt(2 / math.pi)
        best = {0: (0, 0), 1: (0, 0)}; rows = []
        for m in range(1, M0 + 1):
            tot = c[m + OFF] if m % 2 == 0 else 0.0
            if m >= 3:
                r = np.arange(1, (m - 1) // 2 + 1)
                base = np.maximum(m - 2 * r, r)
                cr2 = 2 * c[r + OFF]
                for N in range(3, min(m, NTOP) + 1, 2):
                    x = np.maximum(base - 2 * (N - 3), -OFF)
                    tot += w[N] * float(np.max(cr2 * c[x + OFF]))
                if m > NTOP: tot += s2pi / math.sqrt(m) * tail
            v = tot * math.sqrt(m)
            rows.append((m, tot, v))
            if v > best[m % 2][1]: best[m % 2] = (m, v)
        for m, tot, v in rows:
            if m <= 100 or m % 100 == 0 or m % 100 == 99:
                print(f"m = {m:5d}  B(m) = {tot:.6f}  sqrt(m) B(m) = {v:.5f}")
        print(f"largest sqrt(m) B(m) over even m <= {M0}: {best[0][1]:.6f} at m = {best[0][0]}")
        print(f"largest sqrt(m) B(m) over odd  m <= {M0}: {best[1][1]:.6f} at m = {best[1][0]}")
        for lo in (9, 21, 25, 47, 100, 300, 1000):
            for par in (0, 1):
                vv = max((v, m) for m, tot, v in rows if m >= lo and m % 2 == par)
                print(f"  largest over {'even' if par == 0 else 'odd '} m in [{lo}, {M0}]: {vv[0]:.6f} at m = {vv[1]}")
        # m > M0
        sA = sum(w[N] for N in w if N <= NA); sB = sum(w[N] * math.sqrt(N) for N in w if N > NA)
        f1 = math.sqrt(M0 / (M0 - 2 * NA + 2))
        # gamma(m, N) sqrt(m) / sqrt(2/pi) for m >= M0, N <= NA:  r <= 2: at most f1;  3 <= r <= m/9: at most f2;
        # r > m/9: at most f3  (each is decreasing in m and increasing in N; section 5 of result.md)
        f2 = 0.75 * math.sqrt(M0 / (7 * M0 / 9 - 2 * NA + 6))
        f3 = 2 * s2pi * 3 / math.sqrt(M0 / 9 - 2 * NA + 6)
        print(f"m > {M0}, N <= {NA}: the three factors (1) {f1:.6f} (2) {f2:.6f} (3) {f3:.6f}; (2), (3) <= (1): {f2 <= f1 and f3 <= f1}")
        odd_inf = s2pi * (f1 * sA + sB + tail); even_inf = s2pi * (1 + f1 * sA + sB + tail)
        print(f"sum of cnt 2^-(N-2), N <= {NA}: {sA:.9f};  sum of cnt sqrt(N) 2^-(N-2), {NA} < N <= {NTOP}: {sB:.3e};  tail beyond {NTOP}: {tail:.3e}")
        print(f"for every m > {M0}: sqrt(m) beta(m) <= {even_inf:.6f} (m even), {odd_inf:.6f} (m odd)")

if __name__ == '__main__':
    main()
