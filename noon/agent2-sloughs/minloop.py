"""minloop.py -- how often does the rule "a loop must be longer than three cutoff distances" decide what is cut?
(The referee's question.)  For every setting: the share of the loops cut in the second half of the runs whose length is within
a tenth of that least length.  Where the share is large, what is being cut is any stretch of that length whose ends are near
each other, and the value belongs to the rule.   usage: python minloop.py > minloop.out"""
import glob, re, numpy as np
print("# share of loops cut within 10% of the least length allowed (3 dc), second half of each run, all seeds together")
print("#    P    dc   least length   loops   share   median loop")
for folder in ("out/grid", "out/wide", "out/after"):
    keys = sorted(set(re.match(r".*/(?:between-)?P([\d.]+)-dc([\d.]+)-s\d+\.oxl", f).groups() for f in glob.glob(folder + "/*.oxl") if re.match(r".*/(?:between-)?P([\d.]+)-dc([\d.]+)-s\d+\.oxl", f)), key=lambda k: (float(k[0]), float(k[1])))
    for P, dc in keys:
        arcs = []
        for f in glob.glob(folder + "/*P%s-dc%s-s*.oxl" % (P, dc)):
            if not glob.glob(f.replace(".oxl", ".done")): continue
            a = np.loadtxt(f, ndmin=2); T = a[-1, 0]; arcs.append(a[a[:, 0] > T / 2, 1])
        if not arcs: continue
        arcs = np.concatenate(arcs); least = 3 * float(dc)
        print("%6s %5s %10.1f %10d %7.1f%% %10.1f   %s" % (P, dc, least, len(arcs), 100 * (arcs <= 1.1 * least).mean(), np.median(arcs), folder))
