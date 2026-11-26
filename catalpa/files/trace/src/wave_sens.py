# How much the fitted speed of the step depends on the choices in wave.py: the "before" and "after" windows and the
# fraction of the rise that counts as arrival. Exploration.
import sys, io, contextlib, importlib.util, datetime as dt
import numpy as np
spec = importlib.util.spec_from_file_location('wave', '/home/agent1/trace/src/wave.py')
W = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(W)
from coastline import gc
print("before window    after window    fraction  gauges  km/day  scatter h   San Diego arrival")
for bw in (((9, 20), (9, 27)), ((9, 16), (9, 27)), ((9, 22), (9, 27))):
    for aw in (((10, 1), (10, 6)), ((10, 1), (10, 4)), ((10, 2), (10, 6))):
        for frac in (0.3, 0.5, 0.7):
            km = 0.0; prev = None; pts = []
            for sid, name, lat, lon in W.ST:
                if prev: km += gc(prev, (lat, lon))
                prev = (lat, lon); y = W.filt(sid)
                B = np.nanmean(y[W.h(bw[0]):W.h(bw[1])]); A = np.nanmean(y[W.h(aw[0]):W.h(aw[1])])
                if A - B < 5: continue
                lev = B + frac * (A - B)
                for k in range(W.h((9, 26)), W.h((10, 6))):
                    seg = y[k:k + 12]
                    if not np.isnan(seg).any() and (seg >= lev).all(): pts.append((km, k)); break
            x = np.array([p[0] for p in pts]); t = np.array([p[1] for p in pts], float)
            s, c = np.polyfit(x, t, 1)
            print(f"{bw[0][1]:2d}-{bw[1][1]-1:2d} Sep        {aw[0][1]}-{aw[1][1]-1} Oct         {frac:.1f}     {len(pts):3d}   {1 / s * 24:6.0f}   {np.std(t - (c + s * x)):6.1f}     {(W.T0 + dt.timedelta(hours=int(pts[0][1]))).strftime('%d %b %H:%M')}")
