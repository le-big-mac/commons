# t1_setlift.py -- test of the statement `exists_set_lift`, literally:
#   N >= 1, r prime, j, w : Z_N -> N with  w(x) <= r^j for all x  (hle)  and  some x with w(x) != 0 and w(x) != r^j  (hne).
#   Claim (for r odd): there is a set A in Z_{N r^j} with  #{y in A : y mod N = x} = w(x)  for every x, such that for
#   EVERY d | N r^j:   Phi_d | A(X)   <=>   ( d | N  and  Phi_d | w(X) ).
# For every such w (all of them, or all with support <= maxsupp, or a random sample) three things are tried:
#   (a) the plain lift: the copies of x go to x, x+N, x+2N, ...                       (may gain a divisor)
#   (b) the recipe of the paper's proof, carried out step by step (r odd only)       (should never fail)
#   (c) random lifts (seeded), at most K of them, then, if none works, EVERY lift (if there are at most CAP of them)
# The claim holds for w if (c) -- or (a) or (b) -- gives a set with exactly the divisors required; every witness is
# checked with the remainder tables of core.py, on the big group for the set and on Z_N for w, for every d | N r^j, both
# directions; one in `ldstep` witnesses is checked again by literal long division.
# usage: python t1_setlift.py N r j [maxsupp|0] [sample|0]
import sys, itertools, random, time, json
from math import comb
import numpy as np
from core import *

import os
K = int(os.environ.get("T1_K", "3000"))
CAP = 3_000_000


def recipe_lift(N, r, j, w):
    cur = N
    mult = {x: w[x] for x in range(N) if w[x]}
    for i in range(j, 0, -1):
        assert all(m <= r ** i for m in mult.values())
        assert any(0 < m < r ** i for m in mult.values())
        k = 0
        Np = cur
        while Np % r == 0:
            Np //= r
            k += 1
        rk = r ** k
        nondiv = [x for x in sorted(mult) if mult[x] % r != 0]
        if nondiv:
            x1, case = nondiv[0], 1
        else:
            x1, case = [x for x in sorted(mult) if 0 < mult[x] < r ** i][0], 2
        new = {}
        for x, m in mult.items():
            a, rho = divmod(m, r)
            cnt = [a] * r
            if x != x1:
                if rho <= r - 2:
                    for t in range(1, 1 + rho):
                        cnt[t] += 1
                else:
                    for t in range(r):
                        if t != 1:
                            cnt[t] += 1
            elif case == 1:
                cnt[0] = a + 1
                cnt[r - 1] = a
                for t in range(1, rho):
                    cnt[t] += 1
            else:
                cnt[0] = a + 1
                cnt[r - 1] = a - 1
            assert sum(cnt) == m and min(cnt) >= 0
            for u in range(r):
                t = (x // rk + Np * u) % r
                if cnt[t]:
                    new[x + cur * u] = cnt[t]
        mult = new
        cur *= r
    assert all(m == 1 for m in mult.values())
    return sorted(mult)


def run(N, r, j, maxsupp, sample, seed=2026):
    q = r ** j
    G = N * q
    gN = Group(N)
    gG = Group(G)
    divG = gG.divs
    blocks = [(d, gG.off[d][0], gG.off[d][1], N % d == 0) for d in divG]
    rng = random.Random(seed)

    def wanted(w):
        vw = gN.vec(w)
        return frozenset(d for d in gN.divs if gN.divides(vw, d))

    def ok(A, want):
        v = gG.R[A].sum(axis=0)
        for d, a, b, dN in blocks:
            lhs = not v[a:b].any()
            if lhs != (dN and d in want):
                return False
        return True

    def ok_longdiv(A, w):
        mult = [0] * G
        for y in A:
            mult[y] += 1
        fib = [0] * N
        for y in A:
            fib[y % N] += 1
        if fib != list(w) or max(mult) > 1:
            return False
        for d in divG:
            lhs = divides_longdiv(G, mult, d)
            rhs = (N % d == 0) and divides_longdiv(N, list(w), d)
            if lhs != rhs:
                return False
        return True

    # the w to test
    def all_w():
        if maxsupp:
            for k in range(1, min(maxsupp, N) + 1):
                for supp in itertools.combinations(range(N), k):
                    for vals in itertools.product(range(1, q + 1), repeat=k):
                        w = [0] * N
                        for x, v in zip(supp, vals):
                            w[x] = v
                        yield w
        else:
            for w in itertools.product(range(q + 1), repeat=N):
                yield list(w)

    if sample:
        def gen():
            for _ in range(sample):
                k = rng.randint(1, N)
                supp = rng.sample(range(N), k)
                w = [0] * N
                for x in supp:
                    w[x] = rng.randint(1, q)
                yield w
        ws = gen()
    else:
        ws = all_w()

    st = dict(N=N, r=r, j=j, G=G, maxsupp=maxsupp, sample=sample, tested=0, excluded_hne=0, excluded_hne_fail=0,
              plain_fail=0, recipe_fail=0, random_first_fail=0, max_tries=0, tries_total=0, exhaustive_used=0,
              no_witness=0, undecided=0, longdiv_checked=0, longdiv_bad=0)
    nowit = []
    ldstep = 1 if (sample and sample <= 2000) else 37
    t0 = time.time()
    for w in ws:
        if not any(w):
            continue
        hne = any(v != 0 and v != q for v in w)
        want = wanted(w)
        if not hne:
            # every element of multiplicity r^j: the only set with these fibre counts is the full preimage
            st['excluded_hne'] += 1
            A = [x + N * u for x in range(N) if w[x] for u in range(q)]
            if not ok(A, want):
                st['excluded_hne_fail'] += 1
            continue
        st['tested'] += 1
        witness = None
        A = [x + N * u for x in range(N) for u in range(w[x])]
        if ok(A, want):
            witness = A
        else:
            st['plain_fail'] += 1
        if r != 2:
            A = recipe_lift(N, r, j, w)
            fib = [0] * N
            for y in A:
                fib[y % N] += 1
            assert fib == list(w) and len(set(A)) == len(A)
            if ok(A, want):
                witness = A
            else:
                st['recipe_fail'] += 1
        # (c) random lifts
        found = None
        supp = [x for x in range(N) if w[x]]
        for tr in range(1, K + 1):
            A = []
            for x in supp:
                for u in rng.sample(range(q), w[x]):
                    A.append(x + N * u)
            if ok(A, want):
                found = A
                break
        if found is None:
            nl = 1
            for x in supp:
                nl *= comb(q, w[x])
            if nl <= CAP:
                st['exhaustive_used'] += 1
                for choice in itertools.product(*[itertools.combinations(range(q), w[x]) for x in supp]):
                    A = [x + N * u for x, us in zip(supp, choice) for u in us]
                    if ok(A, want):
                        found = A
                        break
                if found is not None:
                    witness = found
                elif witness is None:
                    st['no_witness'] += 1
                    nowit.append(list(w))
                else:
                    st['only_recipe_or_plain'] = st.get('only_recipe_or_plain', 0) + 1
            elif witness is None:
                st['undecided'] += 1
                nowit.append(('undecided', list(w)))
        else:
            st['tries_total'] += tr
            st['max_tries'] = max(st['max_tries'], tr)
            if tr > 1:
                st['random_first_fail'] += 1
            witness = found
        if witness is not None and st['tested'] % ldstep == 0:
            st['longdiv_checked'] += 1
            if not ok_longdiv(witness, w):
                st['longdiv_bad'] += 1
    st['seconds'] = round(time.time() - t0, 1)
    st['no_witness_list'] = nowit[:40]
    return st


if __name__ == '__main__':
    N, r, j = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    maxsupp = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    sample = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    st = run(N, r, j, maxsupp, sample)
    print(json.dumps(st), flush=True)
