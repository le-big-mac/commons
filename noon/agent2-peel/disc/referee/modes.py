# pooled (both kinds) mode powers with sampling bias removed, and the decay law on the way in
import sys, glob, math
import numpy as np
sys.argv_keep = sys.argv[:]
n = int(sys.argv[1])
alpha, D = 1.3259, 1.081
RR = [0.2, 0.3, 0.5, 0.7, 0.8]
q = (n / math.pi) ** (1 / 3)
def Pm(m, r):
    if m == 1:
        return D * q / (2 * math.pi) * r ** (2 / 3) * math.log(1 / r)
    return D * q / (2 * math.pi) * 3 * (r ** (2 / 3) - r ** (2 * m * m / 3)) / (2 * (m * m - 1))
fs = sorted(glob.glob('/home/agent2/disc-referee/out_%d_*_*.txt' % n))
X = np.concatenate([np.loadtxt(f, ndmin=2) for f in fs]); K = len(X)
print('n=%d pooled clouds=%d' % (n, K))
V = {r: X[:, 2 + 9 * i + 2] for i, r in enumerate(RR)}
C = {r: X[:, 2 + 9 * i + 3: 2 + 9 * i + 9] for i, r in enumerate(RR)}
NP = {r: X[:, 2 + 9 * i] for i, r in enumerate(RR)}
for r in RR:
    for m in [1, 2, 3]:
        p = (C[r][:, 2 * m - 2] ** 2 + C[r][:, 2 * m - 1] ** 2) / 4
        pc = p - V[r] / NP[r]
        se = p.std(ddof=1) / math.sqrt(K)
        print(' r=%.1f m=%d raw %.3f  bias-removed %.3f +- %.3f  predicted %.3f  ratio %.3f +- %.3f' % (r, m, p.mean(), pc.mean(), se, Pm(m, r), pc.mean() / Pm(m, r), se / Pm(m, r)))
print(' decay on the way in: slope of inner coefficient on outer coefficient (c and s pooled) vs (r_in/r_out)^(m^2/3)')
rg = np.random.default_rng(7)
for (ro, ri) in [(0.8, 0.5), (0.8, 0.3), (0.5, 0.2), (0.7, 0.5)]:
    for m in [1, 2, 3]:
        xo = np.concatenate([C[ro][:, 2 * m - 2], C[ro][:, 2 * m - 1]])
        xi = np.concatenate([C[ri][:, 2 * m - 2], C[ri][:, 2 * m - 1]])
        # attenuation by sampling noise in the outer coefficient: var noise = 2 V/Np
        noise = 2 * (V[ro] / NP[ro]).mean()
        sl = (xo * xi).mean() / ((xo * xo).mean() - noise)
        bs = []
        for _ in range(300):
            ix = rg.integers(0, K, K); ix = np.concatenate([ix, ix + K])
            bs.append((xo[ix] * xi[ix]).mean() / ((xo[ix] ** 2).mean() - noise))
        print('  r %.1f -> %.1f  m=%d  slope %.3f +- %.3f   predicted %.3f' % (ro, ri, m, sl, np.std(bs), (ri / ro) ** (m * m / 3)))
