# Figure 3: the rise of 28 September to 1 October 2026 timed at the US gauges (numbers from wave.py).
# Run: ~/ipd/.venv/bin/python -I src/plot_wave.py   (writes wave.png)
import sys, io, contextlib, importlib.util, datetime as dt
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
spec = importlib.util.spec_from_file_location('wave', '/home/agent1/trace/src/wave.py')
W = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(W)
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'; BLUE = '#2a78d6'
rows = [r for r in W.rows if r[4] is not None]; t0 = W.rows[0][4]
x = np.array([r[1] for r in rows]); t = np.array([(r[4] - t0 + 16) / 24 for r in rows])   # days after 28 September 00:00 UTC (San Diego arrived at 16:00); rise = [r[3] - r[2] for r in rows]
s, c = np.polyfit(x, t, 1)
fig = plt.figure(figsize=(8.6, 5.0), facecolor=SURF); ax = fig.add_axes([0.10, 0.13, 0.86, 0.68])
xx = np.array([-30, 1250])
ax.set_xticks([0, 200, 400, 600, 800, 1000, 1200])
ax.plot(xx, c + s * xx, color=BLUE, lw=2, zorder=3)
ax.scatter(x, t, s=46, color=BLUE, edgecolor=SURF, linewidth=1.5, zorder=4)
lab = {'San Diego': (9, -12), 'La Jolla': None, 'Los Angeles': (-9, 10), 'Santa Barbara': (9, -10), 'Port San Luis': (-9, 10), 'Monterey': (-9, 10), 'San Francisco': (9, -13),
       'Point Reyes': (10, -1), 'Arena Cove': (-9, 10), 'North Spit': (0, -15)}
for r, xi, ti in zip(rows, x, t):
    off = lab.get(r[0])
    if off is None: continue
    name = 'Humboldt Bay' if r[0] == 'North Spit' else r[0]
    ax.annotate(f"{name}, +{r[3] - r[2]:.0f} cm", (xi, ti), xytext=off, textcoords='offset points', fontsize=8.5, color=INK, ha='right' if off[0] < 0 else ('center' if off[0] == 0 else 'left'), va='center')
ax.annotate(f'fitted: {1 / s:.0f} km a day', (560, c + s * 560), xytext=(10, -20), textcoords='offset points', fontsize=9, color=INK)
xh = rows[-1][1]; th = 16 / 24 + xh / 241.0
ax.scatter([xh], [th], s=46, facecolor=SURF, edgecolor=INK2, linewidth=1.5, zorder=4)
ax.annotate('at 241 km a day, the speed forecast in the press,\nit would have reached Humboldt Bay here', (xh, th), xytext=(-10, 0), textcoords='offset points', fontsize=9, color=INK2, ha='right', va='center')
ax.axvline(368, color=GRID, lw=1, zorder=1); ax.text(374, 4.55, 'Point Conception', fontsize=8.5, color=INK2, va='center')
ax.set_facecolor(SURF); ax.grid(True, axis='y', color=GRID, lw=1); ax.set_axisbelow(True)
for sp in ('top', 'right', 'left'): ax.spines[sp].set_visible(False)
ax.spines['bottom'].set_color(GRID); ax.tick_params(colors=INK2, length=0, labelsize=9)
ax.set_xlim(-140, 1300); ax.set_ylim(0.2, 5.9)
ax.set_yticks(range(1, 6)); ax.set_yticklabels([(dt.datetime(2026, 9, 28) + dt.timedelta(days=k)).strftime('%-d %b') for k in range(1, 6)])
ax.set_xlabel('distance along the coast from San Diego, km', color=INK2, fontsize=9.5)
fig.text(0.10, 0.92, 'The rise reached Humboldt Bay two and a half days after San Diego', fontsize=11.5, color=INK, va='bottom')
fig.text(0.10, 0.865, 'When the sea, with the tide taken out and air pressure left in, passed halfway between its level of 20–26 September\nand of 1–5 October, and how much it rose. Gauges north of Humboldt Bay rose less than 5 cm and are left out.', fontsize=9, color=INK2, va='top', linespacing=1.4)
fig.text(0.10, 0.02, 'NOAA tide gauges, hourly heights. The marks on the left are midnights, UTC.', fontsize=8, color=INK2, va='bottom')
fig.savefig('/home/agent1/trace/wave.png', dpi=150, facecolor=SURF)
