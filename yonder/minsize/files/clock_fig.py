"""The picture for the front-door page: the five marks 0, 6, 1, 5, 9 on a 12-hour clock, and where the weights land when
the walk takes 1/d of a turn an hour, for d = 12, 6, 4, 3, 2.  The centre of gravity is computed, not drawn by eye.
usage: clock_fig.py OUT.png"""
import sys, math, collections
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
INK, SOFT, SURF, BLUE, ORANGE = '#0b0b0b', '#52514e', '#fcfcfb', '#2a78d6', '#eb6834'
M, MARKS = 12, [0, 6, 1, 5, 9]
def pos(turns, r=1.0):            # clockwise from the top, like a clock
    a = 2 * math.pi * turns; return r * math.sin(a), r * math.cos(a)
fig = plt.figure(figsize=(10.4, 4.6), dpi=150, facecolor=SURF)
ax = fig.add_axes([0.01, 0.10, 0.27, 0.80]); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)
ax.add_patch(plt.Circle((0, 0), 1, fill=False, color=SOFT, lw=1.2))
for h in range(M):
    x, y = pos(h / M); xl, yl = pos(h / M, 1.22)
    ax.plot([0.94 * x, x], [0.94 * y, y], color=SOFT, lw=1)
    ax.text(xl, yl, str(h), ha='center', va='center', fontsize=10, color=INK if h in MARKS else SOFT, fontweight='bold' if h in MARKS else 'normal')
    if h in MARKS: ax.plot([x], [y], 'o', ms=11, color=BLUE, mec=SURF, mew=1.5, zorder=3)
ax.set_title('Five marks on a 12-hour clock:\n0 and 6, with 1, 5 and 9', fontsize=11, color=INK, pad=4)
for k, d in enumerate((12, 6, 4, 3, 2)):
    a2 = fig.add_axes([0.30 + 0.14 * k, 0.26, 0.135, 0.50]); a2.set_aspect('equal'); a2.axis('off'); a2.set_xlim(-1.45, 1.45); a2.set_ylim(-1.45, 1.45)
    a2.add_patch(plt.Circle((0, 0), 1, fill=False, color=SOFT, lw=1.0))
    spots = collections.Counter((x % d) for x in MARKS)                      # weights landing on one spot
    for s, n in spots.items():
        x, y = pos(s / d); a2.plot([x], [y], 'o', ms=(9 if n == 1 else 13 + 2 * n), color=BLUE, mec=SURF, mew=1.2, zorder=3)
        if n > 1: a2.text(x, y - 0.02, f'{n}', ha='center', va='center', fontsize=9.5, color='white', fontweight='bold', zorder=5)
    gx = sum(pos(x / d)[0] for x in MARKS) / len(MARKS); gy = sum(pos(x / d)[1] for x in MARKS) / len(MARKS)
    bal = math.hypot(gx, gy) < 1e-9
    a2.plot([0], [0], '+', ms=7, color=SOFT, mew=1, zorder=2)
    a2.plot([gx], [gy], 'x', ms=9, color=ORANGE, mew=2.4, zorder=4)
    a2.set_title(f'd = {d}', fontsize=11, color=INK, pad=2)
    a2.text(0, -1.80, 'balances' if bal else 'does not\nbalance', ha='center', va='top', fontsize=10, color=INK, fontweight='bold' if bal else 'normal')
    print(d, dict(spots), 'centre of gravity (%.3f, %.3f)' % (gx, gy), 'balances' if bal else 'does not balance')
fig.text(0.645, 0.93, 'Where the five weights land when each hour is 1/d of a turn', ha='center', va='center', fontsize=11, color=INK)
fig.text(0.645, 0.085, 'Blue: the weights (a number on a spot says how many land there).\nOrange cross: their centre of gravity.   Grey +: the centre of the circle.',
         ha='center', va='center', fontsize=9.5, color=SOFT, linespacing=1.5)
fig.savefig(sys.argv[1], facecolor=SURF)
