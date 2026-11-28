"""Odd moduli: the share of BAD signings (signed mask divisible by Phi_e for some e | n, e = 1 included), exactly, by all
signings with the first sign +, for random and structured multisets.  Looks for the largest share for each size m and
for anything above 3/8.
Structured kinds: uniform; few residues with multiplicities; for a prime q | n a full set of residues modulo q with
one heavy class, lifted so that the other primes see chosen patterns; unions.
usage: bad_random.py SEED COUNT MMIN MMAX N [N ...]"""
import sys, random
from fractions import Fraction
import numpy as np
from minshare import red_matrix
from sympy import factorint
from sympy.ntheory.modular import crt
def share(R, blocks, xs):
    m = len(xs)
    E = np.array([[1] + [1 if (s >> i) & 1 else -1 for i in range(m - 1)] for s in range(2 ** (m - 1))], dtype=np.int64).T
    V = R[:, xs] @ E
    bad = np.zeros(V.shape[1], dtype=bool)
    for (start, k, d) in blocks: bad |= ~np.any(V[start:start + k] != 0, axis=0)
    return Fraction(int(bad.sum()), 2 ** (m - 1))
def heavy_pattern(rng, q, m):
    # residues modulo q for m marks: all q residues occupied if m >= q, one class heavy; else random
    if m < q: return [rng.randrange(q) for _ in range(m)]
    kind = rng.randrange(3)
    if kind == 0: return list(range(q)) + [0] * (m - q)
    if kind == 1: return list(range(q)) + [rng.randrange(2) for _ in range(m - q)]
    return [rng.randrange(q) for _ in range(m)]
def gen(rng, n, m, pps):
    kind = rng.randrange(5)
    if kind == 0: return [rng.randrange(n) for _ in range(m)]
    if kind == 1:
        k = rng.randint(1, min(m, 5)); res = [rng.randrange(n) for _ in range(k)]
        return [rng.choice(res) for _ in range(m)]
    # CRT of patterns modulo each prime power
    cols = []
    for (q, a) in pps:
        pat = heavy_pattern(rng, q, m); rng.shuffle(pat)
        if a > 1: pat = [r + q * rng.choice([0, 0, rng.randrange(q ** (a - 1))]) for r in pat]
        cols.append(pat)
    mods = [q ** a for (q, a) in pps]
    return [int(crt(mods, [c[i] for c in cols])[0]) for i in range(m)]
if __name__ == '__main__':
    seed, count, mmin, mmax = (int(v) for v in sys.argv[1:5])
    rng = random.Random(seed)
    for n in map(int, sys.argv[5:]):
        assert n % 2
        R, blocks = red_matrix(n); pps = sorted(factorint(n).items())
        worst = {}; above = 0
        for _ in range(count):
            m = rng.randint(mmin, mmax); xs = gen(rng, n, m, pps); xs = [(x - xs[0]) % n for x in xs]
            s = share(R, blocks, np.array(xs, dtype=np.int64))
            if s > Fraction(3, 8): above += 1; print("ABOVE 3/8:", n, m, sorted(xs), s, flush=True)
            if m not in worst or s > worst[m][0]: worst[m] = (s, sorted(xs))
        print(f"n = {n}  seed {seed}  {count} multisets of {mmin} to {mmax} elements: above 3/8: {above}; largest bad share by m: " + "; ".join(f"{m}: {worst[m][0]} = {float(worst[m][0]):.4f}" for m in sorted(worst)), flush=True)
        for m in sorted(worst): print(f"    m = {m}: {worst[m][1]}", flush=True)
