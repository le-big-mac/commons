# fifth sheet, blind
import json, math, os
import numpy as np
AL, D = 1.3259, 1.081
def load(f):
    x = []; seeds = []; bad = 0; meta = set(); keys = set()
    for l in open(f):
        if l.strip():
            try: d = json.loads(l)
            except Exception: bad += 1; continue
            x.append(d['layers']); seeds.append(d.get('seed', -1)); keys |= set(d.keys()); meta.add((d.get('shape'), d.get('kind'), d.get('maker'), d.get('n0'), d.get('n')))
    return np.array(x, float), np.array(seeds), bad, sorted(keys), meta
def st(x):
    K = len(x); m = x.mean(); v = x.var(ddof=1); m3 = ((x - m) ** 3).mean(); m4 = ((x - m) ** 4).mean()
    return K, m, math.sqrt(v / K), v, math.sqrt((m4 - (K - 3) / (K - 1) * v * v) / K), m3 / v ** 1.5, m4 / v ** 2 - 3
def checks(x, seeds, bad, keys, meta, v, sev):
    K = len(x); k10 = K // 10; bv = np.array([x[i * k10:(i + 1) * k10].var(ddof=1) for i in range(10)]); bm = np.array([x[i * k10:(i + 1) * k10].mean() for i in range(10)])
    return 'min %d max %d blocks chi2 vars %.1f means %.1f halves var %.4f %.4f lag1 %+.4f seeds %d..%d dup %d inorder %s bad %d meta %s keys %s' % (x.min(), x.max(), ((bv - v) ** 2).sum() / (sev ** 2 * 10), ((bm - x.mean()) ** 2).sum() / (v / k10),
        x[:K // 2].var(ddof=1), x[K // 2:].var(ddof=1), np.corrcoef(x[:-1], x[1:])[0, 1], seeds.min(), seeds.max(), K - len(set(seeds.tolist())), bool((np.diff(seeds) > 0).all()), bad, sorted(meta), keys)
Z = np.arange(-8, 8, 0.001) + 0.0005
def lattice(mu, s2, g=0.0):      # Var(round(X)) - s2 - 1/12 for X of mean mu, variance s2, skewness g (Edgeworth)
    s = math.sqrt(s2); pdf = np.exp(-Z * Z / 2) * (1 + g / 6 * (Z ** 3 - 3 * Z)); pdf /= pdf.sum(); y = np.round(mu + s * Z)
    m = (pdf * y).sum(); v = (pdf * (y - m) ** 2).sum(); return v - s2 - 1 / 12, m - mu, (pdf * (y - m) ** 3).sum() / v ** 1.5
meanf = lambda N: 1.32594 * (N / math.pi) ** (2 / 3) * 0.75 + 0.2598 - 0.0178 * math.log(N)
d0 = 10.1648 - meanf(100)                       # anchored on the 100-point clouds of runs4
Vs = lambda N: 0.34208 + 0.08187 * (N ** (1 / 3) - 100 ** (1 / 3))   # the smooth variance: the 100-point clouds with the term off, and the slope of the eight sizes
print('(a) small discs. smooth mean = log form + %.4f; smooth variance anchored at 100 points' % d0)
rows = []; allseeds = set(); shared = 0; chk = []
for N in (83, 90, 98, 105, 113, 120):
    x, seeds, bad, keys, meta = load('runs5/n5-disc-%d.jsonl' % N); K, m, sem, v, sev, sk, ku = st(x); s = set(seeds.tolist()); shared += len(s & allseeds); allseeds |= s
    mp = meanf(N) + d0; L0, dm0, sk0 = lattice(mp, Vs(N) - 1 / 12, 0.0); L1, dm1, sk1 = lattice(mp, Vs(N) - 1 / 12, 0.04)
    rows.append((N, K, m, sem, v, sev, mp, L0, L1, sk, sk1)); chk.append('disc %d: ' % N + checks(x, seeds, bad, keys, meta, v, sev))
    print('   N=%4d K=%6d mean %.4f (%.4f) [smooth %.4f; with the term %.4f] var %.5f (%.5f)  smooth var %.5f  swing measured %+.5f (%.5f)  predicted: normal %+.5f, skew 0.04 %+.5f   skewness %+.3f (rounded quantity %+.3f) kurt %+.3f' % (
        N, K, m, sem, mp, mp + dm1, v, sev, Vs(N), v - Vs(N), sev, L0, L1, sk, sk1, ku))
R = np.array([r[:10] for r in rows]); sw = R[:, 4] - np.array([Vs(n) for n in R[:, 0]]); e = R[:, 5]; W = 1 / e ** 2
for nm, L in (('normal', R[:, 7]), ('skew 0.04', R[:, 8])):
    X = np.column_stack([L, np.ones(6)]); C = np.linalg.inv(X.T @ (X * W[:, None])); b = C @ (X.T @ (W * sw)); chi = (W * (sw - X @ b) ** 2).sum()
    chi1 = (W * (sw - L - ((W * (sw - L)).sum() / W.sum())) ** 2).sum()
    print('   swing = k x predicted (%s) + const: k = %.2f (%.2f), const %+.4f (%.4f), chi2 %.1f on 4;  with k = 1 fixed: const %+.4f, chi2 %.1f on 5' % (nm, b[0], math.sqrt(C[0, 0]), b[1], math.sqrt(C[1, 1]), chi, (W * (sw - L)).sum() / W.sum(), chi1))
mu0 = (W * sw).sum() / W.sum(); print('   a level run (no swing): const %+.4f, chi2 %.1f on 5;  measured swing peak to trough %.4f, predicted %.4f (normal), %.4f (skew)' % (mu0, (W * (sw - mu0) ** 2).sum(), sw.max() - sw.min(), R[:, 7].max() - R[:, 7].min(), R[:, 8].max() - R[:, 8].min()))
# (b) shapes
TH = {'disc': 0.080695, 'triangle': 0.738090 * 0.285315 - 0.169797 * 0.819926 ** 2, 'rtriangle': 0.738090 * 0.268259 - 0.169797 * 0.803421 ** 2}
TT = {'disc': 0.75, 'triangle': 0.819926, 'rtriangle': 0.803421}; RATIO = 0.08205 / 0.080695
print('\n(b) shapes. theory variance per n^(1/3): disc %.6f, triangle %.6f, rtriangle %.6f; the disc\'s fitted coefficient ratio %.5f' % (TH['disc'], TH['triangle'], TH['rtriangle'], RATIO))
S = {('disc', 300): (20.9360, 0.0011, 0.51067, 0.00114), ('disc', 1000): (46.4980, 0.0014, 0.77769, 0.00174), ('disc', 3000): (96.5521, 0.0017, 1.13945, 0.00254)}
for sh, N, f in (('cdisc', 1000, 'n5-cdisc-1000'), ('triangle', 300, 'n5-triangle-300'), ('triangle', 1000, 'n5-triangle-1000'), ('triangle', 3000, 'n5-triangle-3000'), ('rtriangle', 300, 'n5-rtriangle-300'), ('rtriangle', 1000, 'n5-rtriangle-1000'), ('rtriangle', 3000, 'n5-rtriangle-3000')):
    x, seeds, bad, keys, meta = load('runs5/%s.jsonl' % f); K, m, sem, v, sev, sk, ku = st(x); s = set(seeds.tolist()); shared += len(s & allseeds); allseeds |= s
    S[(sh, N)] = (m, sem, v, sev); chk.append('%s %d: ' % (sh, N) + checks(x, seeds, bad, keys, meta, v, sev)); S[(sh, N, 'K')] = K; S[(sh, N, 'sk')] = (sk, ku)
M = {}
for (key, val) in list(S.items()):
    if len(key) != 2: continue
    sh, N = key; base = 'disc' if sh == 'cdisc' else sh; m, sem, v, sev = val; th = TH[base] * N ** (1 / 3); lat = lattice(m, max(v - 1 / 12, 0.05), 0.04)[0]
    M[key] = (v - RATIO * th, sev, th, lat)
    print('   %-9s N=%5d K=%s mean %.4f (%.4f) less 1.3259 rho^(2/3) T: %+.4f   var %.5f (%.5f)  theory %.5f  var/theory %.4f (%.4f)  missing = var - %.4f x theory = %+.5f (%.5f)  as a share of the theory\'s %+.4f (%.4f)  whole-number term there %+.5f' % (
        sh, N, S.get((sh, N, 'K'), 'earlier'), m, sem, m - AL * (N / math.pi) ** (2 / 3) * TT[base], v, sev, th, v / th, sev / th, RATIO, v - RATIO * th, sev, (v - RATIO * th) / th, sev / th, lat))
print('   generators at 1,000 points: cloud.c disc less first-generator disc: variance %+.5f (%.5f), mean %+.4f (%.4f)' % (S[('cdisc', 1000)][2] - S[('disc', 1000)][2], math.hypot(S[('cdisc', 1000)][3], S[('disc', 1000)][3]), S[('cdisc', 1000)][0] - S[('disc', 1000)][0], math.hypot(S[('cdisc', 1000)][1], S[('disc', 1000)][1])))
def cmp(a, b, name, share=False, scale=None):
    out = []; num = den = 0.0
    for N in (300, 1000, 3000):
        ma, ea, tha, la = M[(a, N)]; mb, eb, thb, lb = M[(b, N)]
        if share: da = ma / tha - mb / thb; ee = math.hypot(ea / tha, eb / thb)
        else: da = ma - mb; ee = math.hypot(ea, eb)
        out.append('%d: %+.4f (%.4f)' % (N, da, ee)); num += da / ee ** 2; den += 1 / ee ** 2
    print('   %-66s %s; pooled %+.4f (%.4f), %+.1f errors' % (name, '; '.join(out), num / den, 1 / math.sqrt(den), num / den * math.sqrt(den)))
cmp('triangle', 'disc', 'missing, triangle less disc (the same amount says 0):'); cmp('rtriangle', 'disc', 'missing, rounded triangle less disc:'); cmp('triangle', 'rtriangle', 'missing, triangle less rounded triangle (corners say below 0):')
cmp('triangle', 'disc', 'missing as a share of its theory, triangle less disc (same share says 0):', True); cmp('rtriangle', 'disc', 'the same, rounded triangle less disc:', True); cmp('triangle', 'rtriangle', 'the same, triangle less rounded triangle:', True)
# (c)
E8 = [(100, 0.33863 + 0.00345, 0.00079), (300, 0.51067 + 0.00036, 0.00114), (1000, 0.77769, 0.00174), (3000, 1.13945, 0.00254), (10000, 1.72297, 0.00385), (30000, 2.51300, 0.00561), (100000, 3.76588, 0.00974), (300000, 5.46366, 0.01990)]
A6 = [(r[0], r[4] - r[8], r[5]) for r in rows]; A6raw = [(r[0], r[4], r[5]) for r in rows]
def fits(data, name):
    N = np.array([d[0] for d in data], float); V = np.array([d[1] for d in data]); E = np.array([d[2] for d in data]); W = 1 / E ** 2
    def fit(cols):
        X = np.column_stack([c(N) for c in cols]); C = np.linalg.inv(X.T @ (X * W[:, None])); b = C @ (X.T @ (W * V)); return b, np.sqrt(np.diag(C)), (W * (V - X @ b) ** 2).sum(), (V - X @ b) / E
    b, sb, chi, res = fit([lambda n: n ** (1 / 3), lambda n: np.ones(len(n))])
    ps = [p for p in np.arange(-0.4, 0.3001, 0.005) if abs(p - 1 / 3) > 0.03]; ch = np.array([fit([lambda n: n ** (1 / 3), lambda n, p=p: n ** p])[2] for p in ps]); i = ch.argmin(); ok = [p for p, c in zip(ps, ch) if c <= ch[i] + 1]; ok4 = [p for p, c in zip(ps, ch) if c <= ch[i] + 4]
    bb = fit([lambda n: n ** (1 / 3), lambda n: n ** ps[i]])
    print('   %-44s c = %.5f (%.5f) b = %+.4f (%.4f) chi2 %.1f on %d | power of the lean free: %.2f (within 1: %.2f to %.2f; within 4: %.2f to %.2f), chi2 %.1f, a constant is %.1f above; c then %.5f | residuals %s' % (
        name, b[0], sb[0], b[1], sb[1], chi, len(N) - 2, ps[i] - 1 / 3, min(ok) - 1 / 3, max(ok) - 1 / 3, min(ok4) - 1 / 3, max(ok4) - 1 / 3, ch[i], chi - ch[i], bb[0][0], np.round(res, 1).tolist()))
print('\n(c) variance with the whole-number term off (skew 0.04), c n^(1/3) + b')
fits(A6 + E8, 'fourteen sizes, 83 to 300,000'); fits(A6 + E8[:1], 'seven sizes, 83 to 120'); fits(E8, 'the eight earlier sizes'); fits(A6 + E8[:5], '83 to 10,000'); fits(A6raw + [(100, 0.33863, 0.00079), (300, 0.51067, 0.00114)] + E8[2:], 'fourteen sizes, the term NOT taken off')
print('   B = variance (term off) - 0.08205 n^(1/3): ' + '; '.join('%d: %+.4f (%.4f)' % (d[0], d[1] - 0.08205 * d[0] ** (1 / 3), d[2]) for d in sorted(A6 + E8[:3])))
print('   B raw: ' + '; '.join('%d: %+.4f' % (d[0], d[1] - 0.08205 * d[0] ** (1 / 3)) for d in sorted(A6raw + [(100, 0.33863, 0)])))
print('\n(d) checks'); print('\n'.join(chk)); print('seeds shared among the thirteen files:', shared)
