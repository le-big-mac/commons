"""Measure a trail system: the length of worn trail, and where its junctions are.

The footstep map is thresholded, thinned to a skeleton one cell wide, and the skeleton is traced branch by branch.
Each branch is smoothed (a staircase of cells is longer than the line it stands for) and its length added up.
`python measure.py calibrate` draws figures of known length and measures them the same way.
`python measure.py run-*.npz` prints one line per run."""
import sys
import numpy as np
from skimage.morphology import skeletonize, closing, remove_small_objects

SQ3 = np.sqrt(3)
STEINER_L, STEINER_D = SQ3, 2 / SQ3


def line_d(L):
    """the detour of the best straight network of length L: the line from the Steiner Y to the full triangle"""
    return STEINER_D - (L - STEINER_L) * (STEINER_D - 1) / (3 - STEINER_L)


def trace(skel):
    """skeleton (bool array) -> list of branches, each an ordered array of (row, col)"""
    pts = set(zip(*np.nonzero(skel)))
    def nbrs(p):
        r, c = p
        out = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if (dr or dc) and (r + dr, c + dc) in pts:
                    out.append((r + dr, c + dc))
        # a diagonal step is dropped when the two cells also share an orthogonal neighbour (no little triangles)
        keep = []
        for q in out:
            if abs(q[0] - r) + abs(q[1] - c) == 2 and (((r, q[1]) in pts) or ((q[0], c) in pts)):
                continue
            keep.append(q)
        return keep
    N = {p: nbrs(p) for p in pts}
    nodes = {p for p in pts if len(N[p]) != 2}
    branches, seen = [], set()
    for a in nodes:
        for b in N[a]:
            if (a, b) in seen:
                continue
            path = [a, b]
            seen.add((a, b))
            while path[-1] not in nodes:
                nxt = [q for q in N[path[-1]] if q != path[-2]]
                if not nxt:
                    break
                path.append(nxt[0])
            seen.add((path[-1], path[-2]))
            branches.append(np.array(path, float))
    # closed loops with no end and no junction: walk round each once
    used = {tuple(q.astype(int)) for b in branches for q in b}
    for start in sorted(pts - used):
        if start in used:
            continue
        path = [start, N[start][0]]
        while path[-1] != start:
            nxt = [q for q in N[path[-1]] if q != path[-2]]
            if not nxt:
                break
            path.append(nxt[0])
        used.update(path)
        branches.append(np.array(path, float))
    return branches, nodes


def smooth_length(path, w=9):
    if len(path) < 3:
        return float(np.hypot(*(path[-1] - path[0])))
    k = min(w, len(path) // 2 * 2 - 1)
    if k < 3:
        return float(np.hypot(*np.diff(path, axis=0).T).sum())
    pad = k // 2
    ext = np.vstack([2 * path[0] - path[pad:0:-1], path, 2 * path[-1] - path[-2:-pad - 2:-1]])   # reflect at the ends, so they stay put
    sm = np.stack([np.convolve(ext[:, i], np.ones(k) / k, mode='valid') for i in range(2)], axis=1)
    return float(np.hypot(*np.diff(sm, axis=0).T).sum())


def measure(mask, h, prune=6):
    mask = closing(mask, np.ones((3, 3), bool))
    mask = remove_small_objects(mask, max_size=11)
    skel = skeletonize(mask)
    for _ in range(3):                                                  # prune short spurs, a few times
        branches, nodes = trace(skel)
        ends = {p for p in nodes if sum(1 for b in branches if tuple(b[0].astype(int)) == p or tuple(b[-1].astype(int)) == p) == 1}
        cut = False
        for b in branches:
            a, z = tuple(b[0].astype(int)), tuple(b[-1].astype(int))
            if len(b) <= prune and ((a in ends) != (z in ends)):
                for p in b[1:] if a not in ends else b[:-1]:
                    skel[int(p[0]), int(p[1])] = False
                cut = True
        if not cut:
            break
    branches, nodes = trace(skel)
    L = sum(smooth_length(b) for b in branches) * h
    return L, skel, branches, nodes


def footmask(d, frac=0.10):
    foot = d['foot']
    ref = np.percentile(foot[foot > 0], 98)
    return foot > frac * ref


if __name__ == '__main__':
    if sys.argv[1] == 'calibrate':
        from skimage.draw import line as draw_line
        n, margin = 160, 0.12
        h = 1 / n
        def canvas(segs, width=2):
            nx, ny = int(round((1 + 2 * margin) * n)) + 1, int(round((SQ3 / 2 + 2 * margin) * n)) + 1
            m = np.zeros((ny, nx), bool)
            for (x0, y0), (x1, y1) in segs:
                rr, cc = draw_line(int(round((y0 + margin) * n)), int(round((x0 + margin) * n)), int(round((y1 + margin) * n)), int(round((x1 + margin) * n)))
                for dr in range(-width, width + 1):
                    for dc in range(-width, width + 1):
                        if dr * dr + dc * dc <= width * width:
                            m[np.clip(rr + dr, 0, ny - 1), np.clip(cc + dc, 0, nx - 1)] = True
            return m
        A, B, C = (0, 0), (1, 0), (0.5, SQ3 / 2)
        O = (0.5, SQ3 / 6)
        def inner(x):                                                   # spokes of length x along the bisectors, joined by an inner triangle
            P = [(A[0] + x * np.cos(np.pi / 6), A[1] + x * np.sin(np.pi / 6)), (B[0] - x * np.cos(np.pi / 6), B[1] + x * np.sin(np.pi / 6)), (C[0], C[1] - x)]
            return [(A, P[0]), (B, P[1]), (C, P[2]), (P[0], P[1]), (P[1], P[2]), (P[2], P[0])], 3 * x + 3 * (1 - SQ3 * x)
        figs = [("full triangle", [(A, B), (B, C), (C, A)], 3.0), ("Steiner Y", [(A, O), (B, O), (C, O)], SQ3)]
        for x in (0.15, 0.3, 0.45):
            segs, L = inner(x)
            figs.append((f"spokes of {x} and an inner triangle", segs, L))
        for name, segs, true in figs:
            for width in (1, 2, 3):
                L, _, _, _ = measure(canvas(segs, width), h)
                print(f"{name:38s} drawn {2 * width + 1} cells wide: true length {true:.3f}, measured {L:.3f} ({100 * (L / true - 1):+.1f}%)")
    else:
        print("cap   walked D   bound 1/sqrt(1-c^2)   length L   line at L   D above the line   junctions away from the gates: distance from the centre")
        for fn in sys.argv[1:]:
            d = np.load(fn)
            h = float(d['h'])
            L, skel, branches, nodes = measure(footmask(d), h)
            gates = d['gates']
            lo = d['lo']
            centre = gates.mean(0)
            deg = {}
            for b in branches:
                for p in (tuple(b[0].astype(int)), tuple(b[-1].astype(int))):
                    deg[p] = deg.get(p, 0) + 1
            junc = [np.array([p[1] * h + lo[0], p[0] * h + lo[1]]) for p, k in deg.items() if k >= 3]
            junc = [j for j in junc if min(np.hypot(*(j - g)) for g in gates) > 0.08]
            rj = sorted(round(float(np.hypot(*(j - centre))), 3) for j in junc)
            c, D = float(d['cap']), float(d['detour'])
            print(f"{c:.1f}   {D:.4f}     {1 / np.sqrt(1 - c * c):.4f}              {L:.3f}      {line_d(L):.4f}      {D - line_d(L):+.4f}            {rj}   [{fn}]")
