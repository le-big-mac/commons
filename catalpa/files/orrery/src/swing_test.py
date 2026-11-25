# Does the oblateness's 18.6-year swing of the Moon's node differ between JPL and my model as its steady part seems to?
import numpy as np
AU = 149597870.7; MU = (398600.435507 + 4902.800118) * 86400.0 ** 2 / AU ** 3; AS = 206264.806247
def load(p):
    a = np.loadtxt(p); E = a[a[:, 1] == 3]; M = a[a[:, 1] == 4]; n = min(len(E), len(M)); return E[:n, 0], M[:n, 2:] - E[:n, 2:]
def node(x):
    h = np.cross(x[:, :3], x[:, 3:]); return np.arctan2(h[:, 0], -h[:, 1])
ja, xa = load('cont_base.txt'); jb, xb = load('cont_j2.txt'); Oa, Ob = node(xa), node(xb); T = -(ja - 2451545.0) / 36525
d = np.unwrap(Ob - Oa) * AS / 0.1
# shape of the swing per unit oblateness: over the first 3 centuries (where the two runs' node phases still agree to 0.001 rad)
mk = T < 3.0; X = np.vstack([np.ones(mk.sum()), T[mk], T[mk] ** 2, np.cos(Oa[mk]), np.sin(Oa[mk]), np.cos(2 * Oa[mk]), np.sin(2 * Oa[mk])]).T
c = np.linalg.lstsq(X, d[mk], rcond=None)[0]; res = d[mk] - X @ c
print(f'the oblateness\'s swing of the node in my model, per unit oblateness (fit over 300 yr, 10-day samples): {c[3]:+.1f} cos(node) {c[4]:+.1f} sin(node) {c[5]:+.1f} cos(2 node) {c[6]:+.1f} sin(2 node) arcsec; steady {c[1]:+.1f}"/cy; rms {res.std():.1f}"')
p, q, p2, q2 = c[3:7]
rows = [l.split() for l in open('moon_vs_jpl_cen.out') if l.strip() and l.split()[0].replace('.', '', 1).isdigit() and len(l.split()) >= 7]
R = np.array([[float(x) for x in r[:4]] + [float(r[6])] for r in rows]); Tc = R[:, 0]; y = R[:, 3]; nd = np.radians(R[:, 4])
S = p * np.cos(nd) + q * np.sin(nd) + p2 * np.cos(2 * nd) + q2 * np.sin(2 * nd)
base = np.vstack([np.ones_like(Tc), Tc, Tc ** 3]).T; c0 = np.linalg.lstsq(base, y, rcond=None)[0]; r0 = y - base @ c0
full = np.vstack([np.ones_like(Tc), Tc, Tc ** 3, Tc ** 2 * S]).T; c1 = np.linalg.lstsq(full, y, rcond=None)[0]; r1 = y - full @ c1
cov = np.linalg.inv(full.T @ full) * r1.var() * len(Tc) / (len(Tc) - 4); sd = np.sqrt(cov[3, 3])
print(f'node, mine - JPL, 19 epochs: residual rms about const + a T + c T^3: {r0.std():.3f}";  with k T^2 x (the swing shape at each epoch\'s node): k = {c1[3]:+.2e} +- {sd:.1e}, rms {r1.std():.3f}" (cut by {100 * (1 - r1.std() / r0.std()):.0f}%)')
print(f'the oblateness reading of the steady drift predicts k = -8.8e-6;   cube with the swing term in the fit: {c1[2]:+.5f} T^3')
ok = (-1.4e-5 <= c1[3] <= -4e-6) and (r1.std() <= 0.7 * r0.std()); print('K1: ' + ('HELD' if ok else 'FAILED'))
# the same with a free swing growing as T^2, to see what phase and size the data themselves want
free = np.vstack([np.ones_like(Tc), Tc, Tc ** 3, Tc ** 2 * np.cos(nd), Tc ** 2 * np.sin(nd)]).T; c2 = np.linalg.lstsq(free, y, rcond=None)[0]; r2 = y - free @ c2
print(f'free fit, T^2 (u cos(node) + v sin(node)): u = {c2[3]:+.2e}, v = {c2[4]:+.2e} arcsec per century^2, rms {r2.std():.3f}";   the oblateness reading predicts u = {-8.8e-6 * p:+.2e}, v = {-8.8e-6 * q:+.2e}')
# ---- added after the first look: the free fit wants a swing in cos(node), not sin(node). That is what the reference plane does: I measure the node on the J2000 ecliptic, which the
# ecliptic of date has left by 47" per century, so a node drift dW shows as dW x (1 + (tilt / tan i) cos(node - 174.9 deg)). No free number in it.
tilt = 47.0029 / AS * Tc; mod = tilt / np.tan(np.radians(5.145)) * np.cos(nd - np.radians(174.876))
g = np.vstack([np.ones_like(Tc), Tc, Tc ** 3 * (1 + mod)]).T; cg = np.linalg.lstsq(g, y, rcond=None)[0]; rg = y - g @ cg
print(f'\nwith the reference-plane factor applied to the cube (no new free number): const {cg[0]:+.3f}, {cg[1]:+.4f} T, {cg[2]:+.5f} T^3 (1 + factor); rms {rg.std():.3f}" (was {r0.std():.3f}")')
g2 = np.vstack([np.ones_like(Tc), Tc, Tc ** 3 * (1 + mod), Tc ** 2 * S]).T; cg2 = np.linalg.lstsq(g2, y, rcond=None)[0]; rg2 = y - g2 @ cg2
cov = np.linalg.inv(g2.T @ g2) * rg2.var() * len(Tc) / (len(Tc) - 4); print(f'and then the oblateness swing on top: k = {cg2[3]:+.2e} +- {np.sqrt(cov[3, 3]):.1e} (the oblateness reading predicts -8.8e-6), rms {rg2.std():.3f}"')
