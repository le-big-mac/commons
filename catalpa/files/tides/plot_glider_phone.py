# The glider figure redrawn for a phone (27 Nov 2026) as two pictures 700 px wide with large lettering:
# the height held up by the warm water (coast-height.png) and the current along the coast (coast-current.png).
# Same sums as plot_glider.py. Run: ~/ipd/.venv/bin/python -I ~/tides/plot_glider_phone.py > ~/tides/glider_phone.out
import numpy as np, csv, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
HERE = '/home/agent1/tides'; R = np.load(f'{HERE}/glider/profiles_oct.npy'); R = R[np.isfinite(R[:, 5])]; yr, day, lat, lon, km, D, z26, T100, T200, u, v, line, dep, D200, pmax = R.T
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'; C26, C15 = '#2a78d6', '#1baf7a'
box = (lat >= 32) & (lat <= 34.5) & (line == 90); along = (v - u) / np.sqrt(2); kb = np.floor(km / 25).astype(int)
def clim(k, x):
    mk = box & (kb == k) & (yr >= 2017) & (yr <= 2025) & np.isfinite(x); return x[mk].mean() if mk.sum() >= 30 and len(set(yr[mk])) >= 4 else np.nan
def prof(y, x):
    out = []
    for k in range(0, 12):
        mk = box & (kb == k) & (yr == y) & np.isfinite(x); c = clim(k, x)
        if mk.sum() >= 5 and np.isfinite(c): out.append((25 * k + 12.5, x[mk].mean() - c, x[mk].std() / np.sqrt(mk.sum())))
    return np.array(out)
M = {}
for r in csv.reader(open(f'{HERE}/data/9410170_monthly_mean.csv')):
    if r and r[0].strip().isdigit() and int(r[1]) == 10 and r[5].strip() not in ('', 'NaN'): M[int(r[0])] = 100 * float(r[5])
gb = np.mean([M[y] for y in range(2017, 2026)]); G = {y: M[y] - gb for y in (2015, 2026)}
def frame(fig, a, ylim, yticks, xmax, note, xmin=-10):
    a.axhline(0, color=INK2, lw=1, zorder=2); a.set_facecolor(SURF); a.grid(True, axis='y', color=GRID, lw=1); a.set_axisbelow(True); a.set_ylim(*ylim); a.set_yticks(yticks); a.set_xlim(xmin, xmax)
    for s in ('top', 'right', 'left'): a.spines[s].set_visible(False)
    a.spines['bottom'].set_color(GRID); a.tick_params(colors=INK2, length=0, labelsize=11.5); a.set_xlabel('distance from the coast, km', color=INK2, fontsize=11.5)
    fig.text(0.015, 0.975, note, fontsize=11.5, color=INK2, va='top')
fig = plt.figure(figsize=(5.0, 3.9), facecolor=SURF); ax = fig.add_axes([0.105, 0.15, 0.855, 0.72])
for y, col in ((2026, C26), (2015, C15)):
    p = prof(y, D); ax.plot(p[:, 0], p[:, 1], color=col, lw=2.2, zorder=3); ax.scatter(p[:, 0], p[:, 1], s=28, color=col, edgecolor=SURF, linewidth=1, zorder=4)
    ax.scatter([0], [G[y]], s=95, marker='D', color=col, edgecolor=SURF, linewidth=1.5, zorder=5, clip_on=False)
    ax.text(-9, G[y], f'gauge,\n{y}', ha='right', va='center', fontsize=11, color=INK, linespacing=1.1)
    if y == 2026: ax.annotate(f'gliders, {y}', (p[-1, 0], p[-1, 1]), xytext=(9, 0), textcoords='offset points', va='center', fontsize=11, color=INK)
    else: ax.text(p[-1, 0] + 4, p[-1, 1] + 3.0, f'gliders, {y}', ha='right', va='center', fontsize=11, color=INK)
    print(f"{y}: gauge {G[y]:+.1f}; height by distance {np.round(p[:, 1], 1)} at {p[:, 0]}")
frame(fig, ax, (-4, 38), [0, 10, 20, 30], 345, 'cm above the Octobers of 2017 to 2025', xmin=-62); ax.set_xticks([0, 100, 200, 300])
fig.savefig('/home/agent1/site/img/coast-height.png', dpi=140, facecolor=SURF)
fig = plt.figure(figsize=(5.0, 3.5), facecolor=SURF); bx = fig.add_axes([0.135, 0.165, 0.825, 0.69])
for y, col in ((2026, C26), (2015, C15)):
    q = prof(y, along); q = q[q[:, 0] < 200]
    bx.plot(q[:, 0], q[:, 1], color=col, lw=2.2, zorder=3); bx.scatter(q[:, 0], q[:, 1], s=28, color=col, edgecolor=SURF, linewidth=1, zorder=4)
    bx.text(38, 0.128 if y == 2026 else -0.022, f'October {y}', va='center', ha='left', fontsize=11, color=INK)
    print(f"{y}: current by distance {np.round(q[:, 1], 3)} at {q[:, 0]}")
frame(fig, bx, (-0.08, 0.16), [-0.05, 0, 0.05, 0.10, 0.15], 215, 'metres a second northward, above 2017 to 2025')
fig.savefig('/home/agent1/site/img/coast-current.png', dpi=140, facecolor=SURF)
