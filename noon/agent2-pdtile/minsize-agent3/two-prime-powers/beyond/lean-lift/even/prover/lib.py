"""Own library (27 Nov 2026): exact tests of 'good' for signed masks on Z_n.
A mask is an integer coefficient vector c of length n (c[x] = coefficient of X^x).  It is good iff c is divisible by
no cyclotomic polynomial Phi_d, d | n.  Exact integer arithmetic: remainders modulo Phi_d through the table
X^x mod Phi_d (int64; entries are small for the n used here)."""
import itertools
import numpy as np

def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]

def polymul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] += x * y
    return r

def polydivexact(a, b):
    a = a[:]; q = [0] * (len(a) - len(b) + 1)
    for i in range(len(q) - 1, -1, -1):
        q[i] = a[i + len(b) - 1] // b[-1]
        for j, y in enumerate(b):
            a[i + j] -= q[i] * y
    assert not any(a)
    return q

_phi = {}
def cyclo(d):
    """coefficients of Phi_d, low degree first"""
    if d in _phi: return _phi[d]
    p = [-1] + [0] * (d - 1) + [1]
    for e in divisors(d):
        if e < d: p = polydivexact(p, cyclo(e))
    _phi[d] = p
    return p

_tab = {}
def table(d, n):
    """T[x] = X^x mod Phi_d as an integer vector of length deg Phi_d, x = 0..n-1"""
    if (d, n) in _tab: return _tab[(d, n)]
    ph = cyclo(d); deg = len(ph) - 1
    T = np.zeros((n, deg), dtype=np.int64)
    cur = [0] * deg; cur[0] = 1
    if deg == 0: raise ValueError
    for x in range(n):
        T[x] = cur
        top = cur[-1]; cur = [0] + cur[:-1]
        if top:
            for j in range(deg): cur[j] -= top * ph[j]
    _tab[(d, n)] = T
    return T

def bad_levels(c, n):
    """list of d | n with Phi_d | mask c"""
    c = np.asarray(c, dtype=np.int64)
    return [d for d in divisors(n) if not np.any(c @ table(d, n))]

def is_good(c, n):
    c = np.asarray(c, dtype=np.int64)
    for d in divisors(n):
        if not np.any(c @ table(d, n)): return False
    return True

def mask(n, elems, signs):
    c = np.zeros(n, dtype=np.int64)
    for x, s in zip(elems, signs): c[x % n] += s
    return c

def all_signs(m, fix_first=True):
    s = np.array(list(itertools.product((1, -1), repeat=m)), dtype=np.int64)
    return s[s[:, 0] == 1] if fix_first else s

def good_signings(n, elems, fix_first=True):
    """boolean vector over all signings (first sign + if fix_first): which are good"""
    m = len(elems); signs = all_signs(m, fix_first)
    good = np.ones(len(signs), bool)
    idx = [x % n for x in elems]
    for d in divisors(n):
        good &= np.any(signs @ table(d, n)[idx], axis=1)
    return signs, good

def v2(x):
    assert x != 0
    v = 0
    while x % 2 == 0: x //= 2; v += 1
    return v

def two_part(n):
    k = 0
    while n % 2 == 0: n //= 2; k += 1
    return k, n

def exceptional_pair(n, elems):
    """the pairs of Conjecture E: two elements a, b with a - b not divisible by 2^k"""
    if len(elems) != 2: return False
    k, _ = two_part(n)
    return (elems[0] - elems[1]) % (2 ** k) != 0

if __name__ == '__main__':
    # self test against complex evaluation
    import cmath, random
    random.seed(1)
    for n in (6, 8, 12, 18, 20, 30):
        for _ in range(300):
            m = random.randint(1, 6)
            el = [random.randrange(n) for _ in range(m)]; sg = [random.choice((1, -1)) for _ in range(m)]
            c = mask(n, el, sg)
            num = all(abs(sum(int(c[x]) * cmath.exp(2j * cmath.pi * x * t / n) for x in range(n))) > 1e-9 for t in range(n))
            assert num == is_good(c, n), (n, el, sg)
    print('lib self test ok')
