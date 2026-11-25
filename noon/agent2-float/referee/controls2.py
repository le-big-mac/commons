"""Step 2 controls: (d) dense grid of directions at all 97 registered densities against the author's lowest h in results.json;
(f) what the author's 'also stable' entries at 0.23-0.245 are."""
import json, math, sys
import numpy as np
from ref import h_vec
R = json.load(open('/home/agent2/float/results.json'))
step = 0.008
g = np.arange(-0.02, 1.03, step) + 0.37 * step
Pg, Qg = np.meshgrid(g, g, indexing='ij')
worst = (0, None); n_dir = Pg.size
for c in R['cube']:
    d = c['d']; lowest = min(m['h'] for m in c['minima'])
    H = h_vec(np.ones_like(Pg), Pg, Qg, d)
    gm = float(H.min())
    if lowest - gm > worst[0]:
        worst = (lowest - gm, d)
print("dense grid (%d directions, gnomonic step %.3f, covering the whole fundamental domain and its border) at all %d registered densities:" % (n_dir, step, len(R['cube'])))
print("   largest amount by which any grid direction is LOWER than the author's lowest minimum: %.3e (at d=%s)" % worst)
print("\nauthor's minima at 0.23-0.25 (results.json): tilt, azimuth, h, and h minus the tie-ring formula")
for c in R['cube']:
    d = c['d']
    if 0.2295 <= d <= 0.2505:
        ring = math.sqrt(12 * d * (1 - d) - 1) / (12 * d); tr = math.sqrt(12 * d * (1 - d) - 2)
        x = 2 * d / tr
        arc = 45 - math.degrees(math.acos(min(1.0, x / math.sqrt(2)))) if x < math.sqrt(2) else 45
        print("  d=%.3f (tie arc: azimuth <= %.2f deg, tilt %.3f deg, h=%.9f)" % (d, arc, math.degrees(math.atan(tr)), ring))
        for m in c['minima']:
            u = m['up']
            print("      %-34s tilt %.3f az %.2f  h=%.9f  h-ring=%+.2e" % (m['kind'], math.degrees(math.acos(u[0])), math.degrees(math.atan2(u[2], u[1])), m['h'], m['h'] - ring))
