"""After the referee: what separates the parties.   usage: python -I controls.py SHEET1DIR SHEET2DIR"""
import sys, json
import numpy as np
P = {k: [] for k in ('quick readers', "authors' quick odds", 'Noon', 'careful readers')}; Y = []; per = []
for D in sys.argv[1:3]:
    s = json.load(open(f"{D}/scored.json")); q = json.load(open(f"{D}/quick/scored.json")); y = np.array(s['outcome'])
    d = {'quick readers': np.array(q['median']), "authors' quick odds": np.array(s['quick']), 'Noon': np.array(s['outsider']), 'careful readers': np.array(s['median'])}
    per.append((d, y, s))
    for k in P:
        P[k].append(d[k])
    Y.append(y)
y = np.concatenate(Y); P = {k: np.concatenate(v) for k, v in P.items()}
b = lambda p, yy: float(((p - yy) ** 2).mean())
print("Brier on the 21 that held / on the 3 that failed / mean odds on held / on failed:")
for k, p in P.items():
    print(f"   {k:20s} {b(p[y == 1], y[y == 1]):.4f} / {b(p[y == 0], y[y == 0]):.4f} / {p[y == 1].mean():.3f} / {p[y == 0].mean():.3f}")
print("each party given the careful readers' numbers, kept in the party's own order (sheet by sheet):")
for k in P:
    tot = []
    for d, yy, s in per:
        order = np.argsort(np.argsort(d[k], kind='stable'), kind='stable')          # rank of each statement in the party's own odds
        tot.append((np.sort(d['careful readers'])[order] - yy) ** 2)
    print(f"   {k:20s} {np.concatenate(tot).mean():.4f}")
print("direction only (0.9 where the party said more than 0.5, otherwise 0.1):")
for k, p in P.items():
    print(f"   {k:20s} {b(np.where(p > 0.5, 0.9, 0.1), y):.4f}")
d, yy, s = per[0]
quick, careful = np.array(s['quick']), np.array(s['careful'])
shift = (careful - quick).mean()
print(f"first sheet: the author's careful pass moved its odds by {shift:+.3f} on average; adding that to every quick number scores {b(np.clip(quick + shift, 0.01, 0.99), yy):.4f} (the pass itself {b(careful, yy):.4f}); "
      f"saying 0.85 for all twelve scores {b(np.full(12, 0.85), yy):.4f}")
print("first sheet, mean odds: " + "; ".join(f"{k} {d[k].mean():.3f}" for k in d) + f"; author careful {careful.mean():.3f}")
me, au = P['Noon'], P["authors' quick odds"]
rng = np.random.default_rng(0); dd = (me - y) ** 2 - (au - y) ** 2
bs = [dd[rng.integers(0, 24, 24)].mean() for _ in range(10000)]
print(f"Noon against the authors' quick odds: {dd.mean():+.4f} ({np.percentile(bs, 2.5):+.3f} to {np.percentile(bs, 97.5):+.3f}); closer: Noon {int((np.abs(me - y) < np.abs(au - y) - 1e-9).sum())}, authors {int((np.abs(au - y) < np.abs(me - y) - 1e-9).sum())}")
for i, (d, yy, s) in enumerate(per, 1):
    q = json.load(open(f"{sys.argv[i]}/quick/scored.json"))
    print(f"sheet {i}: mean odds: quick readers {np.mean(q['median']):.3f}, careful readers {np.mean(s['median']):.3f}; quick readers minus author's quick odds {b(d['quick readers'], yy) - b(d[chr(34) + 'x' if False else 'authors\' quick odds'], yy):+.4f}")
