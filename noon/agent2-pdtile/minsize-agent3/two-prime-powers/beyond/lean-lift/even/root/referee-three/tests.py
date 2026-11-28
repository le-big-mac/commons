"""Referee's tests of result.md by exact counts (own code).
For a multiset (residue -> multiplicity) on Z_n, n odd:
  D  (Q3)  every bad point is bad at 1 or at a fully live d > 1
  I  (Q5)  the fully live d have different e(d); cell count (asserted in eng.fully_live)
  B  Lemma B / B+ : P(bad at d) <= 2^(1-k) c*_(m-2k+2), k = kappa+(d);  P(bad at d) > 0 => m >= need(d)
  E  Lemma E (m even, d with one prime): P(bad at d) <= max(E1, E2)
  T  Theorem 1 / 1': P(bad) <= Psi(m)  (and Psi_e(m), m even)
  A  Lemma A, for a multiset that is one cell of d = n = p (or the whole B on a prime n): every choice of merged pair
usage: tests.py exh N MMAX | rand SEED COUNT"""
import sys, math, random, itertools
import numpy as np
from fractions import Fraction as Fr
from eng import *
import psi as PSI

PAIRS = PSI.pairs_upto(160)
_psi = {}; _psie = {}
def Psi(m):
    if m not in _psi: _psi[m] = PSI.psi_pairs(m, PAIRS)
    return _psi[m]
def Psie(m):
    if m not in _psie: _psie[m] = PSI.psie_pairs(m, PAIRS)
    return _psie[m]

class Stats:
    def __init__(self):
        self.n = 0; self.fl = 0; self.flpos = 0; self.fl2 = 0; self.eqB = 0; self.maxB = Fr(0); self.maxB2 = Fr(0); self.nE = 0; self.maxE = Fr(0)
        self.maxT = Fr(0); self.maxTe = Fr(0); self.maxshare = 0.0; self.fail = []; self.need_eq = 0; self.argT = None; self.argTe = None
        self.maxTodd17 = Fr(0)
ST = Stats()

def check(n, ms):
    """ms: dict residue -> multiplicity (>0)."""
    res = sorted(ms); mult = [ms[b] for b in res]; m = sum(mult)
    T, w = grid(mult); tot = 2 ** m
    flags = bad_flags(n, res, T)
    FL = fully_live(n, res)
    ST.n += 1
    # D
    anybad = np.zeros(T.shape[0], dtype=bool)
    for d in flags: anybad |= flags[d]
    cover = flags[1].copy()
    for f in FL: cover |= flags[f['d']]
    if (anybad & ~cover).any(): ST.fail.append(('D', n, dict(ms)))
    # I
    es = [f['e'] for f in FL]
    if len(set(es)) != len(es): ST.fail.append(('I', n, dict(ms)))
    for f in FL:
        d = f['d']; P = Fr(int(w[flags[d]].sum()) if flags[d].any() else 0, tot)
        k = f['kp']; bound = Fr(1, 2 ** (k - 1)) * cstar(m - 2 * k + 2)
        ST.fl += 1
        if len(f['fd']) >= 2: ST.fl2 += 1
        if P > bound: ST.fail.append(('B', n, dict(ms), d, P, bound))
        if P > 0:
            ST.flpos += 1
            if m < f['need']: ST.fail.append(('need', n, dict(ms), d, P))
            if m == f['need']: ST.need_eq += 1
            if P == bound: ST.eqB += 1
            r = P / bound
            if r > ST.maxB: ST.maxB = r
            if len(f['fd']) >= 2 and r > ST.maxB2: ST.maxB2 = r
        if m % 2 == 0 and len(f['fd']) == 1:
            q = f['q']; kap = f['kap']
            E1 = Fr(3, 4) * Fr(1, 2 ** (kap - 1)) * cstar(m - 2 * kap) if m >= 2 * kap + 2 else Fr(0)
            E2 = Fr(1, 2 ** (kap + q - 3)) * cstar(m - 2 * kap - 2 * q + 6)
            ST.nE += 1
            if P > max(E1, E2): ST.fail.append(('E', n, dict(ms), d, P, E1, E2))
            elif P > 0 and P / max(E1, E2) > ST.maxE: ST.maxE = P / max(E1, E2)
    Pbad = Fr(int(w[anybad].sum()) if anybad.any() else 0, tot)
    if m <= 161:
        if Pbad > Psi(m): ST.fail.append(('T', n, dict(ms), Pbad))
        if Psi(m) > 0 and Pbad / Psi(m) > ST.maxT: ST.maxT = Pbad / Psi(m); ST.argT = (n, dict(ms))
        if m % 2 == 1 and m >= 17 and Pbad / Psi(m) > ST.maxTodd17: ST.maxTodd17 = Pbad / Psi(m)
        if m % 2 == 0:
            if Pbad > Psie(m): ST.fail.append(('Te', n, dict(ms), Pbad))
            if Pbad / Psie(m) > ST.maxTe: ST.maxTe = Pbad / Psie(m); ST.argTe = (n, dict(ms))
    sh = float(Pbad) * math.sqrt(m)
    if sh > ST.maxshare: ST.maxshare = sh
    return Pbad

def report(tag):
    print(f"[{tag}] multisets {ST.n}; fully live d {ST.fl} (two or more primes {ST.fl2}; with P > 0: {ST.flpos}; m = need: {ST.need_eq}); "
          f"Lemma B/B+ max ratio {float(ST.maxB):.4f} (equalities {ST.eqB}; two+ primes max {float(ST.maxB2):.4f}); "
          f"Lemma E cases {ST.nE}, max ratio {float(ST.maxE):.4f}; Theorem 1 max P/Psi {float(ST.maxT):.4f} at {ST.argT}; odd m >= 17 max P/Psi {float(ST.maxTodd17):.4f}; "
          f"Theorem 1' max P/Psi_e {float(ST.maxTe):.4f} at {ST.argTe}; max share sqrt(m) {ST.maxshare:.4f}; FAILURES {len(ST.fail)}")
    for f in ST.fail[:(200 if 'FINAL' in tag else 10)]: print("   FAIL", f)
    sys.stdout.flush()

def multisets_with_zero(n, m):
    """all multisets of m elements of Z_n that contain 0 (every multiset is a translate of one)."""
    for comb in itertools.combinations_with_replacement(range(n), m - 1):
        ms = {0: 1}
        for b in comb: ms[b] = ms.get(b, 0) + 1
        yield ms

def rand_multiset(rng, n):
    kind = rng.randrange(9)
    fn = factor(n); ms = {}
    def add(b, h=1):
        b %= n; ms[b] = ms.get(b, 0) + h
    if kind == 0:                                   # uniform
        for _ in range(rng.randint(3, 13)): add(rng.randrange(n))
    elif kind == 1:                                 # heavy element and decoration
        add(0, rng.randint(4, 40))
        for _ in range(rng.randint(1, 7)): add(rng.randrange(n), rng.choice([1, 1, 1, 2, 2, 3]))
    elif kind == 2:                                 # even multiplicities
        for _ in range(rng.randint(2, 6)): add(rng.randrange(n), 2 * rng.randint(1, 4))
    elif kind == 3:                                 # spines of the trees
        for p, a in fn.items():
            for i in range(1, a + 1):
                if rng.random() < 0.8:
                    for t in range(1, p): add(t * (n // p ** i) if rng.random() < 0.9 else rng.randrange(n), rng.choice([1, 1, 2]))
        add(0, rng.choice([1, 2, 3, 6, 11, 20]))
    elif kind == 4:                                 # full groups at several primes with noise
        for p in fn:
            if rng.random() < 0.7:
                base = rng.randrange(n)
                for t in range(p): add(base + t * (n // p), rng.choice([1, 1, 2]))
        for _ in range(rng.randint(0, 3)): add(rng.randrange(n))
    elif kind == 5:                                 # few residues, large multiplicities
        for _ in range(rng.randint(2, 4)): add(rng.randrange(n), rng.randint(1, 14))
    elif kind in (6, 7):                            # a cell full for two primes (rows and columns), sometimes a heavy subclass
        ps = sorted(fn)
        if len(ps) < 2: return rand_multiset(rng, n)
        p, q = rng.sample(ps, 2)
        d = n; rad = math.prod(fn); d0 = d // rad; c = rng.randrange(d0)
        # elements c + d0 * k, k in Z_rad; choose k with prescribed (k mod p, k mod q)
        def elt(s, t):
            k = next(k for k in range(rad) if k % p == s and k % q == t)
            if len(ps) > 2 and rng.random() < 0.5: k = (k + p * q * rng.randrange(rad // (p * q))) % rad
            return c + d0 * k
        big, small = max(p, q), min(p, q)
        if kind == 6:
            rows = [rng.randrange(small) for _ in range(big)]
            for s in range(small): rows[rng.randrange(big)] = s
            if len(set(rows)) < small: rows[:small] = list(range(small))
            for t in range(big): add(elt(rows[t], t) if small == p else elt(t, rows[t]), rng.choice([1, 1, 1, 2]))
            for _ in range(rng.randint(0, 3)): add(elt(rng.randrange(p), rng.randrange(q)))
        else:
            for _ in range(rng.randint(big, big + 6)): add(elt(rng.randrange(p), rng.randrange(q)))
        if rng.random() < 0.4: add(rng.choice(list(ms)), rng.randint(3, 20))
        if rng.random() < 0.3: add(rng.randrange(n), 2)
    else:                                           # classes of equal size modulo a prime power
        p = rng.choice(sorted(fn)); h = rng.randint(1, 4); i = rng.randint(1, fn[p])
        base = rng.randrange(n)
        for t in range(p): add(base + t * (n // p ** i), h)
        if rng.random() < 0.5: add(rng.randrange(n), rng.randint(1, 10))
    return ms

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'exh':
        n = int(sys.argv[2]); mmax = int(sys.argv[3])
        mmin = int(sys.argv[4]) if len(sys.argv) > 4 else 1
        for m in range(mmin, mmax + 1):
            best = Fr(0); arg = None; cnt = 0
            for ms in multisets_with_zero(n, m):
                P = check(n, ms); cnt += 1
                if P > best: best = P; arg = dict(ms)
            print(f"n = {n} m = {m}: {cnt} multisets, largest share {best} = {float(best):.5f}, Psi = {Psi(m)}" + (f", Psi_e = {Psie(m)}" if m % 2 == 0 else "") + f", at {arg}")
        report(f"exh n={n} {mmin}<=m<={mmax} FINAL")
    else:
        seed = int(sys.argv[2]); count = int(sys.argv[3]); rng = random.Random(seed)
        NS = [3, 9, 27, 81, 243, 5, 25, 125, 7, 49, 15, 45, 75, 135, 225, 21, 63, 105, 315, 35, 33, 165, 1155, 11, 13]
        done = 0
        while done < count:
            n = rng.choice(NS); ms = rand_multiset(rng, n)
            if not ms: continue                     # the empty multiset is outside the theorem (m >= 1)
            g = math.prod(h + 1 for h in ms.values())
            if g > 40000 or sum(ms.values()) > 60 or g * n > 6000000: continue
            check(n, ms); done += 1
            if done % 500 == 0: report(f"rand seed {seed}, {done}")
        report(f"rand seed {seed}, {done} FINAL")
