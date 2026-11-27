"""The sums W_X = sum over odd e > 1 with no prime factor in X of 2^(-mu(e)),  mu(e) = max_p v_p(e)(p-1), exact fractions.
A_X(t) = #{e : mu(e) <= t} = prod over odd primes p <= t+1, p not in X, of (1 + floor(t/(p-1))).
Tail: for t >= 42 the terms are at most those of the full sum (X empty), whose tail is < 5.7e-4 (Lemma W of sign-four-result.md).
Also a direct enumeration for t <= 14 as a check of the product formula."""
from fractions import Fraction
def primes(N): return [p for p in range(3, N + 1, 2) if all(p % q for q in range(3, int(p ** .5) + 1, 2))]
def A(t, X): 
    r = 1
    for p in primes(t + 1):
        if p not in X: r *= 1 + t // (p - 1)
    return r
def W(X, T):
    s = Fraction(0)
    for t in range(2, T + 1, 2): s += Fraction(A(t, X) - A(t - 2, X), 2 ** t)
    return s
def mu(e):
    m = 0; p = 3
    while e > 1:
        v = 0
        while e % p == 0: e //= p; v += 1
        m = max(m, v * (p - 1)); p += 2
    return m
for X, name in (((), 'all odd primes'), ((3,), 'no 3'), ((5,), 'no 5'), ((7,), 'no 7'), ((3, 5), 'no 3, no 5')):
    w40 = W(X, 40); w60 = W(X, 60)
    print(f'{name}: partial sum to t=40: {float(w40):.6f}; to t=60: {float(w60):.6f}; with the tail bound 5.7e-4 after t=40: < {float(w40) + 5.7e-4:.6f};  twice that: {2 * (float(w40) + 5.7e-4):.6f}')
# direct check of the product formula
import math
for X in ((), (3,), (5,)):
    for t in (2, 4, 6, 8, 10, 12, 14):
        N = 1
        for p in primes(t + 1):
            if p not in X: N *= p ** (t // (p - 1))
        cnt = sum(1 for e in range(1, N + 1, 2) if N % e == 0 and mu(e) <= t)
        assert cnt == A(t, X), (X, t, cnt, A(t, X))
print('product formula checked against enumeration for t <= 14')
print('p = 3 alone: sum_{l>=1} 2*4^-l = 2/3;  3/4 + 2*W(no 3) <', 0.75 + 2 * (float(W((3,), 40)) + 5.7e-4))
