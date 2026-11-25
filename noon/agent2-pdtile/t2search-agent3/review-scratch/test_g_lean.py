"""Lean version of test_g.py for many candidates: float full LP for every candidate; for every LP-feasible one an exact rational complement
is verified and (T1)/(T2) are checked with exact zeros.  LP-infeasible candidates are NOT certified here (HiGHS verdict only).
usage: test_g_lean.py p a q b candfile [nproc]"""
import sys, time
from multiprocessing import Pool
from common import *
import numpy as np
import wt
p, a, q, b = (int(v) for v in sys.argv[1:5]); M = p ** a * q ** b
cands = [int(l, 16) for l in open(sys.argv[5]) if l.strip()]; nproc = int(sys.argv[6]) if len(sys.argv) > 6 else 4
def work(mask):
    A = [x for x in range(M) if mask >> x & 1]
    feas, f = wt.full_lp(A, M)
    if not feas: return None
    fz = np.where(np.abs(f) < 1e-9, 0, f); ok = any(wt.verify_f(A, M, fr) for fr in wt.rationalise(fz))
    Z = zeros_exact(A, M)
    return mask, len(A), ok, sorted(Z), T1_holds(Z, len(A), p, a, q, b), T2_violations(Z, p, a, q, b)
if __name__ == "__main__":
    t0 = time.time()
    with Pool(nproc) as pool: res = [r for r in pool.imap_unordered(work, cands, chunksize=200) if r is not None]
    sizes = {}
    for r in res: sizes[r[1]] = sizes.get(r[1], 0) + 1
    print(f"Z_{M}: {len(cands)} orbit representatives, full LP on {M} unknowns each, {time.time() - t0:.0f} s: {len(res)} weak tiles by HiGHS "
          f"({sum(1 for r in res if r[2])} with an exactly verified rational complement), by size {dict(sorted(sizes.items()))};  "
          f"(T1) violated by {sum(1 for r in res if not r[4])}, (T2) violated by {sum(1 for r in res if r[5])}")
    for r in res:
        if not r[4] or r[5]: print("   VIOLATION", [x for x in range(M) if r[0] >> x & 1], r[1:])
