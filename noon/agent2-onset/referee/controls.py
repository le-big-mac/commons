"""Referee's controls (step 2). Usage: python controls.py <task>"""
import sys, time
import numpy as np
import kur

task = sys.argv[1]
t0 = time.time()
se = lambda x: np.std(x, ddof=1) / np.sqrt(len(x))

if task in ("below-regular", "below-random"):
    kind = task.split("-")[1]
    N, R, T = 1000, 48, 400
    rng = np.random.default_rng(301 if kind == "regular" else 302)
    rec = kur.runs("gauss", kind, N, 0.5, T, R, rng)
    t = np.arange(rec.shape[1]) * kur.DT
    print(f"control below: Gaussian {kind} N={N} K=0.5, {R} runs, N<r^2> by window (linear-response theory for a smooth Gaussian: 2.484)")
    for a, b in ((12.5, 25), (25, 50), (50, 100), (100, 200), (200, 300), (300, 400)):
        q = N * (rec[:, (t >= a) & (t < b)] ** 2).mean(axis=1)
        print(f"   t {a:5.1f}-{b:5.1f}: {q.mean():.3f} +- {se(q):.3f}")

elif task == "finesweep":
    for seed in (401, 402):
        rng = np.random.default_rng(seed)
        N = 2000
        om = kur.freqs("uniform", "regular", N, 1, rng)
        th = rng.random((1, N)) * 2 * np.pi
        nst = int(round(200 / kur.DT))
        # approach as the author does (0.80 .. 0.94 by 0.02), then fine steps
        for K in [round(0.80 + 0.02 * i, 2) for i in range(8)]:
            th, rec = kur.integrate(om, th, K, nst)
        up = [round(0.96 + 0.005 * i, 3) for i in range(17)]
        down = up[-2::-1]
        ru, rd = {}, {}
        for K in up:
            th, rec = kur.integrate(om, th, K, nst); ru[K] = rec[0, nst // 2:].mean()
        for K in down:
            th, rec = kur.integrate(om, th, K, nst); rd[K] = rec[0, nst // 2:].mean()
        rd[up[-1]] = ru[up[-1]]
        print(f"control fine sweep (uniform regular N=2000, step 0.005, 200 per step) seed {seed}")
        for K in up:
            print(f"   K={K:.3f}  up {ru[K]:.4f}  down {rd[K]:.4f}")
        print(f"   first K up with r>0.5: {min(k for k in up if ru[k] > 0.5):.3f};  lowest K down with r>0.5: {min(k for k in rd if rd[k] > 0.5):.3f}", flush=True)
    # dwell at exactly K = 1 from random phases: does the population jump if one waits?
    rng = np.random.default_rng(403)
    rec = kur.runs("uniform", "regular", 2000, 1.0, 2000, 4, rng)
    t = np.arange(rec.shape[1]) * kur.DT
    print("control dwell at K=1.00 (uniform regular N=2000, 4 runs from random phases, T=2000): mean r per window, per run")
    for a, b in ((0, 100), (100, 200), (200, 400), (400, 800), (800, 1200), (1200, 2000)):
        w = rec[:, (t >= a) & (t < b)].mean(axis=1)
        print(f"   t {a:5d}-{b:5d}: " + " ".join(f"{x:.3f}" for x in w))

elif task == "cubic":
    # direct test of dr/dt = -r^3/4 at K = 1 (Gaussian): big population, start synchronised, relax at K=1.2, then set K=1
    N = 20000
    rng = np.random.default_rng(501)
    om = kur.freqs("gauss", "regular", N, 1, rng)
    th = np.zeros((1, N))
    th, _ = kur.integrate(om, th, 1.2, int(60 / kur.DT))
    th, rec = kur.integrate(om, th, 1.0, int(600 / kur.DT))
    r = rec[0]; t = np.arange(len(r)) * kur.DT
    np.save("/home/agent2/onset/referee/cubic_rec.npy", r[::20])
    print(f"control cubic: Gaussian regular N={N}, K switched from 1.2 (r={r[0]:.3f}) to 1.0 at t=0")
    for a, b in ((0, 25), (25, 50), (50, 100), (100, 200), (200, 400), (400, 600)):
        sel = (t >= a) & (t <= b)
        sl = np.polyfit(t[sel], 1 / r[sel] ** 2, 1)[0]
        print(f"   t {a:4d}-{b:4d}: r from {r[sel][0]:.4f} to {r[sel][-1]:.4f};  d(1/r^2)/dt = {sl:.4f}   (the README's equation says 0.5)")

elif task == "dt":
    dt, R = float(sys.argv[2]), int(sys.argv[3])
    N, T = 3200, 600
    rng = np.random.default_rng(601 + int(dt * 1000))
    nst = int(round(T / dt))
    ms = []
    for c in range(0, R, 6):
        m = min(6, R - c)
        om = kur.freqs("gauss", "regular", N, m, rng)
        th0 = rng.random((m, N)) * 2 * np.pi
        _, rec = kur.integrate(om, th0, 1.0, nst, dt=dt)
        ms.extend(rec[:, nst // 2:].mean(axis=1))
    ms = np.array(ms)
    print(f"control dt: Gaussian regular N=3200 K=1 T=600 step {dt}: mean measured r (300-600) = {ms.mean():.4f} +- {se(ms):.4f}, sd between runs {ms.std(ddof=1):.4f}, {R} runs")

elif task == "threedec":
    rng = np.random.default_rng(701)
    for shape, K, th in (("gauss", 1.5, 0.84968), ("lorentz", 2.0, 0.70711), ("uniform", 1.05, 0.84780)):
        m = kur.measured(kur.runs(shape, "random", 2000, K, 400, 8, rng))
        print(f"control random tempos N=2000 T=400 {shape} K={K}: mean {m.mean():.4f}, sd between runs {m.std(ddof=1):.4f}, range {m.min():.4f}-{m.max():.4f}  (limit {th:.4f}), 8 runs", flush=True)

elif task == "randlong":
    N, R, T = 3200, 16, 1200
    rng = np.random.default_rng(801)
    rec = kur.runs("gauss", "random", N, 1.0, T, R, rng)
    t = np.arange(rec.shape[1]) * kur.DT
    w1 = rec[:, (t >= 300) & (t < 600)].mean(axis=1)
    w2 = rec[:, (t >= 600) & (t < 900)].mean(axis=1)
    w3 = rec[:, (t >= 900) & (t <= 1200)].mean(axis=1)
    o = np.argsort(w1)
    print(f"control random long: Gaussian random N={N} K=1, {R} runs, per run (sorted by the 300-600 reading): 300-600, 600-900, 900-1200")
    for i in o:
        print(f"   {w1[i]:.4f}  {w2[i]:.4f}  {w3[i]:.4f}")
    print(f"   means: {w1.mean():.4f} {w2.mean():.4f} {w3.mean():.4f};  the eight lowest runs: {w1[o[:8]].mean():.4f} {w2[o[:8]].mean():.4f} {w3[o[:8]].mean():.4f}")

print(f"# {task} done in {time.time()-t0:.0f}s", flush=True)
