# Is the West Coast's excess of October 2026 in the top 500 m?  Dynamic (steric) height of the sea surface relative to 500 dbar from Spray glider profiles
# (California Underwater Glider Network, via the IOOS Glider DAC), every October 2014-2026, by distance from the coast.  Lines G1-G3 in ~/journal.md (25 Nov, 16:41 UTC), written
# before any profile was fetched.  Run with python -I (reads downloaded CSV as data); needs gsw (TEOS-10).
#   usage: glider.py [months dir, default glider/oct]    writes glider/profiles_<dir>.npy
import numpy as np, glob, os, sys, gsw
HERE = os.path.dirname(os.path.abspath(__file__)); DIR = sys.argv[1] if len(sys.argv) > 1 else 'oct'
COAST = [(30.4, -115.9), (31.85, -116.62), (32.7, -117.2), (33.46, -117.70), (33.75, -118.2), (34.0, -118.8), (34.45, -120.47), (35.2, -120.9), (36.6, -121.9), (37.8, -122.5)]
CP = np.array([(a[0] + f * (b[0] - a[0]), a[1] + f * (b[1] - a[1])) for a, b in zip(COAST[:-1], COAST[1:]) for f in np.linspace(0, 1, 60)])
def dist(lat, lon): return np.hypot((CP[:, 0] - lat) * 111.2, (CP[:, 1] - lon) * 111.2 * np.cos(np.radians(lat))).min()
# the two cross-shore lines the gliders fly here (CalCOFI lines 90 and 80), each given by two of its stations
LINES = {'90': ((33.485, -117.768), (30.418, -123.999)), '80': ((34.45, -120.52), (32.817, -123.905))}
def offline(lat, lon, a, b):
    ax, ay = a[1] * np.cos(np.radians(33)) * 111.2, a[0] * 111.2; bx, by = b[1] * np.cos(np.radians(33)) * 111.2, b[0] * 111.2; px, py = lon * np.cos(np.radians(33)) * 111.2, lat * 111.2
    t = ((px - ax) * (bx - ax) + (py - ay) * (by - ay)) / ((bx - ax) ** 2 + (by - ay) ** 2); return np.hypot(px - ax - t * (bx - ax), py - ay - t * (by - ay)), t
PG = np.arange(0.0, 501.0, 10.0); recs = []; nfile = 0
for fn in sorted(glob.glob(f'{HERE}/glider/{DIR}/*.csv')):
    year = int(os.path.basename(fn)[:4]); dep = os.path.basename(fn)[5:-4]; nfile += 1; cur = None; buf = []
    def flush(cur, buf):
        if cur is None or len(buf) < 20: return
        a = np.array(buf); p, t, s = a[:, 0], a[:, 1], a[:, 2]; ok = np.isfinite(p + t + s) & (s > 30) & (s < 36) & (t > 2) & (t < 32) & (p >= 0)
        p, t, s = p[ok], t[ok], s[ok]
        if len(p) < 20 or p.min() > 20 or p.max() < 195: return
        deep = p.max() >= 490
        o = np.argsort(p); p, t, s = p[o], t[o], s[o]; tg, sg = np.interp(PG, p, t), np.interp(PG, p, s)
        lat, lon, tm, u, v = cur[1], cur[2], cur[0], cur[3], cur[4]
        SA = gsw.SA_from_SP(sg, PG, lon, lat); CT = gsw.CT_from_t(SA, tg, PG); D = gsw.geo_strf_dyn_height(SA, CT, PG, p_ref=500.0)[0] / 9.8 if deep else np.nan; D200 = gsw.geo_strf_dyn_height(SA[:21], CT[:21], PG[:21], p_ref=200.0)[0] / 9.8
        sig = gsw.sigma0(SA, CT); z26 = np.interp(26.0, sig, PG) if (deep and sig[0] < 26.0 < sig[-1]) else np.nan
        d90, t90 = offline(lat, lon, *LINES['90']); d80, t80 = offline(lat, lon, *LINES['80']); line = 90 if d90 < 25 else (80 if d80 < 25 else 0)
        recs.append((year, tm, lat, lon, dist(lat, lon), 100 * D, z26, tg[10], tg[:21].mean(), u, v, line, hash(dep) % 100000, 100 * D200, p.max()))
    for i, row in enumerate(open(fn)):
        if i < 2: continue
        w = row.rstrip('\n').split(',')
        if len(w) < 9 or w[0] == '': continue
        key = w[0]
        if cur is None or key != cur[5]:
            flush(cur, buf); buf = []
            day = (np.datetime64(w[1][:19]) - np.datetime64(f'{year}-10-01T00:00:00')) / np.timedelta64(1, 'D')
            f = lambda x: float(x) if x not in ('NaN', '') else np.nan
            cur = (float(day), f(w[2]), f(w[3]), f(w[7]), f(w[8]), key)
        try: buf.append((float(w[4]), float(w[5]), float(w[6])))
        except ValueError: pass
    flush(cur, buf)
R = np.array(recs); np.save(f'{HERE}/glider/profiles_{DIR}.npy', R)
print(f'{nfile} deployment-months read; {len(R)} profiles reach 195 dbar, {int(np.isfinite(R[:, 5]).sum())} of them 490 dbar; columns (two added at the end: dynamic height 0/200 in cm, deepest pressure): year, day of October, lat, lon, km from coast, dynamic height 0/500 (cm), depth of sigma0=26.0 (dbar), T at 100 dbar, mean T 0-200, u, v (depth-averaged, m/s), line, deployment')
