"""Referee's tests, third part: multisets built so that divisors with two or three primes and ranks above 1 are fully live
WITH bad signings (cells that are unions of complete p-gons, pairs, and a few loose elements), all checks of tests.py.
Also heavy families with odd m >= 17 for Theorem 1.   usage: tests2.py gon SEED COUNT | heavy"""
import sys, math, random
from fractions import Fraction as Fr
from eng import *
import tests as TS

def gon_multiset(rng, n):
    fn = factor(n); g = math.prod(fn); d0 = n // g; ms = {}
    def add(b, h=1):
        b %= n; ms[b] = ms.get(b, 0) + h
    ncell = rng.choice([1, 1, 2, 3, 4, 5]) if d0 > 1 else 1
    if d0 > 1 and rng.random() < 0.6:
        # cells whose residues make lower levels live: c = t * d0 / p for t in Z_p (a full group one level up)
        p = rng.choice([p for p in fn if fn[p] >= 2]); base = rng.randrange(d0)
        cs = [(base + t * (d0 // p)) % d0 for t in range(p)]
        if rng.random() < 0.4 and fn[p] >= 3: cs += [(base + t * (d0 // p ** 2)) % d0 for t in range(1, p)]
        cs += [rng.randrange(d0) for _ in range(rng.randint(0, 2))]
    else:
        cs = [rng.randrange(d0) for _ in range(ncell)]
    for c in cs:
        for _ in range(rng.choice([1, 1, 1, 2, 2, 3])):
            kind = rng.random(); k0 = rng.randrange(g)
            if kind < 0.6:
                p = rng.choice(sorted(fn))
                for j in range(p): add(c + d0 * (k0 + j * (g // p)))
            elif kind < 0.85: add(c + d0 * k0, 2)
            else: add(c + d0 * k0, rng.choice([1, 2, 3, 4]))
    if rng.random() < 0.25: add(rng.choice(list(ms)), rng.randint(2, 12))
    return ms

if __name__ == '__main__':
    if sys.argv[1] == 'gon':
        seed = int(sys.argv[2]); count = int(sys.argv[3]); rng = random.Random(seed)
        NS = [15, 21, 35, 45, 75, 135, 225, 63, 147, 315, 105, 165, 495, 675, 525, 1155]
        done = 0
        while done < count:
            n = rng.choice(NS); ms = gon_multiset(rng, n)
            if not ms: continue
            gsz = math.prod(h + 1 for h in ms.values())
            if gsz > 70000 or gsz * n > 12000000 or sum(ms.values()) > 60: continue
            TS.check(n, ms); done += 1
            if done % 500 == 0: TS.report(f"gon seed {seed}, {done}")
        TS.report(f"gon seed {seed}, {done} FINAL")
    else:
        # heavy element with the decorations of the brief, odd and even m, and equal classes
        def lift(conds, n):
            out = {}
            for cond, h in conds:
                b = next(b for b in range(n) if all(b % mo == re for mo, re in cond.items())); out[b] = out.get(b, 0) + h
            return out
        fam = []
        D105 = lift([({3: x, 35: 0}, 1) for x in (1, 2)] + [({5: y, 21: 0}, 1) for y in (1, 2, 3, 4)] + [({7: z, 15: 0}, 1) for z in range(1, 7)], 105)
        D15 = lift([({3: x, 5: 0}, 1) for x in (1, 2)] + [({5: y, 3: 0}, 1) for y in (1, 2, 3, 4)], 15)
        D9 = {1: 2, 2: 2, 3: 2, 6: 2}
        D45 = lift([({9: x, 5: 0}, 2) for x in (1, 2, 3, 6)] + [({9: 0, 5: y}, 2) for y in (1, 2, 3, 4)], 45)
        for h in list(range(1, 50)):
            for n, D in ((3, {1: 1, 2: 1}), (15, D15), (105, D105), (9, D9), (45, D45), (3, {1: 2, 2: 2}), (3, {1: 4, 2: 4}), (9, {1: 1, 2: 1, 3: 1, 6: 1})):
                ms = dict(D); ms[0] = ms.get(0, 0) + h
                if sum(ms.values()) > 60: continue
                P = TS.check(n, ms); m = sum(ms.values())
                fam.append((m, n, float(P) * math.sqrt(m), float(P / TS.Psi(m))))
        for par in (1, 0):
            b = max((x for x in fam if x[0] % 2 == par and x[0] >= 17), key=lambda x: x[3])
            print(f"heavy families, m {'odd' if par else 'even'} >= 17: largest P/Psi {b[3]:.4f} at m = {b[0]} on Z_{b[1]} (share sqrt(m) = {b[2]:.4f})")
        b = max((x for x in fam if x[0] % 2 == 1), key=lambda x: x[2]); print(f"largest share sqrt(m), odd m: {b[2]:.4f} at m = {b[0]} on Z_{b[1]}")
        TS.report("heavy FINAL")
