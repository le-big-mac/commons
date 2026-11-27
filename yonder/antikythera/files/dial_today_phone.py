"""The front dial for the public page, drawn for a narrow screen: the same positions as dial_today_page.py (today.json),
the same marks and the same words, with the names set above and below the rings so that the lettering can be read on a phone.
usage: dial_today_phone.py TODAY.json OUT.png
At 350 pixels wide (a phone's column) the type of the labels comes out at about 11 pixels (capitals about 8 pixels high). Colours as in dial_today_page.py."""
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
# where each label sits, in the picture's own x and y (the outer ring has radius 7.4); chosen by eye for this one day:
# four names above the rings and three below, each joined to its own pair of marks by a line that starts on the side of the
# name towards the marks (the last pair of numbers: where on the name the line starts), so that no line runs through a name
SPOT = {'mars': (-8.0, 10.6, 'left', (1.0, 0.5)), 'moon': (8.0, 10.6, 'right', (0.0, 0.5)),
        'jupiter': (-8.0, 8.9, 'left', (0.6, 0.0)), 'saturn': (8.0, 8.9, 'right', (1.0, 0.0)),
        'venus': (-8.0, -8.7, 'left', (1.0, 0.5)), 'mercury': (8.0, -8.7, 'right', (0.0, 0.5)), 'sun': (-2.1, -10.3, 'center', (0.5, 1.0))}
W = 4.6
fig = plt.figure(figsize=(W, W * 25.6 / 16.4 * 0.94 + 0.35))
ax = fig.add_axes([0.0, 0.07, 1.0, 0.93])
ax.set_xlim(-8.2, 8.2); ax.set_ylim(-11.4, 11.6); ax.set_aspect('equal'); ax.axis('off')
th = np.linspace(0, 2 * np.pi, 400)
def xy(deg, r): return r * np.cos(np.radians(deg)), r * np.sin(np.radians(deg))
for i, b in enumerate(ORDER):
    r = i + 1.4
    ax.plot(r * np.cos(th), r * np.sin(th), color=RING, lw=1.0, zorder=1)
    ptr, sky = today[b]
    d = (ptr - sky + 180) % 360 - 180
    arc = sky + np.linspace(0, d, 80)
    ax.plot(*xy(arc, r), color=INK2, lw=1.8, zorder=2)
    ax.plot(*xy(sky, r), marker='o', ms=9, mfc=SURF, mec=ORANGE, mew=2.2, ls='none', zorder=3)
    ax.plot(*xy(ptr, r), marker='o', ms=7, mfc=BLUE, mec=SURF, mew=1.1, ls='none', zorder=4)
    a = abs(d)
    how = f'{a:.0f}° apart' if a >= 1 else 'less than 1° apart'
    lx, ly, ha, rel = SPOT[b]
    mx, my = xy(sky + d / 2, r)
    ax.annotate(f'{NAMES[b]}: {how}', (mx, my), xytext=(lx, ly), textcoords='data', ha=ha, va='center', fontsize=10.5, color=INK,
                fontweight='bold' if b == 'moon' else 'normal', zorder=6, bbox=dict(fc=SURF, ec='none', pad=1.5, alpha=0.9),
                arrowprops=dict(arrowstyle='-', color=GREY, lw=0.8, shrinkA=2, shrinkB=7, relpos=rel))
    print(b, f'{d:+.2f}', how)
ax.plot([0], [0], marker='o', ms=5, color=GREY); ax.text(0.35, -0.05, 'Earth', fontsize=9.5, color=INK2, va='center', ha='left')
h1, = ax.plot([], [], marker='o', ms=7, mfc=BLUE, mec=SURF, mew=1.1, ls='none', label='where the pointer would stand')
h2, = ax.plot([], [], marker='o', ms=9, mfc=SURF, mec=ORANGE, mew=2.2, ls='none', label='where the body really is')
fig.legend(handles=[h1, h2], loc='lower center', bbox_to_anchor=(0.5, 0.0), frameon=False, fontsize=10, labelcolor=INK2, ncol=1, handletextpad=0.3, labelspacing=0.35)
fig.savefig(out, dpi=230)
print('written', out)
