"""Exact D^w(Z) = max { sum_x h(x) : h step function, h(0)=1, h = 0 off {0} u Z, hhat >= 0 }  (h of either sign on Z).
A set A tiles its complement weakly (f >= 0, f(0)=1, 1_A * f = 1; no positive definiteness) iff D^w(Z_A) = |A|.
Same tableau as lp.Setup._solve, with every variable split into a positive and a negative part."""
import os
import sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','flat'))
from fractions import Fraction as Fr
from lp import Setup
class WSetup(Setup):
    def Dweak(s,H):
        H=sorted(H)
        if not H: return Fr(1),{}
        n=len(H); rows=s.divs; m=len(rows)
        tab=[[Fr(-s.T[(d,e)]) for d in H]+[Fr(s.T[(d,e)]) for d in H]+[Fr(1 if i==j else 0) for j in range(m)]+[Fr(1)] for i,e in enumerate(rows)]
        ncol=2*n+m; basis=[2*n+i for i in range(m)]
        cost=[Fr(s.phi[d]) for d in H]+[Fr(-s.phi[d]) for d in H]+[Fr(0)]*m
        z=[sum(cost[basis[i]]*tab[i][j] for i in range(m))-cost[j] for j in range(ncol)]
        while True:
            enter=next((j for j in range(ncol) if z[j]<0),None)
            if enter is None: break
            best=None; leave=None
            for i in range(m):
                a=tab[i][enter]
                if a>0:
                    r=tab[i][-1]/a
                    if best is None or r<best or (r==best and basis[i]<basis[leave]): best=r; leave=i
            if leave is None: raise RuntimeError('unbounded')
            piv=tab[leave][enter]; tab[leave]=[x/piv for x in tab[leave]]
            for i in range(m):
                if i!=leave and tab[i][enter]!=0:
                    f=tab[i][enter]; tab[i]=[x-f*y for x,y in zip(tab[i],tab[leave])]
            f=z[enter]; z=[x-f*y for x,y in zip(z,tab[leave])]
            basis[leave]=enter
        x=[Fr(0)]*ncol
        for i,b in enumerate(basis): x[b]=tab[i][-1]
        h={d:x[j]-x[n+j] for j,d in enumerate(H)}
        val=1+sum(s.phi[d]*h[d] for d in H)
        # verify feasibility exactly
        for e in s.divs: assert 1+sum(h[d]*s.T[(d,e)] for d in H)>=0
        return val,h
if __name__=='__main__':
    import itertools
    from dweak import both
    for M in (30,42,60,36,72):
        S=WSetup(M); o=S.orders; bad=0; diff=[]
        for k in range(len(o)+1):
            for H in itertools.combinations(o,k):
                v,h=S.Dweak(H); a,b=both(S,H); p=S.Dplus(H)[0]
                if abs(float(v)-b)>1e-7 or abs(float(p)-a)>1e-7: bad+=1
                if v!=p: diff.append((H,p,v))
        print(M,'exact vs float mismatches:',bad,' patterns with D^w>D+:',len(diff),' integer D^w among them:',[(H,str(p),str(v)) for H,p,v in diff if v.denominator==1][:6],flush=True)
        if M in (30,42): print('   ',[(H,str(p),str(v)) for H,p,v in diff])
