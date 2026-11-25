"""Build explore.html: a globe you can drag; the half facing you is a hemisphere, and the page shows its shares of
the world's land, people and woodpecker species as you move it. Self-contained (no outside resources).

usage: make_explore.py GRID_DIR OUT_DIR TEMPLATE.html OUTPUT.html

Data embedded (all derived from the grids of this project, coarsened):
  land    coverage on a 0.25-degree grid, one byte per cell
  people  eight epochs of GHS-POP on a 0.5-degree grid, square roots rounded to 16 bits, non-empty cells only
  birds   the woodpecker weights per 5-degree box (three non-species dropped), as text
Shares on the page therefore differ from the note's in the second decimal; the page shows one decimal.
"""
import base64
import json
import os
import sys
import numpy as np

gdir, odir, template, output = sys.argv[1:5]
land = np.load(f'{gdir}/land10.npy')                       # 3600 x 7200 coverage
f = 5
land_q = land.reshape(land.shape[0] // f, f, land.shape[1] // f, f).mean(axis=(1, 3))        # 720 x 1440
land8 = np.clip(np.round(land_q * 255), 0, 255).astype(np.uint8)
years = [(1975, 'pop005_1975'), (2000, 'pop005_2000'), (2005, 'pop005_2005'), (2010, 'pop005_2010'), (2015, 'pop005_2015'),
         (2020, 'pop005'), (2025, 'pop005_2025'), (2030, 'pop005_2030')]
pops = []
for y, name in years:
    p = np.load(f'{gdir}/{name}.npy')
    pops.append(p.reshape(360, 10, 720, 10).sum(axis=(1, 3)))
union = np.zeros((360, 720), dtype=bool)
for p in pops:
    union |= p > 0
idx = np.flatnonzero(union).astype(np.uint32)
roots = [np.clip(np.round(np.sqrt(p.ravel()[idx])), 0, 65535).astype(np.uint16) for p in pops]
totals = [float(p.sum()) for p in pops]
for (y, _), r, t in zip(years, roots, totals):
    back = float((r.astype(np.float64) ** 2).sum())
    print(f'{y}: {t:,.0f} people; after rounding square roots {back:,.0f} ({100 * (back / t - 1):+.4f}%)')
# woodpecker weights of the cleaned list (woodpeckers_clean.py logic, three keys dropped), recomputed here from the maps file
W = np.load(f'{odir}/woodpecker-clean-weights.npy')
b64 = lambda a: base64.b64encode(a.tobytes()).decode('ascii')
data = dict(land=b64(land8), landH=720, landW=1440, popIdx=b64(idx), popRoots=[b64(r) for r in roots], popYears=[y for y, _ in years],
            popTotals=totals, birds=[[round(float(v), 5) for v in row] for row in W])
html = open(template, encoding='utf-8').read()
assert html.count('/*DATA*/') == 1
html = html.replace('/*DATA*/', 'const DATA = ' + json.dumps(data, separators=(',', ':')) + ';')
open(output, 'w', encoding='utf-8').write(html)
print('land cells with any land', int((land8 > 0).sum()), '; people cells', len(idx), '; file', os.path.getsize(output) // 1024, 'kB')
