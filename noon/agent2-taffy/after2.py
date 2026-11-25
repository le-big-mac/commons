"""The two checks that after.py did not reach before it was stopped at its time limit.   usage: python after2.py > after2.out
(a) my odds against the forecasters' by how each line was arrived at; (b) the fluid for the no-growth device s_1 s_2, period by period."""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import taffy as TF
F = json.load(open('forecast/scored.json'))
print("5. My odds against the forecasters', by how each line was arrived at (the grouping is mine, made after the scores were known)")
ids = F['ids']; y = np.array(F['outcome']); me = np.array(F['mine']); med = np.array(F['median'])
for name, grp in (("worked by hand on the sheet (T1, T2, T3, T9)", ['T1', 'T2', 'T3', 'T9']), ("from memory or with a stated doubt (T4, T5, T6, T10)", ['T4', 'T5', 'T6', 'T10']), ("guesses about the fluid (T7, T8)", ['T7', 'T8'])):
    j = [ids.index(g) for g in grp]
    print(f"   {name}: my mean odds {me[j].mean():.3f}, theirs {med[j].mean():.3f}; Brier mine {((me[j] - y[j]) ** 2).mean():.4f}, theirs {((med[j] - y[j]) ** 2).mean():.4f}")
d = (me - y) ** 2 - (med - y) ** 2
print(f"   the gap in Brier score is {d.mean():+.4f}; T5 and T6 alone contribute {d[[ids.index('T5'), ids.index('T6')]].sum() / len(y):+.4f}, T4 {d[ids.index('T4')] / len(y):+.4f}, the other seven {d[[i for i, k_ in enumerate(ids) if k_ not in ('T4', 'T5', 'T6')]].sum() / len(y):+.4f}", flush=True)
print("6. The fluid for the no-growth device s_1 s_2: L/L0 after each period (stopped at 14 periods or 1.5 million points)")
moves = TF.DEVICES['T3'][1]; n = 3; dt = 0.005; x = TF.refine(TF.circle()); L0 = TF.length(x); t = 0.0; r = [1.0]
for per in range(14):
    for _ in range(len(moves) * 200):
        p1, v1 = TF.rods(moves, n, t); p2, v2 = TF.rods(moves, n, t + dt / 2); p3, v3 = TF.rods(moves, n, min(t + dt, math.floor(t) + 1 - 1e-12))
        k1 = TF.velocity(x, p1, v1); k2 = TF.velocity(x + 0.5 * dt * k1, p2, v2); k3 = TF.velocity(x + 0.5 * dt * k2, p2, v2); k4 = TF.velocity(x + dt * k3, p3, v3)
        x = TF.refine(x + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)); t = round(t + dt, 10)
    r.append(TF.length(x) / L0); print(f"   period {per + 1}: L/L0 = {r[-1]:.2f}, ratio to the period before {r[-1] / r[-2]:.3f}, {len(x)} points", flush=True)
    if len(x) > 1_500_000: break
r = np.array(r); k = np.arange(len(r)); late = k >= 6
ex = np.polyfit(k[late], np.log(r[late]), 1); quad = np.polyfit(k[late], r[late], 2)
print(f"   from period 6 on: an exponential fit gives x{math.exp(ex[0]):.3f} a period (rms miss {float(np.sqrt(np.mean((np.exp(np.polyval(ex, k[late])) - r[late]) ** 2))):.2f}); a parabola misses by {float(np.sqrt(np.mean((np.polyval(quad, k[late]) - r[late]) ** 2))):.2f}")
