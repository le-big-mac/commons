import sys, time
sys.path.insert(0, '/tmp/agent2_referee3')
from dplus import *
import numpy as np
from scipy.optimize import linprog

def dplus_float_full(p, mask):
    """float LP over ALL real functions h on Z_M (no step reduction), full DFT."""
    M = p[0]*p[1]*p[2]
    def sub(x):
        return sum(1 << w for w in range(3) if x % p[w])
    allowed = {BIT2SUB[b] for b in range(7) if mask >> b & 1}
    idx = [x for x in range(1, M) if sub(x) in allowed]
    if not idx: return 1.0
    # hat h(xi) = 1 + sum_x h(x) cos(2 pi x xi / M) (+ i sin): require real part >= 0 and imaginary part = 0
    xi = np.arange(M)[:, None]; xs = np.array(idx)[None, :]
    C = np.cos(2*np.pi*xi*xs/M); S = np.sin(2*np.pi*xi*xs/M)
    res = linprog(-np.ones(len(idx)), A_ub=-C, b_ub=np.ones(M), A_eq=S, b_eq=np.zeros(M), bounds=[(0, None)]*len(idx), method='highs')
    assert res.status == 0
    return 1 - res.fun

for p in [(2,3,5), (2,3,7)]:
    t0 = time.time(); worst = 0
    for mask in range(128):
        d = dplus(p, mask)
        d2 = dplus_bruteforce(p, mask)
        assert d == d2, (p, mask, d, d2)
        d3 = dplus_float_full(p, mask)
        worst = max(worst, abs(float(d) - d3))
    print(p, "simplex == vertex enumeration for all 128 patterns; max |exact - full float LP| =", worst, "time", round(time.time()-t0,1))
