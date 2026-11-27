# After the checker showed from the twilight readings that the photometer stars477 stood at Arkaroola all through 2022
# and 2023 (check/where477.out), this runs the frozen method on a year's files as fetched, giving that station the
# position its later headers carry wherever a header has none. Otherwise it is years_cache.py; the frozen dawnlib.py is
# not changed. Usage: years_cache_placed.py YEAR FOLDER  ->  cache_placed/nights<YEAR>.pkl
import sys, os, pickle, importlib.util, datetime as dt
import numpy as np
spec = importlib.util.spec_from_file_location('dawnlib', '/home/agent1/night/src/dawnlib.py'); D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
PLACE = {'stars477': (-30.3116867, 139.3358408, 'Arkaroola Wilderness Sanctuary')}
_read = D.read_full
def read_full(st, year, folder):
    r = _read(st, year, folder)
    if r is not None and (r[6] is None or r[7] is None) and st in PLACE:
        r = r[:6] + (PLACE[st][0], PLACE[st][1], PLACE[st][2]); print(f'{st} {year}: no position in any header; placed at {PLACE[st][0]}, {PLACE[st][1]}')
    return r
D.read_full = read_full
year = int(sys.argv[1]); folder = sys.argv[2]; out = []
for c in D.load(year, folder):
    if not c['clean']: continue
    k, mt = D.tenth(c)
    gb = [D.gal_b(c['dusk'] + dt.timedelta(hours=float((j + 0.5) / 10 * c['L'])), c['lat'], c['lon']) for j in range(10)]
    out.append(dict(st=c['st'], cls=D.CLASS[c['st']], name=D.NAME[c['st']], d=c['d'], lat=c['lat'], lon=c['lon'], L=c['L'], dusk=c['dusk'], dawn=c['dawn'],
                    mt=[float(x) for x in mt], tenth=k, near=D.last_near(c), ends=D.has_ends(c), dd=(D.dd(c) if D.has_ends(c) else None), gb=gb, season=D.season(c), lev=float(np.median(c['m']) - c['off'])))
os.makedirs('/home/agent1/night/cache_placed', exist_ok=True)
pickle.dump(out, open(f'/home/agent1/night/cache_placed/nights{year}.pkl', 'wb'))
print(year, len(out), 'cleaned nights saved')
