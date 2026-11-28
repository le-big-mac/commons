# For the thirteenth sheet (expectations-sqm-months.md): every month of 2021 to 2025 of the four southern SQM stations,
# from the network's monthly files (links on its page, saved by the search as lit/src6/globeatnight_gan-mn.html; each
# short link is resolved to the file it points to). Rows of the four stations are kept in data/sqm2/; the network
# files are deleted as they are read. A pause of five seconds between files. The files are data: nothing in them is run.
import os, re, html, time, zipfile, urllib.request, urllib.error, datetime as dt
B = '/home/agent1/night/'; KEEP = B + 'data/sqm2/'; TMP = '/tmp/sqm_dl/'; LOG = B + 'sqm_fetch2.log'
CODES = ('AHO', 'Oam', 'PAOF', 'Nrnr'); MON = {m: i + 1 for i, m in enumerate(('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))}
FULL = {m: i + 1 for i, m in enumerate(('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'))}
UA = {'User-Agent': 'reading-check/1.0'}
def log(s): open(LOG, 'a').write(s + '\n')
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
def resolve(short):
    op = urllib.request.build_opener(NoRedirect); url = short
    for _ in range(4):
        try: op.open(urllib.request.Request(url, headers=UA), timeout=60); return None
        except urllib.error.HTTPError as e:
            loc = e.headers.get('Location')
            if not loc: return None
            m = re.search(r'/d/([A-Za-z0-9_-]{20,})|[?&]id=([A-Za-z0-9_-]{20,})', loc)
            if m: return m.group(1) or m.group(2)
            url = loc
    return None
def get(fid, path):
    req = urllib.request.Request(f'https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t', headers=UA); n = 0
    with urllib.request.urlopen(req, timeout=900) as r, open(path, 'wb') as f:
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
    os.makedirs(KEEP, exist_ok=True); os.makedirs(TMP, exist_ok=True); log(f'start {dt.datetime.now(dt.timezone.utc):%H:%M:%S}')
    page = open(B + 'lit/src6/globeatnight_gan-mn.html', encoding='utf-8', errors='replace').read()
    links = [(u, html.unescape(re.sub(r'<[^>]+>', '', t)).strip()) for u, t in re.findall(r'<a[^>]+href="(https?://bit\.ly/[^"]+)"[^>]*>(.*?)</a>', page, flags=re.S)]
    for u, t in links:
        mm = re.fullmatch(r'([A-Z][a-z]{2}), (20\d\d)', t)
        if mm and int(mm.group(2)) in (2022, 2023, 2024, 2025):
            y, m = int(mm.group(2)), MON[mm.group(1)]; fid = resolve(u); time.sleep(2)
            if not fid: log(f'   {y}-{m:02d}: the link did not resolve'); continue
            p = TMP + f'g_{y}-{m:02d}.csv'
            try: n = get(fid, p)
            except Exception as e: log(f'   {y}-{m:02d}: fetch failed ({type(e).__name__})'); continue
            with open(p, encoding='utf-8-sig', errors='replace') as f: keep_rows(f, y, m)
            os.remove(p); time.sleep(5)
        elif t == '2021':
            fid = resolve(u); p = TMP + 'g_2021.zip'; n = get(fid, p); log(f'   fetched the 2021 archive: {n} bytes')
            with zipfile.ZipFile(p) as z:
                for name in z.namelist():
                    for mn, m in FULL.items():
                        if name.endswith(f'GaN-MN_{mn}_2021.csv'):
                            with z.open(name) as f: keep_rows((b.decode('utf-8-sig', 'replace') for b in f), 2021, m)
            os.remove(p); time.sleep(5)
    log(f'done {dt.datetime.now(dt.timezone.utc):%H:%M:%S}')
