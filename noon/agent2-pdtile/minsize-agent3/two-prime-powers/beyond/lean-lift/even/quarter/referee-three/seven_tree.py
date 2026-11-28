# Referee, second look: Remark 3.3 on ALL 3-adic tree shapes of depth <= D (exact; the dynamic programme of tree3.py,
# which uses only the definitions F_1 = {s_0 = s_1 = s_2}, F_i = intersection over the classes of F_(i-1)).
#  (a) seven elements: on X the sum of the signs is +-3 (and what fails for nine);
#  (b) two occupied classes of sizes (r,r') in {3,5,7}: largest P(X) against E3(r) E3(r')/2;
#  (c) ten elements: largest P(X), by the class sizes modulo 3 of the top level.
# usage: seven_tree.py D
import sys, time
from math import comb
from fractions import Fraction as Fr
D = int(sys.argv[1]); NB = D + 2; FULL = (1 << NB) - 1
def leaf_law(r):
    return {(2 * k - r, FULL if 2 * k == r else 0): comb(r, k) for k in range(r + 1)}
def combine(laws):
    laws = laws + [None] * (3 - len(laws)); out = {}
    one = [((0, FULL), 1)]
    for (s0, J0), c0 in laws[0].items():
        for (s1, J1), c1 in (laws[1].items() if laws[1] is not None else one):
            for (s2, J2), c2 in (laws[2].items() if laws[2] is not None else one):
                J = (((J0 & J1 & J2) << 1) & FULL) | (1 if s0 == s1 == s2 else 0)
                key = (s0 + s1 + s2, J); out[key] = out.get(key, 0) + c0 * c1 * c2
    return out
shapes = {}
def get(r, d):
    if (r, d) in shapes: return shapes[(r, d)]
    laws = {}
    def add(law): laws[tuple(sorted(law.items()))] = law
    add(leaf_law(r))
    if d >= 1:
        for L in get(r, d - 1): add(combine([L]))
        for r1 in range(1, r // 2 + 1):
            for a in get(r - r1, d - 1):
                for b in get(r1, d - 1): add(combine([a, b]))
        for r2 in range(1, r // 3 + 1):
            for r1 in range(r2, (r - r2) // 2 + 1):
                for a in get(r - r1 - r2, d - 1):
                    for b in get(r1, d - 1):
                        for cc in get(r2, d - 1): add(combine([a, b, cc]))
    shapes[(r, d)] = list(laws.values()); return shapes[(r, d)]
def PX(law, r): return Fr(sum(c for (s, J), c in law.items() if s != 0 and J != 0), 2 ** r)
for m in (3, 5, 7, 9):
    Ls = get(m, D)
    sums = sorted(set(abs(s) for L in Ls for (s, J), c in L.items() if s != 0 and J != 0))
    print('(a) %d elements, every tree of depth <= %d (%d distinct laws): the sums of signs that occur on X: +-%s' % (m, D, len(Ls), sums))
E3 = {3: Fr(1, 4), 5: Fr(3, 16), 7: Fr(5, 32)}
for (r, rr) in ((3, 3), (5, 3), (5, 5), (7, 3), (7, 5), (7, 7)):
    best = max(PX(combine([a, b]), r + rr) for a in get(r, D - 1) for b in get(rr, D - 1))
    print('(b) two classes (%d,%d), subtrees of depth <= %d: largest P(X) = %s ; E3 E3 / 2 = %s ; E3 E3 = %s' % (r, rr, D - 1, best, E3[r] * E3[rr] / 2, E3[r] * E3[rr]))
m = 10; res = {}
for r1 in range(1, m // 2 + 1):
    res[(m - r1, r1)] = max(PX(combine([a, b]), m) for a in get(m - r1, D - 1) for b in get(r1, D - 1))
for r2 in range(1, m // 3 + 1):
    for r1 in range(r2, (m - r2) // 2 + 1):
        res[(m - r1 - r2, r1, r2)] = max(PX(combine([a, b, cc]), m) for a in get(m - r1 - r2, D - 1) for b in get(r1, D - 1) for cc in get(r2, D - 1))
print('(c) ten elements, top classes -> exact largest P(X) (subtrees of depth <= %d): %s' % (D - 1, ', '.join('%s: %s' % (k, v) for k, v in res.items())))
print('    largest over all: %s' % max(res.values()))
