"""The picture for the front-door page, drawn for a narrow screen: the five marks 0, 6, 1, 5, 9 on a 12-hour clock, and where the
weights land when the walk takes 12, 6, 4, 3 or 2 steps to a full turn.  The centre of gravity is computed, not drawn by eye.
Lettering is sized to be readable when the picture is shown 350 pixels wide.   usage: clock_fig2.py OUT.png"""
import sys, math, collections
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
INK, SOFT, SURF, BLUE, ORANGE = '#0b0b0b', '#52514e', '#fcfcfb', '#2a78d6', '#eb6834'
M, MARKS = 12, [0, 6, 1, 5, 9]
def pos(turns, r=1.0):            # clockwise from the top, like a clock
    a = 2 * math.pi * turns; return r * math.sin(a), r * math.cos(a)
W, H = 6.0, 10.6                                   # inches; positions below are given in inches and converted
def fx(x): return x / W
def fy(y): return y / H
fig = plt.figure(figsize=(W, H), dpi=150, facecolor=SURF)
fig.text(0.5, fy(10.30), 'Five marks on a 12-hour clock', ha='center', va='center', fontsize=17, color=INK, fontweight='bold')
fig.text(0.5, fy(9.95), 'at hours 0 and 6, and at 1, 5 and 9', ha='center', va='center', fontsize=15, color=INK)
ax = fig.add_axes([fx(1.3), fy(6.25), fx(3.4), fy(3.4)]); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-1.42, 1.42); ax.set_ylim(-1.42, 1.42)
ax.add_patch(plt.Circle((0, 0), 1, fill=False, color=SOFT, lw=1.6))
for h in range(M):
    x, y = pos(h / M); xl, yl = pos(h / M, 1.24)
    ax.plot([0.93 * x, x], [0.93 * y, y], color=SOFT, lw=1.4)
    ax.text(xl, yl, str(h), ha='center', va='center', fontsize=15, color=INK if h in MARKS else SOFT, fontweight='bold' if h in MARKS else 'normal')
    if h in MARKS: ax.plot([x], [y], 'o', ms=17, color=BLUE, mec=SURF, mew=2, zorder=3)
fig.text(0.5, fy(5.85), 'Where the five weights land', ha='center', va='center', fontsize=16, color=INK, fontweight='bold')
fig.text(0.5, fy(5.50), 'for each number of steps to a full turn', ha='center', va='center', fontsize=15, color=INK)
slots = [(1.05, 3.30), (3.00, 3.30), (4.95, 3.30), (2.00, 0.90), (4.00, 0.90)]      # centre x and bottom y of each small circle, inches
for (cxi, y0), d in zip(slots, (12, 6, 4, 3, 2)):
    a2 = fig.add_axes([fx(cxi - 0.8), fy(y0), fx(1.6), fy(1.6)]); a2.set_aspect('equal'); a2.axis('off'); a2.set_xlim(-1.3, 1.3); a2.set_ylim(-1.3, 1.3)
    a2.add_patch(plt.Circle((0, 0), 1, fill=False, color=SOFT, lw=1.4))
    spots = collections.Counter((x % d) for x in MARKS)                      # weights landing on one spot
    for sp, n in spots.items():
        x, y = pos(sp / d); a2.plot([x], [y], 'o', ms=(13 if n == 1 else 19 + 3 * n), color=BLUE, mec=SURF, mew=1.6, zorder=3)
        if n > 1: a2.text(x, y - 0.02, f'{n}', ha='center', va='center', fontsize=14, color='white', fontweight='bold', zorder=5)
    gx = sum(pos(x / d)[0] for x in MARKS) / len(MARKS); gy = sum(pos(x / d)[1] for x in MARKS) / len(MARKS)
    bal = math.hypot(gx, gy) < 1e-9
    a2.plot([0], [0], '+', ms=11, color=SOFT, mew=1.4, zorder=2)
    a2.plot([gx], [gy], 'x', ms=13, color=ORANGE, mew=3.2, zorder=4)
    fig.text(fx(cxi), fy(y0 + 1.75), f'{d} steps', ha='center', va='center', fontsize=15, color=INK, fontweight='bold')
    fig.text(fx(cxi), fy(y0 - 0.18), 'balances' if bal else 'does not balance', ha='center', va='center', fontsize=13.5, color=INK, fontweight='bold' if bal else 'normal')
    print(d, dict(spots), 'centre of gravity (%.3f, %.3f)' % (gx, gy), 'balances' if bal else 'does not balance')
fig.text(0.5, fy(0.27), 'Blue: the weights (a number says how many on one spot).\nOrange cross: their centre of gravity.  Grey +: the centre.',
         ha='center', va='center', fontsize=12.5, color=SOFT, linespacing=1.45)
fig.savefig(sys.argv[1], facecolor=SURF)
