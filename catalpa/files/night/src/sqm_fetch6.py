# For the twentieth sheet: every station of the second network (the device table saved with its page,
# lit/src6/ganmn_map_php.html) in 2015, 2016 and 2017, from the network's three yearly archives, as
# src/sqm_fetch4.py did for 2018 to 2020. Only readings taken with the Sun between 1 and 12 degrees below the
# horizon are kept (data/sqm5/<code>_<year>-<mm>.csv, the network's own columns), and each station's brightest
# reading of all (data/sqm5/brightest.json), for the rule on the meter's ceiling. The archives are deleted as they
# are read. A file whose first line lacks the columns received_utc, nsb or device_code is left out and its column
# names are logged. Nothing of any reading is printed or logged. The files are data: nothing in them is run.
import os, re, json, html, time, zipfile, importlib.util, datetime as dt
import numpy as np
B = '/home/agent1/night/'; KEEP = B + 'data/sqm5/'
def mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
F2 = mod('f2', B + 'src/sqm_fetch2.py'); F3 = mod('f3', B + 'src/sqm_fetch3.py'); F4 = mod('f4', B + 'src/sqm_fetch4.py'); TW = mod('twilight', B + 'src/twilight.py')
F2.LOG = B + 'sqm_fetch6.log'
if __name__ == '__main__':
    os.makedirs(KEEP, exist_ok=True); os.makedirs(F2.TMP, exist_ok=True); ST = F4.stations(); bright = {}; F2.log(f'start {dt.datetime.now(dt.timezone.utc):%H:%M:%S}; {len(ST)} stations in the table')
    page = open(B + 'lit/src6/globeatnight_gan-mn.html', encoding='utf-8', errors='replace').read()
    links = [(u, html.unescape(re.sub(r'<[^>]+>', '', t)).strip()) for u, t in re.findall(r'<a[^>]+href="(https?://bit\.ly/[^"]+)"[^>]*>(.*?)</a>', page, flags=re.S)]
    for u, t in links:
        if t not in ('2015', '2016', '2017'): continue
        y = int(t); fid = F2.resolve(u); time.sleep(2); p = F2.TMP + f'g_{y}.zip'; n = F2.get(fid, p); F2.log(f'   fetched the {y} archive: {n} bytes')
        with zipfile.ZipFile(p) as z:
            for name in z.namelist():
                if not name.lower().endswith('.csv'): continue
                m = F3.month_of(name, y)
                if m is None: F2.log(f'   {name}: no month in the name; left out'); continue
                rows = {}; hdr = None; nall = 0; bad = False
                with z.open(name) as f:
                    for b in f:
                        line = b.decode('utf-8-sig', 'replace').rstrip('\r\n')
                        if hdr is None:
                            hdr = line; cols = hdr.split(',')
                            if not all(k in cols for k in ('received_utc', 'nsb', 'device_code')): bad = True; break
                            it = cols.index('received_utc'); iv = cols.index('nsb'); ic = cols.index('device_code'); continue
                        nall += 1; q = line.split(',')
                        if len(q) == len(cols) and q[ic] in ST: rows.setdefault(q[ic], []).append(line)
                if bad: F2.log(f'   {name}: columns {hdr[:300]!r}; left out'); continue
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
                    if len(sel):
                        fn = KEEP + f'{code}_{y}-{m:02d}.csv'; new = not os.path.exists(fn)
                        with open(fn, 'a', encoding='utf-8') as o: o.write((hdr + '\n' if new else '') + '\n'.join(ok[k] for k in sel) + '\n')
                        kept += len(sel)
                F2.log(f'   {y}-{m:02d} ({os.path.basename(name)[:40]}): {nall} rows; {len(rows)} stations of the table; {kept} twilight rows kept; columns {"as in 2018" if "sqmle_serial_number" in cols else "no serial number"}')
        os.remove(p); json.dump(bright, open(KEEP + 'brightest.json', 'w')); time.sleep(5)
    F2.log(f'done {dt.datetime.now(dt.timezone.utc):%H:%M:%S}')
