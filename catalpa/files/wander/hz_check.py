# Independent check of siam1868.py: ask JPL Horizons (DE441 and JPL's own Earth orientation) for the apparent Sun and Moon from the French camp at one-second steps around my
# two contacts, and find when ITS Moon covers ITS Sun, using the same radii as mine.  Line K5 in ~/journal.md, written first.  Run with python -I after the two fetches below.
import numpy as np, sys, subprocess, urllib.parse, os
LON, LAT = 99 + 47 / 60 + 44 / 3600, 11 + 42 / 60 + 35 / 3600; AU = 149597870.7; RS, RM = 696000.0, 0.2725076 * 6378.137
MINE = {'c2': 2403562.5 + (5 * 3600 + 0 * 60 + 38.1) / 86400, 'c3': 2403562.5 + (5 * 3600 + 7 * 60 + 29.4) / 86400}       # my contacts, JD UT
def fetch(body, key):
    fn = f'/home/agent1/wander/hz/{body}_{key}.txt'
    if not os.path.exists(fn):
        tl = ' '.join(f'{MINE[key] + k / 86400:.7f}' for k in range(-20, 21))
        q = {'format': 'text', 'COMMAND': f"'{body}'", 'OBJ_DATA': "'NO'", 'MAKE_EPHEM': "'YES'", 'EPHEM_TYPE': "'OBSERVER'", 'CENTER': "'coord@399'", 'COORD_TYPE': "'GEODETIC'",
             'SITE_COORD': f"'{LON:.6f},{LAT:.6f},0.005'", 'TLIST': f"'{tl}'", 'QUANTITIES': "'2,20,30,34'", 'ANG_FORMAT': "'DEG'", 'EXTRA_PREC': "'YES'", 'CSV_FORMAT': "'YES'"}
        url = 'https://ssd.jpl.nasa.gov/api/horizons.api?' + urllib.parse.urlencode(q)
        subprocess.run(['curl', '-s', '-m', '120', '-A', 'ephemeris-check/1.0', url, '-o', fn], check=True)
    rows = []; on = False
    for line in open(fn):
        if line.startswith('$$SOE'): on = True; continue
        if line.startswith('$$EOE'): break
        if on:
            w = [x.strip() for x in line.split(',')]; rows.append(w)
    return rows, fn
if __name__ == '__main__':
    for key in ('c2', 'c3'):
        m, fm = fetch(301, key); s, fs = fetch(10, key)
        if not m or not s: print('no rows; see', fm, fs); continue
        if key == 'c2':
            hdr = [l for l in open(fm) if 'Date_' in l or 'JDUT' in l][:1]; print('columns:', hdr[0].strip()[:200] if hdr else '?'); print('first row:', m[0])
        num = lambda w: [float(x) for x in w if x.replace('.', '', 1).replace('-', '', 1).replace('+', '', 1).replace('E', '', 1).replace('e', '', 1).isdigit()]
        out = []
        for k, (a, b) in enumerate(zip(m, s)):
            fa, fb = num(a), num(b)          # RA, DEC, delta, deldot, TDB-UT, local apparent solar time (the date column is not a number); rows are my instant -20 s ... +20 s
            jd, ram, dem, dm = MINE[key] + (k - 20) / 86400, np.radians(fa[0]), np.radians(fa[1]), fa[2] * AU; ras, des, ds = np.radians(fb[0]), np.radians(fb[1]), fb[2] * AU
            sep = np.arccos(np.sin(dem) * np.sin(des) + np.cos(dem) * np.cos(des) * np.cos(ram - ras)); out.append((jd, sep - (np.arcsin(RM / dm) - np.arcsin(RS / ds)), fa[4], fb[5]))
        last = [o[3] for o in out]; out = np.array([(o[0], o[1], o[2]) for o in out]); g = np.degrees(out[:, 1]) * 3600
        i = np.where(np.diff(np.sign(g)) != 0)[0]
        tz = out[i[0], 0] + (out[i[0] + 1, 0] - out[i[0], 0]) * (0 - g[i[0]]) / (g[i[0] + 1] - g[i[0]]) if len(i) else np.nan
        j = np.abs(out[:, 0] - MINE[key]).argmin()
        print(f'{key}: at my instant JPL has separation minus (Moon radius - Sun radius) = {g[j]:+.2f} arcsec; JPL\'s own contact is {(tz - MINE[key]) * 86400:+.1f} s from mine; JPL TDB-UT = {out[j, 2]:.2f} s (mine: TT-UT 2.3 s, TDB-TT ~0)')
        h = last[j]; print(f'   JPL local apparent solar time at my instant: {int(h):02d}:{int(h * 60 % 60):02d}:{h * 3600 % 60:04.1f};  rows: {m[0][0]} ... {m[-1][0]}')
