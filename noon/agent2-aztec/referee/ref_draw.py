"""Step 2: is the author's drawing a correct picture of a tiling? Re-derive the cells each dimer covers from the formula in
aztec.draw (P and the four offsets) and check: every cell of the Aztec diamond covered exactly once; a, d lying; b, c standing;
a at the top, b right, c left, d bottom in the frozen corners."""
import sys
sys.dont_write_bytecode = True
import numpy as np
from collections import Counter
from ref_core import grow_step
for n, seed in ((7, 1), (40, 2), (150, 3)):
    rng = np.random.default_rng(seed); v = np.zeros((0, 0), np.uint8)
    for _ in range(n): v, _ = grow_step(v, rng)
    P = lambda X, Y: ((X - Y) / 2, (X + Y) / 2 - n)           # as in aztec.draw with s = 1 and the centre at the origin
    cover = Counter(); orient = {}; pos = {k: [] for k in "abcd"}
    for name, bit, (dx1, dy1, dx2, dy2) in (('a', 1, (1, 0, 0, 1)), ('b', 2, (1, 0, 2, 1)), ('c', 4, (0, 1, 1, 2)), ('d', 8, (2, 1, 1, 2))):
        for i, j in zip(*np.nonzero(v & bit)):
            p, q = P(2 * j + dx1, 2 * i + dy1), P(2 * j + dx2, 2 * i + dy2)
            cover[p] += 1; cover[q] += 1
            orient.setdefault(name, set()).add("lying" if p[1] == q[1] and abs(p[0] - q[0]) == 1 else "standing" if p[0] == q[0] and abs(p[1] - q[1]) == 1 else "NOT A DOMINO")
            pos[name].append(((p[0] + q[0]) / 2, (p[1] + q[1]) / 2))
    cells = {(x + 0.5, y + 0.5) for x in range(-n - 1, n + 1) for y in range(-n - 1, n + 1) if abs(x + 0.5) + abs(y + 0.5) <= n}
    ok = set(cover) == cells and set(cover.values()) == {1}
    cm = {k: np.round(np.mean(pos[k], axis=0) / n, 2).tolist() for k in "abcd"}
    print(f"order {n}: {len(cells)} cells (2n(n+1) = {2*n*(n+1)}); every cell covered exactly once: {ok}; orientations {orient}; mean position/n of each kind (x right, y down) {cm}")
