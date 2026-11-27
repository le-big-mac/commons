# t10_round2.py -- second look: two statements added in the revision, tested with all signings (exact).
#  C : Corollary C: share of 3-good >= rho_2 - (L + 1) * sum over the live e' > 1 of 2^(-mu(e'*)),
#      L = number of live levels of the 2-tree, e'* = prod q^(number of live levels of q up to v_q(e')).
#  S2: two residues modulo 2^k: the 3-good signings on Z_{n_3} are those of the multiset on Z_{2n''} with the residues at 0, 1.
import sys, random
from rlib import *

random.seed(808)

def crt(u, w, tk, nodd):
    inv = pow(tk, -1, nodd) if nodd > 1 else 0
    return (u + tk * (((w - u) * inv) % nodd)) % (tk * nodd)

def rho2_mask(B, k):
    g = np.ones(1 << (len(B) - 1), dtype=bool)
    for j in range(k + 1):
        g &= ~bad3_at(B, 2 ** j)
    return g

tot = 0; slack0 = 0; minslack = None
for n3 in (20, 40, 80, 100, 140, 280, 200, 160):
    k = vp(n3, 2); tk = 2 ** k; nodd = n3 >> k
    f = factor(nodd)
    cnt = 0
    for _ in range(400):
        m = random.randint(3, 10)
        # make live levels likely: a full group of some prime, then random or repeated points
        q = random.choice(list(f)); base = random.randrange(nodd)
        ws = [(base + t * (nodd // q)) % nodd for t in range(q)] if random.random() < 0.7 and q <= m else []
        while len(ws) < m:
            ws.append(random.choice(ws) if ws and random.random() < 0.4 else random.randrange(nodd))
        ws = ws[:m]
        t = random.random()
        if t < 0.4:
            us = [random.randrange(tk) for _ in range(m)]
        elif t < 0.7:
            vals = random.sample(range(tk), min(tk, random.randint(1, 3)))
            us = [random.choice(vals) for _ in range(m)]
        else:
            a = random.randrange(tk)
            us = [(a + 2 ** random.randrange(k)) % tk if random.random() < 0.5 else a for _ in range(m)]
        B = [crt(u, w, tk, nodd) for u, w in zip(us, ws)]
        S = 1 << (m - 1)
        g3 = good3_mask(B, n3)
        rho = Fraction(int(rho2_mask(B, k).sum()), S)
        L = len(live_levels(B, 2, k))
        lv = {p: live_levels(B, p, a) for p, a in f.items()}
        tsum = Fraction(0)
        for e in divisors(nodd):
            if e == 1:
                continue
            fe = factor(e)
            if all(i in lv[p] for p, i in fe.items()):
                mu = max(sum(1 for x in lv[p] if x <= i) * (p - 1) for p, i in fe.items())
                tsum += Fraction(1, 2 ** mu)
        sl = Fraction(int(g3.sum()), S) - (rho - (L + 1) * tsum)
        assert sl >= 0, ("Corollary C fails", n3, B)
        slack0 += (sl == 0)
        if minslack is None or sl < minslack:
            minslack = sl
        cnt += 1; tot += 1
    print(f"C: n_3 = {n3}: {cnt} multisets of 3 to 10 elements, all signings: share of 3-good >= rho_2 - (L+1) * sum over live e' of 2^-mu: holds", flush=True)
print(f"C: total {tot}; least slack {minslack}; slack 0 in {slack0} cases")

tot = 0
for k in (2, 3, 4):
    tk = 2 ** k
    for nodd in (5, 7, 25, 35):
        n3 = tk * nodd
        for _ in range(120):
            m = random.randint(2, 9)
            u = random.sample(range(tk), 2)
            q = random.choice(list(factor(nodd))); base = random.randrange(nodd)
            ws = [(base + t * (nodd // q)) % nodd for t in range(q)] if random.random() < 0.6 and q <= m else []
            while len(ws) < m:
                ws.append(random.choice(ws) if ws and random.random() < 0.4 else random.randrange(nodd))
            ws = ws[:m]
            us = [random.choice(u) for _ in range(m)]
            B = [crt(a, w, tk, nodd) for a, w in zip(us, ws)]
            B2 = [crt(0 if a == u[0] else 1, w, 2, nodd) for a, w in zip(us, ws)]
            assert (good3_mask(B, n3) == good3_mask(B2, 2 * nodd)).all(), ("S2 fails", n3, B)
            tot += 1
print(f"S2: {tot} multisets of 2 to 9 elements with one or two residues modulo 2^k, k = 2, 3, 4, n'' = 5, 7, 25, 35: "
      f"the 3-good signings on Z_(n_3) are exactly those of the multiset on Z_(2n'') with the residues at 0 and 1")
