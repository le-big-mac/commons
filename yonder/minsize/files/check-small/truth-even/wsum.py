# sum over e > 1 (prime factors from a given least prime on) of 2^(-mu(e)), mu(e) = max over primes p of (p-1)*v_p(e)
from fractions import Fraction
def primes_upto(n):
    return [p for p in range(2, n + 1) if all(p % q for q in range(2, int(p ** 0.5) + 1))]
def W(least_prime, tmax=400):
    ps = primes_upto(tmax + 1)
    def A(t):
        r = 1
        for p in ps:
            if p < least_prime or p > t + 1:
                continue
            r *= 1 + t // (p - 1)
        return r
    s = Fraction(0)
    prev = 1
    for t in range(1, tmax + 1):
        a = A(t)
        s += Fraction(a - prev, 2 ** t)
        prev = a
    return float(s)
print("odd divisors from 3 on:", W(3))
print("divisors with no factor 2 or 3:", W(5))
print("the part with a factor 3:", W(3) - W(5))
