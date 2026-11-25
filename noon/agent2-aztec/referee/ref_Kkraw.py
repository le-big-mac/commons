"""Step 2: the EXACT law of K at any order, by a one-line gap probability.

Facts used (proved in the referee's notes, and checked here against brute force and against Kasteleyn determinants):
 (1) blocks (0,0)..(k-1,k-1) all hold exactly a  <=>  the whole k x k corner square holds exactly a
     <=>  the top corners V(k, j), j = 0..k-1, of block row k are all matched downward (by a or b of row k).
 (2) the top corners of row k that are matched UPWARD (k of them among n sites j = 0..n-1) form the Krawtchouk
     ensemble: P(x_1 < ... < x_k) proportional to prod_{i<j} (x_i - x_j)^2 prod_i C(n-1, x_i).
So P(K >= k) = P(no point of the k-point ensemble in {0..k-1}) = det[ sum_{x >= k} phi_i(x) phi_j(x) ]_{i,j<k},
phi_i = orthonormal Krawtchouk functions = eigenvectors of the Jacobi matrix (diag (n-1)/2, off-diag sqrt((i+1)(n-1-i))/2).
usage: ref_Kkraw.py n [n ...]
"""
import sys, math
import numpy as np
from scipy.linalg import eigh_tridiagonal


def K_law(n, kmax=None):
    N = n - 1
    i = np.arange(N)
    ev, Phi = eigh_tridiagonal(np.full(N + 1, N / 2.0), 0.5 * np.sqrt((i + 1.0) * (N - i)))
    assert np.abs(ev - np.arange(N + 1)).max() < 1e-6 * max(1, N)
    # Phi[i, x] = phi_i(x): row = degree, column = site x (eigenvalue x)
    if kmax is None:
        kmax = min(n, int(0.1465 * n + 0.5 * n ** (1 / 3) + 10 * 0.27 * n ** (1 / 3)) + 5)
    surv = np.ones(kmax + 1)
    for k in range(1, kmax + 1):
        B = Phi[:k, k:]
        sgn, ld = np.linalg.slogdet(B @ B.T)
        surv[k] = math.exp(ld) if sgn > 0 else 0.0
    pmf = surv[:-1] - surv[1:]
    ks = np.arange(kmax)
    mean = (pmf * ks).sum(); var = (pmf * ks ** 2).sum() - mean ** 2; m3 = (pmf * (ks - mean) ** 3).sum()
    return dict(pmf=pmf, tail=surv[kmax], mean=mean, sd=math.sqrt(var), skew=m3 / var ** 1.5, surv=surv)


if __name__ == "__main__":
    lim = (1 - 1 / math.sqrt(2)) / 2
    out = []
    for n in [int(a) for a in sys.argv[1:]]:
        r = K_law(n)
        exc = r["mean"] - lim * n
        th = 2 ** (-11 / 6) * n ** (1 / 3)
        out.append((n, r["mean"], r["sd"], exc))
        print(f"n={n}: EXACT mean K {r['mean']:.5f}  sd {r['sd']:.5f}  skew {r['skew']:+.4f}  K/n {r['mean']/n:.6f}  excess {exc:.4f} = {exc/n**(1/3):.4f} n^(1/3)  "
              f"sd/n^(1/3) {r['sd']/n**(1/3):.4f}  excess/sd {exc/r['sd']:.4f}  | 0.4970 n^(1/3) - excess = {1.771087*th-exc:+.4f}  sd^2 - (0.2530 n^(1/3))^2 = {r['sd']**2-0.813195*th**2:+.4f}"
              f"  [tail {r['tail']:.1e}, min pmf {r['pmf'].min():.1e}]", flush=True)
        if n <= 1600:
            np.save(f"/home/agent2/aztec/referee/Kkraw_pmf_{n}.npy", r["pmf"])
    if len(out) > 1:
        o = np.array(out)
        print("effective exponent of the exact sd between neighbouring sizes:", np.round(np.diff(np.log(o[:, 2])) / np.diff(np.log(o[:, 0])), 4))
        print("effective exponent of the exact excess between neighbouring sizes:", np.round(np.diff(np.log(o[:, 3])) / np.diff(np.log(o[:, 0])), 4))
        sel = np.isin(o[:, 0], [100, 200, 400, 800, 1600])
        if sel.sum() == 5:
            print("log-log slope of the exact sd over 100, 200, 400, 800, 1600:", round(np.polyfit(np.log(o[sel, 0]), np.log(o[sel, 2]), 1)[0], 4),
                  "; over 100..800:", round(np.polyfit(np.log(o[sel, 0][:4]), np.log(o[sel, 2][:4]), 1)[0], 4))
