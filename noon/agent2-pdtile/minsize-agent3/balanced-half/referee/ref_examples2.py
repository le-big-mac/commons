"""Referee, second reading: the closing example of the new section 7 (p=2, q=3, n=3, E={2}, F={0,3}), literally,
and the variant needed for its first assertion (every class of depth 2 split into two equal halves)."""
import numpy as np
from ref_common import literal_patterns, bits_to_set
from ref_brute13 import least_fibre_depth
p, q, n = 2, 3, 3
def make(split_fibre_classes):
    W = np.zeros((8, 3), dtype=np.int64)            # u = u1 + 2 u2 + 4 u3 ; prefix "u1 u2"
    def put(u1, u2, vec, split):
        base = u1 + 2 * u2
        if split:
            W[base] = [v // 2 for v in vec]; W[base + 4] = [v // 2 for v in vec]
        else:
            W[base] = vec
    put(0, 0, (6, 0, 0), True); put(0, 1, (2, 2, 2), split_fibre_classes)
    put(1, 0, (0, 6, 6), True); put(1, 1, (4, 4, 4), split_fibre_classes)
    return W
for name, sp in (("text's example ((2,2,2) and (4,4,4) each in one child)", False), ("variant (all four classes of depth 2 split evenly)", True)):
    W = make(sp)
    r = literal_patterns(p, q, n, W.reshape(1, 8, 3))[0]
    md, fibs = least_fibre_depth(p, q, n, W.reshape(1, 8, 3))
    E = sorted(bits_to_set(r["E"][0, 0])); F = sorted(bits_to_set(r["F"][0, 0]) | ({0} if r["bal"][0, 0] else set()))
    print(f"{name}: {int(W.sum())} elements, exact pattern E={E} F={F}, least depth of a nonempty fibre class {int(md[0])}, "
          f"nonempty fibre classes of depth 2: {[int(c) for c in np.flatnonzero(fibs[2][0])]} (class index u1 + 2 u2)")
