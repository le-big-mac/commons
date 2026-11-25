"""Step 2: the EXACT law of K (as defined in expectations.md) under the uniform measure, at large orders.
Dimers of a uniform tiling form a determinantal process with kernel M(e, e') = K(e) Kinv[v_e, h_e'] (K = Kasteleyn
matrix, rows = left/right corners, columns = top/bottom corners). So
  P(K >= k) = P(blocks (0,0)..(k-1,k-1) each hold a and not d) = det [[M_AA, M_AB], [-M_BA, I - M_BB]],
A = the a dimers, B = the d dimers of those blocks. Only 2*kmax columns of Kinv are needed: sparse LU.
usage: ref_Kexact.py n [n ...]      (n <= 5: also checked against brute-force enumeration)
"""
import sys, math, time
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spl


def kasteleyn(n):
    N = n * (n + 1)
    I, J = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    I = I.ravel(); J = J.ravel()
    H = lambda i, j: i * (n + 1) + j
    V = lambda i, j: i * n + j
    rows = np.concatenate([H(I, J), H(I, J + 1), H(I, J), H(I, J + 1)])
    cols = np.concatenate([V(I, J), V(I, J), V(I + 1, J), V(I + 1, J)])
    vals = np.concatenate([-np.ones(n * n), np.ones(3 * n * n)])
    return sp.csc_matrix((vals, (rows, cols)), shape=(N, N)), H, V


def K_law(n, kmax=None, verbose=True):
    t0 = time.time()
    Km, H, V = kasteleyn(n)
    if kmax is None:
        kmax = min(n, int(0.1465 * n + 0.5 * n ** (1 / 3) + 9 * 0.26 * n ** (1 / 3)) + 4)
    lu = spl.splu(Km)
    if verbose:
        print(f"  n={n}: N={Km.shape[0]}, LU nnz {lu.L.nnz + lu.U.nnz:,}, factor time {time.time()-t0:.1f}s", flush=True)
    j = np.arange(kmax)
    ha, va = H(j, j), V(j, j)            # a of block (j,j): left corner - top corner, weight -1
    hd, vd = H(j, j + 1), V(j + 1, j)    # d of block (j,j): right corner - bottom corner, weight +1
    hs = np.concatenate([ha, hd]); vs = np.concatenate([va, vd])
    wts = np.concatenate([-np.ones(kmax), np.ones(kmax)])
    Kinv_cols = np.empty((2 * kmax, 2 * kmax))       # [v index, h index] restricted
    for c, h in enumerate(hs):
        e = np.zeros(Km.shape[0]); e[h] = 1.0
        x = lu.solve(e)                               # column h of Kinv
        Kinv_cols[:, c] = x[vs]
    M = wts[:, None] * Kinv_cols                      # M[i, j] = K(e_i) Kinv[v_i, h_j]
    # one-point sanity: probabilities in [0, 1]
    p1 = np.diag(M)
    surv = np.ones(kmax + 1)                          # surv[k] = P(K >= k)
    for k in range(1, kmax + 1):
        A = np.arange(k); B = kmax + np.arange(k)
        top = np.hstack([M[np.ix_(A, A)], M[np.ix_(A, B)]])
        bot = np.hstack([-M[np.ix_(B, A)], np.eye(k) - M[np.ix_(B, B)]])
        surv[k] = np.linalg.det(np.vstack([top, bot]))
    pmf = surv[:-1] - surv[1:]                        # P(K = k), k = 0..kmax-1
    tail = surv[kmax]
    ks = np.arange(kmax)
    mean = (pmf * ks).sum(); var = (pmf * ks ** 2).sum() - mean ** 2
    m3 = (pmf * (ks - mean) ** 3).sum()
    return dict(n=n, kmax=kmax, pmf=pmf, tail=tail, mean=mean, sd=math.sqrt(var), skew=m3 / var ** 1.5, p1min=p1.min(), p1max=p1.max(),
                time=time.time() - t0)


def brute_K_law(n):
    from ref_core import K_of
    # brute-force all tilings (same routine as ref_exact.all_tilings)
    def Vv(i, j): return i * n + j
    nV = (n + 1) * n
    def Hv(i, j): return nV + i * (n + 1) + j
    nvert = 2 * nV
    inc = [[] for _ in range(nvert)]
    for i in range(n):
        for j in range(n):
            blk = i * n + j
            for bit, (u, w) in ((1, (Hv(i, j), Vv(i, j))), (2, (Vv(i, j), Hv(i, j + 1))), (4, (Hv(i, j), Vv(i + 1, j))), (8, (Vv(i + 1, j), Hv(i, j + 1)))):
                inc[u].append((w, blk, bit)); inc[w].append((u, blk, bit))
    cov = [False] * nvert; val = [0] * (n * n); hist = np.zeros(n + 1)
    def rec(start):
        u = start
        while u < nvert and cov[u]: u += 1
        if u == nvert:
            hist[K_of(np.array(val, np.uint8).reshape(n, n))] += 1; return
        cov[u] = True
        for w, blk, bit in inc[u]:
            if not cov[w]:
                cov[w] = True; val[blk] |= bit; rec(u + 1); cov[w] = False; val[blk] &= ~bit
        cov[u] = False
    rec(0)
    return hist / hist.sum()


if __name__ == "__main__":
    lim = (1 - 1 / math.sqrt(2)) / 2
    for n in [int(a) for a in sys.argv[1:]]:
        if n <= 5:
            r = K_law(n, kmax=n, verbose=False); b = brute_K_law(n)
            ex = np.append(r["pmf"], r["tail"])
            print(f"n={n}: exact law of K from determinants {np.round(ex, 10)}; brute force over all tilings {np.round(b, 10)}; max difference {np.abs(ex-b).max():.2e}")
            continue
        r = K_law(n)
        th = 2 ** (-11 / 6) * n ** (1 / 3)
        print(f"n={n}: EXACT mean K {r['mean']:.5f}, sd {r['sd']:.5f}, skewness {r['skew']:+.4f}; K/n {r['mean']/n:.6f}; "
              f"(mean - 0.146447 n) = {r['mean']-lim*n:.4f} = {(r['mean']-lim*n)/n**(1/3):.4f} n^(1/3); sd/n^(1/3) = {r['sd']/n**(1/3):.4f}; "
              f"mean excess / sd = {(r['mean']-lim*n)/r['sd']:.4f}")
        print(f"      vs Tracy-Widom(2) with scale 2^(-11/6) n^(1/3) (from memory): 1.7711*scale - (mean excess) = {1.771087*th-(r['mean']-lim*n):+.4f} blocks; "
              f"sd^2 - (0.9018*scale)^2 = {r['sd']**2-0.813195*th**2:+.4f}")
        print(f"      [mass beyond kmax={r['kmax']}: {r['tail']:.2e}; total {r['pmf'].sum()+r['tail']:.12f}; min pmf {r['pmf'].min():.1e}; one-edge probabilities in [{r['p1min']:.3g}, {r['p1max']:.6f}]; {r['time']:.0f}s]")
        nz = np.flatnonzero(r["pmf"] > 5e-5)
        print("      P(K=k):", ", ".join(f"{k}:{r['pmf'][k]:.4f}" for k in nz), flush=True)
        np.save(f"/home/agent2/aztec/referee/Kpmf_{n}.npy", r["pmf"])
