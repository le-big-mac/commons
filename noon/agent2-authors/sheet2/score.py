"""Author, readers and outsider on one sheet or on several.   usage: python -I score.py DIR [DIR ...]
Each DIR holds results.json (verdicts by the letter), author/odds-quick.json, optionally author/odds-careful.json,
readers/f1..f3.json and mine.json.  With several DIRs the sheets are scored one by one and then together."""
import sys, json, os
import numpy as np
rng = np.random.default_rng(0)
def load_sheet(D):
    verd = json.load(open(f"{D}/results.json"))['verdicts']
    ids = sorted(verd, key=lambda k: int(k[1:]))
    get = lambda p: np.array([float(json.load(open(p))[i]) for i in ids])
    out = dict(ids=ids, y=np.array([1.0 if verd[i] else 0.0 for i in ids]), quick=get(f"{D}/author/odds-quick.json"), mine=get(f"{D}/mine.json"),
               F=np.array([get(f"{D}/readers/f{k}.json") for k in (1, 2, 3)]))
    out['careful'] = get(f"{D}/author/odds-careful.json") if os.path.exists(f"{D}/author/odds-careful.json") else None
    out['med'] = np.median(out['F'], axis=0)
    return out
brier = lambda p, y: float(((p - y) ** 2).mean())
def auc(p, y):
    h, f = p[y == 1], p[y == 0]
    return float('nan') if len(h) == 0 or len(f) == 0 else float(((h[:, None] > f[None, :]).sum() + 0.5 * (h[:, None] == f[None, :]).sum()) / (len(h) * len(f)))
def gap(a, b, y, name):
    d = (a - y) ** 2 - (b - y) ** 2
    bs = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(10000)]
    ca = int((np.abs(a - y) < np.abs(b - y) - 1e-9).sum()); cb = int((np.abs(b - y) < np.abs(a - y) - 1e-9).sum())
    print(f"   {name}: difference {d.mean():+.4f} ({np.percentile(bs, 2.5):+.3f} to {np.percentile(bs, 97.5):+.3f}); closer to the outcome: first {ca}, second {cb}, equal {len(y) - ca - cb}")
def report(name, s):
    y = s['y']
    print(f"=== {name}: {int(y.sum())} held, {int((y == 0).sum())} failed")
    print("      outcome  author quick  author careful  readers (three)     their median   outsider (Noon)")
    for j, i in enumerate(s['ids']):
        c = f"{s['careful'][j]:.2f}" if s['careful'] is not None else " -  "
        print(f"{i:4s}  {'held  ' if y[j] else 'failed'}   {s['quick'][j]:.2f}          {c}            {s['F'][0, j]:.2f} {s['F'][1, j]:.2f} {s['F'][2, j]:.2f}      {s['med'][j]:.2f}           {s['mine'][j]:.2f}")
    line = f"Brier score (lower is better): author quick {brier(s['quick'], y):.4f}; "
    if s['careful'] is not None:
        line += f"author careful {brier(s['careful'], y):.4f}; "
    line += f"readers' median {brier(s['med'], y):.4f}; each reader {', '.join(f'{brier(s['F'][k], y):.4f}' for k in range(3))}; outsider {brier(s['mine'], y):.4f}; saying {y.mean():.2f} every time {brier(np.full(len(y), y.mean()), y):.4f}"
    print(line)
    if 0 < y.sum() < len(y):
        print(f"ranking what held above what failed: author quick {auc(s['quick'], y):.3f}; readers {auc(s['med'], y):.3f}; outsider {auc(s['mine'], y):.3f}" + (f"; author careful {auc(s['careful'], y):.3f}" if s['careful'] is not None else ""))
    print(f"mean odds: author quick {s['quick'].mean():.3f}; readers {s['med'].mean():.3f}; outsider {s['mine'].mean():.3f}; share that held {y.mean():.3f}")
    print("differences in Brier score, first minus second (positive: the first is worse):")
    gap(s['quick'], s['med'], y, "author quick against readers")
    if s['careful'] is not None:
        gap(s['careful'], s['quick'], y, "author careful against author quick")
        gap(s['careful'], s['med'], y, "author careful against readers")
    gap(s['mine'], s['med'], y, "outsider against readers")
    gap(s['mine'], s['quick'], y, "outsider against author quick")
    print(f"agreement (correlation): readers with each other {np.mean([np.corrcoef(s['F'][a], s['F'][b])[0, 1] for a, b in ((0, 1), (0, 2), (1, 2))]):.2f}; author quick with readers {np.corrcoef(s['quick'], s['med'])[0, 1]:.2f}; "
          f"outsider with readers {np.corrcoef(s['mine'], s['med'])[0, 1]:.2f}; outsider with author quick {np.corrcoef(s['mine'], s['quick'])[0, 1]:.2f}")
sheets = [load_sheet(D) for D in sys.argv[1:]]
for D, s in zip(sys.argv[1:], sheets):
    report(D, s)
    json.dump(dict(ids=s['ids'], outcome=s['y'].tolist(), quick=s['quick'].tolist(), careful=None if s['careful'] is None else s['careful'].tolist(), readers=s['F'].tolist(), median=s['med'].tolist(),
                   outsider=s['mine'].tolist()), open(f"{D}/scored.json", 'w'), indent=1)
if len(sheets) > 1:
    both = dict(ids=sum((s['ids'] for s in sheets), []), y=np.concatenate([s['y'] for s in sheets]), quick=np.concatenate([s['quick'] for s in sheets]), mine=np.concatenate([s['mine'] for s in sheets]),
                F=np.concatenate([s['F'] for s in sheets], axis=1), med=np.concatenate([s['med'] for s in sheets]), careful=None)
    report("both sheets together", both)
