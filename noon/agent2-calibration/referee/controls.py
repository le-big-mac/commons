"""Referee controls (after reading the README). Writes controls.out."""
import json, itertools, re, sys
from collections import Counter
import numpy as np
from scipy.stats import spearmanr, binomtest

R = '/home/agent2/calib/'
out = json.load(open(R + 'outcomes.json'))
items = json.load(open(R + 'items.json'))
ids = [it['id'] for it in items]
ix = {i: j for j, i in enumerate(ids)}
rnd = np.array([it['round'] for it in items]); fil = np.array([it['file'] for it in items])
text = [it['text'] for it in items]
F = []
for k in range(1, 6):
    d = {}
    d.update(json.load(open(R + f'f{k}/A.json'))); d.update(json.load(open(R + f'f{k}/B.json')))
    F.append(d)
P = np.array([[F[k][i]['p'] for k in range(5)] for i in ids])
Bs = [[F[k][i]['basis'] for k in range(5)] for i in ids]
y = np.array([out[i] for i in ids]); fc = np.median(P, axis=1)
maj = np.array([Counter(b).most_common(1)[0][0] for b in Bs])
A = rnd == 'A'
rng = np.random.default_rng(1)
L = []
def pr(*a):
    s = ' '.join(str(x) for x in a); L.append(s); print(s)

def auc(s, yy):
    a, b = s[yy == 1], s[yy == 0]
    if len(a) == 0 or len(b) == 0: return float('nan')
    return float(((a[:, None] > b[None, :]).sum() + .5 * (a[:, None] == b[None, :]).sum()) / (len(a) * len(b)))
def mask(excl): return np.array([i not in excl for i in ids])
def brier(p, yy): return float(((p - yy) ** 2).mean())
def cboot(fn, n=2000):
    uf = sorted(set(fil)); o = []
    for _ in range(n):
        s = np.concatenate([np.where(fil == uf[j])[0] for j in rng.choice(len(uf), len(uf))])
        v = fn(s)
        if np.isfinite(v): o.append(v)
    return np.percentile(o, [2.5, 97.5])

pr('== item table: id file round outcome forecast five letters')
for j, i in enumerate(ids):
    pr('  %-4s %-24s %s y=%.1f fc=%.2f  %s  %s' % (i, fil[j], rnd[j], y[j], fc[j], ' '.join('%.2f' % p for p in P[j]), ''.join(Bs[j])))

pr('\n== LEAKS: AUC with sets removed (all / round B / E-majority)')
sets = {'none': [], 'G3,G4 (Noon)': ['G3', 'G4'],
        'G3,G4 + Q1,Q4 (file reports own numbers)': ['G3', 'G4', 'Q1', 'Q4'],
        'G3,G4 + Q1,Q4 + H3,H5 (direction hedge in same file)': ['G3', 'G4', 'Q1', 'Q4', 'H3', 'H5'],
        'whole G file + H file': [i for i in ids if i[0] in 'GH' and rnd[ix[i]] == 'B'],
        'all three antipodes follow-ups (F,G,H)': [i for i in ids if i[0] in 'FGH' and rnd[ix[i]] == 'B']}
for n, ex in sets.items():
    m = mask(ex); E = maj == 'E'
    pr('  %-55s all %.3f (n=%d)  roundB %.3f  E-maj %.3f (held %d failed %d)  E-maj roundA %.3f' % (
        n, auc(fc[m], y[m]), m.sum(), auc(fc[m & ~A], y[m & ~A]), auc(fc[m & E], y[m & E]),
        (y[m & E] == 1).sum(), (y[m & E] == 0).sum(), auc(fc[m & E & A], y[m & E & A])))
m = mask(['G3', 'G4'])
lo, hi = cboot(lambda s: auc(fc[s][m[s]], y[s][m[s]])); pr('  file-resampled interval, no G3/G4: %.2f to %.2f' % (lo, hi))
lo, hi = cboot(lambda s: auc(fc[s][(maj == 'E')[s] & m[s]], y[s][(maj == 'E')[s] & m[s]])); pr('  file-resampled interval, E-majority no G3/G4: %.2f to %.2f' % (lo, hi))
lo, hi = cboot(lambda s: auc(fc[s][~A[s]], y[s][~A[s]])); pr('  file-resampled interval, round B (5 files): %.2f to %.2f' % (lo, hi))
pr('  G3 G4 letters:', ''.join(Bs[ix['G3']]), ''.join(Bs[ix['G4']]), ' forecasts', fc[ix['G3']], fc[ix['G4']])
pr('  round-A items whose result a B file quotes (E2, K2, K7): per forecaster p')
for i in ['E2', 'K2', 'K3', 'K7']:
    pr('    ', i, 'y=%.1f' % y[ix[i]], P[ix[i]])
pr('  per forecaster AUC round A: ' + ' '.join('%.3f' % auc(P[A, k], y[A]) for k in range(5)) + '   round B: ' + ' '.join('%.3f' % auc(P[~A, k], y[~A]) for k in range(5)))

pr('\n== FORM RULES (from items.json text only; higher score = more likely to hold). 7 rules tried, all shown.')
def n_and(t): return len(re.findall(r'\band\b', t)) + t.count(';')
rules = {
    '1 fewer "and"/";"': np.array([-n_and(t) for t in text], float),
    '2 shorter text (chars)': np.array([-len(t) for t in text], float),
    '3 fewer numbers in text': np.array([-len(re.findall(r'\d+(?:[.,]\d+)?', t)) for t in text], float),
    '4 no "between"': np.array([0. if re.search(r'\bbetween\b', t, re.I) else 1. for t in text]),
    '5 one-sided wording (at least/at most/or more/fewer|less|more than/above/below), no "between"': np.array(
        [1. if (re.search(r'at least|at most|or more|fewer than|less than|more than|above|below|no more', t, re.I) and not re.search(r'\bbetween\b', t, re.I)) else 0. for t in text]),
    '6 hedge/anchor words (theorem, test of my, from memory, Hopkins, 2025:)': np.array(
        [1. if re.search(r'theorem|test of my|from memory|Hopkins|2025:|NCEP/NCAR 2025', t, re.I) else 0. for t in text]),
}
z = lambda v: (v - v.mean()) / (v.std() or 1)
rules['7 sum of z-scores of 1, 3 and 6'] = z(rules['1 fewer "and"/";"']) + z(rules['3 fewer numbers in text']) + z(rules[[k for k in rules if k[0] == '6'][0]])
for n, s in rules.items():
    m2 = mask(['G3', 'G4'])
    pr('  %-90s AUC all %.3f  roundA %.3f  E-maj %.3f | Spearman with forecast %+.2f' % (
        n, auc(s, y), auc(s[A], y[A]), auc(s[maj == 'E'], y[maj == 'E']), spearmanr(s, fc).correlation))
s7 = rules['7 sum of z-scores of 1, 3 and 6']
lo, hi = cboot(lambda s: auc(s7[s], y[s])); pr('  rule 7 file-resampled interval: %.2f to %.2f' % (lo, hi))
# forecast within strata of clause count
nc = np.array([n_and(t) for t in text]); st = np.minimum(nc, 2)
num = den = 0.
for v in (0, 1, 2):
    mm = st == v; a = fc[mm & (y == 1)]; b = fc[mm & (y == 0)]
    c = (a[:, None] > b[None, :]).sum() + .5 * (a[:, None] == b[None, :]).sum()
    pr('  forecast AUC among items with %s and/; : %.3f (held %d, failed %d, mean outcome %.2f, mean forecast %.2f)' % (
        ['0', '1', '2+'][v], c / max(1, len(a) * len(b)), len(a), len(b), y[mm].mean(), fc[mm].mean()))
    num += c; den += len(a) * len(b)
pr('  forecast AUC pooled within clause-count strata: %.3f' % (num / den))
# residual of forecast after linear fit on rules 1,3,6
X = np.column_stack([np.ones(len(y)), z(rules['1 fewer "and"/";"']), z(rules['3 fewer numbers in text']), rules[[k for k in rules if k[0] == '6'][0]]])
beta = np.linalg.lstsq(X, fc, rcond=None)[0]; res = fc - X @ beta
pr('  forecast regressed on rules 1,3,6: R^2 = %.2f ; AUC of the fitted part %.3f ; AUC of the residual %.3f' % (
    1 - res.var() / fc.var(), auc(X @ beta, y), auc(res, y)))

pr('\n== FILES: between-file and within-file')
fm = np.array([fc[fil == f].mean() for f in fil])
pr('  AUC of the file-mean forecast (every item gets its file mean): %.3f ; of forecast minus file mean: %.3f' % (auc(fm, y), auc(fc - fm, y)))
num = den = 0.
for f in sorted(set(fil)):
    mm = fil == f; a = fc[mm & (y == 1)]; b = fc[mm & (y == 0)]
    num += (a[:, None] > b[None, :]).sum() + .5 * (a[:, None] == b[None, :]).sum(); den += len(a) * len(b)
pr('  within-file AUC (pairs in the same file only): %.3f over %d pairs' % (num / den, den))
ym = np.array([(y[(fil == f) & (np.arange(len(y)) != j)].mean()) for j, f in enumerate(fil)])
pr('  AUC of "share held among the OTHER expectations of the same file" (not available to forecasters; shows clustering): %.3f' % auc(ym, y))

pr('\n== OUTCOME VARIANTS')
def variant(name, ch):
    yy = y.copy()
    for k, v in ch.items(): yy[ix[k]] = v
    full = yy != .5
    pr('  %-78s held %d failed %d half %d | mean %.3f gap %+.3f | AUC %.3f A %.3f B %.3f E %.3f | Brier %.4f vs %.4f | <0.5: failed %d/%d held %d/%d | fc>=0.8 failed %d | fc<0.3 held %d' % (
        name, (yy == 1).sum(), (yy == 0).sum(), (yy == .5).sum(), yy.mean(), fc.mean() - yy.mean(),
        auc(fc[full], yy[full]), auc(fc[A], yy[A]), auc(fc[~A], yy[~A]), auc(fc[maj == 'E'], yy[maj == 'E']),
        brier(fc, yy), brier(np.full(len(yy), yy.mean()), yy),
        ((yy == 0) & (fc < .5)).sum(), (yy == 0).sum(), ((yy == 1) & (fc < .5)).sum(), (yy == 1).sum(),
        ((yy == 0) & (fc >= .8)).sum(), ((yy == 1) & (fc < .3)).sum()))
    return yy
variant('Noon', {})
yb = variant('brief rule "in full": E4,F4,K5,K6 -> failed; Q4 (held by the letter) -> held', dict(E4=0, F4=0, K5=0, K6=0, Q4=1))
variant('same + O2,O10 by the letter -> failed', dict(E4=0, F4=0, K5=0, K6=0, Q4=1, O2=0, O10=0))
variant('all halves -> failed + O2,O10 failed', dict(E4=0, F4=0, K5=0, K6=0, Q4=0, O2=0, O10=0))
variant('same, and without G3,G4 (set to half = left out of AUC)', dict(E4=0, F4=0, K5=0, K6=0, Q4=0, O2=0, O10=0, G3=.5, G4=.5))
variant('narrow misses flipped to held (B2 by 0.2km, H3 2.24 vs 2.2, C1 .68, C2 .74, C3 .83)', dict(B2=1, H3=1, C1=1, C2=1, C3=1))
variant('barely-held flipped to failed (G2 20.9, S2 7.3)', dict(G2=0, S2=0))
pr('  forecasts: O2 %.2f O10 %.2f E4 %.2f F4 %.2f K5 %.2f K6 %.2f Q4 %.2f' % tuple(fc[ix[i]] for i in ['O2', 'O10', 'E4', 'F4', 'K5', 'K6', 'Q4']))
pr('  highest forecast that failed (Noon scoring): %.2f ; items with forecast above it: %d' % (fc[y == 0].max(), (fc > fc[y == 0].max()).sum()))
pr('  lowest forecast that held: %.2f ; items below it: %d ; items at or below 0.30: %s ; under 0.35: %s' % (
    fc[y == 1].min(), (fc < fc[y == 1].min()).sum(), Counter(y[fc <= .30].tolist()), Counter(y[fc < .35].tolist())))

pr('\n== FIVE ARE ONE')
rs = [spearmanr(P[:, a], P[:, b]).correlation for a, b in itertools.combinations(range(5), 2)]
pr('  Spearman mean %.3f' % np.mean(rs))
w = [(np.abs(P[:, a] - P[:, b]) <= .05 + 1e-9).mean() for a, b in itertools.combinations(range(5), 2)]
w0 = [(np.abs(P[:, a] - P[:, b]) <= .05).mean() for a, b in itertools.combinations(range(5), 2)]
pr('  pairs within 0.05: %.3f with a float tolerance, %.3f with a bare <= (Noon), strictly under 0.05: %.3f' % (
    np.mean(w), np.mean(w0), np.mean([(np.abs(P[:, a] - P[:, b]) < .05 - 1e-9).mean() for a, b in itertools.combinations(range(5), 2)])))
rg = P.max(1) - P.min(1)
pr('  range of the five per item: mean %.3f median %.3f ; items with range >= 0.20: %d ; >= 0.30: %d' % (rg.mean(), np.median(rg), (rg >= .2 - 1e-9).sum(), (rg >= .3 - 1e-9).sum()))
pr('  items where the five are not all on one side of 0.5 (0.5 itself counted with neither): %d' % sum(1 for j in range(len(ids)) if (P[j] > .5).any() and (P[j] < .5).any()))
pr('  letters unanimous on %d of 78 ; split 4-1: %d ; 3-2: %d' % (sum(len(set(b)) == 1 for b in Bs), sum(Counter(b).most_common(1)[0][1] == 4 for b in Bs), sum(Counter(b).most_common(1)[0][1] == 3 for b in Bs)))
# within-file agreement (remove file means)
Pw = P.copy()
for f in set(fil): Pw[fil == f] -= P[fil == f].mean(0)
pr('  Spearman after removing each forecaster\'s file means: %.3f' % np.mean([spearmanr(Pw[:, a], Pw[:, b]).correlation for a, b in itertools.combinations(range(5), 2)]))
E = maj == 'E'
pr('  Spearman among E-majority items only: %.3f ; among items with median in 0.3..0.7 (n=%d): %.3f' % (
    np.mean([spearmanr(P[E, a], P[E, b]).correlation for a, b in itertools.combinations(range(5), 2)]), ((fc >= .3) & (fc <= .7)).sum(),
    np.mean([spearmanr(P[(fc >= .3) & (fc <= .7), a], P[(fc >= .3) & (fc <= .7), b]).correlation for a, b in itertools.combinations(range(5), 2)])))
full = y != .5
for k in range(5):
    oth = np.median(np.delete(P, k, axis=1), axis=1); dev = P[:, k] - oth
    pr('  forecaster %d: AUC %.3f; AUC of median of the other four %.3f; corr(own deviation, y - others) = %+.2f; mean deviation %+.3f' % (
        k + 1, auc(P[full, k], y[full]), auc(oth[full], y[full]), np.corrcoef(dev, y - oth)[0, 1], dev.mean()))
# paired comparison best vs worst forecaster: item-resampled diff in Brier
d = (P[:, 3] - y) ** 2 - (P[:, 0] - y) ** 2
bs = [d[rng.integers(0, 78, 78)].mean() for _ in range(4000)]
pr('  Brier f4 minus f1: %+.4f (item-resampled %.4f to %.4f)' % (d.mean(), *np.percentile(bs, [2.5, 97.5])))
sd = P.std(1)
pr('  does spread flag error? Spearman(sd of five, |forecast - outcome|) = %+.2f' % spearmanr(sd, np.abs(fc - y)).correlation)

pr('\n== TOO DOUBTFUL')
for name, yy in (('Noon (half=0.5)', y), ('in full (brief rule)', yb)):
    g = fc.mean() - yy.mean()
    lo, hi = cboot(lambda s: fc[s].mean() - yy[s].mean())
    fg = np.array([fc[fil == f].mean() - yy[fil == f].mean() for f in sorted(set(fil))])
    pr('  %-22s gap %+.3f ; file-resampled %.3f to %+.3f ; files with forecast below outcome: %d of 14 (above: %d) ; mean of file gaps %+.3f, t = %.2f ; sign test p = %.3f' % (
        name, g, lo, hi, (fg < 0).sum(), (fg > 0).sum(), fg.mean(), fg.mean() / (fg.std(ddof=1) / np.sqrt(14)), binomtest(int((fg < 0).sum()), int((fg != 0).sum())).pvalue))
    pr('     round A gap %+.3f ; round B gap %+.3f ; leave one file out: gap from %+.3f to %+.3f' % (
        fc[A].mean() - yy[A].mean(), fc[~A].mean() - yy[~A].mean(),
        min(fc[fil != f].mean() - yy[fil != f].mean() for f in set(fil)), max(fc[fil != f].mean() - yy[fil != f].mean() for f in set(fil))))
    for bands in ([0, .3, .5, .65, .8, 1.01], [0, .2, .4, .6, .8, 1.01], [0, .25, .5, .75, 1.01]):
        pr('     bands ' + ' | '.join('%.2f-%.2f n=%d said %.2f got %.2f' % (a, min(b, 1), ((fc >= a) & (fc < b)).sum(), fc[(fc >= a) & (fc < b)].mean(), yy[(fc >= a) & (fc < b)].mean()) for a, b in zip(bands[:-1], bands[1:]) if ((fc >= a) & (fc < b)).sum()))
# calibration slope on logit scale (Newton logistic), items with y in {0,1}
def logit_fit(p, yy):
    x = np.log(p / (1 - p)); Xm = np.column_stack([np.ones(len(x)), x]); b = np.zeros(2)
    for _ in range(50):
        mu = 1 / (1 + np.exp(-Xm @ b)); W = mu * (1 - mu)
        b = b + np.linalg.solve(Xm.T @ (Xm * W[:, None]), Xm.T @ (yy - mu))
    return b
b = logit_fit(fc[full], y[full]); pr('  logistic recalibration (Noon outcomes, halves out): intercept %+.2f slope %.2f (slope > 1 = forecasts not extreme enough)' % tuple(b))
bs = []
uf = sorted(set(fil))
for _ in range(1000):
    s = np.concatenate([np.where(fil == uf[j])[0] for j in rng.choice(14, 14)]); s = s[full[s]]
    try:
        v = logit_fit(fc[s], y[s])
        if np.all(np.isfinite(v)) and abs(v[1]) < 20: bs.append(v)
    except Exception: pass
bs = np.array(bs); pr('     file-resampled: intercept %.2f to %.2f ; slope %.2f to %.2f' % (*np.percentile(bs[:, 0], [2.5, 97.5]), *np.percentile(bs[:, 1], [2.5, 97.5])))

pr('\n== WHAT IT SAYS ABOUT ME')
pr('  mean forecast of the 26 failed: %.3f ; of the 47 held: %.3f ; of the 5 half: %.3f' % (fc[y == 0].mean(), fc[y == 1].mean(), fc[y == .5].mean()))
for a, b in ((0, .2), (.2, .3), (.3, .4), (.4, .5), (.5, .6), (.6, .7), (.7, .8), (.8, 1.01)):
    mm = (fc >= a - 1e-12) & (fc < b - 1e-12)
    pr('  forecast %.2f-%.2f: n=%2d held %2d failed %2d half %d' % (a, min(b, 1), mm.sum(), (y[mm] == 1).sum(), (y[mm] == 0).sum(), (y[mm] == .5).sum()))
mm = fc < .5
pr('  of the %d with forecast under 0.5: %d failed, %d held, %d half ; in 0.30-0.50: %d failed, %d held, %d half' % (
    mm.sum(), (y[mm] == 0).sum(), (y[mm] == 1).sum(), (y[mm] == .5).sum(),
    (y[(fc >= .3) & mm] == 0).sum(), (y[(fc >= .3) & mm] == 1).sum(), (y[(fc >= .3) & mm] == .5).sum()))
pr('  threshold at the mean outcome instead (forecast < 0.635): failed %d/26, held %d/47 ; at the median forecast (%.2f): failed %d/26 below, held %d/47 below' % (
    ((y == 0) & (fc < .635)).sum(), ((y == 1) & (fc < .635)).sum(), np.median(fc), ((y == 0) & (fc < np.median(fc))).sum(), ((y == 1) & (fc < np.median(fc))).sum()))
pr('  failures with forecast under 0.5, by file: ' + str(Counter(fil[(y == 0) & (fc < .5)].tolist())))
pr('  failures with forecast under 0.5 that are E / L majority: %s' % Counter(maj[(y == 0) & (fc < .5)].tolist()))
pr('  failed ids under 0.5: ' + ' '.join('%s(%.2f)' % (ids[j], fc[j]) for j in np.argsort(fc) if y[j] == 0 and fc[j] < .5))
pr('  failed ids at 0.5+ : ' + ' '.join('%s(%.2f)' % (ids[j], fc[j]) for j in np.argsort(fc) if y[j] == 0 and fc[j] >= .5))
pr('  held ids under 0.5 : ' + ' '.join('%s(%.2f)' % (ids[j], fc[j]) for j in np.argsort(fc) if y[j] == 1 and fc[j] < .5))

pr('\n== P1-P8 by the letter')
pr('  P3 forecasts: ' + ' '.join('%s %.3f' % (i, fc[ix[i]]) for i in ['E1', 'F1', 'G1', 'H1']))
tl = np.array([sum(c != 'E' for c in b) >= 3 for b in Bs])
pr('  P5: T/L n=%d held %.3f ; E n=%d held %.3f ; diff %+.3f ; with "held" = in full (brief rule): %.3f vs %.3f' % (tl.sum(), y[tl].mean(), (~tl).sum(), y[~tl].mean(), y[tl].mean() - y[~tl].mean(), yb[tl].mean(), yb[~tl].mean()))
bt = np.array([bool(re.search(r'\bbetween\b', t, re.I)) for t in text])
pr('  P6: between n=%d held %.3f ; rest %.3f ; in full: %.3f vs %.3f' % (bt.sum(), y[bt].mean(), y[~bt].mean(), yb[bt].mean(), yb[~bt].mean()))
tr = np.array([bool(re.search(r'\bbetween\b[^.;]*?\d[^.;]*?\band\b[^.;]*?\d', t, re.I)) for t in text])
pr('     true two-sided numeric ranges ("between <number> and <number>"): n=%d held %.3f ; rest %.3f' % (tr.sum(), y[tr].mean(), y[~tr].mean()))
for name, yy in (('Noon', y), ('in full', yb)):
    g = sorted((fc[fil == f].mean() - yy[fil == f].mean(), f) for f in set(fil))
    pr('  P7 (%s): most too low: %s %+.3f, then %s %+.3f ; most too high: %s %+.3f, then %s %+.3f' % (name, g[0][1], g[0][0], g[1][1], g[1][0], g[-1][1], g[-1][0], g[-2][1], g[-2][0]))
pr('  P8: %.4f vs %.4f' % (brier(fc, y), brier(np.full(78, y.mean()), y)))
open(R + 'referee/controls.out', 'w').write('\n'.join(L) + '\n')
