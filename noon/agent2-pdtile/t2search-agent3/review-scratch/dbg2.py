import numpy as np, sys, pickle, time
from fractions import Fraction
from scipy.optimize import linprog
import wt
M=36
res = pickle.load(open("res36.pkl","rb"))
und = [r for r in res if r[2]=="?"]
print(len(und))
def restricted_cert(A, M, method):
    As=set(A); D={(x-y)%M for x in A for y in A}; T=[t for t in range(M) if t not in D]; Ac=[y for y in range(M) if y not in As]
    C=np.array([[1.0 if (y-t)%M in As else 0.0 for y in Ac] for t in T])
    r=linprog(-np.ones(len(Ac)), A_ub=C, b_ub=np.zeros(len(T)), bounds=[(-1,1)]*len(Ac), method=method)
    if r.status!=0 or -r.fun<1e-7: return None, "nolp"
    for Dn in (1,2,3,4,6,12,60,2520,10**5,10**7,10**9):
        wr=[Fraction(float(v)).limit_denominator(Dn) for v in r.x]
        k=len(A); w=[Fraction(0)]*M
        for y,v in zip(Ac,wr): w[y]=v
        for x in A: w[x]=Fraction(-k)
        cert=(w, Fraction(k*k))
        if wt.verify_farkas(A, M, cert): return cert, Dn
    return None, "norat"
import collections
for method in ("highs-ds","highs"):
    cnt=collections.Counter(); t0=time.time()
    for r in und[:400]:
        A=[x for x in range(M) if r[0]>>x&1]
        c, how = restricted_cert(A, M, method); cnt[how]+=1
    print(method, dict(cnt), time.time()-t0)
