"""Direct decision 'is A a weak tile of Z_M?' with exact certificates.  Independent of the pattern logic of the scripts under review.
  full_lp(A, M)        : HiGHS on the M unknowns f(0..M-1) >= 0, f(0) = 1, 1_A * f = 1  (floating point verdict)
  certified(A, M)      : ('yes', f) with an exact rational f verified in rational arithmetic, or ('no', w) with an exact Farkas vector w
                         verified in rational arithmetic, or ('?', None)
  class_lp(A, M, Z)    : the reduction under review, re-implemented: f constant on gcd classes, transform vanishing at orders not in Z."""
import math, sys
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog

import os
USE_MILP = not os.environ.get('NOMILP')

def full_lp(A, M):
    B = np.zeros((M + 1, M))
    for y in range(M):
        for x in A: B[y, (y - x) % M] += 1
    B[M, 0] = 1
    r = linprog(np.zeros(M), A_eq=B, b_eq=np.ones(M + 1), bounds=[(0, None)] * M, method="highs")
    assert r.status in (0, 2), r.message
    return r.status == 0, (r.x if r.status == 0 else None)

def verify_f(A, M, f):
    """exact check of a rational weak complement"""
    return f[0] == 1 and all(v >= 0 for v in f) and all(sum(f[(y - x) % M] for x in A) == 1 for y in range(M))

def verify_farkas(A, M, w):
    """exact check of an infeasibility certificate w (rational, indexed by all y in Z_M, any real values), plus w0 for the row f(0) = 1:
       system: sum_x f(y - x) = 1 (all y), f(0) = 1, f >= 0.   Certificate: for all t: sum_{x in A} w(t + x) + w0 [t = 0] <= 0,  and sum w + w0 > 0."""
    w, w0 = w
    return all(sum(w[(t + x) % M] for x in A) + (w0 if t == 0 else 0) <= 0 for t in range(M)) and sum(w) + w0 > 0

def rationalise(v, dens=(1, 2, 3, 4, 6, 12, 24, 36, 72, 360, 2520, 10 ** 4, 10 ** 6)):
    for D in dens:
        yield [Fraction(float(t)).limit_denominator(D) for t in v]

def certified(A, M):
    feas, f = full_lp(A, M)
    if feas:
        f = np.where(np.abs(f) < 1e-9, 0, f)
        for fr in rationalise(f):
            if verify_f(A, M, fr): return "yes", fr, feas
        return "?", None, feas
    # Farkas, first on the system restricted to the possible support T = Z_M \ (A - A) (smaller, nicer vertices), lifted to a certificate
    # for the FULL system: w = -k on A, w0 = k^2;  the lifted certificate is what gets verified exactly, so nothing rests on the restriction.
    As = set(A); k = len(A); Dset = {(x - y) % M for x in A for y in A}; T = [t for t in range(M) if t not in Dset]; Ac = [y for y in range(M) if y not in As]
    if T:
        C = np.array([[1.0 if (y - t) % M in As else 0.0 for y in Ac] for t in T])
        r = linprog(-np.ones(len(Ac)), A_ub=C, b_ub=np.zeros(len(T)), bounds=[(-1, 1)] * len(Ac), method="highs")
        if r.status == 0 and -r.fun > 1e-7:
            for wr in rationalise(r.x, dens=(1, 2, 3, 4, 6, 12, 60, 2520, 10 ** 5, 10 ** 7, 10 ** 9)):
                w = [Fraction(0)] * M
                for y, v in zip(Ac, wr): w[y] = v
                for x in A: w[x] = Fraction(-k)
                cert = (w, Fraction(k * k))
                if verify_farkas(A, M, cert): return "no", cert, feas
        # integer certificate by a small integer programme (the result is verified exactly, so the solver is only an oracle)
        from scipy.optimize import milp, LinearConstraint, Bounds
        for L in ((1, 2, 3, 5, 10, 30, 100) if USE_MILP else ()):
            r = milp(c=-np.ones(len(Ac)), constraints=[LinearConstraint(C, -np.inf, 0), LinearConstraint(np.ones((1, len(Ac))), 1, np.inf)],
                     integrality=np.ones(len(Ac)), bounds=Bounds(-L * np.ones(len(Ac)), L * np.ones(len(Ac))), options={"time_limit": 20})
            if r.x is not None:
                w = [Fraction(0)] * M
                for y, v in zip(Ac, r.x): w[y] = Fraction(int(round(v)))
                for x in A: w[x] = Fraction(-k * L)
                cert = (w, Fraction(k * k * L))
                if verify_farkas(A, M, cert): return "no", cert, feas
    # Farkas on the full system: maximise sum w + w0 subject to B^T (w, w0) <= 0, -1 <= w, w0 <= 1
    B = np.zeros((M + 1, M))
    for y in range(M):
        for x in A: B[y, (y - x) % M] += 1
    B[M, 0] = 1
    r = linprog(-np.ones(M + 1), A_ub=B.T, b_ub=np.zeros(M), bounds=[(-1, 1)] * (M + 1), method="highs")
    if r.status == 0 and -r.fun > 1e-7:
        for wr in rationalise(r.x):
            cert = (wr[:M], wr[M])
            if verify_farkas(A, M, cert): return "no", cert, feas
    return "?", None, feas

_cache = {}
def class_data(M):
    if M in _cache: return _cache[M]
    divs = [d for d in range(1, M + 1) if M % d == 0]
    cls = {g: [x for x in range(M) if math.gcd(x, M) == g] for g in divs}        # gcd(0, M) = M
    Tm = {}
    for d in divs:
        if d == 1: continue
        row = []
        for g in divs:
            v = np.zeros(M); v[cls[g]] = 1; F = np.fft.fft(v)
            fr = [xi for xi in range(1, M) if M // math.gcd(xi, M) == d]
            vals = F[fr]; assert np.allclose(vals.imag, 0, atol=1e-8) and np.allclose(vals.real, vals.real[0], atol=1e-8)
            assert abs(vals.real[0] - round(vals.real[0])) < 1e-8
            row.append(round(vals.real[0]))
        Tm[d] = row
    _cache[M] = (divs, cls, Tm)
    return _cache[M]

def class_lp(A, M, Z):
    divs, cls, Tm = class_data(M)
    rows = [[1 if g == M else 0 for g in divs]] + [Tm[d] for d in divs if d > 1 and d not in Z] + [[len(cls[g]) for g in divs]]
    rhs = [1] + [0] * (len(rows) - 2) + [M / len(A)]
    r = linprog(np.zeros(len(divs)), A_eq=np.array(rows, float), b_eq=rhs, bounds=[(0, None)] * len(divs), method="highs")
    assert r.status in (0, 2), r.message
    return r.status == 0
