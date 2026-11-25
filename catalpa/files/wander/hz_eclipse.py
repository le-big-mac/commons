# Eclipse contacts at the three stations, computed entirely from JPL Horizons (DE441 Sun and Moon, apparent places from the station), independent of my own orrery.
# Horizons is asked in TT; the station is moved in longitude by the rotation that separates JPL's clock correction from the one being tried.  Its local apparent sidereal time for the moved
# station is then the true local sidereal time under the trial correction.  Radii: Sun 696,000 km; Moon k = 0.2725076 (standard) or 0.272281 (smaller) times 6378.137 km.
import numpy as np, subprocess, urllib.parse, os, sys
D = '/home/agent1/wander/hz/ecl/'; AU = 149597870.7; RS = 696000.0; K = {'standard': 0.2725076 * 6378.137, 'smaller': 0.272281 * 6378.137}
def fetch(tag, body, tl, lon, lat, alt, ttype='TT'):
    fn = D + f'{tag}_{body}.txt'
    if not os.path.exists(fn):
        q = {'format': 'text', 'COMMAND': f"'{body}'", 'OBJ_DATA': "'NO'", 'MAKE_EPHEM': "'YES'", 'EPHEM_TYPE': "'OBSERVER'", 'CENTER': "'coord@399'", 'COORD_TYPE': "'GEODETIC'",
             'SITE_COORD': f"'{lon:.7f},{lat:.6f},{alt}'", 'TLIST': "'" + ' '.join(f'{x:.8f}' for x in tl) + "'", 'TIME_TYPE': f"'{ttype}'", 'QUANTITIES': "'2,7,20,30'", 'ANG_FORMAT': "'DEG'",
             'EXTRA_PREC': "'YES'", 'CSV_FORMAT': "'YES'", 'CAL_FORMAT': "'JD'"}
        subprocess.run(['curl', '-s', '-m', '120', '-A', 'ephemeris-check/1.0', 'https://ssd.jpl.nasa.gov/api/horizons.api?' + urllib.parse.urlencode(q), '-o', fn], check=True)
    rows = []; on = False
    for line in open(fn):
        if line.startswith('$$SOE'): on = True; continue
        if line.startswith('$$EOE'): break
        if on:
            v = []
            for x in line.split(','):
                x = x.strip()
                try: v.append(float(x))
                except ValueError:
                    p = x.split()
                    if len(p) == 3:
                        try: v.append(float(p[0]) + float(p[1]) / 60 + float(p[2]) / 3600)
                        except ValueError: pass
            rows.append(v)
    return np.array(rows)        # columns: JD, RA, Dec, local apparent sidereal time (h), range (au), range rate, TDB-UT
def contacts(name, lon, lat, alt, jd_guess, dt, events):
    """events: list of (label, kind, radius-name, seconds from jd_guess (UT) of the observed time).  Returns for each: seconds from jd_guess (UT under the trial correction) and local sidereal time (h)."""
    pre = fetch(f'{name}_pre', 301, [jd_guess], lon, lat, alt, 'UT'); dt_jpl = pre[0, -1]
    lon2 = lon + (dt_jpl - dt) * 15.04107 / 3600.0; out = {}
    for label, kind, rad, off in events:
        tl = [jd_guess + (off + dt + k * 4.0) / 86400.0 for k in range(-25, 26)]
        m = fetch(f'{name}_{label}_{dt:.2f}', 301, tl, lon2, lat, alt); s = fetch(f'{name}_{label}_{dt:.2f}', 10, tl, lon2, lat, alt)
        t = (m[:, 0] - jd_guess) * 86400 - dt                                   # seconds of UT from the guess
        ram, dem, ras, des = np.radians(m[:, 1]), np.radians(m[:, 2]), np.radians(s[:, 1]), np.radians(s[:, 2])
        sep = np.arccos(np.sin(dem) * np.sin(des) + np.cos(dem) * np.cos(des) * np.cos(ram - ras)); rm = np.arcsin(K[rad] / (m[:, 4] * AU)); rs = np.arcsin(RS / (s[:, 4] * AU))
        g = sep - (rm + rs) if kind in ('c1', 'c4') else sep - (rm - rs); want_falling = kind in ('c1', 'c2')
        for i in range(len(g) - 1):
            if (g[i] > 0 >= g[i + 1]) if want_falling else (g[i] <= 0 < g[i + 1]):
                f = (0 - g[i]) / (g[i + 1] - g[i]); lst = m[i, 3] + f * ((m[i + 1, 3] - m[i, 3] + 12) % 24 - 12)
                out[label] = (t[i] + f * (t[i + 1] - t[i]), lst % 24, np.degrees(g[i + 1] - g[i]) * 3600 / (t[i + 1] - t[i])); break
        else: out[label] = (np.nan, np.nan, np.nan)
    return out, dt_jpl
def hms(h): h = h % 24; return f'{int(h):02d}:{int(h * 60 % 60):02d}:{h * 3600 % 60:04.1f}'
if __name__ == '__main__':
    # Clock corrections tried (TT - UT): the older table I first used; the published curve (Stephenson, Morrison, Hohenkerk 2016/2020); that curve plus 1.0 s and plus 1.4 s,
    # the range that star occultations of the 1860s suggest (see loa.py tables).  The page's figures use the published curve alone.
    T68 = ((2.47, 'older table'), (4.07, 'published curve'), (5.07, 'curve + 1.0 s'), (5.5, 'curve + 1.4 s'))
    T69 = ((1.42, 'older table'), (2.84, 'published curve'), (3.84, 'curve + 1.0 s'), (4.24, 'curve + 1.4 s'))
    # --- Wha-Tonne, 18 Aug 1868.  French times (Tisserand; page image of the report's p. 141) are local mean time: UT = LMT - longitude.  Two places: the memorial (OpenStreetMap),
    #     and the mapped shore at the latitude the French measured (11d42'35" N; OpenStreetMap coastline, osm/coast.json: the shore there is at 99.7500 E).
    jd0 = 2403562.5                        # 18 Aug 1868 0h UT
    for name, lon, lat, what in (('wha', 99.7588, 11.7214, 'memorial'), ('whaS2', 99.7500, 11.7097, 'shore at the French latitude')):
        L = lon / 15.0; obs = {'c2': (11 + 39 / 60 + 23.1 / 3600 - L) * 3600, 'c3': (11 + 46 / 60 + 9.1 / 3600 - L) * 3600}            # seconds of UT after 0h
        for dt, tag in T68:
            ev = [('c2', 'c2', 'smaller', obs['c2']), ('c3', 'c3', 'smaller', obs['c3']), ('c2s', 'c2', 'standard', obs['c2']), ('c3s', 'c3', 'standard', obs['c3'])]
            r, dj = contacts(name, lon, lat, 0.005, jd0, dt, ev)
            mid = ((obs['c2'] + obs['c3']) - (r['c2'][0] + r['c3'][0])) / 2
            print(f'Wha-Tonne, {what}, clock correction {dt} s ({tag}): seen minus computed: start of totality {obs["c2"] - r["c2"][0]:+5.1f} s, end {obs["c3"] - r["c3"][0]:+5.1f} s (smaller Moon); {obs["c2"] - r["c2s"][0]:+5.1f}, {obs["c3"] - r["c3s"][0]:+5.1f} (standard); middle of totality {mid:+5.1f} s (either); computed local mean times {hms((r["c2"][0] + L * 3600) / 3600)} and {hms((r["c3"][0] + L * 3600) / 3600)}; totality {r["c3"][0] - r["c2"][0]:.1f} s')
    # --- Guntoor, 18 Aug 1868.  Local sidereal times from the page images of Tennant's report: his first contact (p. 18), first photograph (p. 33; exposed by a sergeant "as soon as
    #     the Sun vanishes" and timed by a recorder, p. 42), last contact (p. 20).  Captain Branfill: first contact 6h2m37.86s, which he "thought too late" (p. 24); the Sun's limb
    #     "a perfect curve, except the two notches" at 8h47m22.9s, and the notches (two lunar mountains) gone 8.6 s later (p. 27).
    #     Station: Tennant's survey longitude 5h21m46.65s (80d26'39.75"), which he had reduced to the Nautical Almanac's Madras (5h20m57.3s); the site of the Madras Observatory is at
    #     80.2471 E on OpenStreetMap (the meteorological centre that stands there), 30" east of the almanac's figure, so the station is taken 30" further east, at 80.4532 E.
    oL = {'c1': 6 + 2 / 60 + 12.66 / 3600, 'c1B': 6 + 2 / 60 + 37.86 / 3600, 'c2': 7 + 17 / 60 + 2.9 / 3600, 'c3': 7 + 22 / 60 + 34.8 / 3600, 'c4': 8 + 47 / 60 + 24.62 / 3600, 'limb': 8 + 47 / 60 + 22.9 / 3600, 'mtn': 8 + 47 / 60 + 31.5 / 3600}
    guess = {'c1': 2 * 3600 + 53 * 60 + 40, 'c2': 4 * 3600 + 8 * 60 + 15, 'c3': 4 * 3600 + 13 * 60 + 55, 'c4': 5 * 3600 + 38 * 60 + 30}       # rough UT seconds after 0h, to centre the search
    for name, lon, where, only in (('gun', 80.4532, "survey position moved 30 arcsec east for the modern longitude of Madras", None), ('gun0', 80.44438, "survey position as Tennant gives it, not moved", 4.07),
                                   ('gunW36', 80.4195, '3.6 km further west', 4.07), ('gunW', 80.4232, '3.2 km further west', 5.5)):
        for dt, tag in T68:
            if only is not None and dt != only: continue
            ev = [(k, k, 'standard' if k in ('c1', 'c4') else 'smaller', guess[k]) for k in ('c1', 'c2', 'c3', 'c4')]
            r, dj = contacts(name, lon, 16.29286, 0.03, jd0, dt, ev); d = lambda k, c: ((oL[k] - r[c][1] + 12) % 24 - 12) * 3600
            print(f'Guntoor at {lon} E ({where}), clock correction {dt} s ({tag}): seen minus computed, sidereal seconds: Tennant first contact {d("c1", "c1"):+5.1f}; Branfill first contact {d("c1B", "c1"):+5.1f}; first photograph vs start of totality {d("c2", "c2"):+5.1f}; Tennant last contact {d("c4", "c4"):+5.1f}; Branfill limb clear vs last contact {d("limb", "c4"):+5.1f}; Branfill mountains gone vs last contact {d("mtn", "c4"):+5.1f}; last photograph vs end of totality {d("c3", "c3"):+5.1f}; computed start of totality {hms(r["c2"][1])} local sidereal = {hms(r["c2"][0] / 3600)} UT')
    # --- Des Moines, 7 Aug 1869.  Newcomb's times are local mean time (page image, p. 14 of his report: 3h43m02.7s, 4h48m25.2s, 5h45m23.7s); UT = LMT + west longitude.
    lon, lat = -93.6215, 41.5844; Lw = -lon / 15.0; jd0 = 2403916.5                     # 7 Aug 1869 0h UT
    ob = {'c1': (15 + 43 / 60 + 2.7 / 3600 + Lw) * 3600, 'c3': (16 + 48 / 60 + 25.2 / 3600 + Lw) * 3600, 'c4': (17 + 45 / 60 + 23.7 / 3600 + Lw) * 3600}
    for dt, tag in T69:
        ev = [('c1', 'c1', 'standard', ob['c1']), ('c3', 'c3', 'smaller', ob['c3']), ('c3s', 'c3', 'standard', ob['c3']), ('c4', 'c4', 'standard', ob['c4'])]
        r, dj = contacts('dsm', lon, lat, 0.26, jd0, dt, ev)
        print(f'Des Moines, clock correction {dt} s ({tag}): seen minus computed: first contact {ob["c1"] - r["c1"][0]:+5.1f} s, end of totality {ob["c3"] - r["c3"][0]:+5.1f} (smaller Moon) {ob["c3"] - r["c3s"][0]:+5.1f} (standard), last contact {ob["c4"] - r["c4"][0]:+5.1f}')
