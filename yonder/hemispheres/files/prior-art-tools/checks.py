"""Checks on the 0.05-degree population grids of the study (read only).

usage: python -I checks.py GRID_DIR

GRID_DIR holds pop005.npy (2020) and pop005_YYYY.npy; row 0 is the southernmost band, column 0 starts at -180.
A cell counts by its centre, with a hard edge at 90 degrees on a sphere (the study uses a ramp one cell wide,
so shares here can differ from its figures in the third decimal).
"""
import sys, os
import numpy as np

D = sys.argv[1]
CELL = 0.05
H, W = 3600, 7200
lat = -90 + (np.arange(H) + 0.5) * CELL
lon = -180 + (np.arange(W) + 0.5) * CELL
LAT, LON = np.meshgrid(np.radians(lat), np.radians(lon), indexing="ij")
X = np.cos(LAT) * np.cos(LON)
Y = np.cos(LAT) * np.sin(LON)
Z = np.sin(LAT)

def unit(la, lo):
    la, lo = np.radians(la), np.radians(lo)
    return np.array([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)])

def inside(c):
    u = unit(*c)
    return (X * u[0] + Y * u[1] + Z * u[2]) > 0

def load(year):
    name = "pop005.npy" if year == 2020 else "pop005_%d.npy" % year
    return np.load(os.path.join(D, name))

def ang(a, b):
    return float(np.degrees(np.arccos(np.clip(unit(*a) @ unit(*b), -1, 1))))

BERLIN = (52.37, 12.68)      # study's 2020 centre
VALAIS = (46.0, 7.18)        # study's Alpine centre used for the slivers
ALP2010 = (45.1, 6.7)        # study's Alpine summit 2010-2020
ALP2000 = (44.3, 7.3)        # study's best centre in the 2000 grid
RANKIN = (46.5, 7.0)         # Rankin's stated centre ("roughly 46.5 N, 7 E")
NANTES = (47.217, -1.533)
CATALAN = (40.82, 1.72)

print("== distances between centres, km on a sphere of 6371.0088 km")
for n1, a, n2, b in [("Rankin", RANKIN, "study 2020", BERLIN), ("Rankin", RANKIN, "study 2000 best", ALP2000),
                     ("Rankin", RANKIN, "Valais summit", VALAIS), ("Alpine 45.1,6.7", ALP2010, "study 2020", BERLIN),
                     ("Valais", VALAIS, "study 2020", BERLIN)]:
    print("  %-16s to %-16s %7.0f km" % (n1, n2, ang(a, b) * np.pi / 180 * 6371.0088))

print("== share of people in the half centred on named points, by grid")
for year in (1975, 2000, 2005, 2010, 2015, 2020, 2025, 2030):
    p = load(year)
    tot = p.sum()
    row = ["%d total %.3f bn" % (year, tot / 1e9)]
    for name, c in [("Rankin 46.5,7.0", RANKIN), ("Valais 46.0,7.18", VALAIS), ("study2000 44.3,7.3", ALP2000),
                    ("Berlin 52.37,12.68", BERLIN), ("Nantes", NANTES), ("Catalan", CATALAN)]:
        row.append("%s %.3f%%" % (name, 100 * p[inside(c)].sum() / tot))
    print("  " + " | ".join(row))

print("== 2020: people outside the half centred at 52.37 N, 12.68 E, between 30 W and 60 E")
p = load(2020)
out = ~inside(BERLIN)
band = (np.degrees(LON) >= -30) & (np.degrees(LON) < 60)
m = out & band & (p > 0)
print("  cells with people: %d, people: %.1f" % (m.sum(), p[m].sum()))
ii, jj = np.nonzero(m)
for i, j in zip(ii, jj):
    print("    lat %.3f lon %.3f people %.1f  distance from centre %.2f deg" % (lat[i], lon[j], p[i, j], ang(BERLIN, (lat[i], lon[j]))))
# everything populated near Tristan da Cunha and Gough, inside or outside
box = (np.degrees(LAT) > -41) & (np.degrees(LAT) < -36.5) & (np.degrees(LON) > -13.5) & (np.degrees(LON) < -9) & (p > 0)
print("  all populated cells in 41-36.5 S, 13.5-9 W: %d cells, %.1f people" % (box.sum(), p[box].sum()))
for name, lo, hi in [("Americas 170W-30W", -170, -30), ("Africa+Europe 30W-60E", -30, 60)]:
    b = (np.degrees(LON) >= lo) & (np.degrees(LON) < hi)
    print("  %s: %.1f million, outside %.3f million" % (name, p[b].sum() / 1e6, p[b & out].sum() / 1e6))
b = ~((np.degrees(LON) >= -170) & (np.degrees(LON) < 60))
print("  Asia+Oceania 60E-170W: %.1f million, outside %.3f million" % (p[b].sum() / 1e6, p[b & out].sum() / 1e6))

print("== named places: angular distance (deg) from each centre; under 90 is inside")
places = [("Manila", 14.60, 120.98), ("Kuala Lumpur", 3.14, 101.69), ("Singapore", 1.35, 103.82),
          ("Padang (W Sumatra)", -0.95, 100.35), ("Pekanbaru (mid Sumatra)", 0.51, 101.45), ("Medan", 3.59, 98.67),
          ("Palembang", -2.99, 104.76), ("Jakarta", -6.2, 106.85), ("Ho Chi Minh City", 10.8, 106.7), ("Cebu", 10.3, 123.9), ("Davao", 7.07, 125.6),
          ("Sao Paulo", -23.55, -46.63), ("Rio de Janeiro", -22.91, -43.2), ("Curitiba", -25.43, -49.27),
          ("Porto Alegre", -30.03, -51.23), ("Quito", -0.18, -78.47), ("Guayaquil", -2.19, -79.89),
          ("Santa Cruz (Bolivia)", -17.8, -63.18), ("Lima", -12.05, -77.04), ("Buenos Aires", -34.6, -58.38),
          ("Tristan da Cunha", -37.07, -12.31), ("Cape Agulhas", -34.83, 20.0), ("Tokyo", 35.68, 139.69), ("Taipei", 25.03, 121.57)]
print("  %-24s %8s %8s %8s %8s %8s" % ("", "Berlin", "Valais", "45.1,6.7", "Rankin", "Catalan"))
for n, la, lo in places:
    print("  %-24s %8.2f %8.2f %8.2f %8.2f %8.2f" % (n, ang(BERLIN, (la, lo)), ang(VALAIS, (la, lo)), ang(ALP2010, (la, lo)), ang(RANKIN, (la, lo)), ang(CATALAN, (la, lo))))
