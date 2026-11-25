# The model Moon's own rotation (LFIG=3): its rotation angle minus the mean longitude formula = the physical libration in longitude.
# usage: libration.py lib_file
import sys, numpy as np
AS = 206264.806247
a = np.loadtxt(sys.argv[1]); t = a[:, 0]; T = t / 36525.0
Lm = np.radians(218.3164477 + 481266.48434638 * T - 0.00188567 * T ** 2)           # Moon's mean longitude, J2000 ecliptic (Meeus/ELP, precession removed)
tau = (a[:, 1] - Lm + np.pi) % (2 * np.pi) - np.pi; tau = np.unwrap(tau) * AS
opt = ((a[:, 3] - a[:, 1] + np.pi / 2) % np.pi - np.pi / 2) * AS                    # Earth's direction minus the long axis (mod half a turn): the optical libration
print(f'{len(t)} samples over {t[0] / 365.25:.1f} to {t[-1] / 365.25:.1f} yr; rotation angle minus mean longitude: mean {tau.mean():+.1f}", standard deviation {tau.std():.1f}", extremes {tau.min():+.1f} to {tau.max():+.1f}"')
print(f'Earth line minus long axis: standard deviation {opt.std() / 3600:.2f} deg, extremes {opt.min() / 3600:+.2f} to {opt.max() / 3600:+.2f} deg   (real Moon: optical libration in longitude up to about 7.9 deg)')
per = {'annual (365.26 d)': 365.2596, 'anomalistic month (27.555 d)': 27.554550, 'free libration (fitted period)': None, '206-day (2D-2l)': 205.89, 'half-year (182.6 d)': 182.63, 'synodic half-month (14.77 d)': 14.7653, '1.09 yr (411.8 d)': 411.78, '3 yr': 1095.2, '6 yr (2F-2l)': 2190.3}
def design(pf):
    cols = [np.ones_like(t), t]
    for k, p in per.items():
        p = pf if p is None else p; cols += [np.cos(2 * np.pi * t / p), np.sin(2 * np.pi * t / p)]
    return np.vstack(cols).T
best = None
for pf in np.arange(900, 1200, 2.0):
    A = design(pf); c, res, *_ = np.linalg.lstsq(A, tau, rcond=None); r = ((tau - A @ c) ** 2).sum()
    if best is None or r < best[0]: best = (r, pf, c)
r, pf, c = best; print(f'least squares: constant {c[0]:+.2f}", drift {c[1] * 36525:+.2f}" per century; best free period {pf:.0f} d ({pf / 365.25:.2f} yr; theory 2 pi/(n sqrt(3 gamma)) = 2.86 yr); residual rms {np.sqrt(r / len(t)):.2f}"')
for i, k in enumerate(per): print(f'   {k:32s} amplitude {np.hypot(c[2 + 2 * i], c[3 + 2 * i]):7.2f}"')
