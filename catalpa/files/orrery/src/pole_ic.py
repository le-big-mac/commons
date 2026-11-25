# The Earth's pole as a variable of the integration (POLE=1): tune H to the observed precession rate and the starting pole so that the MEAN pole at J2000 is the standard one.
import subprocess, os, numpy as np
AS = 206264.806247; EPS0 = 23.4392911 * 3600; RATE = 5038.481507          # arcsec; arcsec per century (IAU 2006 psi_A, relative to the fixed J2000 ecliptic)
H, dpsi0, deps0 = 0.0032737949, 0.0, 0.0
PER = [6798.38, 3399.19, 182.621, 365.2596, 13.6608, 27.5545, 121.75, 9.133, 31.812, 1305.48, 1095.18, 177.84, 205.89]
def run(H, dpsi0, deps0, years=100):
    env = dict(os.environ, J2='1', TIDE='195', LFIG='3', POLE='1', HDYN='%.12g' % H, DPSI0='%.6f' % dpsi0, DEPS0='%.6f' % deps0, LIBOUT='/tmp/claude-1004/pole_ic.txt')
    subprocess.run(['./orrery_pole', 'data/ic.txt', str(years), '0.05', '2', '1', 'state'], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    a = np.loadtxt('/tmp/claude-1004/pole_ic.txt'); t = a[:, 0]; p = a[:, 4:7]; p /= np.linalg.norm(p, axis=1)[:, None]
    eps = np.arccos(p[:, 2]) * AS; psi = (np.pi / 2 - np.unwrap(np.arctan2(p[:, 1], p[:, 0]))) * AS; T = t / 36525
    cols = [np.ones_like(T), T, T * T]
    for P in PER: cols += [np.cos(2 * np.pi * t / P), np.sin(2 * np.pi * t / P)]
    A = np.vstack(cols).T; ce = np.linalg.lstsq(A, eps, rcond=None)[0]; cp = np.linalg.lstsq(A, psi, rcond=None)[0]
    amp = lambda c, i: np.hypot(c[3 + 2 * i], c[4 + 2 * i])
    return ce, cp, amp, np.sqrt(((eps - A @ ce) ** 2).mean()), np.sqrt(((psi - A @ cp) ** 2).mean())
for it in range(4):
    ce, cp, amp, re_, rp_ = run(H, dpsi0, deps0)
    print(f'round {it}: H = {H:.10f}, DPSI0 = {dpsi0:+.4f}", DEPS0 = {deps0:+.4f}"  ->  precession {cp[1]:.4f} {cp[2]:+.4f} T "/cy (target {RATE}); mean pole at J2000: longitude offset {cp[0]:+.4f}", tilt {ce[0] - EPS0:+.4f}" from 23.4392911 deg; tilt rate {ce[1]:+.4f}"/cy, {ce[2]:+.4f} T^2', flush=True)
    print(f'         nutation: 18.6 yr: tilt {amp(ce, 0):.3f}", longitude {amp(cp, 0):.3f}";  9.3 yr: {amp(ce, 1):.3f}", {amp(cp, 1):.3f}";  half-year: {amp(ce, 2):.3f}", {amp(cp, 2):.3f}";  fortnight: {amp(ce, 4):.3f}", {amp(cp, 4):.3f}";  residual rms {re_:.3f}", {rp_:.3f}"', flush=True)
    if abs(cp[1] - RATE) < 0.002 and abs(cp[0]) < 0.002 and abs(ce[0] - EPS0) < 0.002: break
    H *= RATE / cp[1]; dpsi0 -= cp[0]; deps0 -= ce[0] - EPS0
print('FINAL HDYN=%.12g DPSI0=%.6f DEPS0=%.6f' % (H, dpsi0, deps0))
