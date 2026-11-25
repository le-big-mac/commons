"""theirs.py -- the author's eight open-reach runs, read (not run): distance between the ends at t = 125 and t = 500, window means, the end's place.
usage: python -I theirs.py"""
import glob, numpy as np
for tag in ("beatton", "inlet"):
    for f in sorted(glob.glob("/home/agent2/meander/out/open/%s-s*.out" % tag)):
        r = np.array([[float(v) for v in l.split()] for l in open(f) if l.strip() and not l.startswith("#")]); t = r[:, 0]
        i125 = np.argmin(abs(t - 125)); m1 = (t >= 12.5) & (t <= 125); m2 = (t >= 250) & (t <= 500)
        print("%-8s %s  dist at t=125: %.0f, at t=500: %.0f (end at %.0f, %.0f); mean dist 12.5-125: %.0f, 250-500: %.0f (min %.0f, max %.0f);  L/dist %.2f %.2f;  L/LX %.2f %.2f" % (
            tag, f.split("-s")[-1][:1], r[i125, 6], r[-1, 6], r[-1, 7], r[-1, 8], r[m1, 6].mean(), r[m2, 6].mean(), r[m2, 6].min(), r[m2, 6].max(), r[m1, 5].mean(), r[m2, 5].mean(), r[m1, 2].mean(), r[m2, 2].mean()))
