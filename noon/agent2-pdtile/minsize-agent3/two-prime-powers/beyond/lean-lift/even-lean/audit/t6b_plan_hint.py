"""The last sentence of the plan's route for the second final statement says: if the order of a - b is 2^s * odd with
s >= 1, then Phi_(2^s) divides X^a + X^b.  Checked here for every exceptional pair with n <= 64, by long division;
and which d does work: d = 2^(v_2(a - b) + 1)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from math import gcd
from ecore import cyclo, pdivmod

tot = hint_ok = right_ok = 0
ex = []
for n in range(2, 65, 2):
    for a in range(n):
        for b in range(a):
            g = (a - b) % n
            o = n // gcd(n, g)
            if o % 2:
                continue
            s = 0
            while o % 2 ** (s + 1) == 0:
                s += 1
            v = 0
            while g % 2 ** (v + 1) == 0:
                v += 1
            mask = [0] * n
            mask[a] += 1
            mask[b] += 1
            tot += 1
            h = not any(pdivmod(mask, list(cyclo(2 ** s)))[1])
            r = (n % 2 ** (v + 1) == 0) and not any(pdivmod(mask, list(cyclo(2 ** (v + 1))))[1])
            hint_ok += h
            right_ok += r
            if not h and len(ex) < 4:
                ex.append((n, b, a, f"order {o}, 2^s = {2 ** s}, works: d = {2 ** (v + 1)}"))
print(f"exceptional pairs with n <= 64: {tot}; Phi_(2^s) (2^s the power of 2 in the order of a - b) divides X^a + X^b "
      f"for {hint_ok} of them; Phi_d with d = 2^(v_2(a - b) + 1) divides n and X^a + X^b for {right_ok} of them")
print("examples where the plan's Phi_(2^s) fails (n, b, a, ...):", ex)
