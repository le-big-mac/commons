"""The figure: sixteen claims, the class a blind referee gave each, the mark I had given it, and what was read.   usage: python figures.py prior.png"""
import sys, json, re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
INK, MUTED, GRID, BLUE, ORANGE = "#2b2622", "#6f675e", "#e4dfd6", "#2a78d6", "#eb6834"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 9.5})
FIN = json.load(open("final.json")); M = json.load(open("mine.json")); sheet = open("expectations.md").read(); marks = dict(re.findall(r"^(W\d+)\. \((.*?)\)", sheet, re.M))
NAME = {"W1": "weak tiles of cyclic groups", "W2": "brick bonds", "W3": "opposite points with the same weather", "W4": "desire paths", "W5": "snowdrops", "W6": "when a league is settled", "W7": "what paces the ice ages", "W8": "ranked-ballot elections",
        "W9": "what makes a smell foul", "W10": "born just after the line", "W11": "do numbers decide battles", "W12": "which way up a cube floats", "W13": "which blocks of ice roll over", "W14": "hawks and doves with neighbours", "W15": "the arXiv's daily boundary", "W16": "how chancy is outselling"}
SAID = {"W1": "the open question and who asked it", "W2": "nothing (textbooks, from memory)", "W3": "a book, from memory", "W4": "the paper, unread", "W5": "nothing for the trend", "W6": "nothing", "W7": "the paper, from memory", "W8": "the survey, read",
        "W9": "the paper, for its data only", "W10": "\"known since the 1980s\"", "W11": "three works, from memory", "W12": "\"neither of us looked\"", "W13": "a search tool's summary", "W14": "the paper; a tool's summary", "W15": "a search tool's summary", "W16": "a search tool's report"}
X = {"not found": 0, "found in part": 1, "found": 2}; order = sorted(FIN, key=lambda k: (-X[FIN[k]], marks[k] != "remembered", int(k[1:])))
fig = plt.figure(figsize=(11.6, 6.6)); ax = fig.add_axes([0.335, 0.085, 0.21, 0.72])
for j, k in enumerate(order):
    y = len(order) - 1 - j; ax.plot([0, 2], [y, y], color=GRID, lw=0.8, zorder=1); col = BLUE if marks[k] == "remembered" else ORANGE
    ax.plot([X[FIN[k]]], [y], marker='o' if marks[k] == "remembered" else 's', ms=9, color=col, markeredgecolor='white', markeredgewidth=0.8, zorder=3)
    ax.text(-0.35, y, NAME[k], ha='right', va='center', fontsize=9.2, color=INK); ax.text(2.4, y, SAID[k], ha='left', va='center', fontsize=9.2, color=INK)
ax.set_xlim(-0.3, 2.3); ax.set_ylim(-0.7, len(order) - 0.3); ax.set_xticks([0, 1, 2]); ax.set_xticklabels(["not found", "in part", "found"]); ax.xaxis.tick_top(); ax.set_yticks([]); ax.tick_params(length=0)
for sp in ax.spines.values(): sp.set_visible(False)
ax.plot([], [], ls='none', marker='o', ms=9, color=BLUE, label="I had marked it \"remembered\""); ax.plot([], [], ls='none', marker='s', ms=9, color=ORANGE, label="I had marked it \"guessed\""); ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.02), ncol=1, frameon=False, fontsize=8.8)
fig.text(0.335 + 0.21 + 0.036, 0.845, "what the study's own README had named", fontsize=9, color=MUTED); fig.text(0.335 - 0.012, 0.845, "the study", fontsize=9, color=MUTED, ha='right')
fig.suptitle("Who already knew?", x=0.04, y=0.965, ha='left', fontsize=15, color=INK)
fig.text(0.04, 0.925, "Sixteen of my studies, looked up afterwards: was the main claim already in print? Each is placed by the class a fresh instance gave it, blind, from the passages I quoted.", fontsize=9.5, color=MUTED, va='top')
fig.savefig(sys.argv[1], dpi=130, facecolor='white')
