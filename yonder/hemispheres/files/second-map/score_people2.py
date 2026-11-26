"""Score expectations-people-2.md from the seven JSON files, and print the table of all three datasets.
usage: score_people2.py OUT_DIR"""
import sys, json, os
od = sys.argv[1]
def J(n):
    p = f'{od}/{n}.json'
    return json.load(open(p)) if os.path.exists(p) else None
G2 = {y: J(f'g2-{y}') for y in (2015, 2020, 2025, 2030)}; G1 = {y: J(f'g1-{y}') for y in (2000, 2010, 2020)}
GHS = {y: J(f'ghs-{y}') for y in (1975, 2000, 2005, 2010, 2015, 2020, 2025, 2030)}
def top(r):
    """the highest of the search's best and the three climbs"""
    c = [('search', r['best']['lat'], r['best']['lon'], r['best']['share'])] + [(k, v['lat'], v['lon'], v['share']) for k, v in r['climb'].items()]
    return max(c, key=lambda t: t[3])
print('dataset year | total (thousand million) | best share, where (found by) | share: Valais 46.0,7.18 | Palatinate 49.4,12.4 | Berlin 52.37,12.68 | L points | only Berlin half M | only Valais half M | difference M')
for name, D in (('GHS-POP R2023A', GHS), ('WorldPop older (G1)', G1), ('WorldPop newer (G2)', G2)):
    for y, r in D.items():
        if r is None: print(name, y, 'not computed'); continue
        t = top(r)
        print(f"{name} {y} | {r['total'] / 1e9:.4f} | {100 * t[3]:.3f}% at {t[1]:.2f} N, {t[2]:.2f} E ({t[0]}) | {100 * r['hard']['valais']:.3f} | {100 * r['hard']['palatinate']:.3f} | {100 * r['hard']['berlin']:.3f} | {r['L']:+.3f} | "
              f"{r['only_berlin'] / 1e6:.1f} | {r['only_valais'] / 1e6:.1f} | {(r['only_berlin'] - r['only_valais']) / 1e6:+.1f}")
if any(v is None for v in list(G1.values()) + list(G2.values())): sys.exit('not all seven grids are computed')
KM = 6371.0088 * 3.141592653589793 / 180
import math
def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    return 6371.0088 * math.acos(min(1, math.sin(la1) * math.sin(la2) + math.cos(la1) * math.cos(la2) * math.cos(lo1 - lo2)))
t20 = top(G2[2020]); t00 = top(G1[2000])
L2 = {y: G2[y]['L'] for y in G2}; L1 = {y: G1[y]['L'] for y in G1}
lines = [
 ('E1', 0.75, L2[2020] > 0, f"L = {L2[2020]:+.3f}"),
 ('E2', 0.65, t20[1] > 48.5, f"best centre {t20[1]:.2f} N, {t20[2]:.2f} E"),
 ('E3', 0.45, km((t20[1], t20[2]), (52.37, 12.68)) < 300, f"{km((t20[1], t20[2]), (52.37, 12.68)):.0f} km"),
 ('E4', 0.85, L2[2015] < L2[2020] < L2[2025] < L2[2030], ', '.join(f'{L2[y]:+.3f}' for y in (2015, 2020, 2025, 2030))),
 ('E5', 0.55, L2[2015] > 0, f"L = {L2[2015]:+.3f}"),
 ('E6', 0.80, 0.9250 <= t20[3] <= 0.9290, f"{100 * t20[3]:.3f}%"),
 ('E7', 0.75, L1[2000] < 0, f"L = {L1[2000]:+.3f}"),
 ('E8', 0.70, t00[1] < 47.5, f"best centre {t00[1]:.2f} N, {t00[2]:.2f} E"),
 ('E9', 0.55, L1[2020] > 0, f"L = {L1[2020]:+.3f}"),
 ('E10', 0.85, L1[2000] < L1[2010] < L1[2020], ', '.join(f'{L1[y]:+.3f}' for y in (2000, 2010, 2020))),
 ('E11', 0.85, all(abs(v) < 0.3 for v in list(L1.values()) + list(L2.values())), f"largest |L| {max(abs(v) for v in list(L1.values()) + list(L2.values())):.3f}"),
 ('E12', 0.85, 7.78e9 <= G2[2020]['total'] <= 7.90e9, f"{G2[2020]['total'] / 1e9:.4f}"),
]
b = 0
for k, p, ok, what in lines:
    b += (p - (1 if ok else 0)) ** 2; print(f"{k:4s} {int(100 * p)}%  {'held' if ok else 'FAILED'}  {what}")
print(f"{sum(1 for l in lines if l[2])} of {len(lines)} held; Brier score {b / len(lines):.4f}")
