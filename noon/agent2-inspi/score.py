"""Scoring the sealed lines S5 and S6 completely, and trying the 1981 paper's sentence on my turtle.
usage: python -I score.py > score.out        (numpy; imports inspi.py, whose doing part is guarded)

The sealed run measured only the 400 pairs that reach furthest from (or stay nearest to) their start.  A figure's
width (the greatest distance between two corners) is at least its reach and at most twice its reach, so "the 400
furthest" does not settle which figure is widest: here every pair whose reach allows it to matter is measured."""
import math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))      # -I leaves the script's own folder off the path
from inspi import walk_all, predicted, corners, width


def segments(inc, A, n):
    """the distinct sides among the first n steps, each side as an unordered pair of corners rounded to 1e-6"""
    pts = corners(inc, A, n); seen = set()
    for a, b in zip(pts[:-1], pts[1:]):
        ka = (round(a.real, 6), round(a.imag, 6)); kb = (round(b.real, 6), round(b.imag, 6))
        seen.add((min(ka, kb), max(ka, kb)))
    return len(seen)


if __name__ == '__main__':
    first, reach, end = walk_all()
    closed = [(reach[inc, A], inc, A) for inc in range(1, 360) for A in range(360) if first[inc, A] > 0]
    print(f"closed pairs: {len(closed)}; pairs that never come home in 720 steps: {359 * 360 - len(closed)}")

    # ---- S5, completely: measure in order of reach, furthest first, until twice the reach is below the best width
    closed.sort(reverse=True); best = 0.0; measured = []
    for r, inc, A in closed:
        if 2 * r < best - 1e-9: break
        w = width(corners(inc, A, first[inc, A])); measured.append((w, inc, A)); best = max(best, w)
    measured.sort(reverse=True)
    top = [m for m in measured if m[0] > best - 1e-6]
    print(f"S5: {len(measured)} pairs measured (every pair whose reach is at least half the best width); the widest is {best:.6f} steps across, reached by {len(top)} pairs:")
    print("    " + "; ".join(f"INC {inc} ANGLE {A}" for w, inc, A in sorted(top, key=lambda t: (t[1], t[2]))))
    print(f"    their widths agree to {max(t[0] for t in top) - min(t[0] for t in top):.1e}; steps to close: {sorted(set(int(first[inc, A]) for w, inc, A in top))}; T: {sorted(set(predicted(inc, A)[1] for w, inc, A in top))}")
    nxt = [m for m in measured if m[0] <= best - 1e-6]
    seen = [];
    for w, inc, A in nxt:
        if not seen or abs(seen[-1][0] - w) > 1e-6: seen.append((w, inc, A))
        if len(seen) == 4: break
    print("    the next widths down: " + "; ".join(f"{w:.4f} (INC {inc}, ANGLE {A}, T = {predicted(inc, A)[1]}, {first[inc, A]} steps)" for w, inc, A in seen))
    for A in (89, 91, 269, 271):
        w = width(corners(180, A, first[180, A]))
        rank = 1 + sum(1 for m in measured if m[0] > w + 1e-6)
        print(f"    the sealed guess, INC 180 ANGLE {A}: {w:.4f} steps across, closing after {first[180, A]} steps; {rank - 1} pairs are wider")

    # ---- S6, completely: measure in order of reach, nearest first, until the reach is above the best (smallest) width
    closed.sort(); best = 1e9; small = []
    for r, inc, A in closed:
        if r > best + 1e-9: break
        w = width(corners(inc, A, first[inc, A])); small.append((w, r, inc, A)); best = min(best, w)
    small.sort()
    low = [s for s in small if s[0] < best + 1e-6]
    print(f"S6: {len(small)} pairs measured (every pair whose reach is at most the best width); the narrowest is {best:.6f} steps across, reached by {len(low)} pairs:")
    print("    " + "; ".join(f"INC {inc} ANGLE {A} ({first[inc, A]} steps)" for w, r, inc, A in low))
    print(f"    2 cos 15 degrees = {2 * math.cos(math.radians(15)):.6f}")
    within = [(inc, A) for r, inc, A in closed if r <= 1 + 1e-9]
    for inc, A in within:
        pts = corners(inc, A, first[inc, A])
        print(f"    every corner within 1 step of the start: INC {inc} ANGLE {A}, {first[inc, A]} steps, corners {[(round(float(z.real), 6), round(float(z.imag), 6)) for z in pts]}, width {width(pts):.6f}")
    # a figure under 2 steps across reaches less than 2 from its start: measure every such pair (the first version of this
    # script counted only among the pairs measured above, whose reach is at most the best width, and printed 12; the referee found 20)
    under = [(width(corners(inc, A, first[inc, A])), inc, A) for r, inc, A in closed if r < 2 - 1e-9]
    two = sorted(t for t in under if t[0] < 2 - 1e-9)
    print(f"    closed pairs reaching less than 2 steps from their start: {len(under)}, all measured; less than 2 steps across: {len(two)}; their INCs: {sorted(set(inc for w, inc, A in two))}; their ANGLEs: {sorted(A for w, inc, A in two)}")
    print(f"    their widths: " + "; ".join(f"{w:.4f} x{sum(1 for t in two if abs(t[0] - w) < 1e-9)}" for w in sorted(set(round(t[0], 9) for t in two))))
    print(f"    closed figures exactly 2 steps across (to 1e-9) among those measured: " + "; ".join(f"INC {inc} ANGLE {A}" for w, r, inc, A in small if abs(w - 2) < 1e-9))
    print(f"    narrowest closed figure with INC other than 180, among those measured: " + "; ".join(f"{w:.4f} (INC {inc}, ANGLE {A})" for w, r, inc, A in [s for s in small if s[2] != 180][:3]))

    # ---- S2's last clause, on every pair (the sealed run tried 8): each lap is the lap before turned through T about one point,
    # so turning the closed figure through T carries corner k onto corner k + q; and has any figure more matching parts than v?
    from scipy.spatial import cKDTree
    sym = notsym = 0; worst = 0.0; more = []; tried = 0; ctl = {2: 0, 3: 0, 5: 0}; ctl_hit = {2: 0, 3: 0, 5: 0}
    for r, inc, A in closed:
        q, T, n = predicted(inc, A); pts = corners(inc, A, n)[:-1]; c = pts.mean()
        dep = float(np.abs(np.roll(pts, -q) - c - (pts - c) * np.exp(-2j * np.pi * T / 360)).max()); worst = max(worst, dep)
        if dep < 1e-9: sym += 1
        else: notsym += 1
        v = 360 // math.gcd(T, 360); tree = cKDTree(np.c_[pts.real, pts.imag]); tried += 1
        for ell in (2, 3, 5):
            rot = c + (pts - c) * np.exp(2j * np.pi / (v * ell)); d, _ = tree.query(np.c_[rot.real, rot.imag])
            if d.max() < 1e-7: more.append((inc, A, v, ell, n)); break
        if tried % 7 == 0:          # the control: told that v is a half, a third or a fifth of what it is, the same loop must find that further division, and at that step
            for part in (2, 3, 5):
                if v % part: continue
                vv = v // part; found = None
                for ell in (2, 3, 5):
                    rot = c + (pts - c) * np.exp(2j * np.pi / (vv * ell)); d, _ = tree.query(np.c_[rot.real, rot.imag])
                    if d.max() < 1e-7: found = ell; break
                ctl[part] += 1; ctl_hit[part] += (found == part)
    print(f"S2, the symmetry, on every pair that comes home: turning the figure through T about the middle of its corners carries corner k onto corner k + q in {sym} of {sym + notsym} (largest departure {worst:.1e})")
    print(f"    figures whose corners also fit themselves when turned through a half, a third or a fifth of 1/v of a turn (more matching parts than v): {len(more)} of {tried}" + ("; the first few (INC, ANGLE, v, the further division, steps): " + "; ".join(str(m) for m in more[:10]) if more else ""))
    print("    control (every seventh figure): told that v is a half, a third or a fifth of its true value, the same loop finds just that further division in " + "; ".join(f"{ctl_hit[k]} of {ctl[k]} (1/{k})" for k in (2, 3, 5)))
    if more:
        from collections import Counter
        print("    by INC: " + "; ".join(f"INC {i}: {c}" for i, c in sorted(Counter(m[0] for m in more).items())[:40]))

    # ---- the 1981 sentence (Dekking and Mendes France, Example 4.2), tried on my turtle
    # their curve for u_n = n^2 p/q is INSPI with ANGLE = 360 p/q and INC = 720 p/q; whole degrees: q a divisor of 360
    print("the 1981 sentence: for u_n = n^2 p/q the curve is 'either a bounded polygon with q/2 sides (iff q = 2 mod 4), or an infinite polygon'")
    rows = bounded_ok = sides_ok = 0; notes = []
    for q in [d for d in range(2, 361) if 360 % d == 0]:
        for p in range(1, q):
            if math.gcd(p, q) != 1: continue
            A = (360 * p // q) % 360; inc = (720 * p // q) % 360
            if inc == 0: continue                       # q = 2: the turtle only goes back and forth; not in my range of INC
            rows += 1; home = int(first[inc, A]); says_bounded = (q % 4 == 2)
            bounded_ok += (home > 0) == says_bounded
            if home > 0:
                s = segments(inc, A, home); sides_ok += (s == q // 2)
                if s != q // 2 and len(notes) < 6: notes.append(f"q = {q}, p = {p}: {s} distinct sides in {home} steps")
    nb = sum(1 for q in [d for d in range(3, 361) if 360 % d == 0] for p in range(1, q) if math.gcd(p, q) == 1 and q % 4 == 2)
    print(f"    {rows} whole-degree cases (q from 3 to 360): bounded exactly when q = 2 mod 4 in {bounded_ok}; of the {nb} bounded ones, the number of distinct sides is q/2 in {sides_ok}" + ("; otherwise: " + "; ".join(notes) if notes else ""))
