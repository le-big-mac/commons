"""Validation of the enumeration pipeline used for Z_36 (enum36.c + test_g.py) on a small group by pure brute force:
every set containing 0 (no filter at all) is decided by the full LP; the weak tiles found must be exactly the affine orbits of the
weak tiles that the pipeline reports.   usage: test_g_validate.py p a q b candfile respickle [nproc]"""
import sys, pickle, math, time
from multiprocessing import Pool
from common import *
import wt
p, a, q, b = (int(v) for v in sys.argv[1:5]); M = p ** a * q ** b
def work(mask):
    A = [x for x in range(M) if mask >> x & 1]
    feas, _ = wt.full_lp(A, M)
    return mask, feas
def canon(mask):
    A = [x for x in range(M) if mask >> x & 1]; best = None
    for u in units(M):
        B = [(u * x) % M for x in A]
        for t in B:
            m = 0
            for y in B: m |= 1 << ((y - t) % M)
            if best is None or m < best: best = m
    return best
if __name__ == "__main__":
    res = pickle.load(open(sys.argv[6], "rb")); nproc = int(sys.argv[7]) if len(sys.argv) > 7 else 4
    pipeline = {r[0] for r in res if r[2] == "yes"}
    assert all(canon(m) == m for m in pipeline)
    t0 = time.time()
    masks = [m | 1 for m in range(0, 2 ** M, 2)]                                    # all sets containing 0
    masks = [m for m in masks if 2 <= bin(m).count("1") < M]
    with Pool(nproc) as pool: out = pool.map(work, masks, chunksize=500)
    brute = {m for m, f in out if f}
    brute_orbits = {canon(m) for m in brute}
    print(f"Z_{M}: brute force over {len(masks)} sets containing 0 (sizes 2..{M-1}), {time.time() - t0:.0f} s: {len(brute)} weak tiles in {len(brute_orbits)} affine orbits; "
          f"pipeline reports {len(pipeline)} orbits; identical: {brute_orbits == pipeline}")
    # T1 / T2 on all brute-force weak tiles
    bad1 = bad2 = 0
    for m in brute:
        A = [x for x in range(M) if m >> x & 1]; Z = zeros_exact(A, M)
        bad1 += not T1_holds(Z, len(A), p, a, q, b); bad2 += bool(T2_violations(Z, p, a, q, b))
    print(f"   (T1) violations among them: {bad1}; (T2) violations: {bad2}")
