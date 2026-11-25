"""D^w(Z): like D+ but h may take either sign on the classes of Z (only hhat >= 0 is required).
A weakly tiles its complement (Lev-Matolcsi) iff D^w(Z_A) = |A|   [same averaging argument as Prop 1].
Float LP first (HiGHS), to see where D^w > D+."""
import os
import sys, itertools
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','flat'))
import numpy as np
from scipy.optimize import linprog
from lp import Setup
def both(S,H):
    H=sorted(H); 
    if not H: return 1.0,1.0
    c=-np.array([S.phi[d] for d in H],float)
    A=np.array([[-S.T[(d,e)] for d in H] for e in S.divs],float); b=np.ones(len(S.divs))
    r1=linprog(c,A_ub=A,b_ub=b,bounds=[(0,None)]*len(H),method='highs')
    r2=linprog(c,A_ub=A,b_ub=b,bounds=[(None,None)]*len(H),method='highs')
    return 1-r1.fun, (1-r2.fun if r2.status==0 else float('inf'))
if __name__=='__main__':
    for M in range(2,int(sys.argv[1])+1):
        S=Setup(M); o=S.orders
        if len(o)>12: continue
        diff=[]; tot=0
        for k in range(len(o)+1):
            for H in itertools.combinations(o,k):
                tot+=1
                a,b=both(S,H)
                if abs(a-b)>1e-7: diff.append((H,round(a,4),round(b,4)))
        if diff: print(M,'patterns',tot,'with D^w != D+:',len(diff),'e.g.',diff[:3],flush=True)
    print('done')
