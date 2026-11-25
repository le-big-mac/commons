"""Independent check of the exact simplex: D+ recomputed with scipy's HiGHS (floating point, different algorithm and
code), and with the transform table rebuilt by direct summation of roots of unity instead of Ramanujan sums."""
import sys, pickle, random, cmath
import numpy as np
from math import gcd
from scipy.optimize import linprog
from lp import divisors
def table(M):
    divs=divisors(M); order=lambda u:M//gcd(u,M); T={}
    for e in divs:
        x=M//e
        acc={d:0j for d in divs}
        for u in range(M): acc[order(u)]+=cmath.exp(2j*cmath.pi*u*x/M)
        for d in divs: T[(d,e)]=acc[d].real
    return divs,T
for M in [int(x) for x in sys.argv[1:]]:
    O,D=pickle.load(open(f'D_{M}.pkl','rb')); divs,T=table(M); size={d:sum(1 for u in range(M) if M//gcd(u,M)==d) for d in divs}
    random.seed(7); masks=range(len(D)) if len(D)<=4096 else random.sample(range(len(D)),3000); worst=0
    for mask in masks:
        Z=[O[i] for i in range(len(O)) if mask>>i&1]
        if not Z: continue
        A=np.array([[-T[(d,e)] for d in Z] for e in divs]); r=linprog(-np.array([size[d] for d in Z],float),A_ub=A,b_ub=np.ones(len(divs)),bounds=[(0,None)]*len(Z),method='highs')
        worst=max(worst,abs(1-r.fun-float(D[mask])))
    print(f'M={M}: {len(list(masks))} patterns, largest |exact - HiGHS| = {worst:.2e}',flush=True)
