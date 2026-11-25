"""base.py -- every estimate on file of the base case's long-run mean (P = 3, dc = 0.4), side by side.  (The referee's point: the
sheet's four seeds give the highest of them.)   usage: python base.py > base.out"""
import glob, re, json, numpy as np
def sbar(fn, lo=None, hi=None):
    r = np.array([[float(v) for v in l.split()[:3]] for l in open(fn) if l.strip() and not l.startswith("#")]); T = float(re.search(r" T=([\d.]+)", open(fn).readline()).group(1))
    lo = T / 2 if lo is None else lo; hi = T if hi is None else hi
    return float(r[(r[:, 0] >= lo) & (r[:, 0] <= hi + 1e-9), 2].mean())
rows = []
g = [sbar(f) for f in sorted(glob.glob("out/grid/P3-dc0.4-s*.out"))]
rows.append(("the sealed grid, seeds 1 to 4 (second half of each run)", g))
rows.append(("seed 5, the same length (the run kept for snapshots)", [sbar("out/extra/snap-s5.out")]))
r = np.array([[float(v) for v in l.split()[:3]] for l in open("out/long/P3-dc0.4-s6.out") if l.strip() and not l.startswith("#")]); w = 7464 / 10
win = [float(r[(r[:, 0] >= k * w) & (r[:, 0] < (k + 1) * w), 2].mean()) for k in range(1, 10)]
rows.append(("seed 6, run five times longer: its second window, as the sealed mean is taken", [win[0]]))
rows.append(("seed 6: the mean of its nine later windows", [float(np.mean(win))]))
rows.append(("valley of 400 D, seeds 1 and 2", [sbar(f) for f in sorted(glob.glob("out/extra/LX400-s*.out"))]))
rows.append(("valley of 100 D, seeds 1 and 2", [sbar(f) for f in sorted(glob.glob("out/extra/LX100-s*.out"))]))
for tag, label in (("amin2", "a loop cut if longer than 2 dc"), ("smooth2", "two nodes dropped either side of each join"), ("every1", "necks looked for at every step"), ("dt2", "half the time step")):
    rows.append((label, [sbar(f) for f in sorted(glob.glob("out/sweep/%s-s*.out" % tag))]))
rows.append(("node spacing 0.05, to t = 1370 (stopped early)", [sbar(f, hi=1370) for f in sorted(glob.glob("out/fine/ds05-s?.out"))]))
ref = [float(re.search(r"seed1\s+([\d.]+)", l).group(1)) for l in open("referee/blind.out") if l.startswith("1. P=3")] + [float(re.search(r"mean2ndhalf=([\d.]+)", open("referee/s1_seed2.txt").read()).group(1))]
print("# every estimate on file of the long-run mean at P = 3, cutoff distance 0.4")
for label, v in rows:
    print("%-80s %s   mean %.3f" % (label, ", ".join("%.2f" % x for x in v), np.mean(v)))
six = g + [sbar("out/extra/snap-s5.out"), win[0]]
print("six seeds of the plain base case (1 to 5, and seed 6's second window): mean %.3f, standard error %.3f" % (np.mean(six), np.std(six, ddof=1) / np.sqrt(6)))
others = [np.mean(v) for label, v in rows[1:]]
print("the sheet's four seeds: %.3f; the other estimates above run from %.2f to %.2f" % (np.mean(g), min(others), max(others)))
print("the referee's own program, written blind (referee/blind.out, referee/s1_seed2.txt): %s, two seeds, t = 450 to 900" % " and ".join("%.2f" % v for v in ref))
