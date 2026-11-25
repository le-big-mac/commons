"""How much of Honshu changes sides? Honshu is cut from Kyushu at the Kanmon strait by hand (the grid joins them)."""
import sys, numpy as np
from scipy import ndimage
g = sys.argv[1]
land = np.asarray(np.load(f'{g}/land10.npy', mmap_mode='r'), dtype=np.float64)
n, m = land.shape; d = 180.0 / n
lat = -90 + d * (np.arange(n) + 0.5); lon = -180 + d * (np.arange(m) + 0.5)
R = 6371.0088
band = R * R * np.radians(d) * (np.sin(np.radians(lat + d / 2)) - np.sin(np.radians(lat - d / 2)))
r0, r1 = int((30 + 90) / d), int((46 + 90) / d); c0, c1 = int((128 + 180) / d), int((146.5 + 180) / d)
L = land[r0:r1, c0:c1]; w = L * band[r0:r1, None]
la = np.radians(lat[r0:r1])[:, None]; lo = np.radians(lon[c0:c1])[None, :]
LA, LO = np.meshgrid(lat[r0:r1], lon[c0:c1], indexing='ij')
def half(c):
    a, b = np.radians(c[0]), np.radians(c[1])
    return np.sin(a) * np.sin(la) + np.cos(a) * np.cos(la) * np.cos(lo - b) > 0
A = half((40.8195, 1.7243)); B = half((47.42, -2.3596))
# cut the strait: remove cells in a thin window around Shimonoseki / Moji so that the two islands separate
cutmask = (LA > 33.85) & (LA < 34.02) & (LO > 130.85) & (LO < 131.05)
M = (L > 0.5) & ~cutmask
lab, k = ndimage.label(M)
sizes = ndimage.sum(w, lab, index=np.arange(1, k + 1))
for o in np.argsort(sizes)[::-1][:7]:
    sel = lab == o + 1
    # add back the partly-land cells touching this piece is not attempted: areas are of cells more than half land, weighted by coverage
    ys, xs = np.where(sel)
    a = w[sel].sum()
    print(f'piece {a:,.0f} km2, lat {LA[sel].min():.1f}-{LA[sel].max():.1f}, lon {LO[sel].min():.1f}-{LO[sel].max():.1f}: only in the Breton half {w[sel & B & ~A].sum():,.0f} ({100 * w[sel & B & ~A].sum() / a:.0f}%), in both {w[sel & A & B].sum():,.0f} ({100 * w[sel & A & B].sum() / a:.0f}%), in neither {w[sel & ~A & ~B].sum():,.0f} ({100 * w[sel & ~A & ~B].sum() / a:.0f}%)')
J = (LA < 45.6) & (LO > 128.5) & ~((LA > 34.5) & (LO < 130.0)) & ~((LA > 41.3) & (LO < 139.0)) & ~((LA>42.0)&(LO<139.5))
print(f'all of Japan in this window (roughly): land {w[J].sum():,.0f} km2, only in the Breton half {w[J & B & ~A].sum():,.0f} ({100*w[J & B & ~A].sum()/w[J].sum():.0f}%); south of Hokkaido (lat<41.6): land {w[J & (LA<41.6)].sum():,.0f}, only Breton {w[J & (LA<41.6) & B & ~A].sum():,.0f} ({100*w[J & (LA<41.6) & B & ~A].sum()/w[J & (LA<41.6)].sum():.0f}%)')
