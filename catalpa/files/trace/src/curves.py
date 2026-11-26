# Daily anomalies (rule L's line and waves evaluated day by day), 15-day running mean, every 5 days,
# 1 June to 31 October 2026 (the Hawaii files stop at 30 September; San Diego and San Francisco are
# carried through October with NOAA's hourly heights). Exploration after the sealed lines were scored.
import sys, io, contextlib, importlib.util, csv, datetime as dt
import numpy as np
spec = importlib.util.spec_from_file_location('trace', '/home/agent1/trace/src/trace.py')
T = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(T)
def fitday(name, d):
    # the monthly fit is a smooth function of time; evaluate it at the day
    yy = d.year + (d.timetuple().tm_yday - 0.5) / (366 if d.year % 4 == 0 else 365)
    return T.fit[name](yy, 0.5) if False else T.fit[name](d.year, (yy - d.year) * 12 + 0.5)
def coops(sid, name):
    # NOAA's hourly heights with the tide filtered out by Godin's filter (running means of 24, 24 and 25 hours folded
    # into one centred weight of 71 hours), read at noon UTC of each day. Values in cm above station datum.
    t0 = dt.datetime(2026, 1, 1); n = 24 * 330; x = np.full(n, np.nan)
    for r in csv.reader(open(f'/home/agent1/trace/data/coops/h{sid}.csv')):
        try: t = dt.datetime.strptime(r[0], '%Y-%m-%d %H:%M'); v = float(r[1])
        except (ValueError, IndexError): continue
        k = int((t - t0).total_seconds() // 3600)
        if 0 <= k < n: x[k] = v * 100
    y = godin(x)
    return {(t0 + dt.timedelta(hours=k)).date(): float(y[k]) for k in range(12, n, 24) if not np.isnan(y[k])}
K = np.convolve(np.convolve(np.ones(24), np.ones(24)), np.ones(25)); K = K / K.sum()
def godin(x):
    bad = np.convolve(np.isnan(x).astype(float), np.ones(len(K)), 'same') > 0
    y = np.convolve(np.where(np.isnan(x), 0, x), K, 'same'); y[bad] = np.nan
    y[:len(K) // 2] = np.nan; y[-(len(K) // 2):] = np.nan
    return y
def curve(name, y, d0, d1, extra=None, w=15):
    d = dict(T.daily[name])
    if extra:
        for k, v in extra.items(): d.setdefault(k, v)
    out = {}
    day = d0
    while day <= d1:
        seg = [d[day + dt.timedelta(days=k)] - fitday(name, day + dt.timedelta(days=k)) for k in range(-(w // 2), w // 2 + 1) if (day + dt.timedelta(days=k)) in d]
        out[day] = float(np.mean(seg)) if len(seg) >= 0.8 * w else None
        day += dt.timedelta(days=1)
    return out
if __name__ == "__main__":
    names = ["Callao", "La Libertad", "Santa Cruz", "San Diego", "San Francisco", "Crescent City", "Neah Bay"]
    ex = {"San Diego": coops("9410170", "San Diego"), "San Francisco": coops("9414290", "San Francisco"),
          "Crescent City": coops("9419750", "Crescent City"), "Neah Bay": coops("9443090", "Neah Bay")}
    for y in (2026, 1997, 2015):
        d0, d1 = dt.date(y, 6, 1), dt.date(y, 12, 31) if y != 2026 else dt.date(2026, 10, 31)
        cs = {n: curve(n, y, d0, d1, ex.get(n) if y == 2026 else None) for n in names}
        print(f"\n{y}: 15-day running mean of the daily anomaly, cm")
        print("date        " + "".join(f"{n[:11]:>12}" for n in names))
        day = d0
        while day <= d1:
            print(f"{day}  " + "".join(("           -" if cs[n][day] is None else f"{cs[n][day]:12.1f}") for n in names))
            day += dt.timedelta(days=5)
