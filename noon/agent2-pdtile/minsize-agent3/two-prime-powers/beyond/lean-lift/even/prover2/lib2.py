# Exact arithmetic for signed masks on Z_n: remainders modulo cyclotomic polynomials, "bad at d", "3-bad at d".
import itertools, functools
import numpy as np

def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]

@functools.lru_cache(maxsize=None)
def cyclo(d):
    # coefficients of Phi_d, low degree first (python ints), by exact division of X^d - 1
    num = [-1] + [0] * (d - 1) + [1]
    for e in divisors(d):
        if e < d:
            den = cyclo(e)
            q = [0] * (len(num) - len(den) + 1)
            num = list(num)
            for i in range(len(q) - 1, -1, -1):
                c = num[i + len(den) - 1] // den[-1]
                q[i] = c
                for j, b in enumerate(den):
                    num[i + j] -= c * b
            assert all(v == 0 for v in num)
            num = q
    return tuple(num)

@functools.lru_cache(maxsize=None)
def powrem(d):
    # matrix R (d x phi(d)): row x = remainder of X^x modulo Phi_d, 0 <= x < d
    phi = cyclo(d)
    deg = len(phi) - 1
    rows = []
    cur = [0] * deg
    if deg == 0:
        return np.zeros((d, 0), dtype=np.int64)
    cur[0] = 1
    for x in range(d):
        rows.append(list(cur))
        # multiply by X and reduce
        top = cur[-1]
        cur = [0] + cur[:-1]
        if top:
            for j in range(deg):
                cur[j] -= top * phi[j]
    return np.array(rows, dtype=np.int64)

def all_signs(m, fix_first=True):
    # (2^(m-1) or 2^m) x m matrix of signs
    k = m - 1 if fix_first else m
    idx = np.arange(1 << k, dtype=np.int64)
    S = np.ones((1 << k, m), dtype=np.int64)
    off = 1 if fix_first else 0
    for b in range(k):
        S[:, b + off] = 1 - 2 * ((idx >> b) & 1)
    return S

def values(B, n, d, S):
    # for each signing (row of S) the remainder of the signed mask modulo Phi_d  (rows x phi(d))
    R = powrem(d)
    M = R[[x % d for x in B], :]
    return S @ M

def bad_table(B, n, S, ds=None):
    # dict d -> boolean vector over signings: Phi_d divides the mask
    out = {}
    for d in (ds or divisors(n)):
        V = values(B, n, d, S)
        out[d] = ~V.any(axis=1)
    return out

def bad3_table(B, n, S, ds=None):
    out = {}
    for d in (ds or divisors(n)):
        V = values(B, n, d, S)
        out[d] = ~((V % 3).any(axis=1))
    return out

def is_bad(B, signs, n, d):
    V = values(B, n, d, np.array([signs], dtype=np.int64))
    return not V.any()

def is_bad3(B, signs, n, d):
    V = values(B, n, d, np.array([signs], dtype=np.int64))
    return not (V % 3).any()

def good(B, signs, n):
    return not any(is_bad(B, signs, n, d) for d in divisors(n))

def multisets_with_zero(n, m):
    for rest in itertools.combinations_with_replacement(range(n), m - 1):
        yield (0,) + rest

def two_part(n):
    k = 0
    while n % 2 == 0:
        n //= 2; k += 1
    return k, n
