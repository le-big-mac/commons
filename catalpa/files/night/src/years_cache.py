# Saves, for every cleaned night of a year by the frozen method (dawnlib.py), the few figures later looks need, so that
# they need not read the photometer files again. Usage: years_cache.py YEAR FOLDER  ->  cache/nights<YEAR>.pkl
import sys, pickle, importlib.util, datetime as dt
import numpy as np
spec = importlib.util.spec_from_file_location('dawnlib', '/home/agent1/night/src/dawnlib.py'); D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
year = int(sys.argv[1]); folder = sys.argv[2]; out = []
for c in D.load(year, folder):
    if not c['clean']: continue
    k, mt = D.tenth(c)
    gb = [D.gal_b(c['dusk'] + dt.timedelta(hours=float((j + 0.5) / 10 * c['L'])), c['lat'], c['lon']) for j in range(10)]
    out.append(dict(st=c['st'], cls=D.CLASS[c['st']], name=D.NAME[c['st']], d=c['d'], lat=c['lat'], lon=c['lon'], L=c['L'], dusk=c['dusk'], dawn=c['dawn'],
                    mt=[float(x) for x in mt], tenth=k, near=D.last_near(c), ends=D.has_ends(c), dd=(D.dd(c) if D.has_ends(c) else None), gb=gb, season=D.season(c), lev=float(np.median(c['m']) - c['off'])))
import os; os.makedirs('/home/agent1/night/cache', exist_ok=True)
pickle.dump(out, open(f'/home/agent1/night/cache/nights{year}.pkl', 'wb'))
print(year, len(out), 'cleaned nights saved')
