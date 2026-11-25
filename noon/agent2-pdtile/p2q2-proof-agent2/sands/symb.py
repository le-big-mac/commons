"""Symbolic (in p,q) primal/dual certificates for the step LP of Z_{p^2 q^2}, pattern by pattern.
Primal: gamma >= 0 on classes, gamma_22 = 1, Lambda_d(gamma) = 0 for orders d not in Z u {0}; minimise sigma = Lambda_00.
Dual:   y on rows (row0: normalisation, others: the orders outside Z); reduced cost r_c = cost_c - sum_rows y_row*A[row][c] >= 0;
        value = y_0.   D^w = M / sigma_min.
"""
import itertools, sympy as sp, numpy as np
from scipy.optimize import linprog
P,Q=sp.symbols('p q',positive=True)
CLS=[(i,j) for i in range(3) for j in range(3)]
ORDS=[(l,m) for l in range(3) for m in range(3)]
def ram(p,l,i):
    if i==2: return sp.Integer(1)
    return (p**(2-i) if l<=i else 0) - (p**(1-i) if l<=i+1 else 0)
def coef(p,q,o,c): return ram(p,o[0],c[0])*ram(q,o[1],c[1])
def subs_(S): return itertools.chain.from_iterable(itertools.combinations(S,r) for r in range(len(S)+1))
def patterns():
    for Ep in subs_((1,2)):
        for Eq in subs_((1,2)):
            for F in subs_([(1,1),(1,2),(2,1),(2,2)]):
                yield Ep,Eq,F
def Zof(Ep,Eq,F): return {(l,0) for l in Ep}|{(0,m) for m in Eq}|set(F)
def system(Z,p,q,allowed=None):
    """rows (list of (name, coeffs over allowed classes, rhs)), cost over allowed classes."""
    cl=[c for c in CLS if allowed is None or c in allowed]
    rows=[('norm',[sp.Integer(1) if c==(2,2) else sp.Integer(0) for c in cl],sp.Integer(1))]
    for o in ORDS:
        if o==(0,0) or o in Z: continue
        rows.append((o,[coef(p,q,o,c) for c in cl],sp.Integer(0)))
    cost=[coef(p,q,(0,0),c) for c in cl]
    return cl,rows,cost
def numeric(Z,pv,qv,allowed=None):
    cl,rows,cost=system(Z,pv,qv,allowed)
    A=np.array([[float(x) for x in r[1]] for r in rows]); b=np.array([float(r[2]) for r in rows])
    res=linprog([float(x) for x in cost],A_eq=A,b_eq=b,bounds=[(0,None)]*len(cl),method='highs-ds')
    if res.status!=0: return None
    return res.fun,{c:res.x[k] for k,c in enumerate(cl)},res.eqlin.marginals
def primal_symbolic(Z,support):
    """solve the equality system with gamma supported on `support` (list of classes); returns dict or None."""
    cl,rows,cost=system(Z,P,Q,allowed=set(support))
    xs=sp.symbols('g0:%d'%len(cl))
    eqs=[sum(a*x for a,x in zip(r[1],xs))-r[2] for r in rows]
    sol=sp.linsolve(eqs,xs)
    if not sol: return None
    s=list(sol)[0]
    if any(e.free_symbols & set(xs) for e in s): 
        s=tuple(e.subs({x:0 for x in xs}) for e in s)       # pick a particular solution
        if any(sp.simplify(sum(a*x for a,x in zip(r[1],s))-r[2])!=0 for r in rows): return None
    g={c:sp.factor(sp.simplify(e)) for c,e in zip(cl,s)}
    val=sp.factor(sp.simplify(sum(a*g[c] for a,c in zip(cost,cl))))
    return g,val
def dual_symbolic(Z,tight,target=None):
    """find y with reduced cost = 0 on the classes in `tight`; returns (y dict, reduced costs dict, value)."""
    cl,rows,cost=system(Z,P,Q)
    ys=sp.symbols('y0:%d'%len(rows))
    eqs=[cost[k]-sum(ys[i]*rows[i][1][k] for i in range(len(rows))) for k,c in enumerate(cl) if c in tight]
    if target is not None: eqs.append(ys[0]-target)
    sol=sp.linsolve(eqs,ys)
    if not sol: return None
    s=list(sol)[0]
    free=set().union(*[e.free_symbols for e in s]) & set(ys)
    return s,ys,free,cl,rows,cost
