# Plate II (lower half of n402.jpg): hatch classes along horizontal rows at given miles below the town.
import sys
import numpy as np
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texture import load, tensor, classify, runs
a = load(sys.argv[1]); c = classify(*tensor(a))
PX = 20.04; cx, cy = 773.5, 1342.0
for mi in (2, 4, 6, 8, 9, 10, 11, 12, 16, 18, 20, 24, 28, 32, 36, 38):
    y = int(round(cy + mi * PX)); x0 = max(0, int(cx - 40 * PX)); x1 = min(c.shape[1] - 1, int(cx + 40 * PX))
    s = ''.join(c[y, x0:x1:2])
    res = []; i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]: j += 1
        if j - i >= 4: res.append((s[i], (x0 + 2 * i - cx) / PX, (x0 + 2 * j - cx) / PX))
        i = j
    print('%2d mi down: ' % mi + ' '.join('%s:%.1f..%.1f' % r for r in res))
