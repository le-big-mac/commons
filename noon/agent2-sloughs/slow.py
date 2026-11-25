"""slow.py -- the river model again, written apart from river.c, to test it.

Same rules, different workings: the upstream integral is a closed-form sum (river.c steps along the stream),
neck cutoffs are found by measuring every pair of nodes (river.c sorts nodes into cells), and the spacing rule
is written out afresh.  It starts from a file of nodes written by river.c at t = 0, so that both begin from
the same river, and prints the same columns.

usage: python slow.py P DC LX T START.txt [DS [F0SQ]]

It is for small valleys: the closed-form sum underflows when the river is longer than about 700.
"""
import sys
import numpy as np

P, DC, LX, T = (float(a) for a in sys.argv[1:5])
start = sys.argv[5]
DS = float(sys.argv[6]) if len(sys.argv) > 6 else 0.1
DT = 0.1 * DS * DS
F0SQ = float(sys.argv[7]) if len(sys.argv) > 7 else None      # the feedback of length on the reach-wide values
AMIN = 3 * DC
EVERY = 5

f = open(start).readline().split()
xy = np.array(f[2:], float).reshape(-1, 2)
x = xy[:, 0].copy(); y = xy[:, 1].copy()


def geometry(x, y):
    n = len(x)
    xn = np.roll(x, -1).copy(); xn[-1] += LX; yn = np.roll(y, -1)
    xp = np.roll(x, 1).copy(); xp[0] -= LX; yp = np.roll(y, 1)
    ax, ay = x - xp, y - yp            # the segment arriving
    bx, by = xn - x, yn - y            # the segment leaving
    la = np.hypot(ax, ay); lb = np.hypot(bx, by)
    cx, cy = ax + bx, ay + by; c = np.hypot(cx, cy)
    kappa = 2 * (ax * by - ay * bx) / (la * lb * c)
    return la, lb, kappa, -cy / c, cx / c


def upstream(la, kappa):
    """I(s_i) = sum over the segments above of their exact share, each damped by exp(-distance).
    la: the segment lengths, already divided by the decay length."""
    n = len(la)
    kp = np.roll(kappa, 1)
    E = np.exp(-la); c2 = (1 - E * (1 + la)) / la; c1 = 1 - E
    q = kappa * (c1 - c2) + kp * c2                 # the share of the segment that ends at node i
    s = np.cumsum(la)                               # distance of node i below the node before node 0
    total = s[-1]
    # twice round: the river above node i is the nodes 0..i of this lap and all of the lap before
    w = np.exp(s - s[-1])                           # at most 1, so nothing overflows
    cum = np.cumsum(q * w)
    this_lap = cum / w
    lap_before = cum[-1] * np.exp(-s)               # the whole previous lap, seen from node i
    return this_lap + lap_before, total


def respace(x, y):
    n = len(x)
    lo, hi = 0.5 * DS, 1.5 * DS
    xn = np.roll(x, -1).copy(); xn[-1] += LX
    d = np.hypot(xn - x, np.roll(y, -1) - y)
    if d.max() <= hi and d.min() >= lo:
        return x, y
    X2 = []; Y2 = []
    for i in range(n):
        a = i - 1; j = (i + 1) % n; k = (j + 1) % n
        xa = x[a] - (LX if i == 0 else 0); ya = y[a]
        xi = x[i]; yi = y[i]
        xj = x[j] + (LX if j == 0 else 0); yj = y[j]
        xk = x[k] + (LX if (j == 0 or k == 0) else 0); yk = y[k]
        if X2 and i > 0 and np.hypot(xi - X2[-1], yi - Y2[-1]) < lo:
            continue
        if i == n - 1 and len(X2) > 1 and np.hypot(X2[0] + LX - xi, Y2[0] - yi) < lo:
            continue
        X2.append(xi); Y2.append(yi)
        dist = np.hypot(xj - xi, yj - yi)
        if dist > hi:
            parts = int(np.ceil(dist / DS))
            for q in range(1, parts):
                t = q / parts; t2 = t * t; t3 = t2 * t
                w0 = -0.5 * t3 + t2 - 0.5 * t; w1 = 1.5 * t3 - 2.5 * t2 + 1
                w2 = -1.5 * t3 + 2 * t2 + 0.5 * t; w3 = 0.5 * t3 - 0.5 * t2
                X2.append(w0 * xa + w1 * xi + w2 * xj + w3 * xk); Y2.append(w0 * ya + w1 * yi + w2 * yj + w3 * yk)
    return np.array(X2), np.array(Y2)


def cutoff(x, y):
    """Every pair measured.  The first node (going downstream) that has a partner within DC and further than
    AMIN along the loop; of its partners, the one that closes the longest loop."""
    n = len(x)
    xn = np.roll(x, -1).copy(); xn[-1] += LX
    seg = np.hypot(xn - x, np.roll(y, -1) - y)
    s = np.concatenate([[0], np.cumsum(seg)[:-1]]); total = seg.sum()
    for i in range(n):
        dx = x[i + 1:] - x[i]; dy = y[i + 1:] - y[i]
        k = np.floor(dx / LX + 0.5); dx = dx - k * LX
        near = dx * dx + dy * dy < DC * DC
        if not near.any():
            continue
        a1 = s[i + 1:] - s[i]
        arc = np.where(k == 0, a1, total - a1)
        if np.any(near & (k != 0) & (k != 1)):
            raise SystemExit("winding")
        ok = near & (arc > AMIN)
        if not ok.any():
            continue
        arcs = np.where(ok, arc, -1.0)
        jj = int(np.argmax(arcs)); j = i + 1 + jj; kk = int(k[jj])
        if kk == 0:
            x2 = np.concatenate([x[:i + 1], x[j:]]); y2 = np.concatenate([y[:i + 1], y[j:]])
        else:
            x2 = x[i:j + 1].copy(); y2 = y[i:j + 1].copy()
            x2 -= LX * np.floor(x2[0] / LX)
        return x2, y2, float(arcs[jj])
    return None


now = 0.0; nstep = 0; ncut = 0; cutlen = 0.0; nextout = 0.0
print("# slow.py P=%g DC=%g LX=%g T=%g DS=%g DT=%g" % (P, DC, LX, T, DS, DT))
while True:
    if now >= nextout - 1e-9:
        la, lb, kappa, nx, ny = geometry(x, y)
        length = lb.sum(); w = 0.5 * (la + lb)
        ym = (y * w).sum() / length; y2 = (y * y * w).sum() / length - ym * ym
        print("%.4f %d %.6f %d %.4f %.6f %.4f %.4f %.4f %.4f" % (now, len(x), length / LX, ncut, cutlen, (np.abs(kappa) * w).sum() / length,
                                                             np.abs(kappa).max(), y.min(), y.max(), np.sqrt(max(y2, 0))))
        sys.stdout.flush()
        nextout += 1.0
    if now >= T - 1e-9:
        break
    la, lb, kappa, nx, ny = geometry(x, y)
    if F0SQ is None:
        I, total = upstream(la, kappa)
        V = kappa - P * I
    else:
        tau = lb.sum() / LX; dec = tau ** (1 / 3)
        I, total = upstream(la / dec, kappa)
        V = (kappa - (F0SQ / tau + 2 * P - F0SQ) / 2 * I) / dec
    x = x + DT * V * nx; y = y + DT * V * ny
    nstep += 1; now = nstep * DT
    x, y = respace(x, y)
    if nstep % EVERY == 0:
        while True:
            r = cutoff(x, y)
            if r is None:
                break
            x, y, arc = r; ncut += 1; cutlen += arc
            x, y = respace(x, y)
