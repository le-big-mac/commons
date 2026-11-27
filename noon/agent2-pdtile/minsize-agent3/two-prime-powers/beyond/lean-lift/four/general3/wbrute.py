"""Lemma W by brute force, as a check of wsum.py: the sum of 2^(-mu(d)) over the odd d with 1 < d <= X,
mu(d) = max over primes p | d of v_p(d) * (p - 1), with exact fractions.  It is a lower bound for W and must
stay below the value of wsum.py (0.844473784...).

usage: wbrute.py [X=2000000]
"""
import sys
from fractions import Fraction as Fr

X = int(sys.argv[1]) if len(sys.argv) > 1 else 2000000
mu = [0] * (X + 1)
sieve = bytearray(X + 1)
for p in range(3, X + 1, 2):
    if sieve[p]:
        continue
    for q in range(p * p, X + 1, 2 * p):
        sieve[q] = 1
    pk = p
    v = 1
    while pk <= X:
        w = v * (p - 1)
        for d in range(pk, X + 1, pk):
            if mu[d] < w:
                mu[d] = w
        pk *= p
        v += 1
counts = {}
for d in range(3, X + 1, 2):
    counts[mu[d]] = counts.get(mu[d], 0) + 1
tot = Fr(0)
rest = 0
for t, c in counts.items():
    if t <= 200:
        tot += Fr(c, 2 ** t)
    else:
        rest += c          # these d contribute less than 2^(-200) each
print(f"sum over odd d, 1 < d <= {X}, with mu(d) <= 200, of 2^(-mu(d)) = {float(tot):.12f}"
      f" (the other {rest} such d add less than {rest} * 2^-200)")
small = {t: counts[t] for t in sorted(counts) if t <= 16}
print("number of odd d <= X with mu(d) = t, for t <= 16:", small)
print("(wsum.py: #{d : mu(d) = t} = 1, 4, 10, 14, 42, 264, 48, 696 for t = 2, 4, .., 16; the counts here are complete")
print(" for t <= 10 once X >= 3^5 * 5^2 * 7 * 11 = 467775, and partial for larger t)")
