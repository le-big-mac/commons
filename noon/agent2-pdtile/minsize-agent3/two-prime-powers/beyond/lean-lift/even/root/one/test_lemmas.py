"""Tests of the lemmas of result.md by exact arithmetic (integers and fractions), from the definitions.

A multiset on Z_n (n odd) is a list of (residue, multiplicity).  Instead of the 2^m signings the program lists the
vectors of signed sums of the distinct residues, with their binomial weights (so heavy elements are possible).
"bad at d" is tested from the definition: the signed mask reduced modulo Phi_d is 0 (integer arithmetic).

For every multiset:
  T1  (descent, Lemma 2 of the text "two")  bad  <=>  bad at 1 or at some fully live d > 1;
  T2  a fully live d has at least G(d) cells; the map d -> (ranks) is one to one on the fully live d;
      a p-full cell of d sits at a live level of p;
  T3  for every fully live d, every prime p | d and every p-full cell (classes r_0 <= r_1 <= ...), N = k + p - 1:
        share(bad at d) <= 2^-(N-2) c_ceil(m/N)                                  (Lemma B, crude)
        share(bad at d) <= 2^-(N-3) c_(r_1) c_(m - r_0 - r_1 - 2(N-3))           (Lemma C)
        share(bad at d) <= 2^-(N-2) gamma(m, N)  and  <= 2^-(N*-2) gamma(m, N*),  N* = G(d) + P(d) - 1
      and share = 0 if some cell of d has a single element;
  T4  share(bad) <= [m even] c_m + sum over the fully live d of 2^-(N*-2) gamma(m, N*)  <=  B(m);
  T5  (Lemma E, m even) for every fully live prime power d = p^i with k cells and every class L modulo p^i:
        share(bad at d and not bad at 1) <= 2^-(k+2p-5) c_|L|;
  T6  (Lemmas E and F, m even) the same d, with s = m - (the largest class modulo p^i), N = k + p - 1:
        share(bad at d and not bad at 1) <= 2^-(N-2) c_(m-s) min(g, 2 c_(ceil(s/2) - 2(N-3))),
        g = 2^-(p-2), and g = 17/64 if p = 3 and k = 1 (Lemma E');
  T7  (m even) share(bad) <= B_E(m) of bound_even.py (floating point, tolerance 1e-12).
  T8  (the two results of the first text used in Theorem 5; a look, they are not mine)
        m odd:  share(bad at some power of 3) <= c_(m-2)/2;
        m even: share(bad at some 3^i, i >= 1, and not at 1) <= 309/8192.

usage: test_lemmas.py MODE N ARGS...
   exhaustive N M          every multiset of M elements of Z_N that contains 0
   random N M COUNT SEED   random multisets of M elements
   shaped N COUNT SEED     shaped multisets (heavy element and decoration; pairs; fours; cosets; deep trees)
"""
import sys, math, random
from fractions import Fraction
from itertools import combinations_with_replacement
import numpy as np
sys.path.insert(0, '/home/agent3/lean/lift-check/even/root/one')
from bound import c_frac, gamma_exact, cnt_table, B_exact
from bound_even import Even

CMAX = 400
C = c_frac(CMAX)
def c(x): return C[x] if x >= 1 else Fraction(1)

def factor(n):
    f = {}; p = 3
    while n > 1:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 2
    return f

def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]

def polydiv_exact(a, b):                       # integer polynomials, lists low degree first, b monic
    a = a[:]; q = [0] * (len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        q[i] = a[i + len(b) - 1]
        for j, bj in enumerate(b): a[i + j] -= q[i] * bj
    assert not any(a)
    return q

_PHI = {}
def phi_poly(d):
    if d not in _PHI:
        a = [-1] + [0] * (d - 1) + [1]
        for e in divisors(d):
            if e < d: a = polydiv_exact(a, phi_poly(e))
        _PHI[d] = a
    return _PHI[d]

def red_matrix(n, d):                          # column b: X^b modulo Phi_d
    ph = phi_poly(d); deg = len(ph) - 1
    cols = []; v = [1] + [0] * (deg - 1) if deg > 0 else []
    for b in range(d):
        cols.append(v[:])
        w = [0] + v                          # times X
        top = w[deg]; w = w[:deg]
        if top:
            for j in range(deg): w[j] -= top * ph[j]
        v = w
    M = np.array([cols[b % d] for b in range(n)], dtype=np.int64).T.reshape(deg, n)
    return M

class Mod:
    def __init__(self, n):
        self.n = n; self.fac = factor(n); self.divs = divisors(n)
        self.R = {d: red_matrix(n, d) for d in self.divs}
        self.dfac = {d: factor(d) for d in self.divs if d > 1}

STAT = dict(t8=0, t8_eq=0, t7=0, multisets=0, pairs_fl=0, t3=0, t3_eq=0, t5=0, t5_eq=0, t6=0, t4_max=Fraction(0), fl_comp=0, signings=0, t5_pos=0)
BEST = {}
CNT = cnt_table(CMAX)
EVEN = Even(CMAX)
_BE = {}
def BEm(m):
    if m not in _BE: _BE[m] = EVEN.BE(m)
    return _BE[m]
_B = {}
def Bm(m):
    if m not in _B: _B[m] = B_exact(m, C, CNT)
    return _B[m]
_G = {}
def gam(m, N):
    if (m, N) not in _G: _G[(m, N)] = gamma_exact(C, m, N)
    return _G[(m, N)]

def check(mod, items):
    n = mod.n
    acc = {}
    for b, a in items:
        if a > 0: acc[b % n] = acc.get(b % n, 0) + a
    items = sorted(acc.items()); m = sum(a for _, a in items)
    res = [b for b, _ in items]; mult = [a for _, a in items]
    grids = [np.arange(-a, a + 1, 2, dtype=np.int64) for a in mult]
    S = np.array(np.meshgrid(*grids, indexing='ij')).reshape(len(items), -1)
    W = None
    for a, g in zip(mult, grids):
        w = np.array([math.comb(a, (a + int(s)) // 2) for s in g], dtype=object)
        W = w if W is None else np.multiply.outer(W, w)
    W = W.reshape(-1)
    tot = 2 ** m
    assert int(W.sum()) == tot
    bad = {}
    for d in mod.divs:
        V = mod.R[d][:, res] @ S
        bad[d] = ~np.any(V != 0, axis=0)
    def share(mask): return Fraction(int(W[mask].sum()), tot)
    bad_any = np.zeros(S.shape[1], dtype=bool)
    for d in mod.divs: bad_any |= bad[d]
    # live levels of each prime (the brief's sense)
    live = {}
    for p, a in mod.fac.items():
        live[p] = []
        for i in range(1, a + 1):
            groups = {}
            for b in res: groups.setdefault(b % p ** (i - 1), set()).add(b % p ** i)
            if any(len(v) == p for v in groups.values()): live[p].append(i)
    info = {}; keys = {}
    bad_fl = bad[1].copy()
    bound_sum = c(m) if m % 2 == 0 else Fraction(0)
    for d in mod.divs:
        if d == 1: continue
        fd = mod.dfac[d]; g = 1
        for p in fd: g *= p
        d0 = d // g
        cells = {}
        for b, a in items: cells.setdefault(b % d0, []).append((((b - b % d0) // d0) % g, a))
        k = len(cells)
        full = {p: [] for p in fd}
        for cc, els in cells.items():
            for p in fd:
                cl = {}
                for kb, a in els: cl[kb % p] = cl.get(kb % p, 0) + a
                if len(cl) == p: full[p].append(sorted(cl.values()))
        if not all(full[p] for p in fd): continue
        # fully live
        STAT['pairs_fl'] += 1
        if len(fd) > 1: STAT['fl_comp'] += 1
        bad_fl |= bad[d]
        ranks = {}
        for p in fd:
            assert fd[p] in live[p], ("p-full cell at a level that is not live", n, items, d, p)
            ranks[p] = live[p].index(fd[p]) + 1
        key = tuple(sorted(ranks.items()))
        assert key not in keys, ("two fully live d with the same ranks", n, items, d, keys[key])
        keys[key] = d
        G = max(1 + (j - 1) * (p - 1) for p, j in ranks.items())
        assert k >= G, ("fewer cells than G(d)", n, items, d, k, G)
        P = max(fd); Nstar = G + P - 1
        sh = share(bad[d])
        sizes = [sum(a for _, a in els) for els in cells.values()]
        if min(sizes) == 1: assert sh == 0, ("a cell of one element", n, items, d)
        if Nstar <= m: bound_sum += Fraction(1, 2 ** (Nstar - 2)) * gam(m, Nstar)
        else: assert sh == 0, ("N* > m but share > 0", n, items, d)
        if sh > 0:
            assert sh <= Fraction(1, 2 ** (Nstar - 2)) * gam(m, Nstar), ("N* bound", n, items, d, sh)
        for p in fd:
            N = k + p - 1
            for cl in full[p]:
                r0, r1 = cl[0], cl[1]
                STAT['t3'] += 1
                b1 = Fraction(1, 2 ** (N - 2)) * c(-(-m // N))
                b2 = Fraction(1, 2 ** (N - 3)) * c(r1) * c(m - r0 - r1 - 2 * (N - 3))
                b3 = Fraction(1, 2 ** (N - 2)) * gam(m, N) if N <= m else None
                assert sh <= b1, ("Lemma B", n, items, d, p, sh, b1)
                assert sh <= b2, ("Lemma C", n, items, d, p, sh, b2)
                if b3 is not None: assert b2 <= b3, ("gamma below Lemma C", n, items, d, p, b2, b3)
                else: assert sh == 0
                if sh == b2: STAT['t3_eq'] += 1
        # Lemmas E and F: prime powers, m even
        if len(fd) == 1 and m % 2 == 0:
            p = P; i = fd[p]
            cls = {}
            for b, a in items: cls[b % p ** i] = cls.get(b % p ** i, 0) + a
            e = share(bad[d] & ~bad[1])
            ell = max(cls.values()); s = m - ell; N = k + p - 1
            for L in set(cls.values()):
                STAT['t5'] += 1
                bE = Fraction(1, 2 ** (k + 2 * p - 5)) * c(L)
                assert e <= bE, ("Lemma E", n, items, d, e, bE, L)
                if e == bE: STAT['t5_eq'] += 1
            if e > 0: STAT['t5_pos'] += 1
            STAT['t6'] += 1
            g = Fraction(17, 64) if (p == 3 and k == 1) else Fraction(1, 2 ** (p - 2))
            bF = Fraction(1, 2 ** (N - 2)) * c(m - s) * min(g, 2 * c(-(-s // 2) - 2 * (N - 3)))
            assert e <= bF, ("Lemma F", n, items, d, e, bF)
    assert np.array_equal(bad_fl, bad_any), ("descent fails", n, items)
    if 3 in mod.fac and m >= 3:
        b3 = np.zeros(S.shape[1], dtype=bool)
        for i in range(1, mod.fac[3] + 1): b3 |= bad[3 ** i]
        if m % 2:
            x = share(b3 | bad[1])
            assert x <= c(m - 2) / 2, ("T8 odd: first text, Theorem A", n, items, x)
            if x == c(m - 2) / 2: STAT['t8_eq'] += 1
        else:
            x = share(b3 & ~bad[1])
            assert x <= Fraction(309, 8192), ("T8 even: first text, Theorem B", n, items, x)
        STAT['t8'] += 1
    sb = share(bad_any)
    assert sb <= bound_sum, ("T4: union bound over the fully live d", n, items, sb, bound_sum)
    assert bound_sum <= Bm(m), ("T4: B(m)", n, items, bound_sum, Bm(m))
    if m % 2 == 0:
        assert float(sb) <= BEm(m) + 1e-12, ("T7: B_E(m)", n, items, sb, BEm(m))
        STAT['t7'] += 1
    STAT['multisets'] += 1; STAT['signings'] += tot
    if sb > BEST.get(m, (Fraction(0),))[0]: BEST[m] = (sb, n, items)
    return sb

def shaped(mod, rng):
    n = mod.n; kind = rng.randrange(8)
    units = [x for x in range(1, n)]
    if kind == 0:      # a heavy element and a decoration
        h = rng.randrange(1, 41); r = rng.randrange(1, 6)
        return [(0, h)] + [(rng.choice(units), 1) for _ in range(r)]
    if kind == 1:      # all elements in pairs
        r = rng.randrange(2, 7)
        return [(rng.randrange(n), 2) for _ in range(r)]
    if kind == 2:      # fours and pairs, a heavy even element
        r = rng.randrange(2, 5)
        return [(0, 2 * rng.randrange(1, 15))] + [(rng.choice(units), rng.choice([2, 4])) for _ in range(r)]
    if kind == 3:      # a heavy element and one element in each nonzero class modulo a prime of n (and perhaps another)
        ps = list(mod.fac); out = [(0, rng.randrange(1, 30))]
        for p in rng.sample(ps, rng.randrange(1, min(2, len(ps)) + 1)):
            out += [(t * n // p, rng.choice([1, 1, 2])) for t in range(1, p)]
        return out
    if kind == 4:      # deep tree of the smallest prime: full groups at several levels, random multiplicities
        p = min(mod.fac); a = mod.fac[p]; q = n // p ** a
        out = [(0, rng.randrange(1, 12))]
        for i in range(a):
            for t in range(1, p):
                if rng.random() < 0.9: out.append((t * p ** i * q * rng.choice([1, 1, 1, 2]) % n, rng.choice([1, 1, 2, 3])))
        return out
    if kind == 5:      # few residues with multiplicities
        r = rng.randrange(2, 6)
        return [(rng.randrange(n), rng.randrange(1, 9)) for _ in range(r)]
    if kind == 6:      # union of cosets of the subgroups of prime order
        out = []
        for _ in range(rng.randrange(1, 4)):
            p = rng.choice(list(mod.fac)); x = rng.randrange(n)
            out += [((x + t * n // p) % n, 1) for t in range(p)]
        if rng.random() < 0.5: out.append((rng.randrange(n), rng.randrange(1, 20)))
        return out
    # a heavy class modulo a prime (different residues in one class) and singles in the other classes
    p = rng.choice(list(mod.fac)); out = []
    for _ in range(rng.randrange(1, 4)): out.append((p * rng.randrange(n // p), rng.randrange(1, 10)))
    out += [((t + p * rng.randrange(n // p)) % n, rng.choice([1, 2])) for t in range(1, p)]
    return out

def grid_size(items):
    acc = {}
    for b, a in items: acc[b] = acc.get(b, 0) + a
    g = 1
    for a in acc.values(): g *= a + 1
    return g, sum(acc.values())

def main():
    mode = sys.argv[1]; n = int(sys.argv[2]); mod = Mod(n)
    if mode == 'exhaustive':
        m = int(sys.argv[3])
        for rest in combinations_with_replacement(range(n), m - 1):
            check(mod, [(0, 1)] + [(b, 1) for b in rest])
    elif mode == 'random':
        m = int(sys.argv[3]); count = int(sys.argv[4]); rng = random.Random(int(sys.argv[5]))
        for _ in range(count):
            check(mod, [(rng.randrange(n), 1) for _ in range(m)])
    elif mode == 'shaped':
        count = int(sys.argv[3]); rng = random.Random(int(sys.argv[4])); done = 0
        while done < count:
            items = [(b % n, a) for b, a in shaped(mod, rng)]
            g, m = grid_size(items)
            if g > 60000 or m > CMAX or m < 3: continue
            check(mod, items); done += 1
    print(' '.join(sys.argv[1:]), '| no failure |',
          ' '.join(f"{k}={v}" for k, v in STAT.items() if k != 't4_max'))
    for m in sorted(BEST):
        sb, nn, items = BEST[m]
        if m <= 16 or m % 10 == 0:
            print(f"   largest bad share met, m = {m}: {sb} = {float(sb):.5f}, times sqrt(m) = {float(sb) * math.sqrt(m):.4f}, B(m) = {float(Bm(m)):.4f}, at {items}")

if __name__ == '__main__':
    main()
