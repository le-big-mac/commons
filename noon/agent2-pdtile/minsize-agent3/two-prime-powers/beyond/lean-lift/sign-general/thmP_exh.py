# thmP_exh.py -- Theorem P on the box 3 x 5, every 0/1 function and every function with values in {0,+1,-1}
# supported on at most 6 cells: least fraction of good patterns, over Q and over F_7, F_11.
import sys, itertools, numpy as np
sys.argv = [sys.argv[0], 'none']
from thmP_test import setup
pre = setup([3, 5]); cells, T, lev, S = pre
def least(W, q):
    W = np.array(W, dtype=np.int64); out = 1.0
    for a in range(0, len(W), 4096):
        w = W[a:a + 4096]
        I = np.einsum('sc,nc,jc->nsj', S, w, T)        # n functions, s patterns, j entries
        if q: I %= q
        g = np.ones(I.shape[:2], dtype=bool)
        for L in range(4): g &= np.any(I[:, :, lev == L] != 0, axis=2)
        nz = np.any((w % q if q else w) != 0, axis=1)
        if nz.any(): out = min(out, g[nz].mean(axis=1).min())
    return out
W01 = list(itertools.product((0, 1), repeat=15))
Wsp = []
for r in range(1, 7):
    for supp in itertools.combinations(range(15), r):
        for signs in itertools.product((1, -1), repeat=r - 1):
            w = [0] * 15; w[supp[0]] = 1
            for c, e in zip(supp[1:], signs): w[c] = e
            Wsp.append(w)
for q in (0, 7, 11):
    print("box 3 x 5 over %s: all %d functions with values 0/1: least fraction %.4f; all %d functions with values in {0,1,-1} on at most 6 cells (first value +1): least fraction %.4f"
          % ("F_%d" % q if q else "Q", len(W01) - 1, least(W01, q), len(Wsp), least(Wsp, q)))
    sys.stdout.flush()
