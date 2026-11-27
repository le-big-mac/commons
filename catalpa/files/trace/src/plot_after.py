# Figure for rise.html: San Diego day by day, 1 September to 15 November, in 2026, 1997 and 2015, with air pressure
# allowed for. Reads after_series.csv (src/after_series.py). Drawn 700 px wide with large lettering, so that it can be
# read on a phone without zooming. Run: ~/ipd/.venv/bin/python -I src/plot_after.py   (writes ~/site/img/rise-after.png)
import csv, datetime as dt
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'; COL = {2026: '#2a78d6', 1997: '#eb6834', 2015: '#1baf7a'}
rows = list(csv.DictReader(open('/home/agent1/trace/after_series.csv')))
x = [(dt.date(2026, int(r['day'][:2]), int(r['day'][3:])) - dt.date(2026, 9, 1)).days for r in rows]
fig = plt.figure(figsize=(5.0, 4.5), facecolor=SURF); ax = fig.add_axes([0.105, 0.105, 0.775, 0.745]); ax.set_facecolor(SURF)
for y in (1997, 2015, 2026):
    v = [(xi, float(r[f'{y} pressure allowed for'])) for xi, r in zip(x, rows) if r[f'{y} pressure allowed for']]
    ax.plot([a for a, b in v], [b for a, b in v], color=COL[y], lw=2.6 if y == 2026 else 1.8, zorder=4 if y == 2026 else 3, solid_capstyle='round', solid_joinstyle='round')
    last = sum(b for a, b in v[-5:]) / 5
    ax.text(76.5, {2026: last, 1997: last + 1.0, 2015: last - 1.5}[y], str(y), fontsize=13, color=INK, va='center', ha='left', fontweight='bold' if y == 2026 else 'normal')
ax.axvline(27, color=INK2, lw=1, ls=(0, (3, 3)), zorder=2); ax.text(26.2, 44.5, 'the quick rise,\n28 September', fontsize=10.5, color=INK2, ha='right', va='top', linespacing=1.15)
ax.set_xlim(0, 75.5); ax.set_ylim(0, 45); ax.set_xticks([0, 30, 61]); ax.set_xticklabels(['1 Sep', '1 Oct', '1 Nov'], fontsize=12); ax.set_yticks([0, 10, 20, 30, 40]); ax.set_yticklabels(['0', '10', '20', '30', '40'], fontsize=12)
ax.grid(True, axis='y', color=GRID, lw=1); ax.set_axisbelow(True); ax.tick_params(colors=INK2, length=0); ax.tick_params(axis='x', pad=9)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color(INK2)
fig.text(0.02, 0.965, 'cm above the usual for the day', fontsize=11.5, color=INK2, va='top')
# legend: a swatch and a name for each year, in ink
lx = 0.105
for y in (2026, 1997, 2015):
    fig.lines.append(matplotlib.lines.Line2D([lx, lx + 0.05], [0.895, 0.895], transform=fig.transFigure, color=COL[y], lw=2.6 if y == 2026 else 1.8, solid_capstyle='round'))
    fig.text(lx + 0.062, 0.895, str(y), fontsize=11.5, color=INK, va='center'); lx += 0.20
fig.savefig('/home/agent1/site/img/rise-after.png', dpi=140, facecolor=SURF)
print('written', fig.get_size_inches() * 140)
