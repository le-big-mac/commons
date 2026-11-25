"""Exact test of Phi_d | A(X) by integer polynomial remainder (agent3 / Yonder)."""
def polymul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): r[i + j] += x * y
    return r
def polydivmod(a, b):                     # b monic, integer coefficients, lowest degree first
    a = a[:]; q = [0] * max(1, len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        c = a[i + len(b) - 1]; q[i] = c
        if c:
            for j, y in enumerate(b): a[i + j] -= c * y
    return q, a[:len(b) - 1]
_cyc = {}
def cyclo(n):
    if n not in _cyc:
        p = [-1] + [0] * (n - 1) + [1]
        for d in range(1, n):
            if n % d == 0: p, rem = polydivmod(p, cyclo(d)); assert not any(rem)
        _cyc[n] = p
    return _cyc[n]
def divides(d, A, M):
    a = [0] * M
    for x in A: a[x] = 1
    return not any(polydivmod(a, cyclo(d))[1])
