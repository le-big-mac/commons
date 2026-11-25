"""How a cube floats: the "up" direction of the lowest state against density, and a few cubes drawn.
usage: python figures.py results.json out.png d1 d2 d3 d4 d5   (the densities to draw)"""
import sys, json, math, itertools
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R = json.load(open(sys.argv[1])); OUT = sys.argv[2]; DRAW = [float(x) for x in sys.argv[3:]]
INK, MUTED, GRID, BLUE, ORANGE, AQUA, WATER = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834", "#1baf7a", "#9cc3ee"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})
cube = R['cube']; d = np.array([c['d'] for c in cube]); up = np.array([c['minima'][0]['up'] for c in cube]); kinds = [c['minima'][0]['kind'] for c in cube]
fig = plt.figure(figsize=(12.4, 8.6))
ax = fig.add_axes([0.07, 0.50, 0.90, 0.36])
D1, D3 = (3 - math.sqrt(3)) / 6, 0.226893                                          # face up ends; corner up takes over (sliver.py, after.py)
lean = lambda x: math.atan(math.sqrt(max(0.0, 12 * x * (1 - x) - 2)))
c3 = 1 / math.sqrt(3)
pieces = [(np.linspace(0.02, D1, 50), lambda x: (1.0, 0.0, 0.0)), (np.linspace(D1, D3, 60), lambda x: (math.cos(lean(x)), math.sin(lean(x)), 0.0)), (np.linspace(D3, 0.5, 50), lambda x: (c3, c3, c3))]
for k, (col, name) in enumerate(((BLUE, "largest"), (ORANGE, "middle"), (AQUA, "smallest"))):
    for j, (xs, f) in enumerate(pieces):                                          # the closed forms, each stretch drawn separately; a cube of density 1 - d floats like one of density d turned over
        ys = [f(x)[k] for x in xs]
        ax.plot(xs, ys, color=col, lw=2, label=f"{name} component" if j == 0 else None, solid_capstyle='butt')
        ax.plot(1 - xs, ys, color=col, lw=2, solid_capstyle='butt')
    for x in (D3, 1 - D3):                                                         # the jump on to the corner
        ax.plot([x, x], [pieces[1][1](D3)[k], c3], color=col, lw=1, ls=(0, (1, 2)))
    dd = np.r_[d, 1 - d[::-1][1:]]; uu = np.r_[up, up[::-1][1:]]
    show = np.array([round(x * 1000) % 20 == 0 or 0.2 < min(x, 1 - x) < 0.24 for x in dd])   # every 0.02, and every 0.005 round the change
    ax.plot(dd[show], uu[show, k], ls='none', marker='o', ms=4.2, markerfacecolor='white', markeredgecolor=col, markeredgewidth=1.1, zorder=3)
ax.set_xlim(0, 1), ax.set_ylim(-0.03, 1.05)
ax.set_xlabel("density of the cube (water = 1)"), ax.set_ylabel("components of “up” in the cube's axes")
ax.grid(color=GRID, lw=0.8), ax.set_axisbelow(True), ax.tick_params(length=0)
for sp in ax.spines.values():
    sp.set_visible(False)
ax.legend(loc='center', bbox_to_anchor=(0.5, 0.27), frameon=False, fontsize=9.5)
ax.text(0.5, 0.115, "lines: the closed forms.  circles: what the search found.  dotted: the jump on to a corner", ha='center', fontsize=8.5, color=MUTED)
ax.annotate("0.211 to 0.227: leaning,\nequally low any way round\n(one way is drawn)", (0.219, 0.62), xytext=(0.2, 0.62), fontsize=9, color=INK, va='center', ha='right', arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.annotate("the same, turned over", (0.781, 0.62), xytext=(0.80, 0.62), fontsize=9, color=INK, va='center', arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
for x0, x1, lab in ((0.02, D1, "face up"), (D1, D3, ""), (D3, 1 - D3, "corner up"), (1 - D3, 1 - D1, ""), (1 - D1, 0.98, "face up")):
    ax.plot([x0 + 0.002, x1 - 0.002], [1.02, 1.02], color=INK, lw=1.2, solid_capstyle='butt')
    ax.text((x0 + x1) / 2, 1.035, lab, ha='center', va='bottom', fontsize=8.5, color=INK)
ax.set_title("Which way is up for the lowest attitude: (1, 0, 0) is a face, (0.71, 0.71, 0) an edge, (0.58, 0.58, 0.58) a corner", loc='left', fontsize=10.5, color=INK, pad=30)

def draw(axp, n, dens):
    n = np.array(n, float); n /= np.linalg.norm(n)
    a = np.cross(n, [0.0, 0.0, 1.0])
    if np.linalg.norm(a) < 1e-9:
        Rm = np.eye(3)
    else:
        a /= np.linalg.norm(a); ang = math.acos(np.clip(n[2], -1, 1)); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
        Rm = np.eye(3) + math.sin(ang) * K + (1 - math.cos(ang)) * K @ K                # turns n to the vertical
    V = (np.array(list(itertools.product([0, 1], repeat=3)), float) - 0.5) @ Rm.T
    zs = np.sort(V[:, 2]); pts = (np.random.default_rng(1).random((200000, 3)) - 0.5) @ Rm.T; level = np.quantile(pts[:, 2], dens)
    faces = [[0, 1, 3, 2], [4, 5, 7, 6], [0, 1, 5, 4], [2, 3, 7, 6], [0, 2, 6, 4], [1, 3, 7, 5]]
    axp.add_collection3d(Poly3DCollection([V[f] for f in faces], facecolor='#f4efe6', edgecolor=INK, linewidths=1.0, alpha=0.55))
    s = 0.95
    axp.add_collection3d(Poly3DCollection([[(-s, -s, level), (s, -s, level), (s, s, level), (-s, s, level)]], facecolor=WATER, edgecolor='none', alpha=0.35))
    axp.set_xlim(-0.8, 0.8), axp.set_ylim(-0.8, 0.8), axp.set_zlim(-0.8, 0.8), axp.set_box_aspect((1, 1, 1)), axp.set_proj_type('ortho'), axp.view_init(elev=12, azim=-58), axp.set_axis_off()
for i, dens in enumerate(DRAW):
    j = int(np.argmin(np.abs(d - min(dens, 1 - dens))))
    n = np.array(cube[j]['minima'][0]['up']) * (1 if dens <= 0.5 else -1)
    axp = fig.add_axes([0.03 + i * 0.19, 0.03, 0.20, 0.36], projection='3d')
    draw(axp, n, dens)
    fig.text(0.13 + i * 0.19, 0.045, f"density {dens:g}: {cube[j]['minima'][0]['kind'].split(',')[0]}", ha='center', fontsize=9.5, color=INK)
fig.suptitle("How a uniform cube floats", x=0.07, y=0.975, ha='left', fontsize=15, color=INK)
fig.savefig(OUT, dpi=130, facecolor='white')
