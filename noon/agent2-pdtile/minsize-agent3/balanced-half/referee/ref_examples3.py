"""Referee, second reading: a small example for "the size condition in (*) cannot be dropped":
p=2, q=3, n=3, E = {}, F = {0,3} (x = 1, E+ = {3}, q p^(e+k') = 6): 12 elements, exact pattern (E+, F), fibre class of depth 2."""
import numpy as np
from ref_common import literal_patterns, bits_to_set, rule
from ref_brute13 import least_fibre_depth
p, q, n = 2, 3, 3
W = np.zeros((8, 3), dtype=np.int64)                 # u = u1 + 2 u2 + 4 u3
for (u1, u2, leaf) in ((0, 0, (1, 0, 0)), (0, 1, (1, 1, 1)), (1, 0, (0, 1, 1))):    # each class of depth 2 = two equal leaves
    W[u1 + 2 * u2] = leaf; W[u1 + 2 * u2 + 4] = leaf
r = literal_patterns(p, q, n, W.reshape(1, 8, 3))[0]
md, fibs = least_fibre_depth(p, q, n, W.reshape(1, 8, 3))
E = sorted(bits_to_set(r["E"][0, 0])); F = sorted(bits_to_set(r["F"][0, 0]) | ({0} if r["bal"][0, 0] else set()))
print(f"{int(W.sum())} elements, exact pattern E={E} F={F}, nonempty fibre classes of depth 2: {[int(c) for c in np.flatnonzero(fibs[2][0])]} "
      f"(index u1 + 2 u2), least depth {int(md[0])}; rule for (E, F) = ([], [0, 3]): (value, x, a0, k') = {rule(p, q, n, set(), {0, 3})}")
