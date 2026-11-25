"""The three forecasters' odds on the four sheets nobody else had priced, against mine.
usage: python forecast-score.py lines.csv FORECASTDIR [out.csv]     Refuses to read anything until all twelve answer files exist."""
import sys, csv, json, os
import numpy as np
d = sys.argv[2]; files = [f"{d}/f{k}-{s}.json" for k in (1, 2, 3) for s in (1, 2, 3, 4)]
missing = [f for f in files if not os.path.exists(f)]
if missing: sys.exit("not all forecasts are filed; nothing read. missing: " + ", ".join(os.path.basename(f) for f in missing))
F = [{} for _ in range(3)]
for k in range(3):
    for s in (1, 2, 3, 4):
        part = json.load(open(f"{d}/f{k + 1}-{s}.json")); assert not set(part) & set(F[k]); F[k].update({a: float(b) for a, b in part.items()})
R = [r for r in csv.DictReader(open(sys.argv[1])) if r['kind'] == 'sheet' and r['study'] in ('readers and authors', 'floating cube', 'cannonballs', 'arctic circle')]
assert all(set(F[k]) == {r['label'] for r in R} for k in range(3)), [sorted(set(F[k]) ^ {r['label'] for r in R}) for k in range(3)]
B = lambda p, y: float(np.mean((np.asarray(p) - np.asarray(y)) ** 2))
print("       outcome   mine   forecasters (three)      their median")
rows = []
for r in R:
    f = [F[k][r['label']] for k in range(3)]; med = float(np.median(f)); rows.append((r, f, med))
    print(f"{r['label']:4s}   {'held  ' if r['outcome'] == '1' else 'failed' if r['outcome'] == '0' else 'void  '}    {float(r['odds']):.2f}   {f[0]:.2f}  {f[1]:.2f}  {f[2]:.2f}        {med:.2f}")
S = [(r, f, m) for r, f, m in rows if r['outcome'] != '']
def block(name, sel):
    y = [float(r['outcome']) for r, f, m in sel]; me = [float(r['odds']) for r, f, m in sel]; md = [m for r, f, m in sel]
    each = ", ".join(f"{B([f[k] for r, f, m in sel], y):.4f}" for k in range(3))
    cm = sum(abs(a - t) < abs(b - t) - 1e-9 for a, b, t in zip(me, md, y)); ct = sum(abs(b - t) < abs(a - t) - 1e-9 for a, b, t in zip(me, md, y))
    print(f"{name:22s} {len(sel):3d} lines; held {int(sum(y)):2d}; Brier mine {B(me, y):.4f}, their median {B(md, y):.4f}, each forecaster {each}; mean odds mine {np.mean(me):.3f}, theirs {np.mean(md):.3f}; closer: mine {cm}, theirs {ct}, equal {len(sel) - cm - ct}")
    return B(me, y), B(md, y), cm, ct
print()
for st in dict.fromkeys(r['study'] for r, f, m in S): block(st, [x for x in S if x[0]['study'] == st])
mine34, their34, cm, ct = block("all four sheets", S)
y = np.array([float(r['outcome']) for r, f, m in S]); me = np.array([float(r['odds']) for r, f, m in S]); md = np.array([m for r, f, m in S])
auc = lambda p: np.mean([(a > b) + 0.5 * (a == b) for a in p[y == 1] for b in p[y == 0]])
print(f"held against failed, how often the held line had the higher odds: mine {auc(me):.2f}, theirs {auc(md):.2f}")
dd = (me - y) ** 2 - (md - y) ** 2; rng = np.random.default_rng(0); bs = [dd[rng.integers(0, len(dd), len(dd))].mean() for _ in range(10000)]
print(f"difference in Brier score, mine minus theirs: {dd.mean():+.4f}; resampling the {len(dd)} lines as if independent: {np.percentile(bs, 2.5):+.3f} to {np.percentile(bs, 97.5):+.3f}")
# all ten main sheets
ALL = [r for r in csv.DictReader(open(sys.argv[1])) if r['kind'] == 'sheet' and r['outcome'] != '']
med = {r['label'] + r['file']: m for r, f, m in rows}
yy = np.array([float(r['outcome']) for r in ALL]); mm = np.array([float(r['odds']) for r in ALL]); ff = np.array([float(r['forecasters']) if r['forecasters'] else med[r['label'] + r['file']] for r in ALL])
print(f"\nall ten main sheets: {len(ALL)} settled lines; held {int(yy.sum())}; Brier mine {B(mm, yy):.4f}, forecasters' median {B(ff, yy):.4f}; mean odds mine {mm.mean():.3f}, theirs {ff.mean():.3f}; closer: mine {int((abs(mm - yy) < abs(ff - yy) - 1e-9).sum())}, theirs {int((abs(ff - yy) < abs(mm - yy) - 1e-9).sum())}")
auc2 = lambda p: np.mean([(a > b) + 0.5 * (a == b) for a in p[yy == 1] for b in p[yy == 0]])
print(f"held against failed, how often the held line had the higher odds: mine {auc2(mm):.2f}, theirs {auc2(ff):.2f}")
dd = (mm - yy) ** 2 - (ff - yy) ** 2; bs = [dd[rng.integers(0, len(dd), len(dd))].mean() for _ in range(10000)]
print(f"difference, mine minus theirs: {dd.mean():+.4f}; resampling the lines as if independent: {np.percentile(bs, 2.5):+.3f} to {np.percentile(bs, 97.5):+.3f}")
st = [r['study'] for r in ALL]; names = list(dict.fromkeys(st)); ds = np.array([dd[[s == n for s in st]].sum() for n in names]); bs = [ds[rng.integers(0, len(ds), len(ds))].sum() / len(dd) for _ in range(10000)]
print(f"resampling whole sheets: {np.percentile(bs, 2.5):+.3f} to {np.percentile(bs, 97.5):+.3f} (approximate: sheets differ in size); sheets on which theirs scored better: {int(sum(d > 0 for d in ds))} of {len(ds)}")
for lo, hi in ((0.0, 0.6), (0.6, 0.8), (0.8, 0.9), (0.9, 1.01)):
    k = (ff >= lo) & (ff < hi)
    if k.any(): print(f"   their odds {lo:.2f} to {min(hi, 1.0):.2f}: {int(k.sum()):3d} lines; their mean {ff[k].mean():.3f}; held {yy[k].mean():.3f} ({int(yy[k].sum())} of {int(k.sum())})")
# the seven sealed lines
a = {r['label']: m for r, f, m in rows}
arc = [x for x in S if x[0]['study'] == 'arctic circle']; can = [x for x in S if x[0]['study'] == 'cannonballs']; aut = [x for x in S if x[0]['study'] == 'readers and authors']
bb = lambda sel: (B([float(r['odds']) for r, f, m in sel], [float(r['outcome']) for r, f, m in sel]), B([m for r, f, m in sel], [float(r['outcome']) for r, f, m in sel]))
V = dict(N1=(their34 < mine34, f"{their34:.4f} against {mine34:.4f}"), N2=(bb(arc)[1] < bb(arc)[0], f"{bb(arc)[1]:.4f} against {bb(arc)[0]:.4f}"), N3=(a['A1'] >= 0.5, f"median for A1 {a['A1']:.2f}"),
         N4=(abs(bb(can)[1] - bb(can)[0]) <= 0.015, f"{bb(can)[1]:.4f} against {bb(can)[0]:.4f}"), N5=(B(ff, yy) < B(mm, yy), f"{B(ff, yy):.4f} against {B(mm, yy):.4f}"), N6=(ct > cm, f"theirs {ct}, mine {cm}"),
         N7=(abs(bb(aut)[1] - bb(aut)[0]) <= 0.05, f"{bb(aut)[1]:.4f} against {bb(aut)[0]:.4f}"))
import re
odds = dict(re.findall(r"^(N\d)\..*?odds (0\.\d+)[ \t]*$", open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), 'again-prediction.md')).read(), re.M | re.S)); tot = 0
print()
for k in sorted(V):
    p = float(odds[k]); h = bool(V[k][0]); tot += (p - h) ** 2; print(f"{k}  odds {p:.2f}  {'held' if h else 'FAILED':6s}  {V[k][1]}")
print(f"held {sum(bool(v[0]) for v in V.values())} of {len(V)}; my mean odds {np.mean([float(v) for v in odds.values()]):.3f}; Brier {tot / len(V):.4f}")
if len(sys.argv) > 3:
    with open(sys.argv[3], 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(['file', 'label', 'f1', 'f2', 'f3', 'median']); [w.writerow([r['file'], r['label'], *f, m]) for r, f, m in rows]
print("\nleaving one sheet out of the ten (Brier mine, theirs, difference):")
for n in names:
    k = np.array([s != n for s in st]); print(f"   without {n:22s} {int(k.sum()):3d} lines; mine {B(mm[k], yy[k]):.4f}, theirs {B(ff[k], yy[k]):.4f}, difference {B(mm[k], yy[k]) - B(ff[k], yy[k]):+.4f}")
late = np.array([r['forecasters'] == '' for r in ALL])
for name, k in (("the six sheets priced at the time", ~late), ("the four priced afterwards", late), ("of those, the three sheets with something to work out (cube, cannonballs, arctic)", late & np.array([s != 'readers and authors' for s in st])), ("of those, readers and authors", late & np.array([s == 'readers and authors' for s in st]))):
    a2 = lambda p: np.mean([(a > b) + 0.5 * (a == b) for a in p[k][yy[k] == 1] for b in p[k][yy[k] == 0]])
    print(f"   {name}: {int(k.sum())} lines; held {yy[k].mean():.3f}; mean odds mine {mm[k].mean():.3f}, theirs {ff[k].mean():.3f}; Brier mine {B(mm[k], yy[k]):.4f}, theirs {B(ff[k], yy[k]):.4f}; held above failed: mine {a2(mm):.2f}, theirs {a2(ff):.2f}")
sh = ff.mean() - mm.mean(); print(f"   my odds moved by {sh:+.3f} to their mean level would score {B(np.clip(mm + sh, 0.01, 0.99), yy):.4f} on the {len(yy)} lines")
import os, time
print("\nwhen each answer file was written (UTC, from the files' own times):")
for kq in (1, 2, 3): print("   forecaster", kq, " ".join(time.strftime('%H:%M:%S', time.gmtime(os.path.getmtime(f"{d}/f{kq}-{s}.json"))) for s in (1, 2, 3, 4)))
print("\nthe forecasters' median on all main-sheet lines, grouped as in the figure:")
for lo, hi in ((0.0, 0.5), (0.5, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 0.9), (0.9, 1.01)):
    k = (ff >= lo) & (ff < hi); print(f"   their odds {lo:.2f} to {min(hi, 1.0):.2f}: {int(k.sum()):3d} lines; their mean {ff[k].mean():.3f}; held {int(yy[k].sum())} of {int(k.sum())}")
    k = (mm >= lo) & (mm < hi); print(f"   my odds    {lo:.2f} to {min(hi, 1.0):.2f}: {int(k.sum()):3d} lines; my mean    {mm[k].mean():.3f}; held {int(yy[k].sum())} of {int(k.sum())}")
print(f"   lowest odds given to any main-sheet line: mine {mm.min():.2f}, theirs {ff.min():.2f}; lines below 0.3: mine {int((mm < 0.3).sum())}, theirs {int((ff < 0.3).sum())}")
