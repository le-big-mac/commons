"""After the reader of the public page (25 Nov): the land that changes sides between the Catalan and the Breton half,
by region, from the 0.05-degree land grid of the scored run. My own recount of the reader's lunes.out.
usage: traded.py GRID_DIR"""
import sys, numpy as np
g = sys.argv[1]
land = np.load(f'{g}/land10.npy')                    # 3600 x 7200 coverage fractions, row 0 at the south? (checked below)
n, m = land.shape; d = 180.0 / n
lat = -90 + d * (np.arange(n) + 0.5); lon = -180 + d * (np.arange(m) + 0.5)
R = 6371.0088
area = (R * R * np.radians(d) * (np.sin(np.radians(lat + d / 2)) - np.sin(np.radians(lat - d / 2))))[:, None] * np.ones(m)
tot = float((land * area).sum())
if not (146.0e6 < tot < 147.5e6): land = land[::-1]; tot = float((land * area).sum())
# orientation: Antarctica (land south of 70 S) must be large
assert float((land[lat < -70] * area[lat < -70]).sum()) > 5e6, 'grid upside down'
def inside(c):
    la0, lo0 = np.radians(c[0]), np.radians(c[1])
    la, lo = np.radians(lat)[:, None], np.radians(lon)[None, :]
    return (np.sin(la0) * np.sin(la) + np.cos(la0) * np.cos(la) * np.cos(lo - lo0)) > 0
A = inside((40.83, 1.72)); B = inside((47.42, -2.36))
w = land * area
print(f'land {tot:,.0f} km2; Catalan half {w[A].sum():,.0f}; Breton half {w[B].sum():,.0f}; difference {w[A].sum() - w[B].sum():,.0f}')
LA, LO = np.meshgrid(lat, lon, indexing='ij')
regions = [('East Asia (100E-150E, north of 16N)', (LO > 100) & (LO < 150) & (LA > 16)),
           ('Sumatra to Cambodia (90E-112E, south of 16N)', (LO > 90) & (LO < 112) & (LA <= 16)),
           ('South America east of the Andes and its Atlantic side (72W-30W, south of 15S)', (LO > -72) & (LO < -30) & (LA < -15)),
           ('Pacific coast of Peru (82W-72W, 20S-5S)', (LO > -82) & (LO <= -72) & (LA > -20) & (LA < -5)),
           ('Galapagos (93W-88W, 2S-2N)', (LO > -93) & (LO < -88) & (LA > -2) & (LA < 2)),
           ('Baja California and its islands (120W-105W, 15N-30N)', (LO > -120) & (LO < -105) & (LA > 15) & (LA < 30))]
for name, sel in (('only in the Catalan half (taken in)', A & ~B), ('only in the Breton half (given up)', B & ~A)):
    print(f'{name}: {w[sel].sum():,.0f} km2')
    rest = sel.copy()
    for rn, rs in regions:
        v = float(w[sel & rs].sum()); rest &= ~rs
        if v > 50: print(f'    {rn}: {v:,.0f}')
    print(f'    elsewhere: {w[rest].sum():,.0f}')
