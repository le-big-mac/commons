# Hurricane passages off the ocean side of Baja California, 1990-2025, from the hurricane centre's best tracks
# (HURDAT2, eastern Pacific). Prints the list of events only: no sea level is read here.
# A passage: a storm with at least one 6-hourly point at hurricane strength (64 knots or more) that lies north of
# 22 N, west of the peninsula's ocean-side coast line, and within 300 km of that line (Cabo San Lucas to Ensenada,
# from src/coastline.py). Its day is the UTC day of the first such point. One event a storm.
import sys, datetime as dt
sys.path.insert(0, '/home/agent1/trace/src')
from coastline import WAY, gc
names = [w[0] for w in WAY]; i0, i1 = names.index("Cabo San Lucas"), names.index("Ensenada")
line = []
for a, b in zip(WAY[i0:i1], WAY[i0 + 1:i1 + 1]):
    for f in [k / 20 for k in range(20)]: line.append((a[1] + f * (b[1] - a[1]), a[2] + f * (b[2] - a[2])))
line.append(WAY[i1][1:])
def near(lat, lon):
    d, p = min((gc((lat, lon), q), q) for q in line)
    return d, lon < p[1]          # distance to the line; True if the point is west of the line's nearest point
def events(path='/home/agent1/trace/data/hurdat/nepac.txt', y0=1990, y1=2025):
    out = []; cur = None
    for l in open(path):
        w = [x.strip() for x in l.split(',')]
        if w[0][:2] in ('EP', 'CP') and len(w[0]) == 8: cur = (w[0], w[1]); first = None; pts = []; continue
        if cur is None or len(w) < 7: continue
        d = dt.datetime.strptime(w[0] + w[1], '%Y%m%d%H%M')
        if not (y0 <= d.year <= y1): continue
        lat = float(w[4][:-1]) * (1 if w[4][-1] == 'N' else -1); lon = -float(w[5][:-1]) if w[5][-1] == 'W' else float(w[5][:-1]); kt = int(w[6])
        if kt >= 64 and lat >= 22.0:
            dist, west = near(lat, lon)
            if dist <= 300 and west and not any(e[0] == cur[0] for e in out):
                out.append((cur[0], cur[1], d, lat, lon, kt, round(dist)))
    return out
if __name__ == "__main__":
    ev = events()
    print(f"{len(ev)} passages, 1990-2025")
    for e in ev: print(f"  {e[0]} {e[1]:<10} {e[2].strftime('%Y-%m-%d %H:%M')}  {e[3]:.1f}N {abs(e[4]):.1f}W  {e[5]} kt  {e[6]} km off the line")
    by = {}
    for e in ev: by[e[2].month] = by.get(e[2].month, 0) + 1
    print("by month:", dict(sorted(by.items())))
