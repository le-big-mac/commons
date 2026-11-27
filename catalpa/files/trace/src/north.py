# The eighteen quick rises at San Diego (rises.out): do they show at La Jolla, and further north at San Francisco
# and Crescent City? Daily values from the Hawaii files, cm above rule L, air pressure left in (as the eighteen are).
# The sum is the list's: mean of days +1..+5 less mean of days -10..-4, taken on day D + L at the other gauge.
# Rules fixed in expectations-7.md before this was run. Run: ~/ipd/.venv/bin/python -I src/north.py > north.out
import sys, io, contextlib, importlib.util, datetime as dt
import numpy as np
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
R = load('rises'); CO = R.CO; C = R.C; T = R.T
EV = R.events                                   # (day D, rise, two weeks on, level before) at San Diego
HUR = [bool(R.near(e[0], 64)) for e in EV]
def series(name): return {k: v - C.fitday(name, k) for k, v in T.daily[name].items() if k.year >= 1949}
S = {n: series(n) for n in ("San Diego", "La Jolla", "San Francisco", "Crescent City")}
def summ(name, day):
    m = CO.measure(S[name], day); return None if m is None else m[0]
def best(name, D, lags):
    v = [(summ(name, D + dt.timedelta(days=L)), L) for L in lags]; v = [x for x in v if x[0] is not None]
    return max(v) if v else None
LAGS = {"La Jolla": (0,), "San Francisco": (0, 1, 2, 3, 4), "Crescent City": (0, 1, 2, 3, 4, 5, 6)}
FLOOR = {"La Jolla": 8.0, "San Francisco": 5.0, "Crescent City": 5.0}
def ordinary(name, lags, floor):
    # every day of August-October 1950-2025 more than 20 days from each of the eighteen
    n = k = 0; vals = []
    for y in range(1950, 2026):
        day = dt.date(y, 8, 1)
        while day <= dt.date(y, 10, 31):
            if all(abs((day - e[0]).days) > 20 for e in EV):
                b = best(name, day, lags)
                if b is not None: n += 1; k += b[0] >= floor; vals.append(b[0])
            day += dt.timedelta(days=1)
    return n, k, vals
print("THE EIGHTEEN QUICK RISES AT SAN DIEGO, AND THE SAME SUM FURTHER NORTH (cm; lag in days after San Diego's day D)")
print(f"  {'day D':<11} {'San Diego':>9} {'La Jolla':>9} {'San Francisco':>16} {'Crescent City':>16}   hurricane near")
rows = []
for e, h in zip(EV, HUR):
    D = e[0]; lj = best("La Jolla", D, LAGS["La Jolla"]); sf = best("San Francisco", D, LAGS["San Francisco"]); cc = best("Crescent City", D, LAGS["Crescent City"])
    rows.append((D, e[1], lj, sf, cc, h))
    f = lambda b, lag=True: "      -" if b is None else (f"{b[0]:+6.1f} (+{b[1]}d)" if lag else f"{b[0]:+6.1f}")
    print(f"  {D}  {e[1]:+8.1f} {f(lj, False):>9} {f(sf):>16} {f(cc):>16}   {'yes' if h else '-'}")
res = {}
for name in ("La Jolla", "San Francisco", "Crescent City"):
    j = {"La Jolla": 2, "San Francisco": 3, "Crescent City": 4}[name]
    have = [r for r in rows if r[j] is not None]; hit = sum(1 for r in have if r[j][0] >= FLOOR[name])
    n, k, vals = ordinary(name, LAGS[name], FLOOR[name]); share = k / n
    ratio = float(np.median([r[j][0] / r[1] for r in have]))
    res[name] = (len(have), hit, share, ratio)
    print(f"\n{name}: {len(have)} of the eighteen have the days; {hit} reach {FLOOR[name]:.0f} cm (largest of lags {LAGS[name][0]} to {LAGS[name][-1]})")
    print(f"   ordinary days ({n}): {100 * share:.1f}% reach it, so chance gives {len(have) * share:.1f}; the middle ordinary value {np.median(vals):+.1f}, spread (sd) {np.std(vals):.1f}")
    print(f"   the eighteen: mean {np.mean([r[j][0] for r in have]):+.1f}, middle {np.median([r[j][0] for r in have]):+.1f}; middle of the ratio to San Diego's rise {ratio:.2f}")
    hh = [r[j][0] for r in have if r[5]]; nn = [r[j][0] for r in have if not r[5]]
    print(f"   with a hurricane near ({len(hh)}): mean {np.mean(hh):+.1f}; without ({len(nn)}): mean {np.mean(nn):+.1f}")
    if name != "La Jolla":
        lg = [r[j][1] for r in have if r[j][0] >= FLOOR[name]]
        print(f"   lag of the largest sum, for those that reach the floor: {sorted(lg)}")
print("\nTHE LINES OF expectations-7.md")
n1, h1, s1, q1 = res["La Jolla"]; n2, h2, s2, q2 = res["San Francisco"]; n3, h3, s3, q3 = res["Crescent City"]
print(f"G1 (La Jolla: 8 cm on the same day in all but two at most of those with the days): {h1} of {n1} -> " + ("HELD" if h1 >= n1 - 2 else "FAILED"))
print(f"G2 (San Francisco: at least half reach 5 cm, and at least twice the ordinary share): {h2} of {n2}, ordinary {100 * s2:.0f}% -> " + ("HELD" if h2 >= n2 / 2 and h2 / n2 >= 2 * s2 else "FAILED"))
print(f"G3 (San Francisco: middle ratio to San Diego's rise 0.4 or more): {q2:.2f} -> " + ("HELD" if q2 >= 0.4 else "FAILED"))
print(f"G4 (Crescent City: at least a third reach 5 cm, and at least one and a half times the ordinary share): {h3} of {n3}, ordinary {100 * s3:.0f}% -> " + ("HELD" if h3 >= n3 / 3 and h3 / n3 >= 1.5 * s3 else "FAILED"))
j = 3; have = [r for r in rows if r[j] is not None]; hh = np.mean([r[j][0] for r in have if r[5]]); nn = np.mean([r[j][0] for r in have if not r[5]])
print(f"G5 (San Francisco: the ones with a hurricane near have the larger mean): {hh:+.1f} against {nn:+.1f} -> " + ("HELD" if hh > nn else "FAILED"))
print("\nOTHER CHOICES (not sealed): San Francisco and Crescent City at other floors and lag ranges; the eighteen / ordinary share")
for name, j in (("San Francisco", 3), ("Crescent City", 4)):
    for lags in ((0,), (0, 1, 2), LAGS[name], tuple(range(-2, 7))):
        for fl in (4.0, 5.0, 6.0, 8.0):
            b = [best(name, r[0], lags) for r in rows]; b = [x for x in b if x is not None]
            n, k, vals = ordinary(name, lags, fl)
            print(f"   {name}, lags {lags[0]} to {lags[-1]}, floor {fl:.0f}: {sum(1 for x in b if x[0] >= fl)} of {len(b)}; ordinary {100 * k / n:.0f}% (chance {len(b) * k / n:.1f})")
