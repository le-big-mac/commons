"""More digits of the constants quoted in result.md (exact fractions, then decimal).  usage: digits.py"""
from fractions import Fraction
from decimal import Decimal, getcontext
from const import pairs, Psi_exact, Qbound
getcontext().prec = 30
PR = pairs(160)
def root(fr): return (Decimal(fr.numerator) / Decimal(fr.denominator)).sqrt()
for name, m, kw in (("sqrt(14) Psi(14)", 14, {}), ("sqrt(14) Psi_e(14)", 14, dict(parity=True)), ("sqrt(20) Psi_e(20)", 20, dict(parity=True)), ("sqrt(24) Psi(24)", 24, {}),
                    ("sqrt(13) Psi(13)", 13, {}), ("sqrt(15) Psi(15)", 15, {}), ("sqrt(17) Psi(17)", 17, {})):
    v = Psi_exact(m, PR, **kw); print(f"{name} = {root(v * v * m):.8f}   (Psi = {v})")
print("sqrt(18) 47/128 =", f"{root(Fraction(47, 128) ** 2 * 18):.8f}", "  sqrt(20) 47/128 =", f"{root(Fraction(47, 128) ** 2 * 20):.8f}", "  sqrt(22) 47/128 =", f"{root(Fraction(47, 128) ** 2 * 22):.8f}")
