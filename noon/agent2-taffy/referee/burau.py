# Referee: unreduced Burau at t=-1, both orientation conventions, exact char polys.
import sympy as sp, numpy as np
from words import DEVICES, parse

def bmat(n, i, cw, conv):
    t = sp.Integer(-1)
    M = sp.eye(n)
    blk = sp.Matrix([[1 - t, t], [1, 0]])
    pos = (cw == conv)   # conv True: s_i = sigma_i ; False: s_i = sigma_i^-1
    if not pos:
        blk = blk.inv()
    M[i - 1:i + 1, i - 1:i + 1] = blk
    return M

x = sp.symbols('x')
for n, dev in DEVICES:
    for conv in (True, False):
        P = sp.eye(n)
        for (i, cw) in parse(dev):
            P = P * bmat(n, i, cw, conv)
        cp = sp.factor(P.charpoly(x).as_expr())
        ev = np.linalg.eigvals(np.array(P.tolist(), dtype=float))
        print(f"n={n} {dev} conv={'s=sigma' if conv else 's=sigma^-1'}: charpoly {cp}; max|eig|={max(abs(ev)):.6f}; "
              f"eigs={np.round(ev,5)}")
