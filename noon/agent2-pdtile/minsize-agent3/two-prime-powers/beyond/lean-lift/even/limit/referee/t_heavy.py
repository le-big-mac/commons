"""The heavy step of section 3 as it is used: L a divisor of n (often a proper one), H = the elements of B that are
x modulo L (several different elements of Z_n), D the others, D' = D - x on Z_L.  Exact:
   P(bad at some d | L)  <=  c_h * K_(h mod 2)(D'),      h = |H| >= 1.
Also with some elements that are x modulo L put into D (a decoration that contains 0), and L = 1.
usage: t_heavy.py SEED SECONDS"""
import sys, math, random, time
from fractions import Fraction
sys.path.insert(0, '/home/agent3/lean/lift-check/even/limit/referee')
from lib import *

if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1])); secs = float(sys.argv[2]); t0 = time.time()
    n_cases = 0; fail = 0; worst = Fraction(0); n_eq = 0; n_zero_in_D = 0; n_L1 = 0; n_proper = 0; by_par = {0: Fraction(0), 1: Fraction(0)}
    while time.time() - t0 < secs:
        n = rng.choice((9, 15, 15, 27, 45, 45, 63, 105, 105, 135)); L = rng.choice(divisors(n)); x = rng.randrange(L)
        cls = [b for b in range(n) if b % L == x]
        Hres = rng.sample(cls, rng.randint(1, min(3, len(cls))))
        Hitems = [(b, rng.choice((1, 2, 3, 5, 8, 20, 21))) for b in Hres]
        # decoration: cosets of prime order through the heavy class or elsewhere, small multiplicities
        D = []
        for _ in range(rng.randint(0, 3)):
            ps = [q for q in (3, 5, 7) if n % q == 0]; p = rng.choice(ps); x0 = rng.choice(Hres + [rng.randrange(n)])
            mult = rng.choice((1, 1, 2))
            for j in range(1, p): D += [(x0 + j * (n // p)) % n] * mult
            if rng.random() < 0.3: D.append(rng.randrange(n))
        D = D[:9]
        moved = 0
        if rng.random() < 0.3:      # put a few elements of the heavy class into the decoration (0 in D')
            moved = rng.randint(1, 2); D += [rng.choice(cls) for _ in range(moved)]
        # H must be ALL elements that are x modulo L except those deliberately moved: take out of D the others
        if moved == 0:
            extra = [b for b in D if b % L == x]; D = [b for b in D if b % L != x]
            for b in extra: Hitems.append((b, 1))
        h = sum(a for _, a in Hitems); r = len(D)
        g = 1
        for _, a in merge(n, Hitems + [(b, 1) for b in D]): g *= a + 1
        if g > 300000: continue
        cnt, m = bad_count(n, Hitems + [(b, 1) for b in D], divs=divisors(L)); assert m == h + r
        k = K(L, [(b - x) % L for b in D])
        bound = c(h) * k[h % 2]; s = Fraction(cnt, 2 ** m)
        n_cases += 1; n_zero_in_D += moved > 0; n_L1 += L == 1; n_proper += 1 < L < n
        if s > bound: fail += 1; print("HEAVY STEP FAILS:", n, L, x, Hitems, D, s, bound, flush=True)
        if bound > 0:
            q = s / bound; worst = max(worst, q); n_eq += q == 1; by_par[m % 2] = max(by_par[m % 2], q)
        elif s != 0: fail += 1; print("share > 0 with K = 0:", n, L, x, Hitems, D, flush=True)
    print(f"seed {sys.argv[1]}: {n_cases} multisets (L = 1 in {n_L1}, 1 < L < n in {n_proper}, decoration containing 0 in {n_zero_in_D}); "
          f"P(bad at some d | L) <= c_h K_(h mod 2)(D'): failures {fail}; equal in {n_eq}; largest quotient {float(worst):.6f} (m even {float(by_par[0]):.6f}, m odd {float(by_par[1]):.6f})")
