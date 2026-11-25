# Fit on everything observed so far (hourly), then write the forecast: six-minute levels from now to ten days on, for three stations.
# usage: python -I predict.py   -> forecast_<station>.csv (UTC time, my level in m above MSL datum, NOAA's prediction for the same instant)
import numpy as np, sys, hashlib
sys.path.insert(0, '/home/agent1/tides')
from tide import *
START, END = day_of('2026-11-25 15:30'), day_of('2026-12-05 18:00')
for st, (name, lon) in STATIONS.items():
    t, y = load_noaa(st, 'water_level'); tp, yp = load_noaa(st, 'predictions')
    hourly = np.abs((t * 24) % 1.0) < 1e-6; th, yh = t[hourly], y[hourly]
    X = design(th, lon); w = np.linalg.lstsq(X, yh, rcond=None)[0]
    tf = START + np.arange(int(round((END - START) * 240)) + 1) / 240.0; f = design(tf, lon) @ w
    # the part that is not tide: carry the recent offset forward.  fast = mean of (observed - model) over the last 24 h, slow = over the last 15 days;
    # the forecast offset starts at fast and relaxes to slow with a 2-day time constant.  The same recipe is applied to NOAA's predictions.
    t0 = t[-1]; nz = np.interp(tf, tp, yp); off = {}
    for key, model_past in (('mine', design(t[t > t0 - 15], lon) @ w), ('noaa', np.interp(t[t > t0 - 15], tp, yp))):
        r = y[t > t0 - 15] - model_past; tr_ = t[t > t0 - 15]; fast, slow = r[tr_ > t0 - 1].mean(), r.mean(); off[key] = (fast, slow, slow + (fast - slow) * np.exp(-(tf - t0) / 2.0))
    with open(f'forecast_{st}.csv', 'w') as out:
        out.write('UTC,mine_m,noaa_m,mine_offset_m,noaa_offset_m\n')
        for i in range(len(tf)): out.write(f'{when(tf[i])},{f[i]:.4f},{nz[i]:.4f},{off["mine"][2][i]:.4f},{off["noaa"][2][i]:.4f}\n')
    print(f'   offsets carried forward (cm): mine fast {100 * off["mine"][0]:+.1f}, slow {100 * off["mine"][1]:+.1f};  NOAA fast {100 * off["noaa"][0]:+.1f}, slow {100 * off["noaa"][1]:+.1f}')
    np.save(f'weights_{st}.npy', w)
    print(f'{name}: fitted on {len(th)} hourly values, {when(th[0])} to {when(th[-1])} (last observation used); in-sample sd {100 * np.std(yh - X @ w):.2f} cm; forecast {when(tf[0])} to {when(tf[-1])}, {len(tf)} values; sha256 {hashlib.sha256(open(f"forecast_{st}.csv","rb").read()).hexdigest()[:16]}')
