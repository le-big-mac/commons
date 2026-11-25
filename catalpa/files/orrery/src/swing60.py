# Is there a real 18.6-year swing difference in the node between my model and JPL?  Sixty continuous years of daily samples, 970-1030 AD.
# usage: python -I swing60.py <my daily states (Earth, Moon lines)> <dir with hz60_301.txt, hz60_399.txt> <label>
import sys, re, numpy as np
mine, hzdir, label = sys.argv[1:4]
AU = 149597870.7; MU = (398600.435507 + 4902.800118) * 86400.0 ** 2 / AU ** 3; AS = 206264.806247
num = r'([-+]?\d\.\d+E[-+]\d+)'
def hz(p):
    b = open(p).read().split('$$SOE')[1].split('$$EOE')[0]
    return np.array([[float(x) for x in m.groups()] for m in re.finditer(r'(\d+\.\d+) = [AB]\.[DC]\..*?\n\s*X\s*=\s*' + num + r'\s*Y\s*=\s*' + num + r'\s*Z\s*=\s*' + num + r'\s*\n\s*VX=\s*' + num + r'\s*VY=\s*' + num + r'\s*VZ=\s*' + num, b)])
Hm, He = hz(f'{hzdir}/hz60_301.txt'), hz(f'{hzdir}/hz60_399.txt'); jd = Hm[:, 0]
E, M = {}, {}
for line in open(mine):
    w = line.split()
    (E if w[1] == '3' else M)[w[0]] = [float(x) for x in w[2:]]
keys = [f'{x:.2f}' for x in jd]; ok = np.array([k in E and k in M for k in keys]); print(f'== {label}: {ok.sum()} matching days of {len(jd)}')
me = np.array([M[k] for k, o in zip(keys, ok) if o]) - np.array([E[k] for k, o in zip(keys, ok) if o]); jp = (Hm[:, 1:] - He[:, 1:])[ok]; t = (jd[ok] - 2451545.0) / 36525
def node(x): h = np.cross(x[:, :3], x[:, 3:]); return np.arctan2(h[:, 0], -h[:, 1])
Oj = np.unwrap(node(jp)); d = ((node(me) - node(jp) + np.pi) % (2 * np.pi) - np.pi) * AS
def box(y, m): c = np.cumsum(np.insert(y, 0, 0.0)); return (c[m:] - c[:-m]) / m
m = 413; ds, ts, Os = box(d, m), box(t, m), box(Oj, m)
X = np.vstack([np.ones_like(ts), ts - ts.mean(), (ts - ts.mean()) ** 2, np.cos(Os), np.sin(Os), np.cos(2 * Os), np.sin(2 * Os)]).T; c = np.linalg.lstsq(X, ds, rcond=None)[0]; r = ds - X @ c
X0 = X[:, :3]; c0 = np.linalg.lstsq(X0, ds, rcond=None)[0]; r0 = ds - X0 @ c0
print(f'   node, mine - JPL, 413-day running means over {ts[-1] * 100 - ts[0] * 100:.1f} years: mean {ds.mean():+.3f}", trend {c[1]:+.4f}"/cy; scatter about a parabola {r0.std():.4f}"')
print(f'   in step with the node: {c[3]:+.4f} cos(node) {c[4]:+.4f} sin(node)  -> amplitude {np.hypot(c[3], c[4]):.4f}";   twice the node: amplitude {np.hypot(c[5], c[6]):.4f}";   scatter left {r.std():.4f}"')
T0 = -ts.mean(); print(f'   the century samples suggested, at T = {T0:.1f}: (mine with J2(t)) - JPL: -4.2e-4 T^2 cos + 5.8e-4 T^2 sin = {-4.2e-4 * T0 ** 2:+.4f} cos {5.8e-4 * T0 ** 2:+.4f} sin;   a swing growing with J2: {8.3e-6 * T0 ** 2 * 93.7:.4f}" x (-7.2 cos + 93.4 sin)/93.7')
