"""Side check: the checker's UT of full moons (JPL tables, catalogue Delta T) against the first column of Jones (2020), Table 1
(UT of oppositions 'computed by modern theory', Alcyone; typed from page.txt lines 442-459), and against Carman and Evans's 13:21 UT
for the full moon of 12 May 205 BC (paper.txt 3351)."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, own
full, new = own.syz('then')
cat = own.catalogue(-299, 0); cj = np.array([r['jd'] for r in cat]); cd = np.array([r['dt'] for r in cat])
J = {2: '4:26', 8: '7:42', 14: '5:16', 20: '22:33', 26: '10:36', 32: '8:20', 37: '15:11', 43: '15:29', 49: '8:15', 55: '16:25', 61: '22:47', 67: '0:10', 73: '6:45', 79: '14:24', 84: '13:43', 90: '22:20', 96: '16:36', 102: '10:19'}
d = []
for cell, s in J.items():
    t = full[cell - 1]; ut = ((t - np.interp(t, cj, cd) / 86400 + 0.5) % 1) * 24
    h, m = s.split(':'); j = int(h) + int(m) / 60
    x = ((ut - j + 12) % 24 - 12) * 60; d.append(x)
    print(f'cell {cell:3d}: mine {int(ut):2d}:{int(round((ut % 1) * 60)):02d} UT, Jones {s}, mine - Jones {x:+.0f} min')
d = np.array(d); print(f'mean {d.mean():+.1f} min, sd {d.std():.1f}; in longitude {d.mean() / 4:+.1f} deg')
t = full[0]; ut = ((t - np.interp(t, cj, cd) / 86400 + 0.5) % 1) * 24
print(f'full moon of 12 May 205 BC: mine {int(ut)}:{int((ut % 1) * 60):02d} UT (Delta T {np.interp(t, cj, cd):.0f} s); Carman and Evans quote 13:21 UT from Espenak\'s catalogue of phases')
