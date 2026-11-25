"""The onset of synchrony in Kuramoto's model.   usage: python onset.py TASK out.json   (TASK: check | sheet | curves | sizes-random | sizes-regular)
d theta_i/dt = omega_i + K r sin(psi - theta_i),  r e^(i psi) = mean of e^(i theta_j).  Fourth-order Runge-Kutta, step 0.05.
Frequencies: three shapes scaled so that Kc = 2/(pi g(0)) = 1; "regular" = quantiles at (i - 1/2)/N, "random" = independent draws."""
import sys, json, math, time
import numpy as np
from scipy.stats import norm
from scipy.special import ive
from scipy.optimize import brentq
from concurrent.futures import ProcessPoolExecutor

DT = 0.05

def freqs(shape, q):
    if shape == 'lorentz': return 0.5 * np.tan(np.pi * (q - 0.5))
    if shape == 'gauss': return math.sqrt(math.pi / 8) * norm.ppf(q)
    if shape == 'uniform': return (math.pi / 4) * (2 * q - 1)
    raise ValueError(shape)

def regular(shape, N, runs):
    return np.tile(freqs(shape, (np.arange(1, N + 1) - 0.5) / N), (runs, 1))

def random(shape, N, runs, rng):
    return freqs(shape, rng.random((runs, N)))

def simulate(om, K, T, rng, th=None, series=False):
    """om: runs x N.  Returns measured r (mean over the second half) and mean r^2 per run, the final phases, and r(t) if asked."""
    steps = int(round(T / DT)); half = steps // 2
    if th is None: th = rng.uniform(0, 2 * math.pi, om.shape)
    acc = np.zeros(om.shape[0]); acc2 = np.zeros(om.shape[0]); rs = [] if series else None
    def f(x):
        c, s = np.cos(x), np.sin(x); zr, zi = c.mean(1, keepdims=True), s.mean(1, keepdims=True)
        return om + K * (zi * c - zr * s), np.hypot(zr, zi)[:, 0]
    for n in range(steps):
        k1, r = f(th)
        if n >= half: acc += r; acc2 += r * r
        if series: rs.append(r.copy())
        k2, _ = f(th + 0.5 * DT * k1); k3, _ = f(th + 0.5 * DT * k2); k4, _ = f(th + DT * k3)
        th = th + (DT / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
    return acc / (steps - half), acc2 / (steps - half), th, (np.array(rs) if series else None)

# ---- theory in the limit of many oscillators
def r_theory(shape, K):
    if K <= 1: return 0.0
    if shape == 'lorentz': return math.sqrt(1 - 1 / K)
    if shape == 'gauss':                                  # 1 = K e^(-u) (I0(u) + I1(u)),  u = 2 (K r)^2 / pi
        u = brentq(lambda u: K * (ive(0, u) + ive(1, u)) - 1, 1e-12, 200); return math.sqrt(math.pi * u / 2) / K
    if shape == 'uniform':                                # every oscillator locked:  2a/K = phi + sin(phi) cos(phi),  r = a / (K sin(phi)),  a = pi/4
        a = math.pi / 4; phi = brentq(lambda p: p + math.sin(p) * math.cos(p) - 2 * a / K, 1e-9, math.pi / 2); return a / (K * math.sin(phi))

def point(args):
    shape, kind, N, runs, K, T, seed = args
    rng = np.random.default_rng(seed)
    om = regular(shape, N, runs) if kind == 'regular' else random(shape, N, runs, rng)
    r, r2, _, _ = simulate(om, K, T, rng)
    return dict(shape=shape, kind=kind, N=N, runs=runs, K=K, T=T, r=float(r.mean()), sd=float(r.std(ddof=1)) if runs > 1 else 0.0, r2=float(r2.mean()), each=[float(x) for x in r])

def sweep(seed):
    rng = np.random.default_rng(seed); om = regular('uniform', 2000, 1); th = None; out = []
    ks = [round(0.80 + 0.02 * i, 2) for i in range(21)]
    for leg, K in [('up', k) for k in ks] + [('down', k) for k in ks[-2::-1]]:
        r, _, th, _ = simulate(om, K, 200, rng, th=th); out.append(dict(leg=leg, K=K, r=float(r[0])))
    return out

def rise(args):
    K, seed = args
    rng = np.random.default_rng(seed); om = regular('lorentz', 2000, 20)
    _, _, _, rs = simulate(om, K, 300, rng, series=True); target = 0.85 * r_theory('lorentz', K)
    t = [float(np.argmax(rs[:, j] >= target) * DT) if (rs[:, j] >= target).any() else None for j in range(rs.shape[1])]
    return dict(K=K, target=target, times=t, mean_curve=[float(x) for x in rs.mean(1)[::20]])

SIZES = [(100, 200), (200, 150), (400, 100), (800, 60), (1600, 40), (3200, 24), (6400, 12), (12800, 8)]

if __name__ == '__main__':
    task, out = sys.argv[1], sys.argv[2]; t0 = time.time(); res = {}
    with ProcessPoolExecutor(max_workers=8) as ex:
        if task == 'check':                               # K = 0: N times the mean of r^2 is 1 whatever the frequencies
            p = point(('gauss', 'random', 1000, 200, 0.0, 40, 1)); res['check'] = p; print(f"K = 0, N = 1000, 200 runs: N x mean r^2 = {1000 * p['r2']:.3f} (exactly 1 in expectation)")
            print("theory: Lorentzian r(2) = %.4f, r(1.5) = %.4f; Gaussian and uniform values are not printed before the forecasts are in" % (r_theory('lorentz', 2), r_theory('lorentz', 1.5)))
        if task == 'sheet':
            jobs = [('lorentz', 'regular', 2000, 10, 2.0, 400, 11), ('lorentz', 'regular', 2000, 10, 1.5, 400, 12), ('gauss', 'regular', 2000, 10, 1.5, 400, 13),
                    ('uniform', 'regular', 2000, 10, 0.9, 400, 14), ('uniform', 'regular', 2000, 10, 1.05, 400, 15), ('gauss', 'random', 1000, 100, 0.5, 200, 16),
                    ('gauss', 'regular', 2000, 10, 1.02, 400, 17), ('gauss', 'regular', 2000, 10, 1.05, 400, 18), ('gauss', 'regular', 2000, 10, 1.10, 400, 19)]
            fs = ex.submit(sweep, 21); fr = [ex.submit(rise, (K, s)) for K, s in ((1.2, 31), (2.0, 32))]
            res['points'] = list(ex.map(point, jobs)); res['sweep'] = fs.result(); res['rise'] = [f.result() for f in fr]
        if task == 'curves':
            ks = [round(0.5 + 0.05 * i, 2) for i in range(41)]
            jobs = [(sh, 'regular', 2000, 4, K, 400, 1000 + 50 * a + i) for a, sh in enumerate(('lorentz', 'gauss', 'uniform')) for i, K in enumerate(ks)]
            res['curves'] = list(ex.map(point, jobs)); res['theory'] = {sh: [[K, r_theory(sh, K)] for K in [round(0.5 + 0.005 * i, 3) for i in range(401)]] for sh in ('lorentz', 'gauss', 'uniform')}
        if task in ('sizes-random', 'sizes-regular'):
            kind = task.split('-')[1]
            jobs = [('gauss', kind, N, runs, 1.0, 600, 2000 + i + (100 if kind == 'regular' else 0)) for i, (N, runs) in enumerate(SIZES)]
            res['sizes'] = list(ex.map(point, jobs[::-1]))[::-1]
    res['seconds'] = time.time() - t0
    json.dump(res, open(out, 'w'))
    print(f"{task}: {res['seconds']:.0f} s")
