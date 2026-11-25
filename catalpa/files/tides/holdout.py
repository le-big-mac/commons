# Held-out test before anything is predicted for the future: fit on everything up to 30 days ago, predict the last 30 days, and set the errors beside NOAA's own predictions.
# usage: python -I holdout.py
import numpy as np, sys
sys.path.insert(0, '/home/agent1/tides')
from tide import *
print('station                 trained on (h)   last 30 days, hourly: sd of (observed - mine)   sd of (observed - NOAA)   sd of (mine - NOAA)   [cm; means removed]   in-sample sd')
for st, (name, lon) in STATIONS.items():
    t, y = load_noaa(st, 'water_level'); tp, yp = load_noaa(st, 'predictions')
    hourly = np.abs((t * 24) % 1.0) < 1e-6; t, y = t[hourly], y[hourly]; cut = t[-1] - 30.0; tr = t < cut; te = ~tr
    X = design(t, lon); w = np.linalg.lstsq(X[tr], y[tr], rcond=None)[0]; fit = X @ w
    noaa = np.interp(t, tp, yp); sd = lambda v: 100 * np.std(v)
    print(f'{name:22s}  {tr.sum():6d}            {sd((y - fit)[te]):6.2f}                          {sd((y - noaa)[te]):6.2f}                    {sd((fit - noaa)[te]):6.2f}                               {sd((y - fit)[tr]):6.2f}')
    for label, lags, extras in (('no lags but 0', (0.0,), True), ('lags 0, +-2 d', (-2.0, 0.0, 2.0), True), ('5 lags, no extras', LAGS, False)):
        X2 = design(t, lon, lags, extras); w2 = np.linalg.lstsq(X2[tr], y[tr], rcond=None)[0]; print(f'      variant {label:18s}: held-out sd of (observed - mine) {sd((y - X2 @ w2)[te]):6.2f}; of (mine - NOAA) {sd((X2 @ w2 - noaa)[te]):6.2f}')
