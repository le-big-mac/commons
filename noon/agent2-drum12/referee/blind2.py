import sys; sys.path.insert(0, "/home/agent2/drum12/referee")
import numpy as np, time, json
import sol
F = int(sys.argv[1]); Mmax = float(sys.argv[2]); seed = int(sys.argv[3]); nst = int(sys.argv[4]); R = int(sys.argv[5])
tlim = float(sys.argv[6]) if len(sys.argv) > 6 else 100.0
modes = sol.fam_modes(F); rng = np.random.default_rng(seed)
w = sol.ring_w(R); r = (np.arange(R) + 0.5) / R
t0 = time.time(); best = (9, None); log = []
for s in range(nst):
    if time.time() - t0 > tlim: break
    kind = (s + seed) % 6
    if kind == 0:
        a = np.zeros(R) if s == 0 else rng.uniform(0, 1, R) * Mmax * rng.uniform(0.2, 1)
    elif kind == 1:
        a = np.full(R, Mmax * rng.uniform(0.3, 1.0))
    elif kind == 2:
        a = rng.exponential(1, R); a *= Mmax * rng.uniform(0.3, 1) / (w @ a)
    elif kind == 3:
        k = rng.uniform(0.2, 0.8); a = np.where(r < k, 1.0, 0.0); a *= Mmax * rng.uniform(0.5, 1) / (w @ a)
    elif kind == 4:
        a = np.zeros(R)
        for _ in range(3):
            a += rng.uniform(0, 1) * np.exp(-((r - rng.uniform(0, 1)) / rng.uniform(0.05, 0.3))**2)
        a *= Mmax * rng.uniform(0.3, 1) / (w @ a)
    else:
        a = np.zeros(R); idx = rng.choice(R, 5, replace=False); a[idx] = rng.exponential(1, 5); a *= Mmax * rng.uniform(0.3, 1) / (w @ a)
    a, f = sol.slp(a, modes, Mmax, p=max(4, 320 // R), iters=250)
    a, f = sol.slp(a, modes, Mmax, p=max(8, 800 // R), iters=120, tr0=0.2)
    log.append((kind, f, w @ a))
    print("start %d kind %d miss %.4f%% mass %.3f  t=%.0fs" % (s, kind, 100 * f, w @ a, time.time() - t0), flush=True)
    if f < best[0]: best = (f, a)
f, a = best
a, f2 = sol.slp(a, modes, Mmax, p=max(8, 800 // R), iters=40, exact=True, tr0=0.05)
c = sol.misses(sol.ring_edges(R), 1 + a, modes, 40, exact=True)
print("BEST F=%d M=%.2f R=%d: fem miss %.4f%% -> exact-polished %.4f%%, exact recheck %.4f%%, mass used %.4f" % (F, Mmax, R, 100 * f, 100 * f2, 100 * np.abs(c).max(), w @ a))
print("misses %:", " ".join("(%d,%d)%+.3f" % (m, n, 100 * ci) for (m, n, _), ci in zip(modes[1:], c)))
print("load a by ring:", " ".join("%.2f" % x for x in a))
json.dump({"F": F, "M": Mmax, "R": R, "seed": seed, "a": a.tolist(), "exact": float(np.abs(c).max()), "log": log}, open("/home/agent2/drum12/referee/blind2_F%d_M%s_R%d_s%d.json" % (F, sys.argv[2], R, seed), "w"))
