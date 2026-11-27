"""Referee's attempt to break Theorem P by descent: start from a random function, change one or two cells at a time,
keep the change when the share of good patterns does not rise.  All (normalised) patterns are enumerated at each step.
Also Remark (1): the product of vectors (1, 1, 0, ..., 0) has exactly the share 2^-k.
usage: thmP_attack.py SEED
"""
import sys, time
import numpy as np
from fractions import Fraction as Fr
from boxtools import all_levels, pattern_array, fraction_good

def descend(rng, sides, q, steps, restarts, PA, levels):
    k = len(sides); best_all = None; hits = 0
    for r in range(restarts):
        if q:
            g = rng.integers(0, q, size=sides) * (rng.random(sides) < rng.choice([0.2, 0.5, 1.0]))
        else:
            g = rng.integers(-1, 2, size=sides)
        if not g.any(): g[(0,) * k] = 1
        cur = fraction_good(g, levels, [q], PA)[q][0]
        for _ in range(steps):
            h = g.copy()
            for _c in range(rng.integers(1, 3)):
                idx = tuple(rng.integers(0, n) for n in sides)
                h[idx] = rng.integers(0, q) if q else rng.integers(-2, 3)
            if not (h % q if q else h).any(): continue
            c = fraction_good(h, levels, [q], PA)[q][0]
            if c <= cur: g, cur = h, c
        fr = Fr(cur, PA.shape[0])
        if best_all is None or fr < best_all[0]: best_all = (fr, g.copy())
        if fr == Fr(1, 2 ** k): hits += 1
        assert fr >= Fr(1, 2 ** k), ('VIOLATION of Theorem P', sides, q, g.tolist(), fr)
    return best_all, hits

if __name__ == '__main__':
    rng = np.random.default_rng(int(sys.argv[1]))
    # Remark (1)
    for sides in [(3, 5), (5, 7), (3, 5, 7), (5, 5, 7)]:
        k = len(sides); g = np.ones(sides, dtype=np.int64)
        for j, n in enumerate(sides):
            v = np.zeros(n, dtype=np.int64); v[:2] = 1
            sh = [1] * k; sh[j] = n; g = g * v.reshape(sh)
        PA, _ = pattern_array(sides)
        c, tot = fraction_good(g, all_levels(k), [None], PA)[None]
        print(f'Remark (1): box {sides}, product of (1, 1, 0, ..): share of good patterns {Fr(c, tot)} (2^-k = {Fr(1, 2 ** k)})')
        assert Fr(c, tot) == Fr(1, 2 ** k)
    plan = [((3, 5), 7, 1500, 30), ((3, 5), 11, 1500, 30), ((3, 5), None, 1500, 30), ((5, 5), 3, 1200, 20), ((3, 7), 5, 1200, 20),
            ((5, 7), 3, 500, 8), ((3, 5, 7), None, 250, 4), ((3, 5, 7), 11, 250, 4)]
    for sides, q, steps, restarts in plan:
        t0 = time.time(); k = len(sides); PA, _ = pattern_array(sides)
        (fr, g), hits = descend(rng, sides, q, steps, restarts, PA, all_levels(k))
        print(f'descent on box {sides}, field {"Q" if q is None else "F_%d" % q}: {restarts} starts of {steps} steps: least share reached {fr} '
              f'(bound {Fr(1, 2 ** k)}), reached the bound in {hits} starts, never below; a minimiser: {g.tolist()}  [{time.time() - t0:.0f} s]', flush=True)
