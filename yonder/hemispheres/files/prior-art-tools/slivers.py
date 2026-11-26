"""Where the people of the two slivers live (read-only check on the study's 0.05-degree grids).

usage: python -I slivers.py GRID_DIR

Sliver A: inside the half centred 52.37 N, 12.68 E and outside the half centred 46.0 N, 7.18 E.
Sliver B: the reverse. Hard edge by cell centre on a sphere. People are summed in 5-degree boxes
(south-west corner printed), for the 1975 and 2020 grids.
"""
import sys, os
import numpy as np

D = sys.argv[1]
CELL = 0.05
H, W = 3600, 7200
lat = -90 + (np.arange(H) + 0.5) * CELL
lon = -180 + (np.arange(W) + 0.5) * CELL
LAT, LON = np.meshgrid(np.radians(lat), np.radians(lon), indexing="ij")
X = np.cos(LAT) * np.cos(LON); Y = np.cos(LAT) * np.sin(LON); Z = np.sin(LAT)

def unit(la, lo):
    la, lo = np.radians(la), np.radians(lo)
    return np.array([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)])

def inside(c):
    u = unit(*c)
    return (X * u[0] + Y * u[1] + Z * u[2]) > 0

B_ = inside((52.37, 12.68)); V_ = inside((46.0, 7.18))
A = B_ & ~V_
B = V_ & ~B_
bi = np.floor((np.degrees(LAT) + 90) / 5).astype(int)
bj = np.floor((np.degrees(LON) + 180) / 5).astype(int)
for year in (1975, 2020):
    p = np.load(os.path.join(D, "pop005.npy" if year == 2020 else "pop005_%d.npy" % year))
    for name, m in (("A: only in the Berlin half", A), ("B: only in the Alpine half", B)):
        tot = p[m].sum()
        print("== %d  %s: %.2f million" % (year, name, tot / 1e6))
        h = np.bincount((bi[m] * 72 + bj[m]), weights=p[m], minlength=36 * 72).reshape(36, 72)
        ii, jj = np.nonzero(h > 0.2e6)
        for i, j in sorted(zip(ii, jj), key=lambda t: -h[t[0], t[1]]):
            print("    box lat %4d..%4d lon %5d..%5d : %7.2f million" % (-90 + 5 * i, -85 + 5 * i, -180 + 5 * j, -175 + 5 * j, h[i, j] / 1e6))
        print("    (boxes under 0.2 million together: %.2f million)" % ((h[h <= 0.2e6].sum()) / 1e6))
        # coarse regions
        la, lo = np.degrees(LAT), np.degrees(LON)
        if name.startswith("A"):
            regs = [("Philippines (lon 116.5-128, lat 4-22)", (lo > 116.5) & (lo < 128) & (la > 4) & (la < 22)),
                    ("Malay Peninsula with Singapore and the south of Thailand (lon 98-105, lat 1.1-9, east of Sumatra's coast is not separated)", (lo > 98) & (lo < 105) & (la > 1.1) & (la < 9)),
                    ("Borneo (lon 108.5-119.5, lat -5-7.5)", (lo > 108.5) & (lo < 119.5) & (la > -5) & (la < 7.5) & ~((lo > 116.5) & (la > 4))),
                    ("Indochina (lon 100-110, lat 8-16)", (lo > 100) & (lo < 110) & (la > 8) & (la < 16)),
                    ("elsewhere east of 60 E", (lo > 60)), ("west of 60 E", lo <= 60)]
        else:
            regs = [("Brazil-Paraguay-Uruguay-Argentina side (lon -60 to -30, lat -40 to -10)", (lo > -60) & (lo < -30) & (la > -40) & (la < -10)),
                    ("Bolivia and inland (lon -70 to -60, lat -30 to -8)", (lo > -70) & (lo <= -60) & (la > -30) & (la < -8)),
                    ("Ecuador, north Peru, south Colombia (lon -82 to -70, lat -10 to 3)", (lo > -82) & (lo < -70) & (la > -10) & (la < 3)),
                    ("elsewhere west of 30 W", lo < -30), ("east of 30 W", lo >= -30)]
        done = np.zeros_like(m)
        for rn, rm in regs:
            mm = m & rm & ~done
            print("    %-90s %7.2f million" % (rn, p[mm].sum() / 1e6))
            done |= mm
