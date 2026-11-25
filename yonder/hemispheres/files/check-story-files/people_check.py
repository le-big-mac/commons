"""Second reader's recount for the people section: shares, slivers and named cities.  usage: people_check.py GRID_DIR"""
import sys, numpy as np
g = sys.argv[1]
R = 6371.0088; KM = np.pi * R / 180
def load(name):
    a = np.load(f'{g}/{name}', mmap_mode='r'); return np.asarray(a, dtype=np.float64)
P20 = load('pop005.npy'); n, m = P20.shape; d = 180.0 / n
lat = -90 + d * (np.arange(n) + 0.5); lon = -180 + d * (np.arange(m) + 0.5)
def cell(P, la_, lo_, r=3):
    i, j = int((la_ + 90) / d), int((lo_ + 180) / d); return P[i - r:i + r + 1, j - r:j + r + 1].sum()
print('grid', P20.shape, 'total 2020', f'{P20.sum():,.0f}')
print('orientation test (people within 0.35 degree): Delhi', f'{cell(P20, 28.6, 77.2):,.0f}', 'same latitude south', f'{cell(P20, -28.6, 77.2):,.0f}', 'Sao Paulo', f'{cell(P20, -23.55, -46.63):,.0f}', 'Tokyo', f'{cell(P20, 35.69, 139.69):,.0f}')
assert cell(P20, 28.6, 77.2) > 5e6 and cell(P20, -28.6, 77.2) == 0 and cell(P20, -23.55, -46.63) > 5e6
la = np.radians(lat)[:, None]; lo = np.radians(lon)[None, :]
def half(c):
    a, b = np.radians(c[0]), np.radians(c[1])
    return np.sin(a) * np.sin(la) + np.cos(a) * np.cos(la) * np.cos(lo - b) > 0
def ang(c, p):
    a, b, x, y = map(np.radians, (c[0], c[1], p[0], p[1]))
    return float(np.degrees(np.arccos(np.sin(a) * np.sin(x) + np.cos(a) * np.cos(x) * np.cos(y - b))))
BER = (52.369, 12.679); ALP = (46.0, 7.18); ALP10 = (45.05, 6.69); ALP00 = (44.35, 7.28); PAL = (49.37, 12.38); LANDC = (40.8195, 1.7243); BER15 = (52.06, 12.79)
HB, HA, HL = half(BER), half(ALP), half(LANDC)
print(f'2020: share in the half centred at {BER}: {100 * P20[HB].sum() / P20.sum():.3f}%; at the Alpine point {ALP}: {100 * P20[HA].sum() / P20.sum():.3f}%; in the half with the most land: {100 * P20[HL].sum() / P20.sum():.3f}%')
for nm, c in (('2010 Alpine summit', ALP10), ('2000 Alpine summit', ALP00), ('Upper Palatinate', PAL)):
    print(f'   2020 share at {nm} {c}: {100 * P20[half(c)].sum() / P20.sum():.3f}%')
print('centre of the people half to the middle of Berlin (52.52, 13.405):', round(ang(BER, (52.52, 13.405)) * KM), 'km; bearing: it is', round((13.405 - 12.679) * np.cos(np.radians(52.45)) * 111.2), 'km west and', round((52.52 - 52.369) * 111.2), 'km south of it; to Brandenburg an der Havel (52.41, 12.56)', round(ang(BER, (52.41, 12.56)) * KM), 'km; 2015 Brandenburg summit to Berlin', round(ang(BER15, (52.52, 13.405)) * KM), 'km')
print('Alpine points to: Lausanne', round(ang(ALP, (46.52, 6.63)) * KM), 'Sion', round(ang(ALP, (46.23, 7.36)) * KM), '; 2010 summit to Turin', round(ang(ALP10, (45.07, 7.69)) * KM), 'to Briancon', round(ang(ALP10, (44.9, 6.64)) * KM), '; 2000 summit to Cuneo', round(ang(ALP00, (44.39, 7.55)) * KM), 'km')
print('Upper Palatinate point 49.37, 12.38: to Regensburg', round(ang(PAL, (49.02, 12.10)) * KM), 'km, to Weiden', round(ang(PAL, (49.68, 12.16)) * KM), 'km, to the Czech border town Furth im Wald (49.31, 12.84)', round(ang(PAL, (49.31, 12.84)) * KM), 'km')
print('Berlin summit to Alpine points: ', round(ang(BER, ALP) * KM), round(ang(BER, ALP10) * KM), round(ang(BER, ALP00) * KM), 'km; to Upper Palatinate', round(ang(BER, PAL) * KM))
places = {'Manila': (14.6, 120.98), 'Kuala Lumpur': (3.14, 101.69), 'Singapore': (1.35, 103.82), 'Sao Paulo': (-23.55, -46.63), 'Rio de Janeiro': (-22.91, -43.17), 'Curitiba': (-25.43, -49.27), 'Porto Alegre': (-30.03, -51.23), 'Florianopolis': (-27.6, -48.55),
          'Belo Horizonte': (-19.92, -43.94), 'Lima': (-12.05, -77.04), 'Quito': (-0.18, -78.47), 'Guayaquil': (-2.19, -79.89), 'Santa Cruz (Bolivia)': (-17.8, -63.18), 'La Paz': (-16.5, -68.15), 'Asuncion': (-25.26, -57.58), 'Medan': (3.59, 98.67), 'Pekanbaru (mid Sumatra)': (0.51, 101.45), 'Jakarta': (-6.2, 106.85), 'Cebu': (10.32, 123.9), 'Davao': (7.07, 125.6), 'Ho Chi Minh City': (10.82, 106.63), 'Taipei': (25.03, 121.57), 'Tokyo': (35.69, 139.69), 'Osaka': (34.69, 135.5), 'Bogota': (4.71, -74.07), 'Cali': (3.45, -76.53)}
print('places: degrees from the Berlin-side centre, from the Alpine centre (46.0, 7.18), from the 2010 Alpine summit (45.05, 6.69)')
for k, p in places.items():
    a, b, c = ang(BER, p), ang(ALP, p), ang(ALP10, p)
    st = 'both' if a < 90 and b < 90 else 'neither' if a >= 90 and b >= 90 else 'Berlin half only' if a < 90 else 'Alpine half only'
    print(f'    {k:26s} {a:7.2f} {b:7.2f} {c:7.2f}   {st}')
LA, LO = np.meshgrid(lat, lon, indexing='ij')
def slivers(P, yr):
    onlyB = HB & ~HA; onlyA = HA & ~HB
    print(f'{yr}: total {P.sum() / 1e9:.3f} billion; only in the Berlin half {P[onlyB].sum() / 1e6:.1f} million; only in the Alpine half {P[onlyA].sum() / 1e6:.1f} million')
    reg = {'Philippines (4-22N, 116-128E)': (LA > 4) & (LA < 22) & (LO > 116) & (LO < 128), 'Malay Peninsula and Singapore (0.8-8N, 99-105E)': (LA > 0.8) & (LA < 8) & (LO > 99) & (LO < 105),
           'Sumatra (6S-6N, 94-106E, not the peninsula box)': (LA > -6.5) & (LA < 6) & (LO > 94) & (LO < 106.5) & ~((LA > 0.8) & (LA < 8) & (LO > 99) & (LO < 105)),
           'Borneo (5S-8N, 108-120E)': (LA > -5) & (LA < 8) & (LO > 108) & (LO < 120), 'elsewhere east of 60E': (LO > 60)}
    rest = onlyB.copy(); 
    for k, s in reg.items():
        v = P[onlyB & s & rest].sum(); rest &= ~s
        if v > 1e5: print(f'      Berlin only, {k}: {v / 1e6:.1f} M')
    print(f'      Berlin only, anywhere else: {P[rest].sum() / 1e6:.2f} M')
    regA = {'south and south-east Brazil with Paraguay east and Uruguay north (35S-10S, 60W-34W)': (LA > -35) & (LA < -10) & (LO > -60) & (LO < -34),
            'Bolivia and around (25S-9S, 70W-60W)': (LA > -25) & (LA < -9) & (LO > -70) & (LO <= -60), 'Ecuador, Peru, Colombia side (20S-5N, 82W-70W)': (LA > -20) & (LA < 5) & (LO > -82) & (LO <= -70), 'elsewhere west of 30W': (LO < -30)}
    rest = onlyA.copy()
    for k, s in regA.items():
        v = P[onlyA & s & rest].sum(); rest &= ~s
        if v > 1e5: print(f'      Alpine only, {k}: {v / 1e6:.1f} M')
    print(f'      Alpine only, anywhere else: {P[rest].sum() / 1e6:.2f} M')
slivers(P20, 2020)
del P20
slivers(load('pop005_1975.npy'), 1975)
