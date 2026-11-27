# the shares 1 - 2 p_m - 2 W_m(no 3), recomputed by a fresh reader (exact fractions)
from fractions import Fraction
def primes(n):
    s = [True]*(n+1); s[0]=s[1]=False
    for i in range(2,int(n**0.5)+1):
        if s[i]:
            for j in range(i*i,n+1,i): s[j]=False
    return [i for i,v in enumerate(s) if v]
T = 400
P = [q for q in primes(T+2) if q >= 5]
def N(t):  # number of e* (1 included) with all prime factors >= 5 and max_q v_q (q-1) <= t
    r = 1
    for q in P:
        if q-1 > t: break
        r *= 1 + t//(q-1)
    return r
def W(m):  # sum over e* > 1 with mu <= m-1 of 2^-mu
    s = Fraction(0)
    for t in range(1, m):
        a = N(t) - N(t-1)
        s += Fraction(a, 2**t)
    return s
def p(m): return Fraction(1,3) + Fraction(2,3)*Fraction(-1,2)**m
best = None
for m in range(5, 301):
    v = 1 - 2*p(m) - 2*W(m)
    if m <= 12 or m in (20, 60, 100, 200, 300): print(m, p(m) if m<=12 else '', W(m) if m <= 12 else float(W(m)), v if m <= 12 else '', float(v))
    if best is None or v < best[0]: best = (v, m)
print("least over 5..300:", float(best[0]), "at m =", best[1], "; W(300) =", float(W(301)))
print("limit 1/3 - 2 W:", float(Fraction(1,3) - 2*W(301)))
