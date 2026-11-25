"""Check: D^w(Z) = min { sum_x G(x) : G >= 0 step function, G(0) >= 1, Ghat = 0 on the classes of Z }   (float LP),
and    D+(Z)  = min { sum_x G(x) : G >= 0 step function, G(0) >= 1, Ghat <= 0 on the classes of Z }."""
import os
import sys, itertools, random
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','flat'))
import numpy as np
from scipy.optimize import linprog
from weaklp import WSetup
random.seed(3); bad=0; tot=0
for M in (12,30,36,42,60,72,90,120):
    S=WSetup(M); O=S.orders; divs=S.divs
    pats=[[d for d in O if random.random()<0.5] for _ in range(60)]
    for Z in pats:
        if not Z: continue
        c=np.array([S.phi[e] for e in divs],float)          # mass = sum_e phi(e) G_e
        Aeq=np.array([[S.T[(e,d)] for e in divs] for d in Z],float)   # Ghat at a point of order d = sum_e G_e T[e,d]
        bnds=[(1,None)]+[(0,None)]*(len(divs)-1)
        r1=linprog(c,A_eq=Aeq,b_eq=np.zeros(len(Z)),bounds=bnds,method='highs')
        r2=linprog(c,A_ub=Aeq,b_ub=np.zeros(len(Z)),bounds=bnds,method='highs')
        w=float(S.Dweak(Z)[0]); p=float(S.Dplus(Z)[0]); tot+=1
        if abs(r1.fun-w)>1e-7 or abs(r2.fun-p)>1e-7: bad+=1; print('MISMATCH',M,Z,r1.fun,w,r2.fun,p)
print('patterns tested:',tot,' mismatches:',bad)
