# Brute-force tests of Section 2 on all subsets of Z_M.
import sys, cmath, math
from itertools import product, combinations
from math import gcd
import numpy as np
from sympy import symbols, Poly, cyclotomic_poly, divisors, factorint, ZZ
from scipy.optimize import linprog

X = symbols('X')

def cyc(d):
    return [int(c) for c in Poly(cyclotomic_poly(d, X), X, domain=ZZ).all_coeffs()]  # high -> low

def polyrem_is_zero(coefs_low, phi_high):
    # coefs_low: list of ints, index = exponent; phi monic, high->low
    r = list(coefs_low)
    dphi = len(phi_high) - 1
    phi_low = phi_high[::-1]
    for k in range(len(r) - 1, dphi - 1, -1):
        c = r[k]
        if c:
            for j in range(dphi + 1):
                r[k - dphi + j] -= c * phi_low[j]
    return all(x == 0 for x in r[:dphi]) if dphi > 0 else all(x == 0 for x in r)

def order(xi, M):
    return M // gcd(xi, M)

def prime_powers(M):
    return [(p ** a, p, a) for p, e in sorted(factorint(M).items()) for a in range(1, e + 1)]

def exact(s, d):
    return d % s == 0 and gcd(s, d // s) == 1

def gen(M, p, a):
    Mp = M
    while Mp % p == 0:
        Mp //= p
    return p ** (a - 1) * Mp

def digit_multiset(M, S):  # S list of (s,p,a); returns list with multiplicity
    out = []
    for c in product(*[range(p) for (s, p, a) in S]):
        out.append(sum(ci * gen(M, p, a) for ci, (s, p, a) in zip(c, S)) % M)
    return out

def run(M, do_lp=True, verbose=True):
    divs = divisors(M)
    PP = prime_powers(M)
    phis = {d: cyc(d) for d in divs}
    w = [cmath.exp(2j * cmath.pi * k / M) for k in range(M)]
    N = 1 << M
    elems = [[a for a in range(M) if (m >> a) & 1] for m in range(N)]
    # --- zeros (exact) and Lemma gal
    zeros = [None] * N
    gal_fail = 0
    for m in range(N):
        A = elems[m]
        co = [0] * M
        for a in A: co[a] = 1
        z = frozenset(d for d in divs if polyrem_is_zero(co, phis[d]))
        zeros[m] = z
        for xi in range(M):
            h = sum(w[(xi * a) % M] for a in A)
            numzero = abs(h) < 1e-9
            if numzero != (order(xi, M) in z):
                gal_fail += 1
    print(f"M={M}: Lemma gal (numeric zero at xi  <=>  Phi_ord(xi) | A(X)) failures: {gal_fail}")
    # --- Lemma digit, all S
    dig_fail = 0
    for r in range(len(PP) + 1):
        for S in combinations(PP, r):
            ms = digit_multiset(M, list(S))
            T = set(ms)
            pr = 1
            for (s, p, a) in S: pr *= p
            m = sum(1 << t for t in T)
            want = frozenset(d for d in divs if any(exact(s, d) for (s, p, a) in S))
            if len(ms) != len(T) or len(T) != pr or zeros[m] != want:
                dig_fail += 1
                print("  digit failure", M, S, sorted(T), sorted(zeros[m]), sorted(want))
    print(f"M={M}: Lemma digit failures over all {2**len(PP)} S: {dig_fail}")
    # --- S_A, T1, T2, CM(1), CM(2)
    def SA(m): return [(s, p, a) for (s, p, a) in PP if s in zeros[m]]
    def prodSA(m):
        pr = 1
        for (s, p, a) in SA(m): pr *= p
        return pr
    def T1(m): return len(elems[m]) == prodSA(m)
    def T2(m):
        sa = set(s for (s, p, a) in SA(m))
        return all(d in zeros[m] for d in divs if d > 1 and all(s in sa for (s, p, a) in PP if exact(s, d)))
    def is_tiling(A, B):
        cnt = [0] * M
        for a in A:
            for b in B: cnt[(a + b) % M] += 1
        return all(c == 1 for c in cnt)
    cm1_fail = sum(1 for m in range(N) if len(elems[m]) % prodSA(m) != 0)
    print(f"M={M}: CM(1) failures: {cm1_fail}")
    cm2_fail = 0; nT12 = 0
    for m in range(N):
        if T1(m) and T2(m):
            nT12 += 1
            sa = set(s for (s, p, a) in SA(m))
            B = set(digit_multiset(M, [(s, p, a) for (s, p, a) in PP if s not in sa]))
            if not is_tiling(elems[m], B): cm2_fail += 1
    print(f"M={M}: sets with T1&T2: {nT12}; CM(2) failures: {cm2_fail}")
    # --- tiles by brute force (A tiles iff exists B)
    tile = [False] * N
    bysize = {}
    for m in range(N): bysize.setdefault(len(elems[m]), []).append(m)
    for m in range(1, N):
        k = len(elems[m])
        if M % k: continue
        # search B containing 0 of size M/k such that A+B = Z_M : use translates-of-A exact cover with B
        full = N - 1
        trans = [sum(1 << ((a + b) % M) for a in elems[m]) for b in range(M)]
        def rec(cov):
            if cov == full: return True
            v = (~cov & full); v = (v & -v).bit_length() - 1
            for b in range(M):
                t = trans[b]
                if (t >> v) & 1 and not (t & cov):
                    if rec(cov | t): return True
            return False
        tile[m] = rec(0)
    ntile = sum(tile)
    tT = sum(1 for m in range(N) if tile[m] and not (T1(m) and T2(m)))
    Tt = sum(1 for m in range(N) if (T1(m) and T2(m)) and not tile[m])
    print(f"M={M}: tiles: {ntile}; tiles failing T1 or T2: {tT}; T1&T2 non-tiles: {Tt}")
    # --- weak tiles by LP in f
    weak = [False] * N; cert = [False] * N
    for m in (range(1, N) if do_lp else []):
        A = elems[m]
        # variables f(1..M-1) >= 0 ; f(0)=1
        Aeq = np.zeros((M, M - 1)); beq = np.ones(M)
        for v in range(M):
            for a in A:
                x = (v - a) % M
                if x == 0: beq[v] -= 1
                else: Aeq[v, x - 1] += 1
        if M == 1:
            weak[m] = abs(beq[0]) < 1e-12
        else:
            res = linprog(np.zeros(M - 1), A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * (M - 1), method='highs')
            weak[m] = (res.status == 0)
            if res.status not in (0, 2): print("  LP status", res.status, A)
        # counting certificate LP in mu
        nd = len(divs)
        Aeq2 = np.zeros((M + 1, nd)); beq2 = np.ones(M + 1)
        for v in range(M):
            for j, d in enumerate(divs):
                Aeq2[v, j] = sum(1 for a in A if (a - v) % d == 0)
        Aeq2[M, :] = 1
        Aub = np.zeros((nd, nd))
        for i, g in enumerate(divs):
            for j, d in enumerate(divs):
                if g % d == 0: Aub[i, j] = -1
        res2 = linprog(np.zeros(nd), A_ub=Aub, b_ub=np.zeros(nd), A_eq=Aeq2, b_eq=beq2,
                       bounds=[(None, None)] * nd, method='highs')
        cert[m] = (res2.status == 0)
        if res2.status not in (0, 2): print("  LP2 status", res2.status, A)
    if not do_lp:
        weak = list(tile); cert = list(tile); print('  (no LP: using tiles as the weak tiles below)')
    nweak = sum(weak)
    print(f"M={M}: weak tiles (LP): {nweak}; weak != cert: {sum(1 for m in range(N) if weak[m] != cert[m])}; "
          f"weak != tile: {sum(1 for m in range(N) if weak[m] != tile[m])}")
    # --- (S)
    # min size of nonempty A' whose zero set contains Z (d>1)
    S_fail = 0
    zsets = {}
    for m in range(1, N):
        z = frozenset(d for d in zeros[m] if d > 1)
        zsets.setdefault(z, len(elems[m]))
        zsets[z] = min(zsets[z], len(elems[m]))
    for m in range(1, N):
        if weak[m]:
            zA = frozenset(d for d in zeros[m] if d > 1)
            best = min(sz for z, sz in zsets.items() if zA <= z)
            if len(elems[m]) > best: S_fail += 1
    print(f"M={M}: (S) failures: {S_fail}")
    # --- (C): all B
    diffmask = [0] * N
    for m in range(N):
        B = elems[m]; dm = 0
        for b in B:
            for b2 in B:
                if b != b2: dm |= 1 << ((b - b2) % M)
        diffmask[m] = dm
    C_fail = 0; C_tight = 0; ccache = {}
    for m in range(1, N):
        if weak[m]:
            bad = sum(1 << x for x in range(1, M) if order(x, M) in zeros[m])  # differences not allowed
            if bad not in ccache: ccache[bad] = max(len(elems[b]) for b in range(N) if not (diffmask[b] & bad))
            mx = ccache[bad]
            if len(elems[m]) * mx > M: C_fail += 1
            if len(elems[m]) * mx == M: C_tight += 1
    print(f"M={M}: (C) failures: {C_fail} (tight for {C_tight} of {nweak} weak tiles)")
    # --- CM(3)
    cm3_fail = 0; cm3_app = 0
    for m in range(1, N):
        if weak[m]:
            sa = [s for (s, p, a) in SA(m)]
            if all(any(exact(s, d) for s in sa) for d in zeros[m] if d > 1):
                cm3_app += 1
                if not T1(m): cm3_fail += 1
    print(f"M={M}: CM(3) applicable to {cm3_app} weak tiles; failures: {cm3_fail}")
    if len(factorint(M)) <= 1:
        print(f"M={M}: CM(4) (prime power) weak-not-tile: {sum(1 for m in range(N) if weak[m] and not tile[m])}")
    # weak tile empty set?
    print(f"M={M}: empty set: zeros={sorted(zeros[0])}, T1={T1(0)}, T2={T2(0)}, CM1 ok={len(elems[0]) % prodSA(0) == 0}")

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        nolp = arg.endswith('t')
        run(int(arg.rstrip('t')), do_lp=not nolp)
        print()
