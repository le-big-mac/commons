# A second way to time the eighteen rises up the coast, chosen AFTER sheet 8 was scored and after I had looked at
# seven of them day by day (the halfway rule sorts badly when a rise comes in two steps). Settings fixed before
# the first run and not changed: San Diego's filtered level from 6 days before its halfway hour to 10 days after,
# against each gauge's level shifted by -72 to +168 hours; the shift with the highest correlation is the gauge's
# delay; gauges with a correlation under 0.6, or whose best shift is the first or last one tried, are not used;
# a line needs five gauges of the ten to Humboldt Bay. Kinds: scatter about the line of 12 hours or less and
# 24 to 160 hours per 1000 km (150 to 1000 km a day northward) = north in order; scatter of 12 hours or less and
# under 24 hours per 1000 km either way = at once; anything else = no order.
# Not sealed. Run: ~/ipd/.venv/bin/python -I src/north_lag.py > north_lag.out
import sys, io, contextlib, importlib.util, datetime as dt
import numpy as np
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
H = load('north_hourly'); KM = H.KM; ST = H.ST
LAGS = range(-72, 169)
def delay(x, y, k):
    w0, w1 = k - 6 * 24, k + 10 * 24; a = x[w0:w1]
    if np.isnan(a).mean() > 0.05: return None
    best = None
    for L in LAGS:
        if w0 + L < 0 or w1 + L > len(y): continue
        b = y[w0 + L: w1 + L]; ok = ~np.isnan(a) & ~np.isnan(b)
        if ok.mean() < 0.95: continue
        r = np.corrcoef(a[ok], b[ok])[0, 1]
        if best is None or r > best[0]: best = (r, L)
    return best
def event(Y, k):
    out = []
    for y in Y:
        out.append(None if y is None else delay(Y[0], y, k))
    use = [(KM[i], d[1]) for i, d in enumerate(out[:10]) if d is not None and d[0] >= 0.6 and LAGS[0] < d[1] < LAGS[-1]]
    if len(use) < 5: return out, len(use), None, None, None
    s, sc = H.line([u[0] for u in use], [u[1] for u in use]); s1000 = s * 1000
    kind = "north in order" if sc <= 12 and 24 <= s1000 <= 160 else ("at once" if sc <= 12 and abs(s1000) < 24 else "no order")
    return out, len(use), s1000, sc, kind
def cells(out): return " ".join("    -" if d is None else (f"{d[1]:5d}" if d[0] >= 0.6 and LAGS[0] < d[1] < LAGS[-1] else ("    x" if d[0] < 0.6 else "    e")) for d in out)
print("DELAY OF EACH GAUGE AFTER SAN DIEGO BY LAGGED CORRELATION (hours; 'x' correlation under 0.6, 'e' best shift at the end of the range, '-' no record)")
print(f"  {'day D':<11} " + " ".join(f"{n[:5]:>5}" for s, n, *_ in ST) + "   used  h/1000km   km/day  scatter h  kind")
o26, n26, s26, sc26, k26 = event(H.Y26 + [None], 27 * 24 + 16)
print(f"  {'2026-09-28':<11} " + cells(o26) + f"   {n26:4d}  {s26:8.1f}  " + (f"{24000 / s26:7.0f}" if s26 > 0 else "      -") + f"  {sc26:8.1f}   {k26}   (the halfway rule gave 440 km/day)")
kinds = {}
for e in H.EV:
    out, n, s1000, sc, kind = event(e["Y"], e["k"]); kinds[e["D"]] = kind
    print(f"  {str(e['D']):<11} " + cells(out) + f"   {n:4d}  " + ("" if s1000 is None else f"{s1000:8.1f}  " + (f"{24000 / s1000:7.0f}" if s1000 > 0 else "      -") + f"  {sc:8.1f}   {kind}") + ("   hurricane near" if e["hur"] else ""))
v = list(kinds.values())
print(f"\n  with a line: {sum(1 for k in v if k)} of {len(v)}; north in order {sum(1 for k in v if k == 'north in order')}, at once {sum(1 for k in v if k == 'at once')}, no order {sum(1 for k in v if k == 'no order')}")
for tag, sub in (("with a hurricane near", [e for e in H.EV if e["hur"]]), ("without", [e for e in H.EV if not e["hur"]])):
    kk = [kinds[e["D"]] for e in sub]; print(f"  {tag}: north in order {sum(1 for k in kk if k == 'north in order')}, at once {sum(1 for k in kk if k == 'at once')}, no order {sum(1 for k in kk if k == 'no order')}, no line {sum(1 for k in kk if k is None)}")
print("\n  delay at San Francisco (hours), where its correlation is 0.6 or more: " + ", ".join(str(event(e["Y"], e["k"])[0][6][1]) for e in H.EV if event(e["Y"], e["k"])[0][6] is not None and event(e["Y"], e["k"])[0][6][0] >= 0.6))
