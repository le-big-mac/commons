"""agent3's own check of four numbers a prior-art reader gave (26 Nov 2026), with a hard edge on the 0.05-degree grids
and none of the reader's code: (1) the share of people, in the 2000 grid, of the half centred on Rankin's point 46.5 N, 7 E;
(2) the share, in the 2020 grid, of the half centred on Nantes (47.22 N, 1.55 W) and on the Catalan summit of the land;
(3) the distance from Rankin's point to my 2020 centre; (4) which named places are outside the best woodpecker half.
usage: own_check.py GRID_DIR"""
import sys, numpy as np
g = sys.argv[1]
lat = np.radians(-90 + (np.arange(3600) + 0.5) * 0.05); lon = np.radians(-180 + (np.arange(7200) + 0.5) * 0.05)
def unit(la, lo):
    la, lo = np.radians(la), np.radians(lo); return np.array([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)])
def share(pop, la, lo):
    c = unit(la, lo)
    dot = (np.cos(lat)[:, None] * np.cos(lon)[None, :]) * c[0] + (np.cos(lat)[:, None] * np.sin(lon)[None, :]) * c[1] + np.sin(lat)[:, None] * c[2]
    return float(pop[dot > 0].sum() / pop.sum())
def deg(a, b): return float(np.degrees(np.arccos(np.clip(unit(*a) @ unit(*b), -1, 1))))
p2000 = np.load(f'{g}/pop005_2000.npy'); p2020 = np.load(f'{g}/pop005.npy')
print('2000 grid: half centred on Rankin 46.5 N, 7.0 E   %.3f%%' % (100 * share(p2000, 46.5, 7.0)))
print('2000 grid: half centred on 44.3 N, 7.3 E (my best)  %.3f%%' % (100 * share(p2000, 44.3, 7.3)))
print('2020 grid: half centred on 52.37 N, 12.68 E         %.3f%%' % (100 * share(p2020, 52.37, 12.68)))
print('2020 grid: half centred on Nantes 47.22 N, 1.55 W   %.3f%%' % (100 * share(p2020, 47.22, -1.55)))
print('2020 grid: half centred on 40.82 N, 1.72 E (Catalan) %.3f%%' % (100 * share(p2020, 40.82, 1.72)))
print('Rankin 46.5 N, 7 E to 52.37 N, 12.68 E: %.0f km' % (deg((46.5, 7.0), (52.37, 12.68)) * np.pi * 6371.0088 / 180))
W = (43.0, -0.9)
for name, ll in (('Hong Kong', (22.32, 114.17)), ('Guangzhou', (23.13, 113.26)), ('Fuzhou', (26.07, 119.30)), ('Haikou', (20.04, 110.34)), ('Da Nang', (16.05, 108.21)),
                 ('Phnom Penh', (11.56, 104.92)), ('Ho Chi Minh City', (10.82, 106.63)), ('Shanghai', (31.23, 121.47)), ('Hanoi', (21.03, 105.85)), ('Beijing', (39.90, 116.40)),
                 ('Lima', (-12.05, -77.04)), ('Santiago', (-33.45, -70.67)), ('Buenos Aires', (-34.60, -58.38))):
    d = deg(W, ll); print('  %-18s %6.2f deg from 43.0 N, 0.9 W: %s' % (name, d, 'inside' if d < 90 else 'OUTSIDE'))
