"""Looking for a refutation of "beta(m) <= 1/sqrt(m)" (exact arithmetic, own routines from lib.py).
mode K:      K_same and K_other of a decoration D (items b:a, none at 0) beside a heavy element at 0:
             the expected number of distinct integers v, of each parity class, with Q(zeta) + v = 0 for some n-th root
             of unity zeta (Q = signed mask of D).  K_same counts v = r (mod 2), r = |D| (the case m even).
             beta(m) sqrt(m) -> at least K_same sqrt(2/pi) along even m, so K_same > sqrt(pi/2) = 1.2533 would refute (b).
mode share:  the exact share of bad signings of a multiset, times sqrt(m).
usage: search.py K N 'b:a,b:a,...' [...]            exact K of given decorations
       search.py Kclimb N SEED TRIES STEPS GRIDMAX  hill-climbing on multiplicities for K_same
       search.py share N 'b:a,...' [...]            exact share of given multisets
       search.py climb N M SEED TRIES STEPS GRIDMAX hill-climbing on multisets of M elements for share * sqrt(M)"""
import sys, math, random
from fractions import Fraction
import numpy as np
from lib import *
BIG = 10 ** 9
def Kvals(n, items):
    items = [(b, a) for b, a in items if a > 0 and b % n != 0]
    if not items: return Fraction(1), Fraction(0)
    S, W, r = grid(items); G = S.shape[1]; ds = divisors(n)
    M = np.full((len(ds), G), BIG, dtype=np.int64)
    for i, d in enumerate(ds):
        V = red(d)[:, [b % d for b, _ in items]] @ S
        isint = ~np.any(V[1:] != 0, axis=0) if V.shape[0] > 1 else np.ones(G, dtype=bool)
        M[i, isint] = -V[0, isint]
    M.sort(axis=0)
    new = np.ones_like(M, dtype=bool); new[1:] = M[1:] != M[:-1]
    valid = (M != BIG) & new
    same = (valid & ((M - r) % 2 == 0)).sum(axis=0); other = (valid & ((M - r) % 2 != 0)).sum(axis=0)
    tot = 2 ** r
    return Fraction(int((W * same.astype(object)).sum()), tot), Fraction(int((W * other.astype(object)).sum()), tot)
def share(n, items):
    items = [(b % n, a) for b, a in items if a > 0]
    S, W, m = grid(items); bad = np.zeros(S.shape[1], dtype=bool)
    for d in divisors(n): bad |= bad_mask(d, items, S)
    return Fraction(int(W[bad].sum()), 2 ** m), m
def parse(t): return [(int(x.split(':')[0]), int(x.split(':')[1])) for x in t.split(',') if x]
def gsize(st): return math.prod(a + 1 for a in st.values() if a > 0)
if __name__ == '__main__':
    mode = sys.argv[1]; n = int(sys.argv[2])
    if mode == 'K':
        for t in sys.argv[3:]:
            ks, ko = Kvals(n, parse(t))
            print(f"n = {n}  D = {t}:  K_same = {ks} = {float(ks):.6f}   K_other = {ko} = {float(ko):.6f}   K_same sqrt(2/pi) = {float(ks) * math.sqrt(2 / math.pi):.4f}", flush=True)
    elif mode == 'share':
        for t in sys.argv[3:]:
            s, m = share(n, parse(t))
            print(f"n = {n}  {t}:  m = {m}  bad share {s} = {float(s):.6f}  times sqrt(m) = {float(s) * math.sqrt(m):.4f}", flush=True)
    elif mode == 'Kclimb':
        seed, tries, steps, gmax = map(int, sys.argv[3:7]); rng = random.Random(seed); best = (Fraction(0), None)
        for t in range(tries):
            st = {b: 0 for b in range(1, n)}
            for _ in range(rng.randrange(2, 7)): st[rng.randrange(1, n)] += rng.choice((1, 2, 2, 4))
            cur = Kvals(n, list(st.items()))[0]
            for _ in range(steps):
                s2 = dict(st); b = rng.randrange(1, n); s2[b] = max(0, s2[b] + rng.choice((-2, -1, 1, 2)))
                if rng.random() < 0.3: b = rng.randrange(1, n); s2[b] = max(0, s2[b] + rng.choice((-2, -1, 1, 2)))
                if gsize(s2) > gmax: continue
                c2 = Kvals(n, list(s2.items()))[0]
                if c2 >= cur: st, cur = s2, c2
            if cur > best[0]: best = (cur, sorted((b, a) for b, a in st.items() if a))
            print(f"n = {n} try {t}: K_same {cur} = {float(cur):.6f} at {sorted((b, a) for b, a in st.items() if a)}", flush=True)
        print(f"n = {n}  seed {seed}: best K_same {best[0]} = {float(best[0]):.6f}  (threshold 1.2533)  at {best[1]}", flush=True)
    elif mode == 'climb':
        m, seed, tries, steps, gmax = map(int, sys.argv[3:8]); rng = random.Random(seed); best = (Fraction(0), None)
        for t in range(tries):
            st = {b: 0 for b in range(n)}; st[0] = m - 2 * (m // 4)
            for _ in range(m // 4): st[rng.randrange(1, n)] += 2
            cur = share(n, list(st.items()))[0]
            for _ in range(steps):
                s2 = dict(st); a = rng.choice([b for b in s2 if s2[b] > 0]); b = rng.randrange(n); k = min(s2[a], rng.choice((1, 2)))
                if a == b: continue
                s2[a] -= k; s2[b] += k
                if gsize(s2) > gmax: continue
                c2 = share(n, list(s2.items()))[0]
                if c2 >= cur: st, cur = s2, c2
            if cur > best[0]: best = (cur, sorted((b, a) for b, a in st.items() if a))
            print(f"n = {n} m = {m} try {t}: share {cur} = {float(cur):.6f}  times sqrt(m) = {float(cur) * math.sqrt(m):.4f} at {sorted((b, a) for b, a in st.items() if a)}", flush=True)
        print(f"n = {n}  m = {m}  seed {seed}: best share {best[0]} = {float(best[0]):.6f}  times sqrt(m) = {float(best[0]) * math.sqrt(m):.4f}  at {best[1]}", flush=True)
