# The frozen method (dawnlib.py, unchanged and imported) made fit for any year of the share, with what was settled on
# 27 November after the third sheet written in as rules, and with three more figures kept for each night.
#
# Rules added (all decided before any year earlier than 2022, or 2026, was fetched):
#  1. Where the photometer was. Each station has a home: the position in its 2024 headers. A monthly file whose header
#     gives a position more than 0.05 degree from home is not used. A file whose header gives no position is used, at
#     home, only if the photometer's own twilight says it was there (rule 2); otherwise it is not used.
#  2. The twilight test, month by month, for files with no position. Whenever the reading passes 14.0 magnitudes in
#     twilight (between two successive minutes, going darker in the evening or brighter in the morning), the Sun's
#     altitude at home is worked out. At home these crossings come at one altitude, about 7 degrees down, evening and
#     morning alike; a photometer 5 degrees of longitude away would show them 3 or 4 degrees apart. The month is used
#     if it has 10 crossings or more, at least 3 in the evening and 3 in the morning, their middle altitude is within
#     1.5 degrees of the station's 2024 middle, and the evening and morning middles are within 1.5 degrees of each other.
#  3. Not the sky. After the frozen method's own cleaning, a night whose level (by the file's formula) is more than
#     1 magnitude from the station's 2024 level is left out.
#
# Figures added for each cleaned night:
#  zp     the middle value of the file's zero-point column over the night
#  mf     the night's minute readings as 20.5 - 2.5 log10(frequency): the raw count on one fixed scale, so that a change
#         of the header's zero point or of the printed column makes no step
#  lev40  the middle of mf over the minutes at which the point overhead is 40 degrees or more from the Milky Way's
#         plane (None if there are fewer than 60 such minutes); n40 their number
#  levall the middle of mf over the whole night;  levdark  the mean of mf over the night's darkest tenth
#  mac    the photometer's own address, from the header of the month's file: a change of it is a change of instrument
import os, re, glob, math, pickle, datetime as dt, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('dawnlib', '/home/agent1/night/src/dawnlib.py'); D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
sky = D.sky
FROZEN_READ = D.read_full          # the frozen reader itself, kept here because load() below puts a wrapper in its place while it runs
HOME = {'stars1': (40.4246043, -3.560279), 'stars4': (28.6865, -17.7665), 'stars7': (42.81732, -1.64543), 'stars9': (38.409226, -4.894376),
        'stars19': (32.223877, -110.767532), 'stars24': (27.90083333, -15.51472222), 'stars33': (40.4478574, -3.6637624), 'stars35': (45.93, 13.91),
        'stars36': (42.3177194, -72.4757444), 'stars52': (36.8787604, -2.4418338), 'stars62': (42.02459, 0.734797), 'stars76': (39.478898, -0.376524),
        'stars225': (41.474, -1.4821), 'stars289': (38.1657813, -2.3268926), 'stars426': (28.29871203, -16.50948217), 'stars477': (-30.3116867, 139.3358408)}
_ref = None
def ref2024():
    """each station's 2024 level by the formula and its 2024 middle Sun altitude at the twilight crossings"""
    global _ref
    if _ref is None: _ref = pickle.load(open('/home/agent1/night/cache2/ref2024.pkl', 'rb'))
    return _ref
def sun_alt_vec(tsec, t0, lat, lon):
    return np.array([sky.sun_alt(t0 + dt.timedelta(seconds=float(x)), lat, lon) for x in tsec])
def crossings(tsec, M, t0, lat, lon):
    """Sun altitudes at home at the moments the reading passes 14.0 in twilight: (evening list, morning list)"""
    ok = M > 0; ts = tsec[ok]; m = M[ok]; ev, mo = [], []
    if len(ts) < 3: return ev, mo
    step = np.diff(ts); i = np.where((step < 200) & ((m[:-1] - 14.0) * (m[1:] - 14.0) < 0))[0]
    for k in i:
        f = (14.0 - m[k]) / (m[k + 1] - m[k]); tc = ts[k] + f * (ts[k + 1] - ts[k]); a = sky.sun_alt(t0 + dt.timedelta(seconds=float(tc)), lat, lon)
        if not (-12.0 < a < -3.0): continue          # twilight only: a lamp or a cloud at night is not a crossing
        (ev if m[k + 1] > m[k] else mo).append(a)
    return ev, mo
MACS = {}
def read_station(st, year, folder, log):
    """the frozen read_full, on the files that pass rules 1 and 2; returns what read_full returns, with the position set to home, plus the frequency and zero-point columns' own arrays (they are already in it)"""
    lat0, lon0 = HOME[st]; t0 = dt.datetime(year, 1, 1); keep = []
    for fn in sorted(glob.glob(os.path.join(folder, f'{st}_{year}-??.dat'))):
        txt = open(fn, encoding='utf-8', errors='replace').read()
        if '# END OF HEADER' not in txt: log.append(f'{os.path.basename(fn)}: no header end; not used'); continue
        head = txt.split('# END OF HEADER', 1)[0]; m = re.search(r'# Position: ([-\d.]+), ([-\d.]+)', head)
        mm = re.search(r'# TESS MAC address: (\S+)', head); MACS[(st, year, int(os.path.basename(fn)[-6:-4]))] = mm.group(1) if mm else None
        if m:
            la, lo = float(m.group(1)), float(m.group(2))
            if abs(la - lat0) > 0.05 or abs(lo - lon0) > 0.05: log.append(f'{os.path.basename(fn)}: header position {la}, {lo} is not home; not used'); continue
            keep.append(fn); continue
        # no position: the twilight test for this month
        T, M = [], []
        for line in txt.split('# END OF HEADER', 1)[1].splitlines():
            p = line.split(';')
            if len(p) < 7: continue
            try: v = float(p[5]); t = dt.datetime.strptime(p[0][:19], '%Y-%m-%dT%H:%M:%S')
            except ValueError: continue
            T.append((t - t0).total_seconds()); M.append(v)
        if not T: log.append(f'{os.path.basename(fn)}: no position and no readings; not used'); continue
        o = np.argsort(T); ev, mo = crossings(np.array(T)[o], np.array(M)[o], t0, lat0, lon0)
        if len(ev) + len(mo) >= 10 and len(ev) >= 3 and len(mo) >= 3:
            mid = float(np.median(ev + mo)); d = abs(float(np.median(ev)) - float(np.median(mo))); r = ref2024()['cross'].get(st)
            if r is not None and abs(mid - r) <= 1.5 and d <= 1.5: keep.append(fn); log.append(f'{os.path.basename(fn)}: no position; twilight at home ({len(ev)} evening and {len(mo)} morning crossings, middle {mid:+.1f}, apart {d:.1f}; 2024 {r:+.1f}); used'); continue
            log.append(f'{os.path.basename(fn)}: no position; twilight not as at home (middle {mid:+.1f}, evening and morning apart {d:.1f}; 2024 {r if r is None else round(r, 1)}); not used'); continue
        log.append(f'{os.path.basename(fn)}: no position; too few twilight crossings ({len(ev)} evening, {len(mo)} morning); not used')
    if not keep: return None
    # the frozen reader, given only the kept files (by a folder of links, so that its own text is what runs)
    tmp = f'/tmp/dawnlib2_{os.getpid()}_{st}_{year}'; os.makedirs(tmp, exist_ok=True)
    for f in glob.glob(tmp + '/*'): os.remove(f)
    for fn in keep: os.symlink(fn, os.path.join(tmp, os.path.basename(fn)))
    r = FROZEN_READ(st, year, tmp)
    for f in glob.glob(tmp + '/*'): os.remove(f)
    os.rmdir(tmp)
    if r is None: return None
    return r[:6] + (lat0, lon0, r[8])
def gal_b_vec(dusk, hours, lat, lon):
    """distance of the point overhead from the Milky Way's plane, degrees, at each of the given hours after dusk"""
    lst0 = (sky.gmst_deg(sky.jd(dusk)) + lon) % 360; a = np.radians(lst0 + 15.0 * 1.0027379 * np.asarray(hours)); d = math.radians(lat); an, dn = math.radians(192.85948), math.radians(27.12825)
    return np.abs(np.degrees(np.arcsin(math.sin(d) * math.sin(dn) + math.cos(d) * math.cos(dn) * np.cos(a - an))))
def load(year, folder, log=None, screen=True):
    """every cleaned night of the year, as a small dictionary (what years_cache.py saved, and the added figures)"""
    if log is None: log = []
    _rf = D.read_full; cols = {}
    def rf(st, y, fo):
        r = read_station(st, y, fo, log)
        if r is not None: cols[st] = (r[0], r[4], r[5])          # seconds, frequency, zero point
        return r
    D.read_full = rf
    try: N = D.load(year, folder)
    finally: D.read_full = _rf
    t0 = dt.datetime(year, 1, 1); out = []
    for c in N:
        if not c['clean']: continue
        lev = float(np.median(c['m']) - c['off'])
        if screen and abs(lev - ref2024()['lev'][c['st']]) > 1.0: log.append(f"{c['st']} {c['d']}: level {lev:.1f} is not the sky; left out"); continue
        tsec, FQ, ZP = cols[c['st']]; a = (c['dusk'] - t0).total_seconds(); b = (c['dawn'] - t0).total_seconds(); i0, i1 = np.searchsorted(tsec, a), np.searchsorted(tsec, b)
        zp = float(np.median(ZP[i0:i1])) if i1 > i0 else float('nan')
        mf = c['m'] - c['off'] - (zp - 20.5)
        k, mt = D.tenth(c); gb = gal_b_vec(c['dusk'], c['t'], c['lat'], c['lon']); far = gb >= 40.0
        bt = np.minimum((c['t'] / c['L'] * 10).astype(int), 9)
        gb10 = [D.gal_b(c['dusk'] + dt.timedelta(hours=float((j + 0.5) / 10 * c['L'])), c['lat'], c['lon']) for j in range(10)]
        out.append(dict(st=c['st'], cls=D.CLASS[c['st']], name=D.NAME[c['st']], d=c['d'], lat=c['lat'], lon=c['lon'], L=c['L'], dusk=c['dusk'], dawn=c['dawn'],
                        mt=[float(x) for x in mt], tenth=k, near=D.last_near(c), ends=D.has_ends(c), dd=(D.dd(c) if D.has_ends(c) else None), gb=gb10, season=D.season(c), lev=lev,
                        zp=zp, off=float(c['off']), lev40=(float(np.median(mf[far])) if far.sum() >= 60 else None), n40=int(far.sum()), levall=float(np.median(mf)), levdark=float(mf[bt == k].mean()),
                        tenc=float(np.median(c['te'])), y=year, mac=MACS.get((c['st'], c['dusk'].year, c['dusk'].month))))
    return out
if __name__ == '__main__':
    import sys
    year = int(sys.argv[1]); folder = sys.argv[2]; log = []
    out = load(year, folder, log); os.makedirs('/home/agent1/night/cache2', exist_ok=True)
    pickle.dump(out, open(f'/home/agent1/night/cache2/nights{year}.pkl', 'wb')); open(f'/home/agent1/night/cache2/log{year}.txt', 'w').write('\n'.join(log) + '\n')
    print(year, len(out), 'cleaned nights saved;', len(log), 'lines in the log')
