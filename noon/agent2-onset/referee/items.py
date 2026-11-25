"""Blind items 1-9. Usage: python items.py <item> ; prints to stdout."""
import sys, time
import numpy as np
from scipy import integrate as sint, optimize as sopt
import kur

item = sys.argv[1]
t0 = time.time()


def se(x):
    x = np.asarray(x)
    return x.std(ddof=1) / np.sqrt(len(x)) if len(x) > 1 else float("nan")


def rep(label, m):
    print(f"{label}: mean measured r = {m.mean():.4f}  se = {se(m):.4f}  runs = {len(m)}", flush=True)


if item == "1":
    rng = np.random.default_rng(101)
    for K in (2.0, 1.5):
        m = kur.measured(kur.runs("lorentz", "regular", 2000, K, 400, 8, rng))
        rep(f"item1 Lorentzian regular N=2000 T=400 K={K} (theory sqrt(1-1/K)={np.sqrt(1-1/K):.4f})", m)

elif item == "2":
    rng = np.random.default_rng(102)
    res = {}
    for K in (1.5, 1.02, 1.05, 1.10):
        m = kur.measured(kur.runs("gauss", "regular", 2000, K, 400, 8, rng))
        res[K] = m.mean()
        rep(f"item2 Gaussian regular N=2000 T=400 K={K}", m)
    ks = np.array([1.02, 1.05, 1.10])
    sl = np.polyfit(np.log(ks - 1), np.log([res[k] for k in ks]), 1)[0]
    print(f"item2 slope log r vs log(K-1) over 1.02,1.05,1.10 = {sl:.4f}")

elif item == "3":
    rng = np.random.default_rng(103)
    for K in (0.9, 1.05):
        m = kur.measured(kur.runs("uniform", "regular", 2000, K, 400, 8, rng))
        rep(f"item3 Uniform regular N=2000 T=400 K={K}", m)

elif item == "4":
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 104
    rng = np.random.default_rng(seed)
    N = 2000
    om = kur.freqs("uniform", "regular", N, 1, rng)
    th = rng.random((1, N)) * 2 * np.pi
    up = [round(0.80 + 0.02 * i, 2) for i in range(21)]
    down = [round(1.18 - 0.02 * i, 2) for i in range(20)]
    nst = int(round(200 / kur.DT))
    ru, rd = {}, {}
    for K in up:
        th, rec = kur.integrate(om, th, K, nst)
        ru[K] = rec[0, nst // 2:].mean()
    for K in down:
        th, rec = kur.integrate(om, th, K, nst)
        rd[K] = rec[0, nst // 2:].mean()
    rd[1.20] = ru[1.20]
    print(f"item4 Uniform regular N=2000 sweep seed={seed} (up 0.80..1.20, down 1.18..0.80; 1.20 not repeated)")
    print("  K     r_up    r_down")
    for K in up:
        print(f"  {K:.2f}  {ru[K]:.4f}  {rd[K]:.4f}")
    first_up = min(k for k in up if ru[k] > 0.5)
    last_down = min(k for k in rd if rd[k] > 0.5)
    print(f"item4 first K on the way up with r>0.5: {first_up:.2f}")
    print(f"item4 last K on the way down with r>0.5 (i.e. lowest K still above 0.5): {last_down:.2f}")

elif item == "5":
    rng = np.random.default_rng(105)
    N, R = 1000, 96
    rec = kur.runs("gauss", "random", N, 0.5, 200, R, rng)
    n = rec.shape[1] - 1
    q = N * (rec[:, n // 2:] ** 2).mean(axis=1)
    print(f"item5 Gaussian random N=1000 K=0.5 T=200: N<r^2> = {q.mean():.4f}  se = {se(q):.4f}  runs = {R}")
    # same with regular frequencies as an extra
    rec = kur.runs("gauss", "regular", N, 0.5, 200, 48, rng)
    q = N * (rec[:, n // 2:] ** 2).mean(axis=1)
    print(f"item5-extra Gaussian REGULAR N=1000 K=0.5 T=200: N<r^2> = {q.mean():.4f}  se = {se(q):.4f}  runs = 48")

elif item == "6":
    kind = sys.argv[2]
    Ns = [int(x) for x in sys.argv[3].split(",")]
    Rs = [int(x) for x in sys.argv[4].split(",")]
    rng = np.random.default_rng(106 + (0 if kind == "random" else 1) + 7 * Ns[0])
    for N, R in zip(Ns, Rs):
        rec = kur.runs("gauss", kind, N, 1.0, 600, R, rng)
        m = kur.measured(rec)
        # also the mean of r in the two halves of the measuring window, to see drift
        n = rec.shape[1] - 1
        a = rec[:, n // 2: 3 * n // 4].mean(axis=1).mean()
        b = rec[:, 3 * n // 4:].mean(axis=1).mean()
        print(f"item6 Gaussian {kind} K=1 T=600 N={N}: mean measured r = {m.mean():.5f} se = {se(m):.5f} runs = {R}  [t300-450: {a:.5f}  t450-600: {b:.5f}]  ({time.time()-t0:.0f}s)", flush=True)

elif item == "7":
    rng = np.random.default_rng(107)
    for K, T in ((1.2, 200.0), (2.0, 60.0)):
        rec = kur.runs("lorentz", "regular", 2000, K, T, 40, rng)
        target = 0.85 * np.sqrt(1 - 1 / K)
        ts = []
        for row in rec:
            idx = np.nonzero(row >= target)[0]
            ts.append(idx[0] * kur.DT if len(idx) else np.inf)
        ts = np.array(ts)
        print(f"item7 Lorentzian regular N=2000 K={K}: target r = {target:.4f}; median first-reach time = {np.median(ts):.2f} "
              f"(quartiles {np.percentile(ts,25):.2f}-{np.percentile(ts,75):.2f}, min {ts.min():.2f}, max {ts.max():.2f}, runs = {len(ts)}, never reached: {np.isinf(ts).sum()})", flush=True)

elif item == "8":
    rng = np.random.default_rng(108)
    R = 6
    rec = kur.runs("gauss", "regular", 3200, 1.0, 1200, R, rng)
    t = np.arange(rec.shape[1]) * kur.DT
    np.save("/home/agent2/onset/referee/item8_rec.npy", rec[:, ::20])
    print(f"item8 Gaussian regular K=1 N=3200 T=1200, {R} runs: mean r in windows")
    for a, b in ((0, 50), (50, 100), (100, 200), (200, 300), (300, 600), (600, 1200)):
        sel = (t >= a) & (t < b) if b < 1200 else (t >= a) & (t <= b)
        w = rec[:, sel].mean(axis=1)
        print(f"  {a:5d}-{b:5d}: {w.mean():.4f}  se {se(w):.4f}   per run: " + " ".join(f"{x:.4f}" for x in w))
    pk = rec.max(axis=1); tp = t[rec.argmax(axis=1)]
    print("  peak r per run: " + " ".join(f"{x:.3f}@t={y:.0f}" for x, y in zip(pk, tp)))

elif item == "9":
    sig = kur.SIG
    g = lambda w: np.exp(-w * w / (2 * sig * sig)) / (sig * np.sqrt(2 * np.pi))

    def F(r, K):  # self-consistency residual for the locked-only contribution (symmetric unimodal g)
        val, _ = sint.quad(lambda th: np.cos(th) ** 2 * g(K * r * np.sin(th)), -np.pi / 2, np.pi / 2)
        return K * val - 1.0

    for K in (1.5, 1.02, 1.05, 1.10):
        r = sopt.brentq(F, 1e-6, 1.0, args=(K,))
        print(f"item9 Gaussian K={K}: r_inf = {r:.5f}   (leading-order sqrt(pi(K-1)) = {np.sqrt(np.pi*(K-1)):.5f})")
    # uniform on [-gam, gam]: for K>1 all locked: r = (1/(2a))*(a*sqrt(1-a^2)+asin(a)), a = gam/(K r)
    gam = np.pi / 4

    def G(r, K):
        a = gam / (K * r)
        return (a * np.sqrt(1 - a * a) + np.arcsin(a)) / (2 * a) - r

    for K in (1.0, 1.05, 1.2):
        if K == 1.0:
            print(f"item9 Uniform K=1 (onset, jump): r_c = pi/4 = {np.pi/4:.5f}")
            continue
        r = sopt.brentq(G, gam / K + 1e-12, 1.0, args=(K,))
        print(f"item9 Uniform K={K}: r_inf = {r:.5f}  (all locked; K r = {K*r:.4f} > pi/4)")
    # extra: fluctuation below onset, linear-response theory for random phases:
    # N<r^2> = int g(w) / |eps(w)|^2 dw, eps(w) = 1 - (K/2) * int_0^inf ghat(t) e^{i w t} dt
    # for the Gaussian ghat(t) = exp(-sig^2 t^2/2)
    from scipy.special import wofz
    def eps(w, K):
        # int_0^inf exp(-sig^2 t^2/2 + i w t) dt = sqrt(pi/2)/sig * wofz(w/(sig*sqrt2))
        return 1 - (K / 2) * np.sqrt(np.pi / 2) / sig * wofz(w / (sig * np.sqrt(2)))
    for K in (0.5,):
        val, _ = sint.quad(lambda w: g(w) / abs(eps(w, K)) ** 2, -12, 12, limit=400)
        print(f"item9-extra Gaussian K={K}: linear-response N<r^2> = {val:.4f}  (the Lorentzian formula 1/(1-K) would give {1/(1-K):.4f})")

print(f"# item {item} done in {time.time()-t0:.0f}s", flush=True)
