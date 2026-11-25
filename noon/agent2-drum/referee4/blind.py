import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from rsolve import Drum, slp, exact_miss, MODES, TARG
from scipy.optimize import minimize


def polish(dr, a, M, mono, maxiter=200):
    K = dr.K; w = dr.w
    cache = {}
    def ev(x):
        key = x[:K].tobytes()
        if key not in cache:
            cache.clear()
            cache[key] = dr.miss(np.clip(x[:K], 0, None) / w, True)
        return cache[key]
    S = 100.0  # t scaled
    def c1(x):
        mis, J = ev(x); return np.concatenate([x[K] / S - mis, x[K] / S + mis, [M - x[:K].sum()]])
    def j1(x):
        mis, J = ev(x); J = J / w
        top = np.hstack([-J, np.full((8, 1), 1 / S)]); bot = np.hstack([J, np.full((8, 1), 1 / S)])
        return np.vstack([top, bot, np.hstack([-np.ones(K), [0.0]])])
    cons = [dict(type='ineq', fun=c1, jac=j1)]
    if mono:
        Mm = np.zeros((K - 1, K + 1))
        for j in range(K - 1):
            Mm[j, j] = 1 / w[j]; Mm[j, j + 1] = -1 / w[j + 1]
        cons.append(dict(type='ineq', fun=lambda x: Mm @ x, jac=lambda x: Mm))
    b = a * w
    f0 = np.abs(dr.miss(a)).max()
    x0 = np.concatenate([b, [f0 * S]])
    res = minimize(lambda x: x[K], x0, jac=lambda x: np.eye(K + 1)[K], bounds=[(0, None)] * (K + 1), constraints=cons,
                   method='SLSQP', options=dict(maxiter=maxiter, ftol=1e-12))
    bn = np.clip(res.x[:K], 0, None)
    if mono:
        bn = np.minimum.accumulate(bn / w) * w
    if bn.sum() > M:
        bn *= M / bn.sum()
    fn = np.abs(dr.miss(bn / w)).max()
    return (bn / w, fn) if fn < f0 else (a, f0)

M = float(sys.argv[1])
mono = sys.argv[2] == 'mono'
K = int(sys.argv[3])
tlim = float(sys.argv[4])
tag = sys.argv[5]
seed = int(sys.argv[6]) if len(sys.argv) > 6 else 0
rng = np.random.default_rng(seed)
edges = np.linspace(0, 1, K + 1)
dr = Drum(edges, cells=max(4, 400 // K))
w = dr.w
t0 = time.time()

# sanity: bare skin against Bessel zeros
if seed == 0:
    from scipy.special import jn_zeros
    ex = exact_miss(edges, np.zeros(K))
    z = [jn_zeros(m, n)[-1] for m, n in MODES]
    print('bare check: exact', np.round([ex[3][k] for k in MODES], 6), 'zeros', np.round(z, 6), flush=True)

starts = []
mid = 0.5 * (edges[1:] + edges[:-1])
for R in (0.25, 0.35, 0.45, 0.55, 0.7, 1.0):
    for frac in (1.0, 0.4):
        a = np.where(mid < R, 1.0, 0.0)
        a *= frac * M / (a * w).sum()
        starts.append(('disc R=%.2f frac=%.1f' % (R, frac), a))
if not mono:
    for (r1, r2) in ((0.3, 0.6), (0.5, 0.8), (0.2, 0.5), (0.6, 1.0)):
        a = np.where((mid > r1) & (mid < r2), 1.0, 0.0)
        a *= M / (a * w).sum()
        starts.append(('ring %.1f-%.1f' % (r1, r2), a))
if len(sys.argv) > 7:
    extra = json.load(open(sys.argv[7]))
    starts = [('given %d' % i, np.repeat(np.array(x), K // len(x))) for i, x in enumerate(extra)] + starts
best = (9, None, None)
results = []
i = 0
while time.time() - t0 < tlim:
    if i < len(starts):
        name, a0 = starts[i]
    else:
        name = 'random %d' % i
        b = rng.dirichlet(np.full(K, rng.choice([0.2, 0.5, 1.0]))) * M * rng.uniform(0.3, 1)
        a0 = b / w
        if mono:
            a0 = np.sort(a0)[::-1]
            a0 *= min(1, M / (a0 * w).sum())
    i += 1
    a, f1 = slp(dr, a0 * w, M, mono=mono, maxit=150, tlim=tlim, t0=t0)
    a, f2 = polish(dr, a, M, mono)
    a, f = slp(dr, a * w, M, mono=mono, maxit=150, tlim=tlim, t0=t0)
    name += ' (slp %.5f slsqp %.5f)' % (f1, f2)
    results.append((f, name))
    print('%-50s miss %.6f mass %.4f' % (name, f, (a * w).sum()), flush=True)
    if f < best[0]:
        best = (f, a, name)
f, a, name = best
drf = Drum(edges, cells=40)
for _ in range(3):
    a, f = polish(drf, a, M, mono, maxiter=150)
    a, f = slp(drf, a * w, M, mono=mono, maxit=60)
em, r, fvm, _ = exact_miss(edges, a)
out = dict(tag=tag, M=M, mono=mono, K=K, miss_fv=f, miss_exact=em, mass=float((a * w).sum()), a=list(map(float, a)),
           ratios=list(map(float, r)), start=name, nstarts=i, all=sorted([(float(x), n) for x, n in results])[:12])
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), ('blind_%s.json' if tag in ('f143','f12','m12') else 'ctrl_%s.json') % tag), 'w'))
print('BEST', tag, 'fv', f, 'exact', em, 'mass', (a * w).sum(), 'from', name)
print('a per ring:', np.round(a, 3))
print('ratios:', np.round(r, 5))
