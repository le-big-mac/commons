"""The length of one lap's displacement when the turtle does come home: it is not the square root of q then.
usage: python -I extras3.py > extras3.out      (numpy)"""
import math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inspi import predicted, corners

if __name__ == '__main__':
    for inc, A in ((135, 22), (180, 89), (180, 179), (20, 2), (7, 0), (45, 22)):
        q, T, n = predicted(inc, A); B = abs(corners(inc, A, q)[-1])
        print(f"INC {inc}, ANGLE {A}: lap of {q}, T = {T}; one lap ends {B:.4f} steps from its start; the square root of {q} is {math.sqrt(q):.4f}")
    # why the widest is not the turtle with the smallest T: the circle the lap ends lie on, and how far the corners reach outside it
    for inc, A in ((135, 22), (45, 22), (180, 89)):
        q, T, n = predicted(inc, A); pts = corners(inc, A, n)[:-1]; ends = pts[::q]; c = ends.mean(); R = abs(ends[0] - c)
        spread = np.abs(np.abs(ends - c) - R).max(); far = np.abs(pts - c).max()
        wid = float(np.abs(pts[:, None] - pts[None, :]).max())
        print(f"INC {inc}, ANGLE {A}: the {len(ends)} lap ends lie on a circle of radius {R:.4f} (to {spread:.1e}); the farthest corner is {far:.4f} from its middle, {far - R:.4f} outside it; width {wid:.4f}, twice the farthest {2 * far:.4f}")
    worst = 0.0; lo = (9e9, None); hi = (0.0, None)
    for inc in range(1, 360):
        q = 360 // math.gcd(inc, 360); sq = 0.0
        for A in range(360):
            b = abs(corners(inc, A, q)[-1]); sq += b * b
            r = b / math.sqrt(q)
            if r > hi[0]: hi = (r, (inc, A, q, b))
        worst = max(worst, abs(sq / 360 - q))
    print(f"for each amount, the mean of the square of that length over the 360 whole-degree first turns is q: largest departure {worst:.1e}")
    print(f"the longest lap displacement in proportion to the square root of q: {hi[0]:.4f} times (INC {hi[1][0]}, ANGLE {hi[1][1]}: lap of {hi[1][2]}, {hi[1][3]:.4f} steps)")
    ties = [(inc, A) for inc in range(1, 360) for A in range(360) if abs(abs(corners(inc, A, 360 // math.gcd(inc, 360))[-1]) / math.sqrt(360 // math.gcd(inc, 360)) - hi[0]) < 1e-9]
    print(f"   reached by {len(ties)} pairs: " + "; ".join(f"INC {i} ANGLE {a}" for i, a in ties))
