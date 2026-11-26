# Figure 1: the tropics against San Diego, month by month, in three El Ninos.
# Run: ~/ipd/.venv/bin/python -I src/plot_pairs.py   (writes pairs.png)
import sys, io, contextlib, importlib.util
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
spec = importlib.util.spec_from_file_location('pairs', '/home/agent1/trace/src/pairs.py')
P = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(P)
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'; BLUE, ORANGE = '#2a78d6', '#eb6834'
fig, axes = plt.subplots(1, 3, figsize=(11, 4.4), facecolor=SURF, sharey=True)
fig.subplots_adjust(left=0.065, right=0.985, top=0.80, bottom=0.19, wspace=0.07)
lab = list("AMJJASONDJFMAMJ")
for ax, y0 in zip(axes, (1997, 2015, 2026)):
    months = [(y0, m) for m in range(4, 13)] + [(y0 + 1, m) for m in range(1, 7)]
    tr = [P.trop(y, m) for y, m in months]; sd = [P.g("San Diego", y, m) for y, m in months]
    for v, col, name in ((tr, ORANGE, 'Ecuador and the\nGalápagos'), (sd, BLUE, 'San Diego')):
        x = [i for i, a in enumerate(v) if a is not None]; yv = [a for a in v if a is not None]
        ax.plot(x, yv, color=col, lw=2, zorder=3, solid_capstyle='round'); ax.scatter(x, yv, s=26, color=col, edgecolor=SURF, linewidth=1, zorder=4)
    ax.axhline(0, color=INK2, lw=1, zorder=2); ax.set_facecolor(SURF); ax.grid(True, axis='y', color=GRID, lw=1); ax.set_axisbelow(True)
    for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color(GRID); ax.tick_params(colors=INK2, length=0, labelsize=9)
    ax.set_xticks(range(15)); ax.set_xticklabels(lab); ax.set_xlim(-0.6, 14.6); ax.set_ylim(-6, 42)
    ax.set_title(f'{y0}' + (f'–{str(y0 + 1)[2:]}' if y0 != 2026 else ''), loc='left', fontsize=11, color=INK, pad=6)
    ax.axvline(8.5, color=GRID, lw=1, zorder=1); ax.text(8.6, -5.2, f'{y0 + 1}', fontsize=8, color=INK2, va='bottom')
    ax.axvspan(4.5, 6.5, color='#f0efec', zorder=0)   # September and October
axes[0].set_ylabel('sea level above the usual for the month, cm', color=INK2, fontsize=9.5)
a = axes[0]; a.text(9.2, 39.5, 'Ecuador and\nthe Galápagos', fontsize=9, color=INK, va='center'); a.text(10.3, 3.0, 'San Diego', fontsize=9, color=INK, va='center')
a = axes[2]
a.text(4.6, 37.5, 'Ecuador and the\nGalápagos,\nSeptember', fontsize=9, color=INK, ha='right', va='center')
a.text(6.5, 36.5, 'San Diego,\nOctober', fontsize=9, color=INK, ha='left', va='center')
a.text(11.2, 16, 'not yet\nin the files', fontsize=9, color=INK2, ha='center', va='center')
fig.text(0.065, 0.93, 'Off Ecuador, September 2026 stood where 1997 stood in November. San Diego stood twice as high as it ever did in 1997.', fontsize=11.5, color=INK, va='bottom')
fig.text(0.065, 0.885, 'Monthly sea level at tide gauges, measured from each gauge\'s own trend and seasons. The shaded months are September and October.', fontsize=9, color=INK2, va='bottom')
fig.text(0.065, 0.025, 'Ecuador and the Galápagos: mean of the gauges at La Libertad and Santa Cruz (University of Hawaii Sea Level Center; the files end on 30 September 2026).\nSan Diego: the same files, and NOAA for October 2026.', fontsize=8, color=INK2, va='bottom', linespacing=1.4)
fig.savefig('/home/agent1/trace/pairs.png', dpi=150, facecolor=SURF)
