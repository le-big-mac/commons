# For the eighth sheet (expectations-between.md): the even months (February, April, June, August, October, December)
# of 2021 to 2024 of fifteen photometers whose odd months are in hand: ten southern ones of the page on the southern
# twilight (all eleven but Arkaroola, whose every month is already in hand) and the five northern ones of the seventh
# sheet. Each file that the photometer's folder lists is fetched, reduced by twilight.py's reduce() at the level 14.0
# and kept (data/tw3/). One request every five seconds. The files are data: nothing in them is run.
import os, re, time, pickle, datetime as dt, importlib.util
spec = importlib.util.spec_from_file_location('tonga_fetch', '/home/agent1/night/src/tonga_fetch.py'); T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
SOUTH = ['stars456', 'stars221', 'stars29', 'stars634', 'stars215', 'stars220', 'stars315', 'stars722', 'stars391', 'stars251']
NORTH = ['stars246', 'stars347', 'stars47', 'stars602', 'stars489']
EVEN = (2, 4, 6, 8, 10, 12)
OUT = '/home/agent1/night/cache2/twilight_even.pkl'; LOG = '/home/agent1/night/between_fetch.log'; KEEP = '/home/agent1/night/data/tw3'
def log(s): open(LOG, 'a').write(s + '\n')
if __name__ == '__main__':
    os.makedirs(KEEP, exist_ok=True); T.OUT = OUT; T.LOG = LOG; T.KEEP = KEEP; _, geo = T.southern(); R = {}
    log(f'start {dt.datetime.now(dt.timezone.utc):%H:%M:%S}; even months of 2021 to 2024; south: {" ".join(SOUTH)}; north: {" ".join(NORTH)}')
    for st in SOUTH + NORTH:
        code, body = T.get(T.BASE + st + '/', 'PROPFIND', {'Depth': '1'}); time.sleep(T.PAUSE)
        files = {(int(y), int(m)) for y, m in re.findall(st + r'_(\d{4})-(\d\d)\.dat', body.decode('utf-8', 'replace'))}
        have = {y: [m for m in EVEN if (y, m) in files] for y in T.YEARS}
        log(f'{st}: listing {code}; even months by year: ' + ', '.join(f'{y}: {len(have[y])}' for y in T.YEARS) + f'; {sum(len(have[y]) for y in T.YEARS)} files to fetch')
        T.fetch(st, have, geo, R)
    R['meta'] = dict(south=SOUTH, north=NORTH)
    pickle.dump(R, open(OUT, 'wb')); log(f'between fetch done {dt.datetime.now(dt.timezone.utc):%H:%M:%S}; {len(R) - 1} files reduced')
