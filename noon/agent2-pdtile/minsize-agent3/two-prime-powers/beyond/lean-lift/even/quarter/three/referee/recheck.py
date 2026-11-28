# referee recomputation (independent of bounds.py): E3, tail constants, BB table, Theorem 7 numbers
from fractions import Fraction as F
from math import comb
from itertools import combinations
import numpy as np
def pm(r, v):
    if (r+v) % 2 or abs(v) > r: return F(0)
    return F(comb(r, (r+v)//2), 2**r)
def c(r): return pm(r, 0)
def g(a, b, d):
    return sum(pm(a, v)*pm(b, v)*pm(d, v) for v in range(-min(a, b, d), min(a, b, d)+1) if v)
E = {1: F(0), 2: F(0)}
MX = 16
for m in range(3, MX+1):
    best = F(0)
    for r1 in range(1, m//2+1):
        r0 = m-r1
        if r0 in (3, 5) and r1 in (3, 5): val = E[r0]*E[r1]/2
        else: val = c(r0)*E[r1]+c(r1)*E[r0]+E[r0]*E[r1]
        best = max(best, val)
    for r2 in range(1, m//3+1):
        for r1 in range(r2, (m-r2)//2+1):
            r0 = m-r1-r2
            val = g(r0, r1, r2)+(c(r0)+E[r0])*(c(r1)+E[r1])*(c(r2)+E[r2])-c(r0)*c(r1)*c(r2)
            best = max(best, val)
    E[m] = best
print("E3 3..16:", [str(E[m]) for m in range(3, 17)])
# float version to 200
N = 200
P = np.zeros((N+1, 2*N+1))
for r in range(N+1):
    for v in range(-r, r+1, 2):
        P[r, v+N] = comb(r, (r+v)//2)/2.0**r
C = P[:, N].copy()
P0 = P.copy(); P0[:, N] = 0
Ef = np.zeros(N+1)
for m in range(3, N+1):
    best = 0.0
    for r1 in range(1, m//2+1):
        r0 = m-r1
        if r0 in (3, 5) and r1 in (3, 5): val = Ef[r0]*Ef[r1]/2
        else: val = C[r0]*Ef[r1]+C[r1]*Ef[r0]+Ef[r0]*Ef[r1]
        best = max(best, val)
    for r2 in range(1, m//3+1):
        r1 = np.arange(r2, (m-r2)//2+1)
        r0 = m-r1-r2
        gg = (P0[r0]*P0[r1]*P0[r2][None, :]).sum(axis=1)
        val = gg+(C[r0]+Ef[r0])*(C[r1]+Ef[r1])*(C[r2]+Ef[r2])-C[r0]*C[r1]*C[r2]
        best = max(best, val.max())
    Ef[m] = best
print("float vs exact max diff m<=16:", max(abs(Ef[m]-float(E[m])) for m in range(3, 17)))
bad = [m for m in range(5, 200, 2) if abs(Ef[m]-0.5*P[m-2, N+1]) > 1e-13]
print("odd m in 5..199 where E3 != P(S_{m-2}=1)/2:", bad)
ev = [(Ef[m], m) for m in range(2, 201, 2)]
print("largest even E3 up to 200:", max(ev), "5/128=", 5/128)
print("odd m>=7 max E3:", max((Ef[m], m) for m in range(7, 200, 2)), "5/32=", 5/32)
print("P(S67=1)", P[67, N+1], "c(68)", C[68], "c(202)", comb(202, 101)/2.0**202)
# W_m(no 3) by listing e* : count A(t) by product formula
def primes(lo, hi):
    return [p for p in range(lo, hi+1) if all(p % d for d in range(2, int(p**.5)+1))]
def A(t):
    a = 1
    for p in primes(5, t+1): a *= 1+t//(p-1)
    return a
def W(m):
    return sum(F(A(t)-A(t-1), 2**t) for t in range(1, m))
print("W8,W10,W12,W14:", W(8), W(10), W(12), W(14))
vals = [(float(c(m))+Ef[m]+float(W(m)), m) for m in range(12, 201)]
print("Thm7 max over 12..200:", max(vals), 377/1024, " m=14:", vals[2], 2977/8192)
print("Thm7 odd max 13..199:", max(v for v in vals if v[1] % 2), 469/2048)
print("m=16:", vals[4], 11431/32768, " m=18:", vals[6], " 11/32=", 11/32)
# BB table
BB = {1: F(0), 2: F(1, 2)}
def parts(total, k, mx=None):
    if mx is None: mx = total
    if k == 0:
        if total == 0: yield ()
        return
    for a in range(min(mx, total-(k-1)), 0, -1):
        for rest in parts(total-a, k-1, a): yield (a,)+rest
def pairing_min(sz, q):
    best = None
    def rec(rem, prod, npairs):
        nonlocal best
        if npairs == q//2:
            best = prod if best is None else min(best, prod); return
        i = rem[0]
        for j in rem[1:]:
            rec([x for x in rem if x not in (i, j)], prod*BB[sz[i]+sz[j]], npairs+1)
        if len(rem) % 2 == 1 or True:
            if len(rem)-1 >= 2*(q//2-npairs): rec(rem[1:], prod, npairs)
    rec(list(range(q)), F(1), 0)
    return best
def lam(sz, R, q, m):
    om = F(1) if R == 0 else (F(0) if R == 1 else F(1, 2))
    k = sum(1 for s in sz if s == 1)
    if k >= 1:
        ph = F(1, 2**(k-1))
        for s in sz:
            if s >= 2: ph *= BB[s+1]
    else:
        ph = pairing_min(sz, q)
        if q == 5 and sz == (2, 2, 2, 2, 2): ph = F(2, 1024) if R == 0 else F(34, 1024)
        if q == 5 and sz == (4, 2, 2, 2, 2) and R == 0: ph = F(2, 1024)+(BB[6]-c(6))/8
        if q == 5 and sz == (3, 3, 2, 2, 2): ph = min(ph, BB[5]**2/2)
    return ph*om
for m in range(3, 13):
    tot = c(m)+E[m]; terms = [str(c(m)), str(E[m])]
    for q in primes(5, m):
        psi = max(lam(sz, R, q, m) for R in range(0, m-q+1) for sz in parts(m-R, q))
        tot += ((m-1)//(q-1))*psi; terms.append("%d*%s" % ((m-1)//(q-1), psi))
    BB[m] = tot
    print("BB(%d) =" % m, tot, terms)
