# thm7_check.py -- Theorem 7 end to end on cyclic groups, and the primitivity of the sibling cube functions.
# n = m * q^b (q = 0: n = m, over the integers).  Z_m is read as the tree box with one coordinate Z_{p^a} per prime
# power of m.  For a multiset B on Z_n: g = indicator of the cells (classes modulo m) with an odd number of elements,
# or 2*delta if there is none; random product patterns sigma (one arbitrary sign vector per coordinate) are tried
# until sigma*g is good at every level of the tree box modulo q; B is signed with cell sums sigma(c) g(c); the signed
# mask is then divided by Phi_d for EVERY d | n (exact integer long division) and must leave a nonzero remainder.
# Also counted: how often "all signs +" has a cyclotomic divisor (so that the samples test something).
# usage: python thm7_check.py m q b N seed
import sys, random, itertools
import numpy as np
from sympy import factorint, divisors, cyclotomic_poly, Symbol
import tb

X = Symbol("x")
_phi = {}
def phi_coeffs(d):
    if d not in _phi:
        from sympy import Poly
        _phi[d] = np.array([int(t) for t in Poly(cyclotomic_poly(d, X), X).all_coeffs()][::-1], dtype=object)  # low to high
    return _phi[d]

def has_divisor(S, n):
    """S: integer array of length n (coefficients).  Returns the list of d | n with Phi_d | S."""
    out = []
    for d in divisors(n):
        R = np.array(S.reshape(n // d, d).sum(axis=0), dtype=object)     # S modulo X^d - 1
        ph = phi_coeffs(d); dg = len(ph) - 1
        for i in range(d - 1, dg - 1, -1):
            c = R[i]
            if c: R[i - dg:i + 1] -= c * ph
        if not any(R[:dg]): out.append(d)
    return out

def check_primitive(m, rnd, trials):
    """the sibling cube functions on Z_{d'} are primitive (sum 0 over every coset of every subgroup of prime order)."""
    f = factorint(m)
    for _ in range(trials):
        lev = {p: rnd.randrange(0, a + 1) for p, a in f.items()}
        dd = 1
        for p, i in lev.items(): dd *= p ** i
        pairs = {}
        for p, i in lev.items():
            if i == 0: continue
            u = rnd.randrange(p ** i)
            u2 = (u + rnd.randrange(1, p) * p ** (i - 1)) % p ** i
            pairs[p] = (u, u2)
        h = np.zeros(dd, dtype=np.int64)
        for y in range(dd):
            w = 1
            for p, (u, u2) in pairs.items():
                r = y % p ** lev[p]
                w *= (1 if r == u else 0) - (1 if r == u2 else 0)
            h[y] = w
        for p in factorint(dd):
            step = dd // p
            for y in range(step):
                assert sum(int(h[(y + t * step) % dd]) for t in range(p)) == 0, "not primitive"
    return trials

def make_B(n, m, rnd, kind):
    B = []
    if kind == 0:                     # random set
        k = rnd.randrange(1, min(n, 60))
        B = rnd.sample(range(n), k)
    elif kind == 1:                   # union of cosets of subgroups, a few points changed
        S = set()
        for _ in range(rnd.randrange(1, 4)):
            d = rnd.choice([t for t in divisors(n) if 1 < t < n])
            c = rnd.randrange(n)
            S |= {(c + t * d) % n for t in range(n // d)}
        for _ in range(rnd.randrange(0, 3)):
            S ^= {rnd.randrange(n)}
        B = sorted(S)
    elif kind == 2:                   # multiset
        k = rnd.randrange(1, 40)
        B = [rnd.randrange(n) for _ in range(k)] + [rnd.randrange(n)] * rnd.randrange(0, 4)
    elif kind == 3:                   # every cell modulo m even (needs n > m), else a small set
        if n > m:
            k = rnd.randrange(1, 6)
            for _ in range(k):
                x = rnd.randrange(n)
                B += [x, (x + m * rnd.randrange(1, n // m)) % n]
        else:
            B = rnd.sample(range(n), 2)
    else:                             # a class modulo a divisor, restricted: product-like sets
        d = rnd.choice([t for t in divisors(n) if 1 < t < n])
        e = rnd.choice([t for t in divisors(n) if 1 < t < n])
        B = sorted({(a * d + b_ * e) % n for a in range(rnd.randrange(1, 6)) for b_ in range(rnd.randrange(1, 6))})
    return B

def main():
    m, q, b, N, seed = [int(t) for t in sys.argv[1:6]]
    n = m * (q ** b if q else 1)
    qq = q or None
    rnd = random.Random(seed)
    f = factorint(m)
    spec = [(p, a) for p, a in sorted(f.items())]
    mods = [p ** a for p, a in spec]
    nprim = check_primitive(m, rnd, 200)
    cells_index = [tuple(c % M for M in mods) for c in range(m)]
    tries_total = 0; maxtries = 0; allplus_bad = 0; done = 0; viol = 0
    for it in range(N):
        B = make_B(n, m, rnd, it % 5)
        if not B: continue
        cells = {}
        for x in B: cells.setdefault(x % m, []).append(x)
        odd = [c for c, l in cells.items() if len(l) % 2]
        g = np.zeros(mods, dtype=np.int64)
        if odd:
            for c in odd: g[cells_index[c]] = 1
        else:
            c0 = next(iter(cells))
            g[cells_index[c0]] = 2
        tries = 0
        while True:
            tries += 1
            sig = [np.array([rnd.choice([1, -1]) for _ in range(M)], dtype=np.int64) for M in mods]
            h = g
            for j, s in enumerate(sig):
                shp = [1] * len(mods); shp[j] = mods[j]
                h = h * s.reshape(shp)
            if tb.good_one(h, spec, qq): break
            assert tries < 2000
        tries_total += tries; maxtries = max(maxtries, tries)
        S = np.zeros(n, dtype=np.int64)
        for c, l in cells.items():
            t = int(h[cells_index[c]])
            sg = 1 if t >= 0 else -1
            for idx, x in enumerate(l):
                if idx < abs(t): S[x] += sg
                else: S[x] += 1 if (idx - abs(t)) % 2 == 0 else -1
            assert sum(1 for _ in l) % 2 == abs(t) % 2 and abs(t) <= len(l)
        # the signing is a signing of B
        cnt = np.zeros(n, dtype=np.int64)
        for x in B: cnt[x] += 1
        assert ((S - cnt) % 2 == 0).all() and (np.abs(S) <= cnt).all()
        bad = has_divisor(S, n)
        if bad: viol += 1; print("VIOLATION", B, bad)
        if has_divisor(cnt, n): allplus_bad += 1
        done += 1
    print("n = %d = %d * %s^%d, tree box %s over %s: %d multisets; a pattern good in the tree box found after %.2f random patterns on average (at most %d); signings with a cyclotomic divisor: %d; (all signs + had a divisor for %d of them); sibling cube functions primitive in %d random cases"
          % (n, m, q if q else 1, b, spec, "F_%d" % q if q else "Q", done, tries_total / max(done, 1), maxtries, viol, allplus_bad, nprim))

if __name__ == "__main__":
    main()
