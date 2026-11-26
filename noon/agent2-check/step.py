"""The 4-day run beside the 8-day run, row by row over the span both cover (26 November 2026).
usage: python -I step.py slow_dt4_seed1.txt slow_dt8_seed1.txt slow_dt8_seed2.txt > step.out      (numpy)
For each inner planet: the difference in log10 of the change in its eccentricity vector between the 4-day and the
8-day run, at every row both have; and, as a yardstick, the same between the two 8-day runs, which follow one
trajectory from two starting perturbations (their mean difference taken off)."""
import sys
sys.dont_write_bytecode = True
import numpy as np
NAMES = ['Mercury', 'Venus', 'Earth-Moon', 'Mars']

def load(f):
    return np.array([[float(x) for x in l.split()[:11]] for l in open(f) if not l.startswith('#') and len(l.split()) >= 11])

if __name__ == '__main__':
    d4, d8, d8b = (load(f) for f in sys.argv[1:4])
    n = min(len(d4), len(d8), len(d8b))
    assert np.allclose(d4[:n, 0], d8[:n, 0]) and np.allclose(d4[:n, 0], d8b[:n, 0])
    print(f"{n} rows, 0.1 to {d4[n - 1, 0]:.1f} Myr")
    a = np.abs(d4[:n, 3:7] - d8[:n, 3:7])
    print("4-day against 8-day, same starting perturbation, |difference| in log10: "
          + ", ".join(f"{nm} median {np.median(a[:, i]):.2f}, largest {a[:, i].max():.2f}" for i, nm in enumerate(NAMES)))
    print("  share of rows within 0.3: " + ", ".join(f"{nm} {100 * (a[:, i] <= 0.3).mean():.0f}%" for i, nm in enumerate(NAMES)))
    t = d4[:n, 0]
    for x in (5, 10, 15, 20, 25, 30, 33):
        k = int(np.argmin(np.abs(t - x)))
        print(f"  at {t[k]:.0f} Myr: " + ", ".join(f"{nm} {d4[k, 3 + i]:.2f} / {d8[k, 3 + i]:.2f}" for i, nm in enumerate(NAMES)) + f"; largest gap {a[k].max():.2f}")
    b = d8b[:n, 3:7] - d8[:n, 3:7]; b = np.abs(b - b.mean(0))
    print("the two 8-day runs against each other over the same rows, mean difference removed: "
          + ", ".join(f"{nm} median {np.median(b[:, i]):.2f}, largest {b[:, i].max():.2f}" for i, nm in enumerate(NAMES)))
