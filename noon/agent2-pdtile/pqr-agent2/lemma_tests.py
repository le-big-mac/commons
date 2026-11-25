"""Solver tests of the counting lemmas used for Z_{pqr} (agent2). Each line asks CP-SAT (counts model from pdflat/sat.py,
no Proposition 3) whether a set contradicting a lemma exists; the lemma predicts INFEASIBLE. Positive controls show the
model can find sets when the lemma's hypothesis is weakened."""
import sys, itertools
sys.path.insert(0,'/home/agent2/pdflat')
from ortools.sat.python import cp_model
from sat import count_exprs
def exists(M,sizes,must,mustnot,limit=200):
    m=cp_model.CpModel(); x=[m.NewBoolVar(f'x{i}') for i in range(M)]; m.Add(x[0]==1)
    lo,hi=sizes; m.Add(sum(x)>=lo); m.Add(sum(x)<=hi)
    res=count_exprs(m,x,M)
    for d in must:
        for e in res(d): m.Add(e==0)
    for d in mustnot:
        lits=[]
        for j,e in enumerate(res(d)):
            a=m.NewBoolVar(f'p{d}_{j}'); b=m.NewBoolVar(f'n{d}_{j}'); m.Add(e>=1).OnlyEnforceIf(a); m.Add(e<=-1).OnlyEnforceIf(b); lits+=[a,b]
        m.AddBoolOr(lits)
    s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=limit; s.parameters.num_workers=6
    st=s.Solve(m); return s.StatusName(st)
bad=0; n=0
def t(label,pred,got):
    global bad,n; n+=1
    ok=(got==pred); bad+=(not ok)
    if not ok or '-v' in sys.argv: print(('ok   ' if ok else 'FAIL ')+label,got,flush=True)
for P in [(2,3,5),(2,3,7),(2,5,7),(3,5,7),(2,3,11),(2,7,11),(3,5,11)]:
    M=P[0]*P[1]*P[2]; p=min(P)
    for (a,b) in itertools.permutations(P,2):
        c=[z for z in P if z not in (a,b)][0]
        if a<b:
            # Lemma X: |A| = ab, Phi_a, Phi_b, Phi_M  =>  Phi_ab
            t(f'M={M} X  |A|={a*b}, Phi_{a},Phi_{b},Phi_{M}, not Phi_{a*b}','INFEASIBLE',exists(M,(a*b,a*b),[a,b,M],[a*b]))
            t(f'M={M} X  control: same without Phi_{M}','OPTIMAL',exists(M,(a*b,a*b),[a,b],[a*b]))
            # two-dimensional lower bound: Phi_ab, not Phi_a, not Phi_b => |A| >= a+b
            t(f'M={M} L3 Phi_{a*b}, not Phi_{a}, not Phi_{b}, |A| <= {a+b-1}','INFEASIBLE',exists(M,(1,a+b-1),[a*b],[a,b]))
            t(f'M={M} L3 control: |A| = {a+b}','OPTIMAL',exists(M,(a+b,a+b),[a*b],[a,b]))
        # case (c): E contains a; Phi_bc and Phi_M; |A| = a*k with k < min(b,c): impossible; with k = min(b,c): forces Phi_min
        if b<c:
            if b>1 and a*(b-1)>=1:
                t(f'M={M} c3 Phi_{a},Phi_{b*c},Phi_{M}, |A| <= {a*(b-1)}','INFEASIBLE',exists(M,(1,a*b-1),[a,b*c,M],[]))
            t(f'M={M} c3 Phi_{a},Phi_{b*c},Phi_{M}, |A| = {a*b}, not Phi_{b}','INFEASIBLE',exists(M,(a*b,a*b),[a,b*c,M],[b]))
            t(f'M={M} c3 control: |A| = {a*b}','OPTIMAL',exists(M,(a*b,a*b),[a,b*c,M],[]))
            # case (c) with a second pair: Phi_a, Phi_bc, Phi_ab, not Phi_b, not Phi_c, |A| <= a*min(b,c)
            t(f'M={M} c2 Phi_{a},Phi_{b*c},Phi_{a*b}, not Phi_{b}, not Phi_{c}, |A| <= {a*b}','INFEASIBLE',exists(M,(1,a*b),[a,b*c,a*b],[b,c]))
            t(f'M={M} c2 Phi_{a},Phi_{b*c},Phi_{a*c}, not Phi_{b}, not Phi_{c}, |A| <= {a*b}','INFEASIBLE',exists(M,(1,a*b),[a,b*c,a*c],[b,c]))
    # case (d): Phi_M alone with |A| <= p forces Phi_p
    t(f'M={M} d  Phi_{M}, |A| <= {p}, not Phi_{p}','INFEASIBLE',exists(M,(1,p),[M],[p]))
    t(f'M={M} d  control: Phi_{M}, |A| = {p}','OPTIMAL',exists(M,(p,p),[M],[]))
    # case (d), three pairs: Phi_pq, Phi_pr, Phi_qr, none of Phi_p, Phi_q, Phi_r, |A| <= product of the two smallest
    a,b,c=sorted(P)
    t(f'M={M} d3 all three pairs, no prime, |A| <= {a*b}','INFEASIBLE',exists(M,(1,a*b),[a*b,a*c,b*c],[a,b,c]))
print(f'{n} tests, {bad} not as predicted')
