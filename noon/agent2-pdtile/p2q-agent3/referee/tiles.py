"""Independent check of the theorem's conclusion for M = 12, 18, 20:

 (1) brute force: which subsets A of Z_M containing 0 tile Z_M (exact cover search for a complement),
     with no reference to cyclotomic polynomials or D+;
 (2) compare with the list of sets with D+(Z_A) = |A| saved by enum_p2q.py (pdmask_M.npy);
 (3) direct LP for the definition of pd-tiling (f(0)=1, f>=0, fhat>=0, 1_A * f = 1), no step functions,
     no D+: on every set for M=12, and on all 'pd' sets plus a random sample of the others for M=18, 20.
"""
import sys
import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(20261120)


def tiles(M, Amask, n):
    if M % n:
        return False
    full = (1 << M) - 1
    shifts = [((Amask << s) | (Amask >> (M - s))) & full for s in range(M)]
    elems = [a for a in range(M) if Amask >> a & 1]

    def rec(cov):
        if cov == full:
            return True
        z = 0
        while cov >> z & 1:
            z += 1
        for a in elems:
            sh = shifts[(z - a) % M]
            if sh & cov == 0 and rec(cov | sh):
                return True
        return False

    return rec(Amask)        # complement contains 0


def pd_tiles_lp(M, Amask):
    """feasibility of: f even, f(0)=1, f>=0, sum_x f(x) cos(2 pi x xi/M) >= 0, sum_{a in A} f(z-a) = 1."""
    # f even is forced by fhat real; impose it explicitly
    elems = [a for a in range(M) if Amask >> a & 1]
    A_eq, b_eq = [], []
    row = np.zeros(M)
    row[0] = 1
    A_eq.append(row)
    b_eq.append(1.0)
    for x in range(1, M):
        if x < (M - x) % M:
            row = np.zeros(M)
            row[x] = 1
            row[M - x] = -1
            A_eq.append(row)
            b_eq.append(0.0)
    for z in range(M):
        row = np.zeros(M)
        for a in elems:
            row[(z - a) % M] += 1
        A_eq.append(row)
        b_eq.append(1.0)
    A_ub = [[-np.cos(2 * np.pi * x * xi / M) for x in range(M)] for xi in range(M)]
    r = linprog(np.zeros(M), A_ub=A_ub, b_ub=np.zeros(M), A_eq=np.array(A_eq), b_eq=b_eq,
                bounds=[(0, None)] * M, method="highs")
    return r.status == 0


for M in [12, 18, 20]:
    pd_idx = set(int(i) for i in np.load(f"pdmask_{M}.npy"))
    nsub = 1 << (M - 1)
    tile_idx = set()
    for i in range(nsub):
        n = bin(i).count("1") + 1
        if M % n == 0:
            if tiles(M, (i << 1) | 1, n):
                tile_idx.add(i)
    print(f"M={M}: tiles containing 0 (brute force): {len(tile_idx)}; sets with D+(Z_A)=|A|: {len(pd_idx)}; "
          f"equal as sets of sets: {tile_idx == pd_idx}")
    # direct LP
    if M == 12:
        sample = list(range(nsub))
    else:
        others = [i for i in rng.choice(nsub, size=1500, replace=False) if int(i) not in pd_idx]
        sample = sorted(pd_idx) + [int(i) for i in others]
    agree = 0
    dis = []
    for i in sample:
        feas = pd_tiles_lp(M, (i << 1) | 1)
        if feas == (i in pd_idx):
            agree += 1
        else:
            dis.append(i)
    print(f"   direct pd-tiling LP on {len(sample)} sets ({sum(1 for i in sample if i in pd_idx)} of them 'pd'): "
          f"agrees with [D+(Z_A) = |A|] on {agree}; disagreements: {dis[:10]}")
    sys.stdout.flush()
