# Map for rise.html: the coast from Baja California to northern California, the tide gauges, when the quick rise of
# 28 September 2026 passed each (hours after San Diego, from older.out, the same figures as the page's table), and
# where Hurricane Polo came ashore (midway between the hurricane center's advisories 34 and 35, polo.out).
# Land outline: Natural Earth, 1:50 million (public domain). Drawn 700 px wide with large lettering for a phone.
# Run: ~/ipd/.venv/bin/python -I src/plot_map.py   (writes ~/site/img/rise-map.png)
import json, math, re
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
SURF, INK, INK2, GRID, WASH = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df', '#efeeea'; BLUE, ORANGE = '#2a78d6', '#eb6834'
X0, X1, Y0, Y1 = -127.6, -108.3, 22.0, 42.6
fig = plt.figure(figsize=(5.0, 6.52), facecolor=SURF); ax = fig.add_axes([0, 0, 1, 1]); ax.set_facecolor(SURF)
for f in json.load(open('/home/agent1/trace/data/ne/ne_50m_land.geojson'))['features']:
    g = f['geometry']; polys = [g['coordinates']] if g['type'] == 'Polygon' else g['coordinates']
    for p in polys:
        ring = p[0]
        if any(X0 - 3 < x < X1 + 3 and Y0 - 3 < y < Y1 + 3 for x, y in ring): ax.add_patch(Polygon(ring, closed=True, facecolor=WASH, edgecolor=INK2, lw=0.8, zorder=1))
for f in json.load(open('/home/agent1/trace/data/ne/ne_50m_admin_0_boundary_lines_land.geojson'))['features']:
    g = f['geometry']; lines = [g['coordinates']] if g['type'] == 'LineString' else g['coordinates']
    for l in lines:
        if any(X0 < x < X1 and Y0 < y < Y1 for x, y in l): ax.plot([x for x, y in l], [y for x, y in l], color=INK2, lw=0.8, ls=(0, (4, 3)), zorder=2)
ax.set_xlim(X0, X1); ax.set_ylim(Y0, Y1); ax.set_aspect(1 / math.cos(math.radians(32.5))); ax.axis('off')
# the gauges and their hours, from older.out (the block for 2026)
POS = {"San Diego": (32.714, -117.174), "Los Angeles": (33.720, -118.272), "Santa Barbara": (34.405, -119.692), "Port San Luis": (35.169, -120.754), "Monterey": (36.605, -121.888),
       "San Francisco": (37.806, -122.466), "Arena Cove": (38.915, -123.711), "North Spit": (40.767, -124.217)}
hours = {}
blk = open('/home/agent1/trace/older.out').read().split('KAY 2022')[0]
for l in blk.splitlines():
    m = re.match(r'^(San Diego|La Jolla|Los Angeles|Santa Barbara|Port San Luis|Monterey|San Francisco|Point Reyes|Arena Cove|North Spit)\s+(\d+)\s+([\d.]+)\s+(\d\d \w\w\w \d\d:\d\d)\s+(-?\d+)', l)
    if m: hours[m.group(1)] = (int(m.group(2)), float(m.group(3)), m.group(4), int(m.group(5)))
NAME = {"North Spit": "Humboldt Bay"}
for n, (la, lo) in POS.items():
    km, rise, when, h = hours[n]
    ax.plot([lo], [la], 'o', ms=8, color=BLUE, mec=SURF, mew=1.2, zorder=5)
    ax.text(lo + 0.5, la + (0.22 if h == 0 else 0.0), NAME.get(n, n) + (", 28 Sep 16:00" if h == 0 else f", {h} hours later"), fontsize=11, color=INK, ha='left', va='center', zorder=6)
# Point Conception, the corner
ax.annotate('Point\nConception', xy=(-120.47, 34.45), xytext=(-123.0, 33.3), fontsize=10.5, color=INK2, ha='right', va='center', linespacing=1.1, arrowprops=dict(arrowstyle='-', color=INK2, lw=0.8, shrinkA=1, shrinkB=2), zorder=6)
# Polo's landfall
adv = [l.split() for l in open('/home/agent1/trace/polo.out') if re.match(r'^\s+3[45]\s+29 Sep', l)]
pts = [(float(a[4][:-1]), -float(a[5][:-1])) for a in adv]; pla = sum(p[0] for p in pts) / 2; plo = sum(p[1] for p in pts) / 2
ax.plot([plo], [pla], 'X', ms=8, color=ORANGE, mec=SURF, mew=0.6, zorder=5)
ax.text(plo - 0.7, pla - 0.1, 'Hurricane Polo\ncame ashore\nabout here,\n29 Sep 06:00', fontsize=10.5, color=INK, ha='right', va='top', linespacing=1.2, zorder=6)
ax.text(-115.6, 28.9, 'Baja\nCalifornia', fontsize=10.5, color=INK2, ha='right', va='center', linespacing=1.1, style='italic', zorder=6)
ax.text(-121.3, 39.85, 'California', fontsize=11, color=INK2, ha='center', va='center', style='italic', zorder=6)
ax.text(-110.6, 29.9, 'Mexico', fontsize=11, color=INK2, ha='center', va='center', style='italic', zorder=6)
ax.text(-124.3, 29.0, 'Pacific\nOcean', fontsize=11, color=INK2, ha='center', va='center', style='italic', linespacing=1.1, zorder=6)
# scale: 500 km along a meridian is 4.497 degrees of latitude
ax.plot([-126.9, -126.9], [23.0, 23.0 + 500 / 111.19], color=INK2, lw=1.5, solid_capstyle='butt', zorder=6); ax.text(-126.5, 23.0 + 250 / 111.19, '500 km', fontsize=10.5, color=INK2, va='center', zorder=6)
fig.savefig('/home/agent1/site/img/rise-map.png', dpi=140, facecolor=SURF)
print('landfall mark at', round(pla, 2), round(plo, 2), '| hours:', {NAME.get(k, k): v[3] for k, v in hours.items() if k in POS})
