# Points every 100 km along the coast line, and for each the sea cells of the altimetry grid within 60 km
# (90 km if fewer than two). Writes data/alt/points.json and the list of requests data/alt/requests.txt.
# Run: python3 -I src/points.py     (reads data/alt/mask.csv only for which cells hold a value; prints no values)
import sys, json, math
sys.path.insert(0, '/home/agent1/trace/src')
from coastline import WAY, gc
cum = [0.0]
for i in range(1, len(WAY)): cum.append(cum[-1] + gc(WAY[i - 1][1:], WAY[i][1:]))
i0 = [w[0] for w in WAY].index("La Libertad"); cum = [c - cum[i0] for c in cum]
def at(s):
    for i in range(1, len(WAY)):
        if cum[i - 1] <= s <= cum[i]:
            f = (s - cum[i - 1]) / (cum[i] - cum[i - 1])
            return (WAY[i - 1][1] + f * (WAY[i][1] - WAY[i - 1][1]), WAY[i - 1][2] + f * (WAY[i][2] - WAY[i - 1][2]))
sea = set()
for line in open('/home/agent1/trace/data/alt/mask.csv').read().splitlines()[2:]:
    w = line.split(',')
    if w[3] not in ('NaN', ''): sea.add((float(w[1]), float(w[2])))
pts = []; reqs = []
for s in range(-1200, 8801, 100):
    p = at(s)
    for R in (60, 90):
        cells = [c for c in sea if abs(c[0] - p[0]) < 1.0 and abs(c[1] - p[1]) < 1.3 and gc(p, c) <= R]
        if len(cells) >= 2: break
    if not cells: print("no sea cell at", s, p); continue
    la = (min(c[0] for c in cells), max(c[0] for c in cells)); lo = (min(c[1] for c in cells), max(c[1] for c in cells))
    pts.append({"km": s, "lat": round(p[0], 3), "lon": round(p[1], 3), "radius": R, "cells": sorted(cells), "box": [la, lo]})
    tag = f"p{s:+05d}"
    base = "https://coastwatch.noaa.gov/erddap/griddap/noaacwBLENDEDsshDaily.csv?sla"
    box = f"[({la[0]}):1:({la[1]})][({lo[0]}):1:({lo[1]})]"
    reqs.append(f"{tag}_base.csv {base}[(2017-03-01T00:00:00Z):10:(2025-12-31T00:00:00Z)]{box}")
    reqs.append(f"{tag}_2026.csv {base}[(2026-05-01T00:00:00Z):1:(2026-11-25T00:00:00Z)]{box}")
json.dump(pts, open('/home/agent1/trace/data/alt/points.json', 'w'))
open('/home/agent1/trace/data/alt/requests.txt', 'w').write("\n".join(reqs) + "\n")
print(len(pts), "points;", len(reqs), "requests; cells per point: min", min(len(p["cells"]) for p in pts), "max", max(len(p["cells"]) for p in pts),
      "; points needing 90 km:", [p["km"] for p in pts if p["radius"] == 90])
