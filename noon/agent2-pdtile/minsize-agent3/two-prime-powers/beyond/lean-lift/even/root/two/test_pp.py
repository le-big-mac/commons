# Exact test of section 1-3 of result.md.  usage: test_pp.py seed seconds
# Bad at d is tested from the definition: Phi_d divides S(X) (integer long division), not from the slice criterion.
# Multisets are given with multiplicities; the count goes over the signed sums of the distinct residues with
# binomial weights (all signings are counted, exactly, in int64; m <= 60).
import sys, math, random, time, itertools
from math import comb
from fractions import Fraction
import numpy as np
import recp
seed = int(sys.argv[1]); budget = float(sys.argv[2]); rnd = random.Random(seed); t0 = time.time()
def polydiv_exact(num, den):            # integer polynomials, low degree first; den monic
    num = num[:]; q = [0] * (len(num) - len(den) + 1)
    for i in range(len(num) - len(den), -1, -1):
        q[i] = num[i + len(den) - 1]
        for j, dj in enumerate(den): num[i + j] -= q[i] * dj
    assert all(v == 0 for v in num); return q
PHI = {}
def phi(d):
    if d not in PHI:
        num = [-1] + [0] * (d - 1) + [1]
        for e in range(1, d):
            if d % e == 0: num = polydiv_exact(num, phi(e))
        PHI[d] = num
    return PHI[d]
def factor(n):
    f = {}; q = 3
    while n > 1:
        while n % q == 0: f[q] = f.get(q, 0) + 1; n //= q
        q += 2
    return f
def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]
def analyse(n, res, mult):
    """returns dict d -> boolean array over sign-sum configurations, and the weights"""
    D = len(res); grids = [np.arange(-h, h + 1, 2, dtype=np.int64) for h in mult]
    wts = [np.array([comb(h, (h + s) // 2) for s in range(-h, h + 1, 2)], dtype=np.int64) for h in mult]
    mesh = np.meshgrid(*grids, indexing='ij'); wm = np.meshgrid(*wts, indexing='ij')
    N = mesh[0].size; W = np.ones(N, dtype=np.int64)
    for a in wm: W *= a.reshape(N)
    V = np.zeros((N, n), dtype=np.int64)
    for i, b in enumerate(res): V[:, b % n] += mesh[i].reshape(N)
    bad = {}
    for d in divisors(n):
        Vd = np.zeros((N, d), dtype=np.int64)
        for c in range(n): Vd[:, c % d] += V[:, c]
        ph = np.array(phi(d), dtype=np.int64); k = len(ph) - 1
        for deg in range(d - 1, k - 1, -1):
            co = Vd[:, deg].copy()
            Vd[:, deg - k:deg + 1] -= co[:, None] * ph[None, :]
        bad[d] = ~Vd[:, :k].any(axis=1)
    return bad, W
def live_primes(f, res):
    """primes of n with a live level: some class modulo p^(i-1) meets all p classes modulo p^i"""
    out = set()
    for p, vp in f.items():
        for i in range(1, vp + 1):
            grp = {}
            for b in res: grp.setdefault(b % p ** (i - 1), set()).add(b % p ** i)
            if any(len(v) == p for v in grp.values()): out.add(p)
    return out
def first_split(p, vp, res, mult):
    """class sizes at the first branching level of the p-tree (None if no branching)"""
    for j in range(1, vp + 1):
        cl = {}
        for b, h in zip(res, mult): cl[b % p ** j] = cl.get(b % p ** j, 0) + h
        if len(cl) > 1: return tuple(sorted(cl.values()))
    return None
TAB = {3: recp.table(3, 60), 5: recp.table(5, 60), 7: recp.table(7, 36)}; t0 = time.time()
kap = math.sqrt(2 / math.pi)
def a_p(p): return math.sqrt(p) * 2.0 ** (1 - p) / (1 - 0.8165 * math.sqrt(p) * 2.0 ** (2 - p))
def own_term(p, rs):
    E, U, c, _ = TAB[p]; m = sum(rs); k = len(rs)
    if p == 3 and k == 2 and rs[0] in (3, 5, 7) and rs[1] in (3, 5, 7): return Fraction(E[rs[0]] * E[rs[1]] // 2, 1 << m)
    pu = 1; pc = 1
    for r in rs: pu *= U[r]; pc *= c[r]
    t = pu - pc
    if k == p and all((r - rs[0]) % 2 == 0 for r in rs):
        g = 0
        for v in range(2 - rs[0] % 2, rs[0] + 1, 2):
            q = 1
            for r in rs: q *= comb(r, (r + v) // 2)
            g += q
        t += 2 * g
    return Fraction(t, 1 << m)
def gen(n, kind):
    f = factor(n)
    if kind == 'random':
        D = rnd.randint(2, 9); res = rnd.sample(range(n), min(D, n)); mult = [rnd.choice([1, 1, 1, 2, 2, 3]) for _ in res]
    elif kind == 'heavy':
        D = rnd.randint(2, 6); res = [0] + rnd.sample(range(1, n), D - 1); mult = [rnd.randint(8, 30)] + [rnd.choice([1, 1, 2, 2, 3, 4]) for _ in range(D - 1)]
    elif kind == 'even':
        D = rnd.randint(2, 6); res = rnd.sample(range(n), D); mult = [rnd.choice([2, 2, 2, 4, 4, 6, 10]) for _ in res]
    elif kind == 'tree':            # residues that are multiples of large divisors: deep trees, several primes live
        D = rnd.randint(3, 8); res = set()
        while len(res) < D:
            d = rnd.choice(divisors(n)[:-1]); res.add((d * rnd.randrange(n // d)) % n)
        res = sorted(res); mult = [rnd.choice([1, 1, 2, 2, 3, 5]) for _ in res]
    elif kind == 'full':            # a full group at a level i of a prime p of n (the level is live), then more below it
        p = rnd.choice(list(f)); i = rnd.randint(1, f[p]); base = rnd.randrange(n); cl = {}
        for t in range(p):
            b = (base + p ** (i - 1) * t + p ** i * rnd.choice([0, 0, rnd.randrange(n // p ** i)])) % n
            cl[b] = cl.get(b, 0)
        pat = rnd.choice(['ones', 'heavy', 'twos', 'small', 'heavy2'])
        for j, b in enumerate(cl):
            cl[b] = {'ones': 1, 'heavy': (rnd.randint(4, 30) if j == 0 else 1), 'twos': 2, 'small': rnd.choice([1, 1, 2, 3, 4]),
                     'heavy2': (2 * rnd.randint(2, 12) if j == 0 else 2)}[pat]
        for _ in range(rnd.choice([0, 0, 1, 2, 3])):          # extra elements congruent modulo p^i to old ones
            b = (rnd.choice(list(cl)) + p ** i * rnd.randrange(n // p ** i)) % n
            cl[b] = cl.get(b, 0) + rnd.choice([1, 1, 2])
        res = list(cl); mult = [cl[b] for b in res]
        while len(res) > 11: res.pop(); mult.pop()
    else:                           # 'two': two heavy elements
        D = rnd.randint(3, 6); res = rnd.sample(range(n), D); mult = [rnd.randint(5, 14), rnd.randint(5, 14)] + [rnd.choice([1, 1, 2, 2]) for _ in range(D - 2)]
    while True:
        N = 1
        for h in mult: N *= h + 1
        if N <= 40000 and sum(mult) <= (36 if n % 7 == 0 else 60): break
        i = max(range(len(mult)), key=lambda i: mult[i]); mult[i] = max(1, mult[i] // 2)
    return res, mult
MODS = [27, 81, 243, 9, 25, 125, 49, 45, 75, 225, 135, 105, 315, 175, 63, 147, 15, 21, 35]
KINDS = ['random', 'heavy', 'even', 'tree', 'two', 'full', 'full', 'full']
stats = {'multisets': 0, 'X3>0': 0, 'X5>0': 0, 'X7>0': 0, 'own-split equal': 0, 'own-split tests': 0}
best_pp = {0: (0, None), 1: (0, None)}; best_all = {0: (0, None), 1: (0, None)}; best_gap = (0, None)
bym = {}
while time.time() - t0 < budget:
    n = rnd.choice(MODS); kind = rnd.choice(KINDS); res, mult = gen(n, kind); m = sum(mult)
    if m < 3: continue
    bad, W = analyse(n, res, mult); tot = 1 << m; f = factor(n)
    assert int(W.sum()) == tot
    F0 = bad[1]; pp = F0.copy(); allbad = F0.copy(); bound = Fraction(TAB[3][2][m], tot)     # c(m)
    assert int(W[F0].sum()) == (comb(m, m // 2) if m % 2 == 0 else 0)
    for d in bad: allbad |= bad[d]
    for p, vp in f.items():
        Xp = np.zeros_like(F0)
        for i in range(1, vp + 1): Xp |= bad[p ** i]
        pp |= Xp; Xp &= ~F0
        share = Fraction(int(W[Xp].sum()), tot)
        if share > 0 and p in (3, 5, 7): stats[f'X{p}>0'] += 1
        if p in TAB:
            E = TAB[p][0]
            assert share <= Fraction(E[m], tot), ("table", n, res, mult, p, share)
            bound += Fraction(E[m], tot)
            rs = first_split(p, vp, res, mult)
            if rs is None: assert share == 0
            else:
                t = own_term(p, rs); stats['own-split tests'] += 1
                assert share <= t, ("own split", n, res, mult, p, rs, share, t)
                if share == t and t > 0: stats['own-split equal'] += 1
        if p >= 5:
            assert float(share) * math.sqrt(m) <= a_p(p) + 1e-12, ("a_p", n, res, mult, p, share)
        else:
            assert float(share) * math.sqrt(m) <= (0.44 if m % 2 else 0.16) + 1e-12, ("a_3", n, res, mult, share)
    spp = Fraction(int(W[pp].sum()), tot); sall = Fraction(int(W[allbad].sum()), tot)
    assert spp <= bound, ("sum", n, res, mult, spp, bound)
    if len(f) == 1: assert float(spp) * math.sqrt(m) <= 1.0, ("prime power, C=1", n, res, mult, spp)
    lp = live_primes(f, res)
    if len(lp) <= 1:                       # Corollary 5: at most one prime with a live level
        stats['one live prime'] = stats.get('one live prime', 0) + 1
        only = Fraction(int(W[F0 | np.logical_or.reduce([bad[q ** i] for q in lp for i in range(1, f[q] + 1)] + [F0])].sum()), tot)
        assert sall == only, ("Corollary 5: bad = bad at a power of the live prime", n, res, mult, sall, only)
        lim = 1.0 if lp - {3} else (0.9487 if m % 2 == 0 else 0.4331)
        assert sall * sall * m <= Fraction(lim) ** 2, ("Corollary 5: bound", n, res, mult, sall)
        if len(f) > 1: stats['one live prime, composite n'] = stats.get('one live prime, composite n', 0) + 1
    if len(res) <= 4: stats['at most 4 residues'] = stats.get('at most 4 residues', 0) + 1; assert lp <= {3}
    stats['multisets'] += 1; x = float(spp) * math.sqrt(m); y = float(sall) * math.sqrt(m); par = m % 2
    if x > best_pp[par][0]: best_pp[par] = (x, (n, res, mult, str(spp)))
    if y > best_all[par][0]: best_all[par] = (y, (n, res, mult, str(sall)))
    if float(sall - spp) * math.sqrt(m) > best_gap[0]: best_gap = (float(sall - spp) * math.sqrt(m), (n, res, mult, str(sall), str(spp)))
    bym[m] = bym.get(m, 0) + 1
print("seed", seed, "seconds", budget, "NO FAILURE")
print(stats)
print("sizes m met: from", min(bym), "to", max(bym), "; multisets with m >= 20:", sum(v for k, v in bym.items() if k >= 20))
for par in (0, 1):
    print(f"parity {par}: largest sqrt(m)*share(bad at a prime power or 1) = {best_pp[par][0]:.4f} at {best_pp[par][1]}")
    print(f"parity {par}: largest sqrt(m)*share(bad at any d)             = {best_all[par][0]:.4f} at {best_all[par][1]}")
print(f"largest sqrt(m)*(share bad at composite d only) = {best_gap[0]:.4f} at {best_gap[1]}")
