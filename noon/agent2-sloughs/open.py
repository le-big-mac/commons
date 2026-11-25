"""open.py -- the open reach with one paper's values (open.c, open.sh; four seeds each way): the river's length over the valley's
272, the straight distance between its two ends, and the paper's measure, length over that distance.
  quiet:  the river above the fixed first node is straight (no curvature there)
  fed:    the first node is given the curvature the far end had a step before (-inlet: the paper's rule, as I read it)
  k9, k6: every node pushed at every step by a Gaussian of sd 1e-9 or 1e-6 along its normal (the second referee's test)
usage: python open.py > open-reach.out"""
import glob, numpy as np
print("# open reach, first node fixed, last node free; P = 6.43, cutoff distance 0.476, valley 272, feedback with F0^2 = 1.86 (open.c)")
print("# each line: four seeds, mean ± standard error; then the four seeds")
for tag, label in (("quiet", "quiet inlet"), ("quiet-k9", "quiet inlet, pushes of 1e-9"), ("quiet-k6", "quiet inlet, pushes of 1e-6"), ("fed", "fed inlet"), ("fed-k9", "fed inlet, pushes of 1e-9")):
    R = []
    for f in sorted(glob.glob("out/open/%s-s?.out" % tag)):
        r = np.array([[float(v) for v in l.split()] for l in open(f) if l.strip() and not l.startswith("#")]); assert r[-1, 0] >= 499.9, f; R.append(r)
    assert len(R) == 4, tag
    for name, lo, hi in (("12.5 to 125", 12.5, 125), ("250 to 500", 250, 500)):
        ratio = np.array([r[(r[:, 0] >= lo) & (r[:, 0] <= hi), 5].mean() for r in R]); lv = np.array([r[(r[:, 0] >= lo) & (r[:, 0] <= hi), 2].mean() for r in R])
        print("%s, t = %s: length/distance %.2f ± %.2f (%s); length/272 %.2f ± %.2f" % (label, name, ratio.mean(), ratio.std(ddof=1) / 2, ", ".join("%.2f" % v for v in ratio), lv.mean(), lv.std(ddof=1) / 2))
    for t in (125.0, 500.0):
        d = [r[np.argmin(np.abs(r[:, 0] - t)), 6] for r in R]; ye = [r[np.argmin(np.abs(r[:, 0] - t)), 8] for r in R]; xe = [r[np.argmin(np.abs(r[:, 0] - t)), 7] for r in R]
        print("%s, at t = %g: distance between the ends %s (272 at the start); the free end is at x = %s, y = %s" % (label, t, ", ".join("%.0f" % v for v in d), ", ".join("%.0f" % v for v in xe), ", ".join("%.0f" % v for v in ye)))
# how much of the head is straight at t = 125: the length of river from the first node before the direction first turns by more than 0.05 radian
print("# the straight head at t = 125: river from the first node to where its direction first differs by 0.05 radian from the first segment's")
for tag in ("quiet", "quiet-k9", "quiet-k6", "fed"):
    out = []
    for f in sorted(glob.glob("out/open/%s-s?.snap" % tag)):
        for line in open(f):
            w = line.split()
            if abs(float(w[0]) - 125) < 1e-6:
                xy = np.array(w[2:], float).reshape(-1, 2); d = np.diff(xy, axis=0); th = np.unwrap(np.arctan2(d[:, 1], d[:, 0])); s = np.cumsum(np.hypot(d[:, 0], d[:, 1]))
                k = np.argmax(np.abs(th - th[0]) > 0.05); out.append(s[k] if np.abs(th - th[0]).max() > 0.05 else s[-1])
    print("%s: %s" % (tag, ", ".join("%.0f" % v for v in out)))
