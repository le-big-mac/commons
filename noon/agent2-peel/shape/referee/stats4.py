# fourth sheet, blind: n4-disc-{4,100,300,1000} with the five of runs3
import json, math, os
import numpy as np
AL = 1.3259
def load(f):
    x = []; seeds = []; bad = 0; keys = set(); ns = set(); other = set()
    for l in open(f):
        if l.strip():
            try: d = json.loads(l)
            except Exception: bad += 1; continue
            x.append(d['layers']); seeds.append(d.get('seed', -1)); keys |= set(d.keys()); ns.add(d.get('n')); other.add((d.get('shape'), d.get('kind'), d.get('maker'), d.get('n0')))
    return np.array(x, float), np.array(seeds), bad, sorted(keys), ns, other
# (a)
x, seeds, bad, keys, ns, other = load('runs4/n4-disc-4.jsonl'); K = len(x); p = (x == 1).mean(); ex = 1 - 35 / (12 * math.pi ** 2)
print('(a) N=4: K=%d values %s; share in one layer %.5f (%.5f); exact 1 - 35/(12 pi^2) = %.5f; %+.1f errors; seeds %d..%d dup %d inorder %s bad %d n %s %s' % (
    K, dict(zip(*[a.tolist() for a in np.unique(x, return_counts=True)])), p, math.sqrt(p * (1 - p) / K), ex, (p - ex) / math.sqrt(ex * (1 - ex) / K), seeds.min(), seeds.max(), K - len(set(seeds.tolist())), bool((np.diff(seeds) > 0).all()), bad, ns, other))
h = K // 2; print('    halves: %.5f %.5f; lag1 %+.4f' % ((x[:h] == 1).mean(), (x[h:] == 1).mean(), np.corrcoef(x[:-1], x[1:])[0, 1]))
rows = []; allseeds = set(seeds.tolist()); shared = 0
for N, f in ((100, 'runs4/n4-disc-100.jsonl'), (300, 'runs4/n4-disc-300.jsonl'), (1000, 'runs4/n4-disc-1000.jsonl'), (3000, 'runs3/n3-disc-3000.jsonl'), (10000, 'runs3/n3-disc-10000.jsonl'),
             (30000, 'runs3/n3-disc-30000.jsonl'), (100000, 'runs3/n3-disc-100000.jsonl'), (300000, 'runs3/n3-disc-300000.jsonl')):
    x, seeds, bad, keys, ns, other = load(f); K = len(x); m = x.mean(); v = x.var(ddof=1); m3 = ((x - m) ** 3).mean(); m4 = ((x - m) ** 4).mean()
    sev = math.sqrt((m4 - (K - 3) / (K - 1) * v * v) / K); sem = math.sqrt(v / K); pred = AL * (N / math.pi) ** (2 / 3) * 0.75
    B = 200; kb = K // B; jv = np.array([np.delete(x[:kb * B].reshape(B, kb), i, 0).var(ddof=1) for i in range(0, B, 1)]) if N <= 1000 else None
    sej = math.sqrt((B - 1) / B * ((jv - jv.mean()) ** 2).sum()) if jv is not None else float('nan')
    s = set(seeds.tolist()); shared += len(s & allseeds); allseeds |= s
    k10 = K // 10; bv = np.array([x[i * k10:(i + 1) * k10].var(ddof=1) for i in range(10)]); bm = np.array([x[i * k10:(i + 1) * k10].mean() for i in range(10)])
    rows.append((N, K, m, sem, v, sev))
    print('(b) N=%6d K=%6d mean %9.4f (%.4f) var %.5f (%.5f; jk %.5f)  var/N^(1/3) %.5f  mean-theory %+.4f (%.4f)  skew %+.3f kurt %+.3f  min %d max %d  blocks chi2 vars %.1f means %.1f  halves var %.4f %.4f  lag1 %+.4f  seeds %d..%d dup %d inorder %s bad %d n %s %s' % (
        N, K, m, sem, v, sev, sej, v / N ** (1 / 3), m - pred, sem, m3 / v ** 1.5, m4 / v ** 2 - 3, x.min(), x.max(), ((bv - v) ** 2).sum() / (sev ** 2 * 10), ((bm - m) ** 2).sum() / (v / k10),
        x[:K // 2].var(ddof=1), x[K // 2:].var(ddof=1), np.corrcoef(x[:-1], x[1:])[0, 1], seeds.min(), seeds.max(), K - len(s), bool((np.diff(seeds) > 0).all()), bad, ns, other if N <= 1000 else ''))
print('seeds shared between files:', shared)
R = np.array(rows); Ns = R[:, 0]
def wls(sel, cols, y, e):
    N = Ns[sel]; X = np.column_stack([c(N) for c in cols]); W = 1 / e[sel] ** 2
    C = np.linalg.inv(X.T @ (X * W[:, None])); b = C @ (X.T @ (W * y[sel])); chi = (W * (y[sel] - X @ b) ** 2).sum(); return b, np.sqrt(np.diag(C)), chi, len(N) - len(cols), (y[sel] - X @ b) / e[sel]
subsets = [('all eight, 100 up', list(range(8))), ('300 up', list(range(1, 8))), ('1,000 up', list(range(2, 8))), ('3,000 up', list(range(3, 8))), ('10,000 up', list(range(4, 8))), ('100 to 10,000', list(range(0, 5)))]
V = R[:, 4]; EV = R[:, 5]; one = lambda N: np.ones(len(N)); c13 = lambda N: N ** (1 / 3)
print('\n(c) variance = c N^(1/3) + b')
for nm, sel in subsets:
    b, sb, chi, dof, res = wls(sel, [c13, one], V, EV); print('   %-18s c = %.5f (%.5f)  b = %+.4f (%.4f)  chi2 %.1f on %d   residuals in errors: %s' % (nm, b[0], sb[0], b[1], sb[1], chi, dof, np.round(res, 1).tolist()))
print('   variance = c N^(1/3) + b N^p, p free')
for nm, sel in subsets[:5]:
    ps = [p for p in np.arange(-0.6, 0.301, 0.01) if abs(p - 1 / 3) > 0.03]; ch = np.array([wls(sel, [c13, lambda N, p=p: N ** p], V, EV)[2] for p in ps]); i = ch.argmin(); ok = [p for p, c in zip(ps, ch) if c <= ch[i] + 1]; ok4 = [p for p, c in zip(ps, ch) if c <= ch[i] + 4]
    b, sb, chi, dof, res = wls(sel, [c13, lambda N: N ** ps[i]], V, EV); c0 = wls(sel, [c13, one], V, EV)[2]
    lo = wls(sel, [c13, lambda N: N ** min(ok)], V, EV)[0][0]; hi = wls(sel, [c13, lambda N: N ** max(ok)], V, EV)[0][0]
    print('   %-18s best p = %+.2f (chi2 %.1f on %d; at p = 0 it is %.1f); within 1: %+.2f to %+.2f; within 4: %+.2f to %+.2f; c at best %.5f, over the range within 1: %.5f to %.5f; b at best %+.4f' % (nm, ps[i], chi, dof - 1, c0, min(ok), max(ok), min(ok4), max(ok4), b[0], lo, hi, b[1]))
print('   variance = c N^(1/3) + b + e N^(-1/3)')
for nm, sel in subsets[:4]:
    b, sb, chi, dof, res = wls(sel, [c13, one, lambda N: N ** (-1 / 3)], V, EV); print('   %-18s c = %.5f (%.5f)  b = %+.4f (%.4f)  e = %+.4f (%.4f)  chi2 %.1f on %d' % (nm, b[0], sb[0], b[1], sb[1], b[2], sb[2], chi, dof))
print('   b from neighbouring pairs (c fixed at 0.08226 and at 0.08068): ' + '; '.join('%d: %+.4f, %+.4f (%.4f)' % (R[i, 0], V[i] - 0.08226 * Ns[i] ** (1 / 3), V[i] - 0.08068 * Ns[i] ** (1 / 3), EV[i]) for i in range(8)))
M = R[:, 2]; EM = R[:, 3]; lead = lambda N: (N / math.pi) ** (2 / 3) * 0.75
print('\n(d) mean = A (N/pi)^(2/3) 0.75 + ...')
forms = [('+ m0', [lead, one]), ('+ m0 + m1 N^(-1/3)', [lead, one, lambda N: N ** (-1 / 3)]), ('+ m0 + m1 N^(-2/3)', [lead, one, lambda N: N ** (-2 / 3)]), ('+ k N^(1/3) + m0', [lead, c13, one]),
         ('+ m0 + g log N', [lead, one, lambda N: np.log(N)]), ('+ m0 + m1 N^(-1/3) + m2 N^(-2/3)', [lead, one, lambda N: N ** (-1 / 3), lambda N: N ** (-2 / 3)]), ('+ k N^(1/3) + m0 + m1 N^(-1/3)', [lead, c13, one, lambda N: N ** (-1 / 3)])]
for nm, sel in (subsets[0], subsets[2], subsets[3]):
    for fn, cols in forms:
        if len(sel) - len(cols) < 1: continue
        b, sb, chi, dof, res = wls(sel, cols, M, EM); print('   %-10s %-34s A = %.5f (%.5f)  ' % (nm[:10], fn, b[0], sb[0]) + '  '.join('%+.4f (%.4f)' % (b[i], sb[i]) for i in range(1, len(b))) + '   chi2 %.1f on %d' % (chi, dof))
print('   with A fixed at 1.3259: offsets ' + '; '.join('%d: %+.4f (%.4f)' % (R[i, 0], M[i] - AL * lead(np.array([Ns[i]]))[0], EM[i]) for i in range(8)))
