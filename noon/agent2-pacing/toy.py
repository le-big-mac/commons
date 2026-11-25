"""A toy, after Huybers (2007), to show why terminations paced by the tilt come two or three tilt cycles apart.
Ice grows at a steady rate.  It collapses when it exceeds a threshold that is lower when the tilt is high:
    collapse when  ice > T0 - a * (tilt - mean) / sd.
After a collapse the ice starts again from zero.  The tilt is the real one of the last two million years.
usage: python -I toy.py DATADIR toy.npz"""
import sys
import numpy as np
D = sys.argv[1]
orb = np.array([[float(x.replace('D', 'E')) for x in line.split()] for line in open(f"{D}/INSOLN.LA2004.BTL.ASC") if line.strip()])
orb = orb[(orb[:, 0] <= 0) & (orb[:, 0] >= -2000)][::-1]                # oldest first, one row per thousand years
tilt = np.degrees(orb[:, 2])
z = (tilt - tilt.mean()) / tilt.std()
T0s = np.arange(20, 170.5, 0.5)
rows = []
for a in (0.0, 10.0, 25.0):
    means, spreads = [], []
    for T0 in T0s:
        ice, last, gaps = 0.0, None, []
        for k in range(len(z)):
            ice += 1.0
            if ice > T0 - a * z[k]:
                if last is not None:
                    gaps.append(k - last)
                last, ice = k, 0.0
        g = np.array(gaps[2:])                                           # forget the start
        means.append(g.mean()), spreads.append(g.std())
    rows.append((a, np.array(means), np.array(spreads)))
    m = rows[-1][1] / 41.0
    print(f"pull of the tilt a = {a:4.1f}: share of thresholds whose mean interval is within 0.05 of a whole number of tilt cycles: {100 * np.mean(np.abs(m - np.rint(m)) < 0.05):.0f}%")
np.savez(sys.argv[2], T0s=T0s, **{f"mean{int(a)}": m for a, m, s in rows}, **{f"sd{int(a)}": s for a, m, s in rows})
