"""Exact tests of the statements of result.md on random multisets (weights by multiplicity, no floating point).
For each multiset B on Z_n and each divisor d of n:
  (T1) descent: every bad grid point is bad at 1 or at a fully live d > 1;
  (T2) a fully live d is determined by its ranks (two fully live d never have the same ranks);
  (T3) P(bad at d) <= 2^(1-k) c*_(m - 2k + 2) for every fully live d, k = kappa+ (kappa from the ranks, plus 1 if d has two or
       more primes; c*_r = c_r for r >= 1, 1/2 for r <= 0), m >= kappa + 1, and m >= need(d) whenever P(bad at d) > 0
       (need = q + 2 s, and q + 1 for two or more primes with s = 0; q the largest prime, s = max (j_p - 1)(p - 1));
  (T4) P(bad) <= Psi(m); and P(bad) <= Psi_e(m) for even m (Theorem 1');
  (TE) Lemma E: for even m and d a power of one prime, P(bad at d) <= max(E1, E2);
  (T5) [m even] P(bad at d, not bad at 1) for the fully live d of type e = 3 (rank 1, prime 3 only): recorded, largest
       ratio to c_(m-2)/2 printed (not a claim; for the parity refinement).
usage: test_bound.py SEED CASES"""
import sys, random, math
from fractions import Fraction
import numpy as np
from lib import *
from const import pairs, Psi_exact, even_pp
PR = pairs(80)
def Psi(m): return Psi_exact(m, PR)
def need_of(ranks):
    q = max(ranks); s_ = max((j - 1) * (p - 1) for p, j in ranks.items())
    return q + 2 * s_ + (1 if (len(ranks) > 1 and s_ == 0) else 0)
def cstar(r): return c(r) if r >= 1 else Fraction(1, 2)
NS = [3, 9, 27, 81, 243, 15, 45, 75, 135, 225, 21, 63, 105, 315, 35, 165, 1155, 5, 25, 7, 49]
def gen(rng):
    n = rng.choice(NS); kind = rng.randrange(8); f = factor(n)
    if kind >= 6:                                   # a cell full for two primes: random occupied subclasses of Z_p x Z_q
        n = rng.choice([15, 21, 35, 45, 75, 105, 225, 63, 315]); f = factor(n); p, q = rng.sample(sorted(f), 2)
        occ = set()
        if kind == 6:                               # every row and every column occupied, few subclasses
            for s_ in range(p): occ.add((s_, rng.randrange(q)))
            for t_ in range(q):
                if not any(o[1] == t_ for o in occ): occ.add((rng.randrange(p), t_))
            for _ in range(rng.randrange(0, 3)): occ.add((rng.randrange(p), rng.randrange(q)))
        else:                                       # a row and a column, or rows and columns
            for _ in range(rng.randrange(1, 3)):
                s0 = rng.randrange(p); occ |= {(s0, t_) for t_ in range(q)}
            for _ in range(rng.randrange(0, 2)):
                t0 = rng.randrange(q); occ |= {(s_, t0) for s_ in range(p)}
        occ = sorted(occ); rng.shuffle(occ); occ = occ[:13]; items = []
        mult = rng.choice(((2,), (2, 2, 2, 4), (1, 1, 2), (1,), (1, 1, 2, 2, 3, 4))) if len(occ) <= 9 else rng.choice(((2,), (1,), (1, 1, 2)))
        for (s_, t_) in occ:
            cand = [x for x in range(n) if x % p == s_ and x % q == t_]
            flat = [x for x in cand if x % (p ** f[p]) == s_ and x % (q ** f[q]) == t_ and all(x % r_ == 0 for r_ in f if r_ not in (p, q))]
            b = rng.choice(flat) if (flat and rng.random() < 0.6) else rng.choice(cand)
            items.append((b, rng.choice(mult)))
        if rng.random() < 0.4: items[0] = (items[0][0], rng.randrange(3, 12))          # one heavy subclass
        d = {}
        for b, a in items: d[b] = d.get(b, 0) + a
        return n, sorted(d.items())
    if kind == 0:                                   # uniform
        m = rng.randrange(3, 14); el = [rng.randrange(n) for _ in range(m)]; items = [(b, 1) for b in el]
    elif kind == 1:                                 # one heavy element and a decoration
        h = rng.randrange(4, 41); r = rng.randrange(0, 10); items = [(0, h)]
        for _ in range(r):
            p = rng.choice(list(f)); items.append(((n // p ** rng.randrange(1, f[p] + 1)) * rng.randrange(1, p) % n if rng.random() < 0.7 else rng.randrange(n), 1))
    elif kind == 2:                                 # even multiplicities
        k = rng.randrange(2, 8); items = [(rng.randrange(n), 2 * rng.randrange(1, 4)) for _ in range(k)]
    elif kind == 3:                                 # along the spine of each prime: multiples of n / p^i
        items = [(0, rng.randrange(1, 12))]
        for p in f:
            for i in range(1, f[p] + 1):
                for t in range(1, p):
                    if rng.random() < 0.8: items.append(((n // p ** i) * t % n, rng.randrange(1, 3)))
        items = items[:13]
    elif kind == 4:                                 # full groups at several primes, random multiplicities, then noise
        items = [(0, rng.randrange(1, 8))]
        for p in f:
            if rng.random() < 0.8:
                a = rng.randrange(1, 4)
                for t in range(1, p): items.append(((n // p) * t % n, a if rng.random() < 0.8 else rng.randrange(1, 4)))
        for _ in range(rng.randrange(0, 3)): items.append((rng.randrange(n), 1))
        items = items[:14]
    else:                                           # few distinct residues, large multiplicities
        k = rng.randrange(2, 6); pool = [rng.randrange(n) for _ in range(k)]
        items = [(b, rng.randrange(1, 9)) for b in pool]
    # merge equal elements
    d = {}
    for b, a in items: d[b] = d.get(b, 0) + a
    return n, sorted(d.items())
if __name__ == '__main__':
    seed = int(sys.argv[1]); cases = int(sys.argv[2]); rng = random.Random(seed)
    stats = dict(cases=0, fl=0, t3_equal=0, viol=0, maxratio=Fraction(0), maxtot=Fraction(0), flcomp=0, t5=Fraction(0), t5n=0, cpos=0, ceq=0, cmax=Fraction(0), needpos=0, needeq=0, en=0, eeq=0, emax=Fraction(0), t4e=0)
    ex_ratio = None; ex_tot = None; ex_t5 = None; ex_c = None
    for _ in range(cases):
        n, items = gen(rng)
        if math.prod(a + 1 for _, a in items) > 300_000 or sum(a for _, a in items) < 3: continue
        S, W, m = grid(items)
        elems = [b for b, _ in items]; tot = 2 ** m
        bad1 = bad_mask(1, items, S); anybad = bad1.copy(); covered = bad1.copy(); seen = {}
        for d in divisors(n):
            if d == 1: continue
            bd = bad_mask(d, items, S); anybad |= bd
            ranks = fully_live(d, elems)
            if ranks is None: continue
            key = tuple(sorted(ranks.items()))
            if key in seen: stats['viol'] += 1; print("T2 VIOLATION", n, items, d, seen[key])
            seen[key] = d
            covered |= bd; stats['fl'] += 1; stats['flcomp'] += len(ranks) > 1
            k0 = kappa(ranks); k = k0 + (len(ranks) > 1); p = Fraction(int(W[bd].sum()), tot); bound = Fraction(1, 2 ** (k - 1)) * cstar(m - 2 * k + 2)
            if m < k0 + 1: stats['viol'] += 1; print("T3 VIOLATION (m < kappa + 1)", n, items, d, ranks)
            if p > 0:
                stats['needpos'] += 1; stats['needeq'] += m == need_of(ranks)
                if m < need_of(ranks): stats['viol'] += 1; print("T3 VIOLATION (P > 0 and m < need)", n, items, d, ranks)
            if m % 2 == 0 and len(ranks) == 1:              # Lemma E
                q_ = max(ranks); be = even_pp(m, q_, k0); stats['en'] += 1; stats['eeq'] += p == be
                if p > be: stats['viol'] += 1; print("LEMMA E VIOLATION", n, items, d, ranks, p, be)
                if be > 0 and p / be > stats['emax']: stats['emax'] = p / be
            if len(ranks) > 1:
                stats['cpos'] += p > 0
                if p == bound: stats['ceq'] += 1
                if p / bound > stats['cmax']: stats['cmax'] = p / bound; ex_c = (n, items, d, ranks, str(p), str(bound))
            if p > bound: stats['viol'] += 1; print("T3 VIOLATION", n, items, d, ranks, p, bound)
            if p == bound: stats['t3_equal'] += 1
            if bound > 0 and p / bound > stats['maxratio']: stats['maxratio'] = p / bound; ex_ratio = (n, items, d, ranks, str(p), str(bound))
            if m % 2 == 0 and key == ((3, 1),):
                q = Fraction(int(W[bd & ~bad1].sum()), tot) / (c(m - 2) / 2); stats['t5n'] += 1
                if q > stats['t5']: stats['t5'] = q; ex_t5 = (n, items, d, str(q))
        if (anybad & ~covered).any(): stats['viol'] += 1; print("T1 VIOLATION", n, items)
        pb = Fraction(int(W[anybad].sum()), tot)
        if pb > Psi(m): stats['viol'] += 1; print("T4 VIOLATION", n, items, pb, Psi(m))
        if m % 2 == 0 and pb > Psi_exact(m, PR, parity=True): stats['viol'] += 1; stats['t4e'] += 1; print("T4e VIOLATION", n, items, pb)
        r = pb * Fraction(math.isqrt(m * 10 ** 12), 10 ** 6)
        if r > stats['maxtot']: stats['maxtot'] = r; ex_tot = (n, items, m, str(pb))
        stats['cases'] += 1
    print(f"seed {seed}: multisets tested {stats['cases']}; fully live divisors met {stats['fl']} (with two or more primes: {stats['flcomp']}); "
          f"violations {stats['viol']}; T3 with equality {stats['t3_equal']}; largest P(bad at d)/bound {float(stats['maxratio']):.4f} at {ex_ratio}; "
          f"largest P(bad) sqrt(m) {float(stats['maxtot']):.4f} at {ex_tot}; T5 cases {stats['t5n']}, largest ratio {float(stats['t5']):.4f} at {ex_t5}; "
          f"divisors with two or more primes: P(bad at d) > 0 in {stats['cpos']}, equal to the bound in {stats['ceq']}, largest ratio {float(stats['cmax']):.4f} at {ex_c}; "
          f"fully live d with P(bad at d) > 0: {stats['needpos']}, all with m >= need(d), {stats['needeq']} with m = need(d); "
          f"Lemma E (m even, d a power of one prime): {stats['en']} divisors, equality {stats['eeq']}, largest ratio {float(stats['emax']):.4f}; T4e violations {stats['t4e']}")
