# Second look at JPL Horizons: the same Moon and Sun (DE441), but with MY clock correction (TT - UT = 2.3 s) instead of JPL's 4.15 s for 1868.  Times are given to Horizons in TT, and the
# site's longitude is moved east by the 1.85 s of rotation that separates the two corrections, so that the beach is where my Earth puts it at each TT instant.  What is left is my Moon against JPL's.
import numpy as np, subprocess, urllib.parse, os
LON, LAT = 99 + 47 / 60 + 44 / 3600, 11 + 42 / 60 + 35 / 3600; AU = 149597870.7; RS, RM = 696000.0, 0.2725076 * 6378.137; DT_MINE, DT_JPL = 2.3, 4.1548
SHIFT = (DT_JPL - DT_MINE) * 15.04107 / 3600.0            # degrees of longitude turned in 1.85 s
MINE_UT = {'c2': 2403562.5 + (5 * 3600 + 0 * 60 + 38.1) / 86400, 'c3': 2403562.5 + (5 * 3600 + 7 * 60 + 29.4) / 86400}
def fetch(body, key):
    fn = f'/home/agent1/wander/hz/tt_{body}_{key}.txt'
    if not os.path.exists(fn):
        tl = ' '.join(f'{MINE_UT[key] + (DT_MINE + k) / 86400:.7f}' for k in range(-20, 21))
        q = {'format': 'text', 'COMMAND': f"'{body}'", 'OBJ_DATA': "'NO'", 'MAKE_EPHEM': "'YES'", 'EPHEM_TYPE': "'OBSERVER'", 'CENTER': "'coord@399'", 'COORD_TYPE': "'GEODETIC'",
             'SITE_COORD': f"'{LON + SHIFT:.6f},{LAT:.6f},0.005'", 'TLIST': f"'{tl}'", 'TIME_TYPE': "'TT'", 'QUANTITIES': "'2,20,30'", 'ANG_FORMAT': "'DEG'", 'EXTRA_PREC': "'YES'", 'CSV_FORMAT': "'YES'"}
        subprocess.run(['curl', '-s', '-m', '120', '-A', 'ephemeris-check/1.0', 'https://ssd.jpl.nasa.gov/api/horizons.api?' + urllib.parse.urlencode(q), '-o', fn], check=True)
    rows = []; on = False
    for line in open(fn):
        if line.startswith('$$SOE'): on = True; continue
        if line.startswith('$$EOE'): break
        if on: rows.append([x.strip() for x in line.split(',')])
    return rows
num = lambda w: [float(x) for x in w if x.replace('.', '', 1).replace('-', '', 1).replace('+', '', 1).replace('E', '', 1).replace('e', '', 1).isdigit()]
for key in ('c2', 'c3'):
    m, s = fetch(301, key), fetch(10, key)
    if not m: print('no rows for', key); continue
    g = []
    for a, b in zip(m, s):
        fa, fb = num(a), num(b); ram, dem, dm = np.radians(fa[0]), np.radians(fa[1]), fa[2] * AU; ras, des, ds = np.radians(fb[0]), np.radians(fb[1]), fb[2] * AU
        g.append(np.degrees(np.arccos(np.sin(dem) * np.sin(des) + np.cos(dem) * np.cos(des) * np.cos(ram - ras)) - (np.arcsin(RM / dm) - np.arcsin(RS / ds))) * 3600)
    g = np.array(g); i = np.where(np.diff(np.sign(g)) != 0)[0]; k0 = (i[0] + (0 - g[i[0]]) / (g[i[0] + 1] - g[i[0]]) - 20) if len(i) else np.nan
    print(f'{key}: with my clock correction, JPL\'s Moon and Sun put the contact {k0:+.1f} s from mine (at my instant: {g[20]:+.2f} arcsec); first row {m[0][0]}')
