"""Where on its line could a number stand clear? For the lines 0.01 and 0.2 of the phone map: walk along each line (as matplotlib
draws it from the grid) and at each point measure how far it is from the coast, the marks, the lettered boxes, the names, the
joining lines, the other numbers and the frame. Prints the best spots. Positions in km east and north of the middle of the map.
usage: contour_candidates.py WIDE.npz COAST.geojson DUMP.json     (DUMP.json: where the phone program put its texts and marks, from labels_dump.py)
The coastline file is a download: it is only parsed as JSON here."""
import sys, json, math
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
R_KM = 6371.0088; KM = math.pi * R_KM / 180
Wz = np.load(sys.argv[1]); offs, G, north, east, c0 = Wz['offs'], Wz['G'], Wz['north'], Wz['east'], Wz['c_mid']
ext = offs * KM; loss = (np.nanmax(G) - G) * 100
dump = json.load(open(sys.argv[3]))
(fx0, fy0), (fx1, fy1) = dump['frame_px']
ppk = (fx1 - fx0) / (ext[-1] - ext[0])
def km(px, py): return ext[0] + (px - fx0) / ppk, ext[-1] - (py - fy0) / ppk
def proj(lat, lon):
    la, lo = np.radians(lat), np.radians(lon)
    v = np.stack([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)], axis=-1)
    t = np.degrees(np.arccos(np.clip(v @ c0, -1, 1))); s = np.sin(np.radians(np.maximum(t, 1e-12)))
    return t * (v @ east) / s * KM, t * (v @ north) / s * KM, t
coast = []
for f in json.load(open(sys.argv[2], encoding='utf-8'))['features']:
    g = f['geometry']
    for poly in (g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]):
        for ring in poly:
            r = np.asarray(ring, dtype=float)[:, :2]
            x, y, t = proj(r[:, 1], r[:, 0])
            if (t < 14).any():
                # densify: points every few km along each stretch of coast near the map
                for i in range(len(x) - 1):
                    if t[i] < 14 and t[i + 1] < 14:
                        nseg = max(1, int(math.hypot(x[i + 1] - x[i], y[i + 1] - y[i]) / 4))
                        for q in range(nseg): coast.append((x[i] + (x[i + 1] - x[i]) * q / nseg, y[i] + (y[i + 1] - y[i]) * q / nseg))
coast = np.array(coast); coast = coast[(np.abs(coast[:, 0]) < 900) & (np.abs(coast[:, 1]) < 900)]
boxes = []      # lettered boxes and names, in km: (x0, y0, x1, y1), y0 < y1
for t in dump['texts']:
    bx0, by0, bx1, by1 = t['box_px']
    if by1 < fy0: continue                                   # the heading above the map
    (a, b), (c, d) = km(bx0, by1), km(bx1, by0); boxes.append((a, b, c, d, t['text'].split('\n')[0]))
marks = [(m['km'][0], m['km'][1], m['size_pt'] * 230 / 72 / 2 / ppk) for m in dump['marks']]
joins = []      # joining lines: from the mark to the nearest point of its label's box
for t in dump['texts']:
    if t['target_km']:
        bx0, by0, bx1, by1 = t['box_px']; (a, b), (c, d) = km(bx0, by1), km(bx1, by0)
        tx, ty = t['target_km']; nxp, nyp = min(max(tx, a), c), min(max(ty, b), d)
        joins.append(((tx, ty), ((a + c) / 2, (b + d) / 2)))          # matplotlib draws the joining line from the middle of the box to the mark
def dist_box(x, y, bx):
    a, b, c, d = bx[:4]; return math.hypot(max(a - x, 0, x - c), max(b - y, 0, y - d))
def dist_seg(x, y, p, q):
    (x1, y1), (x2, y2) = p, q; dx, dy = x2 - x1, y2 - y1; u = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)))
    return math.hypot(x - x1 - u * dx, y - y1 - u * dy)
numbers = [(n['text'], n['km'][0], n['km'][1]) for n in dump['numbers']]
fig, ax = plt.subplots()
cs = ax.contour(ext, ext, loss, levels=[0.01, 0.05, 0.1, 0.2, 0.4, 0.8])
for lev, segs in zip(cs.levels, cs.allsegs):
    if lev not in (0.01, 0.05, 0.1, 0.2, 0.4, 0.8): continue
    print(f'\nline {lev:g}: {len(segs)} piece(s), {sum(len(s) for s in segs)} points')
    cand = []
    for seg in segs:
        for i in range(0, len(seg), 2):
            x, y = seg[i]
            if abs(x) > 830 or abs(y) > 830: continue
            dc = float(np.hypot(coast[:, 0] - x, coast[:, 1] - y).min())
            dm = min(math.hypot(x - mx, y - my) - mr for mx, my, mr in marks)
            db = min(dist_box(x, y, b) for b in boxes); wb = min(boxes, key=lambda b: dist_box(x, y, b))[4]
            dj = min(dist_seg(x, y, p, q) for p, q in joins)
            dn = min(math.hypot(x - nx, y - ny) for t, nx, ny in numbers if float(t) != lev)
            j = min(i + 1, len(seg) - 1); k = max(i - 1, 0); ang = math.degrees(math.atan2(seg[j][1] - seg[k][1], seg[j][0] - seg[k][0]))
            cand.append((min(dc, dm, db, dj, dn), x, y, dc, dm, db, dj, dn, wb, ang))
    cand.sort(reverse=True)
    shown = []
    for c in cand:
        if all(math.hypot(c[1] - s[1], c[2] - s[2]) > 60 for s in shown):
            shown.append(c)
            print(f'  ({c[1]:+7.1f}, {c[2]:+7.1f}) km: nearest thing {c[0]:5.1f} km away  [coast {c[3]:5.1f}, marks {c[4]:5.1f}, boxes and names {c[5]:5.1f} ({c[8]}), joining lines {c[6]:5.1f}, other numbers {c[7]:5.1f}]; the line runs at {c[9]:+.0f} deg there')
        if len(shown) >= 9: break
print(f'\n(one number of four characters at 8.5 pt is about {60.5 / ppk:.0f} km long and {20 / ppk:.0f} km high on this map; "0.2" about {43 / ppk:.0f} km long)')
