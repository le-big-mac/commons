"""An attempt to break the count: local search for multisets with FEW good signings (all signings enumerated).

Start from a multiset of m elements on Z_n, change one element at a time, keep the change if the fraction of
good signings does not go up.  Reported: the least fraction of good signings found, the multiset, its contracted
group, and the lower bound 1 - c_m - sum over d | n_flat, d > 1 of 2^(-mu(d)) of the result file for it (may be
negative for even m between 14 and 24, where the result file sharpens the level d = 3).

usage: adversary.py n m starts steps seed
"""
import sys
import random
from fractions import Fraction as Fr
import numpy as np
from lib4 import divisors, mu, all_signs, bad_table, contract, c_even
from test_levels import gen_full, gen_coset, gen_random


def good_fraction(B, n, E):
    bad = np.zeros(E.shape[0], dtype=bool)
    for d, b in bad_table(B, n, E).items():
        bad |= b
    return 1 - Fr(int(bad.sum()), E.shape[0])


def main():
    n = int(sys.argv[1]); m = int(sys.argv[2]); starts = int(sys.argv[3]); steps = int(sys.argv[4]); seed = int(sys.argv[5])
    rng = random.Random(seed)
    E = all_signs(m)
    best = Fr(1); best_B = None
    for s in range(starts):
        k = rng.choice(['full', 'coset', 'random'])
        B = {'random': gen_random, 'full': gen_full, 'coset': gen_coset}[k](n, m, rng) or gen_random(n, m, rng)
        g = good_fraction(B, n, E)
        for _ in range(steps):
            B2 = list(B)
            j = rng.randrange(m)
            if rng.random() < 0.5:
                B2[j] = rng.randrange(n)
            else:      # move by a subgroup element, or copy another element
                d = rng.choice(divisors(n))
                B2[j] = (rng.choice(B) + rng.randrange(d) * (n // d)) % n
            g2 = good_fraction(B2, n, E)
            if g2 <= g:
                B, g = B2, g2
        if g < best:
            best, best_B = g, sorted(B)
    Bf, nf = contract(best_B, n)
    bound = 1 - c_even(m) - sum(Fr(1, 2 ** mu(d)) for d in divisors(nf) if d > 1)
    print(f"n={n} m={m} starts={starts} steps={steps} seed={seed}: least fraction of good signings found = {best} = {float(best):.4f}; "
          f"multiset {best_B}; n_flat = {nf}; proved lower bound for it {float(bound):.4f}")


main()
