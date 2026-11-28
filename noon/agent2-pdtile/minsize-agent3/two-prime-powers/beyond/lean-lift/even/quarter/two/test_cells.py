#!/usr/bin/env python3
"""Tests of the lemmas of result.md on actual multisets, all signings, exact integers.

For a multiset B of m elements on Z_n (n odd) and every signing with first sign + (the events are even):
  (1) "bad at d" by the remainder of the signed mask modulo Phi_d (the definition);
  (2) cell criterion: bad at d  iff  every class modulo d0 = d/rad(d) has a signed sum 0 at a root of unity of
      order rad(d)                                                                         [Lemma 1]
  (3) descent: a bad signing is bad at 1 or at a fully live d > 1                          [Lemma 2]
  (4) for every fully live d > 1 and every prime p | d:  share bad at d  <=  product over the cells of the cell
      value through p (actual sizes)  <=  BF_p(G(d), m) of lo_union2.py                    [Lemmas 3, 4, 5]
  (5) number of cells of d >= G(d) = max_p (1 + (rank_p - 1)(p - 1))                       [Lemma 5]
  (6) share (bad at some p^i, i >= 1, and not at 1) <= U_p(m) of ptree.py                  [section 5]
  (7) share bad <= [m even] c_m + sum_p U_p(m) + sum over fully live composite d of min_p BF_p(G(d), m)

usage: test_cells.py MODE n m COUNT SEED     MODE = random | all | shaped
"""
import sys, random, itertools
from fractions import Fraction
from math import comb, gcd
import numpy as np
import lo_union2 as L


def factor(n):
    f = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


_cyc = {}
def cyclo(d):
    """coefficients of Phi_d, lowest first (python ints)"""
    if d in _cyc:
        return _cyc[d]
    num = [-1] + [0] * (d - 1) + [1]
    for e in divisors(d):
        if e < d:
            den = cyclo(e)
            q = [0] * (len(num) - len(den) + 1)
            num = num[:]
            for i in range(len(q) - 1, -1, -1):
                q[i] = num[i + len(den) - 1] // den[-1]
                for j, cj in enumerate(den):
                    num[i + j] -= q[i] * cj
            assert all(x == 0 for x in num)
            num = q
    _cyc[d] = num
    return num


_tab = {}
def powtable(d):
    """row b: X^b mod Phi_d, b = 0..d-1"""
    if d in _tab:
        return _tab[d]
    phi = cyclo(d)
    deg = len(phi) - 1
    rows = []
    cur = [0] * deg
    if deg == 0:
        raise ValueError
    cur[0] = 1
    if d == 1:
        rows = [[1]]
    else:
        for b in range(d):
            rows.append(cur[:])
            top = cur[-1]
            cur = [0] + cur[:-1]
            if top:
                for j in range(deg):
                    cur[j] -= top * phi[j]
    _tab[d] = np.array(rows, dtype=np.int64)
    return _tab[d]


def signings(m):
    k = 2 ** (m - 1)
    E = np.ones((k, m), dtype=np.int64)
    for j in range(1, m):
        E[:, j] = 1 - 2 * ((np.arange(k) >> (j - 1)) & 1)
    return E


def rad(d):
    r = 1
    for p in factor(d):
        r *= p
    return r


class Ctx:
    def __init__(self, mmax):
        self.T = L.Tab(mmax, True)
        self.gen = {}
        for p in L.primes_upto(mmax):
            Gmax = max(1, (mmax - p) // 2 + 1)
            vnf, vf = L.general_tables(p, self.T)
            _, bf = L.level_dp(vnf, vf, Gmax, mmax, self.T.zero)
            self.gen[p] = (Gmax, bf)
        self.U = L.read_exact_U()
        self.BFcache = {}

    def BF(self, p, G, m):
        key = (p, m)
        if key not in self.BFcache:
            Gmax, bf = self.gen[p]
            self.BFcache[key] = L.suffix_max(bf, Gmax, m, self.T.zero)
        B = self.BFcache[key]
        return B[G] if G < len(B) else Fraction(0)


def cell_value(ctx, p, sizes):
    """bound for the share of signings of a cell that vanish, the cell seen through p; sizes: the p class sizes"""
    T = ctx.T
    half, quarter = Fraction(1, 2), Fraction(1, 4)
    def z(r):
        if r == 1: return Fraction(0)
        if r == 2: return half
        if r == 3: return Fraction(0) if p == 3 else quarter
        return T.c[r]
    def cnz(r):
        if r == 1: return half
        if r == 2: return quarter
        return T.c[r]
    occ = [r for r in sizes if r > 0]
    zp = Fraction(1)
    for r in occ:
        zp *= z(r)
    if len(occ) < p:
        return zp
    others = sorted(occ)[1:]
    nz = Fraction(1)
    for r in others:
        nz *= cnz(r)
    if p == 3 and min(occ) == 1 and 2 in others:
        nz = Fraction(0)
    return zp + nz


def check(ctx, n, B, E, stats):
    m = len(B)
    fn = factor(n)
    half = E.shape[0]
    Bmat = np.array(B)
    bad = {}
    for d in divisors(n):
        tab = powtable(d)
        vals = E @ tab[Bmat % d]
        bad[d] = ~vals.any(axis=1)
    # p-trees: live levels
    live = {}
    for p, a in fn.items():
        lv = []
        for k in range(1, a + 1):
            groups = {}
            for b in B:
                groups.setdefault(b % p ** (k - 1), set()).add(b % p ** k)
            if any(len(s) == p for s in groups.values()):
                lv.append(k)
        live[p] = lv
    anybad = np.zeros(half, dtype=bool)
    covered = bad[1].copy()
    comp_bound = Fraction(0)
    pp_union = {p: np.zeros(half, dtype=bool) for p in fn}
    for d in divisors(n):
        anybad |= bad[d]
        if d == 1:
            continue
        fd = factor(d)
        g = rad(d); d0 = d // g
        cells = {}
        for idx, b in enumerate(B):
            cells.setdefault(b % d0, []).append(idx)
        # (2) cell criterion
        tabg = powtable(g)
        allv = np.ones(half, dtype=bool)
        for c, idxs in cells.items():
            ks = np.array([((B[i] - c) // d0) % g for i in idxs])
            v = E[:, idxs] @ tabg[ks]
            allv &= ~v.any(axis=1)
        assert (allv == bad[d]).all(), ("cell criterion", n, B, d)
        stats['cellcrit'] += 1
        # fully live?
        full_for = {}
        for p in fd:
            full_for[p] = any(len({((B[i] - c) // d0) % p for i in idxs}) == p for c, idxs in cells.items())
        fully = all(full_for.values())
        if len(fd) == 1:
            p = next(iter(fd))
            pp_union[p] |= bad[d]
        if not fully:
            continue
        covered |= bad[d]
        share = Fraction(int(bad[d].sum()), half)
        # ranks and G(d)
        G = 1
        for p, i in fd.items():
            assert i in live[p], ("fully live but level not live", n, B, d, p)
            j = live[p].index(i) + 1
            G = max(G, 1 + (j - 1) * (p - 1))
        assert len(cells) >= G, ("number of cells", n, B, d)
        bounds = []
        for p in fd:
            prodv = Fraction(1)
            for c, idxs in cells.items():
                sizes = [0] * p
                for i in idxs:
                    sizes[((B[i] - c) // d0) % p] += 1
                prodv *= cell_value(ctx, p, sizes)
            assert share <= prodv, ("cell product bound", n, B, d, p, share, prodv)
            bf = ctx.BF(p, G, m)
            assert prodv <= bf, ("BF bound", n, B, d, p, prodv, bf)
            bounds.append(bf)
            stats['dbounds'] += 1
            if share == prodv and share > 0:
                stats['dbound_attained'] += 1
        if len(fd) >= 2:
            comp_bound += min(bounds)
    # (3) descent
    assert (covered == anybad).all(), ("descent", n, B)
    # (6) prime powers
    total = Fraction(comb(m, m // 2), 2 ** m) if m % 2 == 0 else Fraction(0)
    for p in fn:
        new = pp_union[p] & ~bad[1]
        sh = Fraction(int(new.sum()), half)
        if p <= m:
            u = ctx.U[(p, m)]
        else:
            u = Fraction(0)
        assert sh <= u, ("U_p", n, B, p, sh, u)
        if sh == u and u > 0:
            stats['U_attained'] += 1
        total += u
    total += comp_bound
    shb = Fraction(int(anybad.sum()), half)
    assert shb <= total, ("union", n, B, shb, total)
    stats['multisets'] += 1
    stats['signings'] += half
    if shb > stats['maxbad'].get(m, (Fraction(0),))[0]:
        stats['maxbad'][m] = (shb, n, tuple(B))


def shaped(rng, n, m):
    """multisets shaped like the hard cases: few residues, heavy classes, even class sizes, repeated elements"""
    fn = factor(n)
    kind = rng.randrange(5)
    if kind == 0:      # few distinct elements with multiplicities
        k = rng.randint(2, min(m, 6))
        pts = [rng.randrange(n) for _ in range(k)]
        return sorted(rng.choice(pts) for _ in range(m))
    if kind == 1:      # one heavy element and a coset-like rest
        base = rng.randrange(n)
        p = rng.choice(list(fn))
        step = n // p
        B = [base] * (m - min(m - 1, p - 1)) + [(base + (j + 1) * step) % n for j in range(min(m - 1, p - 1))]
        return sorted(B)
    if kind == 2:      # pairs (all class sizes even)
        pts = [rng.randrange(n) for _ in range(m // 2)]
        B = pts + pts + ([rng.randrange(n)] if m % 2 else [])
        return sorted(B)
    if kind == 3:      # union of cosets of prime order subgroups, padded
        B = []
        while len(B) < m:
            p = rng.choice(list(fn))
            base = rng.randrange(n)
            step = n // p ** rng.randint(1, fn[p])
            B += [(base + j * step) % n for j in range(p)]
        return sorted(B[:m])
    # rows and columns of a p x q block
    ps = list(fn)
    if len(ps) >= 2:
        p, q = rng.sample(ps, 2)
        base = rng.randrange(n)
        B = [(base + j * (n // p)) % n for j in range(p)] + [(base + j * (n // q)) % n for j in range(1, q)]
        while len(B) < m:
            B.append(rng.choice(B))
        return sorted(B[:m])
    return sorted(rng.randrange(n) for _ in range(m))


def main():
    mode, n, m, count, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    rng = random.Random(seed)
    ctx = Ctx(max(m, 3))
    E = signings(m)
    stats = dict(cellcrit=0, dbounds=0, dbound_attained=0, U_attained=0, multisets=0, signings=0, maxbad={})
    if mode == 'all':
        it = ((0,) + t for t in itertools.combinations_with_replacement(range(n), m - 1))
        for B in it:
            check(ctx, n, list(B), E, stats)
    else:
        for _ in range(count):
            B = shaped(rng, n, m) if mode == 'shaped' else sorted(rng.randrange(n) for _ in range(m))
            check(ctx, n, B, E, stats)
    mb = stats.pop('maxbad')
    print("mode=%s n=%d m=%d seed=%d :" % (mode, n, m, seed), stats,
          "largest bad share:", {k: (str(v[0]), v[1], v[2]) for k, v in mb.items()}, "NO FAILURE", flush=True)


if __name__ == '__main__':
    main()
