# Every number in the page's prose that is not already a line of another output. Run after trace.py, october.py,
# alt_trace.py: ~/ipd/.venv/bin/python -I src/facts.py > facts.out
import sys, io, contextlib, importlib.util, json, datetime as dt
import numpy as np
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
P = load('pairs'); T = P.T
print("TROPICS = mean of La Libertad and Santa Cruz, rule L, cm")
for y in (1997, 2015, 2026):
    v = [P.trop(y, m) for m in range(5, 10)]
    print(f"  {y}: May-Sep by month " + ", ".join(f"{x:.1f}" for x in v) + f"; mean {np.mean(v):.1f}; September {v[-1]:.1f}; August {v[-2]:.1f}")
m97, m26 = np.mean([P.trop(1997, m) for m in range(5, 10)]), np.mean([P.trop(2026, m) for m in range(5, 10)])
print(f"  May-Sep mean, 2026 over 1997: {m26 / m97:.2f}; September, 2026 over 1997: {P.trop(2026, 9) / P.trop(1997, 9):.2f}; over 2015: {P.trop(2026, 9) / P.trop(2015, 9):.2f}")
print("  1997-98 highest month: " + ", ".join(f"{n} {max((T.anom(n, y, m), y, m) for y in (1997, 1998) for m in range(1, 13) if T.anom(n, y, m) is not None)}" for n in ("La Libertad", "Santa Cruz", "Baltra", "Callao")))
best = max((P.trop(y, m), y, m) for y in (1997, 1998) for m in range(1, 13) if P.trop(y, m) is not None); print(f"  tropics' highest month of 1997-98: {best[0]:.1f} in {best[1]}-{best[2]:02d}")
first = [(y, m) for y in (1997,) for m in range(1, 13) if P.trop(y, m) is not None and P.trop(y, m) >= P.trop(2026, 9)]
print(f"  months of 1997 in which the tropics stood at or above September 2026's {P.trop(2026, 9):.1f}: {first}")
print("  September by gauge, 1997 / 2015 / 2026: " + "; ".join(f"{n} {T.anom(n, 1997, 9):.1f} / {T.anom(n, 2015, 9) if T.anom(n, 2015, 9) is not None else float('nan'):.1f} / {T.anom(n, 2026, 9):.1f}" for n in ("Callao", "La Libertad", "Santa Cruz", "Baltra")))
print("\nSAN DIEGO, rule L, cm")
print("  " + ", ".join(f"{y}: Aug {T.anom('San Diego', y, 8):.1f}, Sep {T.anom('San Diego', y, 9):.1f}, Oct {P.g('San Diego', y, 10):.1f}" for y in (1997, 2015, 2026)))
print(f"  October 2026 over October 1997: {33.0 / T.anom('San Diego', 1997, 10):.2f}; over October 2015: {33.0 / T.anom('San Diego', 2015, 10):.2f}")
top = sorted(((T.anom('San Diego', y, m), y, m) for (y, m) in T.mon['San Diego'] if 1990 <= y <= 2025), reverse=True)[:3]
print("  three highest months of 1990-2025: " + ", ".join(f"{v:.1f} ({y}-{m:02d})" for v, y, m in top))
print("  San Diego's month over the tropics' month before: " + ", ".join(f"{y} Oct/Sep {P.g('San Diego', y, 10) / P.trop(y, 9):.2f}" for y in (1997, 2015, 2026)) + f"; 2026 Nov(1-24)/Oct(satellite near La Libertad 37.1): {32.3 / 37.1:.2f}")
print("\nSATELLITE AGAINST GAUGE (different baselines: 2017-2025 for the satellite, rule L for the gauge), cm")
pts = json.load(open('/home/agent1/trace/data/alt/points.json')); raw = np.load('/home/agent1/trace/alt_raw.npy'); D0 = dt.date(2026, 5, 1)
def mm(kms, m):
    a = (dt.date(2026, m, 1) - D0).days; b = (dt.date(2026, m + 1, 1) - D0).days if m < 11 else (dt.date(2026, 11, 25) - D0).days + 1
    return float(np.nanmean([np.nanmean(raw[i, a:b]) for i, p in enumerate(pts) if p['km'] in kms]))
print("  near La Libertad (0, 100, 200 km): " + ", ".join(f"{dt.date(2026, m, 1).strftime('%b')} {mm((0, 100, 200), m):.1f}" for m in range(6, 12)) + f"; the gauge: Aug {T.anom('La Libertad', 2026, 8):.1f}, Sep {T.anom('La Libertad', 2026, 9):.1f}")
print("  off San Diego (6,800 km): " + ", ".join(f"{dt.date(2026, m, 1).strftime('%b')} {mm((6800,), m):.1f}" for m in range(6, 12)) + f"; the gauge: Aug {T.anom('San Diego', 2026, 8):.1f}, Sep {T.anom('San Diego', 2026, 9):.1f}, Oct 33.0, 1-24 Nov 32.3")
print("  off San Francisco (7,600 km): " + ", ".join(f"{dt.date(2026, m, 1).strftime('%b')} {mm((7600,), m):.1f}" for m in range(6, 12)) + "; the gauge: Oct 25.8, 1-24 Nov 31.4")
for name, a, b in (("Peru and Ecuador, -1,200 to 400 km", -1200, 400), ("Colombia to Costa Rica, 500 to 2,000", 500, 2000), ("El Salvador to Acapulco, 2,100 to 4,000", 2100, 4000), ("Acapulco to Cabo San Lucas, 4,100 to 5,400", 4100, 5400),
                   ("Baja California, 5,500 to 6,600", 5500, 6600), ("San Diego to Point Conception, 6,700 to 7,100", 6700, 7100), ("central California, 7,200 to 7,800", 7200, 7800), ("north of Cape Mendocino, 7,900 to 8,800", 7900, 8800)):
    ks = tuple(range(a, b + 1, 100)); print(f"  {name:<46} " + "  ".join(f"{dt.date(2026, m, 1).strftime('%b')} {mm(ks, m):5.1f}" for m in range(7, 12)))
print("\nTHE SEALED LINES: sheet 1: T3, T6, T8 held of 8; sheet 2: S3, S5 held of 6; N1 failed. 5 of 15.")
odds = [(.75, 0), (.55, 0), (.60, 1), (.65, 0), (.65, 0), (.40, 1), (.35, 0), (.50, 1), (.45, 0), (.40, 0), (.65, 1), (.40, 0), (.55, 1), (.35, 0), (.60, 0)]
print(f"  Brier score over the 15: {np.mean([(p - o) ** 2 for p, o in odds]):.3f} (0.25 is what saying 50% to everything would score); sum of the odds given: {sum(p for p, o in odds):.2f} expected to hold, {sum(o for p, o in odds)} held")

# ---- added after the fresh reader's check (26 Nov, 17:30 on): the numbers the rewritten story uses
print("\nADDED AFTER THE CHECK")
print("  tropics, 2026 over 1997 by month, May to September: " + ", ".join(f"{P.trop(2026, m) / P.trop(1997, m):.2f}" for m in range(5, 10)))
print(f"  tropics, September: 2026 minus 1997 {P.trop(2026, 9) - P.trop(1997, 9):+.1f} cm, minus 2015 {P.trop(2026, 9) - P.trop(2015, 9):+.1f} cm")
print(f"  San Diego, October: 2026 minus 1997 {33.0 - T.anom('San Diego', 1997, 10):+.1f} cm, minus 2015 {33.0 - T.anom('San Diego', 2015, 10):+.1f} cm")
print("  the September ratio 2026 over 1997 if 'usual' were c cm lower: " + ", ".join(f"c={c:+d}: {(P.trop(2026, 9) + c) / (P.trop(1997, 9) + c):.2f}" for c in (-3, 0, 5, 10)))
print("  by gauge, September 2026 over 1997: " + ", ".join(f"{n} {T.anom(n, 2026, 9) / T.anom(n, 1997, 9):.2f}" for n in ("La Libertad", "Santa Cruz", "Baltra", "Callao", "San Diego")))
def peak(fn, years):
    return max((fn(y, m), y, m) for y in years for m in range(1, 13) if fn(y, m) is not None)
for ev, ys in (("1982-83", (1982, 1983)), ("1997-98", (1997, 1998)), ("2015-16", (2015, 2016))):
    a = peak(lambda y, m: P.g("San Diego", y, m), ys); b = peak(P.trop, ys)
    print(f"  {ev}: San Diego's highest month {a[0]:.1f} ({a[1]}-{a[2]:02d}); the tropics' highest month {b[0]:.1f} ({b[1]}-{b[2]:02d}); ratio {a[0] / b[0]:.2f}")
print(f"  2026 so far: San Diego's highest month 33.0 (October); over the tropics' September by gauge {33.0 / P.trop(2026, 9):.2f}; over October by satellite (37.1) {33.0 / 37.1:.2f}; over 1-25 November by satellite (46.5) {33.0 / 46.5:.2f}")
print(f"  San Diego when the tropics stood at September 2026's height in 1997: Nov {T.anom('San Diego', 1997, 11):.1f}, Dec {T.anom('San Diego', 1997, 12):.1f}, Jan {T.anom('San Diego', 1998, 1):.1f} (tropics Nov {P.trop(1997, 11):.1f}, Dec {P.trop(1997, 12):.1f})")
print("  San Diego's month over the tropics' month before, every pair where the tropics stood at 8 cm or more:")
for y0 in (1997, 2015, 2026):
    months = [(y0, m) for m in range(5, 13)] + [(y0 + 1, 1)]
    out = []
    for (y, m), (py, pm) in zip(months[1:], months[:-1]):
        a, b = P.g("San Diego", y, m), P.trop(py, pm)
        if a is not None and b is not None and b >= 8: out.append(f"{'JFMAMJJASOND'[m - 1]}{str(y)[2:]} {a / b:.2f}")
    print(f"    {y0}: " + ", ".join(out))
print(f"  Cocos Island to the nearest point of the coast line (Cabo Blanco, Costa Rica): {T.dist and __import__('coastline').gc((5.557, -87.048), (9.56, -85.11)):.0f} km")
print("  El Nino indices (NOAA CPC tables, August-October): see indices.out, copied from the first page's work")

# ---- added on the evening of 26 November, after the page first went up: the wind, the hurricane, the tally
print("\nADDED ON THE EVENING OF 26 NOVEMBER")
print("  San Diego above its level of 20-26 September (after2.out, H): 13-19 October as measured 28.5 - 13.8 = +14.7, barometer out 30.7 - 14.1 = +16.6;")
print("     20-29 October as measured 36.2 - 13.8 = +22.4, barometer out 38.1 - 14.1 = +24.0")
sheets = [("sheets 1 and 2 and N1", odds),
          ("sheet 3 (the wind)", [(.50, 1), (.30, 0), (.40, 0), (.40, 1), (.55, 0), (.25, 0), (.35, 0), (.15, 0)]),
          ("sheet 4 (earlier hurricanes)", [(.65, 1), (.60, 0), (.55, 1), (.40, 1), (.45, 1)]),
          ("sheet 5 (Kay and Nora)", [(.45, 0), (.45, 0)])]
allp = []
for name, o in sheets:
    allp += o; print(f"  {name}: {sum(x[1] for x in o)} of {len(o)} held; Brier {np.mean([(p - q) ** 2 for p, q in o]):.3f}")
print(f"  all {len(allp)} lines: {sum(x[1] for x in allp)} held; the odds summed to {sum(x[0] for x in allp):.2f}; Brier {np.mean([(p - q) ** 2 for p, q in allp]):.3f} (0.25 for saying 50% to everything)")
ev = sheets[1][1] + sheets[2][1] + sheets[3][1]
print(f"  the evening's three sheets together (the second page): {sum(x[1] for x in ev)} of {len(ev)} held; the odds summed to {sum(x[0] for x in ev):.2f}; Brier {np.mean([(p - q) ** 2 for p, q in ev]):.3f}")
