"""Score the five forecasters against the published outcomes.   usage: python -I score.py CALIBDIR
Reads items.json, outcomes.json and f1..f5/{A,B}.json; writes scored.json and prints the registered quantities P1-P8."""
import sys, json, itertools
import numpy as np
from scipy.stats import spearmanr
D = sys.argv[1]
items = json.load(open(f"{D}/items.json"))
outcome = json.load(open(f"{D}/outcomes.json"))
ids = [it['id'] for it in items]
assert sorted(ids) == sorted(outcome), set(ids) ^ set(outcome)
F = []
for k in range(1, 6):
    d = {}
    for part in 'AB':
        d.update(json.load(open(f"{D}/f{k}/{part}.json")))
    assert sorted(d) == sorted(ids), (k, set(d) ^ set(ids))
    assert all(0.0 < float(v['p']) < 1.0 and v['basis'] in 'TLE' for v in d.values()), k
    F.append(d)
P = np.array([[float(f[i]['p']) for i in ids] for f in F])                 # forecaster x expectation
B = np.array([[f[i]['basis'] for i in ids] for f in F])
y = np.array([outcome[i] for i in ids])
fc = np.median(P, axis=0)
rng = np.random.default_rng(0)

def auc(p, y):
    a, b = p[y == 1], p[y == 0]
    return float(((a[:, None] > b[None, :]).sum() + 0.5 * (a[:, None] == b[None, :]).sum()) / (len(a) * len(b)))

def boot(fn, n=4000):
    out = []
    for _ in range(n):
        s = rng.integers(0, len(y), len(y))
        try:
            out.append(fn(s))
        except Exception:
            pass
    return np.percentile(out, [2.5, 97.5])

print(f"{len(ids)} expectations: {int((y == 1).sum())} held, {int((y == 0).sum())} failed, {int((y == 0.5).sum())} half; share held (half = 0.5): {y.mean():.3f}")
lo, hi = boot(lambda s: fc[s].mean() - y[s].mean())
print(f"P1  mean forecast {fc.mean():.3f}; share held {y.mean():.3f}; gap {fc.mean() - y.mean():+.3f}  (resampling expectations: {lo:+.3f} to {hi:+.3f})")
full = y != 0.5
lo, hi = boot(lambda s: auc(fc[s][y[s] != 0.5], y[s][y[s] != 0.5]))
print(f"P2  AUC of the forecast, held against failed: {auc(fc[full], y[full]):.3f}  ({lo:.2f} to {hi:.2f})")
print("P3  forecasts for the four theorem expectations: " + ", ".join(f"{i} {fc[ids.index(i)]:.2f}" for i in ('E1', 'F1', 'G1', 'H1')))
rs = [spearmanr(P[a], P[b])[0] for a, b in itertools.combinations(range(5), 2)]
print(f"P4  agreement between two forecasters (Spearman): mean {np.mean(rs):.2f}, from {min(rs):.2f} to {max(rs):.2f}")
tl = (B != 'E').sum(axis=0) >= 3
print(f"P5  marked T or L by three or more: {int(tl.sum())} expectations, held {y[tl].mean():.3f}; the other {int((~tl).sum())}: {y[~tl].mean():.3f}; difference {y[tl].mean() - y[~tl].mean():+.3f}")
for lab in 'TLE':
    m = (B == lab).sum(axis=0) >= 3
    if m.sum():
        print(f"       majority {lab}: {int(m.sum())} expectations, held {y[m].mean():.2f}, mean forecast {fc[m].mean():.2f}")
bt = np.array([it['between'] for it in items])
print(f"P6  with the word 'between': {int(bt.sum())} expectations, held {y[bt].mean():.3f}; the rest {int((~bt).sum())}: {y[~bt].mean():.3f}; difference {y[bt].mean() - y[~bt].mean():+.3f}")
files = sorted(set(it['file'] for it in items), key=lambda f: [it['file'] for it in items].index(f))
gaps = []
print("P7  file by file: forecast, share held, gap")
for f in files:
    m = np.array([it['file'] == f for it in items])
    gaps.append((fc[m].mean() - y[m].mean(), f))
    print(f"       {f:28s} n={int(m.sum()):2d}  forecast {fc[m].mean():.2f}  held {y[m].mean():.2f}  gap {fc[m].mean() - y[m].mean():+.2f}")
print(f"     most too high: {max(gaps)[1]}; most too low: {min(gaps)[1]}")
brier = float(((fc - y) ** 2).mean()); base = float(((y.mean() - y) ** 2).mean())
lo, hi = boot(lambda s: ((y[s].mean() - y[s]) ** 2).mean() - ((fc[s] - y[s]) ** 2).mean())
print(f"P8  Brier score: forecast {brier:.4f}; saying {y.mean():.2f} every time {base:.4f}; improvement {base - brier:+.4f}  ({lo:+.3f} to {hi:+.3f})")
print("afterwards, not registered:")
for k in range(5):
    print(f"   forecaster {k + 1}: mean {P[k].mean():.2f}, AUC {auc(P[k][full], y[full]):.2f}, Brier {((P[k] - y) ** 2).mean():.3f}; letters T {int((B[k] == 'T').sum())}, L {int((B[k] == 'L').sum())}, E {int((B[k] == 'E').sum())}")
print(f"   mean of five in place of the median: mean {P.mean(0).mean():.3f}, AUC {auc(P.mean(0)[full], y[full]):.3f}, Brier {((P.mean(0) - y) ** 2).mean():.4f}")
print("   forecast in bands: " + "; ".join(f"{a:.2f}-{min(b, 1):.2f}: n={int(((fc >= a) & (fc < b)).sum())}, held {y[(fc >= a) & (fc < b)].mean():.2f}" for a, b in ((0, .3), (.3, .5), (.5, .65), (.65, .8), (.8, 1.01)) if ((fc >= a) & (fc < b)).sum()))
for rnd in 'AB':
    m = np.array([it['round'] == rnd for it in items])
    print(f"   round {rnd}: n={int(m.sum())}, forecast {fc[m].mean():.2f}, held {y[m].mean():.2f}, AUC {auc(fc[m & full], y[m & full]):.2f}")
order = np.argsort(-(fc - y))
print("   surest and wrong: " + "; ".join(f"{ids[i]} ({fc[i]:.2f}, {'failed' if y[i] == 0 else 'half'})" for i in order[:6]))
print("   least sure and right: " + "; ".join(f"{ids[i]} ({fc[i]:.2f})" for i in order[::-1][:6] if y[i] == 1))
print(f"   spread between forecasters (standard deviation of the five probabilities, mean over expectations): {P.std(axis=0).mean():.3f}")
json.dump([dict(it, outcome=float(y[j]), forecast=float(fc[j]), probs=[float(x) for x in P[:, j]], basis=''.join(B[:, j])) for j, it in enumerate(items)], open(f"{D}/scored.json", 'w'), indent=1)

# ---- controls on the headline (not registered)
fileof = np.array([it['file'] for it in items]); rnd = np.array([it['round'] for it in items])
ufiles = sorted(set(fileof))
def cluster_boot(fn, n=4000):
    out = []
    for _ in range(n):
        pick = rng.choice(len(ufiles), len(ufiles))
        s = np.concatenate([np.where(fileof == ufiles[j])[0] for j in pick])
        try:
            v = fn(s)
            if np.isfinite(v):
                out.append(v)
        except Exception:
            pass
    return np.percentile(out, [2.5, 97.5])
lo, hi = cluster_boot(lambda s: auc(fc[s][y[s] != 0.5], y[s][y[s] != 0.5]))
print(f"   AUC, resampling whole files (14) in place of single expectations: {lo:.2f} to {hi:.2f}")
lo, hi = cluster_boot(lambda s: fc[s].mean() - y[s].mean())
print(f"   gap between mean forecast and share held, resampling whole files: {lo:+.3f} to {hi:+.3f}")
A = rnd == 'A'
lo, hi = boot(lambda s: auc(fc[s][A[s] & (y[s] != 0.5)], y[s][A[s] & (y[s] != 0.5)]))
print(f"   first round only (no file there quotes another's results): n={int(A.sum())}, AUC {auc(fc[A & full], y[A & full]):.3f} ({lo:.2f} to {hi:.2f}), mean forecast {fc[A].mean():.3f}, held {y[A].mean():.3f}, "
      f"Brier {((fc[A] - y[A]) ** 2).mean():.4f} against {((y[A].mean() - y[A]) ** 2).mean():.4f}")
noleak = np.array([i not in ('G3', 'G4') for i in ids])
print(f"   without G3 and G4 (a later file in the same round says they failed): AUC {auc(fc[noleak & full], y[noleak & full]):.3f}; second round without them: {auc(fc[~A & noleak & full], y[~A & noleak & full]):.3f}")
maj = np.array(['T' if (B[:, j] == 'T').sum() >= 3 else 'L' if (B[:, j] == 'L').sum() >= 3 else 'E' if (B[:, j] == 'E').sum() >= 3 else 'E' for j in range(len(ids))])
score_letter = np.array([{'T': 2, 'L': 1, 'E': 0}[m] for m in maj], float)
print(f"   the letter alone (T above L above E) as a forecast: AUC {auc(score_letter[full], y[full]):.3f}")
for lab in 'LE':
    m = (maj == lab) & full
    print(f"   among the {int((maj == lab).sum())} expectations marked {lab}: AUC of the forecast {auc(fc[m], y[m]):.3f}  ({int((y[m] == 1).sum())} held, {int((y[m] == 0).sum())} failed)")
yl = np.array([json.load(open(f"{D}/outcomes-letter.json"))[i] for i in ids])
fl = yl != 0.5
print(f"   with O2 and O10 scored by the letter (failed): share held {yl.mean():.3f}, gap {fc.mean() - yl.mean():+.3f}, AUC {auc(fc[fl], yl[fl]):.3f}, Brier {((fc - yl) ** 2).mean():.4f} against {((yl.mean() - yl) ** 2).mean():.4f}")
low = fc < 0.3
print(f"   forecasts under 0.30: {int(low.sum())} expectations: {int((y[low] == 1).sum())} held, {int((y[low] == 0.5).sum())} half, {int((y[low] == 0).sum())} failed; forecasts of 0.80 or more: {int((fc >= 0.8).sum())}: "
      f"{int((y[fc >= 0.8] == 1).sum())} held, {int((y[fc >= 0.8] == 0.5).sum())} half, {int((y[fc >= 0.8] == 0).sum())} failed")
print(f"   failed expectations with a forecast under 0.5: {int(((y == 0) & (fc < 0.5)).sum())} of {int((y == 0).sum())}; held with a forecast of 0.5 or more: {int(((y == 1) & (fc >= 0.5)).sum())} of {int((y == 1).sum())}")
half = y == 0.5
print("   the five halves: " + "; ".join(f"{ids[j]} {fc[j]:.2f}" for j in np.where(half)[0]))
ident = np.mean([(np.abs(P[a] - P[b]) <= 0.05 + 1e-9).mean() for a, b in itertools.combinations(range(5), 2)])      # the referee: a bare <= on floats undercounted
print(f"   two forecasters within 0.05 of each other on {100 * ident:.0f}% of expectations; largest disagreement: " + "; ".join(f"{ids[j]} ({P[:, j].min():.2f} to {P[:, j].max():.2f})" for j in np.argsort(-(P.max(0) - P.min(0)))[:4]))
ind = [((P[k] - y) ** 2).mean() for k in range(5)]
print(f"   Brier: each forecaster {min(ind):.3f} to {max(ind):.3f}; the median of five {brier:.3f}")

# ---- after the referee: its main controls, recomputed here
print("after the referee:")
def pair_auc(p, y, same):
    """AUC over pairs (held, failed) from the same file (same=True) or from different files"""
    hit = n = 0
    for a in np.where(y == 1)[0]:
        for b in np.where(y == 0)[0]:
            if (fileof[a] == fileof[b]) == same:
                n += 1; hit += 1.0 if p[a] > p[b] else 0.5 if p[a] == p[b] else 0.0
    return hit / n, n
w, nw = pair_auc(fc, y, True); bt_, nb = pair_auc(fc, y, False)
print(f"   a held and a failed expectation of the SAME file: the forecast ranks them right {w:.3f} of the time ({nw} pairs); of different files {bt_:.3f} ({nb} pairs)")
yy = y.copy(); yy[~noleak] = 0.5                                        # drop G3, G4 from the pairs
w2, nw2 = pair_auc(fc, yy, True)
def within_idx(s):
    f2, y2, fl2 = fc[s], yy[s], fileof[s]
    hit = n = 0
    for a in np.where(y2 == 1)[0]:
        for b in np.where(y2 == 0)[0]:
            if fl2[a] == fl2[b]:
                n += 1; hit += 1.0 if f2[a] > f2[b] else 0.5 if f2[a] == f2[b] else 0.0
    return hit / n
lo, hi = cluster_boot(within_idx, 2000)
print(f"   same file, without G3 and G4: {w2:.3f} ({nw2} pairs); resampling whole files {lo:.2f} to {hi:.2f}")
filemean = np.array([fc[fileof == f].mean() for f in fileof])
print(f"   giving every expectation its file's mean forecast: AUC {auc(filemean[full], y[full]):.3f}")
mE = (maj == 'E') & full & noleak
lo, hi = cluster_boot(lambda s: auc(fc[s][(maj[s] == 'E') & (y[s] != 0.5) & noleak[s]], y[s][(maj[s] == 'E') & (y[s] != 0.5) & noleak[s]]))
print(f"   among the own estimates not given away ({int(((maj == 'E') & noleak).sum())}): AUC {auc(fc[mE], y[mE]):.3f}; resampling whole files {lo:.2f} to {hi:.2f}")
infull = y.copy()
for lab_, v in (('E4', 0), ('F4', 0), ('K5', 0), ('K6', 0), ('Q4', 1)):
    infull[ids.index(lab_)] = v
print(f"   'in full' as the brief put it (E4, F4, K5, K6 failed; Q4 held): {int(infull.sum())} of {len(infull)} held = {infull.mean():.3f}; gap {fc.mean() - infull.mean():+.3f}; AUC {auc(fc, infull):.3f}")
il = infull.copy(); il[ids.index('O2')] = 0; il[ids.index('O10')] = 0
print(f"   and the smell study by the letter as well: {il.mean():.3f} held; gap {fc.mean() - il.mean():+.3f}; AUC {auc(fc, il):.3f}; without G3 and G4 {auc(fc[noleak], il[noleak]):.3f}")
harsh = np.where(y == 0.5, 0, y); harsh[ids.index('O2')] = 0; harsh[ids.index('O10')] = 0
print(f"   harshest: every half failed, O2 and O10 failed: AUC {auc(fc, harsh):.3f}; without G3 and G4 {auc(fc[noleak], harsh[noleak]):.3f}")
print(f"   held outright: {int((y == 1).sum())} of {len(y)} = {(y == 1).mean():.3f}")
for cut in (0.30, 0.35):
    m = fc <= cut + 1e-9
    print(f"   forecast of {cut:.2f} or less: {int(m.sum())} expectations: {int((y[m] == 1).sum())} held, {int((y[m] == 0.5).sum())} half, {int((y[m] == 0).sum())} failed")
m = (fc < 0.3) & noleak
print(f"   under 0.30 without G3 and G4: {int(m.sum())}: {int((y[m] == 1).sum())} held, {int((y[m] == 0.5).sum())} half, {int((y[m] == 0).sum())} failed")
fa = y == 0
print(f"   the {int(fa.sum())} failures: forecast under 0.30: {int((fa & (fc < 0.3)).sum())}; 0.30 to under 0.50: {int((fa & (fc >= 0.3) & (fc < 0.5)).sum())}; 0.50 or more: {int((fa & (fc >= 0.5)).sum())}; mean forecast {fc[fa].mean():.2f}")
mid = (fc >= 0.3) & (fc <= 0.7)
rs_mid = [spearmanr(P[a][mid], P[b][mid])[0] for a, b in itertools.combinations(range(5), 2)]
split = int(((P.min(0) < 0.5) & (P.max(0) > 0.5)).sum())
print(f"   agreement between two forecasters on the {int(mid.sum())} expectations with a forecast from 0.3 to 0.7: {np.mean(rs_mid):.2f}; the five sit on both sides of 0.5 on {split} expectations")
T6 = maj == 'T'
print(f"   the {int(T6.sum())} expectations marked T: all held; forecasts " + ", ".join(f"{ids[j]} {fc[j]:.2f}" for j in np.where(T6)[0]))
