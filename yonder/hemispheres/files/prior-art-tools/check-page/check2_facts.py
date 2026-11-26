"""Check 2: the facts behind the new sentences, counted again with code of my own.

usage: python -I check2_facts.py GRID_DIR LOG

GRID_DIR holds pop005.npy (2020) and pop005_2000.npy (0.05-degree grids, row 0 southernmost, column 0 at 180 W).
LOG is the searcher's fetch-log.txt.
A cell counts by its centre, hard edge at 90 degrees on a sphere.
"""
import sys, math
import numpy as np

G, LOG = sys.argv[1], sys.argv[2]

# ---- the log
kinds = {}
status = {}
for line in open(LOG, encoding="utf-8"):
    parts = [x.strip() for x in line.rstrip("\n").split("|")]
    if len(parts) < 2:
        continue
    kinds[parts[1]] = kinds.get(parts[1], 0) + 1
    if parts[1] == "FETCH":
        status[parts[4]] = status.get(parts[4], 0) + 1
print("log lines by kind:", kinds, "total", sum(kinds.values()))
print("fetches by status:", status)

# ---- shares
H, W = 3600, 7200
lat = np.radians(-90 + (np.arange(H) + 0.5) * 0.05)
lon = np.radians(-180 + (np.arange(W) + 0.5) * 0.05)
cl, sl = np.cos(lat), np.sin(lat)
co, so = np.cos(lon), np.sin(lon)

def share(pop, la, lo):
    la, lo = math.radians(la), math.radians(lo)
    # cos of angular distance = sin(lat)sin(la) + cos(lat)cos(la)cos(lon-lo)
    cosd = sl[:, None] * math.sin(la) + (cl[:, None] * math.cos(la)) * (co[None, :] * math.cos(lo) + so[None, :] * math.sin(lo))
    return 100.0 * float(pop[cosd > 0].sum(dtype=np.float64) / pop.sum(dtype=np.float64))

def dist_deg(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    c = math.sin(la1) * math.sin(la2) + math.cos(la1) * math.cos(la2) * math.cos(lo1 - lo2)
    return math.degrees(math.acos(max(-1, min(1, c))))

p2000 = np.load(G + "/pop005_2000.npy")
p2020 = np.load(G + "/pop005.npy")
print("totals: 2000 %.4f bn, 2020 %.4f bn" % (p2000.sum(dtype=np.float64) / 1e9, p2020.sum(dtype=np.float64) / 1e9))

print("== 2000 grid, Rankin's point and points around it ('roughly 46.5 N, 7 E')")
for la, lo in [(46.5, 7.0), (46.25, 7.0), (46.75, 7.0), (46.5, 6.5), (46.5, 7.5), (46.0, 7.18), (44.3, 7.3), (52.37, 12.68)]:
    print("   %6.2f N %6.2f E  %.3f%%" % (la, lo, share(p2000, la, lo)))
print("== 2000 grid, coarse search for the best centre, 0.5-degree steps over 40-56 N, 0-20 E")
best = []
for la in np.arange(40, 56.01, 0.5):
    for lo in np.arange(0, 20.01, 0.5):
        best.append((share(p2000, la, lo), la, lo))
best.sort(reverse=True)
for s, la, lo in best[:8]:
    print("   %.3f%% at %.1f N %.1f E, %.0f km from Rankin's point" % (s, la, lo, dist_deg((la, lo), (46.5, 7.0)) * math.pi / 180 * 6371.0088))

print("== 2020 grid, the half centred on Nantes, by choice of coordinates")
for name, la, lo in [("Nantes 47.22 N 1.55 W (own_check.py)", 47.22, -1.55), ("Nantes 47.217 N 1.533 W (checks.py)", 47.217, -1.533),
                     ("47 13' N 1 32' W", 47 + 13 / 60, -(1 + 32 / 60)), ("47.25 N 1.5 W", 47.25, -1.5), ("47.2 N 1.6 W", 47.2, -1.6),
                     ("Ile Dumet 47.41 N 2.62 W", 47.41, -2.62), ("northern summit of land 47.42 N 2.36 W", 47.42, -2.36),
                     ("Catalan summit 40.82 N 1.72 E", 40.82, 1.72), ("study's 2020 centre 52.37 N 12.68 E", 52.37, 12.68)]:
    print("   %-42s %.3f%%" % (name, share(p2020, la, lo)))

print("== distance Rankin's point to the study's 2020 centre: %.0f km" % (dist_deg((46.5, 7.0), (52.37, 12.68)) * math.pi / 180 * 6371.0088))

print("== the woodpecker half centred 43.0 N, 0.9 W: degrees to places (outside if over 90)")
WP = (43.0, -0.9)
places = [
    ("Cambodia: Phnom Penh", 11.56, 104.92), ("Cambodia: Siem Reap", 13.36, 103.86), ("Cambodia: Battambang", 13.10, 103.20),
    ("Cambodia: north-west corner (Poipet)", 13.66, 102.56), ("Cambodia: northernmost (Preah Vihear)", 14.39, 104.68),
    ("Cambodia: north-east (Ratanakiri)", 13.74, 107.0),
    ("Vietnam: Ho Chi Minh City", 10.82, 106.63), ("Vietnam: Nha Trang", 12.24, 109.19), ("Vietnam: Da Nang", 16.05, 108.21),
    ("Vietnam: Hue", 16.46, 107.59), ("Vietnam: Dong Hoi", 17.47, 106.60), ("Vietnam: Vinh", 18.68, 105.68), ("Vietnam: Hanoi", 21.03, 105.85),
    ("Vietnam: Haiphong", 20.86, 106.68),
    ("Laos: Pakse", 15.12, 105.80), ("Laos: Savannakhet", 16.56, 104.75), ("Laos: Vientiane", 17.97, 102.63),
    ("Thailand: Bangkok", 13.75, 100.50), ("Thailand: Ubon Ratchathani", 15.24, 104.85), ("Thailand: Hat Yai", 7.01, 100.47),
    ("Thailand: Phuket", 7.88, 98.39), ("Malaysia: Kuala Lumpur", 3.14, 101.69), ("Malaysia: George Town", 5.41, 100.33),
    ("Singapore", 1.35, 103.82),
    ("Sumatra: Banda Aceh", 5.55, 95.32), ("Sumatra: Medan", 3.59, 98.67), ("Sumatra: Padang", -0.95, 100.35),
    ("Philippines: Manila", 14.60, 120.98), ("Philippines: Laoag (N Luzon)", 18.20, 120.59), ("Philippines: Puerto Princesa", 9.74, 118.74),
    ("Borneo: Kota Kinabalu", 5.98, 116.07), ("Borneo: Pontianak", -0.03, 109.33), ("Java: Jakarta", -6.2, 106.85),
    ("India: Kanyakumari", 8.08, 77.55), ("India: Port Blair (Andamans)", 11.67, 92.74), ("India: Kibithu (far east)", 28.0, 97.0),
    ("China: Guangzhou", 23.13, 113.26), ("China: Hong Kong", 22.32, 114.17), ("China: Haikou", 20.04, 110.34), ("China: Sanya", 18.25, 109.51),
    ("China: Fuzhou", 26.07, 119.30), ("China: Xiamen", 24.48, 118.09), ("China: Shantou", 23.35, 116.68), ("China: Wenzhou", 28.0, 120.67),
    ("China: Shanghai", 31.23, 121.47), ("China: Nanning", 22.82, 108.32), ("China: Changsha", 28.23, 112.94), ("China: Nanchang", 28.68, 115.86),
    ("Taiwan: Taipei", 25.03, 121.57), ("Japan: Tokyo", 35.68, 139.69),
    ("S America: Lima", -12.05, -77.04), ("S America: Arequipa", -16.41, -71.54), ("S America: La Paz", -16.5, -68.15),
    ("S America: Sao Paulo", -23.55, -46.63), ("S America: Asuncion", -25.3, -57.6), ("S America: Santiago", -33.45, -70.67),
    ("S America: Buenos Aires", -34.6, -58.38), ("S America: Montevideo", -34.9, -56.16), ("S America: Porto Alegre", -30.03, -51.23),
    ("S America: Antofagasta", -23.65, -70.4), ("S America: Tacna", -18.01, -70.25), ("S America: Salta", -24.78, -65.41),
    ("S America: Cordoba", -31.42, -64.18),
]
for name, la, lo in places:
    d = dist_deg(WP, (la, lo))
    print("   %-42s %6.2f  %s" % (name, d, "OUTSIDE" if d > 90 else "inside"))

print("== antipodes of places in tropical South America (latitude sign flipped, longitude + 180)")
for name, la, lo in [("Lima", -12.05, -77.04), ("Cusco", -13.53, -71.97), ("Arequipa", -16.41, -71.54), ("Trujillo", -8.11, -79.03),
                     ("Piura", -5.19, -80.63), ("Guayaquil", -2.19, -79.89), ("Quito", -0.18, -78.47), ("Cuenca", -2.90, -79.0),
                     ("Iquitos", -3.75, -73.25), ("Pucallpa", -8.38, -74.55), ("La Paz", -16.5, -68.15), ("Bogota", 4.71, -74.07),
                     ("Cali", 3.45, -76.53), ("Manaus", -3.1, -60.02), ("Caracas", 10.5, -66.9), ("Paramaribo", 5.85, -55.2),
                     ("Belem", -1.45, -48.5), ("Porto Velho", -8.76, -63.9), ("Santa Cruz", -17.8, -63.18), ("Cuiaba", -15.6, -56.1)]:
    print("   %-12s %7.2f %8.2f  -> antipode %6.2f N %7.2f E" % (name, la, lo, -la, lo + 180))
