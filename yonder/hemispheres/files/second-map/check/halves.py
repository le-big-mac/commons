"""Task A2: for each grid, with a hard edge, the share of people in the half centred at 52.37 N, 12.68 E and in the
half centred at 46.0 N, 7.18 E, their difference in points and in millions, and the total; compared with the
author's JSON and with the 30-arc-second count of regrid.py where there is one.

usage: python -I halves.py OUT.json NAME=GRID.npy[=AUTHOR.json[=REGRID.json]] ...
Uses chk.py (the checker's), by two methods (dot-product mask; row cumulative sums), and no code of the author's."""
import sys, json, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chk

FIX = dict(berlin=(52.37, 12.68), valais=(46.0, 7.18), palatinate=(49.4, 12.4), rankin=(46.5, 7.0))
out = {}
print('name | total | Berlin half % | Valais half % | L points | only Berlin M | only Valais M | Berlin minus Valais M | Palatinate % || largest disagreement with author (share, points; people) | L on 30" pixels')
for spec in sys.argv[2:]:
    parts = spec.split('=')
    name, gpath = parts[0], parts[1]
    P = np.load(gpath)
    tot = float(P.sum())
    m = {k: chk.mask_dot(*v) for k, v in FIX.items()}
    s = {k: float(P[m[k]].sum()) for k in FIX}
    cum = chk.Cum(P)
    s2 = {k: cum.share(*v) * tot for k, v in FIX.items()}
    two_methods = max(abs(s[k] - s2[k]) for k in FIX)
    ob = float(P[m['berlin'] & ~m['valais']].sum()); ov = float(P[m['valais'] & ~m['berlin']].sum())
    L = 100 * (s['berlin'] - s['valais']) / tot
    r = dict(total=tot, share={k: s[k] / tot for k in FIX}, L=L, only_berlin=ob, only_valais=ov, diff_millions=(s['berlin'] - s['valais']) / 1e6,
             two_methods_max_diff_people=two_methods)
    cmp_txt = ''
    if len(parts) > 2 and os.path.exists(parts[2]):
        a = json.load(open(parts[2]))
        dshare = max(abs(a['hard'][k] - s[k] / tot) for k in FIX) * 100
        dpeople = max(abs(a['only_berlin'] - ob), abs(a['only_valais'] - ov), abs(a['total'] - tot))
        dL = abs(a['L'] - L)
        r.update(author_max_share_diff_points=dshare, author_max_people_diff=dpeople, author_L_diff=dL)
        cmp_txt = f'{dshare:.2e} pts; {dpeople:.3f} people; L {dL:.2e}'
    nat = ''
    if len(parts) > 3 and os.path.exists(parts[3]):
        g = json.load(open(parts[3]))['native']
        r['native_L'] = g['L']; r['native_diff_millions'] = (g['only_berlin'] - g['only_valais']) / 1e6
        nat = f"{g['L']:+.4f} ({r['native_diff_millions']:+.2f} M)"
    out[name] = r
    print(f"{name} | {tot / 1e9:.4f} | {100 * s['berlin'] / tot:.4f} | {100 * s['valais'] / tot:.4f} | {L:+.4f} | {ob / 1e6:.2f} | {ov / 1e6:.2f} | {(s['berlin'] - s['valais']) / 1e6:+.2f} | "
          f"{100 * s['palatinate'] / tot:.4f} || {cmp_txt} | {nat}   [two methods differ by {two_methods:.4f} people]", flush=True)
json.dump(out, open(sys.argv[1], 'w'), indent=1)
