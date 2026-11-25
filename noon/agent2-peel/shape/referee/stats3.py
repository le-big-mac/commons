# third sheet, blind: five files of discs of exactly N points
import json, glob, os, math
import numpy as np
LINE = 0.37542; AL = 1.3259
rows = []; allseeds = {}
for N in (3000, 10000, 30000, 100000, 300000):
    f = '/home/agent2/shape-referee/runs3/n3-disc-%d.jsonl' % N; D = []; bad = 0
    for l in open(f):
        if l.strip():
            try: D.append(json.loads(l))
            except Exception: bad += 1
    x = np.array([d['layers'] for d in D], float); K = len(x)
    keys = sorted(set().union(*[set(d.keys()) for d in D[:20]]))
    ns = np.array([d.get('n', N) for d in D]); n0 = np.array([d.get('n0', N) for d in D])
    m = x.mean(); v = x.var(ddof=1); m3 = ((x - m) ** 3).mean(); m4 = ((x - m) ** 4).mean()
    sev = math.sqrt((m4 - (K - 3) / (K - 1) * v * v) / K)
    r = v * N / m ** 2 / LINE
    ser = r * math.sqrt((sev / v) ** 2 + 4 * (v / K) / m ** 2 - 4 * (m3 / K) / (m * v))
    B = 200; kb = K // B; S1 = x[:kb * B].reshape(B, kb).sum(1); S2 = (x[:kb * B] ** 2).reshape(B, kb).sum(1); t1 = S1.sum(); t2 = S2.sum(); NN = kb * B; jk = []
    for i in range(B):
        nn = NN - kb; mm = (t1 - S1[i]) / nn; vv = ((t2 - S2[i]) - nn * mm * mm) / (nn - 1); jk.append(vv * N / mm ** 2 / LINE)
    jk = np.array(jk); sejk = math.sqrt((B - 1) / B * ((jk - jk.mean()) ** 2).sum())
    pred = AL * (N / math.pi) ** (2 / 3) * 0.75
    seeds = np.array([d.get('seed', -1) for d in D]); same = np.array([d.get('same', 0) for d in D])
    for s in seeds.tolist(): allseeds[s] = allseeds.get(s, 0) + 1
    k10 = K // 10; bm = np.array([x[i * k10:(i + 1) * k10].mean() for i in range(10)]); bv = np.array([x[i * k10:(i + 1) * k10].var(ddof=1) for i in range(10)])
    chim = ((bm - m) ** 2).sum() / (v / k10); chiv = ((bv - v) ** 2).sum() / (sev ** 2 * 10)
    rows.append((N, r, ser))
    print('N=%6d K=%6d mean %.4f (%.4f) var %.5f (%.5f) r=%.4f (%.4f; jackknife %.4f)  mean - theory %+.4f (%.4f) layers' % (N, K, m, math.sqrt(v / K), v, sev, r, ser, sejk, m - pred, math.sqrt(v / K)))
    print('     skew %+.4f kurt %+.4f  blocks chi2 means %.1f vars %.1f (on 9)  lag1 %+.4f  min %d max %d  n all N: %s n0 all N: %s  seeds %d..%d dup %d in order %s  same %s  bad %d  shapes %s kinds %s keys %s' % (
        m3 / v ** 1.5, m4 / v ** 2 - 3, chim, chiv, np.corrcoef(x[:-1], x[1:])[0, 1], x.min(), x.max(), bool((ns == N).all()), bool((n0 == N).all()), seeds.min(), seeds.max(),
        K - len(set(seeds.tolist())), bool((np.diff(seeds) > 0).all()), dict(zip(*[a.tolist() for a in np.unique(same, return_counts=True)])), bad,
        sorted(set(d.get('shape') for d in D[:1000])), sorted(set(d.get('kind') for d in D[:1000])), keys))
print('seeds shared between files:', sum(1 for s, c in allseeds.items() if c > 1))
R = np.array(rows)
def wls(sel, xf):
    N = R[sel, 0]; y = R[sel, 1]; e = R[sel, 2]; X = np.column_stack([np.ones(len(N)), xf(N)]); W = 1 / e ** 2
    C = np.linalg.inv(X.T @ (X * W[:, None])); b = C @ (X.T @ (W * y)); chi = (W * (y - X @ b) ** 2).sum()
    return b, np.sqrt(np.diag(C)), chi, len(N) - 2, C
four = [1, 2, 3, 4]; five = [0, 1, 2, 3, 4]
b, sb, chi, dof, C = wls(four, lambda N: N ** (-1 / 3))
print('\nFIT r = a + s N^(-1/3), four sizes 10,000 to 300,000: s = %.3f (%.3f) [%.1f errors from 0], a = %.4f (%.4f), chi2 %.2f on %d, corr(a,s) %.2f; predicted at 3,000: %.4f against measured %.4f (%.4f)' % (
    b[1], sb[1], b[1] / sb[1], b[0], sb[0], chi, dof, C[0, 1] / sb[0] / sb[1], b[0] + b[1] * 3000 ** (-1 / 3), R[0, 1], R[0, 2]))
for nm, sel in (('four sizes', four), ('five sizes', five)):
    y = R[sel, 1]; e = R[sel, 2]; mu = (y / e ** 2).sum() / (1 / e ** 2).sum(); print('%s: no lean (a constant): r = %.4f (%.4f), chi2 %.1f on %d' % (nm, mu, 1 / math.sqrt((1 / e ** 2).sum()), (((y - mu) / e) ** 2).sum(), len(sel) - 1))
    for p in (1 / 6, 1 / 4, 1 / 3, 1 / 2, 2 / 3, 1.0):
        b, sb, chi, dof, C = wls(sel, lambda N: N ** (-p)); print('   %s: power -%.3f: s = %9.3f (%.3f), a = %.4f (%.4f), chi2 %.2f on %d' % (nm, p, b[1], sb[1], b[0], sb[0], chi, dof))
    b, sb, chi, dof, C = wls(sel, lambda N: np.log(N / 1e5)); print('   %s: a + s log(N/100,000): s = %.4f (%.4f), value at 100,000 %.4f (%.4f), chi2 %.2f on %d' % (nm, b[1], sb[1], b[0], sb[0], chi, dof))
    ps = np.arange(0.02, 2.001, 0.01); ch = np.array([wls(sel, lambda N: N ** (-p))[2] for p in ps]); i = ch.argmin(); ok = ps[ch <= ch[i] + 1]; ok4 = ps[ch <= ch[i] + 4]
    bb = wls(sel, lambda N: N ** (-ps[i])); print('   %s: free power: best -%.2f (chi2 %.2f on %d, a = %.4f); within 1 of the least chi2: -%.2f to -%.2f; within 4: -%.2f to -%.2f' % (nm, ps[i], ch[i], len(sel) - 3, bb[0][0], ok.min(), ok.max(), ok4.min(), ok4.max()))
# the same as a constant term in the variance: var = c N^(1/3) + b0
print('differences between neighbouring sizes: ' + '; '.join('%d->%d: %+.4f (%.4f)' % (R[i, 0], R[i + 1, 0], R[i + 1, 1] - R[i, 1], math.hypot(R[i, 2], R[i + 1, 2])) for i in range(4)))
