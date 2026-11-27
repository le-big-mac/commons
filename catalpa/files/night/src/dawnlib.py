# The method of the dawn page as it stood after the checker's three readings (27 November 2026), frozen in one place
# and made to take the year as an argument, so that a second year can be put through exactly what the first was.
# Nothing here looks at a result: it reads files, picks nights and computes each night's figures.
#   nights      : end of evening astronomical twilight to start of morning astronomical twilight (Sun 18 degrees down),
#                 five hours or more, Moon below the horizon at every ten-minute step (as dawn.py had it)
#   readings    : reduced to one a minute (the median within the minute); covered if 90 in 100 of minutes have one
#   clear       : spread about a 61-minute running median no more than twice the station's floor (its 20th percentile)
#   the sky     : the night's middle reading within 1 magnitude of the station's own level
#   infrared    : sky temperature within 1.5 C of its hour-long running median for 95 in 100 of the night, and enclosure
#                 less sky at least half the station's best tenth; a station with no temperatures is not tested
#   cleaned set : clear, the sky, and not failing the infrared test
#   darkest tenth: the night in ten equal parts by time; the part with the largest mean reading (larger is darker);
#                 an exact tie goes to the earlier part
import os, re, glob, math, datetime as dt, importlib.util
import numpy as np
_spec = importlib.util.spec_from_file_location('sky', '/home/agent1/night/src/sky.py'); sky = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(sky)
STATIONS = ['stars1', 'stars4', 'stars7', 'stars9', 'stars19', 'stars24', 'stars33', 'stars35', 'stars36', 'stars52', 'stars62', 'stars76', 'stars225', 'stars289', 'stars426', 'stars477']
# classes from the 2024 levels by each file's own formula (dawn_recheck.out, part I); fixed, not derived again
CLASS = {'stars33': 'lit', 'stars76': 'lit', 'stars1': 'lit', 'stars52': 'lit', 'stars7': 'lit',
         'stars36': 'between', 'stars19': 'between', 'stars9': 'between', 'stars225': 'between', 'stars4': 'between', 'stars24': 'between', 'stars426': 'between',
         'stars35': 'dark', 'stars477': 'dark', 'stars62': 'dark', 'stars289': 'dark'}
NAME = {'stars33': "Madrid ring road", 'stars76': "Valencia", 'stars1': "Coslada", 'stars52': "Almería", 'stars7': "Pamplona", 'stars36': "Northampton, USA", 'stars4': "La Palma, a town", 'stars19': "Tucson, USA",
        'stars9': "Añora", 'stars225': "Morata de Jalón", 'stars24': "Temisas", 'stars426': "Teide Observatory", 'stars62': "Àger", 'stars35': "Otlica", 'stars477': "Arkaroola", 'stars289': "Nerpio"}
def runmed(x, w):
    n = len(x); h = w // 2; out = np.empty(n)
    for i in range(n): out[i] = np.median(x[max(0, i - h):min(n, i + h + 1)])
    return out
def spread(m):
    r = m - runmed(m, 61); return 1.4826 * np.median(np.abs(r - np.median(r)))
def slope(t, m): return float(np.polyfit(t, m, 1)[0])
def read_full(st, year, folder):
    t0 = dt.datetime(year, 1, 1); T, M, TE, TS, FQ, ZP, lat, lon, place = [], [], [], [], [], [], None, None, ''
    for fn in sorted(glob.glob(os.path.join(folder, f'{st}_{year}-??.dat'))):
        txt = open(fn, encoding='utf-8', errors='replace').read()
        if '# END OF HEADER' not in txt: continue
        head, body = txt.split('# END OF HEADER', 1)
        m = re.search(r'# Position: ([-\d.]+), ([-\d.]+)', head)
        if m: lat, lon = float(m.group(1)), float(m.group(2))
        m = re.search(r'# Location name: (.*)', head)
        if m: place = m.group(1).split('/')[0].strip()
        for line in body.splitlines():
            p = line.split(';')
            if len(p) < 7: continue
            try: v = float(p[5]); te = float(p[2]); ts = float(p[3]); fq = float(p[4]); zp = float(p[6]); t = dt.datetime.strptime(p[0][:19], '%Y-%m-%dT%H:%M:%S')
            except ValueError: continue
            T.append((t - t0).total_seconds()); M.append(v); TE.append(te); TS.append(ts); FQ.append(fq); ZP.append(zp)
    if not T: return None
    o = np.argsort(T); g = lambda x: np.array(x)[o]
    return g(T), g(M), g(TE), g(TS), g(FQ), g(ZP), lat, lon, place
def _cross(lat, lon, a, b):
    f = lambda t: sky.sun_alt(t, lat, lon) + 18.0
    for _ in range(22):
        mid = a + (b - a) / 2
        if (f(mid) > 0) == (f(a) > 0): a = mid
        else: b = mid
    return a + (b - a) / 2
def nights(lat, lon, year):
    out = []; d = dt.date(year - 1, 12, 31)
    while d <= dt.date(year, 12, 31):
        noon = dt.datetime(d.year, d.month, d.day, 12) - dt.timedelta(hours=lon / 15)
        ts = [noon + dt.timedelta(minutes=10 * k) for k in range(145)]; al = [sky.sun_alt(t, lat, lon) for t in ts]
        dusk = dawn = None
        for k in range(144):
            if al[k] >= -18 > al[k + 1] and dusk is None: dusk = _cross(lat, lon, ts[k], ts[k + 1])
            if al[k] < -18 <= al[k + 1] and dusk is not None and dawn is None: dawn = _cross(lat, lon, ts[k], ts[k + 1])
        if dusk and dawn and (dawn - dusk).total_seconds() >= 5 * 3600:
            moon = max(sky.moon_alt(dusk + dt.timedelta(minutes=10 * k), lat, lon) for k in range(int((dawn - dusk).total_seconds() // 600) + 2))
            out.append((d, dusk, dawn, moon))
        d += dt.timedelta(days=1)
    return out
def load(year, folder):
    """every moonless, covered night of the year at the sixteen stations, with the flags clear, sky, ir and clean"""
    t0 = dt.datetime(year, 1, 1); N = []
    for st in STATIONS:
        r = read_full(st, year, folder)
        if r is None: continue
        tsec, M, TE, TS, FQ, ZP, lat, lon, place = r; cand = []
        for d, dusk, dawn, moon in nights(lat, lon, year):
            if moon >= 0: continue
            a = (dusk - t0).total_seconds(); b = (dawn - t0).total_seconds(); i0, i1 = np.searchsorted(tsec, a), np.searchsorted(tsec, b)
            sel = slice(i0, i1); good = M[sel] > 0
            if good.sum() < 10: continue
            mins = np.floor((tsec[sel][good] - a) / 60).astype(int); nmin = int((b - a) // 60); um = np.unique(mins)
            if len(um) < 0.9 * nmin: continue
            med = lambda x: np.array([np.median(x[sel][good][mins == k]) for k in um])
            fq = FQ[sel][good]; pos = fq > 0; off = float(np.median(M[sel][good][pos] - (ZP[sel][good][pos] - 2.5 * np.log10(fq[pos])))) if pos.sum() > 10 else 0.0
            m = med(M); cand.append(dict(st=st, place=place, d=d, L=(b - a) / 3600, t=(um + 0.5) / 60, m=m, ts=med(TS), te=med(TE), s=spread(m), dusk=dusk, dawn=dawn, lon=lon, lat=lat, off=off))
        if not cand: continue
        floor = float(np.percentile([c['s'] for c in cand], 20)); best = float(np.percentile([np.median(c['te'] - c['ts']) for c in cand], 90))
        cl = [c for c in cand if c['s'] <= 2 * floor]; lev0 = float(np.median([np.median(c['m']) for c in cl])) if cl else float('nan')
        for c in cand:
            c['clear'] = c['s'] <= 2 * floor; c['sky'] = bool(abs(np.median(c['m']) - lev0) <= 1.0)
            if np.all(c['ts'] == 0) or best <= 1: c['ir'] = None
            else: c['ir'] = bool(np.percentile(np.abs(c['ts'] - runmed(c['ts'], 61)), 95) <= 1.5 and np.median(c['te'] - c['ts']) >= 0.5 * best)
            c['clean'] = c['clear'] and c['sky'] and c['ir'] is not False; N.append(c)
    return N
def tenth(c):
    b = np.minimum((c['t'] / c['L'] * 10).astype(int), 9); mt = np.array([c['m'][b == k].mean() if np.any(b == k) else -np.inf for k in range(10)]); return int(np.argmax(mt)), mt
def last_near(c, tol=0.02):
    mt = tenth(c)[1]; return bool(mt.max() - mt[9] <= tol)
def has_ends(c): return bool(np.any(c['t'] >= c['L'] - 0.5) and np.any(c['t'] <= 0.5))
def dd(c): return float(np.median(c['m'][c['t'] >= c['L'] - 0.5]) - np.median(c['m'][c['t'] <= 0.5]))
def gal_b(tu, lat, lon):
    lst = (sky.gmst_deg(sky.jd(tu)) + lon) % 360; a = math.radians(lst); d = math.radians(lat); an, dn = math.radians(192.85948), math.radians(27.12825)
    return abs(math.degrees(math.asin(math.sin(d) * math.sin(dn) + math.cos(d) * math.cos(dn) * math.cos(a - an))))
def milky(c):
    """share (in 100) of the night's minutes, taken every five, at which the point overhead is nearer the plane of the Milky Way than at the middle of the darkest tenth"""
    k = tenth(c)[0]; bm = gal_b(c['dusk'] + dt.timedelta(hours=float((k + 0.5) / 10 * c['L'])), c['lat'], c['lon'])
    b = np.array([gal_b(c['dusk'] + dt.timedelta(hours=float(x)), c['lat'], c['lon']) for x in c['t'][::5]]); return float(100 * np.mean(b < bm))
def season(c):
    m = c['d'].month if c['lat'] > 0 else (c['d'].month + 5) % 12 + 1
    return 'summer' if m in (5, 6, 7, 8) else ('winter' if m in (11, 12, 1, 2) else 'between')
def figures(N):
    """the figures the page gives, from the cleaned set; returns a dict"""
    clean = [c for c in N if c['clean']]; F = {}
    tn = np.array([tenth(c)[0] for c in clean]); F['nights'] = len(clean); F['last'] = float(100 * np.mean(tn == 9)); F['second'] = float(100 * np.mean(tn >= 5)); F['by_tenth'] = [int(np.sum(tn == k)) for k in range(10)]
    def before(sel):
        v = [dd(c) > 0 for c in sel if has_ends(c)]; return (float(100 * np.mean(v)) if v else float('nan'), int(np.sum(v)), len(v))
    for k in ('lit', 'between', 'dark'): F['before_' + k] = before([c for c in clean if CLASS[c['st']] == k])
    F['before_two_darkest'] = before([c for c in clean if c['st'] in ('stars289', 'stars477')]); F['before_otlica_ager'] = before([c for c in clean if c['st'] in ('stars35', 'stars62')])
    for s in ('summer', 'winter'):
        v = [last_near(c) for c in clean if CLASS[c['st']] == 'lit' and season(c) == s]; F['towns_' + s] = (float(100 * np.mean(v)) if v else float('nan'), int(np.sum(v)), len(v))
    F['milky'] = {st: (float(np.median([milky(c) for c in clean if c['st'] == st])), sum(1 for c in clean if c['st'] == st)) for st in ('stars35', 'stars477', 'stars62', 'stars289') if any(c['st'] == st for c in clean)}
    F['stations'] = {st: (sum(1 for c in clean if c['st'] == st), int(np.sum([tenth(c)[0] == 9 for c in clean if c['st'] == st])), int(np.sum([tenth(c)[0] >= 5 for c in clean if c['st'] == st])), before([c for c in clean if c['st'] == st])) for st in STATIONS if any(c['st'] == st for c in clean)}
    return F
