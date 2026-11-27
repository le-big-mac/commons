"""Referee, third pass: Theorem 7 of sign-all-result.md end to end on cyclic groups, from the text of its proof.

n = m q^b (or n = m, q = 0).  For a multiset B on Z_n:  N(c) = number of elements = c (mod m);  g = indicator of the odd
cells, or 2 delta_{c0};  g is read on the TREE box of m (coordinates c mod p^a for p^a || m);  a pattern sigma = one
arbitrary sign vector on each Z_{p^a};  sigma*g good on the tree box over F_q (over Q if n = m) at every level;  the
elements of the cell c get signs summing to sigma(c) g(c);  claim: no Phi_d, d | n, divides the signed mask.

Division.  Phi_d(X) = Phi_r(X^(d/r)), r = rad(d); a polynomial f of degree < d is divisible by Phi_r(X^k) iff each of the
k polynomials f_t (the coefficients of f at the exponents = t mod k, read as a polynomial in X^k) is divisible by Phi_r.
Each f_t is divided by Phi_r by exact long division.  For n up to 11025 this is compared with the plain long division
by Phi_d of the first pass (thm6_own.cyc_divisors).

Also Lemma G' (sibling cube functions are primitive on Z_d', and <h, T> is the cube sum).
usage: thm7_own.py n m q COUNT SEED          thm7_own.py lemmaG SEED
"""
import sys, time
import numpy as np
from fractions import Fraction as Fr
sys.path.insert(0, '/home/agent3/paper/referee-signs')
from thm6_own import cyc_divisors as cyc_divisors_plain, cyclotomic, divisors, signing, make_multiset, factor, KINDS
from treetools import TreeBox, level_matrix
_argv = sys.argv; sys.argv = [_argv[0]]
from coverage3_own import gamma
sys.argv = _argv

def rad(d):
    r = 1
    for p in factor(d): r *= p
    return r

def cyc_divisors_fast(S, n, divs):
    res = []
    xs = np.array(list(S.keys()), dtype=np.int64); cs = np.array(list(S.values()), dtype=np.int64)
    for d in divs:
        r = rad(d); k = d // r; phi = cyclotomic(r); dg = len(phi) - 1
        F = np.zeros((k, r), dtype=np.int64)
        e = xs % d
        np.add.at(F, (e % k, e // k), cs)
        for i in range(r - 1, dg - 1, -1):
            col = F[:, i].copy()
            if col.any():
                F[:, i - dg:i + 1] -= col[:, None] * phi[None, :]
        assert np.abs(F).max(initial=0) < 2 ** 40
        if not F[:, :dg].any(): res.append(d)
    return res

def run(n, m, q, count, seed):
    rng = np.random.default_rng(seed)
    assert n % m == 0
    if q:
        t = n // m
        while t % q == 0: t //= q
        assert t == 1 and m % q and q % 2 == 1 and all(q % d for d in range(2, int(q ** 0.5) + 1))
    else: assert n == m
    fm = factor(m); trees = [(p, fm[p]) for p in sorted(fm)]
    tb = TreeBox(trees); k = len(trees)
    coords = [np.arange(m) % (p ** a) for (p, a) in trees]
    assert len(set(zip(*[c.tolist() for c in coords]))) == m          # Z_m -> tree box is a bijection
    divs = divisors(n)
    G = gamma(tuple(trees))
    compare = n <= 12000
    t0 = time.time()
    tot = dict(sets=0, allplus=0, tries=0, maxtries=0, goodbox=0, verified=0, viol=0, bad_tested=0, bad_but_good=0, g2=0, multi=0, sample_good=0, sample_n=0, cmp=0)
    for it in range(count):
        kind = KINDS[it % len(KINDS)]
        if kind == 'one_cell' and n == m: kind = 'cosets'
        B = make_multiset(rng, n, m, q, kind)
        tot['sets'] += 1
        if max(B.values()) > 1: tot['multi'] += 1
        d0 = cyc_divisors_fast(B, n, divs)
        if compare: assert d0 == cyc_divisors_plain(B, n, divs); tot['cmp'] += 1
        if d0: tot['allplus'] += 1
        Nc = np.zeros(m, dtype=np.int64)
        for x, c in B.items(): Nc[x % m] += c
        if (Nc % 2).any(): g = (Nc % 2).astype(np.int64)
        else:
            c0 = int(np.nonzero(Nc >= 2)[0][0]); g = np.zeros(m, dtype=np.int64); g[c0] = 2; tot['g2'] += 1
        assert (g % q if q else g).any()
        found = False; tries = 0
        while not found and tries < 400:
            tries += 1
            sig = [rng.choice([1, -1], size=s) for s in tb.sides]
            sgm = np.ones(m, dtype=np.int64)
            for j in range(k): sgm = sgm * sig[j][coords[j]]
            box = np.zeros(tb.sides, dtype=np.int64); box[tuple(coords)] = sgm * g
            good_in_box = bool(tb.good(box[None], q if q else None)[0])
            tot['sample_n'] += 1; tot['sample_good'] += int(good_in_box)
            S = signing(B, n, m, sgm * g)
            fold = np.zeros(m, dtype=np.int64)
            for x, c in S.items(): fold[x % m] += c
            assert (fold == sgm * g).all()
            for x, c in S.items(): assert abs(c) <= B[x] and (c - B[x]) % 2 == 0
            bad = cyc_divisors_fast(S, n, divs)
            if compare: assert bad == cyc_divisors_plain(S, n, divs); tot['cmp'] += 1
            if good_in_box:
                tot['goodbox'] += 1
                if bad: tot['viol'] += 1; print('CHAIN VIOLATION', n, m, q, sorted(B.items()), [s.tolist() for s in sig], bad)
                else: tot['verified'] += 1
                found = True
            else:
                tot['bad_tested'] += 1
                if not bad: tot['bad_but_good'] += 1
        assert found
        tot['tries'] += tries; tot['maxtries'] = max(tot['maxtries'], tries)
    print((f'n = {n} = {m} * {q}^b' if q else f'n = m = {n}') + f' (trees {trees}, {len(tb.levels)} levels, field {"F_%d" % q if q else "Q"}; Gamma(m) = {G}' + (' : Theorem 7 does not apply, only the chain is tested' if G <= 0 else '') + '):')
    print(f'   {tot["sets"]} multisets ({tot["multi"]} with a repeated element, {tot["g2"]} with every cell even); all + has a cyclotomic divisor for {tot["allplus"]}; '
          f'a pattern good in the tree box found for each, after {tot["tries"] / tot["sets"]:.2f} random patterns on average, at most {tot["maxtries"]} '
          f'(share of good among all random patterns tried: {tot["sample_good"]}/{tot["sample_n"]});')
    print(f'   signings from patterns good in the tree box: {tot["goodbox"]}; divisible by no Phi_d, d | n ({len(divs)} divisors): {tot["verified"]}; violations: {tot["viol"]}; '
          f'patterns not good in the box carried through: {tot["bad_tested"]}, signing good all the same: {tot["bad_but_good"]}; '
          f'the two division routines compared on {tot["cmp"]} polynomials' + ('' if compare else ' (n too large for the plain one)') + f'  [{time.time() - t0:.0f} s]', flush=True)

def lemmaG(seed):
    rng = np.random.default_rng(seed); n = 0
    for m in [9, 27, 45, 75, 225, 675, 189, 1575, 4375, 6125]:
        fm = factor(m); trees = [(p, fm[p]) for p in sorted(fm)]
        for _ in range(40):
            ip = {p: int(rng.integers(0, fm[p] + 1)) for p in fm}
            dp = 1
            for p, i in ip.items(): dp *= p ** i
            cube = {}
            for p, i in ip.items():
                if i == 0: continue
                grp = int(rng.integers(0, p ** (i - 1))); t1, t2 = rng.choice(p, size=2, replace=False)
                cube[p] = (grp + int(t1) * p ** (i - 1), grp + int(t2) * p ** (i - 1))      # u, u' modulo p^i, equal modulo p^(i-1)
            y = np.arange(dp); h = np.ones(dp, dtype=np.int64)
            for p, (u, u2) in cube.items():
                h = h * ((y % p ** ip[p] == u).astype(np.int64) - (y % p ** ip[p] == u2).astype(np.int64))
            for p in cube:                       # primitive: sum 0 over every coset of the subgroup of order p of Z_d'
                step = dp // p
                assert not h.reshape(p, step).sum(axis=0).any()
            T = rng.integers(-3, 4, size=m)
            lhs = int((h * np.bincount(np.arange(m) % dp, weights=T, minlength=dp).astype(np.int64)).sum())
            x = np.arange(m); w = np.ones(m, dtype=np.int64)
            for p, (u, u2) in cube.items():      # on the tree box: the coordinate is x mod p^a, the classes are residues modulo p^i
                xa = x % p ** fm[p]
                w = w * ((xa % p ** ip[p] == u).astype(np.int64) - (xa % p ** ip[p] == u2).astype(np.int64))
            assert lhs == int((w * T).sum())
            n += 1
    print(f"Lemma G': {n} random (m, d', sibling cube, T), m in 9, 27, 45, 75, 225, 675, 189, 1575, 4375, 6125: h is primitive on Z_d' and <h, T> is the cube sum on the tree box: no exception")

if __name__ == '__main__':
    if sys.argv[1] == 'lemmaG': lemmaG(int(sys.argv[2]))
    else:
        n, m, q, count, seed = (int(a) for a in sys.argv[1:6])
        run(n, m, q, count, seed)
