# Geocentric conjunction in right ascension of Sun and Moon, 18 Aug 1868, from JPL Horizons (DE441), apparent places of date, asked for in TT so that the clock correction is mine to apply.
# Compared with the "Elements" printed in the Nautical Almanac for 1868 (computed in 1864 from Hansen's Moon and Le Verrier's Sun).
import numpy as np, subprocess, urllib.parse, os, sys
D = '/home/agent1/wander/hz/conj/'
def fetch(body, tag, start, stop, step):
    fn = D + f'{tag}_{body}.txt'
    if not os.path.exists(fn):
        q = {'format': 'text', 'COMMAND': f"'{body}'", 'OBJ_DATA': "'NO'", 'MAKE_EPHEM': "'YES'", 'EPHEM_TYPE': "'OBSERVER'", 'CENTER': "'500@399'", 'START_TIME': f"'{start}'", 'STOP_TIME': f"'{stop}'",
             'STEP_SIZE': f"'{step}'", 'TIME_TYPE': "'TT'", 'QUANTITIES': "'2,20,30'", 'ANG_FORMAT': "'DEG'", 'EXTRA_PREC': "'YES'", 'CSV_FORMAT': "'YES'", 'CAL_FORMAT': "'JD'"}
        subprocess.run(['curl', '-s', '-m', '120', '-A', 'ephemeris-check/1.0', 'https://ssd.jpl.nasa.gov/api/horizons.api?' + urllib.parse.urlencode(q), '-o', fn], check=True)
    rows = []; on = False
    for line in open(fn):
        if line.startswith('$$SOE'): on = True; continue
        if line.startswith('$$EOE'): break
        if on:
            w = [x.strip() for x in line.split(',')]; v = []
            for x in w:
                try: v.append(float(x))
                except ValueError: pass
            rows.append(v)
    return np.array(rows)
def hms(h): h = h % 24; return f'{int(h):02d}h{int(h*60%60):02d}m{h*3600%60:05.2f}s'
def dms(d): s = '-' if d < 0 else '+'; d = abs(d); return f'{s}{int(d):02d}d{int(d*60%60):02d}\'{d*3600%60:04.1f}"'
def conj(tag, start, stop, jd0, dT, na_gmt_h, na_ra_h, na_dm, na_ds):
    m, s = fetch(301, tag, start, stop, '36'), fetch(10, tag, start, stop, '36')
    if len(m) == 0: print('no rows', tag); return
    jd, d = m[:, 0], m[:, 1] - s[:, 1]                       # JD (TT), RA Moon - RA Sun in degrees
    i = np.where(np.diff(np.sign(d)) != 0)[0][0]; f = (0 - d[i]) / (d[i + 1] - d[i]); jc = jd[i] + f * (jd[i + 1] - jd[i])
    ra = s[i, 1] + f * (s[i + 1, 1] - s[i, 1]); dm = m[i, 2] + f * (m[i + 1, 2] - m[i, 2]); ds = s[i, 2] + f * (s[i + 1, 2] - s[i, 2])
    rate = (d[i + 1] - d[i]) * 3600 / 10.0                    # arcsec of RA per second of time
    tt_h = (jc - jd0) * 24; ut_h = tt_h - dT / 3600
    print(f'{tag}: JPL conjunction in right ascension {hms(tt_h)} TT = {hms(ut_h)} UT with clock correction {dT} s (JPL itself would use {m[i, -1]:.2f} s)')
    print(f'      almanac: {hms(na_gmt_h)} Greenwich mean time  ->  almanac minus JPL = {(na_gmt_h - ut_h) * 3600:+.1f} s of time = {-(na_gmt_h - ut_h) * 3600 * rate:+.1f} arcsec of Moon-minus-Sun in right ascension (rate {rate:.4f} arcsec/s)')
    print(f'      right ascension at conjunction: JPL {hms(ra / 15)}, almanac {hms(na_ra_h)}  (JPL minus almanac {(ra / 15 - na_ra_h) * 3600:+.2f} s of time)')
    print(f'      declinations at conjunction: Moon JPL {dms(dm)}, almanac {dms(na_dm)} ({(dm - na_dm) * 3600:+.1f}");  Sun JPL {dms(ds)}, almanac {dms(na_ds)} ({(ds - na_ds) * 3600:+.1f}")')
if __name__ == '__main__':
    # 1868 Aug 18 0h UT = JD 2403562.5.  Almanac (OCR, to be checked on the page image): conjunction Aug 17d 17h 13m 5.3s GMT (astronomical day from noon) = 05:13:05.3 on the 18th
    conj('1868', '1868-Aug-18 05:10:00', '1868-Aug-18 05:16:00', 2403562.5, 2.47, 5 + 13 / 60 + 5.3 / 3600, 9 + 51 / 60 + 0.25 / 3600, 12 + 59 / 60 + 16.6 / 3600, 13 + 2 / 60 + 6.0 / 3600)
