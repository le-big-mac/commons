"""Small checks of wording in result.md: does sqrt(m) Psi(m) fall along odd m >= 17 (exact, m <= 161)?  Where does the
exact comparison with the claimed constants stand?  And the inequality c_r <= sqrt(2/(pi r)) for r <= 20000 (integers)."""
import math
from fractions import Fraction as Fr
import psi as PSI
P = PSI.pairs_upto(160)
ex = {m: PSI.psi_pairs(m, P) for m in range(1, 162)}
exe = {m: PSI.psie_pairs(m, P) for m in range(2, 162, 2)}
odd = [m for m in range(17, 162, 2)]
print("m Psi(m)^2 strictly decreasing along odd 17..161:", all(m * ex[m] ** 2 > (m + 2) * ex[m + 2] ** 2 for m in odd[:-1]))
ev = [m for m in range(14, 162, 2)]
print("even m >= 14 where sqrt(m) Psi(m) rises:", [m + 2 for m in ev[:-1] if m * ex[m] ** 2 < (m + 2) * ex[m + 2] ** 2])
print("even m >= 14 where sqrt(m) Psi_e(m) rises:", [m + 2 for m in ev[:-1] if m * exe[m] ** 2 < (m + 2) * exe[m + 2] ** 2])
# exact comparisons with the constants claimed (as fractions): 1.82196, 1.6914, 1.6212, 0.9702
c1 = Fr(182196, 100000); c2 = Fr(16914, 10000); c3 = Fr(16212, 10000); c4 = Fr(9702, 10000)
def Q(m): return Fr(1, 2) if m <= 2 else Fr(1, 4) if (m % 2 and m >= 9) else Fr(47, 128) if (m % 2 == 0 and m >= 10) else Fr(3, 8)
print("m Psi^2 <= 1.82196^2 for all m <= 161:", all(m * ex[m] ** 2 <= c1 ** 2 for m in ex))
print("m Psi_e^2 <= 1.6914^2 for all even m <= 161:", all(m * exe[m] ** 2 <= c2 ** 2 for m in exe))
print("m min(Psi_e, Q)^2 <= 1.6212^2 for all even m <= 161:", all(m * min(exe[m], Q(m)) ** 2 <= c3 ** 2 for m in exe))
print("m Psi^2 <= 0.9702^2 for odd 17 <= m <= 161:", all(m * ex[m] ** 2 <= c4 ** 2 for m in odd))
print("m Psi^2 < 1 for all odd m <= 161:", all(m * ex[m] ** 2 < 1 for m in ex if m % 2))
print("13 * 1129^2 =", 13 * 1129 ** 2, " 4096^2 =", 4096 ** 2, ";  15 * 2095^2 =", 15 * 2095 ** 2, " 8192^2 =", 8192 ** 2)
# c_r^2 * pi * r / 2 <= 1 : with pi > 355/113 - 3e-7 it is enough to check with the float (margin shown)
worst = max(math.exp(2 * PSI.lncstar(r)) * math.pi * r / 2 for r in range(1, 20001))
print(f"largest c_r^2 pi r / 2, r <= 20000: {worst:.9f}")
# tail constants
x = 0.5783
for u0 in (81,):
    t = x ** u0 * ((u0 + 1) - u0 * x) / (1 - x) ** 2
    print(f"sum over u >= {u0} of (u + 1) x^u = {t:.4e}  (so the e with kappa > 160 weigh at most 2 * this = {2 * t:.3e} in sum of 2^(1-kappa))")
u0 = 376; t = x ** u0 * ((u0 + 1) - u0 * x) / (1 - x) ** 2
print(f"sum over u >= 376 of (u + 1) x^u = {t:.3e}, times sqrt(3000): {t * math.sqrt(3000):.3e}")
r2pi = math.sqrt(2 / math.pi)
print(f"m > 3000: sqrt(2/pi) (1 + 1.0581 * 1.0130622) = {r2pi * (1 + 1.0581 * 1.0130622):.6f};  sqrt(2/pi) 1.0581 * 1.0130622 = {r2pi * 1.0581 * 1.0130622:.6f};  sqrt(3000/2680) = {math.sqrt(3000 / 2680):.6f}")
print(f"m > 3000, Theorem 1': sqrt(2/pi) (1 + 1.0581 * 0.8045052) = {r2pi * (1 + 1.0581 * 0.8045052):.6f}")
