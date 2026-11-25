# Choose the Moon's initial rotation angle and rate (LFIG=3) so that its free libration is not excited: run 60 years, fit the free term, remove it from the start, repeat.
import subprocess, os, numpy as np
AS = 206264.806247
th0, om0 = 218.322019991, 481313.22535902         # deg, deg/cy: after three rounds started from the mean longitude 218.3164477 and sidereal mean motion 481266.48434638 (lib_ic.out, first part)
FORCED = [365.2596, 27.554550, 205.89, 1095.18, 182.63, 411.78, 31.812, 14.7653, 173.31, 6798.4, 3232.6]   # 1095.18 d = 2F-2l, a forced term 39 days from the free period
def run(th0, om0):
    env = dict(os.environ, J2='1', TIDE='195', LFIG='3', LIBOUT='/tmp/lib_ic.txt', TH0='%.12f' % th0, OM0='%.9f' % om0)
    subprocess.run(['./orrery_lfig3', 'data/ic.txt', '120', '0.05', '2', '2', 'state'], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    a = np.loadtxt('/tmp/lib_ic.txt'); t = a[:, 0]; T = t / 36525
    tau = np.unwrap((a[:, 1] - np.radians(218.3164477 + 481266.48434638 * T - 0.00188567 * T ** 2) + np.pi) % (2 * np.pi) - np.pi) * AS
    best = None
    for pf in [1056.5]:                                # free period, measured in the first round when the free term was 771 arcsec
        cols = [np.ones_like(t), t, t * t, np.cos(2 * np.pi * t / pf), np.sin(2 * np.pi * t / pf)]
        for p in FORCED: cols += [np.cos(2 * np.pi * t / p), np.sin(2 * np.pi * t / p)]
        A = np.vstack(cols).T; c = np.linalg.lstsq(A, tau, rcond=None)[0]; r = ((tau - A @ c) ** 2).sum()
        if best is None or r < best[0]: best = (r, pf, c)
    return best, len(t)
for it in range(4):
    (r, pf, c), n = run(th0, om0); amp = np.hypot(c[3], c[4])
    print(f'iteration {it}: TH0 = {th0:.9f} deg, OM0 = {om0:.8f} deg/cy -> free libration: period {pf:.1f} d, amplitude {amp:.2f}";  annual {np.hypot(c[5], c[6]):.2f}", monthly {np.hypot(c[7], c[8]):.2f}", 206-day {np.hypot(c[9], c[10]):.2f}", 2F-2l (1095 d) {np.hypot(c[11], c[12]):.2f}";  drift {c[1] * 36525:+.2f}"/cy, residual rms {np.sqrt(r / n):.2f}"', flush=True)
    if amp < 1.0: break
    th0 -= c[3] / 3600.0                                              # free term at t = 0: c3 (arcsec)
    om0 -= (c[4] * 2 * np.pi / pf) * 36525 / 3600.0                   # its rate at t = 0: c4 * 2 pi / P (arcsec/day) -> deg/cy
print('FINAL TH0=%.12f OM0=%.9f' % (th0, om0))
