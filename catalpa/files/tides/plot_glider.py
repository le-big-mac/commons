# Figure: the two warm Octobers on the gliders' line off Dana Point (CalCOFI line 90).  Left: dynamic height of the surface relative to 500 dbar, anomaly from the 2017-2025 mean of the
# same 25-km bin, with the San Diego gauge on the same footing at zero distance.  Right: the depth-averaged current along the coast toward the pole, same anomaly.
import numpy as np, os, csv, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); R = np.load(f'{HERE}/glider/profiles_oct.npy'); R = R[np.isfinite(R[:, 5])]; yr, day, lat, lon, km, D, z26, T100, T200, u, v, line, dep, D200, pmax = R.T     # profiles reaching 490 dbar only
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
fig, (ax, bx) = plt.subplots(1, 2, figsize=(11, 4.9), facecolor=SURF)
for y, col in ((2026, C26), (2015, C15)):
    p = prof(y, D); ax.plot(p[:, 0], p[:, 1], color=col, lw=2, zorder=3); ax.scatter(p[:, 0], p[:, 1], s=26, color=col, edgecolor=SURF, linewidth=1, zorder=4)
    ax.scatter([0], [G[y]], s=80, marker='D', color=col, edgecolor=SURF, linewidth=1.5, zorder=5, clip_on=False)
    ax.annotate(f'+{G[y]:.0f}', (0, G[y]), xytext=(9, 7 if y == 2015 else 0), textcoords='offset points', va='center', fontsize=9, color=INK)
    ax.annotate(f'gliders, October {y}', (p[-1, 0], p[-1, 1]), xytext=(6, 0 if y == 2015 else -2), textcoords='offset points', va='center', fontsize=9, color=INK)
    q = prof(y, along); bx.plot(q[:, 0], q[:, 1], color=col, lw=2, zorder=3); bx.scatter(q[:, 0], q[:, 1], s=26, color=col, edgecolor=SURF, linewidth=1, zorder=4)
    bx.annotate(f'October {y}', (q[-1, 0], q[-1, 1]), xytext=(6, 0), textcoords='offset points', va='center', fontsize=9, color=INK)
for a, ttl, yl in ((ax, 'Height of the sea surface held up by the top 500 m, above the 2017–2025\naverage for the same place (cm). Diamonds: the San Diego tide gauge', (-4, 38)), (bx, 'Current along the coast toward the pole, averaged over\nthe top 500 m, above the 2017–2025 average (m/s)', (-0.08, 0.16))):
    a.axhline(0, color=INK2, lw=1, zorder=2); a.set_facecolor(SURF); a.grid(True, axis='y', color=GRID, lw=1); a.set_axisbelow(True); a.set_ylim(*yl); a.set_xlim(-8, 330)
    for s in ('top', 'right', 'left'): a.spines[s].set_visible(False)
    a.spines['bottom'].set_color(GRID); a.tick_params(colors=INK2, length=0, labelsize=9); a.set_xlabel('distance from the coast, km', color=INK2, fontsize=9.5); a.set_title(ttl, loc='left', fontsize=10.5, color=INK, pad=8)
fig.text(0.012, 0.012, "Spray gliders of the California Underwater Glider Network on the line off Dana Point (CalCOFI line 90), October profiles to 500 m, from the IOOS Glider DAC; NOAA gauge 9410170.", color=INK2, fontsize=8)
fig.tight_layout(rect=(0, 0.04, 1, 1), w_pad=3); fig.savefig('gliders.png', dpi=150, facecolor=SURF)
for y in (2015, 2026): print(y, 'gauge', round(G[y], 1), 'height', np.round(prof(y, D)[:, 1], 1), 'flow', np.round(prof(y, along)[:, 1], 3))
