"""Second batch of referee controls. Writes controls2.out."""
import json, itertools, re
from collections import Counter
import numpy as np
from scipy.stats import spearmanr

R = '/home/agent2/calib/'
out = json.load(open(R + 'outcomes.json')); items = json.load(open(R + 'items.json'))
ids = [it['id'] for it in items]; ix = {i: j for j, i in enumerate(ids)}
rnd = np.array([it['round'] for it in items]); fil = np.array([it['file'] for it in items])
F = []
for k in range(1, 6):
    d = {}; d.update(json.load(open(R + f'f{k}/A.json'))); d.update(json.load(open(R + f'f{k}/B.json'))); F.append(d)
P = np.array([[F[k][i]['p'] for k in range(5)] for i in ids]); Bs = [[F[k][i]['basis'] for k in range(5)] for i in ids]
y = np.array([out[i] for i in ids]); fc = np.median(P, axis=1); A = rnd == 'A'
maj = np.array([Counter(b).most_common(1)[0][0] for b in Bs])
rng = np.random.default_rng(2); uf = sorted(set(fil))
L = []
def pr(*a):
    s = ' '.join(str(x) for x in a); L.append(s); print(s)
def auc(s, yy):
    a, b = s[yy == 1], s[yy == 0]
    if len(a) == 0 or len(b) == 0: return float('nan')
    return float(((a[:, None] > b[None, :]).sum() + .5 * (a[:, None] == b[None, :]).sum()) / (len(a) * len(b)))
def within(s, yy, f):
    num = den = 0.
    for g in set(f):
        mm = f == g; a = s[mm & (yy == 1)]; b = s[mm & (yy == 0)]
        num += (a[:, None] > b[None, :]).sum() + .5 * (a[:, None] == b[None, :]).sum(); den += len(a) * len(b)
    return (num / den if den else float('nan')), den
def cboot(fn, n=2000):
    o = []
    for _ in range(n):
        pick = rng.choice(len(uf), len(uf))
        s = np.concatenate([np.where(fil == uf[j])[0] for j in pick])
        lab = np.concatenate([np.full((fil == uf[j]).sum(), t) for t, j in enumerate(pick)])
        v = fn(s, lab)
        if np.isfinite(v): o.append(v)
    return np.percentile(o, [2.5, 97.5])
def ch(d):
    yy = y.copy()
    for k, v in d.items(): yy[ix[k]] = v
    return yy

pr('== within-file AUC (a held and a failed expectation from the SAME file)')
for name, m in (('all', np.ones(78, bool)), ('without G3,G4', np.array([i not in ('G3', 'G4') for i in ids])), ('round A', A),
                ('round B', ~A), ('round B without G3,G4', ~A & np.array([i not in ('G3', 'G4') for i in ids]))):
    v, den = within(fc[m], y[m], fil[m])
    lo, hi = cboot(lambda s, lab: within(fc[s][m[s]], y[s][m[s]], lab[m[s]])[0])
    pr('  %-24s %.3f over %d pairs (file-resampled %.2f to %.2f)' % (name, v, den, lo, hi))
bet_n = bet_d = 0.
for j in np.where(y == 1)[0]:
    for k in np.where(y == 0)[0]:
        if fil[j] != fil[k]:
            bet_n += (fc[j] > fc[k]) + .5 * (fc[j] == fc[k]); bet_d += 1
pr('  between-file pairs only: %.3f over %d pairs' % (bet_n / bet_d, bet_d))
pr('  per file: ' + '; '.join('%s %d held/%d failed' % (f, (y[fil == f] == 1).sum(), (y[fil == f] == 0).sum()) for f in uf))
pr('  files with no failure or no hold (contribute no within-file pair): ' + ', '.join(f for f in uf if (y[fil == f] == 1).sum() == 0 or (y[fil == f] == 0).sum() == 0))

pr('\n== letter alone')
sc = np.array([{'T': 2, 'L': 1, 'E': 0}[m] for m in maj], float)
pr('  AUC letter alone %.3f ; share of above-chance AUC: %.2f ; T/L vs E two-level: %.3f' % (auc(sc, y), (auc(sc, y) - .5) / (auc(fc, y) - .5), auc((maj != 'E').astype(float), y)))

pr('\n== strict but principled outcome variant, with and without the two given away')
strict = dict(E4=0, F4=0, K5=0, K6=0, Q4=1, O2=0, O10=0)
for name, d in (('brief rule + O2,O10 by the letter', strict), ('same without G3,G4', dict(strict, G3=.5, G4=.5)),
                ('same, Q4 failed (README: "what I measured was the zig-zag")', dict(strict, Q4=0)),
                ('same, Q4 failed, without G3,G4', dict(strict, Q4=0, G3=.5, G4=.5)),
                ('Noon scoring but halves counted as failed in AUC', dict(E4=0, F4=0, K5=0, K6=0, Q4=0)),
                ('Noon scoring, halves as failed, no G3,G4', dict(E4=0, F4=0, K5=0, K6=0, Q4=0, G3=.5, G4=.5))):
    yy = ch(d); f = yy != .5
    lo, hi = cboot(lambda s, lab: auc(fc[s][f[s]], yy[s][f[s]]))
    pr('  %-62s AUC %.3f (files: %.2f to %.2f) ; within-file %.3f ; E-majority %.3f' % (name, auc(fc[f], yy[f]), lo, hi, within(fc[f], yy[f], fil[f])[0], auc(fc[f & (maj == 'E')], yy[f & (maj == 'E')])))

pr('\n== item-level bootstrap of the headline (Noon: 0.75 to 0.93)')
bs = []
for _ in range(4000):
    s = rng.integers(0, 78, 78); bs.append(auc(fc[s], y[s]))
pr('  %.2f to %.2f' % tuple(np.percentile(bs, [2.5, 97.5])))

pr('\n== five are one: more')
sd = P.std(1); d5 = np.abs(fc - .5); err = np.abs(fc - y)
X = np.column_stack([np.ones(78), d5])
r1 = sd - X @ np.linalg.lstsq(X, sd, rcond=None)[0]; r2 = err - X @ np.linalg.lstsq(X, err, rcond=None)[0]
pr('  spread vs |error|: Spearman %+.2f ; after removing distance of the forecast from 0.5 from both: %+.2f' % (spearmanr(sd, err).correlation, spearmanr(r1, r2).correlation))
for a, b in itertools.combinations(range(5), 2):
    d = (P[:, a] - y) ** 2 - (P[:, b] - y) ** 2
    lo, hi = cboot(lambda s, lab: d[s].mean())
    pr('  Brier f%d - f%d: %+.4f (file-resampled %+.4f to %+.4f)%s' % (a + 1, b + 1, d.mean(), lo, hi, '  *' if lo > 0 or hi < 0 else ''))
pr('  per forecaster, round B AUC without G3,G4: ' + ' '.join('%.3f' % auc(P[~A & (y != .5) & np.array([i not in ('G3', 'G4') for i in ids]), k], y[~A & (y != .5) & np.array([i not in ('G3', 'G4') for i in ids])]) for k in range(5)))
pr('  per forecaster mean p, round A / B: ' + ' '.join('%.3f/%.3f' % (P[A, k].mean(), P[~A, k].mean()) for k in range(5)))
pr('  per forecaster count of p < 0.5 : ' + ' '.join(str((P[:, k] < .5).sum()) for k in range(5)) + ' ; p >= 0.8: ' + ' '.join(str((P[:, k] >= .8 - 1e-9).sum()) for k in range(5)))
pr('  per forecaster: failed with own p < 0.5 (of 26): ' + ' '.join(str(((P[:, k] < .5) & (y == 0)).sum()) for k in range(5)) + ' ; held with own p < 0.5 (of 47): ' + ' '.join(str(((P[:, k] < .5) & (y == 1)).sum()) for k in range(5)))
pr('  per forecaster: own p < 0.30: n / held / failed / half: ' + ' '.join('%d/%d/%d/%d' % ((P[:, k] < .3 - 1e-9).sum(), ((P[:, k] < .3 - 1e-9) & (y == 1)).sum(), ((P[:, k] < .3 - 1e-9) & (y == 0)).sum(), ((P[:, k] < .3 - 1e-9) & (y == .5)).sum()) for k in range(5)))
pr('  per forecaster: own p >= 0.80: n / held / failed / half: ' + ' '.join('%d/%d/%d/%d' % ((P[:, k] >= .8 - 1e-9).sum(), ((P[:, k] >= .8 - 1e-9) & (y == 1)).sum(), ((P[:, k] >= .8 - 1e-9) & (y == 0)).sum(), ((P[:, k] >= .8 - 1e-9) & (y == .5)).sum()) for k in range(5)))
pr('  median forecast: values exactly on a band edge: 0.30 x%d, 0.50 x%d, 0.65 x%d, 0.80 x%d' % tuple((np.abs(fc - v) < 1e-9).sum() for v in (.3, .5, .65, .8)))
pr('\n== ids near the cuts')
for j in np.argsort(fc):
    if fc[j] <= .36 or fc[j] >= .74: pr('  %-4s fc %.2f y %.1f %s' % (ids[j], fc[j], y[j], fil[j]))
open(R + 'referee/controls2.out', 'w').write('\n'.join(L) + '\n')
