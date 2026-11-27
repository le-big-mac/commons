# t1b_numbers.py -- two further numbers of the text: section 6, road 1 ("about 0.78") and section 4 ("0.357"); file times.
from fractions import Fraction as Fr
def primes_upto(N):
    return [p for p in range(2, N + 1) if all(p % d for d in range(2, int(p ** 0.5) + 1))]
def A(t):
    r = 1
    for p in primes_upto(t + 1):
        if p >= 5:
            r *= 1 + t // (p - 1)
    return r
s = Fr(0)
for t in range(2, 81, 2):
    c = A(t) - A(t - 2)
    if c:
        inner = sum(Fr(2, 2 ** max(2 * l, t)) for l in range(1, 200))
        s += c * inner
print("sum over e''* (primes >= 5, mu <= 80) and l >= 1 of 2^(1 - max(2l, mu)) =", float(s), "(text, road 1: about 0.78)")
print("3 * 0.119134 =", 3 * 0.119134, "(text: 0.357)")
# m = 9 with only the e2* of rank at most 8 (nine elements span at most 8 dimensions when e2 is dangerous... D <= 9)
