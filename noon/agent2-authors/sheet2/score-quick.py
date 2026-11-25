"""The quick-readers arm against the other parties.   usage: python -I score-quick.py DIR1 DIR2
Each DIR holds scored.json (from score.py) and quick/f1..f3.json."""
import sys, json
import numpy as np
rng = np.random.default_rng(0)
brier = lambda p, y: float(((p - y) ** 2).mean())
allq, ally, allauth, allmed, allme, allF = [], [], [], [], [], []
for D in sys.argv[1:]:
    s = json.load(open(f"{D}/scored.json")); ids = s['ids']; y = np.array(s['outcome'])
    Q = np.array([[float(json.load(open(f"{D}/quick/f{k}.json"))[i]) for i in ids] for k in (1, 2, 3)]); qm = np.median(Q, axis=0)
    auth, med, me = np.array(s['quick']), np.array(s['median']), np.array(s['outsider'])
    print(f"=== {D}")
    print("      outcome  quick readers (three)   their median   careful readers   author quick   outsider")
    for j, i in enumerate(ids):
        print(f"{i:4s}  {'held  ' if y[j] else 'failed'}   {Q[0, j]:.2f} {Q[1, j]:.2f} {Q[2, j]:.2f}          {qm[j]:.2f}           {med[j]:.2f}              {auth[j]:.2f}           {me[j]:.2f}")
    print(f"Brier: quick readers' median {brier(qm, y):.4f} (each {', '.join(f'{brier(Q[k], y):.4f}' for k in range(3))}); careful readers {brier(med, y):.4f}; author quick {brier(auth, y):.4f}; outsider {brier(me, y):.4f}"
          + (f"; author careful {brier(np.array(s['careful']), y):.4f}" if s.get('careful') else ""))
    print(f"   quick readers closer than the author's quick odds on {int((np.abs(qm - y) < np.abs(auth - y) - 1e-9).sum())} of {len(y)} (author closer on {int((np.abs(auth - y) < np.abs(qm - y) - 1e-9).sum())}); "
          f"careful readers closer than quick readers on {int((np.abs(med - y) < np.abs(qm - y) - 1e-9).sum())}; quick readers agree with each other at {np.mean([np.corrcoef(Q[a], Q[b])[0, 1] for a, b in ((0, 1), (0, 2), (1, 2))]):.2f}; mean odds {qm.mean():.3f}")
    allq.append(qm); ally.append(y); allauth.append(auth); allmed.append(med); allme.append(me); allF.append(Q)
    json.dump(dict(ids=ids, quick_readers=Q.tolist(), median=qm.tolist()), open(f"{D}/quick/scored.json", 'w'), indent=1)
q, y, a, m, me = map(np.concatenate, (allq, ally, allauth, allmed, allme))
print("=== both sheets together")
print(f"Brier: quick readers {brier(q, y):.4f}; careful readers {brier(m, y):.4f}; authors' quick odds {brier(a, y):.4f}; outsider {brier(me, y):.4f}")
def gap(x, z, name):
    d = (x - y) ** 2 - (z - y) ** 2
    bs = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(10000)]
    print(f"   {name}: difference {d.mean():+.4f} ({np.percentile(bs, 2.5):+.3f} to {np.percentile(bs, 97.5):+.3f}); closer: first {int((np.abs(x - y) < np.abs(z - y) - 1e-9).sum())}, second {int((np.abs(z - y) < np.abs(x - y) - 1e-9).sum())}")
gap(q, m, "quick readers against careful readers")
gap(q, a, "quick readers against authors' quick odds")
gap(q, me, "quick readers against the outsider")
gap(a, m, "authors' quick odds against careful readers")
