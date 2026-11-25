# How the Earth's oblateness's effect on the Moon changes with time in my own model, from two runs sampled every 10 days throughout.
# (scaled - base)/0.1 in mean longitude, perigee and node; smoothed over the node's period (and the perigee's), then fitted a T + b T^2 + c T^3.
# usage: j2_time_cont.py base scaled
import sys, numpy as np
AU = 149597870.7; MU = (398600.435507 + 4902.800118) * 86400.0 ** 2 / AU ** 3; AS = 206264.806247
def load(p):
    a = np.loadtxt(p); E = a[a[:, 1] == 3]; M = a[a[:, 1] == 4]; n = min(len(E), len(M)); return E[:n, 0], M[:n, 2:] - E[:n, 2:]
def elements(x):
    r, v = x[:, :3], x[:, 3:]; h = np.cross(r, v); rr = np.linalg.norm(r, axis=1); v2 = (v * v).sum(1); rv = (r * v).sum(1)
    e = ((v2 - MU / rr)[:, None] * r - rv[:, None] * v) / MU; ecc = np.linalg.norm(e, axis=1); Om = np.arctan2(h[:, 0], -h[:, 1])
    n = np.stack([np.cos(Om), np.sin(Om), 0 * Om], 1); m = np.cross(h / np.linalg.norm(h, axis=1)[:, None], n)
    w = np.arctan2((e * m).sum(1), (e * n).sum(1)); f = np.arctan2((r * m).sum(1), (r * n).sum(1)) - w
    E = 2 * np.arctan2(np.sqrt(1 - ecc) * np.sin(f / 2), np.sqrt(1 + ecc) * np.cos(f / 2)); return Om, Om + w, Om + w + E - ecc * np.sin(E)
def box(x, m): c = np.cumsum(np.insert(x, 0, 0.0)); return (c[m:] - c[:-m]) / m
ja, xa = load(sys.argv[1]); jb, xb = load(sys.argv[2]); n = min(len(ja), len(jb)); assert np.allclose(ja[:n], jb[:n]); T = -(ja[:n] - 2451545.0) / 36525
def of_date(x, t):
    """rotate positions and velocities into axes whose z is the pole of the ecliptic OF DATE (IAU 2006 P_A, Q_A; t in centuries from J2000, negative for the past), by the smallest turn"""
    P = (4.199094 * t + 0.1939873 * t ** 2 - 0.00022466 * t ** 3) / AS; Q = (-46.811015 * t + 0.0510283 * t ** 2 + 0.00052413 * t ** 3) / AS
    k = np.stack([P, -Q, np.sqrt(1 - P * P - Q * Q)], 1); z = np.array([0, 0, 1.0]); ax = np.cross(k, z); s_ = np.linalg.norm(ax, axis=1); c_ = k[:, 2]
    out = np.empty_like(x)
    for j in (0, 3):
        v = x[:, j:j + 3]; u = ax / np.where(s_ > 0, s_, 1)[:, None]          # Rodrigues: turn by the angle that takes k to z, about k x z
        out[:, j:j + 3] = v * c_[:, None] + np.cross(u, v) * s_[:, None] + u * (u * v).sum(1)[:, None] * (1 - c_)[:, None]
    return out
FRAME = sys.argv[3] if len(sys.argv) > 3 else 'j2000'
if FRAME == 'date': xa, xb = of_date(xa[:n], -T), of_date(xb[:n], -T); print('elements referred to the ecliptic OF DATE')
A, B = elements(xa[:n]), elements(xb[:n])
print(f'{n} samples, every {abs(ja[1] - ja[0]):.0f} days, back to T = {T.max():.2f} centuries')
print('(oblateness x 1.1) - (x 1), divided by 0.1; smoothed by two passes over the node period (6798 d) and one over the perigee period (3233 d); fit a T + b T^2 + c T^3 for 0.5 < T < 19.5')
out = {}
for name, i in (('mean longitude', 2), ('perigee', 1), ('node', 0)):
    d = np.unwrap(B[i] - A[i]) * AS / 0.1; raw_sd = None
    y, t = d, T
    for m in (680, 680, 323): y = box(y, m); t = box(t, m)
    mk = (t > 0.5) & (t < 19.5); X = np.vstack([t[mk], t[mk] ** 2, t[mk] ** 3]).T; c = np.linalg.lstsq(X, y[mk], rcond=None)[0]; res = y[mk] - X @ c
    X2 = X[:, :2]; c2 = np.linalg.lstsq(X2, y[mk], rcond=None)[0]; res2 = y[mk] - X2 @ c2
    # crude error: split the span into halves in alternate 2-century blocks
    blk = (np.floor(t[mk] / 2) % 2 == 0); ca = np.linalg.lstsq(X[blk], y[mk][blk], rcond=None)[0]; cb = np.linalg.lstsq(X[~blk], y[mk][~blk], rcond=None)[0]
    out[name] = c
    print(f'   {name:15s} a = {c[0]:+9.3f}"/cy   b/a = {c[1] / c[0]:+.3e}   c/a = {c[2] / c[0]:+.3e}   rms about the fit {res.std():.3f}"   (alternate blocks: b/a {ca[1] / ca[0]:+.2e}, {cb[1] / cb[0]:+.2e}; c/a {ca[2] / ca[0]:+.2e}, {cb[2] / cb[0]:+.2e})   [no cube: b/a {c2[1] / c2[0]:+.3e}, rms {res2.std():.3f}"]')
print('strength of the oblateness\'s effect as a function of time, F(T) = 1 + 2(b/a) T + 3(c/a) T^2:')
for name, c in out.items(): print(f'   {name:15s} F = 1 {2 * c[1] / c[0]:+.2e} T {3 * c[2] / c[0]:+.2e} T^2      -> at T = 20: {1 + 2 * c[1] / c[0] * 20 + 3 * c[2] / c[0] * 400:.5f}')
print('the simple theory (pull in proportion to 1 - 1.5 sin^2 of the tilt of date): F = 1 - 3.26e-4 T;   the drift against JPL, read as a change in the pull: +8.8e-6 T^2 on top of mine')
# ---- a look at the shape: the smoothed contribution divided by T (arcsec per century back), every two centuries
print('\nsmoothed contribution / T, at T = 1, 3, ... 19:')
for name, i in (('mean longitude', 2), ('perigee', 1), ('node', 0)):
    d = np.unwrap(B[i] - A[i]) * AS / 0.1; y, t = d, T
    for m in (680, 680, 323): y = box(y, m); t = box(t, m)
    print(f'   {name:15s} ' + ' '.join(f'{np.interp(Tq, t, y) / Tq:+9.2f}' for Tq in range(1, 20, 2)))
# ---- the fits above have no constant term, and they need one: the two runs start together, so each swing the oblateness gives an angle leaves a constant behind (its value at the start).
print('\nrefit WITH a constant: c0 + a T + b T^2 + c T^3 (0.5 < T < 19.5), smoothed series:')
for name, i in (('mean longitude', 2), ('perigee', 1), ('node', 0)):
    d = np.unwrap(B[i] - A[i]) * AS / 0.1; y, t = d, T
    for m in (680, 680, 323): y = box(y, m); t = box(t, m)
    mk = (t > 0.5) & (t < 19.5)
    for powers in ((0, 1, 2), (0, 1, 2, 3)):
        X = np.vstack([t[mk] ** p for p in powers]).T; c = np.linalg.lstsq(X, y[mk], rcond=None)[0]; res = y[mk] - X @ c
        blk = (np.floor(t[mk] / 2) % 2 == 0); ca = np.linalg.lstsq(X[blk], y[mk][blk], rcond=None)[0]; cb = np.linalg.lstsq(X[~blk], y[mk][~blk], rcond=None)[0]
        txt = f'c0 = {c[0]:+8.2f}"  a = {c[1]:+9.3f}"/cy  b/a = {c[2] / c[1]:+.3e} (blocks {ca[2] / ca[1]:+.2e}, {cb[2] / cb[1]:+.2e})'
        if len(powers) == 4: txt += f'  c/a = {c[3] / c[1]:+.3e} (blocks {ca[3] / ca[1]:+.2e}, {cb[3] / cb[1]:+.2e})'
        print(f'   {name:15s} {txt}   rms {res.std():.3f}"')
print('theory: b/a = -1.63e-4 (strength falling 3.26e-4 per century back), c/a = 0;  the anomaly against JPL would be |c/a| = 2.9e-6')
