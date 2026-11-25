import sys; sys.path.insert(0, "/home/agent2/drum12/referee")
import numpy as np, json, time
import sol
# does a ring far outside 0.45 open a lower basin at the headline cases?  (the author's best twelve-mode loads have one; the sixteen-mode loads do not)
key, F, M, delta = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]); t0 = time.time()
best = json.load(open("/home/agent2/drum12/best.json")); a0 = np.array(best[key]['a']); w = sol.ring_w(40); modes = sol.fam_modes(F); res = []
for j in range(22, 40, 2):
    a = a0.copy(); a[18:] = 0; a *= (M - delta) / (w @ a); a[j] = delta / w[j]
    a, f = sol.slp(a, modes, M, p=20, iters=300); res.append((f, j, a))
    print("%s: outer ring %d (r %.3f-%.3f) seeded with %.2f skins -> ends at %.4f%% (FEM), mass beyond 0.45: %.3f  t=%.0fs" % (key, j, j / 40, (j + 1) / 40, delta, 100 * f, w[18:] @ a[18:], time.time() - t0), flush=True)
f, j, a = min(res, key=lambda z: z[0]); a, f = sol.slp(a, modes, M, p=20, iters=30, exact=True, tr0=0.05)
c = sol.misses(sol.ring_edges(40), 1 + a, modes, 40, exact=True)
print("BEST %s with an outer ring: %.4f%% exact (author's %.4f%%); mass beyond 0.45: %.3f; load: %s" % (key, 100 * np.abs(c).max(), 100 * best[key]['exact'], w[18:] @ a[18:], " ".join("%.3g" % x for x in a)))
json.dump(dict(a=a.tolist(), exact=float(np.abs(c).max())), open("/home/agent2/drum12/referee/outer_%s_%s.json" % (key.replace("|", "_"), sys.argv[4]), "w"))
