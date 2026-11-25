"""Validate the CP-SAT model against brute force: for small M, every set of orders Z0 and every size n,
does there exist A (0 in A, |A|=n, zero set containing Z0) [with / without] a T1-or-T2 violation?"""
import sys, itertools, random
from sat import search
from cyc import zero_set
from scan import factor
from lp import divisors
def cm_ok(Z,n,M):
    Zs=set(Z); k=1
    for d in Zs:
        f=factor(d)
        if len(f)==1: k*=next(iter(f))
    if k!=n: return False
    for d in divisors(M):
        f=factor(d)
        if len(f)>=2 and all(q**a in Zs for q,a in f.items()) and d not in Zs: return False
    return True
def truth(M):
    T={}   # (frozenset Z_A, n) -> (exists, exists violating)
    sets={}
    for n in range(1,M+1):
        for rest in itertools.combinations(range(1,M),n-1):
            A=(0,)+rest; Z=frozenset(zero_set(A,M)); bad=not cm_ok(Z,n,M)
            key=(Z,n); a,b=sets.get(key,(False,False)); sets[key]=(True,b or bad)
    return sets
for M in [int(x) for x in sys.argv[1:] if x.isdigit()]:
    sets=truth(M); O=[d for d in divisors(M) if d>1]; random.seed(1)
    allZ=[frozenset(c) for r in range(len(O)+1) for c in itertools.combinations(O,r)]
    tests=[(Z0,n) for Z0 in allZ for n in range(1,M+1)]
    if len(tests)>600: tests=random.sample(tests,600)
    bad=0; nsat=[0,0]
    for Z0,n in tests:
        ex=any(Z>=Z0 for (Z,m) in sets if m==n); exv=any(Z>=Z0 and v for (Z,m),(e,v) in sets.items() if m==n)
        F=sys.argv[-1] if sys.argv[-1] in('counts','residues') else 'residues'
        r1=search(M,n,sorted(Z0),violation=False,workers=1,formulation=F)[0]; r2=search(M,n,sorted(Z0),violation=True,workers=1,formulation=F)[0]
        g1=r1 in('OPTIMAL','FEASIBLE'); g2=r2 in('OPTIMAL','FEASIBLE'); nsat[0]+=g1; nsat[1]+=g2
        if g1!=ex or g2!=exv: bad+=1; print('MISMATCH',M,sorted(Z0),n,'truth',ex,exv,'model',r1,r2)
    print(f'M={M}: {len(tests)} (pattern, size) cases; mismatches {bad}; satisfiable without/with violation: {nsat}',flush=True)
