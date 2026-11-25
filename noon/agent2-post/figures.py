"""post.png: the two numbers against the lag for four pegs and six colours, and the scheme for a lag of three.   usage: python -I figures.py"""
import json, itertools, collections
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
INK, MUTED, GRID, BLUE, ORANGE, PAPER = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834", "#ffffff"
B = json.load(open("boards.json"))["4 6"]; K, W = B["K"], B["W"]
fig, (ax, bx) = plt.subplots(1, 2, figsize=(12, 4.8), dpi=140, gridspec_kw=dict(width_ratios=[1.15, 1]))
x = [0, 1, 2, 3, 4]
ax.plot(x, K, color=BLUE, lw=2, marker="o", ms=8, label="K: guesses that always fix the code", zorder=3)
ax.plot(x[:4], W, color=ORANGE, lw=2, marker="s", ms=8, label="W: guesses by which the code has always been sent", zorder=3)
W4 = B["W4"]; ax.plot([3, 4], [W[3], W4], color=ORANGE, lw=2, zorder=2); ax.plot([4], [W4], color=ORANGE, marker="s", ms=8, zorder=3)
for i, v in enumerate(K): ax.annotate(str(v), (x[i], v), textcoords="offset points", xytext=(0, -17), ha="center", color=INK, fontsize=11)
for i, v in enumerate(W + [W4]): ax.annotate(str(v), (x[i], v), textcoords="offset points", xytext=(0, 9), ha="center", color=INK, fontsize=11)
ax.plot(x, [K[d] + d + 1 for d in x], color=MUTED, lw=1, ls=(0, (3, 3)), zorder=1); ax.annotate("K + lag + 1", (4, K[4] + 5), textcoords="offset points", xytext=(8, -3), color=MUTED, fontsize=9.5, va="center")
ax.set_xticks(x); ax.set_xticklabels(["0\n(ordinary play)", "1", "2", "3", "4"]); ax.set_xlim(-0.4, 4.9); ax.set_ylim(3, 12); ax.set_yticks(range(3, 13))
ax.set_xlabel("lag: how many more guesses must be sent before an answer arrives", color=INK); ax.set_ylabel("guesses", color=INK)
ax.set_title("Mastermind by post, four pegs and six colours", color=INK, fontsize=12.5, loc="left")
ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
for s in ("top", "right"): ax.spines[s].set_visible(False)
for s in ("left", "bottom"): ax.spines[s].set_color(GRID)
ax.tick_params(colors=MUTED, length=0); ax.legend(frameon=False, loc="upper left", fontsize=9.5, labelcolor=INK)
def answer(g, s):
    b = sum(a == c for a, c in zip(g, s)); return f"{b}{sum(min(g.count(c), s.count(c)) for c in set(g)) - b}"
book = {}
for line in open("out/final/K-d3-Q5.out"):
    if line.startswith("S "): _, t, rest = line.split(); h, g = rest.split(":"); book[(int(t), h)] = g
blind = [book[(t, "-")] for t in (1, 2, 3, 4)]; codes = ["".join(p) for p in itertools.product("123456", repeat=4)]; size = collections.Counter(answer(blind[0], s) for s in codes)
bx.axis("off"); bx.set_xlim(0, 1); bx.set_ylim(0, 1)
bx.text(0, 0.97, "A lag of three: one look is enough", color=INK, fontsize=12.5, va="top")
bx.text(0, 0.87, "Sent blind:   " + "   ".join(blind), color=INK, fontsize=11.5, va="top", family="monospace")
bx.text(0, 0.79, "The fifth guess, by the answer to " + blind[0] + " alone:", color=MUTED, fontsize=10, va="top")
rows = sorted(size, key=lambda a: -size[a]); y = 0.70
bx.text(0.02, y, "black, white", color=MUTED, fontsize=9); bx.text(0.30, y, "codes", color=MUTED, fontsize=9); bx.text(0.46, y, "fifth", color=MUTED, fontsize=9)
bx.text(0.58, y, "black, white", color=MUTED, fontsize=9); bx.text(0.80, y, "codes", color=MUTED, fontsize=9); bx.text(0.91, y, "fifth", color=MUTED, fontsize=9)
for i, a in enumerate(rows[:7]):
    yy = y - 0.075 * (i + 1); bx.text(0.06, yy, f"{a[0]}, {a[1]}", color=INK, fontsize=10.5, family="monospace"); bx.text(0.30, yy, str(size[a]), color=MUTED, fontsize=10.5, family="monospace"); bx.text(0.46, yy, book.get((5, a), "none"), color=INK, fontsize=10.5, family="monospace")
for i, a in enumerate(rows[7:]):
    yy = y - 0.075 * (i + 1); bx.text(0.62, yy, f"{a[0]}, {a[1]}", color=INK, fontsize=10.5, family="monospace"); bx.text(0.80, yy, str(size[a]), color=MUTED, fontsize=10.5, family="monospace"); bx.text(0.91, yy, book.get((5, a), "none"), color=INK, fontsize=10.5, family="monospace")
bx.text(0, 0.06, "Five guesses then fix every one of the 1,296 codes.\nFive blind guesses never do; nor do four at a lag of one.", color=MUTED, fontsize=9.5, va="top")
fig.tight_layout(); fig.savefig("post.png", facecolor=PAPER); print("wrote post.png")
