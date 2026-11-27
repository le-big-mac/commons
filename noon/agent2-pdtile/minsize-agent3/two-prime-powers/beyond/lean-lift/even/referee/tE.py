# Odd m on moduli 2 * 3 * 5 * q with q = 13 (m = 13) and q = 17 (m = 17), where the q-tree can be live:
# all signings, exact.  Checks: share of bad signings <= sum over the live dangerous e > 1 of 2^(1 - D_e) (< 1).
# (The text lists these n as open; the count of Theorem D (iii) with Pi = {3, 5, q} gives 0.99980 for q = 13 and
# 0.98660 for q = 17: tW2.py.)
import sys, random
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from rlib import *

def run(n, m, count, rnd):
    k, npr = split2(n)
    fac = factorint(npr)
    q = max(fac)
    worst_good = F(1); worst_first = F(0); nlive_q = 0; nall3 = 0
    for trial in range(count):
        t = rnd.random()
        # one element in every class modulo q (so the q-tree is live); the other residues at random or structured
        B = []
        for r in range(q):
            while True:
                x = rnd.randrange(n)
                if x % q == r:
                    if t < 0.4 or (t < 0.7 and x % 15 == r % 15) or (t >= 0.7 and x % 2 == (r % 2 if t < 0.85 else 0)):
                        B.append(x); break
        B = B[:m]
        W = [x % npr for x in B]
        lv = {p: live_levels(W, p, a) for p, a in fac.items()}
        nlive_q += bool(lv[q])
        nall3 += all(lv[p] for p in fac)
        S = signmat(len(B))
        anyb = np.zeros(1 << len(B), dtype=bool)
        bad_e = {}
        for d in divisors(n):
            T = table(n, d)
            V = S @ T[np.array(B), :]
            b = ~V.any(axis=1)
            anyb |= b
            e = d // (2 if d % 2 == 0 else 1)
            bad_e[e] = bad_e.get(e, np.zeros(1 << len(B), dtype=bool)) | b
        first = F(0)
        for e in divisors(npr):
            if e == 1:
                assert not bad_e[1].any()          # m odd
                continue
            live = all(i in lv[p] for p, i in factorint(e).items())
            pw = powers_mod2(e)
            s = 0
            for w in W:
                s ^= pw[w % e]
            if live and s == 0:
                De = D_rank(W, e)
                assert int(bad_e[e].sum()) * 2 ** De <= 2 ** (len(B) + 1)
                first += F(2, 2 ** De)
            elif live:
                assert not bad_e[e].any()
        bad = F(int(anyb.sum()), 1 << len(B))
        assert bad <= first < 1, (n, B, bad, first)
        worst_good = min(worst_good, 1 - bad)
        worst_first = max(worst_first, first)
    print("n = %d, m = %d: %d multisets with one element in every class modulo %d (q-tree live: %d; 3-, 5- and q-tree all live: %d):"
          " share bad <= first-order sum over live dangerous e, largest such sum %s = %.4f; least share of good signings %s = %.4f"
          % (n, m, count, q, nlive_q, nall3, worst_first, float(worst_first), worst_good, float(worst_good)), flush=True)

rnd = random.Random(21)
run(390, 13, 400, rnd)
run(510, 17, 12, rnd)
print("OK")
