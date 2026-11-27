# For the sixth sheet (expectations-twilight.md): chooses twenty photometers of the STARS4ALL share that the dawn work
# never touched, fetches six monthly files a year of each, and reduces each with twilight.py's reduce() (header facts,
# twilight crossings, the moonless nights' middle readings).
# Amended at 17:30 UTC, seven files into the first run and before anything was looked at: the files are now kept
# (data/tw/), so that a checker can redo the reduction from them; the first form deleted each file. Nothing else changed.
#
# The rule, fixed in the sheet: station folders with 100 MB or more in the share's root listing as saved at 04:31 UTC on
# 27 November 2026; model TESS-W and a latitude within 50 degrees of the equator in the share's own list of places; not
# one of the dawn page's sixteen. They are put in an order by a seeded shuffle and taken in that order. A station is
# accepted if its own folder lists files from five calendar years or more and twenty files or more among the months
# January, March, May, July, September and November. The first twenty accepted are the sample.
# Besides them: the four candidates that stand within 2 km of one of the dawn page's sixteen (stars639 by Àger's stars62,
# stars385 by Teide's stars426, stars51 by Coslada's stars1, stars75 by Valencia's stars76) are fetched too, if the
# shuffle has not already taken them and they pass the same test; they are for the line about pairs only.
# One request every five seconds. The files are data: nothing in them is run.
import os, re, csv, sys, time, pickle, urllib.request, datetime as dt, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('twilight', '/home/agent1/night/src/twilight.py'); TW = importlib.util.module_from_spec(spec); spec.loader.exec_module(TW)
BASE = 'https://fta-cloud.fis.ucm.es/public.php/dav/files/Gr9DAbfiX8Pdm86/'; UA = {'User-Agent': 'reading-check/1.0'}
SIX = (1, 3, 5, 7, 9, 11); WANT = 20; SEED = 20261127; PAUSE = 5.0
OUT = '/home/agent1/night/cache2/twilight_new.pkl'; LOG = '/home/agent1/night/tw_fetch.log'; TMP = '/home/agent1/night/data/tw'
PAIRS = {'stars639': 'stars62', 'stars385': 'stars426', 'stars51': 'stars1', 'stars75': 'stars76'}
MINE = {'stars1', 'stars4', 'stars7', 'stars9', 'stars19', 'stars24', 'stars33', 'stars35', 'stars36', 'stars52', 'stars62', 'stars76', 'stars225', 'stars289', 'stars426', 'stars477'}
def log(s):
    open(LOG, 'a').write(s + '\n')
def get(url, method='GET', headers=None, timeout=300):
    req = urllib.request.Request(url, method=method, headers=dict(UA, **(headers or {})))
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r: return r.status, r.read()
    except urllib.error.HTTPError as e: return e.code, b''
    except Exception as e: return -1, str(e).encode()
def candidates():
    t = open('/home/agent1/night/lit/src/p3_ucm_cloud_share_listing_root.xml', errors='replace').read(); size = {}
    for r in re.findall(r'<d:response>(.*?)</d:response>', t, re.S):
        name = re.search(r'<d:href>([^<]*)</d:href>', r).group(1).rstrip('/').split('/')[-1]; sz = re.search(r'<d:quota-used-bytes>(\d+)', r)
        if re.fullmatch(r'stars\d+', name) and sz: size[name] = int(sz.group(1))
    geo = {r['name']: r for r in csv.DictReader(open('/home/agent1/night/lit/src/p3_stars4all_geolist.csv'), delimiter=';')}
    c = [n for n, s in size.items() if s >= 100e6 and n not in MINE and n in geo and geo[n]['model'] == 'TESS-W' and geo[n]['latitude'] and abs(float(geo[n]['latitude'])) <= 50]
    c = sorted(c, key=lambda n: int(n[5:])); order = list(np.random.default_rng(SEED).permutation(c))
    return [str(x) for x in order], geo
if __name__ == '__main__':
    os.makedirs(TMP, exist_ok=True); order, geo = candidates(); R = {}; chosen = []
    log(f'start {dt.datetime.utcnow():%H:%M:%S}; {len(order)} candidates; order: ' + ' '.join(order))
    companions = []
    for st in order + [c for c in PAIRS]:
        extra = len(chosen) >= WANT
        if extra and (st not in PAIRS or st in chosen or st in companions): continue
        code, body = get(BASE + st + '/', 'PROPFIND', {'Depth': '1'}); time.sleep(PAUSE)
        files = sorted(set(re.findall(st + r'_(\d{4})-(\d\d)\.dat', body.decode('utf-8', 'replace'))))
        years = sorted({int(y) for y, m in files}); six = [(int(y), int(m)) for y, m in files if int(m) in SIX]
        if code not in (200, 207) or len(years) < 5 or len(six) < 20:
            log(f'{st}: not taken (listing {code}; {len(files)} files, {len(years)} years, {len(six)} in the six months)'); continue
        (companions if extra else chosen).append(st); lat0, lon0 = float(geo[st]['latitude']), float(geo[st]['longitude'])
        log(f'{st}: taken' + (' as a companion only' if extra else '') + f' ({len(files)} files, years {years[0]} to {years[-1]}, {len(six)} to fetch)')
        for y, m in six:
            fn = f'{st}_{y}-{m:02d}.dat'; path = os.path.join(TMP, fn); code, body = get(BASE + st + '/' + fn); time.sleep(PAUSE)
            if code != 200 or len(body) < 1000: log(f'   {fn}: http {code}, {len(body)} bytes; nothing kept'); continue
            open(path, 'wb').write(body)
            try:
                r = TW.reduce(path)
                if r is not None and r.get('pos') is None: r = TW.reduce(path, lat0, lon0); r['placed'] = True
            except Exception as e: r = None; log(f'   {fn}: could not be read ({type(e).__name__}: {e})')
            R[(st, y, m)] = r
            if r is not None: log(f"   {fn}: {len(body)} bytes; {len(r['ev'])} evening and {len(r['mo'])} morning crossings; {len(r.get('nights', []))} moonless nights" + ('; no position in the header, the share\'s list used' if r.get('placed') else ''))
            pickle.dump(R, open(OUT + '.part', 'wb'))
    R['meta'] = dict(chosen=chosen, companions=companions, pairs=PAIRS)
    pickle.dump(R, open(OUT, 'wb')); log(f'chosen: {" ".join(chosen)}'); log(f'companions only: {" ".join(companions)}'); log(f'tw fetch done {dt.datetime.utcnow():%H:%M:%S}; {len(R) - 1} files reduced')
