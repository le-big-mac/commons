# The picture for the fold on the darker northern twilight of 2019: how much darker the twilight read with the Sun
# 3 degrees down than in the same month of 2018, month by month through 2019 and 2020: the middle of the first
# make's northern places (my reduction: cache2/years.pkl) and the middle of the second make's Korean stations
# (data/sqm3, by src/sqm_north.py's function). Three places or more for a middle. Per cent darker = what a
# reading so many magnitudes fainter means in light.
import pickle, importlib.util
import numpy as np
B = '/home/agent1/night/'
def mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
DP = mod('depth', B + 'src/depth.py'); SN = mod('sn', B + 'src/sqm_north.py')
R = dict(pickle.load(open(B + 'cache2/depth.pkl', 'rb'))); R.update(pickle.load(open(B + 'cache2/years.pkl', 'rb')))
def readings(st, dp=3.0):
    chips = {}
    for (s, y, m), r in R.items():
        if s == st and y == 2021 and r is not None and DP.monthfig(r, dp) is not None: chips[(r.get('mac') or '')[-8:]] = chips.get((r.get('mac') or '')[-8:], 0) + 1
    if not chips: return {}
    ch = max(chips, key=chips.get)
    return {(y, m): DP.monthfig(r, dp) for (s, y, m), r in R.items() if s == st and r is not None and (r.get('mac') or '')[-8:] == ch and DP.monthfig(r, dp) is not None}
T1 = {st: readings(st) for st in DP.NORTH if st not in ('stars4', 'stars426')}          # the two odd units are left out, as in raikoke_night.out
ST = SN.F4.stations(); KOR = ('SNUO', 'CEOU', 'YFAO', 'DAO', 'GYTI'); T2 = {}
for c in KOR:
    T2[c] = {}
    for y in (2018, 2019, 2020):
        for m in range(1, 13):
            r = SN.month(c, ST[c][0], ST[c][1], y, m)
            if r is not None and r[3.0] is not None: T2[c][(y, m)] = r[3.0]
KS = [(y, m) for y in (2019, 2020) for m in range(1, 13)]; pct = lambda mag: 100 * (1 - 10 ** (-0.4 * mag))
def middle(T, k):
    v = [T[s][k] - T[s][(2018, k[1])] for s in T if k in T[s] and (2018, k[1]) in T[s]]; return (float(np.median(v)), len(v)) if len(v) >= 3 else (None, len(v))
m1 = [middle(T1, k) for k in KS]; m2 = [middle(T2, k) for k in KS]
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'; ORANGE = '#eb6834'; AQUA = '#1baf7a'
fig = plt.figure(figsize=(5.0, 4.0), facecolor=SURF); ax = fig.add_axes([0.135, 0.13, 0.845, 0.67]); ax.set_facecolor(SURF)
def line(mm, col, lw):
    seg = []
    for i, (v, n) in enumerate(mm + [(None, 0)]):
        if v is None:
            if seg: ax.plot(*zip(*seg), color=col, lw=lw, zorder=5, marker='o', ms=4.5, mec=SURF, mew=0.7); seg = []
        else: seg.append((2019 + (i + 0.5) / 12, pct(v)))
line(m1, ORANGE, 2.6); line(m2, AQUA, 2.6)
ax.axhline(0, color=INK2, lw=1.0, zorder=3); ax.axvline(2019 + (5 + 21.5 / 30) / 12, color=INK2, lw=1.2, ls=(0, (3, 2)), zorder=3)
ax.text(2019.45, 27.5, 'Raikoke,\n22 June 2019', fontsize=11.5, color=INK2, ha='right', va='top')
ax.plot([2019.56, 2019.68], [-7.5, -7.5], color=ORANGE, lw=3.2, solid_capstyle='round'); ax.text(2019.74, -7.5, 'first make: Spain, Slovenia', fontsize=12.5, color=INK, va='center')
ax.plot([2019.56, 2019.68], [-11.5, -11.5], color=AQUA, lw=3.2, solid_capstyle='round'); ax.text(2019.74, -11.5, 'second make: Korea', fontsize=12.5, color=INK, va='center')
ax.set_xlim(2018.96, 2021.04); ax.set_ylim(-15, 29); ax.set_xticks([2019, 2019.5, 2020, 2020.5]); ax.set_xticklabels(['Jan\n2019', 'Jul', 'Jan\n2020', 'Jul'], fontsize=13)
ax.set_yticks([0, 10, 20]); ax.set_yticklabels(['0', '10', '20'], fontsize=15); ax.grid(True, axis='y', color=GRID, lw=1); ax.set_axisbelow(True); ax.tick_params(colors=INK2, length=0); ax.tick_params(axis='x', length=5, width=1.0)
for sp in ('top', 'right', 'left'): ax.spines[sp].set_visible(False)
ax.spines['bottom'].set_color(INK2)
fig.text(0.015, 0.978, 'twilight overhead, twelve minutes after sunset:', fontsize=13.5, color=INK2, va='top'); fig.text(0.015, 0.912, 'per cent darker than the same month of 2018', fontsize=13.5, color=INK2, va='top')
fig.savefig(B + 'img/tonga-raikoke.png', dpi=140, facecolor=SURF); plt.close(fig)
print('picture: img/tonga-raikoke.png; the reading at 3 degrees less the same month of 2018, month by month from January 2019 to December 2020')
for name, mm in (('the first make, the middle of the northern places', m1), ('the second make, the middle of five Korean stations', m2)):
    print(f'   {name}: magnitudes ' + ' '.join(f'{v:+.2f}' if v is not None else '  .  ' for v, n in mm)); print('      per cent darker ' + ' '.join(f'{pct(v):+4.0f}' if v is not None else '   .' for v, n in mm) + '   | places ' + ' '.join(str(n) for v, n in mm))
