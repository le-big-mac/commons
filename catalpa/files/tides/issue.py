# One issue of the daily forecast: the same recipe as predict.py (which is sealed and left alone), with the time of issue as a parameter.
# usage: python -I issue.py <outdir> [cutoff 'YYYY-MM-DD HH:MM']     uses observations up to the cutoff (default: the last one on disk); forecasts 72 hours on from it.
# Writes <outdir>/forecast_<station>.csv (UTC, mine_m, noaa_m, mine_offset_m, noaa_offset_m) and <outdir>/meta.txt (last observation used, and the offsets).
import numpy as np, sys, os, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tide import load_noaa, design, when, day_of, STATIONS
out = sys.argv[1]; cutoff = day_of(sys.argv[2]) if len(sys.argv) > 2 else None; os.makedirs(out, exist_ok=True); meta = []
for st, (name, lon) in STATIONS.items():
    t, y = load_noaa(st, 'water_level'); tp, yp = load_noaa(st, 'predictions')
    if cutoff is not None: y = y[t <= cutoff + 1e-9]; t = t[t <= cutoff + 1e-9]
    hourly = np.abs((t * 24) % 1.0) < 1e-6; th, yh = t[hourly], y[hourly]
    X = design(th, lon); w = np.linalg.lstsq(X, yh, rcond=None)[0]
    t0 = t[-1]; tf = t0 + np.arange(1, 721) / 240.0; f = design(tf, lon) @ w; nz = np.interp(tf, tp, yp); off = {}
    for key, model_past in (('mine', design(t[t > t0 - 15], lon) @ w), ('noaa', np.interp(t[t > t0 - 15], tp, yp))):
        r = y[t > t0 - 15] - model_past; tr_ = t[t > t0 - 15]; fast, slow = r[tr_ > t0 - 1].mean(), r.mean(); off[key] = (fast, slow, slow + (fast - slow) * np.exp(-(tf - t0) / 2.0))
    fn = f'{out}/forecast_{st}.csv'
    with open(fn, 'w') as o:
        o.write('UTC,mine_m,noaa_m,mine_offset_m,noaa_offset_m\n')
        for i in range(len(tf)): o.write(f'{when(tf[i])},{f[i]:.4f},{nz[i]:.4f},{off["mine"][2][i]:.4f},{off["noaa"][2][i]:.4f}\n')
    meta.append(f'{st} last_observation_used {when(t0)} hourly_values_fitted {len(th)} in_sample_sd_cm {100 * np.std(yh - X @ w):.2f} offsets_cm mine_fast {100 * off["mine"][0]:+.1f} mine_slow {100 * off["mine"][1]:+.1f} noaa_fast {100 * off["noaa"][0]:+.1f} noaa_slow {100 * off["noaa"][1]:+.1f} sha256 {hashlib.sha256(open(fn, "rb").read()).hexdigest()}')
open(f'{out}/meta.txt', 'w').write('\n'.join(meta) + '\n'); print('\n'.join(meta))
