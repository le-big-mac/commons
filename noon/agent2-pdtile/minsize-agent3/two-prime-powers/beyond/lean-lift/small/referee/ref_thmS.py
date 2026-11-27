"""Referee's tests of Theorem S of small-multisets.md on groups Z_n with n far above anything covered before.

For each multiset B of 5..14 elements on Z_n:
  1. the divisors d | n with Phi_d | (mask with all signs +) are listed (so that one sees the case is not empty);
  2. a good signing is searched: random signings first (the first element keeps +), then, if 300 random ones fail, all
     2^(m-1) signings.  Theorem S says there is one; a failure of the full search would be a counterexample;
  3. the signing found is confirmed by exact long division: for every d | n one class polynomial of the split
     S = sum_c X^c f_c(X^(d/rad d)) is divided by Phi_rad(d) and leaves a nonzero remainder (see refbig.py);
     also the least |S(zeta_d)| over d | n in floating point is printed;
  4. the route of the note: B is contracted as far as it goes (Proposition 3) to B-flat on Z_nflat; nflat must divide
     n'_m; every signing of B-flat that is good (all 2^(m-1) of them if m <= MAXALL, else the first good one found)
     is tested on B, where it must be good.
usage: ref_thmS.py GROUP KIND SEED COUNT [nold] [MMIN MMAX]      (sizes 5..14 unless MMIN MMAX are given)
  GROUP: A = 3^6 5^4 7^3 11^2 13;  B = 3^4 5^3 7^2 37 41;  C = 3^5 5^2 37^2 101;  D = 3^3 5^2 7 11 13 17;
         E = 3^7 5^3 7^2 11 13 (= 3 n'_13);  G = 3^6 5^11 7^6 11^2 13;  H = 3^13 5^23 7^5;  I = 3^9 5^12 7^7 11^3 13^2;
         J = 3^14 5^24 7^6 43^2 47
  KIND: random | pool | fibres | subgroup | product | caterpillar | lift
        (lift: a multiset on a small group with few good signings, found by search, is lifted to Z_n by inserting
         digits, none of them equal to p - 1, so that every inserted level is contractible)
  nold: confirm with Psi instead of long division
"""
import sys, random, math, time
from itertools import product
import numpy as np
from reflib import factor, crt, contract, contractible
from refbig import Tester

GROUPS = {'A': {3: 6, 5: 4, 7: 3, 11: 2, 13: 1}, 'B': {3: 4, 5: 3, 7: 2, 37: 1, 41: 1}, 'C': {3: 5, 5: 2, 37: 2, 101: 1},
          'D': {3: 3, 5: 2, 7: 1, 11: 1, 13: 1, 17: 1}, 'E': {3: 7, 5: 3, 7: 2, 11: 1, 13: 1},
          'G': {3: 6, 5: 11, 7: 6, 11: 2, 13: 1},          # 6587407633447265625, the least n covered by none of Theorems 2, 3, 6, 7
          'H': {3: 13, 5: 23, 7: 5},                       # the least n with three primes covered by none of them
          'I': {3: 9, 5: 12, 7: 7, 11: 3, 13: 2},          # a multiple of G's n
          'J': {3: 14, 5: 24, 7: 6, 43: 2, 47: 1}}         # H's shape times primes above 36
MAXALL = 10
MMIN, MMAX = 5, 14          # sizes of the multisets; changed by the optional arguments MMIN MMAX


def nprime(m):
    out = 1
    for p in range(3, m + 1):
        if all(p % d for d in range(2, int(p ** 0.5) + 1)):
            out *= p ** ((m - 1) // (p - 1))
    return out


def fstr(f):
    return ' * '.join(f'{p}^{a}' if a > 1 else f'{p}' for p, a in sorted(f.items())) if f else '1'


def full_contract(el, n):
    steps = []
    while True:
        f = factor(n)
        cand = [(p, t) for p in sorted(f) for t in range(1, f[p] + 1) if contractible(el, p, f[p], t)]
        if not cand:
            return el, n, steps
        p, t = cand[0]
        el = contract(el, n, p, f[p], t); n //= p
        steps.append((p, t))


def from_coords(coords, f):
    """coords: dict prime -> residue modulo p^a."""
    x = 0; mod = 1
    for p, a in f.items():
        x = crt(x, mod, coords[p] % p ** a, p ** a); mod *= p ** a
    return x


def caterpillar_residues(p, a, m, rng):
    """m residues modulo p^a whose tree has a full group at as many levels as m allows (depth floor((m-1)/(p-1)))."""
    res = [0]
    for i in range(a):
        if len(res) + (p - 1) <= m:
            res += [j * p ** i for j in range(1, p)]
    while len(res) < m:
        res.append(rng.choice(res))
    c = rng.randrange(p ** a); u = rng.randrange(1, p)
    res = [(c + u * x) % p ** a for x in res]
    rng.shuffle(res)
    return res


def make(kind, f, n, rng):
    ps = sorted(f)
    m = rng.randint(MMIN, MMAX)
    if kind == 'random':
        return [rng.randrange(n) for _ in range(m)]
    if kind == 'pool':
        pool = [rng.randrange(n) for _ in range(rng.randint(2, 5))]
        el = [rng.choice(pool) for _ in range(m)]
        return el
    if kind == 'fibres':                       # whole groups: c + j * q^i * (n / q^a), j = 0..q-1, small primes q
        el = []
        same = rng.random() < 0.5
        small = [q for q in ps if q <= 13]
        q = rng.choice(small); i = rng.randrange(f[q])
        while len(el) < m:
            if not same:
                q = rng.choice(small); i = rng.randrange(f[q])
            c = rng.randrange(n) if (not el or rng.random() < 0.5) else rng.choice(el) + rng.choice(ps) ** rng.randrange(3) * rng.randrange(1, 5)
            if len(el) + q <= m:
                el += [(c + q ** i * (n // q ** f[q]) * j) % n for j in range(q)]
            else:
                el.append(rng.choice(el) if el and rng.random() < 0.3 else rng.randrange(n))
        return el
    if kind == 'subgroup':                     # B = k * B0 with B0 on a small group Z_N0, N0 | n: cosets inside it
        cands = [N0 for N0 in (45, 105, 135, 225, 315, 525, 675, 945, 1575) if n % N0 == 0]
        N0 = rng.choice(cands); k = n // N0; f0 = factor(N0)
        el0 = []
        while len(el0) < m:
            q = rng.choice(list(f0)); c = rng.randrange(N0)
            if len(el0) + q <= m and rng.random() < 0.85:
                el0 += [(c + (N0 // q) * j) % N0 for j in range(q)]
            else:
                el0.append(rng.choice(el0) if el0 and rng.random() < 0.3 else rng.randrange(N0))
        shift = rng.randrange(n)
        return [(shift + k * x) % n for x in el0]
    if kind == 'product' and MMAX > 14:        # (sizes above 14) sum set of two or three fibres, size at most MMAX
        small = [q for q in ps if q <= 11]
        while True:
            k = rng.choice((2, 2, 3))
            fac = [(q, rng.randrange(f[q])) for q in (rng.choice(small) for _ in range(k))]
            size = math.prod(q for q, _ in fac)
            if len(set(fac)) == k and MMIN <= size <= MMAX:
                break
        el = [rng.randrange(n)]
        for q, i in fac:
            el = [(x + q ** i * (n // q ** f[q]) * j) % n for x in el for j in range(q)]
        if rng.random() < 0.4:                  # one point moved: no longer a product
            el[rng.randrange(len(el))] = rng.randrange(n)
        return el
    if kind == 'product':                      # sum set of two or three fibres of different primes or levels: mask = product
        small = [q for q in ps if q <= 7]
        while True:
            q1 = rng.choice(small); q2 = rng.choice(small)
            i1 = rng.randrange(f[q1]); i2 = rng.randrange(f[q2])
            if (q1, i1) != (q2, i2) and q1 * q2 <= 14:
                break
        A1 = [q1 ** i1 * (n // q1 ** f[q1]) * j for j in range(q1)]
        A2 = [q2 ** i2 * (n // q2 ** f[q2]) * j for j in range(q2)]
        c = rng.randrange(n)
        el = [(c + x + y) % n for x in A1 for y in A2]
        if rng.random() < 0.5 and len(el) > 5:  # one point moved: no longer a product
            el[rng.randrange(len(el))] = rng.randrange(n)
        return el
    if kind == 'caterpillar':                  # every tree as deep as m allows; nothing (or little) can be contracted
        cols = {p: caterpillar_residues(p, f[p], m, rng) for p in ps}
        return [from_coords({p: cols[p][j] for p in ps}, f) for j in range(m)]
    if kind == 'lift':
        from reflib import good_all, divisors
        cands = [N0 for N0 in (27, 45, 135, 105, 315, 225, 675, 945, 81, 405) if n % N0 == 0]
        N0 = rng.choice(cands); f0 = factor(N0); m = rng.randint(5, 10)
        best = None
        for _ in range(150):                    # among 150: all signs + bad if possible, then the smallest share of good signings
            el0 = []
            same = rng.random() < 0.6
            q = rng.choice(list(f0)); i = rng.randrange(f0[q]); top = rng.random() < 0.5
            while len(el0) < m:
                if not same:
                    q = rng.choice(list(f0)); i = rng.randrange(f0[q]); top = rng.random() < 0.5
                c = rng.randrange(N0)
                step = N0 // q if top else q ** i * (N0 // q ** f0[q])
                if len(el0) + q <= m and rng.random() < 0.9:
                    el0 += [(c + step * j) % N0 for j in range(q)]
                else:
                    el0.append(rng.choice(el0) if el0 and rng.random() < 0.4 else rng.randrange(N0))
            g = good_all(N0, el0)
            share = g.sum() / len(g)
            key = (bool(g[0]), share)            # g[0]: all signs +
            if best is None or key < best[0]:
                best = (key, el0)
        (plus_good, share), el0 = best
        el = []
        cols = {}
        for p in ps:                            # new digits in 0..p-2 at random positions; old digits keep their order
            a = f[p]; a0 = f0.get(p, 0)
            pos_old = sorted(rng.sample(range(a), a0))
            col = []
            for x in el0:
                old_digits = [(x % p ** a0 // p ** i) % p for i in range(a0)]
                d = [rng.randrange(p - 1) for _ in range(a)]
                for i, pos in enumerate(pos_old):
                    d[pos] = old_digits[i]
                col.append(sum(v * p ** i for i, v in enumerate(d)))
            cols[p] = col
        el = [from_coords({p: cols[p][j] for p in ps}, f) for j in range(m)]
        make.info = f'lift of B0 = {el0} on Z_{N0} (share of good signings there {share:.3f})'
        return el
    raise ValueError(kind)


def rand_signs(m, rng):
    return [1] + [rng.choice((1, -1)) for _ in range(m - 1)]


def run_case(idx, kind, f, n, el, rng, do_ld):
    m = len(el)
    t0 = time.time()
    T = Tester(f, el)
    plus = [1] * m
    badplus = T.bad_divisors(plus)
    # 2. search
    found = None; tries = 0
    for _ in range(300):
        s = plus if tries == 0 else rand_signs(m, rng)
        tries += 1
        if T.good(s):
            found = s; break
    exhaustive = False
    if found is None:
        exhaustive = True
        for tail in product((1, -1), repeat=m - 1):
            s = [1] + list(tail); tries += 1
            if T.good(s):
                found = s; break
    if found is None:
        print(f'case {idx} ({kind}): m = {m}, B = {el}: NO GOOD SIGNING among all {2 ** (m - 1)} signings.  COUNTEREXAMPLE TO THEOREM S if m <= 36.')
        return dict(fail=1)
    # 3. confirmation
    if do_ld:
        nd, nld, ok = T.confirm_by_long_division(found)
        conf = f'confirmed by long division: {nd} divisors d, {nld} divisions, a nonzero remainder for every d: {ok}'
        assert ok
    else:
        nd = len(T.levels); ok = all(not T.divides(L, found, 'psi') for L in T.levels)
        conf = f'confirmed with Psi (no long division): {nd} divisors d, none divides: {ok}'
        assert ok
    num = T.numeric_min(found)
    # 4. the note's route
    fl, nf, steps = full_contract(el, n)
    ff = factor(nf)
    assert nprime(m) % nf == 0, ('nflat does not divide n\'_m', nf, m)
    Tf = Tester(ff, fl)
    route = ''
    if m <= MAXALL and (len(T.danger) + len(Tf.danger)) * 2 ** (m - 1) <= 400000:
        ngf = 0; viol = 0; conv = 0
        for tail in product((1, -1), repeat=m - 1):
            s = [1] + list(tail)
            a = Tf.good(s); b = T.good(s)
            ngf += a; viol += (a and not b); conv += (b and not a)
        route = f'all {2 ** (m - 1)} signings: good for B-flat {ngf}, of these bad for B {viol}; good for B and bad for B-flat {conv}'
        assert viol == 0, ('VIOLATION of Proposition 3', el, fl, nf)
    else:
        ngf = 0; ntested = 0
        for k in range(2000):
            s = plus if k == 0 else rand_signs(m, rng)
            ntested += 1
            if Tf.good(s):
                ngf += 1
                b = T.good(s)
                assert b, ('VIOLATION of Proposition 3', el, fl, nf, s)
                if ngf == 12: break
        assert ngf > 0
        route = f'{ntested} random signings: good for B-flat {ngf}, each of them good for B'
    print(f'case {idx} ({kind}): m = {m}, B = {el}' + (f'; {make.info}' if kind == 'lift' else ''))
    print(f'   all signs +: Phi_d divides for {len(badplus)} of {len(T.levels)} divisors d' + (f' (least d = {min(badplus)})' if badplus else '')
          + f'; divisors that can divide some signing: {len(T.danger)}')
    print(f'   good signing found at try {tries}' + (' (full search)' if exhaustive else '') + f': {"".join("+" if v > 0 else "-" for v in found)}')
    print(f'   {conf}; least |S(zeta_d)| numerically {num[0]:.6f} at d = {num[1]}')
    print(f'   contracted in {len(steps)} steps to Z_{nf} = {fstr(ff)} (divides n\'_{m}); {route}')
    print(f'   seconds {time.time() - t0:.1f}', flush=True)
    return dict(fail=0, tries=tries, badplus=bool(badplus), nf=nf, exhaustive=exhaustive)


if __name__ == '__main__':
    G, kind, seed, count = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    do_ld = 'nold' not in sys.argv[5:]
    nums = [int(a) for a in sys.argv[5:] if a.isdigit()]
    if len(nums) == 2:
        MMIN, MMAX = nums
    f = GROUPS[G]; n = math.prod(p ** a for p, a in f.items())
    rng = random.Random(seed)
    print(f'group {G}: n = {n} = {fstr(f)}; kind {kind}; seed {seed}; {count} multisets of {MMIN}..{MMAX} elements')
    res = []
    for idx in range(count):
        el = make(kind, f, n, rng)
        res.append(run_case(idx, kind, f, n, el, rng, do_ld))
    nf = sum(r['fail'] for r in res)
    ok = [r for r in res if not r['fail']]
    print(f'SUMMARY group {G} kind {kind}: {len(res)} multisets; no good signing found: {nf}; all signs + bad in {sum(r["badplus"] for r in ok)}; '
          f'largest number of tries {max(r["tries"] for r in ok)}; full search needed in {sum(r["exhaustive"] for r in ok)}; '
          f'largest contracted group order {max(r["nf"] for r in ok)}')
