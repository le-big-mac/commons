# For the second amendment to the seventh sheet (amendment-tonga-2.md): in each southern patch where no photometer
# passed the first rule (all four years 2021 to 2024), the first candidate, largest folder first, whose folder lists
# three or more of May, July, September and November 2022 and, for two or more of those months, the same month of 2021
# or of 2024. Its six months a year of 2021 to 2024, as far as it has them, are fetched, reduced and kept (data/tw2/).
# One request every five seconds. The files are data: nothing in them is run.
import os, re, time, pickle, datetime as dt, importlib.util
spec = importlib.util.spec_from_file_location('tonga_fetch', '/home/agent1/night/src/tonga_fetch.py'); T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
OUT = '/home/agent1/night/cache2/twilight_south2.pkl'; LOG = '/home/agent1/night/tonga_fetch2.log'
def log(s): open(LOG, 'a').write(s + '\n')
def passes2(st):
    code, body = T.get(T.BASE + st + '/', 'PROPFIND', {'Depth': '1'}); time.sleep(T.PAUSE)
    files = {(int(y), int(m)) for y, m in re.findall(st + r'_(\d{4})-(\d\d)\.dat', body.decode('utf-8', 'replace'))}
    mid = [m for m in (5, 7, 9, 11) if (2022, m) in files]; based = [m for m in mid if (2021, m) in files or (2024, m) in files]
    have = {y: [m for m in T.SIX if (y, m) in files] for y in T.YEARS}
    return code in (200, 207) and len(mid) >= 3 and len(based) >= 2, have, code, len(files)
if __name__ == '__main__':
    first = pickle.load(open('/home/agent1/night/cache2/twilight_south.pkl', 'rb'))['meta']['south']
    cells, geo = T.southern(); R = {}; south = []; T.OUT = OUT; T.LOG = LOG
    taken_cells = {c for c, names in cells.items() if any(n in first for n in names)}
    log(f'start {dt.datetime.now(dt.timezone.utc):%H:%M:%S}; patches already served by the first rule: {sorted(taken_cells)}')
    for c, names in cells.items():
        if c in taken_cells: continue
        for st in names:
            ok, have, code, nfiles = passes2(st)
            if not ok: log(f'{st} (patch {c}): not taken (listing {code}; {nfiles} files; the six months by year: ' + ', '.join(f'{y}: {len(have[y])}' for y in T.YEARS) + ')'); continue
            south.append(st); log(f'{st} (patch {c}): taken; {sum(len(have[y]) for y in T.YEARS)} files to fetch'); T.fetch(st, have, geo, R); break
    R['meta'] = dict(south=south, north=[])
    pickle.dump(R, open(OUT, 'wb')); log(f'south, added: {" ".join(south)}'); log(f'tonga fetch 2 done {dt.datetime.now(dt.timezone.utc):%H:%M:%S}; {len(R) - 1} files reduced')
