# The picture of the fourteenth sheet: the four southern stations of the other make, month by month through 2022 and
# 2023, from north to south. Each bar: how much brighter the twilight was with the Sun 7 degrees down, counted from
# the twilight at 3 degrees of the same month, against the same month of 2021 and 2024 (the measure of
# src/sqm_steep.py, recomputed here from the same reductions).
import pickle, importlib.util
import numpy as np
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('sqm_depth', B + 'src/sqm_depth.py'); SD = importlib.util.module_from_spec(spec); spec.loader.exec_module(SD)
R = pickle.load(open(B + 'cache2/sqm_months.pkl', 'rb')); ST = SD.ST; pct = lambda mag: 100 * (10 ** (-0.4 * mag) - 1)
def steep(c, y, m):
    a, b = SD.fig(R[(c, y, m)], 7.0), SD.fig(R[(c, y, m)], 3.0); return (a - b) if a is not None and b is not None else None
def anom(c, y, m):
    v = steep(c, y, m); base = [b for b in (steep(c, yy, m) for yy in (2021, 2024)) if b is not None]
    return (v - float(np.mean(base))) if v is not None and base else None
KS = [(y, m) for y in (2022, 2023) for m in range(1, 13)]
LAB = {'PAOF': 'Brazil, 22° south', 'Nrnr': 'Namibia, 25° south', 'AHO': 'Argentina, 35° south', 'Oam': 'New Zealand, 45° south'}
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'; AQUA = '#1baf7a'
fig = plt.figure(figsize=(5.0, 6.3), facecolor=SURF); n = len(ST); top, bot, gap = 0.865, 0.075, 0.035; h = (top - bot - gap * (n - 1)) / n
print('picture: img/tonga-other-make-months.png; per cent brighter at 7 degrees counted from 3, January 2022 to December 2023 (. no figure)')
for i, c in enumerate(ST):
    ax = fig.add_axes([0.135, top - (i + 1) * h - i * gap, 0.845, h]); ax.set_facecolor(SURF)
    v = [anom(c, y, m) for y, m in KS]; xs = [k for k in range(24) if v[k] is not None]
    ax.bar(xs, [pct(v[k]) for k in xs], width=0.62, color=AQUA, zorder=3)
    for k in range(24):
        if v[k] is None: ax.axvspan(k - 0.5, k + 0.5, ymin=0.30, ymax=0.42, color='#e9e8e4', zorder=0)      # a grey block on the zero line: no figure that month
    ax.axhline(0, color=INK2, lw=1.0, zorder=4); ax.axvline(11.5, color=GRID, lw=1.2, zorder=1)
    ax.set_xlim(-0.8, 23.8); ax.set_ylim(-27, 48); ax.set_yticks([0, 25]); ax.set_yticklabels(['0', '25'], fontsize=13)
    ax.grid(True, axis='y', color=GRID, lw=1); ax.set_axisbelow(True); ax.tick_params(colors=INK2, length=0)
    for sp in ('top', 'right', 'left', 'bottom'): ax.spines[sp].set_visible(False)
    ax.text(23.6, 45, LAB[c], fontsize=13.5, color=INK, va='top', ha='right')
    if i == n - 1: ax.set_xticks([0, 6, 12, 18]); ax.set_xticklabels(['Jan\n2022', 'Jul', 'Jan\n2023', 'Jul'], fontsize=13)
    else: ax.set_xticks([])
    print(f"   {LAB[c]:<24} " + ' '.join(f'{pct(x):+4.0f}' if x is not None else '   .' for x in v))
fig.text(0.015, 0.985, 'the second make, month by month:', fontsize=14, color=INK2, va='top'); fig.text(0.015, 0.945, 'per cent brighter with the Sun 7° down', fontsize=14, color=INK2, va='top')
fig.savefig(B + 'img/tonga-other-make-months.png', dpi=140, facecolor=SURF); plt.close(fig)
