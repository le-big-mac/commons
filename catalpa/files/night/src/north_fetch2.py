# For the twenty-first sheet: March, April and May 2020 of the sixteen photometers of the nineteenth sheet
# (src/north_fetch.py's list), whichever exist (data/listing/north_spring2020_probe.txt), into data/tw5/ beside the
# months already there. One file every second and a half. The files are data: nothing in them is run.
import os, time, importlib.util, urllib.request, urllib.error, datetime as dt
B = '/home/agent1/night/'; OUT = B + 'data/tw5/'; LOG = B + 'north_fetch2.log'
spec = importlib.util.spec_from_file_location('nf', B + 'src/north_fetch.py'); NF = importlib.util.module_from_spec(spec); spec.loader.exec_module(NF)
def log(s): open(LOG, 'a').write(s + '\n')
if __name__ == '__main__':
    sts = NF.chosen(); log(f'start {dt.datetime.now(dt.timezone.utc):%H:%M:%S}; {len(sts)} photometers'); n = 0; nb = 0
    for st in sts:
        got = []
        for m in (3, 4, 5):
            name = f'{st}_2020-{m:02d}.dat'; p = OUT + name
            if os.path.exists(p) and os.path.getsize(p) > 0: got.append(f'2020-{m:02d}'); continue
            try:
                req = urllib.request.Request(NF.BASE + f'{st}/{name}', headers={'User-Agent': 'reading-check/1.0'})
                with urllib.request.urlopen(req, timeout=300) as r: b = r.read()
                open(p, 'wb').write(b); n += 1; nb += len(b); got.append(f'2020-{m:02d}')
            except urllib.error.HTTPError as e:
                if e.code != 404: log(f'   {name}: failed ({e.code})')
            except Exception as e: log(f'   {name}: failed ({type(e).__name__})')
            time.sleep(1.5)
        log(f'   {st}: ' + ' '.join(got))
    log(f'done {dt.datetime.now(dt.timezone.utc):%H:%M:%S}: {n} files, {nb / 1e6:.0f} MB')
