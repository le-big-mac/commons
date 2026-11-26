"""The cheap estimate (the Burau matrix) at every setting on the unit circle.   Added 26 November 2026.
usage: python -I burau.py > burau.out        (numpy; taffy.py beside it)

taffy.py takes the Burau matrix at the one setting t = -1.  The estimate as the field states it is the largest
eigenvalue, in size, over every t of size one.  This scans t = exp(2 pi i x) for x = 0, 0.001, ..., 0.999 and
prints, for each device, the value at -1, the largest value and where it is, and on how much of the circle the
value is within 0.02 of 1 (the matrix used here always has an eigenvalue 1, so 1 means "nothing found").
"""
import os, sys, cmath
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import taffy


def burau(moves, n, t):
    P = np.eye(n, dtype=complex)
    for kind, i in moves:
        B = np.eye(n, dtype=complex); B[i - 1:i + 1, i - 1:i + 1] = [[1 - t, t], [1, 0]]
        P = P @ (B if kind == 's' else np.linalg.inv(B))
    return float(np.abs(np.linalg.eigvals(P)).max())


def arcs(flags, step):
    """runs of True round the circle, as (from, to) in turns"""
    n = len(flags); out = []; k = 0
    if all(flags): return [(0.0, 1.0)]
    while flags[k % n] and k < n: k += 1                    # start at a False
    start = None
    for j in range(k, k + n + 1):
        f = flags[j % n]
        if f and start is None: start = j
        if not f and start is not None: out.append(((start % n) * step, ((j - 1) % n) * step)); start = None
    return out


if __name__ == '__main__':
    N = 1000
    for name, (n, moves) in taffy.DEVICES.items():
        g, _ = taffy.growth(moves, n)
        v = [burau(moves, n, cmath.exp(2j * cmath.pi * k / N)) for k in range(N)]
        best = max(range(N), key=lambda k: v[k]); near = [abs(x - 1) <= 0.02 for x in v]
        print(f"{name}: {n} rods, {' '.join(k + '_' + str(i) for k, i in moves)}: growth {g:.4f}; estimate at -1: {v[N // 2]:.4f}; "
              f"largest on the circle {v[best]:.4f} at {best / N:.3f} of a turn ({100 * v[best] / g:.1f}% of the growth); "
              f"within 0.02 of 1 on {100 * sum(near) / N:.1f}% of the circle")
        if name == 'T4':
            print("   T4, where the estimate is within 0.02 of 1 (turns): " + ", ".join(f"{a:.3f} to {b:.3f}" for a, b in arcs(near, 1 / N)))
            print("   T4, at every twentieth of a turn: " + ", ".join(f"{v[k]:.3f}" for k in range(0, N, N // 20)))
