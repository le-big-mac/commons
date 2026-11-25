# Finer rays on plates III and IV: where does the vertical hatching (third ring) end?
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from texture import load, tensor, classify, ray
a = load(sys.argv[1]); c = classify(*tensor(a)); PX = 19.78; step = 2
def wrun(s):
    # longest run of 'W' between 3 and 20 miles out, in miles (start, end)
    best = (0, 0, 0); i = 0
    while i < len(s):
        if s[i] == 'W':
            j = i
            while j < len(s) and s[j] == 'W': j += 1
            if j - i > best[0] and i * step / PX > 3: best = (j - i, i, j)
            i = j
        else: i += 1
    return best[1] * step / PX, best[2] * step / PX
print('plate III (town price = 1.5 - 0.15*deg/30):')
for deg in (34, 56, 64, 86, 94, 98, 102, 106, 110, 114, 118):
    s = ray(c, 776, 1329, -deg, 500, step); w = wrun(s)
    print('  %3d deg = %.3f Taler: vertical hatch %.1f to %.1f miles (%.1f wide)' % (deg, 1.5 - 0.15 * deg / 30, w[0], w[1], w[1] - w[0]))
print('plate IV (yield = 10 - deg/30):')
for deg in (34, 56, 64, 68, 72, 76, 80, 84, 86):
    s = ray(c, 797, 1329, deg, 500, step); w = wrun(s)
    print('  %3d deg = %.2f Koerner: vertical hatch %.1f to %.1f miles (%.1f wide)' % (deg, 10 - deg / 30, w[0], w[1], w[1] - w[0]))
