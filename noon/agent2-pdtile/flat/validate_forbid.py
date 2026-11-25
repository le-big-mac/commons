"""Brute-force test of the 'forbidden difference orders' statement: for every minimal pattern (Z0, n) of Z_M and every
set A with 0 in A, |A| = n, zero set containing Z0: no two elements of A differ by an element whose order is forbidden.
Also reports how many such sets there are, and that the forbidden list is not vacuous."""
import sys, itertools, pickle, os
from math import gcd
from lp import Setup
from minimal import analyse
from cyc import zero_set
from scan import scan
for M in [int(x) for x in sys.argv[1:]]:
    if not os.path.exists(f'D_{M}.pkl'):
        O,D=scan(M); pickle.dump((O,D),open(f'D_{M}.pkl','wb'))
    S=Setup(M); pats=analyse(M); order=lambda x:M//gcd(x,M)
    byn={}
    for n,Z,k,st,miss in pats: byn.setdefault(n,[]).append((Z,S.forbidden_orders(Z),st))
    nsets=0; viol=0; nonvac=sum(1 for n in byn for Z,E,st in byn[n] if E); tot=sum(len(v) for v in byn.values())
    for n in byn:
        if n>M//2+2 and M>24: continue
        for rest in itertools.combinations(range(1,M),n-1):
            A=(0,)+rest; ZA=set(zero_set(A,M))
            for Z,E,st in byn[n]:
                if set(Z)<=ZA:
                    nsets+=1
                    if any(order(b-a) in E for a,b in itertools.combinations(A,2)): viol+=1; print('VIOLATION',M,n,Z,E,A)
    print(f'M={M}: {tot} minimal patterns ({nonvac} with a nonempty forbidden list); (set, pattern) incidences checked {nsets}; violations {viol}',flush=True)
