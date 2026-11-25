# How the Earth's oblateness's effect on the Moon changes with time in my own model: (run with J2 x 1.1) - (run with J2), century by century.
# usage: j2_time.py base_states scaled_states
import sys, numpy as np
AU = 149597870.7; MU = (398600.435507 + 4902.800118) * 86400.0 ** 2 / AU ** 3; AS = 206264.806247
def load(p):
    E, M = {}, {}
    for line in open(p):
        w = line.split()
        if w[1] == '3': E[w[0]] = [float(x) for x in w[2:]]
        elif w[1] == '4': M[w[0]] = [float(x) for x in w[2:]]
    return E, M
def elements(x):
    r, v = x[:, :3], x[:, 3:]; h = np.cross(r, v); rr = np.linalg.norm(r, axis=1); v2 = (v * v).sum(1); rv = (r * v).sum(1)
    e = ((v2 - MU / rr)[:, None] * r - rv[:, None] * v) / MU; ecc = np.linalg.norm(e, axis=1); Om = np.arctan2(h[:, 0], -h[:, 1])
    n = np.stack([np.cos(Om), np.sin(Om), 0 * Om], 1); m = np.cross(h / np.linalg.norm(h, axis=1)[:, None], n)
    w = np.arctan2((e * m).sum(1), (e * n).sum(1)); f = np.arctan2((r * m).sum(1), (r * n).sum(1)) - w
    E = 2 * np.arctan2(np.sqrt(1 - ecc) * np.sin(f / 2), np.sqrt(1 + ecc) * np.cos(f / 2)); return Om, Om + w, Om + w + E - ecc * np.sin(E)
wrap = lambda x: (x + np.pi) % (2 * np.pi) - np.pi
Ea, Ma = load(sys.argv[1]); Eb, Mb = load(sys.argv[2]); keys = sorted(set(Ea) & set(Eb), key=float); jd = np.array([float(k) for k in keys])
xa = np.array([Ma[k] for k in keys]) - np.array([Ea[k] for k in keys]); xb = np.array([Mb[k] for k in keys]) - np.array([Eb[k] for k in keys])
A, B = elements(xa), elements(xb); T = -(jd - 2451545.0) / 36525
edges = np.where(np.abs(np.diff(jd)) > 100)[0]; st = np.r_[0, edges + 1]; en = np.r_[edges + 1, len(jd)]
rows = []
for s, e in zip(st, en):
    if e - s < 400: continue
    rows.append([T[s:e].mean()] + [(wrap(B[i][s:e] - A[i][s:e]) * AS).mean() / 0.1 for i in (2, 1, 0)])
R = np.array(rows); Tm = R[:, 0]
print('(run with the oblateness x 1.1) - (run with it x 1), divided by 0.1: what the whole oblateness contributes, arcsec, T centuries back; 412-day means')
print('   T      mean longitude    perigee       node')
for r in R: print(f'  {r[0]:5.2f}   {r[1]:+11.2f}   {r[2]:+10.2f}   {r[3]:+10.2f}')
X = np.vstack([Tm, Tm ** 2, Tm ** 3]).T
print('fits a T + b T^2 + c T^3:')
for name, col in (('mean longitude', 1), ('perigee', 2), ('node', 3)):
    c = np.linalg.lstsq(X, R[:, col], rcond=None)[0]; res = R[:, col] - X @ c
    c2 = np.linalg.lstsq(X[:, :2], R[:, col], rcond=None)[0]; res2 = R[:, col] - X[:, :2] @ c2
    print(f'   {name:15s} a = {c[0]:+9.3f}   b/a = {c[1] / c[0]:+.3e}   c/a = {c[2] / c[0]:+.3e}   rms {res.std():.3f}"      (without the cube: b/a = {c2[1] / c2[0]:+.3e}, rms {res2.std():.3f}")')
print('theory for a pull in proportion to 1 - 1.5 sin^2(tilt of date): b/a = -1.63e-4, c/a = 0;   the drift against JPL, read as a change in the pull, would be c/a = 2.9e-6 in size')
# ---- added after the first look: the oblateness also gives each angle a swing in step with the Moon's node (18.6 yr), which one sample per century catches at a random phase.
# Refit with that swing in the model: a T + b T^2 + c T^3 + p cos(node) + q sin(node) + r cos(2 node) + s sin(2 node), node = the base run's mean node in the window.
print('\nrefit with a swing in step with the node (and its double) added:')
nodes = np.array([np.angle(np.exp(1j * A[0][s:e]).mean()) for s, e in zip(st, en) if e - s >= 400])
X2 = np.vstack([Tm, Tm ** 2, Tm ** 3, np.cos(nodes), np.sin(nodes), np.cos(2 * nodes), np.sin(2 * nodes)]).T
for name, col in (('mean longitude', 1), ('perigee', 2), ('node', 3)):
    c, *_ = np.linalg.lstsq(X2, R[:, col], rcond=None); res = R[:, col] - X2 @ c
    cov = np.linalg.inv(X2.T @ X2) * res.var() * len(Tm) / (len(Tm) - X2.shape[1]); sd = np.sqrt(np.diag(cov))
    print(f'   {name:15s} a = {c[0]:+9.3f}   b/a = {c[1] / c[0]:+.2e} (+-{abs(sd[1] / c[0]):.1e})   c/a = {c[2] / c[0]:+.2e} (+-{abs(sd[2] / c[0]):.1e})   swing {np.hypot(c[3], c[4]):.1f}", double {np.hypot(c[5], c[6]):.1f}"   rms {res.std():.3f}"')
