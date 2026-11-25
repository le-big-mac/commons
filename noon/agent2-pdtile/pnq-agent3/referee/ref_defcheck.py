"""Referee: the theorem checked from the DEFINITIONS (not through (I1), (I5)) on every subset containing 0.

For each orbit representative (under x -> r(x - a), r a unit, a in A) of subsets of Z_M containing 0:
  pd   : does f exist with f(0) = 1, f >= 0, fhat >= 0, 1_A * f = 1 ?          (LP feasibility, float)
  tile : does B exist with A (+) B = Z_M ?                                        (exact backtracking)
  cm   : (T1) and (T2) relative to Z_M, from the exact zero set
  dp   : D+(Z_A) = |A| ?                                                          (LP, float)
All four should coincide if (I1), (I5) and the theorem hold.
"""
import sys, math, time
import numpy as np
from scipy.optimize import linprog
from refcommon import *
from ref_certs_lp import order_sums, dplus


def canon(M):
    units = [r for r in range(1, M) if math.gcd(r, M) == 1]
    masks = np.arange(1 << (M - 1), dtype=np.int64) * 2 + 1
    best = masks.copy()
    for a in range(M):
        has = ((masks >> a) & 1) == 1
        for r in units:
            new = np.zeros_like(masks)
            for x in range(M):
                y = (r * (x - a)) % M
                new |= ((masks >> x) & 1) << y
            best = np.where(has, np.minimum(best, new), best)
    return masks, best


def pd_by_definition(M, A):
    # variables f(0..M-1) >= 0 ; f(0) = 1 ; sum_a f(z - a) = 1 for all z ; fhat real and >= 0
    Aeq = []; beq = []
    row = [0.0] * M; row[0] = 1.0
    Aeq.append(row); beq.append(1.0)
    for z in range(M):
        row = [0.0] * M
        for a in A:
            row[(z - a) % M] += 1.0
        Aeq.append(row); beq.append(1.0)
    for xi in range(1, M):
        Aeq.append([math.sin(2 * math.pi * x * xi / M) for x in range(M)]); beq.append(0.0)
    Aub = [[-math.cos(2 * math.pi * x * xi / M) for x in range(M)] for xi in range(M)]
    bub = [0.0] * M
    r = linprog([0.0] * M, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * M, method="highs")
    return r.status == 0


def tiles(M, A):
    if M % len(A):
        return False
    full = (1 << M) - 1
    trans = []
    for t in range(M):
        m = 0
        for a in A:
            m |= 1 << ((a + t) % M)
        trans.append(m)

    def rec(cov):
        if cov == full:
            return True
        z = 0
        while (cov >> z) & 1:
            z += 1
        for t in range(M):
            m = trans[t]
            if (m >> z) & 1 and not (m & cov):
                if rec(cov | m):
                    return True
        return False
    return rec(0)


def run(p, n, q):
    t0 = time.time()
    M = p ** n * q
    masks, best = canon(M)
    reps, inv, counts = np.unique(best, return_inverse=True, return_counts=True)
    divs, R = order_sums(M)
    res = dict(sets=len(masks), orbits=len(reps), pd=0, tile=0, cm=0, dp=0, disagree=0, pd_sets=0)
    for rep, cnt in zip(reps.tolist(), counts.tolist()):
        A = [x for x in range(M) if (rep >> x) & 1]
        Z = zero_set_exact(M, A)
        E, F = EF_from_zero_set(Z, p, n, q)
        cm = (len(A) == p ** len(E) * (q if 0 in F else 1)) and ((0 not in F) or E <= F)
        dpv = abs(dplus(Z, divs, R) - len(A)) < 1e-6
        pdv = pd_by_definition(M, A)
        tl = tiles(M, A)
        res["pd"] += pdv; res["tile"] += tl; res["cm"] += cm; res["dp"] += dpv
        if pdv:
            res["pd_sets"] += cnt
        if not (pdv == tl == cm == dpv):
            res["disagree"] += 1
            print("   DISAGREE", A, dict(pd=pdv, tile=tl, cm=cm, dp=dpv))
    res["seconds"] = round(time.time() - t0, 1)
    print(f"definition check p={p} n={n} q={q} M={M}: {res}", flush=True)


if __name__ == "__main__":
    for s in sys.argv[1:]:
        p, n, q = (int(v) for v in s.split(","))
        run(p, n, q)
