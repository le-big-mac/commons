# share of loops cut at (near) the minimum loop length 3*dc, from Noon's saved loop lists (read only)
import sys, glob, re
import numpy as np
for pat in ["wide", "grid"]:
    for f in sorted(glob.glob("/home/agent2/meander/out/%s/P*-dc*-s1.oxl" % pat)):
        m = re.search(r"P([\d.]+)-dc([\d.]+)-s1", f)
        P, dc = float(m.group(1)), float(m.group(2))
        a = np.loadtxt(f, usecols=(0, 1))
        t, arc = a[:, 0], a[:, 1]
        arc = arc[t > t.max() / 2]
        amin = 3 * dc
        print("%-5s P=%-4g dc=%-4g loops=%6d  median=%6.2f  share with length < 1.1*3dc: %.3f   < 1.5*3dc: %.3f   share of cut length in loops <1.5*3dc: %.3f" % (
            pat, P, dc, len(arc), np.median(arc), np.mean(arc < 1.1 * amin), np.mean(arc < 1.5 * amin), arc[arc < 1.5 * amin].sum() / arc.sum()))
