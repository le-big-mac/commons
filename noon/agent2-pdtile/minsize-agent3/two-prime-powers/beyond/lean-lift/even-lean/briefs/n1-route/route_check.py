"""Numbers for N1' (mine): the sum of 2^(-mu(t)) over t > 1 prime to 6, mu(t) = max over p | t of (p-1) v_p(t).
N6(u) = #{t >= 1 prime to 6 : mu(t) <= u} = prod over primes p >= 5 with p-1 <= u of (1 + floor(u/(p-1))); likewise
Nodd(u) with the prime 3.  Prints the exact partial sums and the counts at each u, and compares the product formula
with a direct enumeration for small u."""
from fractions import Fraction
from math import prod
def primes_upto(n):
    s = bytearray([1]) * (n + 1); s[0:2] = b'\0\0'
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]
PR = primes_upto(2000)
def N(u, pmin): return prod(1 + u // (p - 1) for p in PR if p >= pmin and p - 1 <= u)
def mu(t):
    m = 0; x = t
    for p in PR:
        if p * p > x: break
        if x % p == 0:
            v = 0
            while x % p == 0: x //= p; v += 1
            m = max(m, (p - 1) * v)
    if x > 1: m = max(m, x - 1)
    return m
# direct enumeration against the product formula, for mu <= 12 (t prime to 6): every such t divides 5^3*7^2*11*13
big = 5 ** 3 * 7 ** 2 * 11 * 13
direct = {}
for t in range(1, big + 1):
    if big % t == 0:
        direct.setdefault(mu(t), []).append(t)
for u in range(0, 13):
    cnt = sum(len(v) for k, v in direct.items() if k <= u)
    assert cnt == N(u, 5), (u, cnt, N(u, 5))
print('product formula = direct enumeration for u <= 12 (t prime to 6)')
for u in sorted(direct):
    if u and u <= 12: print(f'  mu = {u}: {len(direct[u])} values of t: {sorted(direct[u])[:12]}{" ..." if len(direct[u]) > 12 else ""}')
def partial(U, pmin):
    return sum(Fraction(N(u, pmin) - N(u - 1, pmin), 2 ** u) for u in range(1, U + 1))
for U in (12, 16, 20, 24, 30, 40, 60):
    a = partial(U, 5); b = partial(U, 3)
    print(f'U = {U}: sum over t prime to 6 with mu <= U: {float(a):.10f};  over odd t: {float(b):.10f};  5/32 - first = {float(Fraction(5, 32) - a):.6f}')
print('counts with mu = u exactly, t prime to 6 / odd t, and count * (5/7)^... check:')
for u in range(4, 41, 2):
    c6 = N(u, 5) - N(u - 1, 5); co = N(u, 3) - N(u - 1, 3)
    print(f'  u = {u}: prime to 6: {c6}; odd: {co}; odd count / 2^u = {co / 2 ** u:.3e}; (7/5)^u * that = {co / 2 ** u * 1.4 ** u:.4f}; N6(u)^2 / 2^u = {N(u,5)**2 / 2**u:.4f}')

# ---- the route for Lean (added): b(u) = #{t >= 1 prime to 6 : mu(t) <= 2u}, exact for u <= 19; W6(U) = sum_{u=1}^U (b(u) - b(u-1)) / 4^u;
# tail: for u > 19, b(u) <= a(u) (a counts all odd t) and this morning's a(u)/4^u <= (5/7)^u, so the tail is at most (5/2)(5/7)^19.
def b(u): return N(2 * u, 5)
def a(u): return N(2 * u, 3)
print('b(u) for u = 0..19:', [b(u) for u in range(20)])
assert all(b(u) <= a(u) for u in range(0, 400))
W6 = Fraction(0)
for u in range(1, 20):
    W6 += Fraction(b(u) - b(u - 1), 4 ** u)
    if u in (6, 13, 19): print(f'W6({u}) = {W6} = {float(W6):.12f}')
tail = Fraction(5, 2) * Fraction(5, 7) ** 19
print('tail bound (5/2)(5/7)^19 =', float(tail)); print('W6(19) + tail =', float(W6 + tail), '< 5/32 =', 5 / 32, ':', W6 + tail < Fraction(5, 32))
assert all(Fraction(a(u), 4 ** u) <= Fraction(5, 7) ** u for u in range(0, 400)), 'a(u)/4^u <= (5/7)^u'
print("this morning's a(u)/4^u <= (5/7)^u holds for u < 400 (it is proved in Lean as a_le)")
# what the assembly needs, for every m >= 5:  2 * p_m + 2 * W < 1 with W < 5/32, p_m <= 11/32
for m in range(3, 12):
    pm = Fraction(1, 3) + Fraction(2, 3) * Fraction(-1, 2) ** m
    print(f'm = {m}: p_m = {pm}; 2 p_m + 2 * 5/32 = {float(2 * pm + Fraction(5, 16)):.5f}', '(no live t for m <= 4)' if m <= 4 else ('< 1' if 2 * pm + Fraction(5, 16) < 1 else ('= 1: needs W < 5/32 strictly' if 2 * pm + Fraction(5, 16) == 1 else 'NOT < 1')))
