"""Exact Delsarte parameters D+(H) for unions of step classes H in Z_M, after Kiss-Londner-Matolcsi-Somlai
(arXiv:2411.03854), Definition 2.4.  Everything in exact rational arithmetic.

Classes are indexed by ORDER d | M:  C_d = {x in Z_M : order of x is d} = {x : gcd(x,M) = M/d},  |C_d| = phi(d).
H is given as a set of orders d > 1 (the class d = 1, i.e. {0}, is always in H).

D+(H) = max sum_x h(x)  over step functions h with h(0)=1, h>=0, h=0 off H, hhat>=0.
"""
from fractions import Fraction as Fr
from math import gcd
from functools import lru_cache

def divisors(n): return [d for d in range(1,n+1) if n%d==0]
def phi(n): return sum(1 for k in range(1,n+1) if gcd(k,n)==1)
def mobius(n):
    r=1; p=2
    while p*p<=n:
        if n%p==0:
            n//=p
            if n%p==0: return 0
            r=-r
        p+=1
    return -r if n>1 else r

@lru_cache(None)
def ramanujan(d,x):
    """sum over elements u of order d in Z_M of exp(2 pi i u x / M), for x with gcd(x, M) = g; depends only on gcd(d, x-ish).
    Here we use the classical Ramanujan sum c_d(k) = sum_{t | gcd(d,k)} mu(d/t) t, with k the 'frequency index'."""
    g=gcd(d,x)
    return sum(mobius(d//t)*t for t in range(1,g+1) if g%t==0)

class Setup:
    def __init__(s,M):
        s.M=M; s.divs=divisors(M); s.orders=[d for d in s.divs if d>1]; s.phi={d:phi(d) for d in s.divs}
        # transform of the indicator of C_d (elements of order d) evaluated at a point of order e:
        # an element of order d is u*M/d with u a unit mod d; a point of order e is v*M/e; the character value is
        # exp(2 pi i u v (M/d)(M/e)/M) = exp(2 pi i u v' / d) with v' = v*(M/e)  ->  Ramanujan sum c_d(M/e).
        s.T={(d,e):ramanujan(d,M//e) for d in s.divs for e in s.divs}
    def _solve(s,H,second=None):
        """Maximise sum_x h(x). If second is given (a dict order -> coefficient, plus constant ignored), then among the
        optimal solutions maximise sum_d second[d]*h_d (lexicographic; exact)."""
        H=sorted(H); n=len(H); rows=s.divs; m=len(rows)
        tab=[[Fr(-s.T[(d,e)]) for d in H]+[Fr(1 if i==j else 0) for j in range(m)]+[Fr(1)] for i,e in enumerate(rows)]
        ncol=n+m; basis=[n+i for i in range(m)]
        def run(cost,allowed):
            z=[sum(cost[basis[i]]*tab[i][j] for i in range(m))-cost[j] for j in range(ncol)]
            while True:
                enter=next((j for j in range(ncol) if allowed[j] and z[j]<0),None)
                if enter is None: return z
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
        cost=[Fr(s.phi[d]) for d in H]+[Fr(0)]*m
        z1=run(cost,[True]*ncol)
        def sol():
            x=[Fr(0)]*ncol
            for i,b in enumerate(basis): x[b]=tab[i][-1]
            return x
        x=sol(); val=1+sum(cost[j]*x[j] for j in range(n))
        if second is None: return val,{d:x[j] for j,d in enumerate(H)}
        out={}
        for key,coef in second.items():
            c2=[Fr(coef.get(d,0)) for d in H]+[Fr(0)]*m
            run(c2,[zj==0 for zj in z1])                 # stay on the optimal face of the first objective
            x=sol(); out[key]=sum(c2[j]*x[j] for j in range(n))
            # z1 remains the reduced-cost row of objective 1 up to pivots inside the face (its zero pattern is what matters);
            # recompute it for the new basis so that the next secondary objective uses a correct face description
            z1=[sum(cost[basis[i]]*tab[i][j] for i in range(m))-cost[j] for j in range(ncol)]
        return val,out
    def Dplus(s,H):
        """H: iterable of orders > 1. Returns (value, {order: h value})."""
        H=list(H)
        if not H: return Fr(1),{}
        return s._solve(H)
    def complement(s,H):
        """An exact pd-tiling complement attached to the pattern H (orders): f(e) = hhat(e)/D+ for one optimal h.
        Returned as {order e (including 1): Fraction}. For any set A with zero set containing H and |A| = D+(H),
        sum over a in A of f(order of (z - a)) = 1 for every z in Z_M."""
        H=list(H); val,h=s.Dplus(H)
        return {e:(1+sum(h[d]*s.T[(d,e)] for d in H))/val for e in s.divs}
    def forbidden_orders(s,H):
        """Orders e > 1 such that SOME optimal h for D+(H) has hhat > 0 on the elements of order e.
        If A is a set with |A| = D+(H) whose zero set contains H, then f = hhat/|A| is a pd-tiling complement of A for
        every optimal h, so f(a-a') = 0 for distinct a, a' in A: no difference of two elements of A has such an order."""
        H=list(H)
        if not H: return []
        second={e:{d:s.T[(d,e)] for d in H} for e in s.orders}     # hhat(e) = 1 + sum_d h_d T[d,e]
        val,mx=s._solve(H,second)
        return [e for e in s.orders if 1+mx[e]>0]

if __name__=='__main__':
    # self-tests
    import cmath
    M=36; S=Setup(M)
    for d in S.divs:
        for e in S.divs:
            x=M//e                      # a point of order e
            v=sum(cmath.exp(2j*cmath.pi*u*x/M) for u in range(M) if M//gcd(u,M)==d)
            assert abs(v-S.T[(d,e)])<1e-9,(d,e,v,S.T[(d,e)])
    print('transform table agrees with direct summation for M=36')
    # a known tiling of Z_12: A={0,1,2}+{0,6}?  use H = whole group: D+ = M ; H = {0}: D+ = 1
    S=Setup(12); print('D+(everything)=',S.Dplus(S.orders)[0],' D+({0})=',S.Dplus([])[0])
    # subgroup of order 4 in Z_12 (orders 2,4): expect 4
    print('D+(subgroup of order 4 in Z_12)=',S.Dplus([2,4])[0],'; its standard complement:',S.Dplus([3,6,12])[0])
    print('forbidden difference orders for Z0=[2,4] (n=4) in Z_12:',S.forbidden_orders([2,4]),' for [3,6,12] (n=3):',S.forbidden_orders([3,6,12]))
