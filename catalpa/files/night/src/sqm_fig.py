# The picture of the other make of meter: June to August 2022 by the depth of the Sun, the four southern stations of
# the other make (the SQM) and their middle, the middle of the eleven TESS-W places, and what the model said the
# other make would show. usage: sqm_fig.py fading|direct
#   fading: every line is counted from the twilight at 3 degrees (the reading at a depth less the reading at 3
#           degrees of the same month), which takes a meter's ageing out; direct: the eleventh sheet's own measure.
import sys, pickle, io, contextlib, importlib.util
import numpy as np
B = '/home/agent1/night/'; MODE = sys.argv[1] if len(sys.argv) > 1 else 'fading'
def mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
DP = mod('depth', B + 'src/depth.py'); SD = mod('sqm_depth', B + 'src/sqm_depth.py'); RH = mod('run_haze', B + 'model/run_haze.py')
with contextlib.redirect_stdout(io.StringIO()): depths, PS, mid, nm = DP.tables(B + 'cache2/depth.pkl')
D = [3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]; pct = lambda mag: 100 * (10 ** (-0.4 * mag) - 1)
# the first make: each place's figure, less its own figure at 3 degrees when counting from there
tess = {}
for d in D:
    v = [PS[(st, d)] - (PS[(st, 3.0)] if MODE == 'fading' else 0.0) for st in DP.SOUTH if PS[(st, d)] is not None and PS[(st, 3.0)] is not None]; tess[d] = (float(np.median(v)), len(v))
# the other make, from the reductions of the thirteenth sheet (the same files as the eleventh for these months), with the eleventh sheet's rules
R = pickle.load(open(B + 'cache2/sqm_months.pkl', 'rb')); ST = SD.ST; JJA = (6, 7, 8); sqm = {}
for c in ST:
    keys = [(c, y, m) for y in (2021, 2022, 2024) for m in JJA if R[(c, y, m)] is not None]
    night = [v for k in keys for v in R[k]['night']]; nl = float(np.median(night)) if night else None; bright = min(R[k]['bright'] for k in keys)
    for d in D:
        flank = [SD.fig(R[(c, y, m)], d) for y in (2021, 2024) for m in JJA]; flank = [v for v in flank if v is not None]
        okd = bool(flank) and (nl is None or np.median(flank) <= nl - 2.0) and np.median(flank) >= bright + 0.3; an = []
        def val(y, m):
            a = SD.fig(R[(c, y, m)], d); b = SD.fig(R[(c, y, m)], 3.0) if MODE == 'fading' else 0.0
            return (a - b) if a is not None and b is not None else None
        for m in JJA:
            v = val(2022, m); base = [x for x in (val(y, m) for y in (2021, 2024)) if x is not None]
            if okd and v is not None and base: an.append(v - float(np.mean(base)))
        sqm[(c, d)] = float(np.mean(an)) if len(an) >= 2 else None
smid = {d: (float(np.median([sqm[(c, d)] for c in ST if sqm[(c, d)] is not None])), sum(sqm[(c, d)] is not None for c in ST)) for d in D}
# the model's sealed run, summed with each make's response as its makers print it (the checker's blind reading, check/fig3_blind.txt)
X = pickle.load(open(B + 'model/haze_central.pkl', 'rb'))['R']
RESP = dict(sqm={425: 0.472, 475: 0.597, 525: 0.673, 575: 0.479, 625: 0.120, 675: 0.009, 725: 0.006}, tess={425: 0.575, 475: 0.670, 525: 0.768, 575: 0.847, 625: 0.924, 675: 0.985, 725: 0.768})
def model(make):
    tot = lambda d, i: sum(RH.RC.SUN[l] * RESP[make][l] * (X[(l, d)]['L1'][i] + X[(l, d)]['L2'][i] + X[(l, d)]['L3'][:, i].mean()) for l in RH.LAMS)
    m = {d: -2.5 * np.log10(tot(int(d), 1) / tot(int(d), 3)) for d in D}; return {d: m[d] - (m[3.0] if MODE == 'fading' else 0.0) for d in D}
msqm, mtess = model('sqm'), model('tess')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'; BLUE = '#2a78d6'; AQUA = '#1baf7a'; PALE = '#bfe6d5'
fig = plt.figure(figsize=(5.0, 4.0), facecolor=SURF); ax = fig.add_axes([0.135, 0.17, 0.845, 0.63]); ax.set_facecolor(SURF)
for c in ST:
    xs = [d for d in D if sqm[(c, d)] is not None]; ax.plot(xs, [pct(sqm[(c, d)]) for d in xs], color=PALE, lw=1.2, zorder=2)
ax.plot(D, [pct(tess[d][0]) for d in D], color=BLUE, lw=2.8, zorder=5, marker='o', ms=5.5, mec=SURF, mew=0.8)
ax.plot(D, [pct(smid[d][0]) for d in D], color=AQUA, lw=2.8, zorder=5, marker='o', ms=5.5, mec=SURF, mew=0.8)
ax.plot(D, [pct(msqm[d]) for d in D], color=INK, lw=2.0, ls=(0, (4, 3)), zorder=6)
ax.axhline(0, color=INK2, lw=1.0, zorder=3)
ax.plot([3.25, 3.75], [112, 112], color=BLUE, lw=3.2, solid_capstyle='round'); ax.text(3.95, 112, 'first make', fontsize=14.5, color=INK, va='center')
ax.plot([3.25, 3.75], [94, 94], color=AQUA, lw=3.2, solid_capstyle='round'); ax.text(3.95, 94, 'second make', fontsize=14.5, color=INK, va='center')
ax.plot([3.25, 3.75], [76, 76], color=INK, lw=2.0, ls=(0, (4, 3))); ax.text(3.95, 76, 'model, second make', fontsize=14.5, color=INK, va='center')
ax.set_xlim(2.7, 9.6); ax.set_ylim(-20, 130); ax.set_xticks([3, 5, 7, 9]); ax.set_xticklabels(['3°', '5°', '7°', '9°'], fontsize=15); ax.set_yticks([0, 50, 100]); ax.set_yticklabels(['0', '50', '100'], fontsize=15)
ax.grid(True, axis='y', color=GRID, lw=1); ax.set_axisbelow(True); ax.tick_params(colors=INK2, length=0)
for sp in ('top', 'right', 'left'): ax.spines[sp].set_visible(False)
ax.spines['bottom'].set_color(INK2)
fig.text(0.015, 0.978, 'two makes of meter, June to August 2022:', fontsize=14, color=INK2, va='top')
fig.text(0.015, 0.912, 'per cent brighter, counted from 3°' if MODE == 'fading' else 'per cent brighter, by the Sun\'s depth', fontsize=14, color=INK2, va='top')
fig.text(0.56, 0.035, 'Sun below the horizon', fontsize=13, color=INK2, ha='center')
out = B + ('img/tonga-other-make-from3.png' if MODE == 'fading' else 'img/tonga-other-make.png'); fig.savefig(out, dpi=140, facecolor=SURF); plt.close(fig)
f = lambda v: 'none' if v is None else f'{v:+.2f}'
print(f'picture: {out[len(B):]} ({MODE}); magnitudes at 3 to 9 degrees, negative for a brighter twilight')
print('   the first make, the middle (places): ' + ', '.join(f'{tess[d][0]:+.2f} ({tess[d][1]})' for d in D))
for c in ST: print(f"   {ST[c][0].split(',')[0]:<14} " + ', '.join(f(sqm[(c, d)]) for d in D))
print('   the second make, the middle (stations): ' + ', '.join(f'{smid[d][0]:+.2f} ({smid[d][1]})' for d in D))
print('   the model for the second make: ' + ', '.join(f'{msqm[d]:+.2f}' for d in D) + '; for the first: ' + ', '.join(f'{mtess[d]:+.2f}' for d in D))
print('   the second make as a share of the first, the middles: ' + ', '.join(f'{d:g}°: {smid[d][0] / tess[d][0]:.2f}' for d in D if d >= 5) + '; in the model: ' + ', '.join(f'{d:g}°: {msqm[d] / mtess[d]:.2f}' for d in D if d >= 5))
print('   per cent brighter: first make ' + ', '.join(f'{pct(tess[d][0]):+.0f}' for d in D) + '; second make ' + ', '.join(f'{pct(smid[d][0]):+.0f}' for d in D) + '; model for the second ' + ', '.join(f'{pct(msqm[d]):+.0f}' for d in D))
