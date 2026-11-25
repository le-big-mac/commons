# Referee's own statistics of the raw runs: count, mean, variance with standard errors.
import json, sys, glob, os, math
import numpy as np
rows = []
for f in sorted(glob.glob('/home/agent2/shape-referee/runs/*.jsonl')):
    L = []; ns = []; same = []; seeds = []; shapes = set(); kinds = set(); n0s = set(); bad = 0
    for line in open(f):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            bad += 1; continue
        L.append(d['layers']); ns.append(d['n']); same.append(d['same']); seeds.append(d['seed'])
        shapes.add(d['shape']); kinds.add(d['kind']); n0s.add(d['n0'])
    x = np.array(L, float); N = len(x)
    mean = x.mean(); var = x.var(ddof=1)
    m4 = ((x - mean) ** 4).mean()
    sev = math.sqrt(max(m4 - (N - 3) / (N - 1) * var ** 2, 0) / N)
    sem = math.sqrt(var / N)
    skew = ((x - mean) ** 3).mean() / var ** 1.5
    kurt = m4 / var ** 2 - 3
    ns = np.array(ns); same = np.array(same); seeds = np.array(seeds)
    # batch check: variance in 10 consecutive blocks, and first half vs second half means
    h = N // 2
    dz = (x[:h].mean() - x[h:].mean()) / math.sqrt(x[:h].var(ddof=1) / h + x[h:].var(ddof=1) / (N - h))
    # same=1 vs same=-1
    s1 = x[same == 1]; s2 = x[same == -1]
    extra = ''
    if len(s1) > 10 and len(s2) > 10:
        extra = ' same=1: %d mean %.3f var %.2f | same=-1: %d mean %.3f var %.2f' % (
            len(s1), s1.mean(), s1.var(ddof=1), len(s2), s2.mean(), s2.var(ddof=1))
    other = set(np.unique(same)) - {1, -1}
    cn = np.corrcoef(ns, x)[0, 1] if ns.std() > 0 else float('nan')
    print('%-28s N=%6d mean=%9.3f +-%.3f var=%7.3f +-%.3f skew=%+.3f kurt=%+.3f n: mean %.1f var %.1f corr(n,N)=%.3f dupseeds=%d bad=%d halves z=%+.2f same1=%d same-1=%d other=%s shapes=%s kinds=%s n0=%s%s' % (
        os.path.basename(f), N, mean, sem, var, sev, skew, kurt, ns.mean(), ns.var(), cn,
        N - len(set(seeds.tolist())), bad, dz, (same == 1).sum(), (same == -1).sum(), sorted(other),
        sorted(shapes), sorted(kinds), sorted(n0s), extra))
