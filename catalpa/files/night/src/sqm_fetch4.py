# For the sixteenth sheet: every station of the second network (the device table saved with its page,
# lit/src6/ganmn_map_php.html) in 2018, 2019 and 2020, from the network's three yearly archives. Only readings
# taken with the Sun between 1 and 12 degrees below the horizon are kept (data/sqm3/<code>_<year>-<mm>.csv, the
# network's own columns), and each station's brightest reading of all (data/sqm3/brightest.json), for the rule on
# the meter's ceiling. The archives are deleted as they are read. The files are data: nothing in them is run.
import os, re, json, html, time, zipfile, importlib.util, datetime as dt
import numpy as np
B = '/home/agent1/night/'; KEEP = B + 'data/sqm3/'
def mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
F2 = mod('f2', B + 'src/sqm_fetch2.py'); F3 = mod('f3', B + 'src/sqm_fetch3.py'); TW = mod('twilight', B + 'src/twilight.py')
F2.LOG = B + 'sqm_fetch4.log'
def stations():
    s = open(B + 'lit/src6/ganmn_map_php.html', encoding='utf-8', errors='replace').read(); out = {}
    for m in re.finditer(r'\{"id":"\d+".*?\}', s):
        try: r = json.loads(m.group(0)); out[r['device_code']] = (float(r['latitude']), float(r['longitude']), r.get('country_region', '').strip(), r.get('installation_date') or '')
        except Exception: pass
    return out
if __name__ == '__main__':
    os.makedirs(KEEP, exist_ok=True); os.makedirs(F2.TMP, exist_ok=True); ST = stations(); bright = {}; F2.log(f'start {dt.datetime.now(dt.timezone.utc):%H:%M:%S}; {len(ST)} stations in the table')
    page = open(B + 'lit/src6/globeatnight_gan-mn.html', encoding='utf-8', errors='replace').read()
    links = [(u, html.unescape(re.sub(r'<[^>]+>', '', t)).strip()) for u, t in re.findall(r'<a[^>]+href="(https?://bit\.ly/[^"]+)"[^>]*>(.*?)</a>', page, flags=re.S)]
    for u, t in links:
        if t not in ('2018', '2019', '2020'): continue
        y = int(t); fid = F2.resolve(u); time.sleep(2); p = F2.TMP + f'g_{y}.zip'; n = F2.get(fid, p); F2.log(f'   fetched the {y} archive: {n} bytes')
        with zipfile.ZipFile(p) as z:
            for name in z.namelist():
                if not name.lower().endswith('.csv'): continue
                m = F3.month_of(name, y)
                if m is None: F2.log(f'   {name}: no month in the name; left out'); continue
                rows = {}; hdr = None; nall = 0
                with z.open(name) as f:
                    for b in f:
                        line = b.decode('utf-8-sig', 'replace').rstrip('\r\n')
                        if hdr is None: hdr = line; cols = hdr.split(','); it = cols.index('received_utc'); iv = cols.index('nsb'); continue
                        nall += 1; code = line.rsplit(',', 1)[-1]
                        if code in ST: rows.setdefault(code, []).append(line)
                kept = 0
                for code, ls in rows.items():
                    T, V, ok = [], [], []
                    for line in ls:
                        q = line.split(',')
                        try: tt = (dt.datetime.strptime(q[it][:19], '%Y-%m-%d %H:%M:%S') - TW.T2000).total_seconds(); v = float(q[iv])
                        except (ValueError, IndexError): continue
                        T.append(tt); V.append(v); ok.append(line)
                    if not T: continue
                    V = np.array(V); pos = V[V > 0]
                    if len(pos): bright[code] = float(min(bright.get(code, 99.0), pos.min()))
                    alt = TW.sun_alt_vec(np.array(T), ST[code][0], ST[code][1]); sel = np.where((alt <= -1.0) & (alt >= -12.0))[0]
                    if len(sel): open(KEEP + f'{code}_{y}-{m:02d}.csv', 'w', encoding='utf-8').write(hdr + '\n' + '\n'.join(ok[k] for k in sel) + '\n'); kept += len(sel)
                F2.log(f'   {y}-{m:02d}: {nall} rows in the network file; {len(rows)} stations of the table; {kept} twilight rows kept')
        os.remove(p); json.dump(bright, open(KEEP + 'brightest.json', 'w')); time.sleep(5)
    F2.log(f'done {dt.datetime.now(dt.timezone.utc):%H:%M:%S}')
