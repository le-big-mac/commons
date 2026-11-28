"""B_E(m) of Theorem 4 in exact fractions, written again from the definitions in result.md (not from bound_even.py),
every pattern with N(d*) <= m taken exactly; compared with the floating point values of bound_even.py; and the
bound with the first text's 309/8192 for the powers of 3 (section 7), tested exactly against 1.5529/sqrt(m).

usage: crosscheck.py MMIN MMAX
"""
import sys, math
from fractions import Fraction
sys.path.insert(0, '/home/agent3/lean/lift-check/even/root/one')
from bound import c_frac, cnt_table, gamma_exact, odd_primes, NTOP
from bound_even import Even

lo, hi = int(sys.argv[1]), int(sys.argv[2])
c = c_frac(hi); cnt = cnt_table(hi); E = Even(hi)
def cc(x): return c[x] if x >= 1 else Fraction(1)

def LC(m, N):
    return Fraction(1, 2 ** (N - 2)) * gamma_exact(c, m, N) if N <= m else Fraction(0)

def Fb(m, p, k, g):
    N = k + p - 1
    if N > m: return Fraction(0)
    best = Fraction(0)
    for s in range(0, m - (-(-m // (p * k))) + 1):
        v = cc(m - s) * min(g, 2 * cc(-(-s // 2) - 2 * (N - 3)))
        if v > best: best = v
    return Fraction(1, 2 ** (N - 2)) * best

def PPE(m, p, j):
    G = 1 + (j - 1) * (p - 1)
    if p >= 11: return LC(m, G + p - 1)
    q = max(2, p - 2); best = LC(m, G + q + p - 1)
    for k in range(G, G + q):
        g = Fraction(17, 64) if (p, j, k) == (3, 1, 1) else Fraction(1, 2 ** (p - 2))
        best = max(best, min(LC(m, k + p - 1), Fb(m, p, k, g)))
    return best

C2 = Fraction(15529, 10000) ** 2; worst = 0.0; allok = True; maxdiff = 0.0
for m in range(lo + lo % 2, hi + 1, 2):
    pps = [(p, j) for p in odd_primes(m) for j in range(1, m) if j * (p - 1) + 1 <= m]
    npp = {}
    for p, j in pps: npp[j * (p - 1) + 1] = npp.get(j * (p - 1) + 1, 0) + 1
    comp = sum((cnt[N] - npp.get(N, 0)) * LC(m, N) for N in range(3, m + 1, 2))
    pp = {(p, j): PPE(m, p, j) for p, j in pps}
    BE = c[m] + comp + sum(pp.values())
    three = sum(v for (p, j), v in pp.items() if p == 3)
    B3 = BE - three + min(three, Fraction(309, 8192))
    fl = E.BE(m); diff = fl - float(BE); maxdiff = max(maxdiff, abs(diff)) if m <= NTOP else maxdiff
    ok = m * B3 * B3 < C2; allok &= ok or m < 48
    print(f"m = {m:4d}  B_E exact = {float(BE):.9f}  float program = {fl:.9f}  (difference {diff:.2e})  sqrt(m) B_E = {math.sqrt(m) * float(BE):.5f}"
          f"  with 309/8192: sqrt(m) B3 = {math.sqrt(m) * float(B3):.5f}  m B3^2 < 1.5529^2 (exact): {ok}")
print(f"largest |float - exact| for m <= {NTOP}: {maxdiff:.2e};  for m > {NTOP} the float program is larger by its tail term only")
print("all m >= 48 in the range below 1.5529/sqrt(m) with the first text's powers of 3:", allok)
