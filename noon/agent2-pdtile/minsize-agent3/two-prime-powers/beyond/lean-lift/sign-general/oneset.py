# oneset.py -- one set B in a box: all signings by enumeration; which are good (every level has a nonzero cube sum).
# Independent of grid.c (numpy, a different organisation).  Exact (int64, tiny values).
import itertools, numpy as np
def analyse(sides, B, name):
    k = len(sides)
    cells = list(itertools.product(*[range(s) for s in sides]))
    # basis: j in the box; level(j) = {i : j_i >= 1}; entry = cube sum with corners 0 / j_i on the level
    def w(x):
        v = []
        for j in cells:
            c = 1
            for i in range(k):
                if j[i] >= 1:
                    c *= 1 if x[i] == j[i] else (-1 if x[i] == 0 else 0)
            v.append(c)
        return v
    W = np.array([w(x) for x in B], dtype=np.int64)            # |B| x |box|
    lev = np.array([sum(1 << i for i in range(k) if j[i] >= 1) for j in cells])
    nb = len(B)
    good = {}
    for bits in range(1 << (nb - 1)):                           # first sign +
        s = np.array([1] + [-1 if bits >> (t - 1) & 1 else 1 for t in range(1, nb)], dtype=np.int64)
        I = s @ W
        ok = all(np.any(I[lev == L] != 0) for L in range(1 << k))
        good[bits] = ok
    def turned(bits):
        t = bin(bits).count("1"); return min(t, nb - t)
    ngood = sum(good.values())
    allplus = good[0]
    singles = [good[1 << (t - 1)] for t in range(1, nb)] + [good[(1 << (nb - 1)) - 1]]  # last: turn element 0 = turn all others
    mint = min(turned(b) for b, g in good.items() if g) if ngood else None
    print("%s: box %s, |B| = %d; good signings %d of %d (first sign +); all + good: %s; single turns that are good: %d of %d; least number of turns: %s"
          % (name, sides, nb, ngood, 1 << (nb - 1), allplus, sum(singles), nb, mint))
# (a) the example found by grid.c
analyse([3, 3, 5], [(0,0,0), (1,0,1), (2,0,2), (0,1,3), (0,2,4)], "five points in 3x3x5")
# (b) the mechanism of strong_cyclic.py in miniature: three coordinates of size 3 (sum of 1/3 = 1), r = 7;
#     all points with exactly one zero among the first three coordinates (12 points), the origin twice; 14 = 2*7
pts = [x for x in itertools.product(range(3), repeat=3) if sum(1 for c in x if c == 0) == 1]
lst = [(0,0,0), (0,0,0)] + pts
B = [x + (t % 7,) for t, x in enumerate(lst)]
assert len(set(B)) == len(B)
analyse([3, 3, 3, 7], B, "toy 3x3x3x7")
