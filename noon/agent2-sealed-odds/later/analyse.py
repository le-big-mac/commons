"""The later lines: totals, the two corrections of the earlier report tried unchanged, the tally by mark, and the scorecard.
usage: python -I analyse.py > analyse.out      (reads lines.csv from collect.py; writes verdicts.out)"""
import csv, math, random
R = [dict(r, odds=float(r["odds"]), outcome=float(r["outcome"])) for r in csv.DictReader(open("lines.csv"))]
logit = lambda p: math.log(p / (1 - p)); expit = lambda x: 1 / (1 + math.exp(-x)); clip = lambda p: min(0.99, max(0.01, p))
A = lambda p: clip(expit(0.277 + 1.413 * logit(p))); B = lambda p: clip(expit(logit(p) + 0.581))
brier = lambda rows, f=lambda p: p: sum((f(r["odds"]) - r["outcome"]) ** 2 for r in rows) / len(rows)
share = lambda rows: sum(r["outcome"] for r in rows) / len(rows); mean = lambda rows: sum(r["odds"] for r in rows) / len(rows)
def line(name, rows):
    h = sum(1 for r in rows if r["outcome"] == 1); f = sum(1 for r in rows if r["outcome"] == 0); half = len(rows) - h - f; s = share(rows)
    return f"   {name:28s} {len(rows):3d} lines; held {h:3d}, failed {f:2d}, half {half}; share that held {s:.3f}; my mean odds {mean(rows):.3f}; Brier {brier(rows):.4f}; one half on every line would score {sum((0.5 - r['outcome']) ** 2 for r in rows) / len(rows):.4f}"
print(f"{len(R)} settled lines in {len({r['sheet'] for r in R})} sheets of {len({r['study'] for r in R})} studies (a half counts as 0.5)\n")
print("1. All the later lines, beside the first 142 (held 0.82, mean odds 0.734, Brier 0.134)"); print(line("all", R))
print("\n2. The earlier report's corrections, unchanged")
sA, sB, s0 = brier(R, A), brier(R, B), brier(R)
print(f"   sealed odds {s0:.4f}; correction A (shift +0.277, slope 1.413) {sA:.4f} ({sA - s0:+.4f}); correction B (shift +0.581) {sB:.4f} ({sB - s0:+.4f})")
random.seed(20261123); studies = sorted({r["study"] for r in R})
def boot(f, by_study):
    out = []
    for _ in range(10000):
        if by_study: samp = [r for s in random.choices(studies, k=len(studies)) for r in R if r["study"] == s]
        else: samp = random.choices(R, k=len(R))
        out.append(brier(samp, f) - brier(samp))
    out.sort(); return out[250], out[9749]
for nm, f in (("A", A), ("B", B)):
    lo, hi = boot(f, False); lo2, hi2 = boot(f, True)
    print(f"   {nm} minus sealed: resampling the lines as if independent {lo:+.4f} to {hi:+.4f}; resampling whole studies {lo2:+.4f} to {hi2:+.4f}")
better = lambda f: sum(1 for s in studies if brier([r for r in R if r["study"] == s], f) < brier([r for r in R if r["study"] == s]))
print(f"   studies that score better corrected: A {better(A)} of {len(studies)}, B {better(B)} of {len(studies)}")
# the shift and slope that would have been best on the later lines themselves (in sample): a coarse search is enough to see the direction
best = min(((sum((clip(expit(a / 100 + b / 100 * logit(r["odds"]))) - r["outcome"]) ** 2 for r in R) / len(R)), a / 100, b / 100) for a in range(-150, 151, 5) for b in range(20, 301, 5))
print(f"   fitted to the later lines themselves (least Brier on a grid, in sample): shift {best[1]:+.2f}, slope {best[2]:.2f}, scoring {best[0]:.4f}")
print("\n3. By the mark each line carried when sealed")
for mk in ("worked", "remembered", "guessed", "none"): print(line(mk, [r for r in R if r["mark"] == mk]))
print("\n4. By my odds"); 
for lo, hi in ((0, 0.45), (0.45, 0.55), (0.55, 0.65), (0.65, 0.75), (0.75, 0.85), (0.85, 1.01)):
    rows = [r for r in R if lo <= r["odds"] < hi]
    if rows: print(line(f"odds {lo:.2f} to under {min(hi, 1):.2f}", rows))
print("\n5. By study")
for s in dict.fromkeys(r["study"] for r in R): print(line(s, [r for r in R if r["study"] == s]))
W = [r for r in R if r["mark"] == "worked"]; G = [r for r in R if r["mark"] == "guessed"]
V = [("Z1", 0.30, sA < s0, f"correction A scores {sA:.4f} against {s0:.4f} sealed (sealed: A better)"),
     ("Z2", 0.35, sB < s0, f"correction B scores {sB:.4f} against {s0:.4f} sealed (sealed: B better)"),
     ("Z3", 0.60, s0 > 0.134, f"my sealed odds score {s0:.4f} on the later lines (sealed: worse than 0.134)"),
     ("Z4", 0.55, share(R) < mean(R), f"share that held {share(R):.3f}, my mean odds {mean(R):.3f} (sealed: the share below the mean odds)"),
     ("Z5", 0.80, share(W) - share(G) >= 0.20, f"worked {share(W):.3f}, guessed {share(G):.3f}: {100 * (share(W) - share(G)):.1f} points apart (sealed: at least 20)"),
     ("Z6", 0.65, share(W) >= 0.85, f"worked lines held {share(W):.3f} of the time (sealed: 0.85 or more)"),
     ("Z7", 0.60, 0.50 <= share(G) <= 0.65, f"guessed lines held {share(G):.3f} of the time (sealed: 0.50 to 0.65)"),
     ("Z8", 0.55, brier(G) >= 0.24, f"on guessed lines my odds score {brier(G):.4f} (sealed: 0.24 or worse)")]
out = [f"{n:3s} guessed  odds {o:.2f}  {'held  ' if ok else 'FAILED'}  {w}" for n, o, ok, w in V]; held = sum(v[2] for v in V)
out.append(f"\nheld {held}, failed {len(V) - held}, of {len(V)}; my mean odds {sum(v[1] for v in V) / len(V):.3f}; Brier {sum((v[1] - v[2]) ** 2 for v in V) / len(V):.4f}; had I said 0.5 on every line, 0.2500")
out.append(f"by the sheet's own marks: marked guessed: {len(V)} lines, {held} held, {len(V) - held} failed")
open("verdicts.out", "w").write("\n".join(out) + "\n"); print("\n6. The sealed sheet\n" + "\n".join(out))
