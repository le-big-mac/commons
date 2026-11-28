"""Lemma 1 (two factors) and the ingredients of Lemma 3, by exact counts with multiplicities.
For a modulus d and class sizes (a_c) on Z_d: bad(d) = number of signings bad at d (exact).  Checked:
  L1: bad(d) <= c_a * c_(m-a) * 2^m for every class size a < m that occurs (a = 0 included when a class is empty);
  T1: bad(d) <= 2^(m-k), k = number of occupied classes modulo d/rad(d), and occupied classes <= k * rad(d);
  L3: bad(d)/2^m <= 2 * c_min(a*, m-a*) * c_m with a* the largest class (m >= 2, a* < m)   [Lemma 3 (ii) for t = min(a*, m-a*)].
usage: t_lemma1.py SEED SECONDS"""
import sys, math, random, time
from fractions import Fraction
sys.path.insert(0, '/home/agent3/lean/lift-check/even/limit/referee')
from lib import *

def rad(d):
    r = 1
    for p in (3, 5, 7, 11, 13):
        if d % p == 0: r *= p
    return r
def primes(d): return [p for p in (3, 5, 7, 11, 13) if d % p == 0]

def config(rng, d):
    shape = rng.choice("AAABBCD")
    sizes = {}
    if shape in "ABD":
        for _ in range(rng.randint(1, 3)):
            p = rng.choice(primes(d)); x0 = rng.randrange(d)
            if rng.random() < 0.5 and sizes: x0 = rng.choice(list(sizes))
            for j in range(p): sizes.setdefault((x0 + j * (d // p)) % d, 0)
        if shape == "A":            # one heavy class (sometimes two), the others small
            keys = list(sizes); rng.shuffle(keys)
            for i, kx in enumerate(keys): sizes[kx] = rng.choice((1, 1, 2, 2, 2, 3, 4, 4, 6))
            sizes[keys[0]] = rng.choice((5, 12, 40, 41, 150, 151, 600, 2001))
            if rng.random() < 0.35 and len(keys) > 1: sizes[keys[1]] = rng.choice((5, 12, 30, 31, 60))
        elif shape == "B":          # equal sizes
            s = rng.randint(1, 8)
            for kx in sizes: sizes[kx] = s
        else:                       # two or three large classes of comparable size
            keys = list(sizes); rng.shuffle(keys)
            for kx in keys: sizes[kx] = rng.choice((1, 2, 2, 3))
            big = rng.choice((10, 20, 21, 50, 51))
            for kx in keys[:rng.randint(2, 3)]: sizes[kx] = big + rng.randint(0, 3)
    else:                           # many small classes
        for _ in range(rng.randint(2, 10)): sizes[rng.randrange(d)] = rng.randint(1, 2)
    return shape, sizes

if __name__ == '__main__':
    seed = int(sys.argv[1]); secs = float(sys.argv[2]); rng = random.Random(seed); t0 = time.time()
    MODS = [3, 5, 7, 9, 15, 15, 21, 25, 27, 33, 35, 45, 45, 63, 75, 105, 105, 135, 165, 315]
    n_conf = 0; n_l1 = 0; n_pos = 0; fail = 0
    worst = {}; worst_l3 = Fraction(0); worst_t1 = Fraction(0); eq = 0
    while time.time() - t0 < secs:
        d = rng.choice(MODS); shape, sizes = config(rng, d)
        items = sorted(sizes.items()); m = sum(a for _, a in items)
        vals = sorted(a for _, a in items)
        G = 1
        for a in vals[:-1]: G *= a + 1
        if G > 250000 or m < 2: continue
        cnt, mm = bad_count(d, items, divs=[d]); assert mm == m
        n_conf += 1
        if cnt > 0: n_pos += 1
        # L1
        occ = set(vals) | ({0} if len(items) < d else set())
        for a in occ:
            if a == m: continue
            bound = c(a) * c(m - a) * 2 ** m
            n_l1 += 1
            q = Fraction(cnt) / bound
            if q > 1: fail += 1; print("LEMMA 1 FAILS:", d, items, a, cnt, bound, flush=True)
            if q == 1: eq += 1
            key = (len(primes(d)) > 1, shape)
            if q > worst.get(key, (Fraction(0),))[0]: worst[key] = (q, d, items, a)
        # T1 and Lemma 2
        d0 = d // rad(d); cells = len({b % d0 for b, _ in items})
        if len(items) > cells * rad(d): fail += 1; print("LEMMA 2 (classes per cell) FAILS:", d, items, flush=True)
        q = Fraction(cnt, 2 ** (m - cells))
        if q > 1: fail += 1; print("T1 2^-k FAILS:", d, items, cells, cnt, flush=True)
        worst_t1 = max(worst_t1, q)
        # Lemma 3 (ii)
        astar = vals[-1]
        if astar < m:
            q = Fraction(cnt, 2 ** m) / (2 * c(min(astar, m - astar)) * c(m))
            if q > 1: fail += 1; print("LEMMA 3 (ii) FAILS:", d, items, cnt, flush=True)
            worst_l3 = max(worst_l3, q)
    print(f"seed {seed}: {n_conf} configurations (modulus, class sizes), {n_pos} with a bad signing at d; Lemma 1: {n_l1} cases (configuration, class size a), equal to the bound in {eq}; failures of any check: {fail}")
    for key in sorted(worst):
        q, d, items, a = worst[key]
        print(f"  several primes: {key[0]}, shape {key[1]}: largest count/bound {float(q):.6f} at d = {d}, a = {a}, sizes {items}")
    print(f"  largest P(bad at d)/2^(-k): {float(worst_t1):.6f};  largest P(bad at d)/(2 c_min(a*, m-a*) c_m): {float(worst_l3):.6f}")
