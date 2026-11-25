"""The modes of the best ringed loads, with 8,000 cells: the nine ratios, their distance from the harmonics in cents, and the next three modes.
usage: python exact7.py chain-free-down.json chain-free-up.json     (unregistered)"""
import sys, json, math
import numpy as np
src = open(__file__.replace("exact7.py", "exact.py")).read(); ns = {}; exec(src[:src.index("rng = np.random.default_rng(40)")], ns)
NINE, NEXT, TARGET, EDGE, AREA = ns['NINE'], ns['NEXT'], ns['TARGET'], ns['EDGE'], ns['AREA']; rows = {}
for f in sys.argv[1:3]:
    for r in json.load(open(f)):
        if r['weight'] not in rows or r['miss'] < rows[r['weight']]['miss']: rows[r['weight']] = r
for M in (1.43, 2.79, 12.0):
    a = np.array(rows[M]['a']); W = ns['solve'](a, 8000, NINE + NEXT, grad=False); r = W / W[0]; c = [1200 * math.log2(r[i] / TARGET[i]) for i in range(1, 9)]
    print(f"added mass {M:g}: largest miss {100 * rows[M]['miss']:.4f}% with 2,000 cells, {100 * np.abs(r[1:9] / TARGET[1:] - 1).max():.4f}% with 8,000 ({max(abs(x) for x in c):.1f} cents)")
    print("   ratios: " + ", ".join(f"{x:.4f}" for x in r[:9]) + "; the next three, (5,1), (3,2), (1,3): " + ", ".join(f"{x:.3f}" for x in r[9:]))
    print("   cents from the harmonic, modes 2 to 9: " + ", ".join(f"{x:+.1f}" for x in c) + f"; (2,1) and (0,2) are {abs(c[2] - c[1]):.1f} apart, (3,1) and (1,2) {abs(c[4] - c[3]):.1f}, and the three aimed at 5 span {max(c[5:8]) - min(c[5:8]):.1f}")
    print("   load by ring from the centre, in skins: " + " ".join(f"{x:.1f}" for x in a[:int(np.max(np.nonzero(a > 1e-6)[0])) + 1]) + f"; added mass {float(a @ AREA):.2f}; heaviest ring from {EDGE[int(np.argmax(a))]:.3f} to {EDGE[int(np.argmax(a)) + 1]:.3f}")
