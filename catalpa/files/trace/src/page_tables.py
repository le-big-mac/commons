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

# ---- added on the evening of 26 November: the buoys, Polo's track, the eighteen earlier passages
B = load('buoys'); CO = load('composite')
def n1(x, signed=True):
    if x is None or (isinstance(x, float) and np.isnan(x)): return '<td class="n">–</td>'
    return f'<td class="n">{(f"{x:+.1f}" if signed else f"{x:.1f}").replace("-", "−")}</td>'
place = {"46086": "San Clemente Basin", "46025": "Santa Monica Basin", "46053": "East Santa Barbara Channel", "46054": "West Santa Barbara Channel", "46011": "Santa Maria", "46028": "Cape San Martin",
         "46042": "Monterey", "46012": "Half Moon Bay", "46026": "San Francisco", "46013": "Bodega Bay", "46014": "Point Arena", "46022": "Eel River", "46027": "St Georges", "46015": "Port Orford"}
rows = ['<tr><th>buoy</th><th class="n">km from San Diego</th><th class="n">mean wind, September</th><th class="n">shift across the first rise</th><th class="n">larger than this share of other shifts</th><th class="n">shift across the second rise</th><th class="n">larger than</th></tr>']
for s in B.IDS + ["Bight", "Central"]:
    a = B.unusual(B.AF[s], B.shift1, B.h(9, 20), B.Y1(B.AF[s])); b = B.unusual(B.AF[s], B.shift2, B.h(10, 13), B.Y2(B.AF[s]))
    nm = f"{s} {place[s]}" if s in place else ("the three buoys of the Bight together" if s == "Bight" else "the five central buoys together")
    km_ = f"{B.geo[s][1]:.0f}" if s in B.geo else "–"
    pc = lambda u: '<td class="n">–</td>' if np.isnan(u[0]) else f'<td class="n">{100 * u[1]:.0f}%</td>'
    rows.append(f'<tr><td>{nm}</td><td class="n">{km_}</td>{n1(B.mean(B.AF[s], B.h(9, 3), B.h(10, 1)))}{n1(a[0])}{pc(a)}{n1(b[0])}{pc(b)}</tr>')
open(O + 't_buoys.html', 'w').write('<div class="tablewrap"><table>\n' + "\n".join(rows) + '\n</table></div>\n')
A4 = load('after4')
rows = ['<tr><th>hurricane</th><th>day</th><th class="n">winds, knots</th><th class="n">nearest to San Diego, km</th><th class="n">San Diego: rise</th><th class="n">two weeks on</th><th class="n">San Francisco: rise</th><th class="n">two weeks on</th></tr>']
near = {(r[1], r[2]): r[0] for r in A4.rows}
for e in CO.EV:
    Dd = e[2].date(); a = CO.measure(CO.A["San Diego"], Dd); b = CO.measure(CO.A["San Francisco"], Dd)
    rows.append(f'<tr><td>{e[1].title()}</td><td>{Dd.strftime("%-d %b %Y")}</td><td class="n">{e[5]}</td><td class="n">{near[(e[1], Dd)]:.0f}</td>{n1(a[0])}{n1(a[1])}{n1(b[0])}{n1(b[1])}</tr>')
rows.append(f'<tr><td><strong>mean of the eighteen</strong></td><td></td><td class="n"></td><td class="n"></td>{n1(float(CO.res["San Diego"][1].mean()))}{n1(float(CO.res["San Diego"][2].mean()))}{n1(float(CO.res["San Francisco"][1].mean()))}{n1(float(CO.res["San Francisco"][2].mean()))}</tr>')
far = [r for r in A4.rows if r[0] >= 400]; close = [r for r in A4.rows if r[0] < 400]
rows.append(f'<tr><td>mean of the three that came within 250 km of San Diego</td><td></td><td class="n"></td><td class="n"></td>{n1(float(np.mean([r[3] for r in close])))}{n1(float(np.mean([r[4] for r in close])))}<td class="n"></td><td class="n"></td></tr>')
rows.append(f'<tr><td>mean of the fifteen that stayed 600 km and more away</td><td></td><td class="n"></td><td class="n"></td>{n1(float(np.mean([r[3] for r in far])))}{n1(float(np.mean([r[4] for r in far])))}<td class="n"></td><td class="n"></td></tr>')
import datetime as _dt
DL = _dt.date(2015, 9, 9); la = CO.measure(CO.A["San Diego"], DL); lb = CO.measure(CO.A["San Francisco"], DL)
rows.append(f'<tr><td>Linda (not on the list: 420 km off)</td><td>9 Sep 2015</td><td class="n">105</td><td class="n">–</td>{n1(la[0])}{n1(la[1])}{n1(lb[0])}{n1(lb[1])}</tr>')
rows.append(f'<tr><td><strong>Polo</strong></td><td>28 Sep 2026</td><td class="n">110</td><td class="n">813</td>{n1(CO.mp[0])}{n1(CO.mp[1])}{n1(CO.mq[0])}{n1(CO.mq[1])}</tr>')
open(O + 't_passages.html', 'w').write('<div class="tablewrap"><table>\n' + "\n".join(rows) + '\n</table></div>\n')
# wind and sea timed by the same rule
rows = ['<tr><th>gauge</th><th class="n">the sea passed halfway (barometer out)</th><th>buoy</th><th class="n">the wind passed halfway</th></tr>']
fm = lambda k: (W.T0 + dt.timedelta(hours=k)).strftime('%-d %b %H:%M') if k is not None else '–'
for gname, gid, bids in (("Port San Luis", "9412110", ["46054", "46011"]), ("Monterey", "9413450", ["46028", "46042"]), ("San Francisco", "9414290", ["46012", "46026"]), ("Point Reyes", "9415020", ["46013"]), ("Arena Cove", "9416841", ["46014"])):
    ks = A4.halfway(W.filt(gid, ib=True))[0]
    for j, bid in enumerate(bids):
        rows.append(f'<tr><td>{gname if j == 0 else ""}</td><td class="n">{fm(ks) if j == 0 else ""}</td><td>{bid} {place[bid]}</td><td class="n">{fm(A4.halfway(B.AF[bid])[0])}</td></tr>')
open(O + 't_windsea.html', 'w').write('<div class="tablewrap"><table>\n' + "\n".join(rows) + '\n</table></div>\n')
import re as _re
rows = ['<tr><th>time, UTC</th><th>position</th><th class="n">winds, km/h</th><th class="n">km from San Diego</th><th class="n">km from Baja California\'s ocean side</th></tr>']
for l in open('/home/agent1/trace/polo.out').read().split('RACHEL')[0].splitlines()[1:]:
    w = l.split()
    if len(w) < 11 or int(w[0]) < 26: continue
    kmh = w[7].strip('()'); side = 'offshore' if w[10] == 'west' else 'inland'
    if w[1] == '29' and w[3] == '03:00': side = 'about to come ashore'
    rows.append(f'<tr><td>{w[1]} {w[2]} {w[3]}</td><td>{w[4]} {w[5]}</td><td class="n">{kmh}</td><td class="n">{w[8]}</td><td class="n">{w[9]}, {side}</td></tr>')
open(O + 't_polo.html', 'w').write('<div class="tablewrap"><table>\n' + "\n".join(rows) + '\n</table></div>\n')

# the eighteen quick rises since 1950 (rises.py)
R = load('rises')
rows = []
for d, r, af, base in R.events:
    h = R.near(d, 64)
    rows.append(f'<tr><td>{d.strftime("%-d %b %Y")}</td>{n1(r)}{n1(af)}{n1(base)}<td>{"; ".join(x.split(" (")[0] for x in h) if h else "none"}</td></tr>')
open(O + 't_rises.html', 'w').write("\n".join(rows) + "\n")
