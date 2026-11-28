# For the seventeenth sheet: the Korean stations of the second network at night, 2018 and 2019. The network's two
# yearly archives again (as src/sqm_fetch4.py, whose functions are used); only readings taken with the Sun 18
# degrees or more below the horizon are kept (data/sqm4/<code>_<year>-<mm>.csv). The archives are deleted as they
# are read. The files are data: nothing in them is run.
import os, re, html, time, zipfile, importlib.util, datetime as dt
import numpy as np
B = '/home/agent1/night/'; KEEP = B + 'data/sqm4/'
spec = importlib.util.spec_from_file_location('f4', B + 'src/sqm_fetch4.py'); F4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(F4)
F2, F3, TW = F4.F2, F4.F3, F4.TW; F2.LOG = B + 'sqm_fetch5.log'
if __name__ == '__main__':
    os.makedirs(KEEP, exist_ok=True); os.makedirs(F2.TMP, exist_ok=True); ST = {c: v for c, v in F4.stations().items() if v[2] == 'Korea'}; F2.log(f'start {dt.datetime.now(dt.timezone.utc):%H:%M:%S}; {len(ST)} Korean stations in the table')
    page = open(B + 'lit/src6/globeatnight_gan-mn.html', encoding='utf-8', errors='replace').read()
    links = [(u, html.unescape(re.sub(r'<[^>]+>', '', t)).strip()) for u, t in re.findall(r'<a[^>]+href="(https?://bit\.ly/[^"]+)"[^>]*>(.*?)</a>', page, flags=re.S)]
    for u, t in links:
        if t not in ('2018', '2019'): continue
        y = int(t); fid = F2.resolve(u); time.sleep(2); p = F2.TMP + f'h_{y}.zip'; n = F2.get(fid, p); F2.log(f'   fetched the {y} archive: {n} bytes')
        with zipfile.ZipFile(p) as z:
            for name in z.namelist():
                if not name.lower().endswith('.csv'): continue
                m = F3.month_of(name, y)
                if m is None: continue
                rows = {}; hdr = None
                with z.open(name) as f:
                    for b in f:
                        line = b.decode('utf-8-sig', 'replace').rstrip('\r\n')
                        if hdr is None: hdr = line; cols = hdr.split(','); it = cols.index('received_utc'); continue
                        code = line.rsplit(',', 1)[-1]
                        if code in ST: rows.setdefault(code, []).append(line)
                kept = 0
                for code, ls in rows.items():
                    T, ok = [], []
                    for line in ls:
                        try: T.append((dt.datetime.strptime(line.split(',')[it][:19], '%Y-%m-%d %H:%M:%S') - TW.T2000).total_seconds()); ok.append(line)
                        except (ValueError, IndexError): continue
                    if not T: continue
                    sel = np.where(TW.sun_alt_vec(np.array(T), ST[code][0], ST[code][1]) <= -18.0)[0]
                    if len(sel): open(KEEP + f'{code}_{y}-{m:02d}.csv', 'w', encoding='utf-8').write(hdr + '\n' + '\n'.join(ok[k] for k in sel) + '\n'); kept += len(sel)
                F2.log(f'   {y}-{m:02d}: {len(rows)} Korean stations; {kept} night rows kept')
        os.remove(p); time.sleep(5)
    F2.log(f'done {dt.datetime.now(dt.timezone.utc):%H:%M:%S}')
