# Two union-bound constants, computed exactly term by term.
# (a) S_mu  = sum over odd d > 1 of 2^(-mu(d)),  mu(d) = max over primes p | d of v_p(d) (p - 1)
#     using N(k) = #{odd d : mu(d) <= k} = prod over odd primes p <= k+1 of (1 + floor(k/(p-1))).
# (b) S_phi = sum over odd m > 1 of 2^(-phi(m)), by direct enumeration up to a bound (terms with phi(m) large are tiny).
from fractions import Fraction
from math import log2

def primes_upto(n):
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    return [i for i in range(n + 1) if sieve[i]]

K = 400
odd_primes = [p for p in primes_upto(K + 2) if p > 2]
def N(k):
    out = 1
    for p in odd_primes:
        if p - 1 > k:
            break
        out *= 1 + k // (p - 1)
    return out
total = Fraction(0)
prev = N(0)
last_term = None
for k in range(1, K + 1):
    cur = N(k)
    term = Fraction(cur - prev, 2 ** k)
    total += term
    prev = cur
    last_term = term
print("S_mu partial sum to mu <=", K, "=", float(total), " last term", float(last_term), " log2 N(K) =", log2(N(K)))

# (b)
M = 200000
phi = list(range(M + 1))
for p in primes_upto(M):
    for j in range(p, M + 1, p):
        phi[j] -= phi[j] // p
s = 0.0
for m in range(3, M + 1, 2):
    if phi[m] < 200:
        s += 2.0 ** (-phi[m])
print("S_phi over odd m in [3, %d] =" % M, s)
