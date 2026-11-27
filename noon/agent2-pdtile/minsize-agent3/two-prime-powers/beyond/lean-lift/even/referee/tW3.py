# Second look: the values S(Pi) to ten places (exact fractions up to mu = 400; what is left out is below 2e-45),
# for comparison with the bounds quoted in the revised text (end of section 5).
from fractions import Fraction as F
T = 400
def primes_upto(N):
    return [p for p in range(3, N + 1, 2) if all(p % q for q in range(3, int(p ** 0.5) + 1, 2))]
PR = primes_upto(T + 1)
def delta(p):
    s, l = F(0), 1
    while (p - 1) * p ** (l - 1) <= 4000:
        s += F(2, 2 ** ((p - 1) * p ** (l - 1))); l += 1
    return s
def S(flt):
    Pi = [p for p in PR if flt(p)]
    def A(t):
        r = 1
        for p in Pi:
            if p - 1 > t: break
            r *= 1 + t // (p - 1)
        return r
    tot = sum(delta(p) for p in Pi)
    prev = 1
    for t in range(2, T + 1, 2):
        a = A(t)
        tot += F(2 * (a - prev - sum(1 for p in Pi if p - 1 <= t and t % (p - 1) == 0)), 2 ** t)
        prev = a
    return tot
def show(x, places=10):
    n = int(x * 10 ** places)          # truncated, not rounded
    s = str(n).rjust(places + 1, '0')
    return s[:-places] + '.' + s[-places:] + '...'
rows = [("{3,5}", lambda p: p in (3, 5), None, "0.98516", "<"),
        ("{3,5,7}", lambda p: p in (3, 5, 7), None, None, None),
        ("{3,5,11}", lambda p: p in (3, 5, 11), None, None, None),
        ("{3,5,13}", lambda p: p in (3, 5, 13), "0.999791", "0.999797", None),
        ("{3,5,17}", lambda p: p in (3, 5, 17), None, None, None),
        ("{3,5} and all p >= 17", lambda p: p in (3, 5) or p >= 17, None, "0.987599", None),
        ("{3,5,13} and all p >= 23", lambda p: p in (3, 5, 13) or p >= 23, None, "0.999891", None),
        ("{3,5,13,17}", lambda p: p in (3, 5, 13, 17), "1.002697", None, None),
        ("{3,5,13,19}", lambda p: p in (3, 5, 13, 19), "1.000637", None, None)]
for name, flt, lo, hi, _ in rows:
    v = S(flt)
    msg = ""
    if lo: msg += "  text: >= %s : %s" % (lo, "TRUE" if v >= F(lo) else "FALSE")
    if hi: msg += "  text: <= %s : %s" % (hi, "TRUE" if v + F(1, 10 ** 40) <= F(hi) else "FALSE")
    print("%-28s S = %s%s" % (name, show(v), msg))
mixed35 = S(lambda p: p in (3, 5)) - delta(3) - delta(5)
print("2 * W({3,5}) = 2 * (1/3 + 1/15) + (mixed part 74/225) =", show(2 * (F(1, 3) + F(1, 15)) + mixed35), " (the text, section 6: 1.1289)")
