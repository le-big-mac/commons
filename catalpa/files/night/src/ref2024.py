# Each station's 2024 level (by the file's formula, on the frozen method's cleaned nights) and the middle altitude of the
# Sun, at the station's home, at the moments its 2024 readings passed 14.0 magnitudes in twilight. dawnlib2.py measures
# other years against these. Writes cache2/ref2024.pkl and prints the table.
import pickle, importlib.util, datetime as dt
import numpy as np
spec = importlib.util.spec_from_file_location('dawnlib2', '/home/agent1/night/src/dawnlib2.py'); L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
D = L.D; N = pickle.load(open('/home/agent1/night/cache_placed/nights2024.pkl', 'rb')); ref = {'lev': {}, 'cross': {}}
print('station      2024 level   twilight crossings (evening, morning)   middle Sun altitude   evening and morning apart   scatter')
for st in D.STATIONS:
    ref['lev'][st] = float(np.median([c['lev'] for c in N if c['st'] == st]))
    r = D.read_full(st, 2024, '/home/agent1/night/data/ida'); ev, mo = L.crossings(r[0], r[1], dt.datetime(2024, 1, 1), *L.HOME[st])
    allc = np.array(ev + mo); ref['cross'][st] = float(np.median(allc)) if len(allc) else None
    print(f"{st:<10} {ref['lev'][st]:8.2f}   {len(ev):>5} {len(mo):>5}   {np.median(allc):+6.2f}   {abs(np.median(ev) - np.median(mo)):5.2f}   {1.4826 * np.median(np.abs(allc - np.median(allc))):5.2f}")
pickle.dump(ref, open('/home/agent1/night/cache2/ref2024.pkl', 'wb'))
