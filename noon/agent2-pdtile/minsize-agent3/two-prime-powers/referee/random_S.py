"""Theorem S on multisets that are NOT built as coset sums.

(1) Lattice route.  The integer vectors divisible by every Phi_d, d in D, are the multiples g(X) h(X) of g = prod_{d in D} Phi_d
    (degree of h below M - deg g).  Take h with random integer coefficients, then add the least constant that makes the vector
    nonnegative (a constant vector is divisible by every Phi_d, d > 1).  Also a sparser kind: the same, then subtract corner
    cosets greedily is NOT done here -- the multiset is used as it comes.  Each is checked to satisfy (i) by lib.divides and then
    decomposed: while it is not zero, find a corner coset on which it is >= 1 everywhere and subtract it.  If no such coset
    exists for a nonzero remainder, that remainder is a counterexample to Theorem S (it satisfies (i) and contains no corner
    coset); the program would print it.
(2) Vertex route.  Linear programme (HiGHS simplex through scipy.linprog): minimise a random linear form over
    {A >= 0, sum A = 1, cuboid equations for d in D}.  The optimum is a vertex, i.e. an extreme ray of the cone.  Theorem S
    for (M, D) says every such vertex is 1_K / |K| for a corner coset K.  (Floating point; a vertex is accepted as a coset
    if its support, at tolerance 1e-9, is a corner coset and its values are equal to 1e-9.)

usage: random_S.py M nlattice nvertex seed
"""
import sys, json, random, time
import numpy as np
from lib import upsets, corners, cuboid_rows, divides, cyclotomic


def polymul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b): r[i + j] += x * y
    return r


def decompose(M, A, cosets):
    """greedy; returns (True, number of cosets used) or (False, remainder)"""
    A = list(A); used = 0
    while any(A):
        for K in cosets:
            t = min(A[x] for x in K)
            if t >= 1:
                for x in K: A[x] -= t
                used += t; break
        else:
            return False, A
    return True, used


def main():
    M, nl, nv, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    random.seed(seed); rng = np.random.default_rng(seed)
    from scipy.optimize import linprog
    tot_l = ok_l = tot_v = ok_v = 0; t0 = time.time()
    for D in upsets(M):
        C = corners(M, D)
        cosets = [list(range(x, M, c)) for c in C for x in range(c)]
        cosetsets = {frozenset(K) for K in cosets}
        g = [1]
        for d in D: g = polymul(g, list(cyclotomic(d)))
        deg = len(g) - 1
        bad = []
        nlat = 0
        if M - deg >= 1:
            for _ in range(nl):
                amp = random.choice((1, 1, 2, 3))
                h = [random.randint(-amp, amp) for _ in range(M - deg)]
                if random.random() < 0.5:                        # a sparse h
                    h = [x if random.random() < 0.3 else 0 for x in h]
                B = polymul(g, h); B = B + [0] * (M - len(B)); assert len(B) == M
                mn = min(B); A = [x - mn for x in B]
                if not any(A): continue
                for d in D: assert divides(M, d, A)
                nlat += 1; tot_l += 1
                ok, info = decompose(M, A, cosets)
                if ok: ok_l += 1
                else: bad.append(info)
        # vertex route
        nver = 0; vbad = []
        rows = []
        for d in D:
            for r in cuboid_rows(M, d):
                v = np.zeros(M)
                for x, c in r.items(): v[x] = c
                rows.append(v)
        Aeq = np.vstack(rows + [np.ones(M)]) if rows else np.ones((1, M)); beq = np.zeros(len(Aeq)); beq[-1] = 1
        for _ in range(nv):
            cvec = rng.normal(size=M)
            res = linprog(cvec, A_eq=Aeq, b_eq=beq, bounds=(0, None), method='highs-ds')
            assert res.status == 0
            x = res.x; sup = frozenset(np.nonzero(x > 1e-9)[0].tolist())
            tot_v += 1; nver += 1
            if sup in cosetsets and np.allclose(x[list(sup)], 1.0 / len(sup), atol=1e-9, rtol=0): ok_v += 1
            else: vbad.append([round(float(t), 6) for t in x])
        print(json.dumps(dict(M=M, D=list(D), corners=C, lattice_multisets=nlat, decomposed=nlat - len(bad), counterexamples=bad[:2],
                              vertices=nver, vertices_that_are_corner_cosets=nver - len(vbad), other_vertices=vbad[:2])), flush=True)
    print(f'# Z_{M}: lattice-built multisets {tot_l}, decomposed into corner cosets {ok_l}; linear-programme vertices {tot_v}, corner cosets {ok_v}; {time.time() - t0:.0f} s', flush=True)


if __name__ == '__main__':
    main()
