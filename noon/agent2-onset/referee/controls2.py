"""More referee controls. Usage: python -B controls2.py <task>"""
import sys, time
import numpy as np
import kur

task = sys.argv[1]
t0 = time.time()

if task == "bign":
    # does the 300-600 reading stay at 0.064 "whatever the size"?  One very large evenly spaced population.
    N = int(sys.argv[2]); T = 600
    rng = np.random.default_rng(901)
    om = kur.freqs("gauss", "regular", N, 1, rng)
    th0 = rng.random((1, N)) * 2 * np.pi
    _, rec = kur.integrate(om, th0, 1.0, int(T / kur.DT))
    r = rec[0]; t = np.arange(len(r)) * kur.DT
    np.save(f"/home/agent2/onset/referee/bign_{N}.npy", r[::20])
    print(f"control big N: Gaussian regular N={N} K=1, one run, mean r by window:")
    for a, b in ((0, 50), (50, 100), (100, 200), (200, 300), (300, 450), (450, 600), (300, 600)):
        print(f"   {a:4d}-{b:4d}: {r[(t >= a) & (t <= b)].mean():.4f}")
    print(f"   largest r {r.max():.4f} at t = {t[r.argmax()]:.0f}; 0.9 N^(-1/4) = {0.9 * N ** -0.25:.4f}")

elif task == "author-dt":
    # the author's own job for P2 (step 0.1, seed 6), run through the author's onset.py, read run by run
    sys.path.insert(0, "/home/agent2/onset")
    import onset as O
    for dt, seed in ((0.1, 6),):
        O.DT = dt
        rng = np.random.default_rng(seed)
        om = O.regular("gauss", 3200, 8)
        _, _, _, rs = O.simulate(om, 1.0, 600, rng, series=True)
        t = np.arange(rs.shape[0]) * dt
        w = rs[(t >= 300) & (t < 600)].mean(axis=0)
        print(f"author's code, step {dt}, seed {seed}: 300-600 per run: " + " ".join(f"{x:.4f}" for x in w) + f"; mean {w.mean():.4f}, sd {w.std(ddof=1):.4f}")
        pk = rs[(t < 300)].max(axis=0)
        print("   largest r before t=300 per run: " + " ".join(f"{x:.3f}" for x in pk))
        # the same initial phases through my integrator, to compare the two codes early on (before chaos separates them)
        rng = np.random.default_rng(seed)
        th0 = rng.uniform(0, 2 * np.pi, om.shape)
        _, rec = kur.integrate(om.copy(), th0, 1.0, int(600 / dt), dt=dt)
        mine = rec.T[:-1]
        for tt in (5, 20, 50, 100):
            i = int(tt / dt)
            print(f"   t={tt}: largest difference in r between the two codes over the 8 runs: {np.abs(mine[i] - rs[i]).max():.2e}")
        w2 = mine[(t >= 300) & (t < 600)].mean(axis=0)
        print(f"   my integrator from the same phases: 300-600 per run: " + " ".join(f"{x:.4f}" for x in w2) + f"; mean {w2.mean():.4f}")

print(f"# {task} done in {time.time()-t0:.0f}s", flush=True)
