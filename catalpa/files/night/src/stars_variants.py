# The sealed lines (stars_sheet.py, run unchanged) on other choices of nights, after the score was known:
#   screened   : every night whose level departs by more than 1 magnitude from the station's usual level in 2024 left out
#                (a screen that does not depend on the station's level in the same year; it removes Santa Cruz de La
#                Palma's nights of 2022, which read 15.4 and cannot be the sky)
#   asfetched  : 2023 as the frozen method first ran it, with Arkaroola's January to May files given its later position
# Each variant's nights are written to their own folder and the sealed program's text is run on that folder.
import os, sys, pickle, io, contextlib
import numpy as np
BASE = '/home/agent1/night/'
ref = pickle.load(open(BASE + 'cache/nights2024.pkl', 'rb')); lev24 = {}
for st in {c['st'] for c in ref}: lev24[st] = float(np.median([c['lev'] for c in ref if c['st'] == st]))
def screened(N): return [c for c in N if abs(c['lev'] - lev24[c['st']]) <= 1.0]
def write(folder, sets):
    os.makedirs(BASE + folder, exist_ok=True)
    for y, N in sets.items(): pickle.dump(N, open(BASE + f'{folder}/nights{y}.pkl', 'wb'))
load = lambda name: pickle.load(open(BASE + f'cache/{name}.pkl', 'rb'))
Y = {y: load(f'nights{y}') for y in (2022, 2023, 2024, 2025)}
print('nights left out by the screen against the 2024 level:')
for y in Y:
    out = [c for c in Y[y] if abs(c['lev'] - lev24[c['st']]) > 1.0]
    print(f"  {y}: {len(out)} of {len(Y[y])}" + (': ' + ', '.join(f"{c['name']} {c['d']} ({c['lev']:.1f})" for c in out) if out else ''))
write('cache_screened', {y: screened(Y[y]) for y in Y})
write('cache_asfetched', {2022: Y[2022], 2023: load('nights2023_asfetched'), 2024: Y[2024], 2025: Y[2025]})
write('cache_asfetched_screened', {2022: screened(Y[2022]), 2023: screened(load('nights2023_asfetched')), 2024: Y[2024], 2025: Y[2025]})
src = open(BASE + 'src/stars_sheet.py').read()
def run(folder, a, b):
    code = src.replace("/home/agent1/night/cache/nights", BASE + folder + '/nights'); assert code != src
    old = sys.argv; sys.argv = ['stars_sheet.py', a, b]; buf = io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code, 'stars_sheet.py', 'exec'), {'__name__': '__main__'})
    sys.argv = old; return buf.getvalue()
for lab, folder, a, b in (('screened: 2022 and 2023', 'cache_screened', '2024,2025', '2022,2023'),
                          ('as fetched: 2022 and 2023', 'cache_asfetched', '2024,2025', '2022,2023'),
                          ('as fetched and screened: 2022 and 2023', 'cache_asfetched_screened', '2024,2025', '2022,2023'),
                          ('screened: 2022 alone', 'cache_screened', '2024,2025', '2022'),
                          ('screened: 2023 alone', 'cache_screened', '2024,2025', '2023'),
                          ('screened: all four years together', 'cache_screened', '2024,2025', '2022,2023,2024,2025')):
    txt = run(folder, a, b); print('\n=== ' + lab + ' ===')
    for line in txt.split('\n'):
        if line.startswith('S') or line.startswith('learned') or 'all nights (' in line or line.startswith('   end of the night'): print(line[:400])
