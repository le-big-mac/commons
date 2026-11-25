"""Three-prime check of the counts formulation: (1) against the residues formulation on random (pattern, size) cases;
(2) against brute force for small sizes at M=30."""
import sys, random, itertools
from sat import search
from cyc import zero_set
from lp import divisors
from validate import cm_ok
random.seed(3)
for M in (30,42,60):
    O=[d for d in divisors(M) if d>1]; bad=0; sat=[0,0]
    for _ in range(150):
        Z0=sorted(random.sample(O,random.randint(0,min(4,len(O))))); n=random.randint(2,M-1); v=random.random()<.6
        a=search(M,n,Z0,violation=v,workers=1,formulation='residues',time_limit=60)[0]; b=search(M,n,Z0,violation=v,workers=1,formulation='counts',time_limit=60)[0]
        fa=a in('OPTIMAL','FEASIBLE'); fb=b in('OPTIMAL','FEASIBLE'); sat[0]+=fa; sat[1]+=fb
        if fa!=fb or 'UNKNOWN' in (a,b): bad+=1; print('MISMATCH',M,Z0,n,v,a,b)
    print(f'M={M}: 150 random cases, residues vs counts: mismatches {bad}; satisfiable {sat}',flush=True)
M=30; O=[d for d in divisors(M) if d>1]; truth={}
for n in range(1,6):
    for rest in itertools.combinations(range(1,M),n-1):
        A=(0,)+rest; Z=frozenset(zero_set(A,M)); bad=not cm_ok(Z,n,M); e,v=truth.get((Z,n),(False,False)); truth[(Z,n)]=(True,v or bad)
allZ=[frozenset(c) for r in range(0,4) for c in itertools.combinations(O,r)]; mism=0; cases=0
for Z0 in allZ:
    for n in range(1,6):
        ex=any(Z>=Z0 for (Z,k) in truth if k==n); exv=any(Z>=Z0 and v for (Z,k),(e,v) in truth.items() if k==n)
        g1=search(M,n,sorted(Z0),violation=False,workers=1,formulation='counts')[0] in('OPTIMAL','FEASIBLE')
        g2=search(M,n,sorted(Z0),violation=True,workers=1,formulation='counts')[0] in('OPTIMAL','FEASIBLE'); cases+=1
        if g1!=ex or g2!=exv: mism+=1; print('MISMATCH brute',sorted(Z0),n,ex,exv,g1,g2)
print(f'M=30, sizes 1-5, {cases} cases, counts model vs brute force: mismatches {mism}')
