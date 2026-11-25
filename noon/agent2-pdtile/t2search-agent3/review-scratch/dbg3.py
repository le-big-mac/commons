import numpy as np, sys
from fractions import Fraction
from scipy.optimize import linprog, milp, LinearConstraint, Bounds
import wt
M=72; A=[0,1,2,3,8]
As = set(A); k = len(A); Dset = {(x - y) % M for x in A for y in A}; T = [t for t in range(M) if t not in Dset]; Ac = [y for y in range(M) if y not in As]
C = np.array([[1.0 if (y - t) % M in As else 0.0 for y in Ac] for t in T])
r = linprog(-np.ones(len(Ac)), A_ub=C, b_ub=np.zeros(len(T)), bounds=[(-1, 1)] * len(Ac), method="highs")
print(r.status, r.fun, len(T), len(Ac)); print(np.round(r.x,5))
# dual-simplex vertex?
for meth in ("highs-ds","highs-ipm"):
    r = linprog(-np.ones(len(Ac)), A_ub=C, b_ub=np.zeros(len(T)), bounds=[(-1, 1)] * len(Ac), method=meth)
    print(meth, r.fun, np.round(r.x[:12],6))
# integer certificate by MILP
import time
for L in (1,2,3,5,10):
    t0=time.time()
    r = milp(c=-np.ones(len(Ac)), constraints=[LinearConstraint(C, -np.inf, 0), LinearConstraint(np.ones((1,len(Ac))), 1, np.inf)], integrality=np.ones(len(Ac)), bounds=Bounds(-L*np.ones(len(Ac)), L*np.ones(len(Ac))), options={"time_limit":20})
    print(L, r.status, None if r.x is None else (-r.fun), time.time()-t0)
    if r.x is not None:
        w=[Fraction(0)]*M
        for y,v in zip(Ac, r.x): w[y]=Fraction(int(round(v)))
        for x in A: w[x]=Fraction(-k*L)
        print("verified:", wt.verify_farkas(A, M, (w, Fraction(k*k*L)))); break
