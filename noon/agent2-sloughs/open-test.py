"""open-test.py -- a test of open.c that could fail.  The open reach differs from the repeating valley only at its two ends, and
what happens at the upstream end travels downstream no faster than the bends do.  So, started from the same nodes, the middle of
an open reach must follow the repeating river node for node for a while.  Here: 200 D of river, the same start, to t = 10;
nodes between x = 110 and x = 180 are compared.  As a control the open reach is also run with P = 3.01 for 3.
usage: python open-test.py > open-test.out"""
import subprocess, numpy as np
start = "out/open/test.start"
subprocess.run(["./river", "3", "0.4", "200", "0", "41", "-snap", "1", start], capture_output=True)
def last(cmd):
    out = subprocess.run(cmd, capture_output=True, text=True).stdout.strip().split("\n")
    f = [l.split() for l in out if not l.startswith("#") and len(l.split()) > 50][-1]
    return float(f[0]), np.array(f[2:], float).reshape(-1, 2)
ta, a = last(["./river", "3", "0.4", "200", "10", "41", "-start", start, "-snap", "10", "/dev/stdout", "-out", "100"])
for label, P in (("the same P", "3"), ("control: the open reach given P = 3.01", "3.01")):
    tb, b = last(["./open", P, "0.4", "200", "10", "41", "-start", start, "-snap", "10", "/dev/stdout", "-out", "100"])
    sel = a[(a[:, 0] > 110) & (a[:, 0] < 180)]
    d = np.array([np.hypot(*(b - p).T).min() for p in sel])
    ends = a[(a[:, 0] < 5)]; de = np.array([np.hypot(*(b - p).T).min() for p in ends])
    print("%s: at t = %g, %d nodes of the repeating river between x = 110 and 180; the nearest node of the open reach is at most %.1e away (amplitude of the river there: %.2f). Within 5 D of the upstream end the two differ by up to %.1e" % (
        label, ta, len(sel), d.max(), np.abs(sel[:, 1]).max(), de.max()))
