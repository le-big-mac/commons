# For the nineteenth sheet: northern photometers of the first make that had never been fetched here. Those of
# data/listing/north_new_probe.txt (made by src/north_probe.sh with HEAD requests) that have October of both 2018
# and 2019 (sixteen): the months March to May and September to November of 2018 and 2019, and September to
# November of 2020, whichever exist, into data/tw5/. One file every second and a half.
# The files are data: nothing in them is run.
import os, time, urllib.request, urllib.error, datetime as dt
B = '/home/agent1/night/'; OUT = B + 'data/tw5/'; LOG = B + 'north_fetch.log'
BASE = 'https://fta-cloud.fis.ucm.es/public.php/dav/files/Gr9DAbfiX8Pdm86/'
MONTHS = [(y, m) for y in (2018, 2019) for m in (3, 4, 5, 9, 10, 11)] + [(2020, m) for m in (9, 10, 11)]
def chosen():
    out = []
    for line in open(B + 'data/listing/north_new_probe.txt'):
        if ':' not in line: continue
        head, months = line.split(':'); st, lat, lon = head.split()
        if '2018-10' in months.split() and '2019-10' in months.split(): out.append((int(st[5:]), st))
    return [st for n, st in sorted(out)]
def log(s): open(LOG, 'a').write(s + '\n')
if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True); sts = chosen(); log(f'start {dt.datetime.now(dt.timezone.utc):%H:%M:%S}; {len(sts)} photometers: ' + ' '.join(sts)); n = 0; nb = 0
    for st in sts:
        got = []
        for y, m in MONTHS:
            name = f'{st}_{y}-{m:02d}.dat'; p = OUT + name
            if os.path.exists(p) and os.path.getsize(p) > 0: got.append(f'{y}-{m:02d}'); continue
            try:
                req = urllib.request.Request(BASE + f'{st}/{name}', headers={'User-Agent': 'reading-check/1.0'})
                with urllib.request.urlopen(req, timeout=300) as r: b = r.read()
                open(p, 'wb').write(b); n += 1; nb += len(b); got.append(f'{y}-{m:02d}')
            except urllib.error.HTTPError as e:
                if e.code != 404: log(f'   {name}: failed ({e.code})')
            except Exception as e: log(f'   {name}: failed ({type(e).__name__})')
            time.sleep(1.5)
        log(f'   {st}: ' + ' '.join(got))
    log(f'done {dt.datetime.now(dt.timezone.utc):%H:%M:%S}: {n} files, {nb / 1e6:.0f} MB')
