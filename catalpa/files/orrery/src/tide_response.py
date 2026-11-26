# How do my Moon's perigee and node answer to a change in the tidal braking alone?  Two runs of my model that differ only in the tidal lag (TIDE=185 against 195 s), in the same nineteen
# century windows as moon_vs_de431.py; the difference of their mean elements, fitted with c + a T + b T^2 (T in centuries back from 2000).  If the T^2 terms of perigee and node stand to the
# T^2 term of the mean longitude as they do in (my run - DE431), the remainder there is my tidal constant.     usage: python3 -I tide_response.py <run A> <run B>
import sys, os, numpy as np; HERE = os.path.dirname(os.path.abspath(__file__))
AU = 149597870.7; MU = (398600.435507 + 4902.800118) * 86400.0 ** 2 / AU ** 3; AS = 206264.806247
STARTS = [int(x) for x in open(HERE + '/../cen_starts.txt').read().split()]
def elements(r, v):
    h = np.cross(r, v); rr = np.linalg.norm(r, axis=1); v2 = (v * v).sum(1); rv = (r * v).sum(1)
    e = ((v2 - MU / rr)[:, None] * r - rv[:, None] * v) / MU; ecc = np.linalg.norm(e, axis=1); a = 1 / (2 / rr - v2 / MU); inc = np.arccos(h[:, 2] / np.linalg.norm(h, axis=1)); Om = np.arctan2(h[:, 0], -h[:, 1])
    n = np.stack([np.cos(Om), np.sin(Om), 0 * Om], 1); m = np.cross(h / np.linalg.norm(h, axis=1)[:, None], n)
    w = np.arctan2((e * m).sum(1), (e * n).sum(1)); f = np.arctan2((r * m).sum(1), (r * n).sum(1)) - w
    Ean = 2 * np.arctan2(np.sqrt(1 - ecc) * np.sin(f / 2), np.sqrt(1 + ecc) * np.cos(f / 2)); return a, ecc, inc, Om, Om + w, Om + w + Ean - ecc * np.sin(Ean)
wrap = lambda x: (x + np.pi) % (2 * np.pi) - np.pi
def mine(fn):
    E, M = {}, {}
    with open(fn) as f:
        for line in f:
            p = line.split()
            if len(p) < 8: continue
            if p[1] == '3': E[p[0]] = [float(x) for x in p[2:]]
            elif p[1] == '4': M[p[0]] = [float(x) for x in p[2:]]
    return E, M
A, B = mine(sys.argv[1]), mine(sys.argv[2]); T = []; rows = []
for d in STARTS:
    keys = [f'{2451545.0 + d + i:.2f}' for i in range(413)]; keys = [k for k in keys if all(k in X for X in (A[0], A[1], B[0], B[1]))]      # the windows are given in days from J2000, the runs print Julian days
    if len(keys) < 400: print(f'window starting day {d}: only {len(keys)} days in both runs; left out'); continue
    ea, eb = [elements(*(lambda s: (s[:, :3], s[:, 3:]))(np.array([R[1][k] for k in keys]) - np.array([R[0][k] for k in keys]))) for R in (A, B)]
    T.append(-(np.mean([float(k) for k in keys]) - 2451545.0) / 36525); rows.append([(wrap(ea[k] - eb[k]) * AS).mean() for k in (5, 4, 3)] + [((ea[2] - eb[2]) * AS).mean(), ((ea[0] - eb[0]) / eb[0]).mean()])
T = np.array(T); R = np.array(rows)
def fit(y, powers):
    M = np.vstack([T ** p for p in powers]).T; c, res, rk, sv = np.linalg.lstsq(M, y, rcond=None); r = y - M @ c; s2 = (r ** 2).sum() / max(1, len(y) - len(powers)); cov = s2 * np.linalg.inv(M.T @ M)
    return c, np.sqrt((r ** 2).mean()), np.sqrt(np.diag(cov))
print(f'{os.path.basename(sys.argv[1])} - {os.path.basename(sys.argv[2])}: {len(T)} windows (arcsec; T in centuries back from 2000)')
print('   T:             ' + ' '.join(f'{t:7.2f}' for t in T)); out = {}
for k, lab in enumerate(('mean longitude', 'perigee', 'node', 'inclination')):
    y = R[:, k]; print(f'   {lab:14s} ' + ' '.join(f'{x:+7.2f}' for x in y))
    if lab == 'inclination': continue
    c, rms, se = fit(y, (0, 1, 2)); c3, rms3, se3 = fit(y, (0, 1, 2, 3)); out[lab] = (c[2], se[2], c3[2], se3[2])
    print(f'        c + a T + b T^2:  b = {c[2]:+.5f} +- {se[2]:.5f}  (a = {c[1]:+.4f}, c = {c[0]:+.3f}; rms {rms:.3f})     with T^3 as well:  T^2 {c3[2]:+.5f} +- {se3[2]:.5f}, T^3 {c3[3]:+.6f} (rms {rms3:.3f})')
print('   semi-major axis, relative difference x 1e9: ' + ' '.join(f'{1e9 * x:+7.2f}' for x in R[:, 4]))
# sturdier forms of the same ratios (the scatter of these differences grows as the square of the time, so a fit with a free constant and slope leans on the last windows): the checking reader's point
def wfit(y):
    M = np.vstack([T ** p for p in (0, 1, 2)]).T; w = 1 / T ** 2; c = np.linalg.lstsq(M * w[:, None], y * w, rcond=None)[0]; return c[2]
pure = lambda y: (y * T ** 2).sum() / (T ** 4).sum()
print('   The two ratios by other forms of fit:')
for k, lab in ((1, 'perigee'), (2, 'node')):
    wr = R[:, k] / R[:, 0]
    print(f'      {lab:8s} weighted for scatter growing as T^2: {wfit(R[:, k]) / wfit(R[:, 0]):+.5f};   pure squares (no constant, no slope): {pure(R[:, k]) / pure(R[:, 0]):+.5f};   mean of the {len(T)} window ratios: {wr.mean():+.5f} (sd {wr.std():.5f})')
print(f"   My model's tidal acceleration by proportion (the braking is proportional to the constant, 195 s; 10 s of it give {out['mean longitude'][0]:+.5f} T^2, half the change of acceleration): {2 * out['mean longitude'][0] * 195 / 10:.2f} arcsec per century squared")
L = out['mean longitude']
for lab in ('perigee', 'node'):
    o = out[lab]; print(f'   T^2 of the {lab} over T^2 of the mean longitude: {o[0] / L[0]:+.5f} +- {abs(o[1] / L[0]):.5f}   (with cubes fitted too: {o[2] / L[2]:+.5f} +- {abs(o[3] / L[2]):.5f})')
print('   On paper (the series in m = n\'/n = 0.0748013 for the rates of perigee and node, differentiated by n): perigee', end=' ')
m = 0.0748013; cp = [(2, 3 / 4), (3, 225 / 32), (4, 4071 / 128), (5, 265493 / 2048), (6, 12822631 / 24576), (7, 1273925965 / 589824)]; cn = [(2, -3 / 4), (3, 9 / 32), (4, 273 / 128), (5, 9797 / 2048)]
print(f"{sum(c * (1 - k) * m ** k for k, c in cp):+.5f} (the series itself gives the rate {sum(c * m ** k for k, c in cp):.6f} n, the true value being 0.008452 n);  node {sum(c * (1 - k) * m ** k for k, c in cn):+.5f} (rate {sum(c * m ** k for k, c in cn):.6f} n, true -0.004022 n)")
