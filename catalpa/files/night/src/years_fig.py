# The picture of the fifteenth sheet: the fading of the twilight from 3 to 7 degrees month by month, 2018 to 2026,
# each month less the same month of 2021, as per cent brighter with the Sun 7 degrees down for the same twilight at
# 3 degrees: each southern place (pale), the middle of the southern places and of the northern places (three or
# more). From the reductions of the ninth and fifteenth sheets (cache2/depth.pkl, cache2/years.pkl), by the functions
# of src/years_depth.py's rule (one unit per place: the chip of most of its months in 2021).
import pickle, importlib.util
import numpy as np
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('depth', B + 'src/depth.py'); DP = importlib.util.module_from_spec(spec); spec.loader.exec_module(DP)
R = dict(pickle.load(open(B + 'cache2/depth.pkl', 'rb'))); R.update(pickle.load(open(B + 'cache2/years.pkl', 'rb')))
def fading(st, dp=7.0):
    chips = {}
    for (s, y, m), r in R.items():
        if s == st and y == 2021 and r is not None and DP.monthfig(r, dp) is not None and DP.monthfig(r, 3.0) is not None: chips[(r.get('mac') or '')[-8:]] = chips.get((r.get('mac') or '')[-8:], 0) + 1
    if not chips: return {}
    ch = max(chips, key=chips.get); F = {}
    for (s, y, m), r in R.items():
        if s != st or r is None or (r.get('mac') or '')[-8:] != ch: continue
        a, b = DP.monthfig(r, dp), DP.monthfig(r, 3.0)
        if a is not None and b is not None: F[(y, m)] = a - b
    return F
pct = lambda mag: 100 * (10 ** (-0.4 * mag) - 1); KS = [(y, m) for y in range(2018, 2027) for m in range(1, 13)]; t = lambda k: k[0] + (k[1] - 0.5) / 12
FS = {st: fading(st) for st in DP.SOUTH}; FN = {st: fading(st) for st in DP.NORTH}
def d(F, k): return (F[k] - F[(2021, k[1])]) if k in F and (2021, k[1]) in F else None
def middle(FF, k):
    v = [d(F, k) for F in FF.values()]; v = [x for x in v if x is not None]; return (float(np.median(v)), len(v)) if len(v) >= 3 else (None, len(v))
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'; BLUE = '#2a78d6'; ORANGE = '#eb6834'
fig = plt.figure(figsize=(5.0, 4.0), facecolor=SURF); ax = fig.add_axes([0.135, 0.13, 0.845, 0.67]); ax.set_facecolor(SURF)
def segs(ks, vals):          # break a line where a month is missing
    out, cur = [], []
    for k, v in zip(ks, vals):
        if v is None:
            if cur: out.append(cur); cur = []
        else: cur.append((t(k), v))
    if cur: out.append(cur)
    return out
for st, F in FS.items():
    for s in segs(KS, [None if d(F, k) is None else pct(d(F, k)) for k in KS]): ax.plot(*zip(*s), color='#c9d8ee', lw=0.9, zorder=2)
ms = [middle(FS, k)[0] for k in KS]; mn = [middle(FN, k)[0] for k in KS]
for s in segs(KS, [None if v is None else pct(v) for v in mn]): ax.plot(*zip(*s), color=ORANGE, lw=2.0, zorder=4)
for s in segs(KS, [None if v is None else pct(v) for v in ms]): ax.plot(*zip(*s), color=BLUE, lw=2.6, zorder=5)
ax.axhline(0, color=INK2, lw=1.0, zorder=3); ax.axvline(2022 + 14.5 / 365, color=INK2, lw=1.2, ls=(0, (3, 2)), zorder=3)
ax.text(2021.9, -17, 'eruption,\n15 Jan 2022', fontsize=11.5, color=INK2, ha='right', va='top')
ax.plot([2018.3, 2018.9], [112, 112], color=BLUE, lw=3.2, solid_capstyle='round'); ax.text(2019.05, 112, 'south', fontsize=14.5, color=INK, va='center')
ax.plot([2018.3, 2018.9], [90, 90], color=ORANGE, lw=2.6, solid_capstyle='round'); ax.text(2019.05, 90, 'north', fontsize=14.5, color=INK, va='center')
ax.set_xlim(2017.9, 2026.95); ax.set_ylim(-45, 135); ax.set_xticks([2018, 2020, 2022, 2024, 2026]); ax.set_xticklabels(['2018', '2020', '2022', '2024', '2026'], fontsize=14.5)      # a label stands at the start of its year
for x in range(2018, 2028): ax.axvline(x, color=GRID, lw=0.8, zorder=1)
ax.set_yticks([0, 50, 100]); ax.set_yticklabels(['0', '50', '100'], fontsize=15); ax.grid(True, axis='y', color=GRID, lw=1); ax.set_axisbelow(True); ax.tick_params(colors=INK2, length=0); ax.tick_params(axis='x', length=5, width=1.0)
for sp in ('top', 'right', 'left'): ax.spines[sp].set_visible(False)
ax.spines['bottom'].set_color(INK2)
fig.text(0.015, 0.978, 'twilight overhead, half an hour after sunset:', fontsize=13.5, color=INK2, va='top'); fig.text(0.015, 0.912, 'per cent brighter than the same month of 2021', fontsize=13.5, color=INK2, va='top')
fig.savefig(B + 'img/tonga-ten-years.png', dpi=140, facecolor=SURF); plt.close(fig)
print('picture: img/tonga-ten-years.png; the middles month by month, per cent brighter than the same month of 2021 (. fewer than three places)')
for name, mm in (('south', ms), ('north', mn)):
    for y in range(2018, 2027):
        row = [mm[KS.index((y, m))] for m in range(1, 13)]
        if any(v is not None for v in row): print(f'   {name} {y}: ' + ' '.join(f'{pct(v):+4.0f}' if v is not None else '   .' for v in row))
