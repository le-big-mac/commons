"""The examples named in result.md, exactly (own routines).  usage: examples.py"""
import math
from fractions import Fraction
from lib import *
from const import pairs, Psi_exact
def pbad(n, d, items):
    S, W, m = grid(items)
    return Fraction(int(W[bad_mask(d, items, S)].sum()), 2 ** m), m
p, m = pbad(15, 15, [(i, 2) for i in range(5)]); print(f"Z_15, two copies of 0..4: m = {m}, P(bad at 15) = {p}  (bound 2^-4 c_2 = {Fraction(1, 16) * c(2)})")
p, m = pbad(15, 15, [(0, 1), (10, 1), (11, 1), (2, 1), (8, 1), (14, 1)]); print(f"Z_15, 0, 10, 11, 2, 8, 14: m = {m}, P(bad at 15) = {p}  (bound 2^-4 / 2 = {Fraction(1, 32)})")
for mm in (9, 13, 21):
    p, m = pbad(3, 3, [(0, mm - 2), (1, 1), (2, 1)]); print(f"Z_3, ({mm - 2}, 1, 1): P(bad at 3) = {p}  (bound c_(m-2)/2 = {c(mm - 2) / 2})")
    p, m = pbad(5, 5, [(0, mm - 4), (1, 1), (2, 1), (3, 1), (4, 1)]); print(f"Z_5, ({mm - 4}, 1, 1, 1, 1): P(bad at 5) = {p}  (bound c_(m-6)/8 = {c(mm - 6) / 8})")
PR = pairs(160)
ex = {m: Psi_exact(m, PR) for m in range(1, 162)}
odd = sorted(((ex[m] ** 2 * m, m) for m in ex if m % 2 and m >= 17), reverse=True)[:3]
print("largest sqrt(m) Psi(m) over odd 17 <= m <= 161:", [(m, round(math.sqrt(v), 5)) for v, m in odd])
print("sqrt(m) Psi(m) decreasing over odd 17 <= m <= 161:", all(ex[m] ** 2 * m > ex[m + 2] ** 2 * (m + 2) for m in range(17, 160, 2)))
print("sqrt(m) Psi(m) over even m, six largest:", [(m, round(math.sqrt(v), 5)) for v, m in sorted(((ex[m] ** 2 * m, m) for m in ex if m % 2 == 0), reverse=True)[:6]])
# the excess over c_m of the best shares found by search.py climb, relative to c_m, against what part (b) allows at that m
import re, glob
for f in sorted(glob.glob('climb-*.out')):
    mo = re.search(r"m = (\d+)  seed \d+: best share (\d+)/(\d+)", open(f).read())
    if mo:
        mm = int(mo.group(1)); sh = Fraction(int(mo.group(2)), int(mo.group(3)))
        print(f"{f}: m = {mm}  share/c_m - 1 = {float(sh / c(mm) - 1):.4f}   allowed by 1/sqrt(m): {1 / (math.sqrt(mm) * float(c(mm))) - 1:.4f}   (limit sqrt(pi/2) - 1 = {math.sqrt(math.pi / 2) - 1:.4f})")
# Lemma E, case (b): (m - 4, 2, 2) modulo 3 against E1 = (3/8) c_(m-4)
for mm in (10, 30, 100):
    p, m = pbad(3, 3, [(0, mm - 4), (1, 2), (2, 2)]); print(f"Z_3, ({mm - 4}, 2, 2): P(bad at 3) = {float(p):.6f}, E1 = (3/8) c_(m-4) = {float(Fraction(3, 8) * c(mm - 4)):.6f}, ratio {float(p / (Fraction(3, 8) * c(mm - 4))):.4f}; formula c_(m-4) (1/4 + (m-4)/(8(m-2))) = {float(c(mm - 4) * (Fraction(1, 4) + Fraction(mm - 4, 8 * (mm - 2)))):.6f}")
