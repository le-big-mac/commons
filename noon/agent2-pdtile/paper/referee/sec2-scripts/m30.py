# Three-prime case M = 30: all A containing 0 with |A| <= 6 (146,596 sets).
# weak tile (LP in f) vs counting certificate (LP in mu) vs tile; CM(1), CM(2), CM(3); (S) (A' within the family
# suffices since a violation needs |A'| < |A| <= 6, and zeros are translation invariant); (C) by clique search.
import sys
from itertools import combinations, product
from math import gcd
import numpy as np
from sympy import divisors
from scipy.optimize import linprog
from brute import cyc, polyrem_is_zero, prime_powers, exact, gen, digit_multiset, order

M = int(sys.argv[1]) if len(sys.argv) > 1 else 30
KMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 6
divs = divisors(M); PP = prime_powers(M); phis = {d: cyc(d) for d in divs}; nd = len(divs)

def zeros_of(A):
    co = [0] * M
    for a in A: co[a] = 1
    return frozenset(d for d in divs if polyrem_is_zero(co, phis[d]))

def tiles(A):
    k = len(A)
    if M % k: return False
    full = (1 << M) - 1
    trans = [sum(1 << ((a + b) % M) for a in A) for b in range(M)]
    def rec(cov):
        if cov == full: return True
        v = (~cov & full); v = (v & -v).bit_length() - 1
        for b in range(M):
            t = trans[b]
            if (t >> v) & 1 and not (t & cov):
                if rec(cov | t): return True
        return False
    return rec(0)

def weak_lp(A):
    Aeq = np.zeros((M, M - 1)); beq = np.ones(M)
    for v in range(M):
        for a in A:
            x = (v - a) % M
            if x == 0: beq[v] -= 1
            else: Aeq[v, x - 1] += 1
    res = linprog(np.zeros(M - 1), A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * (M - 1), method='highs')
    assert res.status in (0, 2), res.status
    return res.status == 0

Aub = np.zeros((nd, nd))
for i, g in enumerate(divs):
    for j, d in enumerate(divs):
        if g % d == 0: Aub[i, j] = -1
def cert_lp(A):
    Aeq2 = np.zeros((M + 1, nd)); beq2 = np.ones(M + 1)
    for v in range(M):
        for j, d in enumerate(divs):
            Aeq2[v, j] = sum(1 for a in A if (a - v) % d == 0)
    Aeq2[M, :] = 1
    res2 = linprog(np.zeros(nd), A_ub=Aub, b_ub=np.zeros(nd), A_eq=Aeq2, b_eq=beq2,
                   bounds=[(None, None)] * nd, method='highs')
    assert res2.status in (0, 2), res2.status
    return res2.status == 0

def clique_number(allowed):  # max |B|, 0 in B, all nonzero differences in `allowed` (symmetric set)
    best = 1
    def rec(B, cand):
        nonlocal best
        if len(B) > best: best = len(B)
        if len(B) + len(cand) <= best: return
        for i, x in enumerate(cand):
            rec(B + [x], [y for y in cand[i + 1:] if (y - x) % M in allowed])
    rec([0], sorted(allowed))
    return best

minsize = {}   # zero set (d>1) -> min size of a set (in family) with exactly this zero set
data = []
n = 0
for k in range(1, KMAX + 1):
    for rest in combinations(range(1, M), k - 1):
        A = (0,) + rest
        z = zeros_of(A); z1 = frozenset(d for d in z if d > 1)
        if z1 not in minsize or minsize[z1] > k: minsize[z1] = k
        w = weak_lp(A); c = cert_lp(A)
        data.append((A, z1, w, c)); n += 1
print(f"M={M}: {n} sets with 0 in A, |A| <= {KMAX}")
print("weak != cert:", sum(1 for (A, z, w, c) in data if w != c))
weak = [(A, z) for (A, z, w, c) in data if w]
print("weak tiles:", len(weak))
nt = sum(1 for (A, z) in weak if not tiles(A))
print("weak tiles that are not tiles:", nt)
print("tiles that LP says are not weak:", sum(1 for (A, z, w, c) in data if (not w) and M % len(A) == 0 and tiles(A)))
# CM(1) on all sets
def SA(z): return [(s, p, a) for (s, p, a) in PP if s in z]
def prodSA(z):
    pr = 1
    for (s, p, a) in SA(z): pr *= p
    return pr
print("CM(1) failures:", sum(1 for (A, z, w, c) in data if len(A) % prodSA(z)))
def T1(A, z): return len(A) == prodSA(z)
def T2(z):
    sa = set(s for (s, p, a) in SA(z))
    return all(d in z for d in divs if d > 1 and all(s in sa for (s, p, a) in PP if exact(s, d)))
f2 = 0; n12 = 0
for (A, z, w, c) in data:
    if T1(A, z) and T2(z):
        n12 += 1
        sa = set(s for (s, p, a) in SA(z))
        B = set(digit_multiset(M, [(s, p, a) for (s, p, a) in PP if s not in sa]))
        cnt = [0] * M
        for a in A:
            for b in B: cnt[(a + b) % M] += 1
        if any(x != 1 for x in cnt): f2 += 1
print(f"T1&T2 sets: {n12}; CM(2) failures: {f2}")
orph = 0; f3 = 0; app = 0; fS = 0; fC = 0; cc = {}
for (A, z) in weak:
    sa = [s for (s, p, a) in SA(z)]
    no_orphan = all(any(exact(s, d) for s in sa) for d in z)
    if no_orphan:
        app += 1
        if not T1(A, z): f3 += 1
    else:
        orph += 1
    best = min(sz for zz, sz in minsize.items() if z <= zz)
    if len(A) > best: fS += 1
    if z not in cc:
        allowed = set(x for x in range(1, M) if order(x, M) not in z)
        cc[z] = clique_number(allowed)
    if len(A) * cc[z] > M: fC += 1
print(f"weak tiles with an orphan zero: {orph}; CM(3) applicable: {app}, failures: {f3}")
print(f"(S) failures: {fS}; (C) failures: {fC}")
ex = [(A, sorted(z)) for (A, z) in weak if not all(any(exact(s, d) for s in [s for (s, p, a) in SA(z)]) for d in z)][:3]
print("examples of weak tiles with orphan zeros:", ex)
