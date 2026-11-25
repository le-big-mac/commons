"""arccheck.py: flow.c's gradient of T on a shape with an arc and flat sides, checked by erode.c alone.   python -I arccheck.py
The quarter disc (radius 2, its corner at the origin). Five small changes of the edge: the arc pushed out and in by a smooth bump
(cos^2, 20 degrees to each side) centred at 22.5, 45 and 67.5 degrees, and each flat side moved out and in. For each, erode.c
gives T of the changed shape both ways (as a polygon of many points), so (T+ - T-) / (2 eps) is the gradient of T summed
against that change; flow.c's g (psi R dtheta at its first step, from -map) summed against the same change should be the same.
Moving the side y = 0 down by eps changes the support function by eps at 270 degrees and by eps |sin| in the two corners' fans
beside it (the corners move with the side). In the limit g is nothing in a fan; on a mesh a little of the side's g lies on the
nodes next to it, so the sum is taken against the whole change; the sum over the three nodes at the side's direction is printed too."""
import json, math, os, subprocess, sys, tempfile
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); TMP = tempfile.mkdtemp(prefix='agent2-arc-', dir='/dev/shm'); R0 = 2.0; W = math.radians(20)
def bump(th, c): d = np.abs(th - c); return np.where(d < W, np.cos(math.pi * d / (2 * W)) ** 2, 0.0)
def dbump(th, c): d = th - c; return np.where(np.abs(d) < W, -math.pi / (2 * W) * np.sin(math.pi * d / W), 0.0)
def shape(eps, c=None, side=None, delta=0.0):
    """corners of the changed quarter disc, counter-clockwise: the arc with h = R0 + eps bump, the flat sides moved out by delta"""
    th = np.linspace(0, math.pi / 2, 3601); h = R0 + (eps * bump(th, c) if c is not None else 0); hp = eps * dbump(th, c) if c is not None else 0 * th
    arc = np.stack([h * np.cos(th) - hp * np.sin(th), h * np.sin(th) + hp * np.cos(th)], 1)
    if side == 'bottom':                                   # the side y = 0 moved to y = -delta
        if delta >= 0: return np.vstack([[0, -delta], [R0, -delta], arc, ])
        t0 = math.asin(-delta / R0); return np.vstack([[0, -delta], arc[th >= t0][0:0], [math.sqrt(R0 ** 2 - delta ** 2), -delta], arc[th > t0]])
    if side == 'left':                                     # the side x = 0 moved to x = -delta
        if delta >= 0: return np.vstack([[-delta, 0], arc, [-delta, R0]])
        t1 = math.acos(-delta / R0); return np.vstack([[-delta, 0], arc[th < t1], [-delta, math.sqrt(R0 ** 2 - delta ** 2)]])
    return np.vstack([[0, 0], arc])
def T(P, tag):
    f = os.path.join(TMP, tag + '.txt'); np.savetxt(f, P, fmt='%.12f'); o = [json.loads(subprocess.run(['nice', '-n', '19', os.path.join(HERE, 'erode'), 'file:' + f, '16384', e, '1e-3'], capture_output=True, text=True).stdout) for e in ('1e-4', '3e-5')]
    return o[1]['T'] + (o[1]['T'] - o[0]['T']) / ((1e-4 / 3e-5) ** (2 / 3.0) - 1), o[1]['area']
# flow's g on the quarter disc at its first step
m = os.path.join(TMP, 'map.txt'); G = {}
for q in ('0.5', '0.25'):
    subprocess.run(['nice', '-n', '19', os.path.join(HERE, 'flow'), 'quarter', '1440', '-q', q, '-map', m, '1000000'], capture_output=True); a = np.loadtxt(m); a = a[a[:, 0] == 0]; G[q] = a[:, 4] * a[:, 5] * (2 * math.pi / 1440)
g = 2 * G['0.25'] - G['0.5']; th = np.arange(1440) * 2 * math.pi / 1440
print('flow.c: the sum of g over the nodes is %.6f; g at the two sides\' directions %.5f (180 degrees) and %.5f (270); the largest g elsewhere off the arc %.1e' % (g.sum(), g[720], g[1080], max(abs(g[k]) for k in range(1440) if k > 361 and k not in (719, 720, 721, 1079, 1080, 1081) and k < 1439)))
T0, A0 = T(shape(0), 'base'); print('erode.c: the quarter disc itself: area %.6f, T %.6f' % (A0, T0)); worst = 0; rows = []
for label, kw, eps, flow_val in [('the arc pushed out about %g degrees' % d, {'c': math.radians(d)}, 0.01, float((g * bump(th, math.radians(d))).sum())) for d in (22.5, 45, 67.5)] + \
                                [('the side y = 0 moved', {'side': 'bottom'}, 0.02, float((g * np.maximum(0, -np.sin(th)) * (th > math.pi + 1e-9)).sum())), ('the side x = 0 moved', {'side': 'left'}, 0.02, float((g * np.maximum(0, -np.cos(th))).sum()))]:
    if 'c' in kw: Tp, Ap = T(shape(eps, **kw), 'p'); Tm, Am = T(shape(-eps, **kw), 'm')
    else: Tp, Ap = T(shape(0, delta=eps, **kw), 'p'); Tm, Am = T(shape(0, delta=-eps, **kw), 'm')
    fd = (Tp - Tm) / (2 * eps); worst = max(worst, abs(fd / flow_val - 1)); print('%-38s erode.c (T+ - T-)/(2 eps) = %.5f   flow.c\'s g summed against it = %.5f   ratio %.4f   (areas %.5f, %.5f)' % (label, fd, flow_val, fd / flow_val, Am, Ap))
print('the furthest the two are apart: %.1f in 1,000' % (worst * 1000))
fan = [k for k in range(1440) if 360 < k < 1440 and k not in (719, 720, 721, 1079, 1080, 1081)]; arc = list(range(0, 361))
print('where flow.c\'s g lies (1,440 angles): on the arc %.5f; at the two sides\' directions (three nodes each) %.5f and %.5f; on the other %d nodes of the three fans %.5f in all, of which within 5 degrees of a side %.5f' % (g[arc].sum(), g[719:722].sum(), g[1079:1082].sum(), len(fan), g[fan].sum(), sum(g[k] for k in fan if min(abs(k - 720), abs(k - 1080)) <= 20)))
import shutil; shutil.rmtree(TMP)
