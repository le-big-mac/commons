"""Checks made after the referee's report, most of them the referee's own, redone here from lines.csv.   usage: python after.py lines.csv"""
import sys, csv
import numpy as np
from scipy.optimize import minimize
R = [r for r in csv.DictReader(open(sys.argv[1])) if r['outcome'] != '']
fo = lambda r: r['forecasters'] or r['forecasters_late']
M = [r for r in R if r['kind'] == 'sheet']
B = lambda p, y: float(np.mean((np.asarray(p, float) - np.asarray(y, float)) ** 2))
od = lambda rows: np.array([float(r['odds']) for r in rows]); yy = lambda rows: np.array([float(r['outcome']) for r in rows]); ff = lambda rows: np.array([float(fo(r)) for r in rows])
early = [r for r in M if r['forecasters']]; late = [r for r in M if not r['forecasters']]
def rank(rows, key, within):
    w = n = 0.0
    for a in rows:
        for b in rows:
            if a['outcome'] == '1' and b['outcome'] == '0' and (not within or a['file'] == b['file']):
                pa, pb = float(key(a)), float(key(b)); w += (pa > pb) + 0.5 * (pa == pb); n += 1
    return w / n, int(n)
print("A. Held above failed: pairs on the same sealed file only, and pairs pooled across files")
for name, rows in (("six priced at the time", early), ("four priced late", late), ("all ten", M), ("all ten less the arctic circle", [r for r in M if r['study'] != 'arctic circle'])):
    a, n = rank(rows, lambda r: r['odds'], True); b, _ = rank(rows, fo, True); c, m = rank(rows, lambda r: r['odds'], False); d, _ = rank(rows, fo, False)
    print(f"   {name:30s} same file ({n:3d} pairs): mine {a:.3f}, theirs {b:.3f};   pooled ({m:4d} pairs): mine {c:.3f}, theirs {d:.3f}")
print("B. How much of the gap is level? My odds moved by a constant (kept within 0.01 and 0.99) to the forecasters' mean")
for name, rows in (("six priced at the time", early), ("four priced late", late), ("all ten", M)):
    m, f, y = od(rows), ff(rows), yy(rows); one = np.clip(m + f.mean() - m.mean(), 0.01, 0.99); per = m.copy()
    for st in {r['study'] for r in rows}:
        k = np.array([r['study'] == st for r in rows]); per[k] = np.clip(m[k] + f[k].mean() - m[k].mean(), 0.01, 0.99)
    gap = B(m, y) - B(f, y)
    print(f"   {name:24s} mine {B(m, y):.4f}, theirs {B(f, y):.4f}; one shift for the set {B(one, y):.4f} (closes {100 * (B(m, y) - B(one, y)) / gap:.0f}% of the gap); a shift for each sheet {B(per, y):.4f} (closes {100 * (B(m, y) - B(per, y)) / gap:.0f}%)")
print("   mean odds by sheet, mine and theirs, with the share held:")
for st in dict.fromkeys(r['study'] for r in sorted(M, key=lambda r: int(r['order']))):
    rows = [r for r in M if r['study'] == st]; print(f"      {st:22s} mine {od(rows).mean():.2f}, theirs {ff(rows).mean():.2f}, held {yy(rows).mean():.2f}")
print("C. The share of each gap that is the arctic circle's main sheet (summed squared error)")
for name, rows in (("four priced late", late), ("all ten", M)):
    d = (od(rows) - yy(rows)) ** 2 - (ff(rows) - yy(rows)) ** 2; k = np.array([r['study'] == 'arctic circle' for r in rows]); rest = [r for r in rows if r['study'] != 'arctic circle']
    cm = int((abs(od(rest) - yy(rest)) < abs(ff(rest) - yy(rest)) - 1e-9).sum()); ct = int((abs(ff(rest) - yy(rest)) < abs(od(rest) - yy(rest)) - 1e-9).sum())
    print(f"   {name:18s} difference {d.sum():.3f}, of which the six lines {d[k].sum():.3f} = {100 * d[k].sum() / d.sum():.0f}%; without them: mine {B(od(rest), yy(rest)):.4f}, theirs {B(ff(rest), yy(rest)):.4f}, closer mine {cm}, theirs {ct}")
low = [(r['study'], r['label'], fo(r), 'held' if r['outcome'] == '1' else 'failed') for r in M if float(fo(r)) < 0.3]
print("   their lines below 0.3: " + "; ".join(f"{a} {b} {float(c):.2f} {d}" for a, b, c, d in low))
k5 = [r for r in M if float(fo(r)) < 0.5]; print(f"   their lines below 0.5: {len(k5)}, held {int(yy(k5).sum())}; on sheets priced at the time {sum(1 for r in k5 if r['forecasters'])}, late {sum(1 for r in k5 if not r['forecasters'])}")
print("D. Cannonballs if J6 (which landed on the end of its interval) is counted otherwise")
can = [r for r in M if r['study'] == 'cannonballs']
for name, v in (("held (as scored)", 1.0), ("failed", 0.0), ("not scored", None)):
    rows = [r for r in can if not (v is None and r['label'] == 'J6')]; y = np.array([v if r['label'] == 'J6' else float(r['outcome']) for r in rows])
    allm = [r for r in M if not (v is None and r['label'] == 'J6')]; ya = np.array([v if r['label'] == 'J6' else float(r['outcome']) for r in allm])
    better = sum(B(ff([r for r in allm if r['study'] == st]), ya[[r['study'] == st for r in allm]]) < B(od([r for r in allm if r['study'] == st]), ya[[r['study'] == st for r in allm]]) for st in {r['study'] for r in allm})
    print(f"   J6 {name:17s} cannonballs: mine {B(od(rows), y):.4f}, theirs {B(ff(rows), y):.4f};   all main sheets: mine {B(od(allm), ya):.4f}, theirs {B(ff(allm), ya):.4f}; sheets on which theirs is better: {better} of 10")
print("   hand figures on the cannonballs sheet: lines whose sealed text says 'By hand': counted in doubts-scan style from the sealed file")
print("E. The correction: where the harm sits, and the form that was really available at the time")
st = np.array([r['study'] for r in R]); p = od(R); y = yy(R); x = np.log(p / (1 - p)); order = {r['study']: int(r['order']) for r in R}
def fit(xx, yv, slope=True):
    def nll(t):
        z = t[0] + (t[1] if slope else 1.0) * xx; return np.sum(np.logaddexp(0, z) - yv * z)
    best = min((minimize(nll, s, method='Nelder-Mead', options=dict(xatol=1e-9, fatol=1e-12, maxiter=40000, maxfev=40000)) for s in ([0, 1], [0.5, 1.5], [-0.5, 0.7])), key=lambda r: r.fun); return best.x[0], (best.x[1] if slope else 1.0)
app = lambda a, b, xx: np.clip(1 / (1 + np.exp(-(a + b * xx))), 0.01, 0.99)
studies = sorted(set(st), key=lambda s: order[s]); q = np.empty_like(p)
for s in studies:
    k = st == s; a, b = fit(x[~k], y[~k]); q[k] = app(a, b, x[k])
d = (q - y) ** 2 - (p - y) ** 2; az = np.array([r['study'] == 'arctic circle' and r['kind'] == 'sheet' and r['outcome'] == '0' for r in R]); na = st != 'arctic circle'
print(f"   leaving one study out: all {len(p)} lines {B(p, y):.4f} to {B(q, y):.4f}; change in summed squared error {d.sum():+.3f}: the four failed lines of the arctic circle's main sheet {d[az].sum():+.3f}, the other {int((~az).sum())} lines {d[~az].sum():+.3f} ({d[~az].mean():+.4f} a line)")
print(f"   the same scored without the arctic circle study: {B(p[na], y[na]):.4f} to {B(q[na], y[na]):.4f}")
print("   forward in time: fitted to all earlier studies, applied to the next")
qf = np.full_like(p, np.nan)
for i, s in enumerate(studies):
    if i < 2: continue
    tr = np.isin(st, studies[:i]); k = st == s; a, b = fit(x[tr], y[tr]); qf[k] = app(a, b, x[k])
    print(f"      {s:22s} a = {a:+7.2f}, b = {b:6.2f}; sealed {B(p[k], y[k]):.4f}, corrected {B(qf[k], y[k]):.4f}")
k = ~np.isnan(qf); print(f"      together ({int(k.sum())} lines): sealed {B(p[k], y[k]):.4f}, corrected {B(qf[k], y[k]):.4f}")
print("F. Doubts: the sheets' own words only ('Marked down', 'Same doubt'), against the other lines of the sheets that have such a line")
own = [r for r in R if r['named_doubt'] == 'marked down']; files = {r['file'] for r in own}; oth = [r for r in R if r['file'] in files and r['named_doubt'] != 'marked down']
for name, rows in (("own words", own), ("others, same sheets", oth), ("others, less the hand-picked", [r for r in oth if not r['named_doubt']])):
    print(f"   {name:30s} {len(rows):3d} lines; held {int(yy(rows).sum()):3d} ({yy(rows).mean():.2f}); my mean odds {od(rows).mean():.3f}; Brier {B(od(rows), yy(rows)):.3f}")
from scipy.stats import binom
print(f"   if each of the 13 held with probability 0.60 independently, 11 or more would hold with probability {1 - binom.cdf(10, 13, 0.604):.3f}")
a1, n1, a2, n2 = yy(own).mean(), len(own), yy(oth).mean(), len(oth); se = (a1 * (1 - a1) / n1 + a2 * (1 - a2) / n2) ** 0.5
print(f"   difference in the share held, own words minus others: {a1 - a2:+.3f}; as if independent, 95% {a1 - a2 - 1.96 * se:+.2f} to {a1 - a2 + 1.96 * se:+.2f}; the difference I priced: {od(own).mean() - od(oth).mean():+.2f}")
print("G. The lines I put below 0.6")
lowm = [r for r in R if float(r['odds']) < 0.6]; meta = [r for r in lowm if r['study'] == 'readers and authors' or r['kind'] == 'bet on my odds']; world = [r for r in lowm if r not in meta]
print(f"   {len(lowm)} lines, held {int(yy(lowm).sum())}: about how odds would score (readers-and-authors lines and the three bets) {len(meta)}, held {int(yy(meta).sum())}, my mean odds {od(meta).mean():.3f}; about the world {len(world)}, held {int(yy(world).sum())}, my mean odds {od(world).mean():.3f}")
print("H. Sheets or sets that scored worse than saying one half (0.25), by sealed file")
for f in dict.fromkeys(r['file'] for r in R):
    rows = [r for r in R if r['file'] == f]
    if B(od(rows), yy(rows)) > 0.25: print(f"   {f:34s} {len(rows)} lines, Brier {B(od(rows), yy(rows)):.4f}")
