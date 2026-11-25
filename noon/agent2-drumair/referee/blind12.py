import numpy as np, sys
from scipy.special import jn_zeros
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fem import *

print("CREF (B / w11^2 on the reference drum) =", CREF)
# sanity: vacuum plain skin against Bessel zeros
w = rich(400, disc_rho(0, 0.5), B=0.0)
print("sanity plain skin, vacuum: (0,n)", [w[(0, j)] for j in (1, 2, 3)], "bessel", jn_zeros(0, 3))
print("   (1,1),(1,2)", w[(1, 1)], w[(1, 2)], jn_zeros(1, 2), " (2,1)", w[(2, 1)], jn_zeros(2, 1), "(4,1)", w[(4, 1)], jn_zeros(4, 1))
# 1
w1 = rich(400, disc_rho(0, 0.5), B=1.0)
print("Q1 plain skin, B=1: raised by", [w1[(0, j)] / w[(0, j)] - 1 for j in (1, 2, 3)], " w:", [w1[(0, j)] for j in (1, 2, 3)])
# 2
d = disc_rho(9.77, 0.4)
wv = rich(400, d, B=0.0)
print("Q2 1954 disc: w11 =", wv[(1, 1)], " B_ref =", CREF * wv[(1, 1)] ** 2)
print("   vacuum:", report(wv)["place"], " missA", report(wv)["missA"])
for nm, f in (("reference", 1.0), ("volume doubled", 0.5), ("volume halved", 2.0)):
    ww = rich(400, d, B=None, cref=CREF * f)
    r = report(ww)
    print("   %-15s B = %.4f  place = %.4f   w01 = %.5f" % (nm, r["B"], r["place"], ww[(0, 1)]))
