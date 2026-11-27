# t3_H.py -- Proposition H by brute force: on an odd modulus, the share of good signings of every multiset of m >= 3
# elements, against 3/4 (m = 3), 5/8 (m = 4), 0.537 (m >= 5); also the share of 3-good signings against
# 1 - p_m - [m >= 5] W(no 3), and "3-good implies good" (Lemma M) for every signing.
# A multiset is given by its distinct points and multiplicities; a signing matters only through the signed count at each
# point, so all signings are covered by all vectors of signed counts with their binomial weights (exact).
# usage: t3_H.py exhaust n:mmax n:mmax ...   |   t3_H.py random
import sys, random
from math import comb
from itertools import product, combinations_with_replacement
from collections import Counter
from rlib import *

W3 = 0.119134
P = [Fraction(1)]
for r in range(64):
    P.append((1 - P[-1]) / 2)

def analyse(n, pts, mult, divs, divs3):
    # returns (number of good signings, number of 3-good signings, lemmaM_ok)
    ranges = [np.arange(-c, c + 1, 2) for c in mult]
    wts = [np.array([comb(c, (c + s) // 2) for s in range(-c, c + 1, 2)], dtype=np.int64) for c in mult]
    G = np.array(np.meshgrid(*ranges, indexing='ij')).reshape(len(mult), -1).T.astype(np.int64)   # V x r
    Wt = wts[0]
    for w in wts[1:]:
        Wt = np.multiply.outer(Wt, w)
    Wt = Wt.reshape(-1)
    V = G.shape[0]
    good = np.ones(V, dtype=bool)
    good3 = np.ones(V, dtype=bool)
    idx = np.asarray(pts)
    for d in divs:
        R = G @ powtable(d)[idx % d]
        good &= R.any(axis=1)
        if d in divs3:
            good3 &= (R % 3).any(axis=1)
    lemmaM = not (good3 & ~good).any()
    return int(Wt[good].sum()), int(Wt[good3].sum()), lemmaM

def bound(m):
    return Fraction(3, 4) if m == 3 else Fraction(5, 8) if m == 4 else Fraction(537, 1000)

def bound3(m):
    return 1 - P[m] - (Fraction(119134, 10 ** 6) if m >= 5 else 0)

mode = sys.argv[1]
if mode == 'exhaust':
    for spec in sys.argv[2:]:
        n, mmax = map(int, spec.split(':'))
        assert n % 2 == 1
        divs = divisors(n)
        n3 = n
        while n3 % 3 == 0:
            n3 //= 3
        divs3 = set(divisors(n3))
        for m in range(3, mmax + 1):
            least = None; least3 = None; cnt = 0; attained = 0
            for rest in combinations_with_replacement(range(n), m - 1):
                c = Counter((0,) + rest)
                pts = sorted(c); mult = [c[x] for x in pts]
                g, g3, ok = analyse(n, pts, mult, divs, divs3)
                assert ok, ("Lemma M fails", n, pts, mult)
                sh = Fraction(g, 2 ** m); sh3 = Fraction(g3, 2 ** m)
                assert sh >= bound(m) and (m <= 4 or sh > bound(m)), ("Proposition H fails", n, pts, mult, sh)
                assert sh3 >= bound3(m), ("3-good share below the bound", n, pts, mult, sh3)
                if least is None or sh < least[0]:
                    least = (sh, pts, mult); attained = 0
                if sh == least[0]:
                    attained += 1
                if least3 is None or sh3 < least3[0]:
                    least3 = (sh3, pts, mult)
                cnt += 1
            print(f"n = {n} m = {m}: all {cnt} multisets with 0: least share of good signings {least[0]} = {float(least[0]):.4f} "
                  f"(bound {bound(m)}{'' if m > 4 else ', attained' if least[0] == bound(m) else ', not attained'}) at points {least[1]} mult {least[2]} ({attained} times); "
                  f"least share of 3-good {least3[0]} (1 - p_m = {1 - P[m]}) at {least3[1]} {least3[2]}", flush=True)
else:
    random.seed(77)
    for n in (9, 15, 27, 45, 75, 105, 135, 225, 315, 525, 1155):
        divs = divisors(n)
        n3 = n
        while n3 % 3 == 0:
            n3 //= 3
        divs3 = set(divisors(n3))
        least = {}
        cnt = 0
        f = factor(n)
        for _ in range(1200):
            m = random.randint(5, 13)
            style = random.random()
            if style < 0.25:
                B = [random.randrange(n) for _ in range(m)]
            elif style < 0.5:     # few distinct points
                base = random.sample(range(n), random.randint(1, 4))
                B = [random.choice(base) for _ in range(m)]
            elif style < 0.75:    # cosets of prime order, possibly repeated, plus a few points
                B = []
                while len(B) < m - 1:
                    p = random.choice(list(f)); x = random.randrange(n)
                    B += [(x + t * (n // p)) % n for t in range(p)]
                B = B[:m] + [random.randrange(n) for _ in range(max(0, m - len(B)))]
            else:                 # all classes modulo 3 (or the least prime) of chosen sizes, inside a subgroup
                p = min(f)
                base = [random.randrange(n // p) * p for _ in range(2)]
                B = [(random.choice(base) + t * (n // p) * random.choice([0, 1])) % n for t in range(m)]
            c = Counter(B)
            pts = sorted(c); mult = [c[x] for x in pts]
            m = sum(mult)
            g, g3, ok = analyse(n, pts, mult, divs, divs3)
            assert ok
            sh = Fraction(g, 2 ** m); sh3 = Fraction(g3, 2 ** m)
            assert sh > bound(m), ("Proposition H fails", n, pts, mult, sh)
            assert sh3 >= bound3(m)
            if m not in least or sh < least[m][0]:
                least[m] = (sh, pts, mult)
            cnt += 1
        print(f"n = {n}: {cnt} random and structured multisets of 5 to 13 elements: least share of good signings by m: "
              + ", ".join(f"{m}: {least[m][0]}" for m in sorted(least)), flush=True)
