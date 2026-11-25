"""Z_108, size 6: among ALL orbit representatives of 6-sets passing the support tests (cand108_eq6.txt), select those that violate (T2) as sets
(zeros by FFT, then exact), and decide each directly by the full LP with certificates.  (Sets satisfying (T2) cannot be (T2) counterexamples.)"""
import sys, time, numpy as np
from multiprocessing import Pool
from common import *
import wt
p, a, q, b = 2, 2, 3, 3; M = 108
masks = [int(l, 16) for l in open("cand108_eq6.txt") if l.strip()]
D = [d for d in divisors(M) if d > 1]
def zero_table(ms):
    X = np.zeros((len(ms), M))
    for r, m in enumerate(ms):
        for x in range(M):
            if m >> x & 1: X[r, x] = 1
    F = np.abs(np.fft.fft(X, axis=1))
    return {d: F[:, M // d] < 1e-9 for d in D}
def work(mask):
    A = [x for x in range(M) if mask >> x & 1]; Z = zeros_exact(A, M)
    v2 = T2_violations(Z, p, a, q, b)
    if not v2: return mask, None, None, sorted(Z), v2
    verdict, cert, feas = wt.certified(A, M)
    return mask, verdict, feas, sorted(Z), v2
if __name__ == "__main__":
    t0 = time.time(); sel = []; nboth = 0
    for s in range(0, len(masks), 50000):
        ms = masks[s:s + 50000]; zt = zero_table(ms)
        viol = np.zeros(len(ms), bool); both = np.zeros(len(ms), bool)
        for i in range(1, a + 1):
            for j in range(1, b + 1):
                both |= zt[p ** i] & zt[q ** j]; viol |= zt[p ** i] & zt[q ** j] & ~zt[p ** i * q ** j]
        nboth += int(both.sum()); sel += [m for m, v in zip(ms, viol) if v]
    print(f"Z_108 size 6: {len(masks)} orbit representatives; {nboth} have some 2^i and some 3^j as zeros; {len(sel)} violate (T2) as sets (FFT)   [{time.time() - t0:.0f} s]", flush=True)
    with Pool(3) as pool: res = pool.map(work, sel, chunksize=20)
    assert all(r[4] for r in res), "FFT and exact zeros disagree"
    print(f"   decided directly: weak tiles {sum(1 for r in res if r[1] == 'yes')}, not weak tiles with exact Farkas certificate {sum(1 for r in res if r[1] == 'no')}, "
          f"not certified {sum(1 for r in res if r[1] == '?')} (of which HiGHS full LP says feasible: {sum(1 for r in res if r[1] == '?' and r[2])})   [{time.time() - t0:.0f} s]")
    for r in res:
        if r[1] == "yes" or (r[1] == "?" and r[2]): print("   (T2)-VIOLATING WEAK TILE?", [x for x in range(M) if r[0] >> x & 1], r[1:])
