"""A small picture of the front dial for the card on the notebook's front page: the same positions as the note's dial-today.png
(today.json), with no lettering. usage: thumb_dial.py TODAY.json OUT.png"""
import json, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
src, out = sys.argv[1:3]
SURF, INK2, RING = '#fcfcfb', '#52514e', '#c9c8c2'
BLUE, ORANGE = '#2a78d6', '#eb6834'
today = json.load(open(src))
ORDER = ['moon', 'mercury', 'venus', 'sun', 'mars', 'jupiter', 'saturn']
fig = plt.figure(figsize=(3.2, 3.2), facecolor=SURF)
ax = fig.add_axes([0.02, 0.02, 0.96, 0.96], projection='polar')
ax.set_facecolor(SURF); ax.grid(False); ax.spines['polar'].set_visible(False); ax.set_ylim(0, 8.0); ax.set_yticks([]); ax.set_xticks([])
th = np.linspace(0, 2 * np.pi, 400)
for i, b in enumerate(ORDER):
    r = i + 1.4
    ax.plot(th, np.full_like(th, r), color=RING, lw=1.3, zorder=1)
    ptr, sky = np.radians(today[b][0]), np.radians(today[b][1])
    d = (ptr - sky + np.pi) % (2 * np.pi) - np.pi
    arc = sky + np.linspace(0, d, 60)
    ax.plot(arc, np.full_like(arc, r), color=INK2, lw=2.0, zorder=2)
    ax.plot([sky], [r], marker='o', ms=9.5, mfc=SURF, mec=ORANGE, mew=2.4, ls='none', zorder=3)
    ax.plot([ptr], [r], marker='o', ms=7.5, mfc=BLUE, mec=SURF, mew=1.0, ls='none', zorder=4)
ax.plot([0], [0], marker='o', ms=5, color=INK2)
fig.savefig(out, dpi=100)
print('written', out)
