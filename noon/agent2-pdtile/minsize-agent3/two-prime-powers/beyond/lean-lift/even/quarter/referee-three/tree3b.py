# Referee: powers of 3 only.  Exact largest P(X(B)) over ALL multisets of m elements whose 3-adic tree has depth <= D
# (that is, all multisets on Z_(3^D), up to the symmetries that permute the subclasses of a class), by a dynamic
# programme on tree shapes that uses only the definitions of result.md section 2:
#   F_0 = {sum of signs = 0};  F_1(B) = {s_0 = s_1 = s_2};  F_i(B) = intersection of F_(i-1)(B_t') (i >= 2);
#   X(B) = (F_1 u F_2 u ...) minus F_0.
# A node's "law" is the exact count of sign vectors by (sum s, set J of levels i >= 1 at which F_i holds).
# usage: tree3.py D mmax
import sys, time
from math import comb
from fractions import Fraction as Fr
from itertools import combinations_with_replacement

D = int(sys.argv[1]); MMAX = int(sys.argv[2])
NB = D + 2
FULL = (1 << NB) - 1
t0 = time.time()

def leaf_law(r):
    # r equal elements: at every level one occupied subclass; F_i = {s = 0}
    law = {}
    for k in range(r + 1):
        s = 2 * k - r
        law[(s, FULL if s == 0 else 0)] = comb(r, k)
    return law

def combine(laws):
    # laws of the occupied subclasses (1, 2 or 3 of them)
    while len(laws) < 3: laws = laws + [None]
    out = {}
    L0, L1, L2 = laws
    for (s0, J0), c0 in L0.items():
        for (s1, J1), c1 in (L1.items() if L1 is not None else [((0, FULL), 1)]):
            for (s2, J2), c2 in (L2.items() if L2 is not None else [((0, FULL), 1)]):
                J = (((J0 & J1 & J2) << 1) & FULL) | (1 if s0 == s1 == s2 else 0)
                key = (s0 + s1 + s2, J)
                out[key] = out.get(key, 0) + c0 * c1 * c2
    return out

# shapes[(r, d)] = list of laws of all shapes with r elements and depth <= d (deduplicated by law)
shapes = {}
def get(r, d):
    if (r, d) in shapes: return shapes[(r, d)]
    laws = {}
    def add(law):
        key = tuple(sorted(law.items()))
        laws[key] = law
    add(leaf_law(r))
    if d >= 1:
        # one child (a chain): only inside matters, but keep it
        for L in get(r, d - 1): add(combine([L]))
        # two children
        for r1 in range(1, r // 2 + 1):
            r0 = r - r1
            A = get(r0, d - 1); B = get(r1, d - 1)
            if r0 == r1:
                for i in range(len(A)):
                    for j in range(i, len(A)): add(combine([A[i], A[j]]))
            else:
                for a in A:
                    for b in B: add(combine([a, b]))
        # three children
        for r2 in range(1, r // 3 + 1):
            for r1 in range(r2, (r - r2) // 2 + 1):
                r0 = r - r1 - r2
                A = get(r0, d - 1); B = get(r1, d - 1); C = get(r2, d - 1)
                for ia, a in enumerate(A):
                    for ib, b in enumerate(B):
                        if r0 == r1 and ib < ia: continue
                        for ic, cc in enumerate(C):
                            if r1 == r2 and ic < ib: continue
                            add(combine([a, b, cc]))
    shapes[(r, d)] = list(laws.values())
    return shapes[(r, d)]

def PX(law, r):
    return Fr(sum(c for (s, J), c in law.items() if s != 0 and J != 0), 2 ** r)
def Pbad(law, r):
    return Fr(sum(c for (s, J), c in law.items() if s == 0 or J != 0), 2 ** r)

for m in range(1, MMAX + 1):
    Ls = get(m, D)
    mx = max(PX(L, m) for L in Ls)
    mb = max(Pbad(L, m) for L in Ls)
    # Remark 3.2
    r32 = ''
    if m in (3, 5, 7, 9):
        ok = all(abs(s) == 3 for L in Ls for (s, J), c in L.items() if s != 0 and J != 0)
        r32 = '  on X the sum is +-3: %s' % ok
    print('depth<=%d m=%d: distinct laws %d  largest P(X) = %s  largest bad share on powers of 3 = %s%s  [%.0fs]' % (D, m, len(Ls), mx, mb, r32, time.time() - t0), flush=True)
    if time.time() - t0 > 500: print('stopping (time)'); break
