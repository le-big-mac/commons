"""Two figures. usage: plots.py   (reads today.json, results-S.json, results-S.npz written by run.py and after.py)
Colours: two slots of the chart palette (validated as a pair), grey for context, text in ink."""
import json, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

H = os.path.dirname(os.path.abspath(__file__))
SURF, INK, INK2, GRID, GREY = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df', '#b4b3ad'
BLUE, ORANGE = '#2a78d6', '#eb6834'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'text.color': INK, 'axes.labelcolor': INK2, 'xtick.color': INK2,
                     'ytick.color': INK2, 'axes.edgecolor': GRID, 'axes.facecolor': SURF, 'figure.facecolor': SURF,
                     'savefig.facecolor': SURF, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True,
                     'grid.color': GRID, 'grid.linewidth': 0.8, 'axes.axisbelow': True, 'lines.solid_capstyle': 'round'})
today = json.load(open(os.path.join(H, 'today.json')))
S = json.load(open(os.path.join(H, 'results-S.json')))
Z = np.load(os.path.join(H, 'results-S.npz'))
NAMES = {'moon': 'Moon', 'mercury': 'Mercury', 'venus': 'Venus', 'sun': 'Sun', 'mars': 'Mars', 'jupiter': 'Jupiter', 'saturn': 'Saturn'}
ORDER = ['moon', 'mercury', 'venus', 'sun', 'mars', 'jupiter', 'saturn']        # the order of the rings, from the centre

# ---- A: the dial today ----
fig = plt.figure(figsize=(6.6, 7.4))
ax = fig.add_axes([0.09, 0.105, 0.82, 0.74], projection='polar')
ax.set_facecolor(SURF); ax.grid(False); ax.spines['polar'].set_visible(False)
ax.set_ylim(0, 8.6); ax.set_yticks([])
ax.set_xticks(np.radians(np.arange(0, 360, 30)))
ax.set_xticklabels([f'{d}°' for d in range(0, 360, 30)], color=INK2, fontsize=9)
th = np.linspace(0, 2 * np.pi, 400)
for i, b in enumerate(ORDER):
    r = i + 1.4
    ax.plot(th, np.full_like(th, r), color=GRID, lw=1.0, zorder=1)
    ptr, sky = np.radians(today[b][0]), np.radians(today[b][1])
    d = (ptr - sky + np.pi) % (2 * np.pi) - np.pi
    arc = sky + np.linspace(0, d, 60)
    ax.plot(arc, np.full_like(arc, r), color=INK2, lw=1.6, zorder=2)
    ax.plot([sky], [r], marker='o', ms=9, mfc=SURF, mec=ORANGE, mew=2.2, ls='none', zorder=3)
    ax.plot([ptr], [r], marker='o', ms=7.5, mfc=BLUE, mec=SURF, mew=1.2, ls='none', zorder=4)
    err = S['today'][b]
    ax.text(np.radians(292), r, f'{NAMES[b]}  {err:+.1f}°' if b != 'sun' else f'{NAMES[b]}  {err:+.1f}°', ha='left', va='center',
            fontsize=9, color=INK, rotation=0, bbox=dict(fc=SURF, ec='none', pad=1.0), zorder=5)
for d in range(0, 360, 30):
    ax.plot(np.radians([d, d]), [8.25, 8.5], color=GREY, lw=1.0)
ax.plot([0], [0], marker='o', ms=5, color=GREY)
ax.text(0, 0, '  Earth', fontsize=8, color=INK2, va='center', ha='left')
fig.text(0.06, 0.975, 'The dial on 23 November 2026, had it been kept turning since 205 BC', fontsize=11.5, color=INK, ha='left', va='top')
fig.text(0.06, 0.945, 'Longitude against the stars (ecliptic of J2000). Number: pointer minus sky.', fontsize=9, color=INK2, ha='left', va='top')
h1, = ax.plot([], [], marker='o', ms=7.5, mfc=BLUE, mec=SURF, mew=1.2, ls='none', label='where the pointer stands')
h2, = ax.plot([], [], marker='o', ms=9, mfc=SURF, mec=ORANGE, mew=2.2, ls='none', label='where the body is')
fig.legend(handles=[h1, h2], loc='lower left', bbox_to_anchor=(0.05, 0.005), frameon=False, fontsize=9, labelcolor=INK2, ncol=2, handletextpad=0.3, columnspacing=1.6)
fig.savefig(os.path.join(H, 'dial-today.png'), dpi=200)
plt.close(fig)

# ---- B: each planet's pointer, in its own time and now ----
PL = ['mercury', 'venus', 'mars', 'jupiter', 'saturn']
fig, axes = plt.subplots(5, 2, figsize=(9.2, 9.6), sharey='row')
rms = lambda x: float(np.sqrt(np.mean(np.asarray(x) ** 2)))
for i, p in enumerate(PL):
    jt, rt = Z['jd_then_' + p], Z['res_then_' + p]
    jn, en = Z['jd_' + p], Z['err_' + p]
    m1 = jt <= jt[0] + 20 * 365.25
    m2 = jn >= jn[-1] - 20 * 365.25
    a, b = axes[i]
    a.plot((jt[m1] - jt[0]) / 365.25, rt[m1], color=BLUE, lw=1.3)
    b.plot(2026.895 + (jn[m2] - jn[-1]) / 365.25, en[m2], color=BLUE, lw=1.3)
    for ax_ in (a, b):
        ax_.axhline(0, color=GREY, lw=0.8)
    lim = max(np.max(np.abs(rt)), np.max(np.abs(en))) * 1.12
    a.set_ylim(-lim, lim)
    a.set_ylabel('pointer minus sky\n(degrees)', fontsize=8.5)
    a.set_title(f'{NAMES[p]}: rms {rms(rt):.1f}°, largest {np.max(np.abs(rt)):.0f}° over 76 years', fontsize=9, color=INK, loc='left', pad=3)
    b.set_title(f'{NAMES[p]}: rms {rms(en):.1f}°, largest {np.max(np.abs(en)):.0f}° over 76 years', fontsize=9, color=INK, loc='left', pad=3)
    a.set_xlim(0, 20); b.set_xlim(2006.895, 2026.895)
    a.set_xticks([0, 5, 10, 15, 20]); b.set_xticks([2010, 2015, 2020, 2025])
    if i == 4:
        a.set_xlabel('years after 1 May 205 BC'); b.set_xlabel('year')
fig.text(0.075, 0.985, 'In its own time: the circle theory at its best', fontsize=10.5, color=INK, ha='left', va='top')
fig.text(0.545, 0.985, 'After 2,231 years of turning', fontsize=10.5, color=INK, ha='left', va='top')
fig.tight_layout(h_pad=0.6, w_pad=1.2, rect=(0, 0, 1, 0.965))
fig.savefig(os.path.join(H, 'then-and-now.png'), dpi=170)
plt.close(fig)
print('written')
