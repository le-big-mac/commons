"""Theorem S by machine, for one group Z_M and every up-set D of the divisors of M (1 not in D).

What is computed: ALL extreme rays of the cone
        P(M, D) = { A in R^M : A >= 0, Phi_d | A for every d in D }
by the double description method in exact integer arithmetic (no solver, no floating point in any decision).

Why that is Theorem S for (M, D):  the cone is rational.  If its extreme rays are exactly the indicators of the cosets
x + cZ_M, c a corner of D, then every A in the cone is a nonnegative real combination of those indicators; if A is also an
integer vector and not 0, some coset K has a positive coefficient, so A > 0 on K, so A >= 1 on K, and A - 1_K is again a
nonnegative integer point of the cone; by induction on |A|, A is a sum of corner cosets.  Conversely Theorem S for (M, D)
gives, by scaling, that every rational point of the cone is a nonnegative combination of corner cosets, so every extreme ray
is one of them.  So:  Theorem S holds for (M, D)  <=>  the extreme rays of P(M, D) are corner cosets.

The equations are the cuboid forms of lib.cuboid_rows (not remainders modulo Phi_d).
Method: rays(D) is obtained from rays(D minus one minimal element d) by adding the d cuboid equations of scale d one at a
time.  Adjacency of two rays is the combinatorial test (no third ray has its support inside the union of their supports),
with the necessary condition |union| <= rank + 2 as a first filter (rank = sum of phi(d) over D, an upper bound for the
rank of the equations added so far).

usage: dd.py M [maxrays]      one line per up-set
"""
import sys, time, json, math
import numpy as np
from lib import divisors, upsets, corners, cuboid_rows, prime_factors, divides


def phi(n):
    r = n
    for p in prime_factors(n): r = r // p * (p - 1)
    return r


class TooBig(Exception):
    pass


def add_equation(R, b, rank, maxrays, stats):
    s = R @ b
    pos = np.nonzero(s > 0)[0]; neg = np.nonzero(s < 0)[0]
    if len(pos) == 0 and len(neg) == 0: return R
    keep = R[s == 0]
    if len(pos) == 0 or len(neg) == 0: return keep
    Sb = (R != 0)
    Sf = Sb.astype(np.float32)
    notneg = None
    new = []
    for i in pos:
        U = Sb[i] | Sb[neg]
        cnt = U.sum(1)
        cand = np.nonzero(cnt <= rank + 2)[0]
        if len(cand) == 0: continue
        notU = (~U[cand]).astype(np.float32)
        outside = Sf @ notU.T                                  # rays x candidates: support points outside the union
        nsub = (outside < 0.5).sum(0)                          # how many rays lie inside the union (the two themselves count)
        for t in np.nonzero(nsub == 2)[0]:
            j = neg[cand[t]]
            v = int(s[i]) * R[j].astype(object) - int(s[j]) * R[i].astype(object)
            g = 0
            for a in v:
                g = math.gcd(g, int(a))
            v = np.array([int(a) // g for a in v], dtype=object)
            if max(v) >= 2 ** 40: raise TooBig('entries too large')
            new.append(v.astype(np.int64))
        if len(keep) + len(new) > maxrays: raise TooBig(f'more than {maxrays} rays')
    if new:
        R2 = np.vstack([keep, np.array(new, dtype=np.int64)])
    else:
        R2 = keep
    stats['peak'] = max(stats['peak'], len(R2))
    return R2


def main():
    M = int(sys.argv[1]); maxrays = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
    ups = upsets(M)
    rays = {(): np.eye(M, dtype=np.int64)}
    ok = bad = skipped = 0
    t00 = time.time()
    for D in ups:
        if not D:
            # D empty: the cone is the orthant, its rays are the points = cosets of MZ_M; corner M
            assert corners(M, D) == [M]
            print(json.dumps(dict(M=M, D=[], corners=[M], rays=M, rays_are_corner_cosets=True, peak=M, seconds=0.0)), flush=True)
            ok += 1; continue
        Dset = set(D)
        mins = [d for d in D if not any(e != d and d % e == 0 for e in D)]
        pred = None
        for d in mins:                                           # a predecessor already computed
            D0 = tuple(sorted(Dset - {d}))
            if D0 in rays: pred = (d, D0); break
        if pred is None:
            print(json.dumps(dict(M=M, D=list(D), skipped='no predecessor computed')), flush=True); skipped += 1; continue
        d, D0 = pred
        rank = sum(phi(e) for e in D)
        R = rays[D0]; stats = dict(peak=len(R)); t0 = time.time()
        try:
            for row in cuboid_rows(M, d):
                b = np.zeros(M, dtype=np.int64)
                for x, c in row.items(): b[x] = c
                R = add_equation(R, b, rank, maxrays, stats)
        except TooBig as e:
            print(json.dumps(dict(M=M, D=list(D), skipped=str(e), seconds=round(time.time() - t0, 1))), flush=True); skipped += 1; continue
        rays[D] = R
        # compare with the corner cosets
        C = corners(M, D)
        want = set()
        for c in C:
            for x in range(c): want.add(frozenset(range(x, M, c)))
        got = set(); all01 = True
        for r in R:
            if r.max() != 1: all01 = False
            got.add(frozenset(np.nonzero(r)[0].tolist()))
        same = all01 and got == want and len(R) == len(want)
        # every ray found does satisfy the divisibilities (exact check by lib.divides)
        for r in R:
            for e in D: assert divides(M, e, r.tolist())
        if same: ok += 1
        else: bad += 1
        rec = dict(M=M, D=list(D), added=d, corners=C, rays=len(R), rays_are_corner_cosets=same, peak=stats['peak'], seconds=round(time.time() - t0, 1))
        if not same:
            extra = [sorted(s) for s in got - want][:5]
            rec['rays_not_cosets_examples'] = [[int(v) for v in r] for r in R if frozenset(np.nonzero(r)[0].tolist()) not in want][:5]
            rec['cosets_missing'] = len(want - got)
        print(json.dumps(rec), flush=True)
    print(f'# Z_{M}: {len(ups)} up-sets; extreme rays are exactly the corner cosets in {ok}; not so in {bad}; not computed {skipped}; {time.time() - t00:.0f} s', flush=True)


if __name__ == '__main__':
    main()
