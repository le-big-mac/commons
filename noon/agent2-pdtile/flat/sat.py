"""Search for a SET that pd-tiles Z_M but violates the Coven-Meyerowitz conditions.
Given a minimal pattern Z0 with D+(Z0) = n: find A in Z_M with 0 in A, |A| = n, Phi_d | A for all d in Z0, and
(T1 fails or T2 fails) for the exact zero set of A. Any such A pd-tiles (its zero set contains Z0) and, for M with at
most two prime factors, does not tile. CP-SAT works in exact integer arithmetic."""
import sys, time
from ortools.sat.python import cp_model
from cyc import residues, zero_set
from scan import factor
from lp import divisors
def count_exprs(m,x,M,ub=None):
    """Second formulation: Phi_d | A stated through the numbers of elements of A in residue classes.
    Write d = prod p_i^{a_i} over the primes with a_i >= 1 and let N be the count function on G = prod Z_{p_i^{a_i}}.
    Phi_d | A  iff  N is a sum of functions each invariant under one of the subgroups K_i = p_i^{a_i-1} Z_{p_i^{a_i}}
               iff  in every coset of prod K_i (a box with sides p_i) all mixed differences vanish:
                    sum over e in {0,1}^s of (-1)^{|e|} N(r_1 + e_1 i_1 p_1^{a_1-1}, ..., r_s + e_s i_s p_s^{a_s-1}) = 0
                    for all 1 <= i_k < p_k.
    Returns a function d -> list of linear expressions that all vanish iff Phi_d | A."""
    import itertools
    f=factor(M); ps=sorted(f); al=[f[p] for p in ps]; s=len(ps); N={}
    def cnt(lev):
        if lev in N: return N[lev]
        mods=[ps[k]**lev[k] for k in range(s)]; T={}
        if list(lev)==al:
            for i in range(M): T[tuple(i%mm for mm in mods)]=x[i]
        else:
            size=M
            for mm in mods: size//=mm
            D=1
            for mm in mods: D*=mm
            cap=min(size,ub.get(D,size)) if ub else size      # ub[D]: at most this many elements of A in a residue class mod D
            for cell in itertools.product(*[range(mm) for mm in mods]): T[cell]=m.NewIntVar(0,cap,'N'+'_'.join(map(str,lev))+'c'+'_'.join(map(str,cell)))
            for k in range(s):
                if lev[k]<al[k]:
                    up=list(lev); up[k]+=1; C=cnt(tuple(up))
                    for cell in T:
                        m.Add(T[cell]==sum(C[cell[:k]+(cell[k]+i*mods[k],)+cell[k+1:]] for i in range(ps[k])))
        N[lev]=T; return T
    def res(d):
        fd=factor(d); lev=tuple(fd.get(p,0) for p in ps); T=cnt(lev); act=[k for k in range(s) if lev[k]>0]
        steps=[ps[k]**(lev[k]-1) if lev[k]>0 else 1 for k in range(s)]
        base=itertools.product(*[range(steps[k]) if lev[k]>0 else range(1) for k in range(s)])
        out=[]
        for r in base:
            for shifts in itertools.product(*[range(1,ps[k]) for k in act]):
                terms=[]
                for e in itertools.product((0,1),repeat=len(act)):
                    cell=list(r)
                    for idx,k in enumerate(act):
                        if e[idx]: cell[k]=r[k]+shifts[idx]*steps[k]
                    terms.append((-1)**sum(e)*T[tuple(cell)])
                out.append(sum(terms))
        return out
    if ub:                                            # make every level exist so that the caps act
        for lev in itertools.product(*[range(a+1) for a in al]): cnt(tuple(lev))
    return res
def search(M,n,Z0,time_limit=600,workers=8,violation=True,formulation='residues',forbid=(),cover=None):
    """forbid: orders e such that no two elements of A may differ by an element of order e (see lp.forbidden_orders)."""
    from math import gcd
    m=cp_model.CpModel(); x=[m.NewBoolVar(f'x{i}') for i in range(M)]
    if forbid:
        fb=set(forbid); bad=[c for c in range(1,M) if M//gcd(c,M) in fb]
        for c in bad: m.Add(x[c]==0)                     # 0 is in A
        if len(bad)*M<=400000:                           # the pairwise exclusions are optional strengthening
            for c in bad:
                for a in range(1,M):
                    b=(a+c)%M
                    if b>a and b!=0: m.AddBoolOr([x[a].Not(),x[b].Not()])
    m.Add(x[0]==1); m.Add(sum(x)==n)
    O=[d for d in divisors(M) if d>1]; Z0=set(Z0)
    if cover:
        # cover: {order: Fraction} = an exact pd-tiling complement f of every set with these zeros and this size.
        # 1_A * f = 1 everywhere: for every z, sum_a x_a f(z-a) = 1. (Implied by the zero conditions; stated for propagation.)
        from math import lcm
        L=1
        for v in cover.values(): L=lcm(L,v.denominator)
        F={e:int(v*L) for e,v in cover.items()}
        for zz in range(M):
            m.Add(sum(F[M//gcd(zz-a,M)]*x[a] for a in range(M) if F[M//gcd(zz-a,M)])==L)
    def res(d):
        R=residues(d,M); k=len(R[0])
        return [sum(R[i][j]*x[i] for i in range(M) if R[i][j]) for j in range(k)]
    if formulation=='counts':
        ub=None
        if forbid:
            # In a residue class mod D (a coset of the subgroup of order M/D) the elements of A differ pairwise by
            # allowed orders dividing M/D, so their number is at most the Delsarte bound of that pattern in Z_{M/D}.
            from lp import Setup as _Setup
            fbs=set(forbid); ub={}
            for D in divisors(M):
                mm=M//D
                if mm>1:
                    allowed=[d for d in divisors(mm) if d>1 and d not in fbs]
                    ub[D]=int(_Setup(mm).Dplus(allowed)[0]) if allowed else 1     # floor of an exact rational
        res=count_exprs(m,x,M,ub)
    for d in Z0:
        for e in res(d): m.Add(e==0)
    z={}
    def zvar(d):
        if d in Z0: return None            # known true
        if d not in z:
            b=m.NewBoolVar(f'z{d}'); z[d]=b; lits=[]
            for j,e in enumerate(res(d)):
                m.Add(e==0).OnlyEnforceIf(b)
                pos=m.NewBoolVar(f'p{d}_{j}'); neg=m.NewBoolVar(f'n{d}_{j}')
                m.Add(e>=1).OnlyEnforceIf(pos); m.Add(e<=-1).OnlyEnforceIf(neg); lits+=[pos,neg]
            m.AddBoolOr(lits+[b])           # not b  =>  some coordinate nonzero
        return z[d]
    primes=sorted(factor(M)); viol=[]
    fn=factor(n)
    for p in primes:
        pps=[p**a for a in range(1,factor(M)[p]+1)]
        known=sum(1 for s in pps if s in Z0); vs=[zvar(s) for s in pps if s not in Z0]
        m.Add(known+sum(vs)<=fn.get(p,0))                 # k(Z_A) divides |A| (Prop. 1(iii)): valid for every set
        t=m.NewBoolVar(f't1def{p}'); m.Add(known+sum(vs)<=fn.get(p,0)-1).OnlyEnforceIf(t); viol.append(t)
    for d in O:
        f=factor(d)
        if len(f)<2 or d in Z0: continue
        ex=[q**a for q,a in f.items()]
        t=m.NewBoolVar(f't2viol{d}')
        for s in ex:
            v=zvar(s)
            if v is not None: m.AddImplication(t,v)
        m.AddImplication(t,zvar(d).Not()); viol.append(t)
    smooth=1
    for p in primes: smooth*=p**fn.get(p,0)
    # if n has a prime factor that does not divide M, T1 (k = n) can never hold: every such set is a violation
    if violation and smooth==n: m.AddBoolOr(viol)
    s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=time_limit; s.parameters.num_workers=workers
    st=s.Solve(m); name=s.StatusName(st)
    A=[i for i in range(M) if s.Value(x[i])] if st in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None
    return name,A,s.WallTime()
if __name__=='__main__':
    M=144
    for Z0 in ([2,3,8,36,48,144],[2,3,12,16,48,72],[2,3,16,24,36,48,72],[4,6,8,9,12,18,144]):
        name,A,t=search(M,12,Z0)
        print(Z0,name,f'{t:.1f}s',A,zero_set(A,M) if A else '',flush=True)
