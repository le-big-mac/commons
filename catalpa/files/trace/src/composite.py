# What San Diego's (and San Francisco's) daily sea level did around the eighteen hurricane passages of 1990-2025
# listed by passages.py. Scores the lines H1 to H5 of expectations-4.md. Hashed before the run.
# Run: ~/ipd/.venv/bin/python -I src/composite.py > composite.out
import sys, io, contextlib, importlib.util, datetime as dt
import numpy as np
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
C = load('curves'); T = C.T; PS = load('passages'); W = load('wave')
EV = PS.events()
def anom(name):
    return {k: v - C.fitday(name, k) for k, v in T.daily[name].items() if k.year >= 1989}
A = {n: anom(n) for n in ("San Diego", "San Francisco", "La Jolla")}
def span(a, D, k0, k1, need):
    v = [a[D + dt.timedelta(days=k)] for k in range(k0, k1 + 1) if (D + dt.timedelta(days=k)) in a]
    return float(np.mean(v)) if len(v) >= need else None
def measure(a, D):
    base = span(a, D, -10, -4, 5); r = span(a, D, 1, 5, 4); aft = span(a, D, 9, 13, 4)
    if base is None or r is None or aft is None: return None
    return r - base, aft - base, base
def curve(a, D):
    base = span(a, D, -10, -4, 5)
    return [None if base is None or (D + dt.timedelta(days=k)) not in a else a[D + dt.timedelta(days=k)] - base for k in range(-12, 21)]
res = {}
for n in ("San Diego", "San Francisco"):
    print(f"{n.upper()}: each passage; base = days D-10 to D-4; rise = days D+1 to D+5; afterwards = days D+9 to D+13; cm")
    print(f"{'storm':<11} {'day D':<11} {'kt':>4} {'base':>6} {'rise':>6} {'afterwards':>11}")
    rows = []
    for e in EV:
        D = e[2].date(); m = measure(A[n], D)
        if m is None: print(f"{e[1]:<11} {D}  {e[5]:>4}   not enough days"); continue
        rows.append((e[1], D, m[0], m[1])); print(f"{e[1]:<11} {D}  {e[5]:>4} {m[2]:6.1f} {m[0]:+6.1f} {m[1]:+11.1f}")
    r = np.array([x[2] for x in rows]); af = np.array([x[3] for x in rows]); res[n] = (rows, r, af)
    print(f"   {len(rows)} events: mean rise {r.mean():+.1f} cm (middle value {np.median(r):+.1f}; {int((r > 0).sum())} above zero); mean afterwards {af.mean():+.1f} cm")
    # yardstick: the same calendar day in other years with no passage within 20 days
    yr = []
    for e in EV:
        D = e[2].date()
        for y in range(1990, 2026):
            try: D2 = D.replace(year=y)
            except ValueError: continue
            if any(abs((D2 - x[2].date()).days) <= 20 for x in EV): continue
            m = measure(A[n], D2)
            if m is not None: yr.append(m[0])
    yr = np.array(yr)
    print(f"   yardstick ({len(yr)} ordinary cases): mean rise {yr.mean():+.2f} cm, spread (sd) {yr.std():.1f} cm; share above zero {100 * (yr > 0).mean():.0f}%; a mean of {len(rows)} ordinary cases would have sd {yr.std() / np.sqrt(len(rows)):.1f} cm")
    print(f"   share of ordinary cases with a rise larger than the events' mean {r.mean():+.1f}: {100 * (yr > r.mean()).mean():.0f}%")
    print("   mean curve, days -12 to +20: " + " ".join(f"{np.mean([c[i] for c in [curve(A[n], e[2].date()) for e in EV] if c[i] is not None]):+.1f}" for i in range(33)))
    print()
# Polo by the same measure: San Diego's daily series carried through October with NOAA's hourly heights
name = "San Diego"; d = dict(T.daily[name]); d.update({k: v for k, v in C.coops("9410170", name).items() if k > dt.date(2026, 9, 30)})
a26 = {k: v - C.fitday(name, k) for k, v in d.items() if k.year == 2026}
mp = measure(a26, dt.date(2026, 9, 28))
name = "San Francisco"; d = dict(T.daily[name]); d.update({k: v for k, v in C.coops("9414290", name).items() if k > dt.date(2026, 9, 30)})
b26 = {k: v - C.fitday(name, k) for k, v in d.items() if k.year == 2026}
mq = measure(b26, dt.date(2026, 9, 28))
print(f"POLO, D = 28 September 2026: San Diego base {mp[2]:.1f}, rise {mp[0]:+.1f}, afterwards {mp[1]:+.1f}; San Francisco base {mq[2]:.1f}, rise {mq[0]:+.1f}, afterwards {mq[1]:+.1f}")
print("   San Diego, days -12 to +20: " + " ".join("-" if x is None else f"{x:+.0f}" for x in curve(a26, dt.date(2026, 9, 28))))

print("\nTHE SEALED LINES")
rows, r, af = res["San Diego"]
print(f"H1: mean rise at San Diego {r.mean():+.1f} cm; 2 or more -> " + ("HELD" if r.mean() >= 2 else "FAILED"))
need = int(np.ceil(13 / 18 * len(r)))
print(f"H2: above zero in {int((r > 0).sum())} of {len(r)} (needs {need}) -> " + ("HELD" if (r > 0).sum() >= need else "FAILED"))
print(f"H3: mean afterwards {af.mean():+.1f} against half the mean rise {r.mean() / 2:+.1f} -> " + ("VOID (mean rise under 1 cm)" if r.mean() < 1 else ("HELD" if af.mean() < r.mean() / 2 else "FAILED")))
big = sorted(rows, key=lambda x: -x[2])[:3]
print(f"H4: Polo's rise {mp[0]:+.1f} cm; the largest earlier: " + ", ".join(f"{x[0]} {x[1].year} {x[2]:+.1f}" for x in big) + " -> " + ("HELD" if mp[0] > r.max() else "FAILED"))
r2 = res["San Francisco"][1]
print(f"H5: San Francisco mean rise {r2.mean():+.1f} cm against San Diego's {r.mean():+.1f} -> " + ("HELD" if 0 < r2.mean() < r.mean() else "FAILED"))
