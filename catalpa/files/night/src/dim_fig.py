# The picture by latitude for the darker northern twilight of 2019: every place that gives a figure, set by how far
# north it stands. Up: how much darker the twilight read with the Sun 3 degrees down from September to November 2019
# than in the same months of 2018 (the mean of the months both years give, two or more), as per cent of light.
#   orange dots: the first make's northern places already in hand (cache2/years.pkl; the two odd units left out)
#   orange rings: the first make's photometers of the nineteenth sheet (cache2/north_new.pkl; one chip; Vienna left out)
#   (until the twentieth sheet the second make's five Korean stations and the one in Germany stood here in green;
#    in that make an ordinary year steps as much as 2019 did, sqm_before.out, and they are left out)
#   violet squares: four meters of a third group, read off published figures (lit/scout-print-2019.md): August to
#                   December 2019 against January to June 2019 about the paper's fitted line, Sun 6 to 7 degrees down
import pickle, importlib.util
import numpy as np
B = '/home/agent1/night/'
def mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
DP = mod('depth', B + 'src/depth.py')
AUT = (9, 10, 11); pct = lambda mag: 100 * (1 - 10 ** (-0.4 * mag)); pts = []
R = dict(pickle.load(open(B + 'cache2/depth.pkl', 'rb'))); R.update(pickle.load(open(B + 'cache2/years.pkl', 'rb')))
for st in DP.NORTH:
    if st in ('stars4', 'stars426'): continue
    chips = {}
    for (s, y, m), r in R.items():
        if s == st and y == 2021 and r is not None and DP.monthfig(r, 3.0) is not None: chips[(r.get('mac') or '')[-8:]] = chips.get((r.get('mac') or '')[-8:], 0) + 1
    if not chips: continue
    ch = max(chips, key=chips.get); V = {(y, m): DP.monthfig(r, 3.0) for (s, y, m), r in R.items() if s == st and r is not None and (r.get('mac') or '')[-8:] == ch and DP.monthfig(r, 3.0) is not None}
    d = [V[(2019, m)] - V[(2018, m)] for m in AUT if (2019, m) in V and (2018, m) in V]
    if len(d) >= 2: pts.append(('first make, in hand', st, float(DP.geo[st]['latitude']), float(np.mean(d))))
N = pickle.load(open(B + 'cache2/north_new.pkl', 'rb')); POS = {}
for line in open(B + 'data/listing/north_new_probe.txt'):
    if ':' in line: st, lat, lon = line.split(':')[0].split(); POS[st] = float(lat)
for st in sorted({k[0] for k in N}):
    if len({r['mac'] for (s, y, m), r in N.items() if s == st and r is not None}) != 1 or st == 'stars65': continue      # stars65 (Vienna) stepped in May 2019 for a reason of its own (check/check-twilight-15.md) and is left out
    d = [N[(st, 2019, m)]['d3'] - N[(st, 2018, m)]['d3'] for m in AUT if N.get((st, 2019, m)) and N.get((st, 2018, m)) and N[(st, 2019, m)]['d3'] is not None and N[(st, 2018, m)]['d3'] is not None]
    if len(d) >= 2: pts.append(('first make, nineteenth sheet', st, POS[st], float(np.mean(d))))
for name, lat, v in (('Stockholm', 59.35, 0.16), ('Potsdam', 52.38, 0.19), ('Vienna', 48.23, 0.24), ('Bodinggraben', 47.79, 0.35)): pts.append(('second make, in print', name, lat, v))
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'; ORANGE = '#eb6834'; AQUA = '#1baf7a'; VIOLET = '#6250d6'
fig = plt.figure(figsize=(5.0, 4.0), facecolor=SURF); ax = fig.add_axes([0.135, 0.17, 0.845, 0.63]); ax.set_facecolor(SURF)
for kind, name, lat, v in pts:
    y = min(pct(v), 52.0)
    if kind == 'first make, in hand': ax.plot(lat, y, 'o', ms=8.5, color=ORANGE, mec=SURF, mew=1.2, zorder=5)
    elif kind == 'first make, nineteenth sheet': ax.plot(lat, y, 'o', ms=8.5, mfc=SURF, mec=ORANGE, mew=2.2, zorder=5)
    else: ax.plot(lat, y, 's', ms=10.0, mfc='none', mec=VIOLET, mew=2.0, zorder=7)
ax.axhline(0, color=INK2, lw=1.0, zorder=3)
for lat, name in ((27.9, 'Canaries'), (40.4, 'Madrid'), (59.3, 'Stockholm'), (78.1, 'Svalbard')): ax.text(lat, 4.4, name, fontsize=12.5, color=INK2, ha='center', va='center')      # where a few of the places are
for i, (mk, kw, lab) in enumerate((('o', dict(color=ORANGE, mec=SURF, mew=1.2, ms=8.5), 'meters I had first'), ('o', dict(mfc=SURF, mec=ORANGE, mew=2.2, ms=8.5), 'meters tested unseen'), ('s', dict(mfc='none', mec=VIOLET, mew=2.0, ms=10.0), 'in published papers'))):
    ax.plot(54.5, 53 - 5.0 * i, mk, zorder=6, **kw); ax.text(56.4, 53 - 5.0 * i, lab, fontsize=12.5, color=INK, va='center')
ax.set_xlim(25, 84); ax.set_ylim(-6, 57); ax.set_xticks([30, 40, 50, 60, 70, 80]); ax.set_xticklabels(['30°', '40°', '50°', '60°', '70°', '80°'], fontsize=14.5); ax.set_yticks([0, 20, 40]); ax.set_yticklabels(['0', '20', '40'], fontsize=15)
ax.grid(True, axis='y', color=GRID, lw=1); ax.set_axisbelow(True); ax.tick_params(colors=INK2, length=0)
for sp in ('top', 'right', 'left'): ax.spines[sp].set_visible(False)
ax.spines['bottom'].set_color(INK2)
fig.text(0.015, 0.978, 'twilight overhead, autumn 2019:', fontsize=14, color=INK2, va='top'); fig.text(0.015, 0.912, 'per cent darker than a year before', fontsize=14, color=INK2, va='top'); fig.text(0.56, 0.035, 'degrees north', fontsize=13, color=INK2, ha='center')
fig.savefig(B + 'img/dim-latitude.png', dpi=140, facecolor=SURF); plt.close(fig)
print('picture: img/dim-latitude.png; each place: kind, name, latitude, magnitudes darker, per cent darker')
for kind, name, lat, v in sorted(pts, key=lambda p: (p[0], p[2])): print(f'   {kind:<30} {name:<13} {lat:+6.1f}  {v:+.2f}  {pct(v):+4.0f}')
for kind in sorted({p[0] for p in pts}):
    v = [p[3] for p in pts if p[0] == kind]; print(f'   {kind}: {len(v)} places; the middle {np.median(v):+.2f} ({pct(np.median(v)):+.0f} per cent); from {min(v):+.2f} to {max(v):+.2f}; at +0.10 or above: {sum(x >= 0.10 for x in v)}')
