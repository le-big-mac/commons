# t4_lift_sets.py -- the step behind the "if" half of `set_sizes_iff_mul`, on groups too large for a census of sets:
# for M = p^n q, s with Q = the largest odd prime power dividing s, and EVERY multiset w on Z_M with 1 <= t < Q elements
# (all of them containing 0, or a random sample), look for a SET A on Z_{M s} with #{y in A : y mod M = x} = w(x) such
# that for every d | M s:  Phi_d | A(X)  <=>  (d | M and Phi_d | w(X)).   Such an A has t elements and, among the
# divisors > 1 of M s, exactly the pattern of w; so the right-hand side of the statement gives the left-hand side.
# Search: random lifts (seeded), at most K; then every lift if there are at most CAP.
# usage: python t4_lift_sets.py M s [tmax|0] [sample_per_size|0]
import sys, itertools, random, time, json
from math import comb
import numpy as np
from core import *
from t2_compare import largest_odd_pp

K = 3000
CAP = 2_000_000


def run(M, s, tmax, sample, seed=77):
    G = M * s
    Q = largest_odd_pp(s)
    gM = Group(M)
    gG = Group(G)
    blocks = [(d, gG.off[d][0], gG.off[d][1], M % d == 0) for d in gG.divs]
    rng = random.Random(seed)
    top = Q - 1 if not tmax else min(Q - 1, tmax)

    def ok(A, want):
        v = gG.R[A].sum(axis=0)
        for d, a, b, dM in blocks:
            if (not v[a:b].any()) != (dM and d in want):
                return False
        return True

    st = dict(M=M, s=s, G=G, Q=Q, tmax=top, sample=sample, tested=0, plain_fail=0, random_first_fail=0, max_tries=0,
              exhaustive_used=0, no_witness=0, undecided=0, maxmult=0, longdiv_checked=0, longdiv_bad=0)
    bad = []
    t0 = time.time()
    for t in range(1, top + 1):
        if sample and comb(M + t - 2, t - 1) > sample:
            def gen():
                for _ in range(sample):
                    yield tuple(sorted(rng.randrange(M) for _ in range(t - 1)))
            it = gen()
        else:
            it = itertools.combinations_with_replacement(range(M), t - 1)
        for rest in it:
            w = [0] * M
            w[0] = 1
            for x in rest:
                w[x] += 1
            st['tested'] += 1
            st['maxmult'] = max(st['maxmult'], max(w))
            vw = gM.vec(w)
            want = frozenset(d for d in gM.divs if gM.divides(vw, d))
            supp = [x for x in range(M) if w[x]]
            A = [x + M * u for x in supp for u in range(w[x])]
            if not ok(A, want):
                st['plain_fail'] += 1
            found = None
            for tr in range(1, K + 1):
                A = []
                for x in supp:
                    for u in rng.sample(range(s), w[x]):
                        A.append(x + M * u)
                if ok(A, want):
                    found = A
                    break
            if found is None:
                nl = 1
                for x in supp:
                    nl *= comb(s, w[x])
                if nl <= CAP:
                    st['exhaustive_used'] += 1
                    for choice in itertools.product(*[itertools.combinations(range(s), w[x]) for x in supp]):
                        A = [x + M * u for x, us in zip(supp, choice) for u in us]
                        if ok(A, want):
                            found = A
                            break
                    if found is None:
                        st['no_witness'] += 1
                        bad.append(w)
                else:
                    st['undecided'] += 1
                    bad.append(('undecided', w))
            else:
                st['max_tries'] = max(st['max_tries'], tr)
                if tr > 1:
                    st['random_first_fail'] += 1
            if found is not None and st['tested'] % 97 == 0:
                st['longdiv_checked'] += 1
                mult = [0] * G
                for y in found:
                    mult[y] += 1
                good = max(mult) == 1 and [sum(mult[x + M * u] for u in range(s)) for x in range(M)] == w
                for d in gG.divs:
                    if divides_longdiv(G, mult, d) != ((M % d == 0) and divides_longdiv(M, w, d)):
                        good = False
                if not good:
                    st['longdiv_bad'] += 1
    st['seconds'] = round(time.time() - t0, 1)
    st['no_witness_list'] = bad[:30]
    return st


if __name__ == '__main__':
    M, s = int(sys.argv[1]), int(sys.argv[2])
    tmax = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    sample = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    print(json.dumps(run(M, s, tmax, sample)), flush=True)
