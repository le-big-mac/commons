"""Fetch geocentric observer tables from JPL Horizons (DE441) for the Antikythera study.
usage: fetch.py OUTDIR [test]
Each table: JD (TT), astrometric RA/Dec (ICRF), apparent ecliptic longitude/latitude of date.
One request at a time, a pause between requests, nothing about us in the request."""
import sys, time, urllib.parse, urllib.request, os
OUT = sys.argv[1]
TEST = len(sys.argv) > 2
BODIES = {'sun': '10', 'moon': '301', 'mercury': '199', 'venus': '299', 'mars': '4', 'jupiter': '5', 'saturn': '6'}   # system barycentres: the planet centres are not in the long ephemeris before 1600
T0 = 1646667.5            # 1 May 205 BC (Julian calendar), 0h TT
T1 = 2461368.0            # 23 Nov 2026, 12h TT
SPAN = 27759.0            # 76 Julian years, one Callippic period
WINDOWS = {'then': (T0, T0 + SPAN), 'now': (T1 - SPAN, T1)}
def get(body, w, step):
    a, b = WINDOWS[w]
    if TEST: b = a + 3
    q = {'format': 'text', 'COMMAND': f"'{BODIES[body]}'", 'OBJ_DATA': "'NO'", 'MAKE_EPHEM': "'YES'",
         'EPHEM_TYPE': "'OBSERVER'", 'CENTER': "'500@399'", 'START_TIME': f"'JD {a}'", 'STOP_TIME': f"'JD {b}'",
         'STEP_SIZE': f"'{step}'", 'QUANTITIES': "'1,31'", 'TIME_TYPE': "'TT'", 'CAL_FORMAT': "'JD'",
         'ANG_FORMAT': "'DEG'", 'CSV_FORMAT': "'YES'", 'EXTRA_PREC': "'YES'"}
    url = 'https://ssd.jpl.nasa.gov/api/horizons.api?' + urllib.parse.urlencode(q)
    req = urllib.request.Request(url, headers={'User-Agent': 'research-script/1.0'})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                return r.read().decode('utf-8', 'replace')
        except Exception as e:
            print('  retry after', repr(e)[:80]); time.sleep(20 * (attempt + 1))
    raise SystemExit('failed: ' + body + ' ' + w)
for w in WINDOWS:
    for body in BODIES:
        step = '8h' if body == 'moon' else '1d'
        f = os.path.join(OUT, f"{body}_{w}{'_test' if TEST else ''}.txt")
        if os.path.exists(f) and os.path.getsize(f) > 1000 and not TEST:
            print('have', f); continue
        t = get(body, w, step)
        open(f, 'w').write(t)
        n = 0
        if '$$SOE' in t: n = t.split('$$SOE')[1].split('$$EOE')[0].count('\n') - 1
        print(body, w, len(t), 'bytes,', n, 'rows'); sys.stdout.flush()
        if TEST and body == 'moon': break
        time.sleep(3)
    if TEST: break
