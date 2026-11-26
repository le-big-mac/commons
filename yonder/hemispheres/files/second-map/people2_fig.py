"""How many more people the half centred near Berlin holds than the half centred in the Alps, by year, on three population maps.
usage: people2_fig.py OUT_DIR FIGURE.png      (reads OUT_DIR/{ghs,g1,g2}-YEAR.json written by run_people2.py)"""
import sys, json, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
od, figp = sys.argv[1], sys.argv[2]
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#d9d8d2'
SER = [('ghs', 'GHS-POP: the maps first used', '#2a78d6', 'o', (1975, 2000, 2005, 2010, 2015, 2020, 2025, 2030)),
       ('g1', "WorldPop's older maps (made in 2018)", '#eb6834', 's', (2000, 2010, 2020)),
       ('g2', "WorldPop's newer maps,\nwhich know the censuses of about 2020", '#1baf7a', 'D', (2015, 2020, 2025, 2030))]
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9.5, 'text.color': INK, 'figure.facecolor': SURF, 'axes.facecolor': SURF, 'savefig.facecolor': SURF,
                     'axes.edgecolor': GRID, 'axes.labelcolor': INK2, 'xtick.color': INK2, 'ytick.color': INK2})
fig, ax = plt.subplots(figsize=(7.6, 4.3), dpi=170)
ax.axhline(0, color=INK2, lw=1.0, zorder=1)
ax.axvspan(2022.5, 2031.5, color='#f1f0ec', zorder=0, lw=0)
ax.text(2027, -12.9, 'projections', color=INK2, ha='center', va='bottom', fontsize=8.5)
ax.text(1974.3, 12.6, '5 million people is 0.06% of the world', color=INK2, fontsize=8.5, va='top')
ends = {}
for key, name, col, mk, years in SER:
    xs, ys = [], []
    for y in years:
        p = f'{od}/{key}-{y}.json'
        if not os.path.exists(p): continue
        r = json.load(open(p)); xs.append(y); ys.append((r['only_berlin'] - r['only_valais']) / 1e6)
    ax.plot(xs, ys, color=col, lw=2, marker=mk, ms=6.5, mec=SURF, mew=1.2, zorder=3)
    if key == 'g1': ax.plot(xs[-1:], ys[-1:], marker=mk, ms=6.5, mfc=SURF, mec=col, mew=1.8, zorder=4, ls='none')      # hollow: a projection
    ends[key] = (xs, ys, name, col)
# direct labels, in ink, each at an end of its own line; the older series' label has a thin leader in its line's colour
ax.text(2032.0, ends['ghs'][1][-1], 'GHS-POP:\nthe maps\nfirst used', color=INK, ha='left', va='center', fontsize=9, clip_on=False)
ax.text(2032.0, ends['g2'][1][-1] - 0.6, "WorldPop's newer\nmaps, which know\nthe censuses of\nabout 2020", color=INK, ha='left', va='center', fontsize=9, clip_on=False)
ax.annotate("WorldPop's older maps\n(made in 2018; their 2020\nis a projection, drawn hollow)", xy=(ends['g1'][0][0] - 0.5, ends['g1'][1][0] + 0.25), xytext=(1997.0, -1.9),
            color=INK, ha='right', va='top', fontsize=9, arrowprops=dict(arrowstyle='-', color=ends['g1'][3], lw=1.0, shrinkA=2, shrinkB=1))
ax.text(1974.3, 0.45, 'above the line, the half centred near Berlin holds more', color=INK2, fontsize=8.5, va='bottom')
ax.text(1974.3, -0.5, 'below it, the half centred in the Alps holds more', color=INK2, fontsize=8.5, va='top')
ax.set_xlim(1973.5, 2031.5); ax.set_ylim(-13.5, 13.5)
ax.set_xticks([1975, 1990, 2000, 2010, 2020, 2030]); ax.set_yticks([-10, -5, 0, 5, 10]); ax.set_yticklabels(['10 fewer', '5 fewer', 'level', '5 more', '10 more'])
ax.set_ylabel('how many more people in the half centred near Berlin\nthan in the half centred in the Alps, millions')
ax.grid(axis='y', color=GRID, lw=0.6); ax.set_axisbelow(True)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.tick_params(length=0)
fig.tight_layout(); fig.subplots_adjust(right=0.83); fig.savefig(figp); print('written', figp)
for key, (xs, ys, name, col) in ends.items(): print(key, [(x, round(y, 1)) for x, y in zip(xs, ys)])
