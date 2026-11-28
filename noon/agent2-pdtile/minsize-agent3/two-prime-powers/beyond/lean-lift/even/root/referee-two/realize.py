# How close do true shares come to the table bound c(m) + \hat E(m) and to 0.9487/sqrt(m) for even m?
# For each m the multiset is built recursively from the maximising split of my table: the classes of sizes
# (r1, r2, r3) modulo 3 are filled with the multisets built for r1, r2, r3 (one residue repeated when the table
# has no split).  The true share of signings bad at a power of 3 is then counted exactly by tree.py.
import sys, math, ast
from fractions import Fraction as F
from math import comb
import tree
E = {}; ARG = {}
for line in open("mytable3-1000.txt"):
    w = line.split(None, 2); E[int(w[0])] = int(w[1], 16); ARG[int(w[0])] = ast.literal_eval(w[2])
def build(m, depth):          # list of (residue, multiplicity) on Z_(3^depth-levels below)
    if ARG.get(m) is None or depth == 0: return {0: m}
    out = {}
    for t, r in enumerate(ARG[m]):
        for b, mu in build(r, depth - 1).items(): out[t + 3 * b] = out.get(t + 3 * b, 0) + mu
    return out
V = 6; best = (0, None); bestr = (0, None)
for m in range(2, int(sys.argv[1]) + 1, 2):
    items = build(m, V)
    mm, f0, x = tree.analyse(3, V, items); assert mm == m
    tot = f0 + x; tab = F(comb(m, m // 2) + E[m], 1 << m)
    assert tot <= tab
    r = float(tot) * math.sqrt(m)
    if r > best[0]: best = (r, m)
    if tot / tab > bestr[0] and m > 12: bestr = (tot / tab, m)
    if m <= 40 or m % 50 == 0: print(f"m = {m}: split {ARG[m]}; true share {float(tot):.6f} = {float(tot / tab):.5f} of c + E; sqrt(m) x true = {r:.6f}; sqrt(m) x (c + E) = {float(tab) * math.sqrt(m):.6f}")
print(f"largest sqrt(m) x true share over even m <= {sys.argv[1]}: {best[0]:.6f} at m = {best[1]} (claimed 0.9487; ratio {best[0] / 0.9487:.4f}); largest true/(c+E) for m > 12: {float(bestr[0]):.5f} at m = {bestr[1]}")
