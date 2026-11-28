# For the eleventh sheet (expectations-sqm.md): the four southern stations of the SQM make that the search found in the
# Globe at Night Sky Brightness Monitoring Network (lit/scout-sqm.md): Buenos Aires (AHO), Oamaru (Oam), Ouro Fino (PAOF),
# NamibRand (Nrnr). The network publishes one file a month for all its stations (170 to 280 MB); this takes June, July
# and August of 2021, 2022 and 2024, keeps the rows of the four stations (data/sqm/<code>_<year>-<month>.csv) and
# deletes the rest. June 2022 is already on disk from the search. The files are data: nothing in them is run.
import os, sys, time, zipfile, urllib.request, datetime as dt
B = '/home/agent1/night/'; KEEP = B + 'data/sqm/'; TMP = '/tmp/sqm_dl/'; LOG = B + 'sqm_fetch.log'
CODES = ('AHO', 'Oam', 'PAOF', 'Nrnr'); MONTH = {'June': 6, 'July': 7, 'August': 8}
IDS = {(2022, 7): '1bL1LW_FCnUqHWLGtN9savbQRHwLNX0z9', (2022, 8): '1t5d_BE2gnrh_usEXnx9n1nrR7Jn1uZHc',
       (2024, 6): '1y7UsA9TX3xJQ5hqIPjRiSSZBnwucQ-wo', (2024, 7): '1LIvDTLYou6t58zaVC-MCRvA-wMEaC0Qn', (2024, 8): '1kmigc71PlrGfXshc4nHC5S5LzHlgDfN5'}
ZIP2021 = '1qAOBOc81KCCV3sibYhzVMD378Nh1F5ag'
URL = 'https://drive.usercontent.google.com/download?id={}&export=download&confirm=t'
def log(s): open(LOG, 'a').write(s + '\n')
def get(fid, path):
    req = urllib.request.Request(URL.format(fid), headers={'User-Agent': 'reading-check/1.0'})
    with urllib.request.urlopen(req, timeout=600) as r, open(path, 'wb') as f:
        n = 0
        while True:
            b = r.read(1 << 20)
            if not b: break
            f.write(b); n += len(b)
    return n
def keep_rows(lines, y, m):
    out = {c: [] for c in CODES}; n = 0; hdr = None
    for line in lines:
        if hdr is None: hdr = line.strip().lstrip('﻿'); continue
        n += 1; code = line.rstrip('\r\n').rsplit(',', 1)[-1]
        if code in out: out[code].append(line.rstrip('\r\n'))
    for c, rows in out.items():
        if rows: open(KEEP + f'{c}_{y}-{m:02d}.csv', 'w', encoding='utf-8').write(hdr + '\n' + '\n'.join(rows) + '\n')
    log(f'   {y}-{m:02d}: {n} rows in the network file; kept ' + ', '.join(f'{c} {len(out[c])}' for c in CODES))
if __name__ == '__main__':
    os.makedirs(KEEP, exist_ok=True); os.makedirs(TMP, exist_ok=True)
    log(f'start {dt.datetime.now(dt.timezone.utc):%H:%M:%S}')
    with open(B + 'lit/src6/ganmn_2022-06.csv', encoding='utf-8-sig', errors='replace') as f: keep_rows(f, 2022, 6)
    for (y, m), fid in IDS.items():
        p = TMP + f'ganmn_{y}-{m:02d}.csv'; n = get(fid, p); log(f'   fetched {y}-{m:02d}: {n} bytes'); time.sleep(5)
        with open(p, encoding='utf-8-sig', errors='replace') as f: keep_rows(f, y, m)
        os.remove(p)
    p = TMP + 'ganmn_2021.zip'; n = get(ZIP2021, p); log(f'   fetched the 2021 archive: {n} bytes')
    with zipfile.ZipFile(p) as z:
        for name in z.namelist():
            for mn, m in MONTH.items():
                if name.endswith(f'GaN-MN_{mn}_2021.csv'):
                    with z.open(name) as f: keep_rows((b.decode('utf-8-sig', 'replace') for b in f), 2021, m)
    os.remove(p); log(f'done {dt.datetime.now(dt.timezone.utc):%H:%M:%S}')
