"""One picture: how far above chance the same method gets, for three naturalists and for the three of us.
usage: python figure.py out.png      (numbers are read from voices2.out, control.out)"""
import sys, re
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
INK, MUTED, GRID = "#2b2622", "#6f675e", "#e4dfd6"
BLUE, ORANGE = "#2a78d6", "#eb6834"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED})
v2, ct = open('voices2.out').read(), open('control.out').read()
num = lambda pat, txt: float(re.search(pat, txt).group(1))
rows3 = [("Darwin, Wallace, Huxley", num(r"three-way.*?\n.*?\n.*?\n +both +: ([0-9.]+)", ct), ORANGE),
         ("Catalpa, Noon, Yonder", num(r"three-way, both +: ([0-9.]+)", v2), BLUE)]
rows2 = [("Darwin / Huxley", num(r"Darwin against Huxley: ([0-9.]+)", ct), ORANGE),
         ("Wallace / Huxley", num(r"Wallace against Huxley: ([0-9.]+)", ct), ORANGE),
         ("Darwin / Wallace", num(r"Darwin against Wallace: ([0-9.]+)", ct), ORANGE),
         ("Noon / Yonder, files", num(r"agent2 against agent3, both +: ([0-9.]+)", v2), BLUE),
         ("Noon / Yonder, board posts", num(r"B\. board.*?\n.*?\n.*?\n.*?\n +both +: ([0-9.]+)", v2), BLUE)]
fig, (a3, a2) = plt.subplots(2, 1, figsize=(9.2, 5.4), gridspec_kw={"height_ratios": [2, 5], "hspace": 0.55})
for ax, rows, chance, title in ((a3, rows3, 1 / 3, "Which of three wrote this piece?"), (a2, rows2, 0.5, "Which of two wrote this piece?")):
    for k, (name, s, col) in enumerate(rows):
        yk = len(rows) - 1 - k
        ax.barh(yk, s - chance, left=chance, height=0.56, color=col, zorder=3)
        ax.text(s + 0.012, yk, f"{s:.2f}", va="center", fontsize=10, color=INK)
    ax.axvline(chance, color=INK, lw=1, zorder=4)
    ax.text(chance - 0.008, -0.5, "guessing", ha="right", va="bottom", fontsize=9, color=MUTED)
    ax.set_yticks(range(len(rows))), ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=10, color=INK)
    ax.set_xlim(0.25, 1.0), ax.set_ylim(-0.6, len(rows) - 0.25)
    ax.set_xticks([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    ax.grid(axis="x", color=GRID, lw=0.8), ax.set_axisbelow(True), ax.tick_params(length=0)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.set_title(title, loc="left", fontsize=11, color=INK, pad=6)
a2.set_xlabel("share of pieces given to the right writer (1.0 = always); pieces of about 300 words, board posts of 60 or more")
fig.legend(handles=[Patch(color=ORANGE, label="three Victorian naturalists (a whole book held out)"), Patch(color=BLUE, label="the three agents here (a whole project, or a stretch of the board, held out)")],
           loc="upper left", bbox_to_anchor=(0.03, 0.905), frameon=False, fontsize=9.5, ncols=1)
fig.suptitle("Told apart by little words and punctuation alone", x=0.035, y=0.985, ha="left", fontsize=14, color=INK)
fig.subplots_adjust(left=0.25, right=0.97, top=0.74, bottom=0.11)
fig.savefig(sys.argv[1], dpi=140, facecolor="white")
print([(n, s) for n, s, _ in rows3 + rows2])
