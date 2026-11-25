# second sheet, blind: the four new quarter-disc files
import json, glob, os, math
import numpy as np
LINE = 0.37408
rows = {}; allseeds = {}
for f in sorted(glob.glob('/home/agent2/shape-referee/runs2/*.jsonl')):
    b = os.path.basename(f); D = []; bad = 0
    for l in open(f):
        if l.strip():
            try: D.append(json.loads(l))
            except Exception: bad += 1
    x = np.array([d['layers'] for d in D], float); K = len(x)
    keys = sorted(set().union(*[set(d.keys()) for d in D[:50]]))
    n0 = D[0].get('n0', D[0].get('n')); ns = np.array([d.get('n', n0) for d in D])
    m = x.mean(); v = x.var(ddof=1); m4 = ((x - m) ** 4).mean()
    sev = math.sqrt((m4 - (K - 3) / (K - 1) * v * v) / K)
    # r and its error by the delta method on (mean, variance), and by ten thousand-free jackknife over 200 blocks
    r = v * n0 / m ** 2 / LINE
    cov_mv = ((x - m) ** 3).mean() / K
    ser = r * math.sqrt((sev / v) ** 2 + 4 * (v / K) / m ** 2 - 4 * cov_mv / (m * v))
    B = 200; kb = K // B; jk = []
    S1 = x[:kb * B].reshape(B, kb).sum(1); S2 = (x[:kb * B] ** 2).reshape(B, kb).sum(1); t1 = S1.sum(); t2 = S2.sum(); N = kb * B
    for i in range(B):
        nn = N - kb; mm = (t1 - S1[i]) / nn; vv = ((t2 - S2[i]) - nn * mm * mm) / (nn - 1); jk.append(vv * n0 / mm ** 2 / LINE)
    jk = np.array(jk); sejk = math.sqrt((B - 1) / B * ((jk - jk.mean()) ** 2).sum())
    seeds = np.array([d.get('seed', -1) for d in D]); same = np.array([d.get('same', 0) for d in D])
    for s in seeds.tolist(): allseeds[s] = allseeds.get(s, 0) + 1
    bm = np.array([x[i * (K // 10):(i + 1) * (K // 10)].mean() for i in range(10)]); bv = np.array([x[i * (K // 10):(i + 1) * (K // 10)].var(ddof=1) for i in range(10)])
    chim = ((bm - m) ** 2).sum() / (v / (K // 10)); chiv = ((bv - v) ** 2).sum() / (sev ** 2 * 10)
    skew = ((x - m) ** 3).mean() / v ** 1.5; kurt = m4 / v ** 2 - 3
    rows[b] = (r, ser)
    print('%-32s K=%6d n=%6d (all n equal: %s) mean %.3f (%.3f) var %.4f (%.4f) r=%.4f (%.4f; jackknife %.4f)  skew %+.3f kurt %+.3f  ten blocks chi2 means %.1f vars %.1f  lag1 %+.4f  min %d max %d  seeds %d..%d dup %d inorder %s  same: %s  bad %d  keys %s' % (
        b, K, n0, bool((ns == n0).all()), m, math.sqrt(v / K), v, sev, r, ser, sejk, skew, kurt, chim, chiv, np.corrcoef(x[:-1], x[1:])[0, 1], x.min(), x.max(),
        seeds.min(), seeds.max(), K - len(set(seeds.tolist())), bool((np.diff(seeds) > 0).all()), dict(zip(*[a.tolist() for a in np.unique(same, return_counts=True)])), bad, keys))
print('seeds shared between the four files:', sum(1 for s, c in allseeds.items() if c > 1))
def comb(names):
    w = np.array([1 / rows[n][1] ** 2 for n in names]); r = np.array([rows[n][0] for n in names]); mu = (w * r).sum() / w.sum()
    return mu, 1 / math.sqrt(w.sum()), (w * (r - mu) ** 2).sum()
N = sorted(rows); c = [n for n in N if 'cloud' in n]; u = [n for n in N if 'numpy' in n]; big = [n for n in N if '100000' in n]; small = [n for n in N if '-30000' in n]
a = comb(N); print('all four together: r = %.4f (%.4f), %+.1f errors from 1; chi2 among the four %.1f on 3' % (a[0], a[1], (a[0] - 1) / a[1], a[2]))
for nm, A, Bb in (('cloud less numpy', c, u), ('100,000 less 30,000', big, small)):
    p = comb(A); q = comb(Bb); print('%s: %.4f (%.4f) less %.4f (%.4f) = %+.4f (%.4f), %+.1f errors' % (nm, p[0], p[1], q[0], q[1], p[0] - q[0], math.hypot(p[1], q[1]), (p[0] - q[0]) / math.hypot(p[1], q[1])))
for n in N: print('   %s: %+.1f errors from 1' % (n, (rows[n][0] - 1) / rows[n][1]))
