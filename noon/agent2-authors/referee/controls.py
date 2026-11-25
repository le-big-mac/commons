import json, statistics as st, math
import numpy as np
from scipy.stats import spearmanr, binomtest
R = {'1': '/home/agent2/authors', '2': '/home/agent2/authors2'}
ld = lambda p: json.load(open(p))
S = {}
for k, d in R.items():
    v = ld(d + '/results.json')['verdicts']
    keys = list(v)
    y = np.array([1.0 if v[q] else 0.0 for q in keys])
    g = lambda p: np.array([float(ld(p)[q]) for q in keys])
    s = dict(keys=keys, y=y, aq=g(d + '/author/odds-quick.json'), noon=g(d + '/mine.json'),
             F=np.array([g(d + '/readers/f%d.json' % i) for i in (1, 2, 3)]),
             Q=np.array([g(d + '/quick/f%d.json' % i) for i in (1, 2, 3)]))
    s['cr'] = np.median(s['F'], axis=0)
    s['qr'] = np.median(s['Q'], axis=0)
    s['ac'] = g(d + '/author/odds-careful.json') if k == '1' else None
    S[k] = s
B = lambda p, y: float(((p - y) ** 2).mean())
cat = lambda name: np.concatenate([S['1'][name], S['2'][name]])
Y = cat('y')
P = {'quick readers': cat('qr'), 'authors quick': cat('aq'), 'Noon': cat('noon'), 'careful readers': cat('cr')}
print('== A. Brier on the 21 held and the 3 failed separately (pooled); mean odds on held / failed')
for n, p in P.items():
    print(f'  {n:16s} all {B(p, Y):.4f}  held(21) {B(p[Y == 1], 1):.4f}  failed(3) {B(p[Y == 0], 0):.4f}   mean odds on held {p[Y == 1].mean():.3f}  on failed {p[Y == 0].mean():.3f}')
ac = S['1']['ac']
print(f'  author careful (sheet 1 only, 12 held) {B(ac, 1):.4f} mean odds {ac.mean():.3f}')
print('  sheet 1 only (all held): mean odds and Brier')
for n, key in (('quick readers', 'qr'), ('author quick', 'aq'), ('Noon', 'noon'), ('careful readers', 'cr'), ('author careful', 'ac')):
    p = S['1'][key]
    print(f'    {n:16s} mean odds {p.mean():.3f}  Brier {B(p, 1):.4f}   Brier of saying its own mean every time {(1 - p.mean()) ** 2:.4f}')
for c in (0.8, 0.85, 0.9, 0.95):
    print(f'    constant {c}: sheet 1 Brier {(1 - c) ** 2:.4f};  pooled 24: {B(np.full(24, c), Y):.4f}')
print('  sheet 2 only: held(9) / failed(3)')
for n, key in (('quick readers', 'qr'), ('author quick', 'aq'), ('Noon', 'noon'), ('careful readers', 'cr')):
    p = S['2'][key]; y = S['2']['y']
    print(f'    {n:16s} all {B(p, y):.4f} held {B(p[y == 1], 1):.4f} failed {B(p[y == 0], 0):.4f}')

print('== B. Common-rule controls (no use of outcomes)')
lg = lambda p: np.log(p / (1 - p))
ex = lambda p, k: 1 / (1 + np.exp(-k * lg(p)))
print('  B1. every number at/above .5 -> .9, below -> .1 (exact .5 stays .5): Brier and number on the right side')
for n, p in P.items():
    q = np.where(p > 0.5, 0.9, np.where(p < 0.5, 0.1, 0.5))
    right = int(((p > .5) & (Y == 1)).sum() + ((p < .5) & (Y == 0)).sum())
    print(f'    {n:16s} {B(q, Y):.4f}   right side {right}/24, at exactly .5: {int((p == .5).sum())}')
print('  B2. log-odds of each party stretched by its own k so that mean |log-odds| equals the careful readers (per sheet)')
for sh in ('1', '2'):
    tgt = np.abs(lg(S[sh]['cr'])).mean()
    row = []
    for n, key in (('quick readers', 'qr'), ('author quick', 'aq'), ('Noon', 'noon'), ('careful readers', 'cr'), ('author careful', 'ac')):
        p = S[sh][key]
        if p is None:
            continue
        k = tgt / np.abs(lg(p)).mean()
        row.append((n, k, B(ex(p, k), S[sh]['y'])))
        S[sh][key + '_eq'] = ex(p, k)
    print(f'    sheet {sh}: ' + '; '.join(f'{n} k={k:.2f} Brier {b:.4f}' for n, k, b in row))
print('    pooled: ' + '; '.join(f"{n} {B(np.concatenate([S['1'][key + '_eq'], S['2'][key + '_eq']]), Y):.4f}" for n, key in (('quick readers', 'qr'), ('author quick', 'aq'), ('Noon', 'noon'), ('careful readers', 'cr'))))
print('  B3. each party keeps its own order within a sheet but is given the careful readers sorted numbers (rank-matching)')
for sh in ('1', '2'):
    tgt = np.sort(S[sh]['cr'])
    row = []
    for n, key in (('quick readers', 'qr'), ('author quick', 'aq'), ('Noon', 'noon'), ('careful readers', 'cr'), ('author careful', 'ac')):
        p = S[sh][key]
        if p is None:
            continue
        # average over tie-breaks by tiny jitter
        vals = []
        rng = np.random.default_rng(1)
        for _ in range(400):
            o = np.argsort(np.argsort(p + rng.uniform(-1e-6, 1e-6, len(p))))
            vals.append(B(tgt[o], S[sh]['y']))
        row.append((n, np.mean(vals)))
        S[sh][key + '_rm'] = np.mean(vals)
    print(f'    sheet {sh}: ' + '; '.join(f'{n} {b:.4f}' for n, b in row))
print('    pooled: ' + '; '.join(f"{n} {(S['1'][key + '_rm'] + S['2'][key + '_rm']) / 2:.4f}" for n, key in (('quick readers', 'qr'), ('author quick', 'aq'), ('Noon', 'noon'), ('careful readers', 'cr'))))
print('  B4. same stretch k applied to every party (pooled Brier)')
for k in (0.5, 1, 1.5, 2, 3):
    print(f'    k={k}: ' + '; '.join(f'{n} {B(ex(p, k), Y):.4f}' for n, p in P.items()))
print('  B5. best k in hindsight for each party (pooled) -- uses outcomes, shown only as a ceiling')
for n, p in P.items():
    ks = np.linspace(0.2, 6, 300); bs = [B(ex(p, k), Y) for k in ks]
    print(f'    {n:16s} best k {ks[int(np.argmin(bs))]:.2f} Brier {min(bs):.4f}')

print('== C. The author careful pass against dumb shifts of its own quick odds (sheet 1)')
aq = S['1']['aq']; cr = S['1']['cr']
d = (ac - aq)
print(f'  careful {B(ac, 1):.4f}; quick {B(aq, 1):.4f}; readers {B(cr, 1):.4f}; mean change {d.mean():+.4f}; raised on {int((d > 0).sum())}, lowered on {int((d < 0).sum())}')
sh = np.clip(aq + d.mean(), 0.01, 0.99)
print(f'  quick odds + the mean change on every statement: {B(sh, 1):.4f}')
k = np.abs(lg(ac)).mean() / np.abs(lg(aq)).mean()
print(f'  quick odds stretched to the careful pass mean |log-odds| (k={k:.2f}): {B(ex(aq, k), 1):.4f}')
print(f'  correlation careful vs quick {np.corrcoef(ac, aq)[0, 1]:.2f}; careful vs readers {np.corrcoef(ac, cr)[0, 1]:.2f}; quick vs readers {np.corrcoef(aq, cr)[0, 1]:.2f}')
print(f'  careful vs each reader: {[round(B(S["1"]["F"][i], 1), 4) for i in range(3)]}; better than {sum(B(ac, 1) < B(S["1"]["F"][i], 1) for i in range(3))} of 3')

print('== D. Noon worst statement')
nn = S['1']['noon']
i = S['1']['keys'].index('A11')
m = np.ones(12, bool); m[i] = False
print(f'  without A11: Noon {B(nn[m], 1):.4f}, readers {B(cr[m], 1):.4f}, author quick {B(aq[m], 1):.4f}, author careful {B(ac[m], 1):.4f}')
drop = lambda p: (np.sort((p - 1) ** 2)[:-1]).mean()
print(f'  each party without ITS OWN worst statement: Noon {drop(nn):.4f}, readers {drop(cr):.4f}, author quick {drop(aq):.4f}, author careful {drop(ac):.4f}, quick readers {drop(S["1"]["qr"]):.4f}')
print(f'  Noon closer than readers on sheet 1 without A11: {int((np.abs(nn[m]-1) < np.abs(cr[m]-1)).sum())} of 11')

print('== E. Quick readers against authors quick odds')
qr, a = P['quick readers'], P['authors quick']
dd = (qr - Y) ** 2 - (a - Y) ** 2
rng = np.random.default_rng(7)
bs = [dd[rng.integers(0, 24, 24)].mean() for _ in range(20000)]
print(f'  pooled diff {dd.mean():+.4f} bootstrap 95% ({np.percentile(bs, 2.5):+.4f} to {np.percentile(bs, 97.5):+.4f}); share of resamples <= 0: {np.mean(np.array(bs) <= 0):.4f}')
print(f'  sheet 1 diff {dd[:12].mean():+.4f}; sheet 2 diff {dd[12:].mean():+.4f}')
names = S['1']['keys'] + S['2']['keys']
o = np.argsort(dd)
print('  per-statement contributions (quick readers sq.err minus author sq.err), extremes:', [(names[j], round(float(dd[j]), 3)) for j in list(o[:3]) + list(o[-3:])])
print(f'  without B6: diff {np.delete(dd, names.index("B6")).mean():+.4f}')
for i in range(3):
    q1, q2 = S['1']['Q'][i], S['2']['Q'][i]
    print(f'  quick reader {i+1}: sheet 1 {B(q1, 1):.4f} vs author {B(S["1"]["aq"], 1):.4f}; sheet 2 {B(q2, S["2"]["y"]):.4f} vs author {B(S["2"]["aq"], S["2"]["y"]):.4f}; closer than author on {int((np.abs(q1-1) < np.abs(S["1"]["aq"]-1)).sum())}/12 and {int((np.abs(q2-S["2"]["y"]) < np.abs(S["2"]["aq"]-S["2"]["y"])).sum())}/12')
print(f'  sign test 21 of 24: p = {binomtest(21, 24).pvalue:.5f} (treats 24 statements as independent)')
print('  bootstrap for the other headline gaps (my seed):')
for n1, n2 in (('quick readers', 'careful readers'), ('authors quick', 'careful readers'), ('Noon', 'careful readers'), ('Noon', 'authors quick')):
    d2 = (P[n1] - Y) ** 2 - (P[n2] - Y) ** 2
    b2 = [d2[rng.integers(0, 24, 24)].mean() for _ in range(20000)]
    print(f'    {n1} minus {n2}: {d2.mean():+.4f} ({np.percentile(b2, 2.5):+.4f} to {np.percentile(b2, 97.5):+.4f})')

print('== F. Ranking (AUC) within sheet 2')
def auc(p, y):
    h, f = p[y == 1], p[y == 0]
    return ((h[:, None] > f[None, :]).sum() + 0.5 * (h[:, None] == f[None, :]).sum()) / (len(h) * len(f))
y2 = S['2']['y']
print('  ' + '; '.join(f'{n} {auc(S["2"][k], y2):.3f}' for n, k in (('quick median', 'qr'), ('author quick', 'aq'), ('Noon', 'noon'), ('careful median', 'cr'))))
print('  quick readers each: ' + ', '.join(f'{auc(S["2"]["Q"][i], y2):.3f}' for i in range(3)) + '; careful each: ' + ', '.join(f'{auc(S["2"]["F"][i], y2):.3f}' for i in range(3)))
print('  pooled 24 (mixes sheets): ' + '; '.join(f'{n} {auc(p, Y):.3f}' for n, p in P.items()))

print('== G. Agreement among careful readers')
for sh in ('1', '2'):
    F = S[sh]['F']; y = S[sh]['y']
    c = np.mean([np.corrcoef(F[a], F[b])[0, 1] for a, b in ((0, 1), (0, 2), (1, 2))])
    ch = np.mean([np.corrcoef(F[a][y == 1], F[b][y == 1])[0, 1] for a, b in ((0, 1), (0, 2), (1, 2))])
    Qm = S[sh]['Q']
    cq = np.mean([np.corrcoef(Qm[a], Qm[b])[0, 1] for a, b in ((0, 1), (0, 2), (1, 2))])
    print(f'  sheet {sh}: careful readers mean pairwise r {c:.3f}; among held only {ch:.3f}; mean |difference| {np.mean([np.abs(F[a]-F[b]).mean() for a, b in ((0, 1), (0, 2), (1, 2))]):.3f}; quick readers r {cq:.3f}, mean |difference| {np.mean([np.abs(Qm[a]-Qm[b]).mean() for a, b in ((0, 1), (0, 2), (1, 2))]):.3f}')

print('== H. Time against score (minutes as typed in figure.py)')
MIN = {'quick': ([29.4 / 60, 36.1 / 60, 22.1 / 60], [41.2 / 60, 34.7 / 60, 47.9 / 60]),
       'careful': ([389.1 / 60, 640.6 / 60, 617.8 / 60], [714.1 / 60, 656.7 / 60, 653.9 / 60]),
       'aq': (8.77, 6.95), 'ac': (16.92, None), 'noon': (2.70, 2.68)}
pts = []
for si, sh in enumerate(('1', '2')):
    y = S[sh]['y']
    for i in range(3):
        pts.append(('quick reader', sh, MIN['quick'][si][i], B(S[sh]['Q'][i], y)))
        pts.append(('careful reader', sh, MIN['careful'][si][i], B(S[sh]['F'][i], y)))
    pts.append(('author quick', sh, MIN['aq'][si], B(S[sh]['aq'], y)))
    pts.append(('Noon', sh, MIN['noon'][si], B(S[sh]['noon'], y)))
pts.append(('author careful', '1', 16.92, B(ac, 1)))
def sp(sel, label):
    t = [p[2] for p in pts if sel(p)]; b = [p[3] for p in pts if sel(p)]
    r = spearmanr(t, b)
    print(f'  {label}: n={len(t)} Spearman rho {r.statistic:+.2f} (p {r.pvalue:.3f})')
sp(lambda p: True, 'all 17 points')
sp(lambda p: p[0] != 'quick reader', 'without the quick readers (11 points)')
sp(lambda p: p[0] != 'quick reader' and p[1] == '1', 'without quick readers, sheet 1 (6 points)')
sp(lambda p: p[0] != 'quick reader' and p[1] == '2', 'without quick readers, sheet 2 (5 points)')
sp(lambda p: p[0] in ('quick reader', 'careful reader'), 'readers only (12 points; two clusters)')
sp(lambda p: p[0] == 'careful reader', 'careful readers only (6)')
sp(lambda p: p[0] == 'quick reader', 'quick readers only (6)')
print('  party means in time order: ')
for n in ('quick reader', 'Noon', 'author quick', 'careful reader', 'author careful'):
    t = [p[2] for p in pts if p[0] == n]; b = [p[3] for p in pts if p[0] == n]
    print(f'    {n:15s} minutes {np.mean(t):5.2f} ({min(t):.2f}-{max(t):.2f})  mean per-sheet Brier {np.mean(b):.4f}')

print('== I. Other definitions of "the readers"')
for sh in ('1', '2'):
    F = S[sh]['F']; y = S[sh]['y']; Q = S[sh]['Q']
    print(f'  sheet {sh}: careful: median-odds {B(np.median(F, 0), y):.4f}, mean-odds {B(F.mean(0), y):.4f}, median of the three scores {np.median([B(F[i], y) for i in range(3)]):.4f}, mean of scores {np.mean([B(F[i], y) for i in range(3)]):.4f} | quick: median-odds {B(np.median(Q, 0), y):.4f}, mean-odds {B(Q.mean(0), y):.4f}, median score {np.median([B(Q[i], y) for i in range(3)]):.4f}')
print(f'  R4 margin: Noon {B(nn, 1):.6f} - readers median {B(cr, 1):.6f} = {B(nn, 1) - B(cr, 1):.6f}; against mean-odds {B(nn, 1) - B(S["1"]["F"].mean(0), 1):.6f}; against median score {B(nn, 1) - np.median([B(S["1"]["F"][i], 1) for i in range(3)]):.6f}')

print('== J. Noon own fourteen sealed expectations as a forecaster')
own = [(.65, 1), (.60, 1), (.55, 0), (.50, 1), (.60, 1), (.65, 1), (.45, 0), (.55, 1), (.55, 0), (.80, 1), (.55, 0), (.50, 0)]
pp = np.array([a for a, _ in own]); yy = np.array([b for _, b in own], float)
print(f'  12 resolved: held {int(yy.sum())}; Brier {B(pp, yy):.4f}; saying 0.5 every time 0.2500; saying the hold rate {B(np.full(12, yy.mean()), yy):.4f}')
print(f'  if these odds were stretched to the careful readers boldness (k=3): {B(ex(pp, 3), yy):.4f}')

print('== K. Quick readers numbers: how round, how hedged')
for n, arr in (('quick readers (72 numbers)', np.concatenate([S['1']['Q'].ravel(), S['2']['Q'].ravel()])), ('careful readers (72)', np.concatenate([S['1']['F'].ravel(), S['2']['F'].ravel()])), ('authors quick (24)', P['authors quick']), ('Noon (24)', P['Noon'])):
    print(f'  {n:28s} multiples of 0.05: {np.mean(np.isclose((arr * 100) % 5, 0) | np.isclose((arr * 100) % 5, 5)):.2f}; mean |p-0.5| {np.abs(arr - .5).mean():.3f}; within .5-.8: {np.mean((arr >= .5) & (arr <= .8)):.2f}')
print('  sheet 1 mean odds: quick readers each', [round(float(S['1']['Q'][i].mean()), 3) for i in range(3)], ' careful each', [round(float(S['1']['F'][i].mean()), 3) for i in range(3)])
