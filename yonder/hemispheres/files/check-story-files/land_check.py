"""Second reader's own recount, from the 0.05-degree land grid, of what changes sides between the two summits.
usage: land_check.py GRID_DIR"""
import sys, numpy as np
from scipy import ndimage
g = sys.argv[1]
land = np.load(f'{g}/land10.npy', mmap_mode='r')
n, m = land.shape; d = 180.0 / n
print('grid', land.shape, land.dtype, 'cell', d)
land = np.asarray(land, dtype=np.float64)
lat = -90 + d * (np.arange(n) + 0.5); lon = -180 + d * (np.arange(m) + 0.5)
R = 6371.0088
band = R * R * np.radians(d) * (np.sin(np.radians(lat + d / 2)) - np.sin(np.radians(lat - d / 2)))
# orientation: with row 0 at the south, 25 N 10 E (Sahara) is land and 25 S 10 E (Atlantic) is sea; 40 N 140 W is sea and 40 N 100 W is land
def cell(la_, lo_): return land[int((la_ + 90) / d), int((lo_ + 180) / d)]
print('orientation test: Sahara', cell(25, 10), 'Atlantic off Namibia', cell(-25, 10), 'Kansas', cell(40, -100), 'Pacific', cell(40, -140), 'Australia', cell(-25, 135))
assert cell(25, 10) == 1 and cell(-25, 10) == 0 and cell(40, -100) == 1 and cell(40, -140) == 0 and cell(-25, 135) == 1
w = land * band[:, None]
tot = w.sum(); print(f'total land {tot:,.0f} km2')
la = np.radians(lat)[:, None]; lo = np.radians(lon)[None, :]
def cosd(c):
    a, b = np.radians(c[0]), np.radians(c[1])
    return np.sin(a) * np.sin(la) + np.cos(a) * np.cos(la) * np.cos(lo - b)
CAT = (40.8195, 1.7243); BRE = (47.42, -2.3596)
A = cosd(CAT) > 0; B = cosd(BRE) > 0
print(f'Catalan half {w[A].sum():,.0f} km2 = {100 * w[A].sum() / tot:.4f}%; Breton half {w[B].sum():,.0f} = {100 * w[B].sum() / tot:.4f}%; difference {w[A].sum() - w[B].sum():,.0f}')
print(f'land as a share of each half\'s surface: {100 * w[A].sum() / (2 * np.pi * R * R):.1f}%')
gain = A & ~B; lose = B & ~A
print(f'taken in (Catalan only) {w[gain].sum():,.0f}; given up (Breton only) {w[lose].sum():,.0f}; net {w[gain].sum() - w[lose].sum():,.0f}; net as a share of the smaller {100 * (w[gain].sum() - w[lose].sum()) / w[lose].sum():.1f}%')
LA, LO = np.meshgrid(lat, lon, indexing='ij')
def box(s, w_, n_, e):
    return (LA >= s) & (LA < n_) & (LO >= w_) & (LO < e)
def rep(name, sel):
    v = w[sel].sum()
    if v > 0:
        ys, xs = np.where(sel & (land > 0))
        print(f'    {name}: {v:,.0f} km2; lat {lat[ys].min():.1f} to {lat[ys].max():.1f}, lon {lon[xs].min():.1f} to {lon[xs].max():.1f}')
    else:
        print(f'    {name}: 0')
print('given up, by region:')
rep('Japan (30-46N, 128-146E)', lose & box(30, 128, 46, 146))
rep('Korea (33-39N, 124-130E)', lose & box(33, 124, 39, 130) & ~box(30, 128, 46, 146))
rep('Taiwan (21.5-25.5N, 119.9-122.2E)', lose & box(21.5, 119.9, 25.5, 122.2))
rep('Hainan (18-20.3N, 108.5-111.2E)', lose & box(18, 108.5, 20.3, 111.2))
rep('rest of East Asia mainland and islands (16-46N, 100-128E, not Taiwan, not Hainan)', lose & box(16, 100, 46, 128) & ~box(21.5, 119.9, 25.5, 122.2) & ~box(18, 108.5, 20.3, 111.2))
rep('Vietnam etc south of 16N (0-16N, 100-112E)', lose & box(0, 100, 16, 112))
rep('Americas, Pacific side (60S-35N, 125W-70W)', lose & box(-60, -125, 35, -70))
rep('  of which Galapagos (2S-2N, 93-88W)', lose & box(-2, -93, 2, -88))
rep('  of which Peru-Chile coast (25S-0, 82-68W)', lose & box(-25, -82, 0, -68))
rep('  of which Mexico (15-33N, 120-100W)', lose & box(15, -120, 33, -100))
rep('everything else', lose & ~box(16, 100, 46, 146) & ~box(0, 100, 16, 112) & ~box(-60, -125, 35, -70))
print('taken in, by region:')
rep('South America (60S-0, 82W-34W)', gain & box(-60, -82, 0, -34))
rep('South-east Asia (10S-25N, 90-112E)', gain & box(-10, 90, 25, 112))
rep('  of which Sumatra and islands (6S-6.2N, 94-100E... south of 6.2N, west of 99.5E)', gain & box(-6, 94, 6.2, 99.5))
rep('  of which north of 16N', gain & box(16, 90, 25, 112))
rep('everything else', gain & ~box(-60, -82, 0, -34) & ~box(-10, 90, 25, 112))

# the islands of Japan by connected pieces of the grid
sub = (slice(int((30 + 90) / d), int((46 + 90) / d)), slice(int((128 + 180) / d), int((146.5 + 180) / d)))
L = land[sub] > 0.5
lab, k = ndimage.label(L)
sizes = ndimage.sum(w[sub], lab, index=np.arange(1, k + 1))
order = np.argsort(sizes)[::-1][:6]
print('Japan: the largest connected pieces of the grid (cells more than half land)')
for o in order:
    sel = lab == o + 1
    ys, xs = np.where(sel)
    area_full = w[sub][sel].sum()
    in_lose = w[sub][sel & lose[sub]].sum(); in_both = w[sub][sel & (A & B)[sub]].sum(); in_none = w[sub][sel & (~A & ~B)[sub]].sum(); in_gain = w[sub][sel & gain[sub]].sum()
    print(f'    piece of {area_full:,.0f} km2 (lat {lat[sub[0]][ys].min():.1f}-{lat[sub[0]][ys].max():.1f}, lon {lon[sub[1]][xs].min():.1f}-{lon[sub[1]][xs].max():.1f}): '
          f'given up {in_lose:,.0f} ({100 * in_lose / area_full:.0f}%), in both halves {in_both:,.0f} ({100 * in_both / area_full:.0f}%), in neither {in_none:,.0f} ({100 * in_none / area_full:.0f}%), taken in {in_gain:,.0f}')

# named places against the two halves
def ang(c, p):
    a, b, x, y = map(np.radians, (c[0], c[1], p[0], p[1]))
    return float(np.degrees(np.arccos(np.sin(a) * np.sin(x) + np.cos(a) * np.cos(x) * np.cos(y - b))))
places = {'Tokyo': (35.6895, 139.6917), 'Osaka': (34.69, 135.50), 'Nagoya': (35.18, 136.91), 'Hiroshima': (34.39, 132.46), 'Sendai': (38.27, 140.87), 'Niigata': (37.92, 139.04), 'Aomori': (40.82, 140.74),
          'Kochi (Shikoku)': (33.56, 133.53), 'Fukuoka (Kyushu)': (33.59, 130.40), 'Kagoshima (Kyushu)': (31.60, 130.56), 'Sapporo': (43.06, 141.35), 'Taipei': (25.03, 121.57),
          'Ningbo': (29.87, 121.55), 'Wenzhou': (28.0, 120.67), 'Fuzhou': (26.07, 119.30), 'Xiamen': (24.48, 118.09), 'Hong Kong': (22.32, 114.17), 'Guangzhou': (23.13, 113.26), 'Shanghai': (31.23, 121.47), 'Haikou (Hainan)': (20.04, 110.34), 'Sanya (Hainan)': (18.25, 109.51),
          'Banda Aceh (Sumatra)': (5.55, 95.32), 'Medan': (3.59, 98.67), 'Phuket': (7.88, 98.39), 'Bangkok': (13.75, 100.5), 'Phnom Penh': (11.56, 104.92), 'Siem Reap': (13.36, 103.86), 'Ho Chi Minh City': (10.82, 106.63),
          'Resistencia (Chaco)': (-27.45, -58.99), 'Salta': (-24.79, -65.41), 'Jujuy': (-24.19, -65.30), 'Corrientes': (-27.47, -58.83), 'Asuncion': (-25.26, -57.58), 'Salto (N Uruguay)': (-31.38, -57.96), 'Rivera (N Uruguay)': (-30.9, -55.55), 'Montevideo': (-34.9, -56.16), 'Buenos Aires': (-34.6, -58.38), 'Porto Alegre': (-30.03, -51.23), 'Santa Cruz (Bolivia)': (-17.8, -63.18),
          'Lima': (-12.05, -77.04), 'Pisco': (-13.71, -76.2), 'Arica': (-18.48, -70.31), 'Puerto Ayora (Galapagos)': (-0.74, -90.31), 'Cabo San Lucas': (22.89, -109.92), 'La Paz (Baja)': (24.14, -110.31)}
print('places: degrees from the Catalan and the Breton summit (inside a half if under 90)')
for k_, p in places.items():
    a, b = ang(CAT, p), ang(BRE, p)
    st = 'both' if a < 90 and b < 90 else 'neither' if a >= 90 and b >= 90 else 'GIVEN UP (Breton only)' if b < 90 else 'TAKEN IN (Catalan only)'
    print(f'    {k_:28s} {a:7.2f} {b:7.2f}  {st}')
print('distances: Catalan summit to Tarragona', round(ang(CAT, (41.1189, 1.2445)) * np.pi * R / 180, 1), 'km; Breton summit to Nantes', round(ang(BRE, (47.2184, -1.5536)) * np.pi * R / 180, 1), 'to Ile Dumet', round(ang(BRE, (47.4117, -2.6208)) * np.pi * R / 180, 1), '; the two summits', round(ang(CAT, BRE) * np.pi * R / 180, 1))
