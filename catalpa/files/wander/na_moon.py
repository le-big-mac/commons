# The Nautical Almanac for 1868 (Hansen's Moon), "The Moon's right ascension and declination" for every hour of Greenwich mean time, read from the page images (August pages IX and X),
# against JPL Horizons (DE441), geocentric apparent place of date, asked for at TT = almanac time + clock correction.  Astronomical days: hour 0 is noon.
import numpy as np, subprocess, urllib.parse, os, sys
DT = float(sys.argv[1]) if len(sys.argv) > 1 else 2.47
NA = [  # (day of August, hour from noon, RA h m s, sign, Dec d m s)
 (17, 16, 9, 47, 55.45, +1, 13, 10, 44.2), (17, 17, 9, 50, 27.18, +1, 13, 1, 20.4), (17, 18, 9, 52, 58.70, +1, 12, 51, 51.2),
 (18, 0, 10, 8, 3.29, +1, 11, 53, 6.9), (18, 12, 10, 37, 48.07, +1, 9, 47, 20.6), (19, 0, 11, 6, 59.23, +1, 7, 32, 50.3), (19, 12, 11, 35, 37.12, +1, 5, 12, 23.7),
 (20, 0, 12, 3, 43.55, +1, 2, 48, 44.5), (20, 12, 12, 31, 21.40, +1, 0, 24, 27.6), (21, 0, 12, 58, 34.21, -1, 1, 58, 5.3), (21, 12, 13, 25, 25.90, -1, 4, 16, 47.3),
 (22, 0, 13, 52, 0.38, -1, 6, 29, 46.3), (22, 12, 14, 18, 21.40, -1, 8, 35, 25.1), (23, 0, 14, 44, 32.37, -1, 10, 32, 21.1), (23, 12, 15, 10, 36.12, -1, 12, 19, 24.2),
 (24, 0, 15, 36, 34.93, -1, 13, 55, 35.9), (24, 12, 16, 2, 30.35, -1, 15, 20, 8.2)]
jd = [2403562.0 + (d - 17) + h / 24.0 + DT / 86400.0 for d, h, *_ in NA]
def fetch(tl, tag):
    fn = f'/home/agent1/wander/hz/conj/na_moon_{tag}.txt'
    if not os.path.exists(fn):
        q = {'format': 'text', 'COMMAND': "'301'", 'OBJ_DATA': "'NO'", 'MAKE_EPHEM': "'YES'", 'EPHEM_TYPE': "'OBSERVER'", 'CENTER': "'500@399'", 'TLIST': "'" + ' '.join(f'{x:.8f}' for x in tl) + "'",
             'TIME_TYPE': "'TT'", 'QUANTITIES': "'2,20'", 'ANG_FORMAT': "'DEG'", 'EXTRA_PREC': "'YES'", 'CSV_FORMAT': "'YES'", 'CAL_FORMAT': "'JD'"}
        subprocess.run(['curl', '-s', '-m', '120', '-A', 'ephemeris-check/1.0', 'https://ssd.jpl.nasa.gov/api/horizons.api?' + urllib.parse.urlencode(q), '-o', fn], check=True)
    rows = []; on = False
    for line in open(fn):
        if line.startswith('$$SOE'): on = True; continue
        if line.startswith('$$EOE'): break
        if on:
            v = []
            for x in line.split(','):
                try: v.append(float(x))
                except ValueError: pass
            rows.append(v)
    return np.array(rows)
a = fetch(jd, f'{DT:.2f}'); b = fetch([x + 60.0 / 86400 for x in jd], f'{DT:.2f}_plus60')      # the second set gives the Moon's rate
print(f'clock correction {DT} s.  Almanac minus JPL, and how many seconds of time the almanac\'s Moon is ahead along its path:')
out = []
for (d, h, rh, rm, rs, sg, dd, dm, ds), r0, r1 in zip(NA, a, b):
    ra = 15 * (rh + rm / 60 + rs / 3600); de = sg * (dd + dm / 60 + ds / 3600)
    dra = (ra - r0[1]) * 3600 * np.cos(np.radians(de)); dde = (de - r0[2]) * 3600
    vra = (r1[1] - r0[1]) * 3600 * np.cos(np.radians(de)) / 60; vde = (r1[2] - r0[2]) * 3600 / 60          # arcsec per second
    along = (dra * vra + dde * vde) / np.hypot(vra, vde); across = (-dra * vde + dde * vra) / np.hypot(vra, vde)
    out.append((along, across, along / np.hypot(vra, vde)))
    print(f'  Aug {d} {h:2d}h: RA {dra:+6.2f}"  Dec {dde:+6.2f}"   along the path {along:+6.2f}" ({along / np.hypot(vra, vde):+5.1f} s)   across {across:+5.2f}"')
o = np.array(out); print(f'mean along the path {o[:, 0].mean():+.2f}" (sd {o[:, 0].std():.2f}), = {o[:, 2].mean():+.1f} s; mean across {o[:, 1].mean():+.2f}"')
