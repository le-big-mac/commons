"""diverge.py -- how fast do two rivers that differ in the seventh decimal place part company?
For each seed: run the base case (P = 3, dc = 0.4, LX = 60) to t = 40, take the river as it is then, move one node by 3e-7,
and run both on to t = 110.  The difference in length/LX is followed from 1e-5 to 1e-2 and a rate fitted to its logarithm.
usage: python diverge.py"""
import subprocess, numpy as np
rates = []
for seed in (31, 32, 33, 34, 35, 36):
    snap = "out/diverge/s%d.snap" % seed
    subprocess.run(["./river", "3", "0.4", "60", "40", str(seed), "-snap", "40", snap, "-out", "100"], capture_output=True)
    line = open(snap).read().strip().split("\n")[-1].split()
    assert abs(float(line[0]) - 40) < 1e-6
    a = "out/diverge/s%d-a.start" % seed; b = "out/diverge/s%d-b.start" % seed
    open(a, "w").write(" ".join(line) + "\n")
    k = 2 + 2 * (int(line[1]) // 2) + 1; line2 = list(line); line2[k] = "%.7f" % (float(line[k]) + 3e-7)
    open(b, "w").write(" ".join(line2) + "\n")
    S = []
    for f in (a, b):
        out = subprocess.run(["./river", "3", "0.4", "60", "70", str(seed), "-start", f, "-out", "0.25"], capture_output=True, text=True).stdout
        S.append(np.array([float(l.split()[2]) for l in out.split("\n") if l and not l.startswith("#")]))
    d = np.abs(S[0] - S[1]); t = 40 + 0.25 * np.arange(len(d))
    first = lambda v: int(np.argmax(d >= v)) if (d >= v).any() else None
    i0, i1 = first(1e-5), first(1e-2)
    if i0 is None or i1 is None or i1 - i0 < 8:
        print("seed %d: the difference in length/LX did not pass from 1e-5 to 1e-2 in the time (greatest %.1e)" % (seed, d.max())); continue
    sel = slice(i0, i1 + 1); ok = d[sel] > 0
    r = np.polyfit(t[sel][ok], np.log(d[sel][ok]), 1)[0]; rates.append(r)
    print("seed %d: difference 1e-5 at t = %.1f, 1e-2 at t = %.1f; rate %.3f per unit of time (tenfold every %.1f)" % (seed, t[i0], t[i1], r, np.log(10) / r))
if rates:
    print("mean rate %.3f (sd %.3f) over %d seeds: tenfold every %.1f units of time; from the sixteenth decimal place to the second in about %.0f" % (
        np.mean(rates), np.std(rates, ddof=1), len(rates), np.log(10) / np.mean(rates), 14 * np.log(10) / np.mean(rates)))
