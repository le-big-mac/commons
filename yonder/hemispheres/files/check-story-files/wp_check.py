"""Second reader: the woodpecker share at the stated centre, from the saved weights (one unit per species, spread evenly over its 5-degree boxes)."""
import sys, numpy as np
wg = np.load(sys.argv[1]); print('weights', wg.shape, 'sum (number of species)', round(float(wg.sum()), 3))
def unit(lat, lon):
    la, lo = np.radians(lat), np.radians(lon)
    return np.stack([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)], -1)
c = unit(43.0, -0.9)
lat = -87.5 + 5 * np.arange(36); lon = -177.5 + 5 * np.arange(72)
LA, LO = np.meshgrid(lat, lon, indexing='ij')
hard = (unit(LA, LO) @ c) > 0
print(f'box counted whole by its centre: {100 * wg[hard].sum() / wg.sum():.2f}%')
# box counted by the fraction of its area inside the half (50 x 50 sub-cells, weighted by cos latitude)
k = 50; sub = (np.arange(k) + 0.5) / k * 5 - 2.5
frac = np.zeros_like(wg)
for i in range(36):
    for j in range(72):
        if wg[i, j] == 0: continue
        la = lat[i] + sub[:, None]; lo = lon[j] + sub[None, :]
        la2, lo2 = np.broadcast_arrays(la, lo)
        ins = (unit(la2, lo2) @ c) > 0; wt = np.cos(np.radians(la2))
        frac[i, j] = (ins * wt).sum() / wt.sum()
print(f'box counted by the part of its area inside: {100 * (wg * frac).sum() / wg.sum():.2f}%')
west = LO < -30; mid = (LO >= -30) & (LO < 60); east = LO >= 60
print(f'weights by sector: west of 30 W {100 * wg[west].sum() / wg.sum():.1f}%, 30 W to 60 E {100 * wg[mid].sum() / wg.sum():.1f}%, east of 60 E {100 * wg[east].sum() / wg.sum():.1f}%')
print(f'outside the half (by centre): Asia and beyond {100 * wg[~hard & east].sum() / wg.sum():.1f}%, Americas {100 * wg[~hard & west].sum() / wg.sum():.1f}%, middle {100 * wg[~hard & mid].sum() / wg.sum():.1f}%')
sa = west & (LA < 13) & (LO > -82) & (LO < -34)
print(f'South America boxes (south of 13 N, 82 W to 34 W): {100 * wg[sa].sum() / wg.sum():.1f}% of the total, of which inside the half {100 * wg[sa & hard].sum() / wg[sa].sum():.0f}%')
trop_asia = east & (LA < 23.5) & (LA > -12) & (LO < 130)
print(f'tropical Asia boxes (12 S to 23.5 N, 60 E to 130 E): {100 * wg[trop_asia].sum() / wg.sum():.1f}% of the total, of which inside the half {100 * wg[trop_asia & hard].sum() / wg[trop_asia].sum():.0f}%')
def ang(p, q=(43.0, -0.9)):
    return float(np.degrees(np.arccos(np.clip(unit(*p) @ unit(*q), -1, 1))))
for name, p in (('Chennai', (13.08, 80.27)), ('Kanyakumari', (8.08, 77.54)), ('Kolkata', (22.57, 88.36)), ('Kathmandu', (27.7, 85.32)), ('east end of the Himalaya (Namcha Barwa)', (29.63, 95.06)), ('Kunming', (25.04, 102.71)),
                ('Beijing', (39.9, 116.4)), ('Shanghai', (31.23, 121.47)), ('Guangzhou', (23.13, 113.26)), ('Hong Kong', (22.32, 114.17)), ('Fuzhou', (26.07, 119.3)), ('Haikou', (20.04, 110.34)), ('Taipei', (25.03, 121.57)),
                ('Bangkok', (13.75, 100.5)), ('Hanoi', (21.03, 105.85)), ('Ho Chi Minh City', (10.82, 106.63)), ('Kuala Lumpur', (3.14, 101.69)), ('Singapore', (1.35, 103.82)), ('Medan (Sumatra)', (3.59, 98.67)), ('Jakarta', (-6.2, 106.85)), ('Kuching (Borneo)', (1.55, 110.35)), ('Manila', (14.6, 120.98)),
                ('Bogota', (4.71, -74.07)), ('Manaus', (-3.1, -60.02)), ('Lima', (-12.05, -77.04)), ('Sao Paulo', (-23.55, -46.63)), ('Asuncion', (-25.26, -57.58)), ('Buenos Aires', (-34.6, -58.38)), ('Santiago', (-33.45, -70.67)), ('La Paz', (-16.5, -68.15))):
    for q, qn in (((43.0, -0.9), 'woodpecker centre'), ((48.86, 2.35), 'Paris'), ((40.42, -3.70), 'Madrid'), ((52.52, 13.40), 'Berlin')):
        pass
    print(f'   {name:42s} {ang(p):6.1f} deg from the woodpecker centre; Paris {ang(p, (48.86, 2.35)):6.1f}; Madrid {ang(p, (40.42, -3.70)):6.1f}; Lisbon {ang(p, (38.72, -9.14)):6.1f}')
# what is antipodal to South America: antipode of Manaus, Lima, Asuncion, Bogota
for name, p in (('Bogota', (4.71, -74.07)), ('Manaus', (-3.1, -60.02)), ('Lima', (-12.05, -77.04)), ('Asuncion', (-25.26, -57.58)), ('Quito', (-0.18, -78.47)), ('Sao Paulo', (-23.55, -46.63))):
    print(f'   antipode of {name}: {-p[0]:.1f} N, {p[1] + 180:.1f} E')
print('Gascony point 43.0 N 0.9 W: km to Larrau (43.02, -0.95)', round(ang((43.02, -0.95)) * 111.19), ', Pau (43.30, -0.37)', round(ang((43.30, -0.37)) * 111.19), ', Auch (43.65, 0.59)', round(ang((43.65, 0.59)) * 111.19), ', Oloron (43.19, -0.61)', round(ang((43.19, -0.61)) * 111.19))
