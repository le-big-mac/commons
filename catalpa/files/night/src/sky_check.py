# Checks src/sky.py against JPL Horizons: the altitude of the Sun and of the Moon every 3 hours for 40 days at four
# places, and the Moon's lit share. Horizons gives apparent altitude without refraction when asked for it
# (QUANTITIES 4 with airless model). Run: python3 -I src/sky_check.py > sky_check.out   (files saved in data/hz/)
import sys, os, re, subprocess, datetime as dt, math, importlib.util
spec = importlib.util.spec_from_file_location('sky', '/home/agent1/night/src/sky.py'); sky = importlib.util.module_from_spec(spec); spec.loader.exec_module(sky)
D = '/home/agent1/night/data/hz/'; os.makedirs(D, exist_ok=True)
SITES = [("Madrid", 40.42, -3.70), ("Linz", 48.30, 14.29), ("La Palma", 28.76, -17.88), ("Cerro Paranal", -24.63, -70.40)]
SPANS = [("2019-01-05", "2019-02-14"), ("2023-06-10", "2023-07-20")]
def fetch(body, name, lat, lon, a, b):
    fn = f"{D}{body}_{name.replace(' ', '_')}_{a}.txt"
    if not os.path.exists(fn):
        url = ("https://ssd.jpl.nasa.gov/api/horizons.api?format=text&COMMAND='%s'&OBJ_DATA='NO'&MAKE_EPHEM='YES'&EPHEM_TYPE='OBSERVER'&CENTER='coord@399'&COORD_TYPE='GEODETIC'"
               "&SITE_COORD='%.4f,%.4f,0'&START_TIME='%s'&STOP_TIME='%s'&STEP_SIZE='3 h'&QUANTITIES='4,10'&APPARENT='AIRLESS'&CSV_FORMAT='YES'" % (body, lon, lat, a, b))
        url = url.replace(" ", "%20").replace("'", "%27")
        subprocess.run(["curl", "-sS", "-g", "-m", "120", "-A", "reading-check/1.0", "-o", fn, url], check=True)
    rows = []; on = False
    for l in open(fn):
        if l.startswith("$$SOE"): on = True; continue
        if l.startswith("$$EOE"): break
        if on:
            p = [x.strip() for x in l.split(",")]
            t = dt.datetime.strptime(p[0], "%Y-%b-%d %H:%M"); rows.append((t, float(p[4]), float(p[5]) if body == '301' else None))
    return rows
print("sky.py against JPL Horizons (airless apparent altitude), every 3 hours")
for name, lat, lon in SITES:
    for a, b in SPANS:
        s = fetch('10', name, lat, lon, a, b); m = fetch('301', name, lat, lon, a, b)
        ds = [sky.sun_alt(t, lat, lon) - el for t, el, _ in s]; dm = [sky.moon_alt(t, lat, lon) - el for t, el, _ in m]; dl = [100 * sky.moon_lit(t) - ill for t, el, ill in m]
        near = [abs(sky.sun_alt(t, lat, lon) - el) for t, el, _ in s if -25 < el < -10]
        print(f"  {name:<14} {a}: {len(s)} times; Sun altitude out by at most {max(map(abs, ds)):.3f} deg (near -18 deg: {max(near) if near else float('nan'):.3f}); Moon altitude by at most {max(map(abs, dm)):.2f} deg, typically {sorted(map(abs, dm))[len(dm) // 2]:.2f}; lit share by at most {max(map(abs, dl)):.1f} points")
