# Before the third sheet is sealed: what do its measures give on made-up nights of known kind? The real nights' frames
# are kept (place, date, dusk, dawn, the ten distances of the point overhead from the Milky Way's plane), and only the
# ten part-means are made up, with noise and rounded to 0.01 as the real means nearly are:
#   stars  : darker the further the point overhead is from the plane (0.5 magnitude between the plane and far from it)
#   clock  : darkening until one o'clock in the morning by the Sun, flat after
#   slope  : darkening all night at 0.03 magnitude an hour
#   nothing: flat
#   notch  : one dark patch fixed to the stars, darkest when star time is 1 h, about five hours wide, 0.3 magnitude deep
#   stars+slope, notch+slope: the same with a darkening of 0.03 magnitude an hour added
# Reads cache/nights2024.pkl and nights2025.pkl. Twenty draws of each kind.
import pickle, importlib.util, datetime as dt
import numpy as np
spec = importlib.util.spec_from_file_location('sky', '/home/agent1/night/src/sky.py'); sky = importlib.util.module_from_spec(spec); spec.loader.exec_module(sky)
N = []
for y in (2024, 2025):
    for c in pickle.load(open(f'/home/agent1/night/cache/nights{y}.pkl', 'rb')):
        st = lambda t: ((sky.gmst_deg(sky.jd(t)) + c['lon']) % 360) / 15.0
        c['lst0'] = st(c['dusk']); c['lst1'] = st(c['dawn']); c['doy'] = (c['d'] - dt.date(c['d'].year, 1, 1)).days
        c['mid'] = [c['dusk'] + dt.timedelta(hours=(j + 0.5) / 10 * c['L']) for j in range(10)]
        c['solj'] = []
        for tm in c['mid']:
            s = (tm.hour + tm.minute / 60 + tm.second / 3600 + c['lon'] / 15.0) % 24; c['solj'].append(s - 24 if s > 12 else s)
        c['lstj'] = [st(tm) for tm in c['mid']]; N.append(c)
rng = np.random.default_rng(20261127)
def make(c, kind, noise):
    gb = np.array(c['gb']); sol = np.array(c['solj']); hrs = (np.arange(10) + 0.5) / 10 * c['L']
    lst = np.array(c['lstj']); dl = np.minimum(np.abs(lst - 1.0), 24 - np.abs(lst - 1.0))
    if kind == 'stars': m = 21.6 - 0.5 * np.exp(-gb / 20.0)
    elif kind == 'stars+slope': m = 21.6 - 0.5 * np.exp(-gb / 20.0) + 0.03 * hrs
    elif kind == 'notch': m = 21.0 + 0.3 * np.exp(-(dl / 2.5) ** 2)
    elif kind == 'notch+slope': m = 21.0 + 0.3 * np.exp(-(dl / 2.5) ** 2) + 0.03 * hrs
    elif kind == 'clock': m = 19.0 + 0.10 * np.minimum(sol, 1.0)
    elif kind == 'slope': m = 20.0 + 0.03 * hrs
    else: m = np.full(10, 20.0)
    return np.round(m + rng.normal(0, noise, 10), 2)
def covers(c, h):
    a, b = c['lst0'], c['lst1']; mid = h + 1.0
    return (a <= mid <= b) if a <= b else (mid >= a or mid <= b)
def inspan(x, spans): return any(lo <= x < hi for lo, hi in spans)
def measures(S, kind, noise):
    k = [int(np.argmax(make(c, kind, noise))) for c in S]
    sol = np.array([c['solj'][j] for c, j in zip(S, k)]); lst = np.array([c['lstj'][j] for c, j in zip(S, k)]); doy = np.array([c['doy'] for c in S]); last = np.array(k) == 9
    aut = (doy >= 213) & (doy < 304); r = float(np.polyfit(doy[aut], sol[aut] * 60, 1)[0]) if aut.sum() >= 20 else float('nan')
    l1 = np.array([c['lst1'] for c in S]); bad = np.array([inspan(x, ((4, 6), (18, 20))) for x in l1]); good = np.array([inspan(x, ((22, 24), (0, 2), (12, 14))) for x in l1])
    c0 = np.array([covers(c, 0) for c in S]); c20 = np.array([covers(c, 20) for c in S]); sep = np.array([c['d'].month == 9 for c in S])
    cor = float(np.median([np.corrcoef(make(c, kind, noise), c['gb'])[0, 1] if np.std(make(c, kind, noise)) > 0 else 0.0 for c in S]))
    return [r, 100 * last[bad].mean(), 100 * last[good].mean(), 100 * ((lst >= 0) & (lst < 2))[c0].mean(), 100 * ((lst >= 20) & (lst < 22))[c20].mean(), 100 * last[sep].mean(), cor, 100 * last.mean(), 100 * (np.array(k) >= 8).mean(), 100 * (np.array(k) >= 5).mean()]
S = [c for c in N if c['lat'] > 0 and c['cls'] in ('between', 'dark')]
print(f'made-up nights on the frames of the {len(S)} real nights at northern places not in towns, 2024 and 2025; twenty draws; the middle draw, and the range')
print('measure: [1] minutes a day, August to October  [2] last tenth darkest when dawn is at star time 4-6 or 18-20 h  [3] when at 22-2 or 12-14 h  [4] darkest tenth at 0-2 h  [5] at 20-22 h  [6] September, last tenth darkest  [7] correlation with distance from the plane  [8] last tenth darkest, all  [9] ninth or last  [10] second half')
for kind in ('stars', 'stars+slope', 'notch', 'notch+slope', 'clock', 'slope', 'nothing'):
    for noise in (0.01, 0.03):
        R = np.array([measures(S, kind, noise) for _ in range(20)]); md = np.median(R, 0); lo = R.min(0); hi = R.max(0)
        print(f'{kind:<12} noise {noise}: ' + '  '.join(f'[{i + 1}] {md[i]:+.1f} ({lo[i]:+.1f} to {hi[i]:+.1f})' if i in (0, 6) else f'[{i + 1}] {md[i]:.0f} ({lo[i]:.0f} to {hi[i]:.0f})' for i in range(10)))
print('\nthe same on the frames of the three northern dark places alone (the drift measure of line S1), and of the five towns (S2)')
for lab, S2 in (('dark', [c for c in N if c['lat'] > 0 and c['cls'] == 'dark']), ('between', [c for c in N if c['lat'] > 0 and c['cls'] == 'between']), ('towns', [c for c in N if c['cls'] == 'lit'])):
    for kind in ('stars', 'stars+slope', 'notch', 'notch+slope', 'clock', 'slope', 'nothing'):
        R = np.array([measures(S2, kind, 0.02)[0] for _ in range(40)]); print(f'{lab:<8}{kind:<12}: minutes a day {np.median(R):+.1f} ({R.min():+.1f} to {R.max():+.1f}; {len(S2)} nights)')
