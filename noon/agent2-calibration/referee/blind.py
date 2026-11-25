"""Blind recomputation. Reads only outcomes.json, items.json, f1..f5/A.json,B.json."""
import json, itertools, sys
from collections import Counter
import numpy as np
from scipy.stats import spearmanr

R = '/home/agent2/calib/'
out = json.load(open(R + 'outcomes.json'))
items = json.load(open(R + 'items.json'))
ids = [it['id'] for it in items]
rnd = {it['id']: it['round'] for it in items}
fil = {it['id']: it['file'] for it in items}
F = []
for k in range(1, 6):
    d = {}
    d.update(json.load(open(R + f'f{k}/A.json')))
    d.update(json.load(open(R + f'f{k}/B.json')))
    F.append(d)
assert set(ids) == set(out), (set(ids) ^ set(out))
for k, d in enumerate(F):
    assert set(d) == set(ids), (k, set(d) ^ set(ids))

P = np.array([[F[k][i]['p'] for k in range(5)] for i in ids])  # 78 x 5
B = [[F[k][i]['basis'] for k in range(5)] for i in ids]
y = np.array([out[i] for i in ids])
med = np.median(P, axis=1)


def auc(score, yy):
    pos = score[yy == 1]; neg = score[yy == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float('nan')
    w = 0.0
    for a in pos:
        w += (a > neg).sum() + 0.5 * (a == neg).sum()
    return w / (len(pos) * len(neg))


L = []
def pr(*a):
    s = ' '.join(str(x) for x in a)
    L.append(s); print(s)

pr('1. n =', len(ids), ' held', int((y == 1).sum()), ' failed', int((y == 0).sum()), ' half', int((y == 0.5).sum()),
   ' mean outcome %.4f' % y.mean())
pr('   round A: n', sum(rnd[i] == 'A' for i in ids), ' round B: n', sum(rnd[i] == 'B' for i in ids))
pr('2. forecast = median of five; mean forecast %.4f  (mean of means %.4f)' % (med.mean(), P.mean()))
A = np.array([rnd[i] == 'A' for i in ids])
pr('3. AUC all %.4f (n1=%d,n0=%d)  A %.4f (n1=%d,n0=%d)  B %.4f (n1=%d,n0=%d)' % (
    auc(med, y), (y == 1).sum(), (y == 0).sum(),
    auc(med[A], y[A]), (y[A] == 1).sum(), (y[A] == 0).sum(),
    auc(med[~A], y[~A]), (y[~A] == 1).sum(), (y[~A] == 0).sum()))
pr('   per forecaster AUC all: ' + ' '.join('%.3f' % auc(P[:, k], y) for k in range(5)))
pr('   per forecaster mean p : ' + ' '.join('%.3f' % P[:, k].mean() for k in range(5)))
pr('   AUC of mean-of-five: %.4f' % auc(P.mean(axis=1), y))
pr('4. Brier forecast %.4f   Brier constant(mean outcome) %.4f   (halves dropped: %.4f vs %.4f)' % (
    ((med - y) ** 2).mean(), ((y.mean() - y) ** 2).mean(),
    ((med[y != .5] - y[y != .5]) ** 2).mean(), ((y[y != .5].mean() - y[y != .5]) ** 2).mean()))
pr('   per forecaster Brier: ' + ' '.join('%.4f' % ((P[:, k] - y) ** 2).mean() for k in range(5)))
rs = [spearmanr(P[:, a], P[:, b]).correlation for a, b in itertools.combinations(range(5), 2)]
pr('5. mean pairwise Spearman %.4f  (min %.3f max %.3f)' % (np.mean(rs), min(rs), max(rs)))
lo = med < 0.30; hi = med >= 0.80
def share(m):
    return 'n=%d held=%d failed=%d half=%d  share held (halves as non-held) %.3f, mean outcome %.3f' % (
        m.sum(), (y[m] == 1).sum(), (y[m] == 0).sum(), (y[m] == .5).sum(),
        (y[m] == 1).mean() if m.sum() else float('nan'), y[m].mean() if m.sum() else float('nan'))
pr('6. forecast <0.30 : ' + share(lo))
pr('   forecast >=0.80: ' + share(hi))
pr('   0.30..0.80     : ' + share(~lo & ~hi))
maj = []
for b in B:
    c = Counter(b).most_common(1)[0]
    maj.append(c[0] if c[1] >= 3 else 'none')
maj = np.array(maj)
pr('7. majority letter:')
for l in ['T', 'L', 'E', 'none']:
    m = maj == l
    pr('   %-4s ' % l + share(m) + '  mean forecast %.3f' % (med[m].mean() if m.sum() else float('nan')))
m = maj == 'E'
pr('   AUC within E-majority %.4f (n1=%d,n0=%d)' % (auc(med[m], y[m]), (y[m] == 1).sum(), (y[m] == 0).sum()))
pr('   AUC within non-E      %.4f (n1=%d,n0=%d)' % (auc(med[~m], y[~m]), (y[~m] == 1).sum(), (y[~m] == 0).sum()))
pr('8. failed with forecast <0.5: %d of %d ;  held with forecast <0.5: %d of %d ; half <0.5: %d of %d' % (
    ((y == 0) & (med < .5)).sum(), (y == 0).sum(), ((y == 1) & (med < .5)).sum(), (y == 1).sum(),
    ((y == .5) & (med < .5)).sum(), (y == .5).sum()))
pr('   (forecast exactly 0.5: %d)' % (med == .5).sum())
open(R + 'referee/blind.out', 'w').write('\n'.join(L) + '\n')
