# The figure clock-five-marks.png against my own computation (second pass).
# 1. For d = 12, 6, 4, 3, 2: the spots where the five weights land (hour x lands x/d of a turn on), how many
#    on each, and the centre of gravity, in exact arithmetic where possible; balance by exact division too.
# 2. The picture drawn again from clock_fig.py and compared with the PNG beside the page, pixel for pixel.
import sys, math, subprocess, collections
from fractions import Fraction
from polylib import balances_exact
MARKS = [0, 6, 1, 5, 9]
for d in (12, 6, 4, 3, 2):
    spots = collections.Counter(x % d for x in MARKS)
    # clockwise from the top (as drawn) and counter-clockwise from the right (as e^{2 pi i x/d}): same verdict
    gx = sum(math.sin(2 * math.pi * x / d) for x in MARKS) / 5; gy = sum(math.cos(2 * math.pi * x / d) for x in MARKS) / 5
    hx = sum(math.cos(2 * math.pi * x / d) for x in MARKS) / 5; hy = sum(math.sin(2 * math.pi * x / d) for x in MARKS) / 5
    turns = {s: str(Fraction(s, d)) for s in sorted(spots)}
    print(f"d = {d}: weights on spots (in turns from the start) " + ", ".join(f"{turns[s]}: {spots[s]}" for s in sorted(spots))
          + f"; centre of gravity drawn clockwise from the top ({gx:+.3f}, {gy:+.3f}), distance from centre {math.hypot(gx, gy):.3f};"
          + f" the other way round ({hx:+.3f}, {hy:+.3f}), distance {math.hypot(hx, hy):.3f};"
          + f" exact division: {'balances' if balances_exact(MARKS, 12, d) else 'does not balance'}")
if len(sys.argv) > 2:
    import numpy as np
    from PIL import Image
    a = np.asarray(Image.open(sys.argv[1]).convert('RGBA')); b = np.asarray(Image.open(sys.argv[2]).convert('RGBA'))
    print("picture drawn again:", a.shape, "; the PNG beside the page:", b.shape, "; pixels that differ:", int((a != b).any(axis=-1).sum()) if a.shape == b.shape else "sizes differ")
