"""My sealed odds against three blind forecasters.   usage: python -I score.py expectations.md results.json FORECASTDIR"""
import sys, re, json
import numpy as np
text = open(sys.argv[1], encoding='utf-8').read()
mine = {}
for m in re.finditer(r"^(M\d+)\.(.*?)odds (0\.\d+)\s*$", text, re.M | re.S):
    mine[m.group(1)] = float(m.group(3))
verd = json.load(open(sys.argv[2]))['verdicts']
ids = sorted(verd, key=lambda k: int(k[1:]))
assert sorted(mine) == sorted(ids), (sorted(mine), ids)
assert all(v is not None for v in verd.values()), "a void expectation"
y = np.array([1.0 if verd[i] else 0.0 for i in ids])
F = np.array([[float(json.load(open(f"{sys.argv[3]}/f{k}.json"))[i]) for i in ids] for k in (1, 2, 3)])
me = np.array([mine[i] for i in ids]); med = np.median(F, axis=0)
print("      outcome   mine   forecasters (three)      their median")
for j, i in enumerate(ids):
    print(f"{i:4s}  {'held  ' if y[j] else 'failed'}    {me[j]:.2f}   {F[0, j]:.2f}  {F[1, j]:.2f}  {F[2, j]:.2f}        {med[j]:.2f}")
brier = lambda p: float(((p - y) ** 2).mean())
print(f"held {int(y.sum())} of {len(y)}")
print(f"Brier score (lower is better): mine {brier(me):.4f}; forecasters' median {brier(med):.4f}; each forecaster {', '.join(f'{brier(F[k]):.4f}' for k in range(3))}; "
      f"saying {y.mean():.2f} every time {brier(np.full(len(y), y.mean())):.4f}; saying 0.5 every time 0.2500")
print(f"mean probability: mine {me.mean():.3f}; forecasters' median {med.mean():.3f}; share that held {y.mean():.3f}")
d = (me - y) ** 2 - (med - y) ** 2
rng = np.random.default_rng(0)
bs = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(10000)]
print(f"difference in Brier score, mine minus theirs: {d.mean():+.4f}; resampling the eleven expectations: {np.percentile(bs, 2.5):+.3f} to {np.percentile(bs, 97.5):+.3f}")
print(f"correlation between my odds and their median: {np.corrcoef(me, med)[0, 1]:.2f}")
json.dump(dict(ids=ids, outcome=y.tolist(), mine=me.tolist(), forecasters=F.tolist(), median=med.tolist()), open(sys.argv[3] + '/scored.json', 'w'), indent=1)
