# For the fifteenth sheet: the southern photometers' monthly files of 2019, 2020, 2025 and 2026 that the STARS4ALL
# share holds (the list made by src/years_probe.sh with HEAD requests: data/listing/south_years.txt), into data/tw4/.
# One file every two seconds. The files are data: nothing in them is run.
import os, time, urllib.request, urllib.error, datetime as dt
B = '/home/agent1/night/'; OUT = B + 'data/tw4/'; LOG = B + 'years_fetch.log'
BASE = 'https://fta-cloud.fis.ucm.es/public.php/dav/files/Gr9DAbfiX8Pdm86/'
def log(s): open(LOG, 'a').write(s + '\n')
if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True); log(f'start {dt.datetime.now(dt.timezone.utc):%H:%M:%S}'); n = 0; nb = 0
    for line in open(B + 'data/listing/south_years.txt'):
        if ':' not in line: continue
        head, months = line.split(':'); st, y = head.split()
        for m in months.split():
            name = f'{st}_{y}-{m}.dat'; p = OUT + name
            if os.path.exists(p) and os.path.getsize(p) > 0: continue
            try:
                req = urllib.request.Request(BASE + f'{st}/{name}', headers={'User-Agent': 'reading-check/1.0'})
                with urllib.request.urlopen(req, timeout=300) as r: b = r.read()
                open(p, 'wb').write(b); n += 1; nb += len(b)
            except Exception as e: log(f'   {name}: failed ({type(e).__name__})')
            time.sleep(2)
        log(f'   {st} {y}: {len(months.split())} months listed')
    log(f'done {dt.datetime.now(dt.timezone.utc):%H:%M:%S}: {n} files, {nb / 1e6:.0f} MB')
