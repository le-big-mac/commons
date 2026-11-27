# The northern photometers that stand furthest from "no change" on the page's figure, month by month, so that the page
# can say what each one does. Uses the same series as tonga_page.py (each month less the same month of 2021 and 2024).
import importlib.util, io, contextlib
import numpy as np
spec = importlib.util.spec_from_file_location('tonga_page', '/home/agent1/night/src/tonga_page.py'); TP = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(TP)   # runs the page program quietly; it rewrites its own table and pictures
S = TP.S; d2 = TP.d2; pct = TP.pct
allnorth = TP.north + TP.canary
D = {st: d2(st) for st in allnorth}; D = {k: v for k, v in D.items() if v is not None}
print(f'photometers north of the equator with the figure: {len(D)} ({len([s for s in D if S[s]["lat"] >= 30])} north of 30 degrees, {len([s for s in D if S[s]["lat"] < 30])} between)')
print('all of them, from the brightest twilight in May to November 2022 to the darkest (magnitudes; parts in 100 brighter):')
for st, v in sorted(D.items(), key=lambda kv: kv[1]):
    print(f"   {st:<9} {S[st]['lat']:+6.1f} {S[st]['lon']:+7.1f}  {v:+.2f} {pct(v):+4.0f}   {S[st]['name'][:40]}")
print('\nthe ones at -0.10 or below, month by month (hundredths of a magnitude; negative: a brighter twilight; . no figure); then evening alone and morning alone for May to November 2022')
MON = [(y, m) for y in (2021, 2022, 2023, 2024) for m in (1, 3, 5, 7, 9, 11)]
for st, v in sorted(D.items(), key=lambda kv: kv[1]):
    if v > -0.10: continue
    a = S[st]['a']
    line = ' | '.join(' '.join(f"{100 * a[(y, m)]:+4.0f}" if (y, m) in a else '   .' for m in (1, 3, 5, 7, 9, 11)) for y in (2021, 2022, 2023, 2024))
    ev = [S[st]['e'][(2022, m)] for m in (5, 7, 9, 11) if (2022, m) in S[st]['e']]; mo = [S[st]['mo'][(2022, m)] for m in (5, 7, 9, 11) if (2022, m) in S[st]['mo']]
    have = [m for m in (5, 7, 9, 11) if (2022, m) in a]
    base = {m: [yy for yy in (2021, 2024) if any(k == (yy, m) for k in a)] for m in have}
    print(f"   {st:<9} {line}   evening {np.mean(ev):+.2f}, morning {np.mean(mo):+.2f}; months of 2022 in the figure: {have}")
n30 = [v for s, v in D.items() if S[s]['lat'] >= 30]
print(f'\nnorth of 30 degrees: {len(n30)} with the figure; at -0.15 or below {sum(1 for v in n30 if v <= -0.15)}; at -0.25 or below {sum(1 for v in n30 if v <= -0.25)}; within 0.10 of nothing {sum(1 for v in n30 if abs(v) < 0.10)}; middle {np.median(n30):+.3f}')
print(f'the southern eleven for comparison: from {max(TP.ds):+.2f} to {min(TP.ds):+.2f}; at -0.25 or below {sum(1 for v in TP.ds if v <= -0.25)}')
# ---- the record of the one northern photometer whose months look like the south's (stars71, Tournefeuille near Toulouse)
import glob, re
print('\nstars71, month by month from its files: rows; the zero point the rows print; the middle step between rows in seconds; first and last row')
for f in sorted(glob.glob('/home/agent1/night/data/tw/stars71_202[12]-??.dat')):
    rows = [l.split(';') for l in open(f, encoding='latin-1') if not l.startswith('#') and l.count(';') >= 7]
    if not rows: print(f"   {f[-11:-4]}  no rows"); continue
    t = np.array([r[0][:19] for r in rows], dtype='datetime64[s]').astype('int64'); zp = sorted({r[6] for r in rows})
    change = next((rows[i][0][:16] for i in range(1, len(rows)) if rows[i][6] != rows[i - 1][6]), None)
    print(f"   {f[-11:-4]}  {len(rows):6d} rows; zero point {'/'.join(zp)}" + (f' (changes at {change})' if change else '') + f"; step {np.median(np.diff(t)) if len(t) > 1 else float('nan'):.0f}; {rows[0][0][:16]} to {rows[-1][0][:16]}")
print('   months of 2021 and 2022 on the six-month list with no file in the folder: ' + ', '.join(f'{y}-{m:02d}' for y in (2021, 2022) for m in (1, 3, 5, 7, 9, 11) if not glob.glob(f'/home/agent1/night/data/tw/stars71_{y}-{m:02d}.dat')))
