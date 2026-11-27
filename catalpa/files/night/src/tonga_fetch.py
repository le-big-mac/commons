# For the seventh sheet (expectations-tonga.md): southern photometers not yet fetched, one for each patch of the map,
# and eight northern ones for comparison; six monthly files a year of 2021 to 2024 of each; each file reduced by
# twilight.py's reduce() and kept (data/tw2/).
#
# The rule, fixed in the sheet.
#  South: photometers of model TESS-W in the share's list of places with a latitude south of 15 degrees south and a
#  folder of 30 MB or more in the root listing saved at 04:31 UTC on 27 November 2026, other than the four already
#  fetched (stars477, stars456, stars221, stars29). The map is cut into patches two degrees on a side; the four patches
#  that hold a photometer already fetched are left out. In each other patch the candidates are tried from the largest
#  folder down, and the first whose own folder lists three or more of the months January, March, May, July, September
#  and November in every one of the years 2021 to 2024 is taken. One photometer for each patch.
#  North: the candidates of the sixth sheet, in that sheet's seeded order, that were not fetched for it and lie north of
#  30 degrees north; the first eight that pass the same test.
# One request every five seconds. The files are data: nothing in them is run.
import os, re, csv, math, time, pickle, datetime as dt, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('tw_fetch', '/home/agent1/night/src/tw_fetch.py'); F6 = importlib.util.module_from_spec(spec); spec.loader.exec_module(F6)
TW = F6.TW; get = F6.get; BASE = F6.BASE; SIX = F6.SIX; PAUSE = 5.0; YEARS = (2021, 2022, 2023, 2024)
OUT = '/home/agent1/night/cache2/twilight_south.pkl'; LOG = '/home/agent1/night/tonga_fetch.log'; KEEP = '/home/agent1/night/data/tw2'
SEEN_SOUTH = {'stars477': (-30.3116867, 139.3358408), 'stars456': (-32.63, 149.49), 'stars221': (-31.80, -69.30), 'stars29': (-38.73, -62.22)}
def log(s): open(LOG, 'a').write(s + '\n')
def cell(lat, lon): return (math.floor(lat / 2), math.floor(lon / 2))
def southern():
    t = open('/home/agent1/night/lit/src/p3_ucm_cloud_share_listing_root.xml', errors='replace').read(); size = {}
    for r in re.findall(r'<d:response>(.*?)</d:response>', t, re.S):
        name = re.search(r'<d:href>([^<]*)</d:href>', r).group(1).rstrip('/').split('/')[-1]; sz = re.search(r'<d:quota-used-bytes>(\d+)', r)
        if re.fullmatch(r'stars\d+', name) and sz: size[name] = int(sz.group(1))
    geo = {r['name']: r for r in csv.DictReader(open('/home/agent1/night/lit/src/p3_stars4all_geolist.csv'), delimiter=';')}
    shut = {cell(*p) for p in SEEN_SOUTH.values()}; cells = {}
    for n, g in geo.items():
        if g['model'] != 'TESS-W' or not g['latitude'] or n in SEEN_SOUTH or size.get(n, 0) < 30e6: continue
        la, lo = float(g['latitude']), float(g['longitude'])
        if la >= -15 or cell(la, lo) in shut: continue
        cells.setdefault(cell(la, lo), []).append((size[n], n))
    return {c: [n for s, n in sorted(v, reverse=True)] for c, v in sorted(cells.items())}, geo
def passes(st):
    code, body = get(BASE + st + '/', 'PROPFIND', {'Depth': '1'}); time.sleep(PAUSE)
    files = sorted(set(re.findall(st + r'_(\d{4})-(\d\d)\.dat', body.decode('utf-8', 'replace'))))
    have = {y: [int(m) for yy, m in files if int(yy) == y and int(m) in SIX] for y in YEARS}
    ok = code in (200, 207) and all(len(have[y]) >= 3 for y in YEARS)
    return ok, have, code, len(files)
def fetch(st, have, geo, R):
    lat0, lon0 = float(geo[st]['latitude']), float(geo[st]['longitude'])
    for y in YEARS:
        for m in have[y]:
            fn = f'{st}_{y}-{m:02d}.dat'; path = os.path.join(KEEP, fn); code, body = get(BASE + st + '/' + fn); time.sleep(PAUSE)
            if code != 200 or len(body) < 1000: log(f'   {fn}: http {code}, {len(body)} bytes; nothing kept'); continue
            open(path, 'wb').write(body)
            try:
                r = TW.reduce(path)
                if r is not None and r.get('pos') is None: r = TW.reduce(path, lat0, lon0); r['placed'] = True
            except Exception as e: r = None; log(f'   {fn}: could not be read ({type(e).__name__}: {e})')
            R[(st, y, m)] = r
            if r is not None: log(f"   {fn}: {len(body)} bytes; {len(r['ev'])} evening and {len(r['mo'])} morning crossings" + ('; no position in the header, the share\'s list used' if r.get('placed') else ''))
            pickle.dump(R, open(OUT + '.part', 'wb'))
if __name__ == '__main__':
    os.makedirs(KEEP, exist_ok=True); cells, geo = southern(); R = {}; south = []; north = []
    log(f'start {dt.datetime.now(dt.timezone.utc):%H:%M:%S}; {len(cells)} southern patches with candidates: ' + '; '.join(f'{c}: {" ".join(v)}' for c, v in cells.items()))
    for c, names in cells.items():
        for st in names:
            ok, have, code, nfiles = passes(st)
            if not ok: log(f'{st} (patch {c}): not taken (listing {code}; {nfiles} files; the six months by year: ' + ', '.join(f'{y}: {len(have[y])}' for y in YEARS) + ')'); continue
            south.append(st); log(f'{st} (patch {c}): taken; {sum(len(have[y]) for y in YEARS)} files to fetch'); fetch(st, have, geo, R); break
    order, geo6 = F6.candidates(); done6 = pickle.load(open('/home/agent1/night/cache2/twilight_new.pkl', 'rb'))['meta']; fetched6 = set(done6['chosen']) | set(done6['companions'])
    for st in order:
        if len(north) >= 8: break
        if st in fetched6 or float(geo6[st]['latitude']) < 30: continue
        ok, have, code, nfiles = passes(st)
        if not ok: log(f'{st} (north): not taken (listing {code}; {nfiles} files; the six months by year: ' + ', '.join(f'{y}: {len(have[y])}' for y in YEARS) + ')'); continue
        north.append(st); log(f'{st} (north): taken; {sum(len(have[y]) for y in YEARS)} files to fetch'); fetch(st, have, geo6, R)
    R['meta'] = dict(south=south, north=north)
    pickle.dump(R, open(OUT, 'wb')); log(f'south: {" ".join(south)}'); log(f'north: {" ".join(north)}'); log(f'tonga fetch done {dt.datetime.now(dt.timezone.utc):%H:%M:%S}; {len(R) - 1} files reduced')
