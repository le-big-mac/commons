"""How the number of pairs depends on the grid.  usage: python -I resolution.py pairs.npz pairs-pres.npz COARSEDIR"""
import sys
import numpy as np
main = {'slp': np.load(sys.argv[1])['counts'], 'pres': np.load(sys.argv[2])['counts']}
print("grid (degrees) | sea-level pressure: mean, median, share of times with exactly 1 pair, even counts | surface pressure: the same")
tot_even = tot = 0
for k in (1, 2, 3, 4, 6, 8, 12):
    row = [f"{2.5 * k:5.1f}"]
    for pv in ('slp', 'pres'):
        c = main[pv] if k == 1 else np.load(f"{sys.argv[3]}/{pv}-{k}.npz")['counts']
        tot_even += int((c % 2 == 0).sum())
        tot += len(c)
        row.append(f"{c.mean():6.1f} {np.median(c):4.0f} {100 * (c == 1).mean():5.1f}% {int((c % 2 == 0).sum()):2d}")
    print(" | ".join(row))
print(f"fields examined in all: {tot}; with an even number of pairs: {tot_even}")
a, b = np.polyfit(np.log([2.5 * k for k in (1, 2, 3, 4, 6, 8, 12)]),
                  np.log([main['slp'].mean()] + [np.load(f"{sys.argv[3]}/slp-{k}.npz")['counts'].mean() for k in (2, 3, 4, 6, 8, 12)]), 1)
print(f"sea-level pressure: mean count is roughly proportional to (grid step)^{a:.2f}")
ks = (12, 8, 6, 4, 3, 2, 1)
means = {k: (main['slp'].mean() if k == 1 else np.load(f"{sys.argv[3]}/slp-{k}.npz")['counts'].mean()) for k in ks}
print("sea-level pressure, local exponent between neighbouring grids:",
      ", ".join(f"{2.5 * a:g} -> {2.5 * b:g} degrees: {np.log(means[b] / means[a]) / np.log(a / b):.2f}" for a, b in zip(ks[:-1], ks[1:])))
