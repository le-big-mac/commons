"""A test of the route proposed in brief N for the Lean proof of N1 (the sum): every inequality the brief states.
a(u) = A(2u) = the number of odd t >= 1 with mu(t) <= 2u = prod over odd primes p <= 2u+1 of (1 + u // ((p-1)/2))."""
from fractions import Fraction as Fr
from math import comb
LIMIT = 12001
_s = bytearray([1]) * (LIMIT + 1); _s[0] = _s[1] = 0
for _i in range(2, int(LIMIT ** .5) + 1):
    if _s[_i]: _s[_i * _i::_i] = bytearray(len(_s[_i * _i::_i]))
ODD_PRIMES = [p for p in range(3, LIMIT + 1) if _s[p]]
import bisect
def primes_upto(n):
    assert n <= LIMIT
    return ODD_PRIMES[:bisect.bisect_right(ODD_PRIMES, n)]
def a(u):
    r = 1
    for p in primes_upto(2 * u + 1): r *= 1 + u // ((p - 1) // 2)
    return r
def mu_le(t, u):
    """is mu(t) <= 2u, for odd t?  (only the odd primes up to 2u+1 can divide such a t)"""
    for p in primes_upto(2 * u + 1):
        v = 0
        while t % p == 0: t //= p; v += 1
        if (p - 1) * v > 2 * u: return False
    return t == 1
# (0) a(u) really is the count, for small u, by brute force over odd t (all t with mu <= 2u are below a bound)
for u in range(0, 5):
    bound = 1
    for p in primes_upto(2 * u + 1): bound *= p ** (u // ((p - 1) // 2))
    cnt = sum(1 for t in range(1, bound + 1, 2) if mu_le(t, u))
    assert cnt == a(u), (u, cnt, a(u))
print('(0) a(u) = #{odd t : mu t <= 2u} for u = 0..4, by brute force:', [a(u) for u in range(5)])
# (1) the halving step: 1 + u//k <= 2 (1 + (u//2)//k) for all k >= 1; so a(u) <= 2^pi'(2u) a(u//2)
for u in range(0, 1200):
    for k in range(1, u + 2): assert 1 + u // k <= 2 * (1 + (u // 2) // k)
pi = lambda u: len(primes_upto(2 * u + 1))
for u in range(0, 1500): assert a(u) <= 2 ** pi(u) * a(u // 2)
print('(1) halving step holds for u < 1200 (factor by factor) and a(u) <= 2^pi a(u//2) for u < 1500')
# (2) the count of odd primes up to 2u+1 is at most (2u+5)/3; and for u >= 20, 2 pi <= 3 ceil(u/2)
for u in range(0, 5000):
    assert 3 * pi(u) <= 2 * u + 5, u
    if u >= 20: assert 2 * pi(u) <= 3 * ((u + 1) // 2), u
bad = [u for u in range(0, 20) if 2 * pi(u) > 3 * ((u + 1) // 2)]
print('(2) 3 pi <= 2u+5 for u < 5000; 2 pi <= 3 ceil(u/2) for 20 <= u < 5000; fails below 20 at u =', bad)
# (3) a(u)^2 <= 8^u : base cases u < 20, and further
for u in range(0, 600): assert a(u) ** 2 <= 8 ** u, u
print('(3) a(u)^2 <= 8^u for u < 600; the ratios a(u)^2/8^u for u = 0..5:', [float(Fr(a(u) ** 2, 8 ** u)) for u in range(6)])
# (4) partial sums W_U = sum_{u=1..U} (a(u) - a(u-1)) / 4^u, the tail bound 15 / 2^(V+1) for U = 2V - 1, and the three cases
def W(U): return sum(Fr(a(u) - a(u - 1), 4 ** u) for u in range(1, U + 1))
print('(4) W_U for U = 1..6:', [str(W(U)) for U in range(1, 7)])
c = lambda m: Fr(comb(m, m // 2), 2 ** m)
print('    even m <= 12: c_m + W_{(m-2)/2} =', [str(c(m) + W((m - 2) // 2)) for m in range(2, 13, 2)])
for V in (9, 10, 11, 12):
    U = 2 * V - 1
    # tail: sum_{u > U} a(u)/4^u, with a(u) <= 3 * 8^(u//2) (from a(u)^2 <= 8^u): u = 2v: 3/2^v ; u = 2v+1: (3/4)/2^v ; v >= V
    tail = Fr(15, 4) * Fr(2, 2 ** V)
    for u in range(U + 1, 400): assert a(u) <= 3 * 8 ** (u // 2)
    print('    U =', U, ' W_U =', float(W(U)), ' tail bound =', float(tail), ' W_U + tail =', float(W(U) + tail),
          ' even m >= 14 needs <', float(1 + Fr(1, 16) - c(14)), ':', W(U) + tail < 1 + Fr(1, 16) - c(14))
for m in range(14, 400, 2): assert c(m + 2) <= c(m)
print('    c_m decreasing for even m from 14 to 400; c_14 =', c(14))
