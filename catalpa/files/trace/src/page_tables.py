# Writes the four tables of the page as HTML fragments (page/t_*.html) from the same modules that print the outputs.
# Run: ~/ipd/.venv/bin/python -I src/page_tables.py
import sys, io, contextlib, importlib.util, json, datetime as dt
import numpy as np
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
P = load('pairs'); T = P.T; W = load('wave')
O = '/home/agent1/trace/page/'
def num(x, signed=True):
    if x is None: return '<td class="n">–</td>'
    s = f"{x:+.1f}" if signed else f"{x:.1f}"
    return f'<td class="n">{s.replace("-", "−")}</td>'
# (a) late summer by gauge
rows = ['<tr><th>gauge</th><th class="n">latitude</th><th class="n">1997</th><th class="n">2015</th><th class="n">2026</th><th class="n">2026 over 1997</th><th class="n">over 2015</th></tr>']
place = {"Callao": "Callao, Peru", "La Libertad": "La Libertad, Ecuador", "Santa Cruz": "Santa Cruz, Galápagos", "Baltra": "Baltra, Galápagos", "San Diego": "San Diego", "La Jolla": "La Jolla",
         "San Francisco": "San Francisco", "Crescent City": "Crescent City, California", "South Beach": "South Beach, Oregon", "Neah Bay": "Neah Bay, Washington", "Tofino": "Tofino, British Columbia",
         "Prince Rupert": "Prince Rupert, British Columbia", "Ketchikan": "Ketchikan, Alaska"}
for sid, name, lat in T.G:
    if name not in T.fit: continue
    v = {y: T.late(name, y) for y in (1997, 2015, 2026)}
    r = lambda y: f'<td class="n">{v[2026] / v[y]:.1f}</td>' if v[y] and v[y] >= 5 else '<td class="n">–</td>'
    rows.append(f'<tr><td>{place[name]}</td><td class="n">{abs(lat):.1f}°{"S" if lat < 0 else "N"}</td>' + "".join(num(v[y]) for y in (1997, 2015, 2026)) + r(1997) + r(2015) + '</tr>')
open(O + 't_late.html', 'w').write('<div class="tablewrap"><table>\n' + "\n".join(rows) + '\n</table></div>\n')
# (b) tropics and San Diego by month
rows = ['<tr><th></th>' + "".join(f'<th class="n">{m}</th>' for m in ("May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")) + '</tr>']
for y in (1997, 2015, 2026):
    rows.append(f'<tr><td>Ecuador and the Galápagos, {y}</td>' + "".join(num(P.trop(y, m)) for m in range(5, 13)) + '</tr>')
for y in (1997, 2015, 2026):
    rows.append(f'<tr><td>San Diego, {y}</td>' + "".join(num(P.g("San Diego", y, m)) for m in range(5, 13)) + '</tr>')
open(O + 't_pairs.html', 'w').write('<div class="tablewrap"><table>\n' + "\n".join(rows) + '\n</table></div>\n')
# (c) satellites by stretch of coast
pts = json.load(open('/home/agent1/trace/data/alt/points.json')); raw = np.load('/home/agent1/trace/alt_raw.npy'); sm = np.load('/home/agent1/trace/alt_smooth.npy'); D0 = dt.date(2026, 5, 1)
ix = lambda d: (d - D0).days
def mm(kms, m):
    a = ix(dt.date(2026, m, 1)); b = ix(dt.date(2026, m + 1, 1)) if m < 11 else ix(dt.date(2026, 11, 25)) + 1
    return float(np.nanmean([np.nanmean(raw[i, a:b]) for i, p in enumerate(pts) if p['km'] in kms]))
def half(kms):
    out = []
    for i, p in enumerate(pts):
        if p['km'] not in kms: continue
        x = sm[i]; jul = np.nanmean(x[ix(dt.date(2026, 7, 1)):ix(dt.date(2026, 8, 1))]); nov = np.nanmean(x[ix(dt.date(2026, 11, 1)):ix(dt.date(2026, 11, 23))]); h = (jul + nov) / 2
        for k in range(ix(dt.date(2026, 7, 1)), len(x) - 10):
            seg = x[k:k + 10]
            if not np.isnan(seg).any() and (seg >= h).all(): out.append(k); break
    return (D0 + dt.timedelta(days=int(np.median(out)))).strftime('%-d %b')
rows = ['<tr><th>stretch of coast</th><th class="n">points</th>' + "".join(f'<th class="n">{m}</th>' for m in ("Jul", "Aug", "Sep", "Oct", "1–25 Nov")) + '<th class="n">halfway on</th></tr>']
for name, a, b in (("Peru and Ecuador", -1200, 400), ("Colombia to Costa Rica", 500, 2000), ("El Salvador to Acapulco", 2100, 4000), ("Acapulco to Cabo San Lucas", 4100, 5400),
                   ("Baja California, Pacific side", 5500, 6600), ("San Diego to Point Conception", 6700, 7100), ("central California", 7200, 7800), ("north of Cape Mendocino", 7900, 8800)):
    ks = tuple(range(a, b + 1, 100))
    rows.append(f'<tr><td>{name}</td><td class="n">{len(ks)}</td>' + "".join(num(mm(ks, m)) for m in range(7, 12)) + f'<td class="n">{half(ks)}</td></tr>')
open(O + 't_sat.html', 'w').write('<div class="tablewrap"><table>\n' + "\n".join(rows) + '\n</table></div>\n')
# (d) the step, gauge by gauge: as measured, and with the barometer taken out
NM = {"North Spit": "North Spit, Humboldt Bay", "Charleston": "Charleston, Oregon", "South Beach": "South Beach, Oregon", "Port Orford": "Port Orford, Oregon", "Garibaldi": "Garibaldi, Oregon",
      "Toke Point": "Toke Point, Washington", "Neah Bay": "Neah Bay, Washington"}
rows = ['<tr><th>gauge</th><th class="n">km from San Diego</th><th class="n">rise, cm</th><th class="n">passed halfway (UTC)</th><th class="n">hours after San Diego</th>'
        '<th class="n">air pressure, hPa</th><th class="n">rise, barometer out</th><th class="n">passed halfway</th><th class="n">hours after San Diego</th></tr>']
t0, t0b = W.rows[0][4], W.rows_ib[0][4]
for (name, km, B, A, arr, dp), (_, _, Bb, Ab, arrb, _) in zip(W.rows, W.rows_ib):
    when = (W.T0 + dt.timedelta(hours=arr)).strftime('%-d %b %H:%M') if arr is not None else 'under 5 cm'
    if Bb is None: tail = '<td class="n">–</td><td class="n">no record</td><td class="n">–</td><td class="n">–</td>'
    else:
        whenb = (W.T0 + dt.timedelta(hours=arrb)).strftime('%-d %b %H:%M') if arrb is not None else 'under 5 cm'
        tail = f'{num(dp)}{num(Ab - Bb)}<td class="n">{whenb}</td><td class="n">{arrb - t0b if arrb is not None else "–"}</td>'
    rows.append(f'<tr><td>{NM.get(name, name)}</td><td class="n">{km:.0f}</td>{num(A - B)}<td class="n">{when}</td><td class="n">{arr - t0 if arr is not None else "–"}</td>{tail}</tr>')
open(O + 't_wave.html', 'w').write('<div class="tablewrap"><table>\n' + "\n".join(rows) + '\n</table></div>\n')
print(open(O + 't_sat.html').read()); print(open(O + 't_late.html').read()[:900])
