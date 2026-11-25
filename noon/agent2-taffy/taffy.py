"""Taffy pullers as braids: growth of a loop, Burau matrices, and a model flow.
usage: python taffy.py identities | python taffy.py sheet results.json
Moves: ('s', i) = the rods in places i and i+1 change places clockwise; ('S', i) = anticlockwise.  Places are numbered from 1."""
import sys, json, math, time
import numpy as np

# ---------------------------------------------------------------- loops as words in the free group
def reduce(word):
    out = []
    for x in word:
        if out and out[-1] == -x: out.pop()
        else: out.append(x)
    return out
def cyclic(word):
    w = reduce(word); a, b = 0, len(w)
    while b - a >= 2 and w[a] == -w[b - 1]: a += 1; b -= 1
    return w[a:b]
def images(move, n):
    """where each generator goes: s_i sends x_i to x_i x_{i+1} x_i^-1 and x_{i+1} to x_i; S_i is its inverse"""
    kind, i = move; img = {k: [k] for k in range(1, n + 1)}
    if kind == 's': img[i] = [i, i + 1, -i]; img[i + 1] = [i]
    else: img[i] = [i + 1]; img[i + 1] = [-(i + 1), i, i + 1]
    for k in range(1, n + 1): img[-k] = [-x for x in reversed(img[k])]
    return img
def act(word, move, n):
    img = images(move, n); out = []
    for x in word:
        for y in img[x]:
            if out and out[-1] == -y: out.pop()
            else: out.append(y)
    return out
def growth(moves, n, cap=2_000_000, start=(1, 2)):
    w = list(start); lengths = [len(cyclic(w))]
    while True:
        for m in moves: w = act(w, m, n)
        w = cyclic(w); lengths.append(len(w))
        if len(w) > cap or len(lengths) > 60: break
    k = max(j for j, L in enumerate(lengths) if L <= cap)
    return lengths[k] / lengths[k - 1], lengths

# ---------------------------------------------------------------- Burau matrices at t = -1
def burau(moves, n, t=-1.0):
    P = np.eye(n)
    for kind, i in moves:
        B = np.eye(n); B[i - 1:i + 1, i - 1:i + 1] = [[1 - t, t], [1, 0]]
        P = P @ (B if kind == 's' else np.linalg.inv(B))
    return float(np.abs(np.linalg.eigvals(P)).max())

# ---------------------------------------------------------------- the flow
SIG = 0.35
def rods(moves, n, t):
    """positions and velocities of the n rods at time t (each move lasts one unit of time), by place"""
    k = int(math.floor(t)); u = t - k; kind, i = moves[k % len(moves)]
    p = np.stack([np.arange(n, dtype=float), np.zeros(n)], 1); v = np.zeros((n, 2))
    c = np.array([i - 0.5, 0.0]); ang = math.pi * (u - math.sin(2 * math.pi * u) / (2 * math.pi)); rate = math.pi * (1 - math.cos(2 * math.pi * u))
    sgn = -1.0 if kind == 's' else 1.0                      # clockwise is a negative angle
    for place in (i - 1, i):
        d = p[place] - c; a = sgn * ang; rot = np.array([d[0] * math.cos(a) - d[1] * math.sin(a), d[0] * math.sin(a) + d[1] * math.cos(a)])
        p[place] = c + rot; v[place] = sgn * rate * np.array([-rot[1], rot[0]])
    return p, v
def velocity(x, p, v):
    G = np.exp(-((x[:, None, :] - p[None, :, :]) ** 2).sum(2) / (2 * SIG ** 2))            # points x rods
    Gp = np.exp(-((p[:, None, :] - p[None, :, :]) ** 2).sum(2) / (2 * SIG ** 2))
    out = np.zeros_like(x)
    for i in np.nonzero(np.abs(v).sum(1) > 0)[0]:
        others = [j for j in range(len(p)) if j != i]
        W = G[:, i] * np.prod(1 - G[:, others], axis=1) / np.prod(1 - Gp[i, others])
        out += W[:, None] * v[i][None, :]
    return out
def refine(x, gap=0.01):
    d = np.linalg.norm(np.roll(x, -1, 0) - x, axis=1); far = np.nonzero(d > gap)[0]
    if len(far) == 0: return x
    mid = (x[far] + np.roll(x, -1, 0)[far]) / 2
    return np.insert(x, far + 1, mid, axis=0)
def length(x):
    return float(np.linalg.norm(np.roll(x, -1, 0) - x, axis=1).sum())
def circle(n_pts=600, centre=(0.5, 0.0), radius=0.8):
    a = np.linspace(0, 2 * math.pi, n_pts, endpoint=False); return np.stack([centre[0] + radius * np.cos(a), centre[1] + radius * np.sin(a)], 1)
def flow(moves, n, periods, dt=0.005, on_step=None, max_points=6_000_000):
    x = refine(circle()); L = [length(x)]; steps = int(round(1 / dt)); t = 0.0
    for per in range(periods):
        for _ in range(len(moves) * steps):
            p1, v1 = rods(moves, n, t); p2, v2 = rods(moves, n, t + dt / 2); p3, v3 = rods(moves, n, min(t + dt, math.floor(t) + 1 - 1e-12))
            k1 = velocity(x, p1, v1); k2 = velocity(x + 0.5 * dt * k1, p2, v2); k3 = velocity(x + 0.5 * dt * k2, p2, v2); k4 = velocity(x + dt * k3, p3, v3)
            x = refine(x + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)); t = round(t + dt, 10)
            if on_step: on_step(t, x)
            if len(x) > max_points: return L, x
        L.append(length(x))
    return L, x

DEVICES = {
    'T1': (3, [('s', 1), ('S', 2)]),
    'T2': (3, [('s', 1), ('s', 1), ('S', 2), ('S', 2)]),
    'T3': (3, [('s', 1), ('s', 2)]),
    'T4': (4, [('s', 1), ('s', 2), ('S', 3)]),
    'T5': (4, [('s', 1), ('s', 3), ('S', 2)]),
    'T6': (4, [('s', 1), ('s', 3), ('S', 2), ('S', 2)]),
}
if __name__ == '__main__':
    if sys.argv[1] == 'identities':
        # the rewriting rules respect the braid relations and inverses (nothing here is on the sealed sheet)
        n = 4; gens = [[k] for k in range(1, n + 1)]
        def run(ms, w):
            for m in ms: w = act(w, m, n)
            return reduce(w)
        ok1 = all(run([('s', 1), ('s', 2), ('s', 1)], g) == run([('s', 2), ('s', 1), ('s', 2)], g) for g in gens)
        ok2 = all(run([('s', 1), ('s', 3)], g) == run([('s', 3), ('s', 1)], g) for g in gens)
        ok3 = all(run([('s', 2), ('S', 2)], g) == g and run([('S', 3), ('s', 3)], g) == g for g in gens)
        ok4 = run([('s', 1), ('s', 2), ('s', 3)], [1, 2, 3, 4]) == [1, 2, 3, 4]              # the loop round all the rods is left alone
        print("braid relation s1 s2 s1 = s2 s1 s2:", ok1, "; far moves commute:", ok2, "; a move and its reverse cancel:", ok3, "; the loop round all rods is unchanged:", ok4)
        p, v = rods([('s', 1)], 3, 0.999999); q, _ = rods([('s', 1)], 3, 0.0)
        print("after one move the two rods have changed places:", np.allclose(p[0], q[1], atol=1e-4) and np.allclose(p[1], q[0], atol=1e-4), "; half way the left rod is above the line (clockwise):", rods([('s', 1)], 3, 0.5)[0][0][1] > 0)
        x = circle(); print("the fluid at a rod moves with the rod, and stands still at the other rods:", np.allclose(velocity(rods([('s', 1)], 3, 0.3)[0], *rods([('s', 1)], 3, 0.3)), rods([('s', 1)], 3, 0.3)[1], atol=1e-12))
    if sys.argv[1] == 'sheet':
        t0 = time.time(); res = {}
        for name, (n, moves) in DEVICES.items():
            g, lengths = growth(moves, n); res[name] = dict(n=n, moves=moves, growth=g, lengths=lengths, burau=burau(moves, n))
            print(f"{name}: {n} rods, {' '.join(k + '_' + str(i) for k, i in moves)}: growth per period {g:.6f} (lengths {lengths[:8]}{' ...' if len(lengths) > 8 else ''}, last {lengths[-1]}); Burau number {res[name]['burau']:.6f}", flush=True)
        for name in ('T2', 'T3'):
            n, moves = DEVICES[name]; L, x = flow(moves, n, 4 if name == 'T2' else 6)
            res['flow_' + name] = dict(L=L, points=len(x)); print(f"flow, device of {name}: lengths after each period {[round(v, 2) for v in L]}; ratios {[round(b / a, 3) for a, b in zip(L, L[1:])]}; {len(x)} points at the end", flush=True)
        res['seconds'] = time.time() - t0; json.dump(res, open(sys.argv[2], 'w')); print(f"{res['seconds']:.0f} s")
