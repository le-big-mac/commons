# Star occultations timed at the Royal Observatory, Greenwich, in 1868-69 (Monthly Notices 29, 252-253, read from the page image), against JPL Horizons (DE441 Moon) and modern star positions
# (SIMBAD: ICRS position and proper motion, carried back to the date).  The question: which clock correction (TT - UT) makes the Moon's dark limb reach the star when the observer saw it vanish?
# Horizons is asked in TT; the observatory is moved east by the rotation that separates JPL's clock correction from the one being tried, so the Earth is turned as the trial correction says.
import numpy as np, subprocess, urllib.parse, os, sys, datetime
HZ = '/home/agent1/wander/occ/'
LON, LAT, ALT = -0.001475, 51.47781, 0.05            # Airy transit circle, WGS84; km
RMOON = 1737.4                                         # km, mean radius of the Moon's limb
STARS = {}
for line in open(HZ + 'stars.csv'):
    w = line.strip().split(','); STARS[w[0].strip('"').replace('*', '').strip().replace('  ', ' ')] = [float(x) for x in w[1:6]]
EVENTS = [  # star, year, month, day, h, m, s of Greenwich mean solar time (astronomical day from noon; these are all evening hours), table clock correction for the date, note
 ('mu. Cet', 1868, 2, 28, 9, 24, 45.7, 2.79, 'cloudy'), ('tet02 Tau', 1868, 3, 1, 6, 38, 24.5, 2.79, ''), ('tet01 Tau', 1868, 3, 1, 6, 38, 37.0, 2.79, ''),
 ('18 Leo', 1868, 5, 27, 10, 30, 59.3, 2.56, ''), ('119 Tau', 1869, 1, 24, 8, 14, 33.3, 1.91, ''), ('120 Tau', 1869, 1, 24, 8, 47, 42.5, 1.91, '')]
def jd_obs(y, mo, d, h, m, s): return datetime.date(y, mo, d).toordinal() + 1721425.0 + (h * 3600 + m * 60 + s) / 86400.0      # noon of the date + the time
def horizons(tag, tl, lon, ttype):
    fn = HZ + tag + '.txt'
    if not os.path.exists(fn):
        q = {'format': 'text', 'COMMAND': "'301'", 'OBJ_DATA': "'NO'", 'MAKE_EPHEM': "'YES'", 'EPHEM_TYPE': "'OBSERVER'", 'CENTER': "'coord@399'", 'COORD_TYPE': "'GEODETIC'",
             'SITE_COORD': f"'{lon:.7f},{LAT:.6f},{ALT}'", 'TLIST': "'" + ' '.join(f'{x:.8f}' for x in tl) + "'", 'TIME_TYPE': f"'{ttype}'", 'QUANTITIES': "'1,20,30'", 'ANG_FORMAT': "'DEG'",
             'EXTRA_PREC': "'YES'", 'CSV_FORMAT': "'YES'", 'CAL_FORMAT': "'JD'"}
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
def unit(ra, de): ra, de = np.radians(ra), np.radians(de); return np.array([np.cos(de) * np.cos(ra), np.cos(de) * np.sin(ra), np.sin(de)])
def contact(rows, star, jd0):
    """seconds from jd0 at which the star crosses the limb going in (first crossing with the gap shrinking); also the rate of approach in arcsec/s"""
    t = (rows[:, 0] - jd0) * 86400; g = []
    for r in rows:
        sep = np.arccos(np.clip(unit(r[1], r[2]) @ star, -1, 1)); g.append(np.degrees(sep - np.arcsin(RMOON / (r[3] * 149597870.7))) * 3600)
    g = np.array(g)
    for i in range(len(g) - 1):
        if g[i] > 0 >= g[i + 1]: return t[i] + (0 - g[i]) / (g[i + 1] - g[i]) * (t[i + 1] - t[i]), (g[i + 1] - g[i]) / (t[i + 1] - t[i]), g
    return np.nan, np.nan, g
if __name__ == '__main__':
    trial = [float(x) for x in sys.argv[1:]] or [None, 10.0]
    res = {}
    for (name, y, mo, d, h, m, s, dt_table, note) in EVENTS:
        ra0, de0, pmra, pmde, plx = STARS[name]; jd = jd_obs(y, mo, d, h, m, s); yrs = (jd - 2451545.0) / 365.25
        star = unit(ra0 + pmra / 3.6e6 * yrs / np.cos(np.radians(de0)), de0 + pmde / 3.6e6 * yrs)
        tag = f'{name.replace(" ", "").replace(".", "")}_{y}{mo:02d}{d:02d}'
        pre = horizons(tag + '_ut', [jd], LON, 'UT'); dt_jpl = pre[0, -1]
        line = f'{y} {mo:2d}/{d:02d} {name:10s} seen {h}h{m:02d}m{s:04.1f}s (JPL uses {dt_jpl:.2f} s):'
        for dt in trial:
            dt = dt_table if dt is None else dt
            lon = LON + (dt_jpl - dt) * 15.04107 / 3600.0
            tl = [jd + (dt + k * 6.0) / 86400.0 for k in range(-40, 41)]
            rows = horizons(f'{tag}_tt{dt:.2f}', tl, lon, 'TT'); c, rate, g = contact(rows, star, jd + dt / 86400.0)
            res.setdefault(dt if dt != dt_table else 'table', []).append(-c)
            line += f'  correction {dt:5.2f} s -> seen minus computed {-c:+6.1f} s (closing {abs(rate):.3f}"/s)'
        print(line + ('  [' + note + ']' if note else ''))
    for k, v in res.items(): print(f'correction {k}: mean seen-minus-computed {np.nanmean(v):+.1f} s, scatter {np.nanstd(v):.1f} s, n={np.sum(~np.isnan(v))}')
