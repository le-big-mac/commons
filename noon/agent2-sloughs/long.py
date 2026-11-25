"""long.py -- does the long-run mean drift?  Three settings were run five times longer than the sealed runs (seed 6).
Each run is cut into ten windows as long as the half-run the sealed mean is taken over; the first is the start-up.
usage: python long.py > long.out"""
import glob, re, json, numpy as np
G = json.load(open("out/grid/settings.json"))
for f in sorted(glob.glob("out/long/*.out")):
    head = open(f).readline(); par = dict(re.findall(r"(\w+)=([-\w.+]+)", head)); P = float(par["P"]); dc = float(par["DC"]); T = float(par["T"])
    r = np.array([[float(v) for v in l.split()] for l in open(f) if l.strip() and not l.startswith("#")]); t = r[:, 0]
    w = T / 10; done = int((t[-1] + 1e-6) // w)
    m = [r[(t >= k * w) & (t < (k + 1) * w), 2].mean() for k in range(done)]; y = [r[(t >= k * w) & (t < (k + 1) * w), 9].mean() for k in range(done)]
    g = [x for x in G if x["P"] == P and x["DC"] == dc][0]
    print("P = %g, dc = %g, run to t = %.0f of %.0f; windows of %.0f; the sealed grid's mean for this setting (window 2 of four other seeds): %.3f ± %.3f" % (P, dc, t[-1], T, w, g["Sbar"], g["se"]))
    print("   mean of S in each window:  " + " ".join("%.3f" % v for v in m))
    print("   rms spread of y:           " + " ".join("%5.1f" % v for v in y))
    if done >= 4:
        later = np.array(m[1:]); k = np.arange(1, done); slope = np.polyfit(k, later, 1)[0]
        print("   windows 2 to %d: mean %.3f, least %.3f, greatest %.3f, sd %.3f; trend %+.4f a window; first half of them %.3f, second half %.3f" % (
            done, later.mean(), later.min(), later.max(), later.std(ddof=1), slope, later[:len(later) // 2].mean(), later[len(later) // 2:].mean()))
