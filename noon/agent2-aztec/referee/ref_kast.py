"""Step 2: an exact check of uniformity at orders beyond 5, by a different route.
Exact one-block probabilities under the uniform measure from the inverse Kasteleyn matrix, compared with
frequencies from (i) the AUTHOR's sampler (aztec.grow, imported read-only) and (ii) the referee's sampler.
usage: ref_kast.py ORDER NSAMPLES SEED
"""
import sys, os, math
sys.dont_write_bytecode = True
import numpy as np
sys.path.insert(0, "/home/agent2/aztec")
import aztec as A
from ref_core import grow_step

n = int(sys.argv[1]); N = int(sys.argv[2]); seed = int(sys.argv[3])


def exact(n):
    """returns p[4, n, n] = P(a), P(b), P(c), P(d) in each block; pad[n, n], pbc[n, n] pair probabilities."""
    nV = (n + 1) * n
    Vv = lambda i, j: i * n + j              # top/bottom corners, i in 0..n
    Hv = lambda i, j: i * (n + 1) + j        # left/right corners, j in 0..n
    Km = np.zeros((nV, nV))                  # rows: H vertices, cols: V vertices
    I, J = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    ha, va = Hv(I, J), Vv(I, J)              # a: left - top
    hb, vb = Hv(I, J + 1), Vv(I, J)          # b: right - top
    hc, vc = Hv(I, J), Vv(I + 1, J)          # c: left - bottom
    hd, vd = Hv(I, J + 1), Vv(I + 1, J)      # d: right - bottom
    Km[ha, va] = -1.0                        # one negative edge in every face (block faces and the faces between)
    Km[hb, vb] = 1.0; Km[hc, vc] = 1.0; Km[hd, vd] = 1.0
    sign, logdet = np.linalg.slogdet(Km)
    Ki = np.linalg.inv(Km)                   # Ki[v, h]
    p = np.abs(np.array([Ki[va, ha], Ki[vb, hb], Ki[vc, hc], Ki[vd, hd]]))
    pad = np.abs(Ki[va, ha] * Ki[vd, hd] - Ki[va, hd] * Ki[vd, ha])
    pbc = np.abs(Ki[vb, hb] * Ki[vc, hc] - Ki[vb, hc] * Ki[vc, hb])
    return p, pad, pbc, logdet / math.log(2)


# sanity of the exact machinery against the referee's exhaustive enumeration
for m, want in ((1, 1.0), (2, 2.0), (3, 3.25), (4, 4.75), (5, 5 + 97 / 64), (6, 6 + 163 / 64)):
    p, pad, pbc, l2 = exact(m)
    print(f"order {m}: log2(number of tilings) from determinant {l2:.6f} (want {m*(m+1)//2}); expected pair blocks {pad.sum()+pbc.sum():.6f} (enumeration: {want})")

# exact expected tosses to reach order n = sum over k <= n of expected number of pair blocks at order k
etoss = 0.0
for k in range(1, n + 1):
    p, pad, pbc, l2 = exact(k)
    etoss += pad.sum() + pbc.sum()
epairs = pad.sum() + pbc.sum()
ponly_a_diag = np.diagonal(p[0] - pad)
# exact expectation of a 'union-bound' on K is not available; report exact P(block (k,k) holds exactly a)
print(f"order {n}: log2 Z = {l2:.4f} (want {n*(n+1)//2}); exact E[pair blocks] = {epairs:.4f}; exact E[tosses to reach order {n}] = {etoss:.4f}; "
      f"exact share of each kind overall {np.round(p.sum(axis=(1,2))/p.sum(),6)}")


def run(sampler, label):
    rng = np.random.default_rng([seed, 1 if label.startswith('author') else 2])
    cnt = np.zeros((4, n, n)); cpair = np.zeros((2, n, n)); toss = []; pairs = []
    for _ in range(N):
        a, b, c, d, t = sampler(rng)
        cnt[0] += a; cnt[1] += b; cnt[2] += c; cnt[3] += d
        cpair[0] += a & d; cpair[1] += b & c
        toss.append(t); pairs.append(int((a & d).sum() + (b & c).sum()))
    toss = np.array(toss, float); pairs = np.array(pairs, float)
    var = N * p * (1 - p)
    ok = var > 5
    z2 = ((cnt - N * p) ** 2 / np.where(ok, var, 1))[ok]
    pp = np.array([pad, pbc]); varp = N * pp * (1 - pp); okp = varp > 5
    z2p = ((cpair - N * pp) ** 2 / np.where(okp, varp, 1))[okp]
    # blocks where the exact probability is ~0 or ~1 must show it
    forced0 = int(cnt[p < 1e-12].sum()); forced1 = int((N - cnt[p > 1 - 1e-12]).sum())
    print(f"[{label}] {N} growths to order {n}: tosses mean {toss.mean():.3f} (se {toss.std(ddof=1)/math.sqrt(N):.3f}) vs exact {etoss:.3f} -> z = {(toss.mean()-etoss)/(toss.std(ddof=1)/math.sqrt(N)):+.2f}; "
          f"pair blocks mean {pairs.mean():.4f} (se {pairs.std(ddof=1)/math.sqrt(N):.4f}) vs exact {epairs:.4f} -> z = {(pairs.mean()-epairs)/(pairs.std(ddof=1)/math.sqrt(N)):+.2f}")
    print(f"      single-dimer frequencies vs exact, {ok.sum()} block-kinds with N p (1-p) > 5: mean z^2 = {z2.mean():.4f} (1 if uniform), max |z| = {math.sqrt(z2.max()):.2f}; "
          f"pair frequencies, {okp.sum()} cells: mean z^2 = {z2p.mean():.4f}, max |z| = {math.sqrt(z2p.max()):.2f}; dimers seen where exact p = 0: {forced0}; missing where p = 1: {forced1}")
    return z2.mean()


def author(rng):
    x, t, _ = A.grow(n, rng)
    a, b, c, d = A.parts(x)
    return a, b, c, d, t


def referee(rng):
    v = np.zeros((0, 0), np.uint8); t = 0
    for _ in range(n):
        v, k = grow_step(v, rng); t += k
    return (v & 1) != 0, (v & 2) != 0, (v & 4) != 0, (v & 8) != 0, t


run(author, "author's aztec.grow")
run(referee, "referee's sampler")
