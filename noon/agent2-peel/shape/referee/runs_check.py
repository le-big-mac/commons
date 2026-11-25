# further checks of the raw runs: seeds, where same=1 sits, blocks, regression of N on n in the chance files
import json, glob, os, math
import numpy as np
allseeds = {}
for f in sorted(glob.glob('/home/agent2/shape-referee/runs/*.jsonl')):
    D = [json.loads(l) for l in open(f) if l.strip()]
    x = np.array([d['layers'] for d in D], float); n = np.array([d['n'] for d in D], float)
    seeds = np.array([d['seed'] for d in D]); same = np.array([d['same'] for d in D])
    N = len(x); b = os.path.basename(f)
    for s in seeds.tolist():
        allseeds.setdefault(s, []).append(b)
    contiguous = (np.diff(np.sort(seeds)) == 1).all()
    inorder = (np.diff(seeds) > 0).all()
    pos = np.nonzero(same == 1)[0]
    # ten blocks: chi-square of block means and block variances
    B = 10; k = N // B
    bm = np.array([x[i*k:(i+1)*k].mean() for i in range(B)]); bv = np.array([x[i*k:(i+1)*k].var(ddof=1) for i in range(B)])
    v = x.var(ddof=1)
    chi_m = ((bm - x.mean())**2).sum() / (v / k)
    chi_v = ((bv - v)**2).sum() / (2 * v * v / k)
    # lag-1 correlation in file order
    r1 = np.corrcoef(x[:-1], x[1:])[0, 1]
    line = '%-28s seeds %d..%d contiguous=%s inorder=%s same=1 at rows %s.. step %s  chi2(means,9)=%.1f chi2(vars,9)=%.1f lag1=%+.4f min=%d max=%d' % (
        b, seeds.min(), seeds.max(), contiguous, inorder, pos[:3].tolist(), sorted(set(np.diff(pos).tolist()))[:4], chi_m, chi_v, r1, x.min(), x.max())
    if n.std() > 0:
        sl = np.cov(n, x)[0, 1] / n.var(ddof=1)
        res = x - x.mean() - sl * (n - n.mean())
        rv = res.var(ddof=1) * N / (N - 1)
        m4 = (res**4).mean()
        line += '\n    chance: slope dN/dn=%.6f (2N/3n=%.6f) residual var=%.3f +-%.3f' % (sl, 2 * x.mean() / 3 / n.mean(), rv, math.sqrt((m4 - rv*rv) / N))
    print(line)
dup = {s: v for s, v in allseeds.items() if len(v) > 1}
print('seeds shared between files:', len(dup))
