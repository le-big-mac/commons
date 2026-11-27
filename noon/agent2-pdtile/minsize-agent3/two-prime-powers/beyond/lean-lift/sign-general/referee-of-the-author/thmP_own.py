"""Referee's tests of Theorem P (sign-general-result.md, section 3): on a box with odd sides n_1 >= 3, n_j >= 2j,
over Q or F_q (q an odd prime dividing no side), every nonzero function has at least the fraction 2^-k of the product
patterns good at every level.  All patterns are enumerated (normalised: see boxtools.pattern_array), exact integers.

usage: thmP_own.py all01          every nonzero 0/1 function on 3x5; Q, F_7, F_11, F_13
       thmP_own.py pm1 PART PARTS every nonzero function with values in {0, 1, -1} on 3x5 (up to sign), in PARTS parts; Q, F_7, F_11
       thmP_own.py field SEED     functions with arbitrary values in F_q, random and structured, several boxes
       thmP_own.py three SEED     box 3x5x7 (and 3x5x9, 5x5x7 which also satisfy the hypothesis)
"""
import sys, time
import numpy as np
from fractions import Fraction as Fr
from itertools import product
from boxtools import all_levels, pattern_array, good_batch_fields, fraction_good

def run_all01():
    sides = (3, 5); levels = all_levels(2); fields = [None, 7, 11, 13]
    PA, _ = pattern_array(sides)
    cells = 15
    idx = np.arange(1, 2 ** cells, dtype=np.int64)
    G = ((idx[:, None] >> np.arange(cells)[None, :]) & 1).astype(np.int64).reshape(-1, 3, 5)
    cnt = {q: np.zeros(G.shape[0], dtype=np.int64) for q in fields}
    for i in range(PA.shape[0]):
        ok = good_batch_fields(G * PA[i][None].astype(np.int64), levels, fields)
        for q in fields: cnt[q] += ok[q]
    npat = PA.shape[0]
    for q in fields:
        mn = int(cnt[q].min())
        print(f'3x5, all {G.shape[0]} nonzero 0/1 functions, field {"Q" if q is None else "F_%d" % q}: least fraction of good patterns '
              f'{Fr(mn, npat)} (bound 1/4), attained by {int((cnt[q] == mn).sum())} functions; none with no good pattern: {mn > 0}')

def run_pm1(part, parts):
    """the 122 admissible first rows are dealt into `parts` parts; this run does part `part` (0-based)."""
    sides = (3, 5); levels = all_levels(2); fields = [None, 7, 11]
    PA, _ = pattern_array(sides); npat = PA.shape[0]
    tail = np.array(list(product((0, 1, -1), repeat=10)), dtype=np.int64)        # 59049 x 10
    least = {q: npat for q in fields}; nfun = 0; nmin = {q: 0 for q in fields}
    t0 = time.time(); ih = -1
    for head in product((0, 1, -1), repeat=5):
        # up to the sign of the function: the first nonzero entry of the head is +1, or the head is 0
        nz = [h for h in head if h != 0]
        if nz and nz[0] == -1: continue
        ih += 1
        if ih % parts != part: continue
        G = np.concatenate([np.tile(np.array(head, dtype=np.int64), (tail.shape[0], 1)), tail], axis=1).reshape(-1, 3, 5)
        keep = G.reshape(G.shape[0], -1).any(axis=1)
        G = G[keep]
        cnt = {q: np.zeros(G.shape[0], dtype=np.int64) for q in fields}
        for i in range(npat):
            ok = good_batch_fields(G * PA[i][None].astype(np.int64), levels, fields)
            for q in fields: cnt[q] += ok[q]
        nfun += G.shape[0]
        for q in fields:
            mn = int(cnt[q].min())
            if mn < least[q]: least[q] = mn; nmin[q] = 0
            if mn == least[q]: nmin[q] += int((cnt[q] == mn).sum())
    for q in fields:
        print(f'3x5, functions with values in {{0, 1, -1}}, part {part + 1} of {parts} ({nfun} functions; over all parts: one of each pair g, -g '
              f'when the first row is not 0, both when it is), field {"Q" if q is None else "F_%d" % q}: least fraction {Fr(least[q], npat)} '
              f'(bound 1/4), attained {nmin[q]} times')
    print(f'   time {time.time() - t0:.0f} s')

def structured(rng, sides, q, kind):
    """a function with values in {0..q-1} (q a prime) or small integers (q None)."""
    k = len(sides); hi = q if q else 5
    def rv(shape):
        return rng.integers(0, hi, size=shape) if q else rng.integers(-3, 4, size=shape)
    if kind == 'random':
        g = rv(sides)
    elif kind == 'sparse':
        g = rv(sides) * (rng.random(sides) < rng.choice([0.1, 0.2, 0.35]))
    elif kind == 'zero_one':
        g = (rng.random(sides) < rng.choice([0.15, 0.3, 0.5, 0.8])).astype(np.int64)
    elif kind == 'product':            # g_1 (x) ... (x) g_k
        g = np.ones(sides, dtype=np.int64)
        for j in range(k):
            sh = [1] * k; sh[j] = sides[j]
            v = rv(sides[j])
            if rng.random() < 0.5:     # vectors of the extremal kind (1, 1, 0, ..) and (c, .., c)
                v = np.zeros(sides[j], dtype=np.int64); m = rng.integers(1, sides[j] + 1); v[rng.permutation(sides[j])[:m]] = 1
            g = g * v.reshape(sh)
    elif kind == 'slices_pm':          # slices along one axis all equal up to sign and 0: g(v, y) = a_v u(y), a in {0, 1, -1}
        ax = rng.integers(0, k); other = [sides[j] for j in range(k) if j != ax]
        u = rv(other); a = rng.choice([1, -1, 0], size=sides[ax], p=[0.45, 0.45, 0.1])
        g = np.moveaxis(a.reshape([-1] + [1] * (k - 1)) * u[None], 0, ax)
    elif kind == 'rank2':              # slices along one axis in the span of two functions
        ax = rng.integers(0, k); other = [sides[j] for j in range(k) if j != ax]
        u1, u2 = rv(other), rv(other); a1, a2 = rv(sides[ax]), rv(sides[ax])
        g = np.moveaxis(a1.reshape([-1] + [1] * (k - 1)) * u1[None] + a2.reshape([-1] + [1] * (k - 1)) * u2[None], 0, ax)
    elif kind == 'line':               # support on a line parallel to an axis
        g = np.zeros(sides, dtype=np.int64); ax = rng.integers(0, k)
        ix = [rng.integers(0, sides[j]) for j in range(k)]; ix[ax] = slice(None)
        g[tuple(ix)] = rv(sides[ax])
    elif kind == 'additive':           # a sum of functions each missing a coordinate, plus a few cells
        g = np.zeros(sides, dtype=np.int64)
        for j in range(k):
            sh = list(sides); sh[j] = 1
            g = g + rv(sh)
        for _ in range(rng.integers(1, 4)):
            g[tuple(rng.integers(0, sides[j]) for j in range(k))] += rng.integers(1, hi)
    elif kind == 'two_products':
        g = structured(rng, sides, q, 'product') + structured(rng, sides, q, 'product')
    g = np.asarray(g, dtype=np.int64)
    if q: g = g % q
    return g

KINDS = ['random', 'sparse', 'zero_one', 'product', 'slices_pm', 'rank2', 'line', 'additive', 'two_products']

def run_boxes(boxes, seed, per_kind):
    rng = np.random.default_rng(seed)
    for sides, fields in boxes:
        k = len(sides); levels = all_levels(k); PA, _ = pattern_array(sides); npat = PA.shape[0]
        t0 = time.time()
        for q in fields:
            worst = {}
            for kind in KINDS:
                mn = npat; nf = 0
                for _ in range(per_kind):
                    g = structured(rng, sides, q, kind)
                    if not (g % q if q else g).any(): continue
                    nf += 1
                    c, _n = fraction_good(g, levels, [q], PA)[q]
                    mn = min(mn, c)
                worst[kind] = (Fr(mn, npat), nf)
            overall = min(v[0] for v in worst.values())
            flag = 'OK' if overall >= Fr(1, 2 ** k) else 'VIOLATION'
            print(f'box {sides}, field {"Q" if q is None else "F_%d" % q}: least fraction {overall} against 2^-k = {Fr(1, 2 ** k)}: {flag}; by kind: '
                  + ', '.join(f'{kd} {v[0]} ({v[1]})' for kd, v in worst.items()))
        print(f'   [{time.time() - t0:.0f} s]', flush=True)

if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'all01': run_all01()
    elif what == 'pm1': run_pm1(int(sys.argv[2]), int(sys.argv[3]))
    elif what == 'field':
        seed = int(sys.argv[2])
        run_boxes([((3, 5), [None, 7, 11, 13, 17]), ((5, 3), [7, 11]), ((5, 5), [None, 3, 7]), ((3, 7), [None, 5, 11]),
                   ((5, 7), [None, 3, 11]), ((3, 9), [5, 7]), ((7, 7), [3, 5])], seed, 250)
    elif what == 'three':
        seed = int(sys.argv[2])
        run_boxes([((3, 5, 7), [None, 11, 13]), ((7, 3, 5), [11]), ((5, 5, 7), [3])], seed, 60)
