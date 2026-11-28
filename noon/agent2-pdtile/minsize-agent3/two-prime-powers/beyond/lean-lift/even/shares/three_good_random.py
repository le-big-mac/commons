"""Random and structured multisets on moduli prime to 6: the share of signings that are not 3-good (3-bad at some
divisor), exactly, by all signings with the first sign +.  Looks for a share above 3/8.
Structured kinds: (a) uniform random elements; (b) few distinct residues with multiplicities; (c) a full set of
residues modulo a prime factor q, one of them heavy, lifted at random; (d) unions of two such.
usage: three_good_random.py SEED COUNT MMAX N [N ...]"""
import sys, random
from fractions import Fraction
import numpy as np
from minshare import red_matrix
from sympy import factorint
def share(R, blocks, xs):
    m = len(xs)
    E = np.array([[1] + [1 if (s >> i) & 1 else -1 for i in range(m - 1)] for s in range(2 ** (m - 1))], dtype=np.int64).T
    V = (R[:, xs] @ E) % 3
    bad = np.zeros(V.shape[1], dtype=bool)
    for (start, k, d) in blocks: bad |= ~np.any(V[start:start + k] != 0, axis=0)
    return Fraction(int(bad.sum()), 2 ** (m - 1))
def gen(rng, n, m, primes):
    kind = rng.randrange(4)
    if kind == 0: return [rng.randrange(n) for _ in range(m)]
    if kind == 1:
        k = rng.randint(1, min(m, 6)); res = [rng.randrange(n) for _ in range(k)]
        return [rng.choice(res) for _ in range(m)]
    q = rng.choice(primes)
    if q > m: return [rng.randrange(n) for _ in range(m)]
    base = [(t * (n // q) + rng.randrange(q) * 0 + rng.choice([0, 0, rng.randrange(n // q) * q if n // q > 1 else 0])) % n for t in range(q)]
    rest = m - q
    if kind == 2: return base + [base[0]] * rest
    return base + [rng.choice(base + [rng.randrange(n)]) for _ in range(rest)]
if __name__ == '__main__':
    seed, count, mmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    for n in map(int, sys.argv[4:]):
        assert n % 2 and n % 3
        R, blocks = red_matrix(n); primes = sorted(factorint(n))
        worst = {}; above = 0
        for _ in range(count):
            m = rng.randint(3, mmax); xs = gen(rng, n, m, primes); xs = [(x - xs[0]) % n for x in xs]
            s = share(R, blocks, np.array(xs, dtype=np.int64))
            if s > Fraction(3, 8): above += 1; print("ABOVE 3/8:", n, m, sorted(xs), s, flush=True)
            if m not in worst or s > worst[m][0]: worst[m] = (s, sorted(xs))
        print(f"n = {n}  seed {seed}  {count} multisets of 3 to {mmax} elements: above 3/8: {above}; largest share by m: " + "; ".join(f"{m}: {worst[m][0]}" for m in sorted(worst)), flush=True)
