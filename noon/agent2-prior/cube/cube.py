"""An independent check of how a uniform cube floats, written from scratch for the audit (not from ~/float).
The energy of a floating body is M g (z_G - z_B): the centre of gravity's height above the centre of buoyancy. With the cube's centre at
the origin and 'down' along -n, the submerged part is the fraction rho of the cube lowest along n; the energy per unit is
E(n) = -(integral over the submerged part of x.n dV).  The cube is sampled on a grid of K^3 midpoints.
usage: python -I cube.py K"""
import sys, numpy as np
K = int(sys.argv[1]); g = (np.arange(K) + 0.5) / K - 0.5; X = np.stack(np.meshgrid(g, g, g, indexing='ij'), -1).reshape(-1, 3); N = len(X)
def energy(n, rho):
    p = X @ n; k = int(round(rho * N)); part = np.partition(p, k)[:k]; return -part.sum() / N
def best(rho, M=40):
    out = []
    for i in range(M + 1):                       # directions over one 48th of the sphere and a little more: n = (a, b, 1) with 0 <= a <= b <= 1
        for j in range(i, M + 1):
            n = np.array([i / M, j / M, 1.0]); n /= np.linalg.norm(n); out.append((energy(n, rho), i / M, j / M))
    return sorted(out)
print(f"the cube sampled at {K}^3 points; attitudes n = (a, b, 1) on a grid of 41 values of a and b; differences below about 0.00001 are the sampling's noise")
for rho in (0.15, 0.2, 0.22, 0.25, 0.3, 0.4, 0.5):
    b = best(rho); face = energy(np.array([0, 0, 1.0]), rho); edge = energy(np.array([0, 1, 1.0]) / 2 ** 0.5, rho); corner = energy(np.array([1, 1, 1.0]) / 3 ** 0.5, rho)
    print(f"density {rho}: face up {face:.6f}; edge up {edge:.6f}; corner up {corner:.6f}; lowest on the grid of directions {b[0][0]:.6f} at n proportional to ({b[0][1]:.3f}, {b[0][2]:.3f}, 1); next {b[1][0]:.6f} at ({b[1][1]:.3f}, {b[1][2]:.3f}, 1)", flush=True)
