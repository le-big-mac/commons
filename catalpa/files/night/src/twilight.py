# The twilight as a lamp: has a photometer itself changed?
#
# In twilight the sky overhead is far brighter than any lamp-lit or starlit night sky, and its brightness at a given
# depth of the Sun below the horizon is nearly the same from year to year. So the depth of the Sun at the moment a
# photometer's reading passes a fixed level tells how sensitive the photometer is: one that has come to read darker
# reaches the level earlier in the evening and leaves it later in the morning, with the Sun higher both times.
#
# For each monthly file this takes, from the raw count on one fixed scale (20.5 - 2.5 log10 of the frequency, so that a
# change of the header's zero point makes no step), every moment at which the reading passes LEVEL between two readings
# less than 200 seconds apart with the Sun between 3 and 12 degrees down at the photometer's place; the Sun's altitude
# then; and the slope of the reading against the Sun's altitude between those two readings. A month's figure is the
# mean of its middle evening altitude and its middle morning altitude (which cancels an error of the clock or of the
# longitude), kept if it has MINX crossings or more of each kind.
#
# The night, for comparison: for each night of the month that has no Moon (the frozen method's nights: the Sun 18 degrees
# down at both ends, five hours or more, the Moon below the horizon throughout, a reading in nine tenths of its minutes),
# the middle raw-count reading and the spread about an hour-long running middle. Which nights count as clear is decided
# later, station by station, as the frozen method does (spread no more than twice the station's 20th percentile).
#
# reduce(file) returns a small dictionary; it is all that later steps need, so a file need not be kept.
import re, math, datetime as dt, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('dawnlib', '/home/agent1/night/src/dawnlib.py'); D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
sky = D.sky
_NIGHTS = {}
LEVEL = 14.0; MINX = 5
def sun_alt_vec(ts, lat, lon):
    """Sun's altitude at the given times (seconds since 2000-01-01), by sky.py's formulas written for arrays"""
    d = np.asarray(ts) / 86400.0 - 0.5                      # days from J2000.0 (2000-01-01 12:00)
    L = np.radians((280.460 + 0.9856474 * d) % 360); g = np.radians((357.528 + 0.9856003 * d) % 360)
    lam = L + np.radians(1.915) * np.sin(g) + np.radians(0.020) * np.sin(2 * g); eps = np.radians(23.439 - 0.0000004 * d)
    ra = np.arctan2(np.cos(eps) * np.sin(lam), np.cos(lam)); dec = np.arcsin(np.sin(eps) * np.sin(lam))
    gmst = np.radians((280.46061837 + 360.98564736629 * d) % 360); ha = gmst + math.radians(lon) - ra; la = math.radians(lat)
    return np.degrees(np.arcsin(np.sin(la) * np.sin(dec) + np.cos(la) * np.cos(dec) * np.cos(ha)))
T2000 = dt.datetime(2000, 1, 1)
def reduce(path, lat=None, lon=None, loss=None):
    """one monthly file -> header facts and its twilight crossings. lat, lon: the place to reckon the Sun from when the
    header gives none (or to override it). loss: for made-up tests only, a function of the time (seconds since 2000)
    giving magnitudes by which the reading is made darker."""
    txt = open(path, encoding='utf-8', errors='replace').read()
    if '# END OF HEADER' not in txt: return None
    head, body = txt.split('# END OF HEADER', 1)
    m = re.search(r'# Position: ([-\d.]+), ([-\d.]+)', head); hp = (float(m.group(1)), float(m.group(2))) if m else None
    mm = re.search(r'# TESS MAC address: (\S+)', head); zz = re.search(r'# TESS zero point: ([-\d.]+)', head); nn = re.search(r'# Location name: (.*)', head)
    if lat is None:
        if hp is None: return dict(pos=None, mac=mm.group(1) if mm else None, n=0, ev=[], mo=[], sl=[], name=nn.group(1).strip() if nn else '')
        lat, lon = hp
    T, F = [], []
    for line in body.splitlines():
        p = line.split(';')
        if len(p) < 7: continue
        try: f = float(p[4]); t = dt.datetime.strptime(p[0][:19], '%Y-%m-%dT%H:%M:%S')
        except ValueError: continue
        if f > 0: T.append((t - T2000).total_seconds()); F.append(f)
    out = dict(pos=hp, used=(lat, lon), mac=mm.group(1) if mm else None, zp=float(zz.group(1)) if zz else None, name=nn.group(1).strip() if nn else '', n=len(T), ev=[], mo=[], sl=[], nights=[])
    if len(T) < 100: return out
    o = np.argsort(T); T = np.array(T)[o]; M = 20.5 - 2.5 * np.log10(np.array(F)[o])
    if loss is not None: M = M + loss(T)
    # the moonless nights that begin in this file's month
    t_first = T2000 + dt.timedelta(seconds=float(T[0])); year = t_first.year; key = (round(lat, 3), round(lon, 3), year)
    if key not in _NIGHTS: _NIGHTS[key] = D.nights(lat, lon, year)
    for d, dusk, dawn, moon in _NIGHTS[key]:
        if moon >= 0 or dusk.month != t_first.month or dusk.year != year: continue
        a = (dusk - T2000).total_seconds(); b = (dawn - T2000).total_seconds(); i0, i1 = np.searchsorted(T, a), np.searchsorted(T, b)
        if i1 - i0 < 10: continue
        mins = np.floor((T[i0:i1] - a) / 60).astype(int); nmin = int((b - a) // 60); um = np.unique(mins)
        if len(um) < 0.9 * nmin: continue
        mm_ = np.array([np.median(M[i0:i1][mins == k]) for k in um]); r = mm_ - D.runmed(mm_, 61)
        out['nights'].append((d, (b - a) / 3600, float(np.median(mm_)), float(1.4826 * np.median(np.abs(r - np.median(r))))))
    i = np.where((np.diff(T) < 200) & (np.diff(T) > 0) & ((M[:-1] - LEVEL) * (M[1:] - LEVEL) < 0))[0]
    if len(i) == 0: return out
    fr = (LEVEL - M[i]) / (M[i + 1] - M[i]); tc = T[i] + fr * (T[i + 1] - T[i])
    a = sun_alt_vec(tc, lat, lon); a0 = sun_alt_vec(T[i], lat, lon); a1 = sun_alt_vec(T[i + 1], lat, lon)
    for k in range(len(i)):
        if not (-12.0 < a[k] < -3.0) or a1[k] == a0[k]: continue
        s = (M[i[k] + 1] - M[i[k]]) / (a1[k] - a0[k])           # magnitudes per degree; negative: darker as the Sun sinks
        if M[i[k] + 1] > M[i[k]] and a1[k] < a0[k]: out['ev'].append(float(a[k])); out['sl'].append(float(s))
        elif M[i[k] + 1] < M[i[k]] and a1[k] > a0[k]: out['mo'].append(float(a[k])); out['sl'].append(float(s))
    return out
def month_value(r):
    """the month's figure (degrees) and its evening and morning parts, or None"""
    if r is None or len(r['ev']) < MINX or len(r['mo']) < MINX: return None
    e = float(np.median(r['ev'])); m = float(np.median(r['mo'])); return (e + m) / 2, e, m
def drift(vals, slope):
    """vals: {(year, month): degrees}. Fits each calendar month's own level and one rate; returns magnitudes a year
    (positive: reading darker), its plain error, and the number of months. slope: magnitudes per degree (its size)."""
    ks = sorted(vals); months = sorted({m for y, m in ks})
    if len(ks) < 12 or len({y for y, m in ks}) < 3: return None
    A = np.zeros((len(ks), len(months) + 1)); yv = np.zeros(len(ks))
    for j, (y, m) in enumerate(ks): A[j, months.index(m)] = 1; A[j, -1] = y + (m - 0.5) / 12 - 2020; yv[j] = vals[(y, m)]
    co, *_ = np.linalg.lstsq(A, yv, rcond=None); e = yv - A @ co; dof = len(ks) - len(months) - 1
    if dof < 3: return None
    cov = float(e @ e) / dof * np.linalg.pinv(A.T @ A)
    return float(co[-1]) * abs(slope), float(np.sqrt(cov[-1, -1])) * abs(slope), len(ks), float(np.sqrt(e @ e / dof)) * abs(slope)
