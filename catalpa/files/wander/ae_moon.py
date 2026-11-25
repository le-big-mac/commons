# (One entry, 14 August hour 10, was first misread in both coordinates and is mended: 6h 25m 31.36s, +19d 15' 39.4".)
# The American Ephemeris for 1868, "The Moon's right ascension and declination" for every hour of Greenwich mean time (astronomical days, hour 0 = noon), read from the page images
# (its pages 119, 132-136), against JPL Horizons (DE441), geocentric apparent place of date, at TT = ephemeris time + the published clock correction.
# Purpose: Major Tennant got nine longitudes for his station at Guntoor from the Moon against stars, "from the data given in the American Nautical Almanac" (his p. 12-13).
# A longitude got with a table Moon that stands X arcsec ahead of the true Moon comes out about X / 0.55 seconds of time too large.
import numpy as np, subprocess, urllib.parse, os, sys
DT = float(sys.argv[1]) if len(sys.argv) > 1 else 4.1
AE = [  # (month, day, hour from noon, RA h m s, sign, Dec d m s)
 (7, 24, 2, 12, 29, 14.37, +1, 0, 32, 56.1), (7, 24, 3, 12, 31, 27.21, +1, 0, 21, 18.6), (7, 24, 4, 12, 33, 39.88, +1, 0, 9, 41.9),
 (8, 1, 3, 19, 21, 12.76, -1, 18, 57, 1.3), (8, 1, 4, 19, 23, 18.66, -1, 18, 55, 2.0), (8, 1, 5, 19, 25, 24.47, -1, 18, 52, 57.5),
 (8, 8, 7, 0, 59, 33.38, +1, 2, 3, 25.8), (8, 8, 8, 1, 1, 29.34, +1, 2, 13, 29.9), (8, 8, 9, 1, 3, 25.40, +1, 2, 23, 33.8),
 (8, 9, 8, 1, 48, 32.11, +1, 6, 12, 53.4), (8, 9, 9, 1, 50, 31.72, +1, 6, 22, 41.7), (8, 9, 10, 1, 52, 31.52, +1, 6, 32, 28.9),
 (8, 11, 8, 3, 28, 35.12, +1, 13, 27, 12.8), (8, 11, 9, 3, 30, 46.92, +1, 13, 35, 7.6), (8, 11, 10, 3, 32, 59.03, +1, 13, 42, 58.6),
 (8, 12, 10, 4, 27, 27.09, +1, 16, 29, 57.6), (8, 12, 11, 4, 29, 47.40, +1, 16, 35, 54.5), (8, 12, 12, 4, 32, 8.05, +1, 16, 41, 46.0),
 (8, 13, 9, 5, 22, 37.20, +1, 18, 22, 1.4), (8, 13, 10, 5, 25, 4.91, +1, 18, 25, 37.5), (8, 13, 11, 5, 27, 32.92, +1, 18, 29, 6.7),
 (8, 14, 10, 6, 25, 31.36, +1, 19, 15, 39.4), (8, 14, 11, 6, 28, 5.40, +1, 19, 16, 8.3), (8, 14, 12, 6, 30, 39.64, +1, 19, 16, 29.2),
 (8, 17, 16, 9, 47, 55.46, +1, 13, 10, 43.6), (8, 17, 17, 9, 50, 27.20, +1, 13, 1, 19.7), (8, 17, 18, 9, 52, 58.73, +1, 12, 51, 50.4)]
NA = [  # the British Nautical Almanac for 1868 (Hansen's Moon), same hours, from its page images (pp. 131, 146-150 of the almanac)
 (7, 24, 2, 12, 29, 14.08, +1, 0, 32, 59.3), (7, 24, 3, 12, 31, 26.93, +1, 0, 21, 21.7), (7, 24, 4, 12, 33, 39.60, +1, 0, 9, 44.9),
 (8, 1, 3, 19, 21, 12.76, -1, 18, 57, 2.6), (8, 1, 4, 19, 23, 18.66, -1, 18, 55, 3.3), (8, 1, 5, 19, 25, 24.47, -1, 18, 52, 58.8),
 (8, 8, 7, 0, 59, 33.71, +1, 2, 3, 23.1), (8, 8, 8, 1, 1, 29.66, +1, 2, 13, 27.3), (8, 8, 9, 1, 3, 25.73, +1, 2, 23, 31.3),
 (8, 9, 8, 1, 48, 32.40, +1, 6, 12, 51.5), (8, 9, 9, 1, 50, 32.01, +1, 6, 22, 39.9), (8, 9, 10, 1, 52, 31.81, +1, 6, 32, 27.1),
 (8, 11, 8, 3, 28, 35.41, +1, 13, 27, 12.7), (8, 11, 9, 3, 30, 47.21, +1, 13, 35, 7.5), (8, 11, 10, 3, 32, 59.32, +1, 13, 42, 58.6),
 (8, 12, 10, 4, 27, 27.50, +1, 16, 29, 57.9), (8, 12, 11, 4, 29, 47.82, +1, 16, 35, 54.8), (8, 12, 12, 4, 32, 8.47, +1, 16, 41, 46.3),
 (8, 13, 9, 5, 22, 37.70, +1, 18, 22, 1.4), (8, 13, 10, 5, 25, 5.41, +1, 18, 25, 37.4), (8, 13, 11, 5, 27, 33.42, +1, 18, 29, 6.6),
 (8, 14, 10, 6, 25, 31.87, +1, 19, 15, 38.7), (8, 14, 11, 6, 28, 5.91, +1, 19, 16, 7.6), (8, 14, 12, 6, 30, 40.14, +1, 19, 16, 28.5),
 (8, 17, 16, 9, 47, 55.45, +1, 13, 10, 44.2), (8, 17, 17, 9, 50, 27.18, +1, 13, 1, 20.4), (8, 17, 18, 9, 52, 58.70, +1, 12, 51, 51.2)]
def jdnoon(mo, d): return 2403562.0 + (d - 17) + (0 if mo == 8 else -31)        # 17 Aug 1868 noon = JD 2403562.0; July has 31 days
jd = [jdnoon(mo, d) + h / 24.0 + DT / 86400.0 for mo, d, h, *_ in AE]
def fetch(tl, tag):
    fn = f'/home/agent1/wander/hz/conj/ae_moon_{tag}.txt'
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
a = fetch(jd, f'{DT:.2f}'); b = fetch([x + 60.0 / 86400 for x in jd], f'{DT:.2f}_plus60')
# Tennant's nine values (seconds beyond 5h 21m), his p. 12-13: (month, day, what, value)
T = [(8, 8, 'occultation, 33 Ceti, immersion', 48.8), (8, 12, 'occultation, alpha Tauri, immersion', 53.1), (8, 12, 'occultation, alpha Tauri, emersion', 50.3),
     (7, 24, 'equal altitudes, gamma Virginis', 53.4), (8, 1, 'equal altitudes, tau Sagittarii', 46.6), (8, 9, 'equal altitudes, alpha Arietis', 43.3),
     (8, 11, 'equal altitudes, zeta Persei', 53.3), (8, 13, 'equal altitudes, zeta Tauri', 47.9), (8, 14, 'equal altitudes, gamma Geminorum', 45.5)]
for label, TAB in (('American Ephemeris', AE), ('British Nautical Almanac (Hansen)', NA)):
    print(f'clock correction {DT} s.  {label} minus JPL:')
    by = {}
    for (mo, d, h, rh, rm, rs, sg, dd, dm, ds), r0, r1 in zip(TAB, a, b):
        ra = 15 * (rh + rm / 60 + rs / 3600); de = sg * (dd + dm / 60 + ds / 3600)
        dra = ((ra - r0[1] + 180) % 360 - 180) * 3600 * np.cos(np.radians(de)); dde = (de - r0[2]) * 3600
        vra = ((r1[1] - r0[1] + 180) % 360 - 180) * 3600 * np.cos(np.radians(de)) / 60; vde = (r1[2] - r0[2]) * 3600 / 60; v = np.hypot(vra, vde)
        along = (dra * vra + dde * vde) / v; across = (-dra * vde + dde * vra) / v
        by.setdefault((mo, d), []).append((along, across, v))
    for (mo, d), q in by.items():
        q = np.array(q); print(f'  {mo}/{d:02d}: along the path {q[:, 0].mean():+6.2f}" (the three hours {q[:, 0].min():+.2f} to {q[:, 0].max():+.2f}; {q[:, 0].mean() / q[:, 2].mean():+5.1f} s of the Moon\'s motion)   across {q[:, 1].mean():+5.2f}"')
    print(f'Tennant\'s longitudes (5h 21m + ...), as he gives them, and turned to the modern Moon on the supposition that he reduced them with the {label}:')
    out = []; xs = []
    for mo, d, what, val in T:
        q = np.array(by[(mo, d)]); lead = q[:, 0].mean() / q[:, 2].mean(); out.append(val - lead); xs.append(lead)
        print(f'  {mo}/{d:02d} {what:38s} {val:5.1f} s  ->  {val - lead:5.1f} s   (table Moon {q[:, 0].mean():+5.1f}" ahead, {lead:+5.1f} s)')
    o = np.array(out); raw = np.array([t[3] for t in T]); xs = np.array(xs)
    byday = lambda z: np.mean([z[0], (z[1] + z[2]) / 2] + list(z[3:]))
    slope = np.polyfit(xs, raw, 1)[0]
    print(f'  as he gives them: mean of nine {raw.mean():.1f} s, sd {raw.std(ddof=1):.1f}; by day {byday(raw):.1f}.  Turned: mean of nine {o.mean():.1f} s, sd {o.std(ddof=1):.1f}; by day {byday(o):.1f}; occultations {o[:3].mean():.1f} (spread {o[:3].max() - o[:3].min():.1f}); altitudes {o[3:].mean():.1f}')
    print(f'  slope of his values against the table\'s lead: {slope:+.2f} (1 if he used this table and the modern Moon is right; 0 if this table\'s swings are not in his values)')
    print()
print('survey longitude moved 30" east for the modern Madras: 48.65 s; the eclipse with the modern Moon wants about 40.7 s')
