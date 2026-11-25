"""Third reading, step 3: Freeth's Note S5 sentence 'for both lunar and solar the North-South divide is in complete agreement
between the EPs in the model and actual eclipses', tested on cycle 0.  usage: run14.py CATDIR [CATDIR...]"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cat2, lists2
K0 = json.load(open(os.path.join(HERE, 'k0.json')))['K0']
FL, FS, info, _ = lists2.freeth()
LE, _, _ = cat2.load('LE', sys.argv[1:], verbose=False); SE, _, _ = cat2.load('SE', sys.argv[1:], verbose=False)
LM = {int(round(cat2.k_of(r['jd']) - 0.5)) - K0 + 1: r for r in LE}
SM = {int(round(cat2.k_of(r['jd']))) - K0: r for r in SE}
# lunar: Note S1: Sun before the descending node point or after the ascending -> Moon SOUTH; otherwise north.
rows = []
for n in FL:
    d, node = info[('L', n)]
    north = (d > 0) if node == 'D' else (d < 0)
    if n in LM: rows.append((n, d, node, 'N' if north else ('at' if d == 0 else 'S'), LM[n]['gamma']))
bad = [r for r in rows if r[1] != 0 and ((r[3] == 'N') != (r[4] > 0))]
print(f'lunar glyph months with an eclipse in cycle 0: {len(rows)}; model north/south against the sign of gamma: disagreements {bad}; at the node point: {[r for r in rows if r[1] == 0]}')
rows = []
for n in FS:
    d, node, ns = info[('S', n)]
    if n in SM: rows.append((n, d, node, ns if d != 0 else 'at', SM[n]['gamma']))
bad = [r for r in rows if r[1] != 0 and ((r[3] == 'N') != (r[4] > 0))]
print(f'solar glyph months with an eclipse in cycle 0: {len(rows)}; disagreements {bad}; at the node point: {[r for r in rows if r[1] == 0]}')
# visible-from-Greece is beyond these pages; but how many of the 28 matched solar eclipses are central (A/T/H) and how many small partials
print('types of the 28 matched solar eclipses:', sorted(SM[n]['typ'] for n in FS if n in SM))
