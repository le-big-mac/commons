# The count of Theorem D (iii) for other sets Pi of odd primes (exact fractions up to mu = 400; the rest is below
# 2 * 7.6e-46 by the tail bound of Lemma W, which holds for every subset of the primes: see tW.py).
#   S(Pi) = sum_{p in Pi} delta_p  +  sum over the e* with at least two prime factors, all in Pi, of 2^(1 - mu(e*)),
#   delta_p = sum_{l >= 1} 2^(1 - (p-1) p^(l-1)).
# The proof of Theorem D (iii) shows, for odd m: share of bad signings <= S(Pi) whenever every odd prime with a live
# level in the trees of B lies in Pi.  (Pi = {3, 5} is the case of the text: 0.98515.)
from fractions import Fraction as F

T = 400
def primes_upto(N):
    return [p for p in range(3, N + 1, 2) if all(p % q for q in range(3, int(p ** 0.5) + 1, 2))]
PR = primes_upto(T + 1)

def delta(p):
    s, l = F(0), 1
    while (p - 1) * p ** (l - 1) <= 4000:
        s += F(2, 2 ** ((p - 1) * p ** (l - 1)))
        l += 1
    return s

def S(flt):
    Pi = [p for p in PR if flt(p)]
    def A(t):
        r = 1
        for p in Pi:
            if p - 1 > t:
                break
            r *= 1 + t // (p - 1)
        return r
    pure = sum(delta(p) for p in Pi)
    mixed = F(0)
    prev = 1
    for t in range(2, T + 1, 2):
        a = A(t)
        npure = sum(1 for p in Pi if p - 1 <= t and t % (p - 1) == 0)
        mixed += F(2 * (a - prev - npure), 2 ** t)
        prev = a
    return pure, mixed

rows = [
    ("{3,5}", lambda p: p in (3, 5)),
    ("{3,5,7}", lambda p: p in (3, 5, 7)),
    ("{3,5,11}", lambda p: p in (3, 5, 11)),
    ("{3,5,13}", lambda p: p in (3, 5, 13)),
    ("{3,5,17}", lambda p: p in (3, 5, 17)),
    ("{3,5,19}", lambda p: p in (3, 5, 19)),
    ("{3,5,13,17}", lambda p: p in (3, 5, 13, 17)),
    ("{3,5,13,19}", lambda p: p in (3, 5, 13, 19)),
    ("{3,5,13,23}", lambda p: p in (3, 5, 13, 23)),
    ("{3,5} and all p >= 13", lambda p: p in (3, 5) or p >= 13),
    ("{3,5} and all p >= 17", lambda p: p in (3, 5) or p >= 17),
    ("{3,5,13} and all p >= 23", lambda p: p in (3, 5, 13) or p >= 23),
    ("{3,5,13} and all p >= 29", lambda p: p in (3, 5, 13) or p >= 29),
    ("{3,7} and all p >= 11 (no 5)", lambda p: p != 5),
    ("{5,7,...} (no 3)", lambda p: p != 3),
    ("{3,5,7} only", lambda p: p in (3, 5, 7)),
    ("all odd primes", lambda p: True),
]
for name, flt in rows:
    pure, mixed = S(flt)
    tot = pure + mixed
    print("%-30s pure = %.7f  mixed = %.7f  S = %.7f  %s" % (name, float(pure), float(mixed), float(tot), "< 1" if tot + F(1, 10 ** 40) < 1 else "NOT < 1"))
print("(primes above 401 enter only through terms with mu > 400, inside the tail bound)")
