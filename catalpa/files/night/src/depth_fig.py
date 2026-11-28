# The picture of the ninth sheet: the brightening of June to August 2022 against the depth of the Sun, each southern
# place and their middle; with the model's central case if a run is given (model/haze_central.pkl).
# usage: depth_fig.py [model.pkl]
import sys, pickle, io, contextlib, importlib.util
import numpy as np
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('depth', B + 'src/depth.py'); DP = importlib.util.module_from_spec(spec); spec.loader.exec_module(DP)
with contextlib.redirect_stdout(io.StringIO()): depths, PS, mid, nm = DP.tables(B + 'cache2/depth.pkl')
pct = lambda mag: 100 * (10 ** (-0.4 * mag) - 1)
D = [d for d in depths if 3.0 <= d <= 11.0]
model = None
if len(sys.argv) > 1:
    # the model's central case, summed over the colours with the meter's response as its makers print it
    # (the checker's blind reading of their figure: check/fig3_blind.txt)
    spec = importlib.util.spec_from_file_location('run_haze', B + 'model/run_haze.py'); RH = importlib.util.module_from_spec(spec); spec.loader.exec_module(RH)
    X = pickle.load(open(sys.argv[1], 'rb')); R = X['R']; RESP = {425: 0.575, 475: 0.670, 525: 0.768, 575: 0.847, 625: 0.924, 675: 0.985, 725: 0.768}
    def tot(d, i): return sum(RH.RC.SUN[l] * RESP[l] * (R[(l, d)]['L1'][i] + R[(l, d)]['L2'][i] + R[(l, d)]['L3'][:, i].mean()) for l in RH.LAMS)
    model = {d: [None, -2.5 * np.log10(tot(d, 1) / tot(d, 3))] for d in RH.DEPTHS}
    others = []      # the same with the layer lower and higher, if those runs are given: thin lines
    for fn in sys.argv[2:]:
        R = pickle.load(open(fn, 'rb'))['R']; others.append({d: -2.5 * np.log10(tot(d, 1) / tot(d, 3)) for d in RH.DEPTHS})
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'; BLUE = '#2a78d6'; ORANGE = '#eb6834'
fig = plt.figure(figsize=(5.0, 4.0), facecolor=SURF); ax = fig.add_axes([0.135, 0.17, 0.845, 0.63]); ax.set_facecolor(SURF)
for st in DP.SOUTH:
    xs = [d for d in D if PS[(st, d)] is not None]; ax.plot(xs, [pct(PS[(st, d)]) for d in xs], color='#c9d8ee', lw=1.0, zorder=2)
ax.plot(D, [pct(mid[d][0]) for d in D], color=BLUE, lw=2.8, zorder=5, marker='o', ms=5.5, mec=SURF, mew=0.8)
nmid = [float(np.median(nm[d])) if nm[d] else np.nan for d in D]; ax.plot(D, [pct(v) for v in nmid], color=ORANGE, lw=2.2, zorder=4)
if model:      # drawn to 9 degrees; beyond that the model's higher orders are not to be trusted (check-twilight-6.md)
    xm = [d for d in D if int(d) in model and d <= 9.0]; ax.plot(xm, [pct(model[int(d)][1]) for d in xm], color=INK, lw=2.0, ls=(0, (4, 3)), zorder=6)
    for o in others: ax.plot(xm, [pct(o[int(d)]) for d in xm], color=INK, lw=0.9, ls=(0, (4, 3)), zorder=6)
ax.axhline(0, color=INK2, lw=1.0, zorder=3)
ax.plot([3.25, 3.75], [150, 150], color=BLUE, lw=3.2, solid_capstyle='round'); ax.text(3.95, 150, 'south', fontsize=14.5, color=INK, va='center')
ax.plot([3.25, 3.75], [128, 128], color=ORANGE, lw=2.6, solid_capstyle='round'); ax.text(3.95, 128, 'north', fontsize=14.5, color=INK, va='center')
if model: ax.plot([3.25, 3.75], [106, 106], color=INK, lw=2.0, ls=(0, (4, 3))); ax.text(3.95, 106, 'model', fontsize=14.5, color=INK, va='center')
if model and others: ax.text(9.15, pct(max(o[9] for o in others)) - 2, 'haze\nlower', fontsize=11.5, color=INK2, va='center', ha='left'); ax.text(9.15, min(170, pct(min(o[9] for o in others))), 'haze\nhigher', fontsize=11.5, color=INK2, va='center', ha='left')
ax.set_xlim(2.7, 11.3); ax.set_ylim(-25, 175); ax.set_xticks([3, 5, 7, 9, 11]); ax.set_xticklabels(['3°', '5°', '7°', '9°', '11°'], fontsize=15); ax.set_yticks([0, 50, 100, 150]); ax.set_yticklabels(['0', '50', '100', '150'], fontsize=15)
ax.grid(True, axis='y', color=GRID, lw=1); ax.set_axisbelow(True); ax.tick_params(colors=INK2, length=0)
for sp in ('top', 'right', 'left'): ax.spines[sp].set_visible(False)
ax.spines['bottom'].set_color(INK2)
fig.text(0.015, 0.978, 'twilight overhead, June to August 2022:', fontsize=14, color=INK2, va='top'); fig.text(0.015, 0.912, 'per cent brighter, by the Sun\'s depth', fontsize=14, color=INK2, va='top')
fig.text(0.56, 0.035, 'Sun below the horizon', fontsize=13, color=INK2, ha='center')
fig.savefig(B + 'img/tonga-depth.png', dpi=140, facecolor=SURF); plt.close(fig)
print('picture: img/tonga-depth.png; the middle of the southern places, per cent brighter: ' + ', '.join(f'{d:g}°: {pct(mid[d][0]):+.0f}' for d in D) + '; the northern middle: ' + ', '.join(f'{d:g}°: {pct(v):+.0f}' for d, v in zip(D, nmid)) + (('; the model: ' + ', '.join(f'{d:g}°: {pct(model[int(d)][1]):+.0f}' for d in D) + ''.join('; the model with the layer moved: ' + ', '.join(f'{d:g}°: {pct(o[int(d)]):+.0f}' for d in D if d <= 9) for o in others)) if model else '') + f'; the highest single place {max(pct(PS[(st, d)]) for st in DP.SOUTH for d in D if PS[(st, d)] is not None):.0f}')
