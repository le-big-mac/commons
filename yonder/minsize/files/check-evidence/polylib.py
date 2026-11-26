# Exact integer polynomial helpers (lists of ints, lowest degree first). No floating point.
from functools import lru_cache

def trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a

def polymul(a, b):
    if not a or not b:
        return []
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] += x * y
    return trim(r)

def polydivmod(a, b):
    """a = q*b + r with b monic; exact integer arithmetic."""
    a = trim(a); b = trim(b)
    assert b and b[-1] == 1
    q = [0] * max(0, len(a) - len(b) + 1)
    a = a[:]
    while len(a) >= len(b):
        c = a[-1]
        k = len(a) - len(b)
        q[k] = c
        for i, y in enumerate(b):
            a[k + i] -= c * y
        a = trim(a)
        if not a:
            break
    return trim(q), a

def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]

@lru_cache(None)
def cyclo(d):
    """Phi_d as a tuple, by dividing X^d - 1 by the Phi_k, k | d, k < d."""
    num = [-1] + [0] * (d - 1) + [1]
    for k in divisors(d):
        if k < d:
            num, r = polydivmod(num, list(cyclo(k)))
            assert r == []
    return tuple(num)

def mask(marks, M):
    """marks: iterable of hours (repeats allowed) -> coefficient list of sum A(x) X^x."""
    a = [0] * M
    for h in marks:
        a[h % M] += 1
    return a

def balances_exact(marks, M, d):
    """Phi_d divides sum A(x) X^x, by exact division."""
    _, r = polydivmod(mask(marks, M), list(cyclo(d)))
    return r == []

def pattern_exact(marks, M):
    return frozenset(d for d in divisors(M) if d > 1 and balances_exact(marks, M, d))
