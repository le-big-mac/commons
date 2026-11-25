"""Independent helpers for the review (not derived from the scripts under review)."""
import sys, math, cmath, itertools, random
from fractions import Fraction
import numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, "/home/agent3/review2")
from lemma_variants import residues          # under review
from cyclo_exact import divides, cyclo       # under review

def divisors(M):
    return [d for d in range(1, M + 1) if M % d == 0]

def zeros_numeric(A, M, tol=1e-8):
    """orders d > 1, d | M, with A(exp(2 pi i / d)) = 0, by floating-point evaluation"""
    out = set()
    for d in divisors(M):
        if d == 1: continue
        s = sum(cmath.exp(2j * math.pi * x / d) for x in A)
        if abs(s) < tol: out.add(d)
    return out

def zeros_exact(A, M):
    return {d for d in divisors(M) if d > 1 and divides(d, A, M)}

def zeros_fft(A, M, tol=1e-8):
    """zeros through the DFT of the indicator on Z_M: d is a zero iff the DFT vanishes at ALL frequencies of order d
    (also checks that vanishing at one frequency of order d is the same as at all)."""
    v = np.zeros(M); v[list(A)] = 1; F = np.fft.fft(v); out = set()
    for d in divisors(M):
        if d == 1: continue
        fr = [xi for xi in range(1, M) if M // math.gcd(xi, M) == d]
        z = [abs(F[xi]) < tol for xi in fr]
        assert all(z) or not any(z)
        if all(z): out.add(d)
    return out

def units(M):
    return [u for u in range(1, M) if math.gcd(u, M) == 1]

def padic(M, p, q):
    a = 0
    while M % p == 0: M //= p; a += 1
    b = 0
    while M % q == 0: M //= q; b += 1
    assert M == 1
    return a, b

def T1_holds(Z, k, p, a, q, b):
    return k == p ** sum(1 for i in range(1, a + 1) if p ** i in Z) * q ** sum(1 for j in range(1, b + 1) if q ** j in Z)

def T2_violations(Z, p, a, q, b):
    return [(i, j) for i in range(1, a + 1) for j in range(1, b + 1) if p ** i in Z and q ** j in Z and p ** i * q ** j not in Z]
