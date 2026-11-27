# t4_G.py -- Theorem G by brute force (all signings, exact).
# usage: t4_G.py exhaust n:mmax ...   every multiset with 0 of 2..mmax elements on n = 2 (mod 4) (or any even n: then only
#                                     those with at most two residues modulo 2^k are tested against the theorem, the others
#                                     only for the existence of a good signing)
#        t4_G.py iff                  "good for B iff eps and eps*tau are both good for B mod n'" for every signing
#        t4_G.py random               larger even m, structured
import sys, random
from itertools import combinations_with_replacement
from rlib import *

def good_shares(E, n):
    # E: N x m; returns integer array N: number of good signings among the 2^(m-1) with first sign +
    N, m = E.shape
    S = 1 << (m - 1)
    good = np.ones((N, S), dtype=bool)
    for d in divisors(n):
        good &= ~batch_bad(E, d)
    return good.sum(axis=1), S

def bound(m):
    return Fraction(1, 2) if m == 3 else Fraction(1, 4) if m == 4 else Fraction(74, 1000)

mode = sys.argv[1]
if mode == 'exhaust':
    for spec in sys.argv[2:]:
        n, mmax = map(int, spec.split(':'))
        k = vp(n, 2); tk = 2 ** k
        assert k >= 1
        for m in range(2, mmax + 1):
            S = 1 << (m - 1)
            phi_max = len(cyclo(n)) - 1
            bs = max(200, min(200000, 30_000_000 // (S * phi_max * max(1, m // 2))))
            least = None; least_any = None; cnt = cnt2 = 0; nogood = 0; exc = 0
            for E in chunks(multisets(n, m, with0=True), bs):
                g, S = good_shares(E, n)
                res = E % tk
                nres = np.array([len(set(r)) for r in res.tolist()]) if k > 1 else None
                two = np.ones(len(E), dtype=bool) if k == 1 else (nres <= 2)
                if m == 2:
                    isexc = (E[:, 0] - E[:, 1]) % tk != 0
                    assert not g[isexc].any(), "an exceptional pair with a good signing"
                    assert (g[~isexc] > 0).all()
                    exc += int(isexc.sum())
                    cnt += len(E)
                    continue
                cnt += len(E); cnt2 += int(two.sum())
                nogood += int((g == 0).sum())
                if two.any():
                    i = int(np.argmin(np.where(two, g, S + 1)))
                    if least is None or Fraction(int(g[i]), S) < least[0]:
                        least = (Fraction(int(g[i]), S), E[i].tolist())
                i = int(np.argmin(g))
                if least_any is None or Fraction(int(g[i]), S) < least_any[0]:
                    least_any = (Fraction(int(g[i]), S), E[i].tolist())
            if m == 2:
                print(f"n = {n} m = 2: all {cnt} pairs with 0: {exc} exceptional, none of them has a good signing; every other pair has one", flush=True)
                continue
            assert nogood == 0, "a multiset without a good signing"
            ok = least is None or (least[0] >= bound(m) if m <= 4 else least[0] > bound(m))
            assert ok, ("Theorem G's share fails", n, m, least)
            if k == 1:
                print(f"n = {n} m = {m}: all {cnt} multisets with 0: each has a good signing; least share of good signings {least[0]} = {float(least[0]):.4f} "
                      f"(Theorem G: {'>= ' if m <= 4 else '> '}{bound(m)}) at {least[1]}", flush=True)
            else:
                print(f"n = {n} m = {m}: all {cnt} multisets with 0: each has a good signing (least share {least_any[0]} at {least_any[1]}); "
                      f"of them {cnt2} with at most two residues modulo {tk}: least share {least[0]} = {float(least[0]):.4f} "
                      f"(Theorem G: {'>= ' if m <= 4 else '> '}{bound(m)}) at {least[1]}", flush=True)

elif mode == 'iff':
    random.seed(5)
    tot = 0
    for n in (6, 10, 12, 18, 20, 24, 30, 36, 40, 42, 60, 72, 84, 90, 120, 180, 210):
        k = vp(n, 2); tk = 2 ** k; nodd = n // tk
        cnt = 0
        for _ in range(600):
            m = random.randint(2, 9)
            u = random.sample(range(tk), random.randint(1, 2))
            if random.random() < 0.5:
                w = [random.randrange(nodd) for _ in range(m)]
            else:
                base = random.sample(range(nodd), min(nodd, 3))
                p = random.choice(list(factor(nodd)))
                w = [(random.choice(base) + random.randrange(p) * (nodd // p)) % nodd for _ in range(m)]
            uu = [random.choice(u) for _ in range(m)]
            # CRT
            B = [next(x for x in range(a, n, tk) if x % nodd == b) for a, b in zip(uu, w)]
            g = good_mask(B, n, half=False)
            g0 = good_mask([b % nodd for b in B], nodd, half=False)
            Sg = signs(m, half=False)
            tau = np.array([1 if a == uu[0] else -1 for a in uu])
            # index of eps*tau: signs() numbers the signings by bits (bit i <-> column m-1-i, 1 = minus)
            flipbits = sum(1 << (m - 1 - c) for c in range(m) if tau[c] == -1)
            idx = np.arange(len(Sg)) ^ flipbits
            assert (Sg[idx] == Sg * tau).all()
            pred = g0 & g0[idx]
            assert (g == pred).all(), (n, B)
            if m == 2:
                assert g.any() == (not is_exceptional(B, n))
            cnt += 1
        tot += cnt
        print(f"n = {n}: {cnt} multisets of 2 to 9 elements with one or two residues modulo {tk}: for every signing, good on Z_n iff eps and eps*tau both good modulo {nodd}: ok", flush=True)
    print("total", tot)

elif mode == 'random':
    random.seed(11)
    for n in (6, 18, 30, 42, 66, 90, 210, 330, 630, 12, 36, 60, 120, 420):
        k = vp(n, 2); tk = 2 ** k; nodd = n // tk
        least = {}
        cnt = 0
        f = factor(nodd)
        for _ in range(500):
            m = random.choice([6, 8, 10, 12, 5, 7, 9, 11])
            u = random.sample(range(tk), 2)
            style = random.random()
            if style < 0.3:
                w = [random.randrange(nodd) for _ in range(m)]
            elif style < 0.6:    # all three classes modulo 3 of even size, few points
                base = random.sample(range(nodd), min(nodd, 3))
                w = []
                for t in range(3):
                    w += [(random.choice(base) * 3 + t * (nodd // 3 if nodd % 9 == 0 else 1)) % nodd] * 2
                w = (w + [random.choice(w) for _ in range(m)])[:m]
            elif style < 0.8:    # cosets
                w = []
                while len(w) < m:
                    p = random.choice(list(f)); x = random.randrange(nodd)
                    w += [(x + t * (nodd // p)) % nodd for t in range(p)]
                w = w[:m]
            else:                # closed under +n/2 in the 2-part: every odd part twice, with both residues
                w = [random.randrange(nodd) for _ in range(m // 2)]
                w = w + w
                w = (w + [0] * m)[:m]
            if style >= 0.8:
                uu = [u[0]] * (m // 2) + [u[1]] * (m - m // 2)
            else:
                uu = [random.choice(u) for _ in range(m)]
            B = [next(x for x in range(a, n, tk) if x % nodd == b) for a, b in zip(uu, w)]
            g = good_mask(B, n)
            sh = Fraction(int(g.sum()), len(g))
            assert sh > bound(m), (n, B, sh)
            if m not in least or sh < least[m]:
                least[m] = sh
            cnt += 1
        print(f"n = {n}: {cnt} structured multisets of 5 to 12 elements with two residues modulo {tk}: least share of good signings by m: "
              + ", ".join(f"{m}: {least[m]}" for m in sorted(least)), flush=True)
