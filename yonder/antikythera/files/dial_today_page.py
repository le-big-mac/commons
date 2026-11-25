"""The front dial for the public page: the same positions as the note's dial-today.png (today.json), drawn for a reader who has
not seen the work: each name beside its own pair of dots, whole degrees, no scale and no title (the caption carries it).
usage: dial_today_page.py TODAY.json OUT.png
Colours: two slots of the chart palette (validated as a pair); text in ink."""
import json, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
src, out = sys.argv[1:3]
SURF, INK, INK2, RING, GREY = '#fcfcfb', '#0b0b0b', '#52514e', '#d5d4ce', '#8f8e88'
BLUE, ORANGE = '#2a78d6', '#eb6834'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'text.color': INK, 'figure.facecolor': SURF, 'savefig.facecolor': SURF})
today = json.load(open(src))
ORDER = ['moon', 'mercury', 'venus', 'sun', 'mars', 'jupiter', 'saturn']
NAMES = {'moon': 'Moon', 'mercury': 'Mercury', 'venus': 'Venus', 'sun': 'Sun', 'mars': 'Mars', 'jupiter': 'Jupiter', 'saturn': 'Saturn'}
# where each label sits, in the picture's own x and y (the outer ring has radius 7.4); chosen by eye for this one day
SPOT = {'moon': (-0.6, 9.0, 'center'), 'jupiter': (-9.6, 5.3, 'left'), 'mars': (-9.6, 1.5, 'left'), 'venus': (-9.6, -1.3, 'left'),
        'mercury': (-9.6, -3.6, 'left'), 'sun': (-6.2, -8.2, 'left'), 'saturn': (9.6, 2.6, 'right')}
fig = plt.figure(figsize=(7.2, 6.6))
ax = fig.add_axes([0.02, 0.07, 0.96, 0.91])
ax.set_xlim(-10, 10); ax.set_ylim(-9.0, 9.6); ax.set_aspect('equal'); ax.axis('off')
th = np.linspace(0, 2 * np.pi, 400)
def xy(deg, r): return r * np.cos(np.radians(deg)), r * np.sin(np.radians(deg))
for i, b in enumerate(ORDER):
    r = i + 1.4
    ax.plot(r * np.cos(th), r * np.sin(th), color=RING, lw=1.0, zorder=1)
    ptr, sky = today[b]
    d = (ptr - sky + 180) % 360 - 180
    arc = sky + np.linspace(0, d, 80)
    ax.plot(*xy(arc, r), color=INK2, lw=1.8, zorder=2)
    ax.plot(*xy(sky, r), marker='o', ms=10, mfc=SURF, mec=ORANGE, mew=2.3, ls='none', zorder=3)
    ax.plot(*xy(ptr, r), marker='o', ms=8, mfc=BLUE, mec=SURF, mew=1.2, ls='none', zorder=4)
    a = abs(d)
    how = f'{a:.0f}° apart' if a >= 1 else 'less than 1° apart'
    lx, ly, ha = SPOT[b]
    mx, my = xy(sky + d / 2, r)
    ax.annotate(f'{NAMES[b]}: {how}', (mx, my), xytext=(lx, ly), textcoords='data', ha=ha, va='center', fontsize=10.5, color=INK,
                fontweight='bold' if b == 'moon' else 'normal', zorder=6, bbox=dict(fc=SURF, ec='none', pad=1.5, alpha=0.9),
                arrowprops=dict(arrowstyle='-', color=GREY, lw=0.8, shrinkA=2, shrinkB=7))
    print(b, f'{d:+.2f}', how)
ax.plot([0], [0], marker='o', ms=5, color=GREY); ax.text(0.35, -0.05, 'Earth', fontsize=8.5, color=INK2, va='center', ha='left')
h1, = ax.plot([], [], marker='o', ms=8, mfc=BLUE, mec=SURF, mew=1.2, ls='none', label='where the pointer would stand')
h2, = ax.plot([], [], marker='o', ms=10, mfc=SURF, mec=ORANGE, mew=2.3, ls='none', label='where the body really is')
fig.legend(handles=[h1, h2], loc='lower center', bbox_to_anchor=(0.5, 0.0), frameon=False, fontsize=10, labelcolor=INK2, ncol=2, handletextpad=0.3, columnspacing=2.0)
fig.savefig(out, dpi=170)
print('written', out)
