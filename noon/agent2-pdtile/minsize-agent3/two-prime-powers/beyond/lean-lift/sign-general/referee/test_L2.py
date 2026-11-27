# Referee test of Lemma 2 (c), (d) for lines/hyperplanes, the case k = 1 exhaustively, and Remark (1).
import itertools
from math import comb
import numpy as np
from fractions import Fraction
from boxlib import *

# (c) by the formula <s,s0> = p - 2j
worst = 0
for p in range(3, 100, 2):
    for q in [0] + [x for x in range(3, 200, 2) if all(x % y for y in range(3, x, 2))]:
        if q and p % q == 0:
            continue
        J = [j for j in range(p + 1) if ((p - 2 * j) % q if q else p - 2 * j) == 0]
        cnt = sum(comb(p, j) for j in J)
        assert cnt <= 2 ** (p - 1) - 2, (p, q)
        worst = max(worst, Fraction(cnt, 2 ** (p - 1) - 2))
print('Lemma 2(c): odd p < 100, Q and odd primes q < 200 not dividing p: holds; largest count/(2^(p-1)-2) =', float(worst))
# and by enumeration for small p
for p, q in [(3, 5), (5, 3), (5, 7), (7, 3), (7, 5), (9, 5), (9, 7)]:
    S = signs(p)
    for s0 in S[:4]:
        assert int((((S @ s0) % q) == 0).sum()) <= 2 ** (p - 1) - 2

# (d) for K a line or a hyperplane: every projective point kappa of F_q^p
for p, q in [(3, 5), (3, 7), (3, 11), (5, 3), (5, 7), (7, 3)]:
    S = signs(p)
    mx = 0
    for kap in itertools.product(range(q), repeat=p):
        nzs = [x for x in kap if x]
        if not nzs or nzs[0] != 1:
            continue
        kap = np.array(kap)
        perp = ((S @ kap) % q) == 0
        # s on the line: s = lam * kap
        online = np.array([any((((lam * kap) - s) % q == 0).all() for lam in range(1, q)) for s in S]) if set(nzs) <= {1, q - 1} and len(nzs) == p else np.zeros(len(S), bool)
        mx = max(mx, int((perp | online).sum()))
    assert mx <= 2 ** (p - 1)
    # k = 1 exhaustively: every nonzero f, number of sign vectors with sum != 0 and not constant
    least = 2 ** p
    for f in itertools.product(range(q), repeat=p):
        if not any(f):
            continue
        V = (S * np.array(f)) % q
        good = (V.sum(axis=1) % q != 0) & (V != V[:, :1]).any(axis=1)
        least = min(least, int(good.sum()))
    print('p=%d q=%d: largest count in K u Kperp over all lines K: %d (2^(p-1) = %d); k=1 least number of good sign vectors over all nonzero f: %d'
          % (p, q, mx, 2 ** (p - 1), least))
    assert least >= 2 ** (p - 1)

# Remark (1): g = tensor of (1,1,0,...,0)
for sides, q in [([3, 5], 0), ([3, 5], 7), ([5, 5], 3), ([3, 5, 7], 0), ([3, 5, 7], 11)]:
    g = np.array([1])
    for n in sides:
        g = np.multiply.outer(g, np.array([1, 1] + [0] * (n - 2)))
    g = g.reshape(sides)
    res, per = good_table(g, sides, q, all_levels(len(sides)))
    print('Remark (1)', sides, 'q =', q, 'fraction', Fraction(int(res.sum()), res.size))

# hypothesis "char does not divide p": what happens on side 3 over F_3 and 5 over F_5 (k = 1)
for p, q in [(3, 3), (5, 5), (9, 3)]:
    S = signs(p)
    least = 2 ** p
    arg = None
    for f in itertools.product(range(q), repeat=p):
        if not any(f):
            continue
        V = (S * np.array(f)) % q
        good = (V.sum(axis=1) % q != 0) & (V != V[:, :1]).any(axis=1)
        if int(good.sum()) < least:
            least, arg = int(good.sum()), f
    print('outside the hypothesis: p=%d over F_%d, k=1: least number of good sign vectors %d of %d at f=%s' % (p, q, least, 2 ** p, arg))
