"""Step-complement LP for Z_M, M = p^a q^b.  Classes (i,j) = (v_p, v_q) capped.  Float (HiGHS) with exact helpers.
gamma[i][j] >= 0, gamma[a][b] = 1; Lambda(l,m) = sum gamma_ij c_l(i) c_m(j) = 0 for (l,m) not in Z, (l,m) != (0,0);
minimise Lambda(0,0) = sum f = M/|A|."""
import itertools, numpy as np
from scipy.optimize import linprog
from fractions import Fraction as Fr
def ram(p,n,l,i):
    """sum of an order-p^l character of Z_{p^n} over the elements of valuation exactly i (i = n: the element 0)."""
    if i==n: return 1
    return (p**(n-i) if l<=i else 0) - (p**(n-i-1) if l<=i+1 else 0)
class Step:
    def __init__(s,p,a,q,b):
        s.p,s.a,s.q,s.b=p,a,q,b; s.M=p**a*q**b
        s.cls=[(i,j) for i in range(a+1) for j in range(b+1)]
        s.ords=[(l,m) for l in range(a+1) for m in range(b+1)]
        s.C={(o,c):ram(p,a,o[0],c[0])*ram(q,b,o[1],c[1]) for o in s.ords for c in s.cls}
    def order_of(s,d):
        l=0
        while d%s.p==0: d//=s.p; l+=1
        m=0
        while d%s.q==0: d//=s.q; m+=1
        return (l,m)
    def solve(s,Z,obj=None,extra_eq=None,maximize=False):
        """Z: set of orders (l,m) where A vanishes.  Returns (value, gamma dict) or None."""
        n=len(s.cls); top=(s.a,s.b)
        Aeq=[];beq=[]
        row=[1.0 if c==top else 0.0 for c in s.cls]; Aeq.append(row); beq.append(1.0)
        for o in s.ords:
            if o==(0,0) or o in Z: continue
            Aeq.append([float(s.C[(o,c)]) for c in s.cls]); beq.append(0.0)
        if extra_eq:
            for r,v in extra_eq: Aeq.append(r); beq.append(v)
        c=[float(s.C[((0,0),cl)]) for cl in s.cls] if obj is None else obj
        if maximize: c=[-x for x in c]
        r=linprog(c,A_eq=np.array(Aeq),b_eq=np.array(beq),bounds=[(0,None)]*n,method='highs')
        if r.status!=0: return None
        val=-r.fun if maximize else r.fun
        return val,{cl:r.x[k] for k,cl in enumerate(s.cls)}
    def face(s,Z):
        """optimal value v = min sum f, and on the optimal face: max total mass of f outside pZ, outside qZ."""
        r=s.solve(Z)
        if r is None: return None
        v=r[0]; tot=[float(s.C[((0,0),cl)]) for cl in s.cls]
        outp=[tot[k] if cl[0]==0 else 0.0 for k,cl in enumerate(s.cls)]
        outq=[tot[k] if cl[1]==0 else 0.0 for k,cl in enumerate(s.cls)]
        mp=s.solve(Z,obj=outp,extra_eq=[(tot,v)],maximize=True)
        mq=s.solve(Z,obj=outq,extra_eq=[(tot,v)],maximize=True)
        both=s.solve(Z,obj=[x+y for x,y in zip(outp,outq)],extra_eq=[(tot,v)],maximize=True)
        return v,(mp[0] if mp else None),(mq[0] if mq else None),both
