# Referee: recompute the sums ./rings keeps, from the author's points, with numpy; compare for every annulus.
import sys, json, math
import numpy as np
pts = np.loadtxt(sys.argv[1], skiprows=1)
J = json.loads(open(sys.argv[2]).read())
n0 = float(sys.argv[3]); half = 0.008
R = 2.0 ** 29
x = pts[:, 0] / R; y = pts[:, 1] / R; d = pts[:, 2]
rho = np.hypot(x, y); th = np.arctan2(y, x)
A0 = 0.75 * 1.3259 * (n0 / math.pi) ** (2 / 3)
worst = 0
for k in range(19):
    r = 0.05 * (k + 1)
    sel = np.abs(rho - r) <= half
    dd = d[sel]; rr = rho[sel]; tt = th[sel]
    mine = [sel.sum(), (dd - A0 * (1 - rr ** (4 / 3))).sum(), dd.sum(), (dd * dd).sum(), rr.sum(), (rr * rr).sum(), (rr * dd).sum()]
    for m in (1, 2, 3, 4):
        mine += [np.cos(m * tt).sum(), np.sin(m * tt).sum(), (dd * np.cos(m * tt)).sum(), (dd * np.sin(m * tt)).sum()]
    theirs = J['rings'][k]
    # compare on the scale of each sum's natural size
    scale = [1, max(1, abs(mine[2])), max(1, abs(mine[2])), max(1, abs(mine[3])), 1, 1, max(1, abs(mine[6]))] + [max(1.0, abs(mine[2]))] * 16
    diff = max(abs(a - b) / s for a, b, s in zip(mine, theirs, scale))
    worst = max(worst, diff)
    if k in (9,):
        print('annulus r=%.2f: points mine %d theirs %d' % (r, mine[0], theirs[0]))
        for nm, a, b in zip(['sum(depth-profile)', 'sum depth', 'sum depth^2', 'sum rho', 'sum rho^2', 'sum rho*depth', 'sum cos1', 'sum sin1', 'sum d cos1', 'sum d sin1', 'sum cos2', 'sum sin2', 'sum d cos2', 'sum d sin2'], mine[1:15], theirs[1:15]):
            print('   %-20s mine %.10g  theirs %.10g' % (nm, a, b))
print('largest relative difference over all 19 annuli and 23 sums: %.2e' % worst)
print('layers in JSON', J['layers'], ' max depth in points', int(d.max()), ' n', J['n'], len(d))
