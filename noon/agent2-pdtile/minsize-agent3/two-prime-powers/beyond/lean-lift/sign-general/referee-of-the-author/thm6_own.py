"""Referee's end-to-end test of Theorem 6 of sign-general-result.md on cyclic groups, written from the text of its proof.

n = m q^b (or n = m with F = Q).  For a multiset B on Z_n:
  N(c) = number of elements = c (mod m);  g = indicator of {c : N(c) odd}, or 2 delta_{c0} if every N(c) is even;
  g is read on the digit box of m (one coordinate of size p for every pair (p, e), dig_{p,e}(c) = floor((c mod p^e)/p^(e-1)));
  a product pattern sigma on the digit box with sigma*g good over F at every tree level (or at every level);
  the elements of the cell c get signs summing to sigma(c) g(c);
  claim: the signed mask is divisible by no Phi_d, d | n.   Tested by exact long division by Phi_d for every d | n.
Also: the share of patterns that are good in the box against the bound (2^-k, or c(m)), by full enumeration on small
boxes and by sampling on larger ones; and Lemma G (the digit cubes are primitive and <h, T> is the cube sum).

usage: thm6_own.py n m q COUNT SEED [tree|all] [exh|sample]
       thm6_own.py lemmaG SEED
"""
import sys, time
import numpy as np
from fractions import Fraction as Fr
from itertools import product, combinations
from math import gcd
from boxtools import all_levels, pattern_array, good_batch

# ---------- exact polynomial arithmetic (numpy int64, guarded) ----------
def rem_monic(f, phi):
    """remainder of f modulo the monic phi; integer arrays, lowest coefficient first."""
    f = np.array(f, dtype=np.int64); dg = len(phi) - 1
    assert phi[-1] == 1
    for i in range(len(f) - 1, dg - 1, -1):
        c = f[i]
        if c:
            f[i - dg:i + 1] -= c * phi
    assert np.abs(f).max(initial=0) < 2 ** 40
    return f[:dg]

def quo_exact(f, phi):
    f = np.array(f, dtype=np.int64); dg = len(phi) - 1; q = np.zeros(len(f) - dg, dtype=np.int64)
    for i in range(len(f) - 1, dg - 1, -1):
        c = f[i]
        if c:
            q[i - dg] = c
            f[i - dg:i + 1] -= c * phi
    assert not f.any()
    return q

_cyc = {}
def cyclotomic(n):
    if n in _cyc: return _cyc[n]
    num = np.zeros(n + 1, dtype=np.int64); num[0] = -1; num[n] = 1
    for d in range(1, n):
        if n % d == 0:
            num = quo_exact(num, cyclotomic(d))
    _cyc[n] = num
    return num

def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]

def cyc_divisors(S, n, divs):
    """S: dict exponent -> integer coefficient (a polynomial modulo X^n - 1).  The d | n with Phi_d | S."""
    res = []
    for d in divs:
        f = np.zeros(d, dtype=np.int64)
        for x, c in S.items(): f[x % d] += c
        if not rem_monic(f, cyclotomic(d)).any(): res.append(d)
    return res

def factor(n):
    f = {}; d = 2
    while d * d <= n:
        while n % d == 0: f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

# ---------- the digit box ----------
def digit_box(m):
    fm = factor(m)
    coords = [(p, e) for p in sorted(fm) for e in range(1, fm[p] + 1)]
    sides = tuple(p for p, _ in coords)
    digs = np.array([[(c % p ** e) // p ** (e - 1) for (p, e) in coords] for c in range(m)], dtype=np.int64).reshape(m, len(coords))
    assert len({tuple(r) for r in digs}) == m                      # a bijection onto the box
    return coords, sides, digs

def tree_levels(coords):
    k = len(coords)
    return [P for P in all_levels(k) if len({coords[i][0] for i in P}) == len(P)]

def c_bound(m):
    from coverage_own import c_rec, factor as f2
    return c_rec(tuple(sorted(f2(m).items())))

# ---------- sets ----------
def make_multiset(rng, n, m, q, kind):
    divs = [d for d in divisors(n) if 1 < d < n]
    B = {}
    def add(x, k=1):
        B[x % n] = B.get(x % n, 0) + k
    def coset(d, x0):
        return {(x0 + d * j) % n for j in range(n // d)}
    if kind == 'cosets':            # union of cosets of subgroups, a few points changed
        S = set()
        for _ in range(rng.integers(1, 4)):
            S |= coset(int(rng.choice(divs)), int(rng.integers(0, n)))
        for _ in range(rng.integers(0, 4)):
            S ^= {int(rng.integers(0, n))}
        for x in S: add(x)
    elif kind == 'cosets_pure':     # union of cosets, nothing changed
        S = set()
        for _ in range(rng.integers(1, 4)):
            S |= coset(int(rng.choice(divs)), int(rng.integers(0, n)))
        for x in S: add(x)
    elif kind == 'sumset':          # A + H, H a subgroup, A a few points
        H = coset(int(rng.choice(divs)), 0); A = {int(rng.integers(0, n)) for _ in range(rng.integers(1, 4))}
        for x in {(a + h) % n for a in A for h in H}: add(x)
    elif kind == 'random':
        for x in range(n):
            if rng.random() < 0.3: add(x)
    elif kind == 'few':
        for _ in range(rng.integers(1, 7)): add(int(rng.integers(0, n)))
    elif kind == 'multiset':        # random multiplicities on a union of cosets
        S = set()
        for _ in range(rng.integers(1, 3)):
            S |= coset(int(rng.choice(divs)), int(rng.integers(0, n)))
        for x in S: add(x, int(rng.integers(1, 4)))
    elif kind == 'all_even':        # every cell count even: g = 2 delta
        S = set()
        for _ in range(rng.integers(1, 3)):
            S |= coset(int(rng.choice(divs)), int(rng.integers(0, n)))
        for x in S: add(x, 2)
    elif kind == 'one_cell':        # points in one cell modulo m (needs n > m): a coset of the subgroup of order n/m, or part of it
        x0 = int(rng.integers(0, n)); pts = [(x0 + m * j) % n for j in range(n // m)]
        take = rng.integers(1, len(pts) + 1)
        for x in rng.permutation(pts)[:take]: add(int(x))
    elif kind == 'whole':
        for x in range(n): add(x)
    if not B: add(0)
    return B

KINDS = ['cosets', 'cosets_pure', 'sumset', 'random', 'few', 'multiset', 'all_even', 'one_cell', 'whole']

def signing(B, n, m, target):
    """signs so that the elements of the cell c sum to target[c]; returns S: dict x -> signed coefficient."""
    cells = {}
    for x in sorted(B):
        cells.setdefault(x % m, []).extend([x] * B[x])
    S = {}
    for c, elems in cells.items():
        t = int(target[c]); N = len(elems)
        assert abs(t) <= N and (N - t) % 2 == 0
        sgn = 1 if t >= 0 else -1
        for i, x in enumerate(elems):
            s = sgn if i < abs(t) else (1 if (i - abs(t)) % 2 == 0 else -1)
            S[x] = S.get(x, 0) + s
    return S

def run(n, m, q, count, seed, levelkind, mode):
    rng = np.random.default_rng(seed)
    assert n % m == 0
    if q:
        b = 0; t = n // m
        while t % q == 0: t //= q; b += 1
        assert t == 1 and m % q and q % 2 == 1 and all(q % d for d in range(2, int(q ** 0.5) + 1)), 'n must be m q^b, q an odd prime not dividing m'
    else:
        assert n == m
    coords, sides, digs = digit_box(m); k = len(coords)
    levels = tree_levels(coords) if levelkind == 'tree' else all_levels(k)
    divs = divisors(n)
    for d in divs: cyclotomic(d)
    if levelkind == 'all':
        srt = sorted(sides); ok_hyp = all(s >= max(3, 2 * (j + 1)) for j, s in enumerate(srt))
        bound = Fr(1, 2 ** k) if ok_hyp else None
    else:
        cb = c_bound(m); bound = cb if cb > 0 else None
    idx = tuple(digs[:, j] for j in range(k))
    if mode == 'exh':
        PA, _ = pattern_array(sides); PA = PA.astype(np.int64)
    t0 = time.time()
    tot = {'sets': 0, 'allplus_bad': 0, 'tries': 0, 'maxtries': 0, 'good_box': 0, 'verified': 0, 'chain_viol': 0, 'badbox_tested': 0,
           'badbox_but_good': 0, 'equiv_viol': 0, 'g2': 0, 'multi': 0}
    least_share = None
    for it in range(count):
        kind = KINDS[it % len(KINDS)]
        if kind == 'one_cell' and n == m: kind = 'cosets'
        B = make_multiset(rng, n, m, q, kind)
        tot['sets'] += 1
        if max(B.values()) > 1: tot['multi'] += 1
        if cyc_divisors(B, n, divs): tot['allplus_bad'] += 1
        Nc = np.zeros(m, dtype=np.int64)
        for x, c in B.items(): Nc[x % m] += c
        if (Nc % 2).any():
            g = (Nc % 2).astype(np.int64)
        else:
            c0 = int(np.nonzero(Nc >= 2)[0][0]); g = np.zeros(m, dtype=np.int64); g[c0] = 2; tot['g2'] += 1
        gbox = np.zeros(sides, dtype=np.int64); gbox[idx] = g
        assert (gbox % q if q else gbox).any()
        if mode == 'exh':
            okv = good_batch(PA * gbox[None], levels, q if q else None)
            share = Fr(int(okv.sum()), PA.shape[0])
            least_share = share if least_share is None else min(least_share, share)
            if bound is not None: assert share >= bound, ('share of good patterns below the bound', n, m, q, B, share, bound)
        # random patterns: until one is good in the box; each one tried is carried through to the division
        found = False; tries = 0
        while not found and tries < 400:
            tries += 1
            sig = [rng.choice([1, -1], size=s) for s in sides]
            sgm = np.ones(m, dtype=np.int64)
            for j in range(k): sgm = sgm * sig[j][digs[:, j]]
            sbox = np.zeros(sides, dtype=np.int64); sbox[idx] = sgm * g
            good_in_box = bool(good_batch(sbox[None], levels, q if q else None)[0])
            S = signing(B, n, m, sgm * g)
            fold = np.zeros(m, dtype=np.int64)
            for x, c in S.items(): fold[x % m] += c
            assert (fold == sgm * g).all()                              # the fold of the signed mask to Z_m is sigma*g
            for x, c in S.items(): assert abs(c) <= B[x] and (c - B[x]) % 2 == 0     # a signing of B
            bad_d = cyc_divisors(S, n, divs)
            if good_in_box:
                tot['good_box'] += 1
                if bad_d: tot['chain_viol'] += 1; print('CHAIN VIOLATION', n, m, q, sorted(B.items()), [s.tolist() for s in sig], bad_d)
                else: tot['verified'] += 1
                found = True
            else:
                tot['badbox_tested'] += 1
                if not bad_d: tot['badbox_but_good'] += 1
                if not q and all(e == 1 for e in factor(n).values()) and not bad_d:
                    tot['equiv_viol'] += 1          # squarefree n over Q: bad in the box should mean a cyclotomic divisor
        assert found
        tot['tries'] += tries; tot['maxtries'] = max(tot['maxtries'], tries)
    fm = factor(m)
    print(f'n = {n} = {m} * {q}^b' if q else f'n = m = {n}', f'(m = {fm}, digit box {sides}, {levelkind} levels: {len(levels)}, field {"F_%d" % q if q else "Q"}):')
    print(f'   {tot["sets"]} multisets ({tot["multi"]} with a repeated element, {tot["g2"]} with every cell count even); all + has a cyclotomic divisor for {tot["allplus_bad"]};')
    print(f'   a pattern good in the box was found for every one, after {tot["tries"] / tot["sets"]:.2f} random patterns on average, at most {tot["maxtries"]};')
    print(f'   signings from patterns good in the box: {tot["good_box"]}, of which divisible by no Phi_d, d | n (exact division, {len(divs)} divisors): {tot["verified"]}; violations of the chain: {tot["chain_viol"]};')
    print(f'   patterns not good in the box carried through as well: {tot["badbox_tested"]}, of which the signing was good all the same: {tot["badbox_but_good"]}'
          + (f' (squarefree n over Q, where bad in the box must give a divisor: {tot["equiv_viol"]} exceptions)' if not q and all(e == 1 for e in fm.values()) else ''))
    if mode == 'exh':
        print(f'   share of patterns good in the box, all {PA.shape[0]} normalised patterns for every multiset: least {least_share}; bound of the text: {bound}')
    print(f'   [{time.time() - t0:.0f} s]')

def lemmaG(seed):
    rng = np.random.default_rng(seed); nchk = 0
    for m in [9, 15, 27, 45, 75, 105, 135, 225, 315, 675, 1575]:
        coords, sides, digs = digit_box(m); k = len(coords)
        fm = factor(m)
        for _ in range(40):
            # a divisor d' and its tree level
            ip = {p: int(rng.integers(0, fm[p] + 1)) for p in fm}
            dp = 1
            for p, i in ip.items(): dp *= p ** i
            Qs = [p for p in fm if ip[p] >= 1]
            cube = {}
            for p in Qs:
                a, a2 = rng.choice(p, size=2, replace=False); cube[p] = (int(a), int(a2))
            h = np.ones(dp, dtype=np.int64)
            for y in range(dp):
                v = 1
                for p in Qs:
                    dg = (y % p ** ip[p]) // p ** (ip[p] - 1)
                    v *= (1 if dg == cube[p][0] else 0) - (1 if dg == cube[p][1] else 0)
                h[y] = v
            # primitive: sums to 0 over every coset of the subgroup of order p, every prime p | d'
            for p in Qs:
                step = dp // p
                for y in range(step):
                    assert sum(int(h[(y + t * step) % dp]) for t in range(p)) == 0
            # <h, T> against the cube sum of T on the digit box of m
            T = rng.integers(-3, 4, size=m)
            fold = np.zeros(dp, dtype=np.int64)
            for x in range(m): fold[x % dp] += T[x]
            lhs = int((h * fold).sum())
            rhs = 0
            for x in range(m):
                v = 1
                for p in Qs:
                    j = coords.index((p, ip[p])); dg = int(digs[x, j])
                    v *= (1 if dg == cube[p][0] else 0) - (1 if dg == cube[p][1] else 0)
                rhs += v * int(T[x])
            assert lhs == rhs
            nchk += 1
    print(f'Lemma G: {nchk} random (m, d\', cube, T) with m in 9, 15, 27, 45, 75, 105, 135, 225, 315, 675, 1575: h is primitive on Z_d\' and <h, T> is the cube sum: no exception')
    # the division routine against a second method: Phi_d | T  iff  T * Psi_d = 0 modulo X^d - 1, Psi_d = (X^d - 1)/Phi_d
    nchk = 0
    for d in [15, 21, 45, 105, 165, 315]:
        phi = cyclotomic(d); num = np.zeros(d + 1, dtype=np.int64); num[0] = -1; num[d] = 1
        psi = quo_exact(num, phi)
        for _ in range(60):
            if rng.random() < 0.5:
                T = rng.integers(-2, 3, size=d)
            else:       # a multiple of Phi_d, folded
                A = rng.integers(-2, 3, size=d - len(phi) + 1); full = np.convolve(A, phi); T = full[:d].copy()
                if rng.random() < 0.3: T[rng.integers(0, d)] += 1
            r1 = not rem_monic(T, phi).any()
            conv = np.convolve(T, psi); fold = np.zeros(d, dtype=np.int64)
            for i, c in enumerate(conv): fold[i % d] += c
            r2 = not fold.any()
            assert r1 == r2; nchk += 1
    print(f'long division by Phi_d against the test T * (X^d - 1)/Phi_d = 0 mod X^d - 1: {nchk} polynomials, no difference')

if __name__ == '__main__':
    if sys.argv[1] == 'lemmaG':
        lemmaG(int(sys.argv[2]))
    else:
        n, m, q, count, seed = (int(a) for a in sys.argv[1:6])
        levelkind = sys.argv[6] if len(sys.argv) > 6 else 'tree'
        mode = sys.argv[7] if len(sys.argv) > 7 else 'sample'
        run(n, m, q, count, seed, levelkind, mode)
