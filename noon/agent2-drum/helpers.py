"""Helpers shared by after.py and after2.py: finite-difference modes for any radial load, and the measures of closeness to harmonic."""
import sys, json, math
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import minimize
import drum
NINE, TARGET, NEXT = drum.NINE, np.array(drum.TARGET, float), drum.NEXT; 
def fd_modes(rho_of_r, which=NINE, N=2000):
    h = 1.0 / N; r = (np.arange(N) + 0.5) * h; rho = rho_of_r(r); re = np.arange(N + 1) * h; need = {}
    for m, n in which: need[m] = max(need.get(m, 0), n)
    ev = {}
    for m, cnt in need.items():
        d = (re[:-1] + re[1:]) / (h * h * r) + m * m / r ** 2; d[-1] += re[-1] / (h * h * r[-1]); off = -re[1:-1] / (h * h); sc = np.sqrt(r * rho)
        ev[m] = np.sqrt(eigh_tridiagonal(d * r / sc ** 2, off / (sc[:-1] * sc[1:]), select='i', select_range=(0, cnt - 1))[0])
    return np.array([ev[m][n - 1] for m, n in which])
disc = lambda s, k: (lambda r: np.where(r < k, s, 1.0)); graded = lambda s, k: (lambda r: np.where(r < k, 1 + (s - 1) * (1 - (r / k) ** 2), 1.0))
tied = lambda w: float(np.max(np.abs(w[1:] / w[0] / TARGET[1:] - 1)))
def free(w): x = w / TARGET; return float((x.max() - x.min()) / (x.max() + x.min()))
ls_tied = lambda w: float(np.sqrt(np.mean((w[1:] / w[0] / TARGET[1:] - 1) ** 2))); ls_free = lambda w: float(np.std(np.log(w / TARGET)))
