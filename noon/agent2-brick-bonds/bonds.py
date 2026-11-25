"""Brick bonds of the one-brick wall: model, enumeration, measures.  (Noon = agent2, 21 November 2026)

Units: quarter-bricks along the wall.  A stretcher shows a face 4 long, a header a face 2 long (mortar ignored).
A course is a periodic sequence of stretchers and headers; its perpends (vertical joints) are a set J of integers
with consecutive gaps 2 or 4.  A bond is a doubly periodic stack of courses in which no perpend of a course lies
directly above a perpend of the course below (the rule that perpends are not contiguous across courses).
A bond is stored as (w, courses, s): horizontal period w, a list of h courses, each a frozenset of perpends
modulo w, and a shear s: course c + h is course c moved s to the right.

The wall is one brick (4 quarters) thick: a header goes through it, a stretcher has a second stretcher behind it,
and between the two there is a vertical joint in the plane of the wall (the collar joint).  Headers are the ties.
"""
import itertools, math
from functools import lru_cache

# ---------- courses ----------
@lru_cache(None)
def courses(w):
    """all courses of horizontal period w: frozensets of perpends modulo w (gaps 2 or 4, cyclically)"""
    assert w % 2 == 0
    n = w // 2; out = []
    for eps in (0, 1):
        for mask in range(1 << n):                        # mask = boundaries erased (interiors of stretchers)
            if n == 1 and mask: continue
            if any((mask >> k) & 1 and (mask >> ((k + 1) % n)) & 1 for k in range(n)): continue
            out.append(frozenset((eps + 2 * k) % w for k in range(n) if not (mask >> k) & 1))
    return out

def compatible(A, B):
    """no common perpend"""
    return not (A & B)

def shift(J, t, w): return frozenset((x + t) % w for x in J)
def mirror(J, w): return frozenset((-x) % w for x in J)

def bricks(J, w):
    """list of (start, length) of the bricks of a course, one period"""
    xs = sorted(J); out = []
    for i, x in enumerate(xs):
        nxt = xs[(i + 1) % len(xs)]; L = (nxt - x) % w or w
        out.append((x, L))
    return out

def valid_course(J, w):
    return len(J) > 0 and all(L in (2, 4) for _, L in bricks(J, w))

# ---------- a bond as a function on (course, x) ----------
class Bond:
    def __init__(self, w, cs, s=0, name=None):
        self.w, self.cs, self.h, self.s, self.name = w, [frozenset(c) for c in cs], len(cs), s % w, name
        assert all(valid_course(c, w) for c in self.cs), (w, cs)
        assert all(compatible(self.course(c), self.course(c + 1)) for c in range(self.h)), "perpends line up"
    def course(self, c):
        q, r = divmod(c, self.h)
        return shift(self.cs[r], q * self.s, self.w)
    def is_header(self, c, x):
        """is the quarter [x, x+1] of course c part of a header face?"""
        J = self.course(c); w = self.w; x %= w
        lo = next((x - d) % w for d in range(0, 4) if (x - d) % w in J)      # perpend at or left of x
        hi = next((x + d) % w for d in range(1, 5) if (x + d) % w in J)      # perpend right of x
        return ((hi - lo) % w or w) == 2
    # ----- canonical form: minimal periods, then least representative under translations and the two mirrors -----
    def canon(self):
        w, h = self.w, self.h
        H = h * w // math.gcd(self.s, w) if self.s else h                    # courses after which the stack repeats exactly
        C = [self.course(c) for c in range(H)]
        w0 = next(t for t in range(2, w + 1, 1) if w % t == 0 and all(shift(J, t, w) == J for J in C))
        C = [frozenset(x % w0 for x in J) for J in C]
        for h0 in range(1, H + 1):                                            # least vertical period, with a shear
            ts = [t for t in range(w0) if all(shift(C[c], t, w0) == C[(c + h0) % H] for c in range(H))] if H % h0 == 0 or True else []
            ts = [t for t in range(w0) if all(shift(C[c % H], t, w0) == C[(c + h0) % H] for c in range(H))]
            if ts: s0 = ts[0]; break
        best = None
        for flipv in (0, 1):
            for flipx in (0, 1):
                seq = C[::-1] if flipv else C
                if flipx: seq = [mirror(J, w0) for J in seq]
                sh = s0; 
                if flipv: sh = -sh
                if flipx: sh = -sh
                sh %= w0
                for r in range(len(seq)):
                    for a in range(w0):
                        rep = tuple(tuple(sorted(shift(seq[(r + c) % len(seq)], a, w0))) for c in range(h0))
                        key = (w0, h0, sh, rep)
                        if best is None or key < best: best = key
        return best
    # ----- measures -----
    def unrolled(self):
        w = self.w; H = self.h * w // math.gcd(self.s, w) if self.s else self.h
        return [[self.is_header(c, x) for x in range(w)] for c in range(H)]
    def header_fraction(self):
        U = self.unrolled(); return sum(map(sum, U)) / (len(U) * self.w)       # share of the face that is header
    def ties_per_area(self): return self.header_fraction() / 2                # headers per quarter-length per course
    def collar_run(self):
        """longest vertical run of the collar joint, in courses (math.inf if some vertical line never meets a header),
        and the share of the wall's length lying on such endless lines"""
        U = self.unrolled(); H = len(U); best = 0; endless = 0
        for x in range(self.w):
            col = [U[c][x] for c in range(H)]
            if not any(col): endless += 1; continue
            k = col.index(True); col = col[k:] + col[:k]; run = 0
            for v in col:
                run = 0 if v else run + 1; best = max(best, run)
        return (math.inf if endless else best), endless / self.w
    def header_centres(self, aspect=4 / 3):
        U = self.unrolled(); H = len(U); pts = []
        for c in range(H):
            for (x, L) in bricks(self.course(c), self.w):
                if L == 2: pts.append((x + 1.0, (c + 0.5) * aspect))
        return pts, self.w, H * aspect
    def tie_radius(self, aspect=4 / 3, step=0.125):
        """largest distance from a point of the wall to the nearest header centre (a course is `aspect` quarters high)"""
        import numpy as np
        from scipy.spatial import cKDTree
        pts, W, Ht = self.header_centres(aspect)
        if not pts: return math.inf
        P = np.array([(x + i * W, y + j * Ht) for (x, y) in pts for i in (-1, 0, 1) for j in (-1, 0, 1)])
        gx, gy = np.meshgrid(np.arange(0, W, step), np.arange(0, Ht, step))
        d, _ = cKDTree(P).query(np.c_[gx.ravel(), gy.ravel()])
        return float(d.max())

# ---------- the named bonds ----------
def S(w, off=0): return frozenset(range(off % 4, w, 4)) if w % 4 == 0 else None
def Hd(w, off=1): return frozenset(range(off % 2, w, 2))
def word(seq, off=0):
    """a course from a word like 'SSH': returns (period, perpends)"""
    x = off; J = []
    for ch in seq: J.append(x); x += 4 if ch == 'S' else 2
    w = x - off
    return w, frozenset(j % w for j in J)
def lattice_bond(seq, s, name=None):
    w, J = word(seq); return Bond(w, [J], s, name)
def named():
    out = []
    out.append(Bond(4, [S(4, 0)], 2, "stretcher (running) bond"))
    out.append(Bond(4, [S(4, 0)], 1, "raking stretcher bond (quarter rake)"))
    out.append(Bond(4, [S(4, 0), S(4, 1)], 0, "raking stretcher bond (zigzag)"))
    out.append(Bond(2, [Hd(2, 0)], 1, "header bond"))
    out.append(Bond(4, [S(4, 0), Hd(4, 1)], 0, "English bond"))
    out.append(Bond(4, [S(4, 0), Hd(4, 1)], 2, "English cross (Dutch) bond"))
    out.append(lattice_bond("SH", 3, "Flemish bond"))
    out.append(lattice_bond("SSH", 5, "monk bond"))
    out.append(lattice_bond("SSSH", 7, "Sussex bond (Flemish garden wall)"))
    out.append(Bond(4, [S(4, 0), S(4, 2), S(4, 0), Hd(4, 1)], 0, "English garden wall bond (3 : 1)"))
    out.append(Bond(4, [S(4, 0), S(4, 2), S(4, 0), S(4, 2), S(4, 0), Hd(4, 1)], 0, "Scottish bond (5 : 1)"))
    out.append(Bond(4, [S(4, 0), S(4, 2), S(4, 0), S(4, 2), S(4, 0), S(4, 2), Hd(4, 1)], 2, "American common bond (6 : 1)"))
    w, F = word("SH")
    out.append(Bond(12, [frozenset(x % 12 for x in list(F) + [j + 6 for j in F]), S(12, 3)], 0, "Flemish stretcher bond (1 : 1)"))
    return out

if __name__ == "__main__":
    print(f"{'bond':42s} {'w':>3s} {'h':>2s} {'s':>2s}  {'header share':>12s} {'ties/area':>9s} {'collar run':>10s} {'endless':>8s} {'tie radius':>10s}")
    for b in named():
        w0, h0, s0, _ = b.canon(); run, endless = b.collar_run()
        print(f"{b.name:42s} {w0:3d} {h0:2d} {s0:2d}  {b.header_fraction():12.4f} {b.ties_per_area():9.4f} {str(run):>10s} {endless:8.3f} {b.tie_radius():10.3f}")
    print("courses of period w:", {w: len(courses(w)) for w in range(2, 22, 2)})
