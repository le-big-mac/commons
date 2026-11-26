"""An independent look at what the two new Lean statements say, on every subset of three small cyclic groups.
For A in Z_N, N = p^n q:  E = {l in 1..n : Phi_{p^l} divides A},  F = {l in 1..n : Phi_{p^l q} divides A},  and Phi_q divides A or not.
Claim U:  Phi_q does not divide A  =>  p^|E u F| <= |A|.
Claim G:  Phi_q does not divide A and k = |F minus E| >= 1  =>  p^|E| (p^k + q) <= |A|.
Divisibility by Phi_d is tested by the value of the mask polynomial at exp(2 pi i / d)."""
import sys, itertools
sys.dont_write_bytecode = True
import numpy as np

def check(p, n, q):
    N = p ** n * q
    ds = [q] + [p ** l for l in range(1, n + 1)] + [p ** l * q for l in range(1, n + 1)]
    roots = np.array([[np.exp(2j * np.pi * a / d) for d in ds] for a in range(N)])            # N x len(ds)
    total = 0; bad_u = bad_g = 0; hyp_u = hyp_g = 0; eq_u = eq_g = 0; ex = None
    step = 1 << 16
    for start in range(0, 1 << N, step):
        idx = np.arange(start, min(start + step, 1 << N), dtype=np.int64)
        bits = ((idx[:, None] >> np.arange(N)[None, :]) & 1).astype(float)                    # subsets as rows
        vals = np.abs(bits @ roots) < 1e-9                                                    # zero at each d
        size = bits.sum(1).astype(int)
        zq = vals[:, 0]; E = vals[:, 1:1 + n]; Fz = vals[:, 1 + n:1 + 2 * n]
        nonempty = size > 0
        e = E.sum(1); union = (E | Fz).sum(1); k = (Fz & ~E).sum(1)
        hu = nonempty & ~zq
        hyp_u += int(hu.sum()); bad_u += int((hu & (p ** union > size)).sum()); eq_u += int((hu & (p ** union == size)).sum())
        hg = hu & (k >= 1)
        bound = p ** e * (p ** k + q)
        hyp_g += int(hg.sum()); bad_g += int((hg & (bound > size)).sum())
        eqm = hg & (bound == size); eq_g += int(eqm.sum())
        if ex is None and (eqm & (k >= 2)).any():
            i = int(np.nonzero(eqm & (k >= 2))[0][0]); ex = (sorted(int(a) for a in np.nonzero(bits[i])[0]), int(e[i]), int(k[i]), int(size[i]))
        total += len(idx)
    print(f"Z_{N} (p = {p}, n = {n}, q = {q}): {total} subsets. Claim U: hypothesis holds for {hyp_u}, bound broken in {bad_u}, met with equality in {eq_u}."
          f" Claim G: hypothesis holds for {hyp_g}, bound broken in {bad_g}, met with equality in {eq_g}." + (f" One set with k >= 2 that meets it: {ex[0]} (e = {ex[1]}, k = {ex[2]}, size {ex[3]})" if ex else ""))

if __name__ == '__main__':
    check(2, 2, 3)      # Z_12
    check(3, 2, 2)      # Z_18
    check(2, 3, 3)      # Z_24
