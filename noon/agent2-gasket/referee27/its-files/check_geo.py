"""Second way of counting: build the circles as geometric objects (centre and radius),
search over ALL swaps (up and down), identify a circle by its curvature and centre,
check tangency of every new circle numerically, and compare the count at each curvature
with the C program's file.  Does not use the 'never undo, always increase' rule."""
import sys, math
import numpy as np

def build(q):
    a, b, c, d = q
    assert a < 0
    R = 1.0 / -a
    circ = [(a, 0.0, 0.0)]
    x2 = R - 1.0 / b
    circ.append((b, b * x2, 0.0))
    def place(k, sign):
        r1 = R - 1.0 / k
        r2 = 1.0 / b + 1.0 / k
        x = (r1 * r1 - r2 * r2 + x2 * x2) / (2 * x2)
        y2 = r1 * r1 - x * x
        y = sign * math.sqrt(max(y2, 0.0))
        return x, y
    x3, y3 = place(c, 1)
    circ.append((c, c * x3, c * y3))
    best = None
    for sg in (1, -1):
        x4, y4 = place(d, sg)
        err = abs(math.hypot(x4 - x3, y4 - y3) - (1.0 / c + 1.0 / d))
        if best is None or err < best[0]:
            best = (err, x4, y4)
    assert best[0] < 1e-6, best
    circ.append((d, d * best[1], d * best[2]))
    return circ

def tangent(c1, c2):
    k1, x1, y1 = c1; k2, x2, y2 = c2
    dist = math.hypot(x1 / k1 - x2 / k2, y1 / k1 - y2 / k2)
    if k1 < 0 or k2 < 0:
        want = abs(1.0 / abs(k1) - 1.0 / abs(k2))
    else:
        want = 1.0 / k1 + 1.0 / k2
    return abs(dist - want)

def run(q, M):
    circ = build(q)
    ids = {}
    circles = []
    def key(c):
        return (c[0], round(c[1] + 0.3183), round(c[2] + 0.7071))
    def get(c):
        kk = key(c)
        if kk in ids:
            return ids[kk]
        ids[kk] = len(circles)
        circles.append(c)
        return ids[kk]
    root = tuple(sorted(get(c) for c in circ))
    seen = {root}
    stack = [root]
    worst = 0.0
    while stack:
        Q = stack.pop()
        cs = [circles[i] for i in Q]
        sk = sum(c[0] for c in cs); sx = sum(c[1] for c in cs); sy = sum(c[2] for c in cs)
        for i in range(4):
            o = cs[i]
            n = (2 * (sk - o[0]) - o[0], 2 * (sx - o[1]) - o[1], 2 * (sy - o[2]) - o[2])
            if n[0] > M:
                continue
            new_before = len(circles)
            j = get(n)
            if j == new_before:  # a new circle: check it really is tangent to the other three
                for t in range(4):
                    if t != i:
                        worst = max(worst, tangent(n, cs[t]) * max(abs(n[0]), 1))
            Q2 = tuple(sorted(Q[:i] + Q[i + 1:] + (j,)))
            if Q2 not in seen:
                seen.add(Q2)
                stack.append(Q2)
    return circles, worst, len(seen)

if __name__ == '__main__':
    M = int(sys.argv[1])
    for q, f in [((-3, 5, 8, 8), 'out/g_-3_5_8_8_1e6.bin'), ((-4, 5, 20, 21), 'out/g_-4_5_20_21_1e6.bin'),
                 ((-1, 2, 2, 3), 'out/g_-1_2_2_3_1e6.bin'), ((-3, 4, 12, 13), 'out/g_-3_4_12_13_1e6.bin'),
                 ((-2, 3, 6, 7), 'out/g_-2_3_6_7_1e6.bin'), ((-23, 48, 49, 52), 'out/g_-23_48_49_52_1e6.bin')]:
        circles, worst, nq = run(q, M)
        geo = np.zeros(M + 1, dtype=np.int64)
        neg = 0
        for c in circles:
            if c[0] < 0: neg += 1
            else: geo[c[0]] += 1
        cc = np.fromfile(f, dtype=np.uint32)[:M + 1].astype(np.int64)
        diff = np.nonzero(geo != cc)[0]
        print(q, 'M', M, 'circles(geo)', len(circles), 'neg', neg, 'quadruples', nq,
              'C total<=M', int(cc.sum()) + 1, 'curvatures differing:', len(diff), list(diff[:10]),
              'worst tangency error (relative)', '%.2e' % worst)
