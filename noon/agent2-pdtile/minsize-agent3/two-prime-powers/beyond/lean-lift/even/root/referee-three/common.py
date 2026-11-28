"""Part F: numbers that result.md (three) and the neighbouring text (one) have in common, recomputed with the referee's code:
the counts of e by kappa (one's cnt(N), N = kappa + 1), the sum over the prime powers, and the K_same of the decorations
that the neighbouring text names on Z_9, Z_27, Z_135.   usage: common.py [big]"""
import sys, math
from fractions import Fraction as Fr
import psi as PSI
from extra import value_sets
P = PSI.pairs_upto(160)
tot = {}
for (q, s, pp, nc) in P:
    k = s + q - 1; tot[k] = tot.get(k, 0) + pp + nc
print("number of e with kappa = 2, 4, ..., 20 (the other text's cnt(N), N = 3, 5, ..., 21: 1, 3, 6, 8, 17, 47, 42, 97, 218, 260):", [tot[k] for k in range(2, 21, 2)])
print("sum over prime powers of 2^(1-kappa) (other text: 0.834228):", float(sum(Fr(pp, 2 ** (s + q - 2)) for (q, s, pp, nc) in P)))
print("sum over all e of 2^(1-kappa) (other text: between 1.191896 and 1.191951):", float(sum(Fr(pp + nc, 2 ** (s + q - 2)) for (q, s, pp, nc) in P)))
r = value_sets(9, {1: 2, 2: 2, 3: 4, 6: 4}); print("Z_9 pairs at 1, 2, fours at 3, 6: K_same", r[1], "(other text 593/512)")
r = value_sets(27, {1: 2, 2: 2, 3: 2, 6: 2, 9: 4, 18: 4}); print("Z_27 pairs at 1, 2, 3, 6, fours at 9, 18: K_same", r[1], "(other text 2385/2048)")
D = {5: 2, 10: 2, 15: 2, 30: 2, 45: 4, 90: 4, 27: 2, 54: 2, 81: 2, 108: 2}
r = value_sets(135, D); print("Z_135 pairs at 5, 10, 15, 30, fours at 45, 90, pairs at 27, 54, 81, 108: K_same", r[1], "=", float(r[1]), "(other text 307665/262144); Theorem H checks failed:", len(r[3]))
sys.stdout.flush()
if len(sys.argv) > 1:
    D = {5: 2, 10: 2, 15: 2, 30: 2, 45: 4, 90: 4, 27: 4, 54: 4, 81: 4, 108: 4}
    r = value_sets(135, D); print("Z_135 the same with fours at 27, 54, 81, 108: K_same", r[1], "=", float(r[1]), "(other text 78764625/67108864); Theorem H checks failed:", len(r[3]))
