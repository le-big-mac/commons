"""ref.py: an outside check of cell2.c. Reads the points that cell2 -check -dump wrote (whole-number units) and peels
them again here, another way: three copies of the window instead of two, Python's exact whole numbers, and the
definition itself for which points go (the corners of the lower hull of the lifted points, found by a chain written
separately). Says how many points of height <= HM have a depth different from the one cell2's streaming gave.
    python -I ref.py DUMP"""
import sys
lines = open(sys.argv[1]).read().split('\n'); WU, HMU = map(int, lines[0].split())
pts = [tuple(map(int, l.split())) for l in lines[1:] if l.strip()]            # x, y, depth by cell2 (0 above HM)
alive = sorted(range(len(pts)), key=lambda i: (pts[i][0], pts[i][1], i)); depth = [0] * len(pts); layer = 0
def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
while any(pts[i][1] <= HMU for i in alive):
    layer += 1
    L = []                                                                    # lifted points of three copies, in order of x
    for shift in (-WU, 0, WU):
        for i in alive: x = pts[i][0] + shift; L.append((x, pts[i][1] + x * x, i, shift))
    hull = []
    for q in L:
        if hull and hull[-1][0] == q[0]:                                      # same x: only the lower can be a corner
            if q[1] >= hull[-1][1]: continue
            hull.pop()
        while len(hull) >= 2 and cross(hull[-2], hull[-1], q) <= 0: hull.pop()
        hull.append(q)
    gone = set(q[2] for q in hull if q[3] == 0)                               # the middle copy speaks
    for i in gone: depth[i] = layer
    alive = [i for i in alive if i not in gone]
differ = sum(1 for i, p in enumerate(pts) if p[1] <= HMU and depth[i] != p[2]); n = sum(1 for p in pts if p[1] <= HMU)
print('points of height <= HM: %d; layers %d; different from cell2: %d' % (n, layer, differ))
sys.exit(1 if differ else 0)
