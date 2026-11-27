# Writes page/t_north.html (the eighteen rises further north) and prints every figure the page's prose uses about
# them. Run: ~/ipd/.venv/bin/python -I src/page_north.py > north_page.out
import sys, io, contextlib, importlib.util, datetime as dt
import numpy as np
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
L = load('north_hourly_look'); H = L.H; EV = H.EV; KM = H.KM; ST = H.ST; W_ = H.W
def num(x): return ("−" if x < 0 else "") + f"{abs(x):.1f}"
MON = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
def day(d): return f"{d.day} {MON[d.month]} {d.year}"
rows = ['<tr><th>day in the list</th><th class="n">San Diego</th><th class="n">Los Angeles</th><th class="n">Port San Luis</th><th class="n">San Francisco</th><th class="n">Humboldt Bay</th><th class="n">gauges timed</th><th class="n">km a day</th><th class="n">scatter, hours</th><th>kind</th></tr>']
kinds = []; sizes = []
for e, sz in zip(EV, L.sizes):
    c, sp, sc, n = L.classify(e, 5, 12); kinds.append(c); sizes.append(sz)
    cell = lambda i: "" if sz[i] is None else num(sz[i])
    rows.append(f'<tr><td>{day(e["D"])}{" (hurricane near)" if e["hur"] else ""}</td>' + "".join(f'<td class="n">{cell(i)}</td>' for i in (0, 2, 4, 6, 9)) + f'<td class="n">{n}</td><td class="n">' + ("" if c is None else (f"{sp:,.0f}" if sp else "not northward")) + '</td><td class="n">' + ("" if sc is None else f"{sc:.0f}") + f'</td><td>{c or "too few gauges"}</td></tr>')
# 2026 put through what the eighteen are: from the largest day of its run (5 October), San Diego's halfway hour by the same search
r26 = L.r26s                                     # its first step, anchored on 28 September
Y26 = H.Y26; i0 = (dt.date(2026, 10, 5) - dt.date(2026, 9, 1)).days * 24; y = Y26[0]
B, A = np.nanmean(y[i0 - 240:i0 - 72]), np.nanmean(y[i0 + 24:i0 + 144]); k26 = H.cross(y, (A + B) / 2, i0 - 72, i0 + 24)
rws = H.single(Y26, (k26 // 24) * 24); ok = [(KM[i], r[1]) for i, r in enumerate(rws[:10]) if r and r[1] is not None and not r[2]]
s_, sc_ = H.line([o[0] for o in ok], [o[1] for o in ok]); r26L = [r[0] for r in rws]
kindL = "no order" if sc_ > 10 else ("north in order" if s_ > 0 and 150 <= 24 / s_ <= 1000 else "at once")
rows.append(f'<tr><td><strong>2026, from the largest day of its run (5 October), as the eighteen are</strong></td>' + "".join(f'<td class="n">{num(r26L[i])}</td>' for i in (0, 2, 4, 6, 9)) + f'<td class="n">{len(ok)}</td><td class="n">{24 / s_:,.0f}</td><td class="n">{sc_:.0f}</td><td>{kindL}</td></tr>')
rows.append(f'<tr><td><strong>2026, its first step (28 September)</strong></td>' + "".join(f'<td class="n">{num(r26[i])}</td>' for i in (0, 2, 4, 6, 9)) + '<td class="n">10</td><td class="n">440</td><td class="n">6</td><td>north in order</td></tr>')
open('/home/agent1/trace/page/t_north.html', 'w').write('<div class="tablewrap"><table>\n' + "\n".join(rows) + '\n</table></div>\n')
print("FIGURES FOR THE PAGE (the eighteen rises further north; sizes by the rule used for 2026)")
for i in (1, 2, 4, 6, 9, 10):
    v = [s[i] for s in sizes if s[i] is not None]
    print(f"  {ST[i][1]:<14} {KM[i]:5.0f} km: {len(v)} with a record; smallest {min(v):.1f}, middle {np.median(v):.1f}, largest {max(v):.1f}; 5 cm or more: {sum(1 for x in v if x >= 5)}" + (f"; 2026 as the eighteen are: {r26L[i]:.1f}, larger than that: {sum(1 for x in v if x > r26L[i])}; 2026's first step: {r26[i]:.1f}, larger than that: {sum(1 for x in v if x > r26[i])}" if i < 10 else ""))
v = [(s[6] / s[0]) for s in sizes if s[6] is not None]; print(f"  San Francisco's rise as a share of San Diego's: middle {np.median(v):.2f}; 2026 as the eighteen are: {r26L[6] / r26L[0]:.2f}, as large a share or larger: {sum(1 for x in v if x >= r26L[6] / r26L[0])} of {len(v)}; 2026's first step: {r26[6] / r26[0]:.2f}, as large or larger: {sum(1 for x in v if x >= r26[6] / r26[0])} of {len(v)}")
print(f"  2026 as the eighteen are: San Diego's halfway hour found at hour {k26} from 1 September ({dt.datetime(2026, 9, 1) + dt.timedelta(hours=k26):%d %b %H:%M}), the first hour searched; {len(ok)} gauges timed, {24 / s_:.0f} km/day, scatter {sc_:.1f} h: {kindL}")
print(f"  kinds at a floor of 5 cm: " + ", ".join(f"{k}: {sum(1 for x in kinds if x == k)}" for k in ("north in order", "at once", "no order")) + f"; too few gauges: {sum(1 for x in kinds if x is None)}")
for e, k in zip(EV, kinds):
    if k == "north in order":
        c, sp, sc, n = L.classify(e, 5, 12); c3, sp3, sc3, n3 = L.classify(e, 3, 12)
        print(f"     {e['D']}: {sp:.0f} km/day at a floor of 5 cm ({n} gauges, scatter {sc:.1f} h); at a floor of 3 cm: {c3}, " + (f"{sp3:.0f} km/day" if sp3 else "not northward") + f" ({n3} gauges, scatter {sc3:.1f} h)")

# 2026's sizes with the barometer taken out, on both footings (after the tenth reading)
YB = [W_.filt(sid, True) for sid, *_ in ST[:10]]
def sizes_at(Y, h0): return [None if r is None else r[0] for r in H.single(Y, h0)]
bL = sizes_at(YB, (k26 // 24) * 24); bF = sizes_at(YB, 27 * 24)
print("  2026 with the barometer out (San Diego, Port San Luis, San Francisco, Humboldt Bay): as the eighteen are " + ", ".join(f"{bL[i]:.1f}" for i in (0, 4, 6, 9)) + " (as measured " + ", ".join(f"{r26L[i]:.1f}" for i in (0, 4, 6, 9)) + "); the first step " + ", ".join(f"{bF[i]:.1f}" for i in (0, 4, 6, 9)) + " (as measured " + ", ".join(f"{r26[i]:.1f}" for i in (0, 4, 6, 9)) + ")")
