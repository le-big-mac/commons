"""Second reader: for each year tried, the share of people in halves centred at the three regional summits of the fold's table
(hard edge, 0.05-degree cells), and the best centre on a plain half-degree lattice over Europe (36-64 N, 6 W-30 E).
A rough check of which region leads in which year; it does not repeat the author's fine search.   usage: epochs_check.py GRID_DIR"""
import sys, numpy as np
g = sys.argv[1]
files = {1975: 'pop005_1975.npy', 2000: 'pop005_2000.npy', 2005: 'pop005_2005.npy', 2010: 'pop005_2010.npy', 2015: 'pop005_2015.npy', 2020: 'pop005.npy', 2025: 'pop005_2025.npy', 2030: 'pop005_2030.npy'}
table = {1975: ((46.01, 7.17), (49.31, 12.38), (51.78, 12.31)), 2000: ((44.35, 7.28), (49.33, 12.40), (51.82, 12.63)), 2005: ((44.35, 7.28), (49.34, 12.40), (52.04, 12.77)),
         2010: ((45.05, 6.69), (49.36, 12.38), (52.04, 12.77)), 2015: ((45.05, 6.69), (49.37, 12.38), (52.07, 12.79)), 2020: ((45.05, 6.69), (49.37, 12.38), (52.37, 12.68)),
         2025: ((45.05, 6.69), (49.38, 12.38), (52.26, 12.77)), 2030: ((45.04, 6.69), (49.38, 12.38), (52.26, 12.78))}
def unit(lat, lon):
    la, lo = np.radians(lat), np.radians(lon)
    return np.stack([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)], -1)
n, m = 3600, 7200; d = 0.05
lat = -90 + d * (np.arange(n) + 0.5); lon = -180 + d * (np.arange(m) + 0.5)
clat = np.arange(36.0, 64.01, 0.5); clon = np.arange(-6.0, 30.01, 0.5)
CLA, CLO = np.meshgrid(clat, clon, indexing='ij'); C = unit(CLA.ravel(), CLO.ravel()).astype(np.float32)
for yr, f in files.items():
    P = np.asarray(np.load(f'{g}/{f}', mmap_mode='r'), dtype=np.float64)
    tot = P.sum()
    ii, jj = np.nonzero(P); w = P[ii, jj]; X = unit(lat[ii], lon[jj]).astype(np.float32)
    row = []
    for p in table[yr]:
        s = w[(X @ unit(*p).astype(np.float32)) > 0].sum() / tot; row.append(100 * s)
    # only cells within 35 degrees of the dividing circles of the lattice's centres can change sides: all centres lie within 25 degrees of 50 N, 12 E
    d0 = X @ unit(50.0, 12.0).astype(np.float32); t0 = np.degrees(np.arccos(np.clip(d0, -1, 1)))
    always = t0 < 90 - 26; band = np.abs(t0 - 90) <= 26
    base = w[always].sum(); Xb = X[band]; wb = w[band]
    S = np.empty(len(C))
    for a in range(0, len(C), 64):
        D = Xb @ C[a:a + 64].T
        S[a:a + 64] = (base + (wb[:, None] * (D > 0)).sum(axis=0)) / tot
    k = int(np.argmax(S)); order = np.argsort(S)[::-1][:5]
    lead = ('western Alps', 'Upper Palatinate', 'west of Berlin')[int(np.argmax(row))]
    print(f'{yr}: {tot / 1e9:.3f} billion; Alps {row[0]:.3f}%  Palatinate {row[1]:.3f}%  Berlin side {row[2]:.3f}%  -> {lead} leads by {sorted(row)[-1] - sorted(row)[-2]:.3f} points; '
          f'best on the half-degree lattice {100 * S[k]:.3f}% at {CLA.ravel()[k]:.1f} N, {CLO.ravel()[k]:.1f} E; next: ' + '; '.join(f'{100 * S[o]:.3f}% at {CLA.ravel()[o]:.1f}, {CLO.ravel()[o]:.1f}' for o in order[1:4]), flush=True)
    del P, X, w
