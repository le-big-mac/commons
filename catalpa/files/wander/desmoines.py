# The eclipse of 7 August 1869 at Des Moines, Iowa (Newcomb's station): the same code as for 1868, as a test of the method.  Lines U1-U3 in ~/journal.md, written first.
import sys, numpy as np, importlib.util
sys.argv = ['x']; spec = importlib.util.spec_from_file_location('core', '/home/agent1/wander/ecl1869_core.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
JPL = -2.5 / 86400.0; hms = m.hms
ev = m.eclipse2.find('/home/agent1/orrery/states_1869.txt')
for jd, g in ev: print(f'geocentric greatest eclipse: {m.eclipse2.cal(jd)} TT, gamma {g:+.4f}')
WASH = 77 + 3 / 60 + 2.3 / 3600                       # the old Naval Observatory, west longitude, as I remember it
lat, lonw = 41 + 35 / 60 + 4 / 3600, WASH + (1 + 6 / 60 + 17.0 / 3600) * 15; lon = -lonw
print(f'Newcomb\'s station: {lat:.4f} N, {lonw:.4f} W ({int(lonw)}d{(lonw % 1) * 60:.2f}\')')
OBS = {'c1': ('first contact', 3, 43, 2.1), 'c3': ('end of totality', 4, 48, 25.2), 'c4': ('last contact', 5, 45, 23.7)}
for dt in (1.4, 8.0):
    m.DT = dt / 86400.0; xyz = m.site(lat, lon, 260.0)
    for k, kn in ((m.K_IAU, 'standard lunar radius'), (m.K_SMALL, 'smaller lunar radius')):
        c = m.contacts(xyz, k); row = []
        for key in ('c1', 'c2', 'c3', 'c4'):
            lmt = ((c[key] + JPL - m.DT + 0.5 + lon / 360.0) % 1.0) * 86400 - 43200; row.append((key, lmt))
        print(f'clock correction {dt:4.1f} s, {kn:22s}: ' + '  '.join(f'{key} {hms((v + 43200) / 86400)}' for key, v in row) + f'   totality {(c["c3"] - c["c2"]) * 86400:.1f} s')
        for key, v in row:
            if key in OBS and ((k == m.K_IAU) or key == 'c3'):
                n, h, mi, s = OBS[key]; print(f'        {n}: Newcomb {h}h{mi:02d}m{s:04.1f}s p.m.; observed minus computed {(h * 3600 + mi * 60 + s) - v:+.1f} s')
