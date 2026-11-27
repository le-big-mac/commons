"""End to end on large groups: multisets of m >= 37 elements (and smaller), every level of every tree with a
full group; random signings are tested exactly.

The exact test: Phi_d | S is decided by lib4.vanishes (the slice criterion, Lemma 1 of the note, prime by
prime).  To avoid running through all divisors of n (millions), levels are pruned by:

  if an element with nonzero coefficient is alone in its class modulo e = d / rad(d), then S(zeta_d) != 0

(1, z, .., z^(e-1), z = zeta_d, is a basis of Q(zeta_d) over Q(z^e), and z^e has order rad(d); the coefficient of
the class of that element is +-1 times a root of unity).  So only the e all of whose occupied classes have at
least two elements are visited (a family closed under taking divisors), and for each of them the levels
d = e * rad(e) * h, h squarefree and prime to e.  The pruning is itself tested against the unpruned test, and the
unpruned test against division by Phi_d, in mode 'selftest'.

usage: test_big.py selftest seed
       test_big.py run m shape nsets nsign seed      (shape: full | small | coset | pair | pair5 | triple | quint | interval | intervalperm)
"""
import sys
import random
import time
from fractions import Fraction as Fr
import numpy as np
from lib4 import (factor, divisors, vanishes, good_big, bad_table, all_signs, all_full, contract, crt, digits)


def odd_primes_upto(x):
    ps = []
    for k in range(3, x + 1, 2):
        if all(k % q for q in ps if q * q <= k):
            ps.append(k)
    return ps


def nprime(m):
    return {p: (m - 1) // (p - 1) for p in odd_primes_upto(m) if (m - 1) // (p - 1) >= 1}


def bad_levels_pruned(B, eps, f, first_only=True):
    """list of the d | n (n given by its factorisation f) with Phi_d | S; stops at the first if first_only"""
    primes = sorted(f)
    found = []
    visited = [0, 0]      # number of e visited, number of levels tested

    def levels_for(e_exp):
        # d = e * rad(e) * h
        base = 1
        free = []
        for p in primes:
            k = e_exp.get(p, 0)
            if k:
                if k + 1 > f[p]:
                    return
                base *= p ** (k + 1)
            else:
                free.append(p)
        for mask in range(1 << len(free)):
            d = base
            for j, p in enumerate(free):
                if mask >> j & 1:
                    d *= p
            yield d

    def test_e(e_exp):
        visited[0] += 1
        for d in levels_for(e_exp):
            visited[1] += 1
            fd = {}
            for x, s in zip(B, eps):
                y = x % d
                fd[y] = fd.get(y, 0) + s
            if vanishes(fd, d):
                found.append(d)
                if first_only:
                    return True
        return False

    def no_singleton(e):
        cnt = {}
        for x in B:
            cnt[x % e] = cnt.get(x % e, 0) + 1
        return all(v >= 2 for v in cnt.values())

    def dfs(start, e, e_exp):
        if test_e(e_exp) and first_only:
            return True
        for j in range(start, len(primes)):
            p = primes[j]
            k = e_exp.get(p, 0)
            if k + 1 > f[p] - 1:          # need v_p(d) = k + 2 <= a_p
                continue
            e2 = e * p
            if not no_singleton(e2):
                continue
            ex2 = dict(e_exp); ex2[p] = k + 1
            if dfs(j, e2, ex2) and first_only:
                return True
        return False

    if len(B) == 1:
        return [], visited
    dfs(0, 1, {})
    return found, visited


def gen_full(f, m, rng, cluster=0.4):
    cols = []
    for p, a in f.items():
        q = p ** a
        spine = rng.randrange(q)
        req = [spine]
        sd = digits(spine, p, a)
        for t in range(1, a + 1):
            for j in range(1, p):
                r = (spine % p ** (t - 1)) + ((sd[t - 1] + j) % p) * p ** (t - 1)
                r += p ** t * rng.randrange(p ** (a - t))
                req.append(r % q)
        if len(req) > m:
            return None
        rest = []
        for _ in range(m - len(req)):
            u = rng.random()
            if u < 1 - cluster - 0.2:
                rest.append(rng.randrange(q))
            elif u < 1 - 0.2:
                base = rng.choice(req + rest)
                t = rng.randrange(a + 1)
                rest.append((base % p ** t) + p ** t * rng.randrange(p ** (a - t)))
            else:
                rest.append(rng.choice(req + rest))
        col = req + rest
        rng.shuffle(col)
        cols.append((col, q))
    return [crt([(col[k], q) for col, q in cols])[0] for k in range(m)]


def gen_coset(n, m, rng):
    B = []
    ds = [d for d in divisors(n) if 1 < d <= m] if n < 10 ** 7 else None
    if ds is None:
        # divisors up to m built from the small primes of n
        ds = [d for d in range(3, m + 1, 2) if n % d == 0]
    tries = 0
    while ds and len(B) < m and tries < 50:
        tries += 1
        d = rng.choice(ds)
        if len(B) + d > m:
            continue
        s = rng.randrange(n)
        B += [(s + k * (n // d)) % n for k in range(d)]
    while len(B) < m:
        B.append(rng.randrange(n))
    rng.shuffle(B)
    return B


def selftest(seed):
    rng = random.Random(seed)
    # 1. lib4.vanishes / good_big against division by Phi_d, small n, all signings
    cnt = 0; ntrue = 0
    for n in (9, 15, 27, 45, 75, 105, 135, 225, 315):
        for _ in range(12):
            m = rng.randint(2, 9)
            B = [rng.randrange(n) for _ in range(m)] if rng.random() < 0.5 else gen_coset(n, m, rng)
            E = all_signs(m)
            tab = bad_table(B, n, E)
            for row in range(E.shape[0]):
                eps = [int(v) for v in E[row]]
                for d in tab:
                    fd = {}
                    for x, s in zip(B, eps):
                        fd[x % d] = fd.get(x % d, 0) + s
                    assert vanishes(fd, d) == bool(tab[d][row]), (n, B, eps, d)
                    cnt += 1; ntrue += bool(tab[d][row])
    print(f"selftest 1: slice-criterion test == division by Phi_d on {cnt} triples (multiset, signing, d), {ntrue} of them with Phi_d | S: ok")
    # 2. pruned list of bad levels == unpruned list, medium n
    cnt = 0; nbad = 0
    for n in (225, 315, 675, 945, 1575, 4725, 3465, 14175, 51975):
        f = factor(n)
        dv = divisors(n)
        for _ in range(25):
            m = rng.randint(2, 24)
            u = rng.random()
            if u < 0.4:
                B = [rng.randrange(n) for _ in range(m)]
            elif u < 0.8:
                B = gen_coset(n, m, rng)
            else:
                B = gen_full(f, m, rng) or [rng.randrange(n) for _ in range(m)]
            for _ in range(6):
                eps = [rng.choice((1, -1)) for _ in range(m)]
                if rng.random() < 0.3:
                    eps = [1] * m
                full = []
                for d in dv:
                    fd = {}
                    for x, s in zip(B, eps):
                        fd[x % d] = fd.get(x % d, 0) + s
                    if vanishes(fd, d):
                        full.append(d)
                pr, _ = bad_levels_pruned(B, eps, f, first_only=False)
                assert sorted(pr) == full, (n, B, eps, pr, full)
                cnt += 1; nbad += bool(full)
    print(f"selftest 2: pruned list of bad levels == unpruned list on {cnt} signed multisets ({nbad} of them bad somewhere): ok")


def make(m, shape, rng):
    """returns (B, n, f) for the shape"""
    if shape in ('full', 'small', 'coset'):
        f = nprime(m)
        if shape == 'small':      # only the primes up to 7 of n'_m
            f = {p: a for p, a in f.items() if p <= 7}
        n = 1
        for p, a in f.items():
            n *= p ** a
        if shape == 'coset':
            return gen_coset(n, m, rng), n, f
        return gen_full(f, m, rng, cluster=0.4 if shape == 'full' else 0.7), n, f
    if shape in ('interval', 'intervalperm'):
        # the k-th element is pi_p(k) modulo p^a, a = floor(log_p m), for every odd prime p <= m (pi_p = identity for
        # 'interval': the multiset is {0, .., m-1}; random permutations for 'intervalperm'): balanced classes
        f = {}
        for p in odd_primes_upto(m):
            a = 0
            while p ** (a + 1) <= m:
                a += 1
            f[p] = a
        cols = []
        n = 1
        for p, a in f.items():
            perm = list(range(m))
            if shape == 'intervalperm':
                rng.shuffle(perm)
            cols.append(([v % p ** a for v in perm], p ** a))
            n *= p ** a
        return [crt([(col[j], q) for col, q in cols])[0] for j in range(m)], n, f
    # shapes with every element doubled or tripled by a shift, so that many moduli e have no class of one element
    if shape == 'pair':
        f = {3: 5, 5: 3, 7: 2, 11: 1}; k = 2; q = 3
    elif shape == 'pair5':
        f = {3: 5, 5: 3, 7: 2, 11: 1}; k = 2; q = 5
    elif shape == 'triple':
        f = {3: 4, 5: 2, 7: 2}; k = 3; q = 3
    elif shape == 'quint':
        f = {3: 3, 5: 2, 7: 1}; k = 5; q = 5
    n = 1
    for p, a in f.items():
        n *= p ** a
    A = None
    while A is None:
        A = gen_full(f, m // k, rng, cluster=0.5)
    B = [(x + j * (n // q)) % n for x in A for j in range(k)]
    while len(B) < m:
        B.append(rng.randrange(n))
    return B, n, f


def run(m, shape, nsets, nsign, seed):
    rng = random.Random(seed)
    B, n, f = make(m, shape, random.Random(0))
    print(f"m={m} shape={shape} seed={seed}: n = " + " * ".join(f"{p}^{a}" for p, a in sorted(f.items())) + f" = {n}")
    tot = good = 0
    allplus_bad = 0
    least = None
    t0 = time.time()
    for it in range(nsets):
        B, n, f = make(m, shape, rng)
        Bf, nf = contract(B, n)
        ff = factor(nf) if nf > 1 else {}
        if shape in ('full', 'small'):
            assert nf == n and all_full(B, n)
        g = 0
        vis = [0, 0]
        ap = None
        for k in range(nsign):
            eps = [1] * m if k == 0 else [rng.choice((1, -1)) for _ in range(m)]
            if nf == 1:
                bad = [1] if sum(eps) == 0 else []
            else:
                bad, v = bad_levels_pruned(Bf, eps, ff)
                if sum(eps) == 0 and not bad:
                    bad = [1]
                vis[0] = max(vis[0], v[0]); vis[1] = max(vis[1], v[1])
            if k == 0:
                allplus_bad += bool(bad); ap = bool(bad)
            else:
                tot += 1; g += not bad
        good += g
        least = g if least is None else min(least, g)
        print(f"  set {it}: n_flat = " + "*".join(f"{p}^{a}" for p, a in sorted(ff.items()))
              + f"; good among {nsign - 1} random signings: {g}; all + bad: {ap}"
              f" (at most {vis[0]} moduli e and {vis[1]} levels visited per signing)", flush=True)
    print(f"  total: {good} of {tot} random signings good ({good / max(tot, 1):.4f}); least per set {least} of {nsign - 1}; "
          f"all signs + bad for {allplus_bad} of {nsets} sets; {time.time() - t0:.0f} s")


if sys.argv[1] == 'selftest':
    selftest(int(sys.argv[2]))
else:
    run(int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]))
