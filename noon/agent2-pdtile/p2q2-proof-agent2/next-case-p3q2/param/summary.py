"""One line per region or band: how many patterns have a single certificate, how many a tree, leaves by category."""
import pickle, sys, os
from collections import Counter
def leaves(r, d=0):
    if r['cat'] == 'split': yield from leaves(r['pos'], d + 1); yield from leaves(r['neg'], d + 1)
    else: yield d, r
rows = []
for name in sys.argv[1:]:
    fn = f"split_{name}.pkl" if os.path.exists(f"split_{name}.pkl") else f"region_{name}.pkl"
    res = pickle.load(open(fn, "rb")); single = trees = nl = 0; cats = Counter(); depth = 0; bad = 0
    for Z, r in res.items():
        if r['cat'] in ('L2', 'a'): continue
        lv = list(leaves(r)); nl += len(lv); depth = max(depth, max(d for d, _ in lv))
        if r['cat'] == 'split': trees += 1
        else: single += 1
        for _, l in lv:
            cats[l['cat']] += 1
            if l['cat'] in ('?', 'empty?'): bad += 1
    rows.append((name, single, trees, depth, nl, dict(cats), bad))
    print(f"| {name} | {single} | {trees} | {depth} | {nl} | " + ", ".join(f"{k} {v}" for k, v in sorted(cats.items())) + f" | {bad} |")
