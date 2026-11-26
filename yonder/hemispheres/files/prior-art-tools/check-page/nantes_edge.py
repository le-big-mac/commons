"""Why does the share of people in the half centred on Nantes move so much with the centre?
Prints the people lying within 0.1 degree (about 11 km) of the edge of the half centred 47.217 N, 1.533 W, by 5-degree box (2020 grid),
the distance from that centre to Tokyo, and the share for centres a few kilometres apart.
usage: python -I nantes_edge.py GRID_DIR"""
import sys, math
import numpy as np
G = sys.argv[1]
H, W = 3600, 7200
lat = np.radians(-90 + (np.arange(H) + 0.5) * 0.05); lon = np.radians(-180 + (np.arange(W) + 0.5) * 0.05)
def cosd(la, lo):
    la, lo = math.radians(la), math.radians(lo)
    return np.sin(lat)[:, None] * math.sin(la) + (np.cos(lat)[:, None] * math.cos(la)) * (np.cos(lon)[None, :] * math.cos(lo) + np.sin(lon)[None, :] * math.sin(lo))
def dist(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    return math.degrees(math.acos(math.sin(la1) * math.sin(la2) + math.cos(la1) * math.cos(la2) * math.cos(lo1 - lo2)))
p = np.load(G + "/pop005.npy").astype(np.float64)
tot = p.sum()
N = (47.217, -1.533)
c = cosd(*N)
band = np.abs(c) < math.sin(math.radians(0.1))
q = np.where(band, p, 0.0)
print("people within 0.1 degree of the edge of the Nantes half: %.2f million = %.3f%% of the world" % (q.sum() / 1e6, 100 * q.sum() / tot))
box = q.reshape(36, 100, 72, 100).sum(axis=(1, 3))
out = sorted(((box[i, j], -90 + 5 * i, -180 + 5 * j) for i in range(36) for j in range(72) if box[i, j] > 2e5), reverse=True)
for v, la, lo in out[:8]:
    print("   lat %4d to %4d, lon %5d to %5d: %6.2f million" % (la, la + 5, lo, lo + 5, v / 1e6))
for name, pt in (("Tokyo (35.68 N, 139.69 E)", (35.68, 139.69)), ("Yokohama", (35.44, 139.64)), ("Saitama", (35.86, 139.65)), ("Chiba", (35.61, 140.11)), ("Osaka", (34.69, 135.50))):
    d = dist(N, pt)
    print("   %-28s %.2f degrees from the centre, %.0f km %s the edge" % (name, d, abs(d - 90) * math.pi / 180 * 6371.0088, "outside" if d > 90 else "inside"))
km = math.pi / 180 * 6371.0088
for la, lo in ((47.217, -1.533), (47.22, -1.55), (47.25, -1.5), (47.2, -1.6), (47.19, -1.50), (47.24, -1.58)):
    s = 100 * p[cosd(la, lo) > 0].sum() / tot
    print("   centre %.3f N %.3f W, %.1f km from 47.217 N 1.533 W: %.3f%%" % (la, -lo, dist(N, (la, lo)) * km, s))
