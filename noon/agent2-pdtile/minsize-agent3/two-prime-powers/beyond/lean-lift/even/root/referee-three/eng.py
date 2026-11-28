"""Referee's own engine: exact shares of bad signings for multisets given with multiplicities, and the structure
(cells, full cells, live levels, fully live divisors, ranks, e(d), kappa, need) straight from the definitions of
result.md sections 1 and 2.  Integer arithmetic only."""
import math
import numpy as np
from fractions import Fraction as Fr

def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]
def factor(n):
    f = {}; p = 2
    while p * p <= n:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def polydiv(a, b):
    a = a[:]; q = [0] * (len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        c = a[i + len(b) - 1]; q[i] = c
        if c:
            for j, bj in enumerate(b): a[i + j] -= c * bj
    assert not any(a)
    return q
_cyc = {}
def cyclo(d):
    if d not in _cyc:
        a = [-1] + [0] * (d - 1) + [1]
        for e in divisors(d):
            if e < d: a = polydiv(a, cyclo(e))
        _cyc[d] = a
    return _cyc[d]
_red = {}
def redmat(n, d):
    """rows b = 0..n-1: coefficients of X^b mod Phi_d."""
    if (n, d) not in _red:
        phi = cyclo(d); deg = len(phi) - 1
        v = [1] + [0] * (deg - 1); rows = []
        for b in range(n):
            rows.append(v[:])
            top = v[-1]; v = [0] + v[:-1]
            if top:
                for j in range(deg): v[j] -= top * phi[j]
        _red[(n, d)] = np.array(rows, dtype=np.int64)
    return _red[(n, d)]

def cstar(r):
    return Fr(1, 2) if r <= 0 else Fr(math.comb(r, r // 2), 2 ** r)

def grid(mults):
    """all vectors of signed sums (T_i), T_i = -h_i, -h_i + 2, ..., h_i, with the number of signings of each."""
    T = np.zeros((1, 0), dtype=np.int64); w = np.ones(1, dtype=object)
    for h in mults:
        vals = np.arange(-h, h + 1, 2, dtype=np.int64)
        bw = np.array([math.comb(h, j) for j in range(h + 1)], dtype=object)
        N = T.shape[0]
        T = np.concatenate([np.repeat(T, h + 1, axis=0), np.tile(vals, N)[:, None]], axis=1)
        w = np.repeat(w, h + 1) * np.tile(bw, N)
    return T, w

def bad_flags(n, res, T):
    """dict d -> boolean array over grid points: Phi_d divides the signed mask."""
    out = {}
    for d in divisors(n):
        M = T @ redmat(n, d)[res]
        out[d] = ~M.any(axis=1)
    return out

def live_levels(n, res):
    out = {}
    for p, a in factor(n).items():
        lv = []
        for i in range(1, a + 1):
            cls = {}
            for b in res: cls.setdefault(b % p ** (i - 1), set()).add(b % p ** i)
            if any(len(s) == p for s in cls.values()): lv.append(i)
        out[p] = lv
    return out

def cells_of(d, res):
    fd = factor(d); rad = math.prod(fd); d0 = d // rad
    cells = {}
    for b in res: cells.setdefault(b % d0, []).append(b)
    return fd, d0, cells

def fully_live(n, res):
    """list of dicts for the fully live d > 1: d, primes, ranks, e, q, s, kappa, kappa+, need, ncells, and the cells."""
    live = live_levels(n, res); out = []
    for d in divisors(n):
        if d == 1: continue
        fd, d0, cells = cells_of(d, res)
        full = {p: [c for c, bs in cells.items() if len({((b - c) // d0) % p for b in bs}) == p] for p in fd}
        if not all(full[p] for p in fd): continue
        for p in fd: assert fd[p] in live[p], "a p-full cell at a level that is not live"
        ranks = {p: live[p].index(fd[p]) + 1 for p in fd}
        q = max(fd); s = max((ranks[p] - 1) * (p - 1) for p in fd)
        kap = s + q - 1; kp = kap if len(fd) == 1 else kap + 1
        need = q + 2 * s
        if len(fd) >= 2 and s == 0: need = q + 1
        for p in fd: assert len(cells) >= 1 + (ranks[p] - 1) * (p - 1), "(Q5) cell count fails"
        out.append(dict(d=d, fd=fd, d0=d0, ranks=ranks, e=math.prod(p ** ranks[p] for p in fd), q=q, s=s, kap=kap, kp=kp,
                        need=need, ncells=len(cells), cells=cells, full=full))
    return out
