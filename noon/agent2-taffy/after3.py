"""After the referee: two of its controls redone with my code.   usage: python after3.py > after3.out
(a) the folding device's fourth-period growth in the fluid for other kernel widths; (b) stretching per exchange, per time step and per return of the rods."""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import taffy as TF
R = json.load(open('sheet.json'))
print("(b) three ways of counting: growth per exchange of two rods; per time step if disjoint pairs turn together (the list read round and round); logarithm of the growth per return of all rods to their own places")
STEPS = {'T1': 2, 'T2': 4, 'T3': 2, 'T4': 2, 'T5': 2, 'T6': 3}
for k, (n, moves) in TF.DEVICES.items():
    perm = list(range(n))
    for kind, i in moves: perm[i - 1], perm[i] = perm[i], perm[i - 1]
    order = 1; q = perm[:]
    while q != list(range(n)): q = [q[j] for j in perm]; order += 1
    g = R[k]['growth'] if k != 'T3' else 1.0
    print(f"   {k} {' '.join(a + str(b) for a, b in moves):12s}: per exchange x{g ** (1 / len(moves)):.3f}; per time step x{g ** (1 / STEPS[k]):.3f}; rods home after {order} period(s): {order * math.log(g):.3f}")
print("(a) the fluid for the folding device s1 s1 S2 S2, four periods, by kernel width (0.35 is the sealed one)", flush=True)
for sig in (0.25, 0.5):
    TF.SIG = sig; L, x = TF.flow(TF.DEVICES['T2'][1], 3, 4)
    print(f"   kernel {sig}: ratios {', '.join(f'{b / a:.3f}' for a, b in zip(L, L[1:]))}", flush=True)
