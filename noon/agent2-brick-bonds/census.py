"""Census of brick bonds with small periods.  (Noon = agent2, 21 November 2026)
usage: census.py out.pkl  h:Wmax [h:Wmax ...]      e.g.  census.py census.pkl 1:20 2:14 3:10 4:8 6:4
For each vertical period h and each horizontal period w <= Wmax (even) and each shear s: every stack of h courses of
period w in which no perpend sits on a perpend, closed up with the shear.  Each is reduced to its least periods and to a
canonical representative under translations and the two mirrors; duplicates are dropped; measures are attached."""
import sys, math, pickle, itertools, time
import numpy as np
from scipy.spatial import Delaunay
ASPECT = 4 / 3                                             # a course is 75 mm high, a quarter-brick 56.25 mm long

def course_masks(w):
    n = w // 2; out = []
    for eps in (0, 1):
        for mask in range(1 << n):
            if n == 1 and mask: continue
            if any((mask >> k) & 1 and (mask >> ((k + 1) % n)) & 1 for k in range(n)): continue
            out.append(sum(1 << ((eps + 2 * k) % w) for k in range(n) if not (mask >> k) & 1))
    return out
def rot(m, a, w):
    a %= w; full = (1 << w) - 1
    return ((m << a) | (m >> (w - a))) & full if a else m
def mir(m, w): return sum(1 << ((-x) % w) for x in range(w) if (m >> x) & 1)
def restrict(m, w0): return m & ((1 << w0) - 1)           # valid when m has period w0

def canon(w, cs, s):
    """(w0, h0, s0, tuple of h0 course masks), least under translations, course rotation and the two mirrors"""
    h = len(cs)
    w0 = next(t for t in range(2, w + 1, 2) if w % t == 0 and all(rot(m, t, w) == m for m in cs))
    cs = [restrict(m, w0) for m in cs]; s %= w0
    course = lambda c: rot(cs[c % h], (c // h) * s, w0)
    for h0 in range(1, h + 1):
        if h % h0: continue
        ts = [t for t in range(w0) if all(course(c + h0) == rot(course(c), t, w0) for c in range(h))]
        if ts: s0 = ts[0]; break
    base = [course(c) for c in range(h0)]
    best = None
    for flipv in (0, 1):
        for flipx in (0, 1):
            seq, sh = base, s0
            if flipv: seq, sh = seq[::-1], -sh             # reading the wall downwards
            if flipx: seq, sh = [mir(m, w0) for m in seq], -sh
            sh %= w0
            for r in range(h0):                            # start at course r: courses r .. r+h0-1, the later ones sheared
                rotated = [seq[(r + c) % h0] if r + c < h0 else rot(seq[(r + c) % h0], sh, w0) for c in range(h0)]
                for a in range(w0):
                    key = (w0, h0, sh, tuple(rot(m, a, w0) for m in rotated))
                    if best is None or key < best: best = key
    return best

def bricks(m, w):
    xs = [x for x in range(w) if (m >> x) & 1]
    return [(x, ((xs[(i + 1) % len(xs)] - x) % w) or w) for i, x in enumerate(xs)]

def measures(key):
    w, h, s, cs = key
    H = h * w // math.gcd(s, w) if s else h                # courses after which the wall repeats exactly
    course = lambda c: rot(cs[c % h], (c // h) * s, w)
    hdr = np.zeros((H, w), bool); centres = []
    for c in range(H):
        for (x, L) in bricks(course(c), w):
            if L == 2:
                hdr[c, x] = hdr[c, (x + 1) % w] = True; centres.append((x + 1.0, (c + 0.5) * ASPECT))
    share = hdr.mean(); ties = share / 2
    endless = 0; run = 0
    for x in range(w):
        col = hdr[:, x]
        if not col.any(): endless += 1; continue
        k = int(np.argmax(col)); col = np.r_[col[k:], col[:k]]; r = 0
        for v in col:
            r = 0 if v else r + 1; run = max(run, r)
    if endless: run = math.inf
    if not centres: return dict(share=0.0, ties=0.0, run=math.inf, endless=1.0, radius=math.inf, eff=0.0, ncourse=len(set(cs)))
    # Header centres of one exact period (w wide, H courses high, no shear), repeated over a patch that reaches at least
    # half a diagonal of that cell beyond it on every side.  A disc of radius above half the diagonal centred in the cell
    # contains a whole cell, hence a header; so every empty circle centred in the cell lies inside the patch, and the
    # Delaunay triangles of the patch with circumcentre in the cell are those of the infinite wall.
    base = [(x + 1.0, (c + 0.5) * ASPECT) for c in range(H) for (x, L) in bricks(course(c), w) if L == 2]
    Ht = H * ASPECT; half = math.hypot(w, Ht) / 2
    nx, ny = math.ceil(half / w) + 1, math.ceil(half / Ht) + 1
    P = np.array([(x + i * w, y + j * Ht) for (x, y) in base for i in range(-nx, nx + 1) for j in range(-ny, ny + 1)])
    try:
        tri = Delaunay(P, qhull_options="QJ")
        A, B, C = P[tri.simplices[:, 0]], P[tri.simplices[:, 1]], P[tri.simplices[:, 2]]
        d = 2 * (A[:, 0] * (B[:, 1] - C[:, 1]) + B[:, 0] * (C[:, 1] - A[:, 1]) + C[:, 0] * (A[:, 1] - B[:, 1]))
        ok = np.abs(d) > 1e-7; A, B, C, d = A[ok], B[ok], C[ok], d[ok]
        a2, b2, c2 = (A ** 2).sum(1), (B ** 2).sum(1), (C ** 2).sum(1)
        ux = (a2 * (B[:, 1] - C[:, 1]) + b2 * (C[:, 1] - A[:, 1]) + c2 * (A[:, 1] - B[:, 1])) / d
        uy = (a2 * (C[:, 0] - B[:, 0]) + b2 * (A[:, 0] - C[:, 0]) + c2 * (B[:, 0] - A[:, 0])) / d
        inside = (uy >= 0) & (uy < Ht) & (ux >= 0) & (ux < w)
        radius = float(np.sqrt((ux[inside] - A[inside, 0]) ** 2 + (uy[inside] - A[inside, 1]) ** 2).max())
    except Exception as e:
        radius = float("nan")
    rho = ties / ASPECT                                    # header centres per square quarter
    hexr = math.sqrt(2 / (3 * math.sqrt(3) * rho))        # covering radius of the hexagonal lattice of that density
    return dict(share=float(share), ties=float(ties), run=run, endless=endless / w, radius=radius, eff=hexr / radius, ncourse=len(set(cs)))

if __name__ == "__main__":
    out = sys.argv[1]; plan = [tuple(int(v) for v in a.split(":")) for a in sys.argv[2:]]
    found = {}; t0 = time.time()
    for h, Wmax in plan:
        for w in range(2, Wmax + 1, 2):
            M = course_masks(w); comp = {m: [n for n in M if not (m & n)] for m in M}; n0 = len(found); raw = 0
            def extend(seq):
                global raw
                if len(seq) == h:
                    for s in range(w):
                        if not (seq[-1] & rot(seq[0], s, w)):
                            raw += 1; k = canon(w, seq, s)
                            if k not in found: found[k] = None
                    return
                for n in comp[seq[-1]]: extend(seq + [n])
            for m in M: extend([m])
            print(f"h={h} w={w}: {raw} stacks, {len(found) - n0} new bonds (total {len(found)})  {time.time() - t0:.0f} s", flush=True)
    for k in found: found[k] = measures(k)
    pickle.dump(found, open(out, "wb"))
    print(f"{len(found)} bonds written to {out}  {time.time() - t0:.0f} s")
