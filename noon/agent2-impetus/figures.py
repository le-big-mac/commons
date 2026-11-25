"""Shapes of four shots in air, and how the shape depends on launch speed over terminal velocity.   usage: python figures.py results.json impetus.png"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import impetus as I
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]
INK, MUTED, GRID, NEUTRAL = "#2b2622", "#6f675e", "#e4dfd6", "#b9b1a5"
COL = {'trebuchet stone': "#2a78d6", '24-pound shot': "#eb6834", 'musket ball': "#1baf7a", 'shuttlecock': "#eda100"}
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 9.5})
fig = plt.figure(figsize=(12.4, 9.0)); a = fig.add_axes([0.07, 0.50, 0.90, 0.36]); b = fig.add_axes([0.07, 0.08, 0.40, 0.30]); c = fig.add_axes([0.57, 0.08, 0.40, 0.30])
def style(ax, title):
    ax.grid(color=GRID, lw=0.8); ax.set_axisbelow(True); ax.tick_params(length=0)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_title(title, loc='left', fontsize=10.5, color=INK, pad=8)
x = np.linspace(0, 1, 200); a.plot(x, x * (1 - x), color=NEUTRAL, lw=1.4, ls=(0, (4, 3)), label="no air: a parabola")
for name in COL:
    q = R[name]; P = np.array(q['at45']['path']) / q['at45']['range']
    a.plot(P[:, 0], P[:, 1], color=COL[name], lw=2, label=f"{name}: launched at {q['v0'] / q['vt']:.1f} times its terminal velocity, range {q['at45']['range']:,.0f} m")
a.set_xlim(0, 1.0); a.set_ylim(0, 0.62); a.set_aspect('equal', adjustable='box', anchor='W'); a.set_xlabel("distance along the ground, as a share of the range"); a.set_ylabel("height, same scale")
a.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), frameon=False, fontsize=9)
style(a, "Four shots at 45 degrees, each drawn to the size of its own range")
F = R['family'] + [dict(ratio=x, **{k: I.fly(100.0 * x, 100.0, 45)[k] for k in ('apex_fraction', 'impact_angle')}) for x in (100, 300, 1000, 3000, 10000)]      # very fast shots, added after the referee
r = np.array([f['ratio'] for f in F])
for ax, key, ref, lab, title in ((b, 'apex_fraction', 0.5, "a parabola: 0.5", "Where the top of the path is, as a share of the range (45-degree launch)"), (c, 'impact_angle', 45.0, "a parabola: 45", "The angle at which it lands, launched at 45 degrees")):
    ax.plot(r, [f[key] for f in F], color=INK, lw=1.6); ax.axhline(ref, color=NEUTRAL, lw=1.2, ls=(0, (4, 3))); ax.text(9000, ref, lab, color=MUTED, fontsize=8.5, va='bottom', ha='right')
    for name in COL:
        q = R[name]; ax.plot(q['v0'] / q['vt'], q['at45'][key], ls='none', marker='o', ms=8, color=COL[name], markeredgecolor='white', markeredgewidth=1.2, zorder=3)
        up = name == 'shuttlecock'
        ax.annotate(name, (q['v0'] / q['vt'], q['at45'][key]), xytext=(-6, 8) if up else (6, -12), ha='right' if up else 'left', textcoords='offset points', fontsize=8.5, color=INK)
    ax.set_xscale('log'); ax.set_xticks([0.1, 1, 10, 100, 1000, 10000]); ax.set_xticklabels(['0.1', '1', '10', '100', '1,000', '10,000']); ax.set_xlim(0.05, 10000); ax.set_xlabel("launch speed, in terminal velocities"); style(ax, title)
b.set_ylim(0.45, 1.0); b.axhline(1.0, color=NEUTRAL, lw=1.2, ls=(0, (1, 2))); b.text(0.052, 0.985, "straight out and straight down: 1", color=MUTED, fontsize=8.5, va='top')
c.set_ylim(40, 92); c.axhline(90, color=NEUTRAL, lw=1.2, ls=(0, (1, 2))); c.text(0.052, 89.3, "straight down: 90", color=MUTED, fontsize=8.5, va='top')
fig.suptitle("Cannonballs in air: between the parabola and the old three-part picture", x=0.07, y=0.965, ha='left', fontsize=15, color=INK)
fig.text(0.07, 0.90, "Point masses with drag as the square of the speed, launched at 45 degrees over level ground.\nAt a given elevation the shape depends on one number: launch speed over terminal velocity.", fontsize=9.5, color=MUTED)
fig.savefig(OUT, dpi=130, facecolor='white')
