# Referee test of Lemma G and Theorem 6 end to end on Z_n, n = m * q^b.
# usage: test_6.py m q b nsets seed      (q = 0: n = m, field Q)
import sys, random, itertools, time
import numpy as np
from sympy import cyclotomic_poly, Poly, symbols, factorint, divisors
from boxlib import *

m, q, b, nsets, seed = [int(x) for x in sys.argv[1:6]]
random.seed(seed)
np.random.seed(seed)
n = m * (q ** b if q else 1)
X = symbols('X')
t0 = time.time()

fac = factorint(m)
coords = [(p, e) for p in sorted(fac) for e in range(1, fac[p] + 1)]
sides = [p for (p, e) in coords]
k = len(coords)


def dig(x, p, e):
    return (x % p ** e) // p ** (e - 1)


cell = np.array([[dig(c, p, e) for (p, e) in coords] for c in range(m)]).reshape(m, k)
assert len({tuple(r) for r in cell.tolist()}) == m, 'digit map not a bijection'

# tree levels <-> divisors d' of m
tree = {}
for choice in itertools.product(*[range(fac[p] + 1) for p in sorted(fac)]):
    dprime = 1
    P = []
    for p, i in zip(sorted(fac), choice):
        if i:
            dprime *= p ** i
            P.append(coords.index((p, i)))
    tree[dprime] = frozenset(P)
assert sorted(tree) == divisors(m)
TL = list(tree.values())

# Lemma G: h is well defined on Z_d', primitive, and <h,T> is the cube sum (random cubes, random T)
for dprime, P in tree.items():
    for _ in range(6):
        cube = {i: random.sample(range(sides[i]), 2) for i in P}
        def h(y):
            w = 1
            for i in P:
                p, e = coords[i]
                w *= (dig(y, p, e) == cube[i][0]) - (dig(y, p, e) == cube[i][1])
            return w
        hv = [h(y) for y in range(dprime)]
        assert all(h(y) == hv[y % dprime] for y in range(m)), 'h not well defined on Z_d'
        for p in factorint(dprime):
            for y in range(dprime // p):
                assert sum(hv[(y + t * (dprime // p)) % dprime] for t in range(p)) == 0, 'h not primitive'
        T = [random.randint(-3, 3) for _ in range(m)]
        fold = [0] * dprime
        for x in range(m):
            fold[x % dprime] += T[x]
        lhs = sum(hv[y] * fold[y] for y in range(dprime))
        rhs = sum(T[x] * h(x) for x in range(m))
        assert lhs == rhs

phis = {d: np.array([int(c) for c in Poly(cyclotomic_poly(d, X), X).all_coeffs()][::-1], dtype=np.int64) for d in divisors(n)}


def divisible(Smat, d):
    """rows of Smat (integer polynomials of degree < n): is Phi_d | row ?  exact long division"""
    R = np.zeros((Smat.shape[0], d), dtype=np.int64)
    for r in range(n // d):
        R += Smat[:, r * d:(r + 1) * d]
    phi = phis[d]
    deg = len(phi) - 1
    for i in range(d - 1, deg - 1, -1):
        c = R[:, i].copy()
        R[:, i - deg:i + 1] -= c[:, None] * phi[None, :]
    assert np.abs(R).max() < 2 ** 50
    return ~R.any(axis=1)


# (1) direct test of the chain Lemma G + Corollary on multiples of Phi_d
viol = 0
nmult = 0
for d in divisors(n):
    dprime = d
    if q:
        while dprime % q == 0:
            dprime //= q
    P = tree[dprime]
    phi = phis[d]
    for _ in range(8):
        Apoly = np.array([random.randint(-2, 2) for _ in range(n)], dtype=np.int64)
        full = np.convolve(Apoly, phi)
        S = np.zeros(n, dtype=np.int64)
        for i, c in enumerate(full):
            S[i % n] += c
        assert divisible(S[None, :], d)[0]
        fold = np.zeros(m, dtype=np.int64)
        for x in range(n):
            fold[x % m] += S[x]
        g = np.zeros(sides, dtype=np.int64)
        for c in range(m):
            g[tuple(cell[c])] = fold[c]
        cs = cube_sums_plain(g, sides, P, q)
        nmult += 1
        if cs.any():
            viol += 1
            print('VIOLATION: Phi_%d | S but a cube sum at the tree level of %d is nonzero' % (d, dprime))
print('n = %d = %d * %s  digit box %s  tree levels %d' % (n, m, ('%d^%d' % (q, b)) if q else '1', sides, len(TL)))
print('  Lemma G checked on all tree levels; multiples of Phi_d tested: %d, violations %d' % (nmult, viol))

# pattern table Sig[pattern, c]
Ss = [signs(p) for p in sides]
Npat = 2 ** sum(sides)
maxpat = 3000


def sigma_rows(idx):
    multi = np.unravel_index(idx, [2 ** p for p in sides])
    out = np.ones((len(idx), m), dtype=np.int64)
    for i in range(k):
        out *= Ss[i][multi[i]][:, cell[:, i]]
    return out


def subgroup_coset(r, a):
    return [(a + t * (n // r)) % n for t in range(r)]


def make_B(kind):
    B = np.zeros(n, dtype=np.int64)
    if kind == 0:
        dens = random.choice([.05, .2, .5, .8])
        B = (np.random.random(n) < dens).astype(np.int64)
    elif kind == 1:
        for _ in range(random.randint(1, 2 * n)):
            B[random.randrange(n)] += 1
    elif kind == 2:  # union of cosets of prime-order subgroups (+ a few points changed)
        for _ in range(random.randint(1, 6)):
            r = random.choice([d for d in divisors(n) if d > 1])
            for x in subgroup_coset(r, random.randrange(n)):
                B[x] = 1
        for _ in range(random.choice([0, 0, 1, 2])):
            B[random.randrange(n)] ^= 1
    elif kind == 3:  # classes modulo a divisor
        d = random.choice([d for d in divisors(n) if 1 < d < n])
        for cl in random.sample(range(d), random.randint(1, d - 1)):
            B[cl::d] = 1
    elif kind == 4:  # all N(c) even: two points in one cell, or doubled set
        if n > m and random.random() < .5:
            c = random.randrange(m)
            x, y = random.sample(range(c, n, m), 2)
            B[x] = 1
            B[y] = 1
        else:
            B = 2 * (np.random.random(n) < .1).astype(np.int64)
            B[random.randrange(n)] += 2
    elif kind == 5:  # product set in the digits of n
        ok = np.ones(n, dtype=bool)
        for p, a in factorint(n).items():
            keep = random.sample(range(p), random.randint(1, p))
            ok &= np.isin(np.arange(n) % p, keep)
        B = ok.astype(np.int64)
    if not B.any():
        B[random.randrange(n)] = 1
    return B


zero_events = 0
tested_pat = 0
good_box_total = 0
sets_done = 0
fail_exist = 0
minfrac = None
for it in range(nsets):
    if time.time() - t0 > 80:
        break
    B = make_B(it % 6)
    N = np.zeros(m, dtype=np.int64)
    for x in range(n):
        N[x % m] += B[x]
    if (N % 2).any():
        gcell = N % 2
    else:
        c0 = random.choice([c for c in range(m) if N[c] >= 2])
        gcell = np.zeros(m, dtype=np.int64)
        gcell[c0] = 2
    assert (gcell % q if q else gcell).any()
    g = np.zeros(sides, dtype=np.int64)
    for c in range(m):
        g[tuple(cell[c])] = gcell[c]
    res, per = good_table(g % q if q else g, sides, q, TL)
    frac = res.sum() / Npat
    if minfrac is None or frac < minfrac:
        minfrac = frac
    if not res.any():
        fail_exist += 1
        print('NO good pattern for a set (Theorem P\' would be refuted if c(m) > 0)')
    # base signing with cell sums gcell: random arrangement of signs inside each cell
    Sbase = np.zeros(n, dtype=np.int64)
    for c in range(m):
        elems = [x for x in range(c, n, m) for _ in range(int(B[x]))]
        random.shuffle(elems)
        tgt = int(gcell[c])
        assert (len(elems) - tgt) % 2 == 0 and tgt <= len(elems)
        sg = [1] * tgt + [1, -1] * ((len(elems) - tgt) // 2)
        for x, s_ in zip(elems, sg):
            Sbase[x] += s_
    assert (np.abs(Sbase) <= B).all() and ((Sbase - B) % 2 == 0).all()
    # patterns: all if few, else a sample that contains good and bad ones
    if Npat <= maxpat:
        idx = np.arange(Npat)
    else:
        flat = res.reshape(-1)
        gi = np.nonzero(flat)[0]
        bi = np.nonzero(~flat)[0]
        idx = np.concatenate([np.random.choice(gi, min(len(gi), maxpat // 2), replace=False) if len(gi) else gi,
                              np.random.choice(bi, min(len(bi), maxpat // 2), replace=False) if len(bi) else bi])
    Sig = sigma_rows(idx)
    Smat = Sig[:, np.arange(n) % m] * Sbase[None, :]
    # legal signing: |S(x)| <= B(x), parity; fold = sigma g
    fold = np.zeros((len(idx), m), dtype=np.int64)
    for r in range(n // m):
        fold += Smat[:, r * m:(r + 1) * m]
    assert (fold == Sig * gcell[None, :]).all()
    boxgood = res.reshape(-1)[idx]
    good_box_total += int(boxgood.sum())
    tested_pat += len(idx)
    anyzero = np.zeros(len(idx), dtype=bool)
    for d in divisors(n):
        z = divisible(Smat, d)
        if not z.any():
            continue
        zero_events += int(z.sum())
        anyzero |= z
        dprime = d
        if q:
            while dprime % q == 0:
                dprime //= q
        lev = per[tree[dprime]].reshape(-1)[idx]
        if (z & lev).any():
            print('VIOLATION: Phi_%d | S although the box is good mod q at the tree level of %d' % (d, dprime), B.tolist())
    if (anyzero & boxgood).any():
        print('VIOLATION: good in the box but zero at a root of unity', B.tolist())
    sets_done += 1
print('  sets %d, (set, pattern) pairs tested %d, of which good in the box %d; events Phi_d | S seen: %d; '
      'sets with no good pattern: %d; least fraction of good patterns %.4f; time %.1fs'
      % (sets_done, tested_pat, good_box_total, zero_events, fail_exist, minfrac, time.time() - t0))
