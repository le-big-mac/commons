"""Brute-force test of the class-size caps used with forbidden differences: for every minimal pattern (Z0, n) of Z_M and
every set A (0 in A, |A| = n, zero set containing Z0), the number of elements of A in any residue class mod D is at
most the cap computed in sat.search. Also runs the full model (counts + forbidden differences + caps, no violation
clause) and checks it is satisfiable exactly when such a set exists."""
import sys, itertools, pickle, os
from lp import Setup, divisors
from minimal import analyse
from cyc import zero_set
from sat import search
for M in [int(x) for x in sys.argv[1:]]:
    S=Setup(M); pats=analyse(M); byn={}
    for n,Z,k,st,miss in pats:
        E=S.forbidden_orders(Z); fbs=set(E); ub={}
        for D in divisors(M):
            mm=M//D
            if mm>1:
                allowed=[d for d in divisors(mm) if d>1 and d not in fbs]
                ub[D]=int(Setup(mm).Dplus(allowed)[0]) if allowed else 1
        byn.setdefault(n,[]).append((Z,E,ub,st,S.complement(Z)))
    inc=0; viol=0; cviol=0; exists={}
    for n in byn:
        for rest in itertools.combinations(range(1,M),n-1):
            A=(0,)+rest; ZA=set(zero_set(A,M))
            for Z,E,ub,st,f in byn[n]:
                if set(Z)<=ZA:
                    inc+=1; exists[(n,tuple(Z))]=True
                    from math import gcd
                    if any(sum(f[M//gcd(z-a,M)] for a in A)!=1 for z in range(M)): cviol+=1; print('COVER VIOLATION',M,n,Z,A)
                    for D,cap in ub.items():
                        cnt={}
                        for a in A: cnt[a%D]=cnt.get(a%D,0)+1
                        if max(cnt.values())>cap: viol+=1; print('CAP VIOLATION',M,n,Z,E,D,cap,A)
    mism=0
    for n in byn:
        for Z,E,ub,st,f in byn[n]:
            got=search(M,n,Z,violation=False,workers=1,formulation='counts',forbid=E,cover=f)[0] in('OPTIMAL','FEASIBLE')
            if got!=exists.get((n,tuple(Z)),False): mism+=1; print('MODEL MISMATCH',M,n,Z,got)
    print(f'M={M}: {len(pats)} minimal patterns; incidences {inc}; cap violations {viol}; covering-equation violations {cviol}; realised by some set: {len(exists)}; full-model mismatches {mism}',flush=True)
