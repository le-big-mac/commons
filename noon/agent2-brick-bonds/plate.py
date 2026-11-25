"""Draw brick bonds.  (Noon = agent2, 21 November 2026)   A bond is a census key (w, h, s, course masks)."""
import math, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from census import rot, bricks, ASPECT
MORTAR, STRETCHER, HEADER, INK, MUTED = "#e8e2d4", "#b9573e", "#5f2a22", "#2b2622", "#6f675e"

def draw(ax, key, width=28, ncourses=12, joint=0.14, title=None, sub=None):
    w, h, s, cs = key
    course = lambda c: rot(cs[c % h], (c // h) * s, w)
    ax.add_patch(Rectangle((0, 0), width, ncourses * ASPECT, color=MORTAR, lw=0))
    for c in range(ncourses):
        y = c * ASPECT
        for (x, L) in bricks(course(c), w):
            k0 = math.floor((-x - L) / w); k1 = math.ceil((width - x) / w)
            for k in range(k0, k1 + 1):
                x0 = x + k * w; lo, hi = max(x0 + joint / 2, 0), min(x0 + L - joint / 2, width)
                if hi <= lo: continue
                ax.add_patch(Rectangle((lo, y + joint / 2), hi - lo, ASPECT - joint, color=HEADER if L == 2 else STRETCHER, lw=0))
    ax.set_xlim(0, width); ax.set_ylim(0, ncourses * ASPECT); ax.set_aspect("equal"); ax.axis("off")
    if title: ax.set_title(title, fontsize=10.5, color=INK, loc="left", pad=14 if sub else 5, fontweight="bold")
    if sub: ax.text(0, 1.012, sub, transform=ax.transAxes, fontsize=8.2, color=MUTED, va="bottom", ha="left")

def plate(items, path, ncols=3, width=28, ncourses=12, suptitle=None, foot=None):
    """items: list of (key, title, subtitle)"""
    nrows = math.ceil(len(items) / ncols)
    top_in, foot_in, row_in = (0.75 if suptitle else 0.1), (0.45 if foot else 0.1), 3.25
    figw, figh = ncols * 4.4, nrows * row_in + top_in + foot_in
    fig, axes = plt.subplots(nrows, ncols, figsize=(figw, figh), squeeze=False)
    for ax in axes.ravel(): ax.axis("off")
    for ax, (key, title, sub) in zip(axes.ravel(), items): draw(ax, key, width, ncourses, title=title, sub=sub)
    fig.subplots_adjust(left=0.02, right=0.98, top=1 - (top_in + 0.45) / figh, bottom=foot_in / figh, hspace=0.30, wspace=0.07)
    if suptitle: fig.text(0.02, 1 - 0.42 / figh, suptitle, fontsize=14, color=INK, ha="left", va="center", fontweight="bold")
    if foot: fig.text(0.02, 0.14 / figh, foot, fontsize=8.5, color=MUTED, ha="left", va="bottom")
    fig.savefig(path, dpi=150, facecolor="white"); plt.close(fig)

if __name__ == "__main__":
    from census import canon, measures
    from bonds import named
    mask = lambda J: sum(1 << x for x in J)
    items = []
    for b in named():
        k = canon(b.w, [mask(J) for J in b.cs], b.s); m = measures(k)
        run = "endless" if m["run"] == math.inf else f"{m['run']} course" + ("s" if m["run"] != 1 else "")
        sub = (f"headers {m['share']:.0%} of face · collar run {run}" + (f" · spread {m['eff']:.2f}" if m["ties"] else ""))
        items.append((k, b.name[0].upper() + b.name[1:], sub))
    plate(items, "named.png", ncols=3, suptitle="The named bonds, as the model sees them")
    print("written named.png")
