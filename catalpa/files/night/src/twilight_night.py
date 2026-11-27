# Does the night reading follow the twilight? For the sixteen photometers: the drift of the night level (the middle
# raw-count reading of each cleaned night, cache2/) fitted the same way as the twilight's (each calendar month's own
# level and one rate), beside the twilight drift (cache2/twilight16.pkl). Unsealed: a look before a sheet is written.
import pickle, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('twilight', '/home/agent1/night/src/twilight.py'); TW = importlib.util.module_from_spec(spec); spec.loader.exec_module(TW)
R = pickle.load(open('/home/agent1/night/cache2/twilight16.pkl', 'rb'))
N = [c for y in range(2016, 2027) for c in pickle.load(open(f'/home/agent1/night/cache2/nights{y}.pkl', 'rb'))]
NAME = {c['st']: c['name'] for c in N}; CLS = {c['st']: c['cls'] for c in N}
order = ['stars33', 'stars76', 'stars1', 'stars52', 'stars7', 'stars36', 'stars19', 'stars9', 'stars225', 'stars4', 'stars24', 'stars426', 'stars35', 'stars477', 'stars62', 'stars289']
print('place                 kind      twilight drift   night drift (all cleaned nights)   night drift (level far from the Milky Way)   months of nights')
tw, nt = [], []
for st in order:
    V = {}; sl = []
    for (s, y, m), r in R.items():
        if s != st or r is None: continue
        mv = TW.month_value(r)
        if mv: V[(y, m)] = mv[0]; sl += r['sl']
    d = TW.drift(V, float(np.median(sl))) if V else None
    def nightdrift(key):
        g = {}
        for c in N:
            if c['st'] == st and c.get(key) is not None: g.setdefault((c['dusk'].year, c['dusk'].month), []).append(c[key])
        M = {k: float(np.median(v)) for k, v in g.items()}
        return TW.drift(M, 1.0), len(M)
    (n1, k1), (n2, k2) = nightdrift('levall'), nightdrift('lev40')
    print(f"{NAME[st]:<20}  {CLS[st]:<8}  " + (f'{d[0]:+.3f} ({d[1]:.3f})' if d else '      -      ') + '    ' + (f'{n1[0]:+.3f} ({n1[1]:.3f})' if n1 else '      -      ') + '                  ' + (f'{n2[0]:+.3f} ({n2[1]:.3f})' if n2 else '      -      ') + f'                 {k1}, {k2}')
    if d and n1: tw.append(d[0]); nt.append(n1[0])
tw = np.array(tw); nt = np.array(nt)
print(f'\nacross the {len(tw)} places with both: correlation of night drift with twilight drift {np.corrcoef(tw, nt)[0, 1]:+.2f}; straight line through them: night = {np.polyfit(tw, nt, 1)[0]:.2f} x twilight {np.polyfit(tw, nt, 1)[1]:+.3f}')
print('the differences, night less twilight: ' + ' '.join(f'{x:+.3f}' for x in nt - tw))
