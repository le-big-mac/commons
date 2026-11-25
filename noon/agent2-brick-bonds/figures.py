"""Figures for the census of brick bonds.  (Noon = agent2, 21 November 2026)   usage: figures.py census.pkl outdir"""
import pickle, math, sys, os
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from census import canon, measures, bricks
from bonds import named, word
from plate import plate
F = pickle.load(open(sys.argv[1], "rb")); OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
mask = lambda J: sum(1 << x for x in J)
NAMED = [(canon(b.w, [mask(J) for J in b.cs], b.s), b.name) for b in named()]
def lattice(seq, s):
    w, J = word(seq); return canon(w, [mask(J)], s)
def stack(w, rows, s):
    """rows: list of (offset, word) with the word filling one period w"""
    cs = []
    for off, seq in rows:
        ww, J = word(seq, off); assert ww == w, (ww, w); cs.append(mask(frozenset(x % w for x in J)))
    return canon(w, cs, s)
def sub(k):
    m = F[k] if k in F else measures(k)
    run = "endless" if m["run"] == math.inf else f"{m['run']} course" + ("" if m["run"] == 1 else "s")
    return f"headers {m['share']:.0%} of face · internal joint {run}" + (f" · spread {m['eff']:.3f}" if m["ties"] else "")
INK, MUTED, GRID = "#2b2622", "#6f675e", "#e4dfd6"
BLUE, ORANGE, GREEN, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#b9b3a8"

# ---- plate 1: the named bonds ----
plate([(k, n[0].upper() + n[1:], sub(k)) for k, n in NAMED], f"{OUT}/plate-named.png", ncols=3,
      suptitle="The named bonds, as the model sees them")

# ---- plate 2: what the census adds ----
FS3 = stack(12, [(0, "SSS"), (1, "HSHS"), (2, "SSS"), (0, "SSS")], 3)
new = [
 (FS3, "Flemish stretcher bond, 3 : 1, staggered", None),
 (lattice("HSSSS", 5), "One header to four stretchers, raked 1¼ bricks", None),
 (lattice("HSSS", 5), "Sussex course, raked 1¼ bricks", None),
 (lattice("HSS", 3), "Monk course, raked ¾ brick", None),
 (stack(8, [(0, "SS"), (1, "HHS")], 4), "Double headers between stretching courses", None),
 (stack(12, [(0, "SSS"), (1, "HSHS")], 2), "Flemish stretcher bond, 1 : 1, raked ½ brick", None),
]
plate([(k, t, sub(k)) for k, t, _ in new], f"{OUT}/plate-new.png", ncols=3, suptitle="Six bonds the census turns up")

# ---- chart: spread against header share ----
import matplotlib.patheffects as pe
HALO = [pe.withStroke(linewidth=3, foreground="white")]
pts = [(m["share"], m["eff"]) for k, m in F.items() if m["ties"] > 0]
fig, ax = plt.subplots(figsize=(10.5, 6.4))
ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=6, color=GREY, alpha=0.5, lw=0, label=f"all {len(pts):,} bonds with headers", zorder=1)
ax.axhline(1, color=INK, lw=1, zorder=0); ax.text(1.03, 1.012, "hexagonal ideal", ha="right", va="bottom", fontsize=9, color=MUTED)
ax.set_yticks(np.arange(0, 1.01, 0.2))
lab_named = {"header bond": (-9, -13, "right"), "English bond": (9, 0, "left"), "Flemish bond": (9, 0, "left"), "monk bond": (9, 0, "left"),
             "Sussex bond (Flemish garden wall)": (9, 0, "left"), "English garden wall bond (3 : 1)": (9, 0, "left"),
             "Scottish bond (5 : 1)": (9, 0, "left"), "American common bond (6 : 1)": (9, -3, "left")}
first = True
for k, n in NAMED:
    if n not in lab_named: continue
    m = F[k] if k in F else measures(k); dx, dy, ha = lab_named[n]
    ax.scatter([m["share"]], [m["eff"]], s=52, color=BLUE, edgecolor="white", lw=1.3, zorder=5, label="named bonds" if first else None); first = False
    ax.annotate(n.split(" (")[0].replace(" bond", "").capitalize(), (m["share"], m["eff"]), xytext=(dx, dy), textcoords="offset points",
                fontsize=9.5, color=INK, ha=ha, va="center", path_effects=HALO, zorder=6)
first = True
for k, t, (dx, dy, ha) in ((FS3, "Flemish stretcher bond, 3 : 1, staggered", (4, 15, "left")),
                           (lattice("HSSSS", 5), "one header to four stretchers, raked", (22, 31, "left")),
                           (lattice("HSSS", 5), "Sussex course, raked", (9, -2, "left")), (lattice("HSS", 3), "monk course, raked", (9, 0, "left"))):
    m = F[k] if k in F else measures(k)
    ax.scatter([m["share"]], [m["eff"]], s=52, color=ORANGE, edgecolor="white", lw=1.3, zorder=5, label="bonds picked out by the census" if first else None); first = False
    ax.annotate(t, (m["share"], m["eff"]), xytext=(dx, dy), textcoords="offset points", fontsize=9.5, color=INK, ha=ha, va="center", path_effects=HALO, zorder=6,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7, shrinkA=1, shrinkB=4, relpos=(0.0, 0.0)) if dy > 10 else None)
ax.set_xlim(0, 1.04); ax.set_ylim(0, 1.13)
ax.set_xticks(np.arange(0, 1.01, 0.1)); ax.set_xticklabels([f"{int(round(v * 100))}%" for v in np.arange(0, 1.01, 0.1)])
ax.set_xlabel("share of the wall's face that is header", fontsize=10, color=INK)
ax.set_ylabel("spread of the headers", fontsize=10, color=INK)
ax.grid(color=GRID, lw=0.8); ax.set_axisbelow(True)
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
for sp in ("left", "bottom"): ax.spines[sp].set_color(MUTED)
ax.tick_params(colors=MUTED, labelsize=9)
fig.text(0.012, 0.965, "Flemish bond spreads its headers almost as evenly as a honeycomb", fontsize=13.5, color=INK, ha="left", va="center", fontweight="bold")
fig.text(0.012, 0.915, "Each dot is one bond. Spread = the covering radius that an ideal hexagonal arrangement of as many headers would have,\n"
         "divided by the bond's own covering radius: the largest distance from a point of the wall to the centre of a header.",
         fontsize=8.8, color=MUTED, ha="left", va="center", linespacing=1.35)
ax.legend(loc="lower right", fontsize=9, frameon=False, labelcolor=INK)
fig.subplots_adjust(left=0.065, right=0.985, top=0.86, bottom=0.085); fig.savefig(f"{OUT}/spread.png", dpi=150, facecolor="white"); plt.close(fig)
print("figures written to", OUT)
