# For the fifteenth sheet: the second make's four southern stations in 2019 and 2020, from the network's two yearly
# archives (links on its page, as in src/sqm_fetch2.py, whose functions are used). Rows of the four stations are kept
# in data/sqm2/; the archives are deleted as they are read. The files are data: nothing in them is run.
import os, re, html, time, zipfile, importlib.util, datetime as dt
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('f2', B + 'src/sqm_fetch2.py'); F2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(F2)
F2.LOG = B + 'sqm_fetch3.log'
MONTHS = {**{k.lower(): v for k, v in F2.FULL.items()}, **{k.lower(): v for k, v in F2.MON.items()}}
def month_of(name, year):
    s = os.path.basename(name).lower()
    for k in sorted(MONTHS, key=len, reverse=True):
        if re.search(r'(?<![a-z])' + k + r'(?![a-z])', s): return MONTHS[k]
    m = re.search(rf'{year}[-_ ]?(\d{{2}})(?!\d)', s) or re.search(rf'(?<!\d)(\d{{2}})[-_ ]?{year}', s)
    return int(m.group(1)) if m and 1 <= int(m.group(1)) <= 12 else None
if __name__ == '__main__':
    os.makedirs(F2.KEEP, exist_ok=True); os.makedirs(F2.TMP, exist_ok=True); F2.log(f'start {dt.datetime.now(dt.timezone.utc):%H:%M:%S}')
    page = open(B + 'lit/src6/globeatnight_gan-mn.html', encoding='utf-8', errors='replace').read()
    links = [(u, html.unescape(re.sub(r'<[^>]+>', '', t)).strip()) for u, t in re.findall(r'<a[^>]+href="(https?://bit\.ly/[^"]+)"[^>]*>(.*?)</a>', page, flags=re.S)]
    for u, t in links:
        if t not in ('2019', '2020'): continue
        y = int(t); fid = F2.resolve(u); time.sleep(2); p = F2.TMP + f'g_{y}.zip'; n = F2.get(fid, p); F2.log(f'   fetched the {y} archive: {n} bytes')
        with zipfile.ZipFile(p) as z:
            for name in z.namelist():
                if not name.lower().endswith('.csv'): continue
                m = month_of(name, y)
                if m is None: F2.log(f'   {name}: no month in the name; left out'); continue
                with z.open(name) as f: F2.keep_rows((b.decode('utf-8-sig', 'replace') for b in f), y, m)
        os.remove(p); time.sleep(5)
    F2.log(f'done {dt.datetime.now(dt.timezone.utc):%H:%M:%S}')
