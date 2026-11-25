"""Machine check of the two lemmas for M = p^4 q^2, n = p^2 q:
 (a) no A, |A| = n, with Phi_d | A for d in {q, p^4, p^4 q, p^3 q, p^3 q^2, p^2 q^2}
 (b) no B, |B| = n, with Phi_d | B for d in {p^2, p^3, q^2, pq, pq^2, p^2 q}
and whether each hypothesis is needed (drop one divisor at a time)."""
import sys
from sat import search
from cyc import zero_set
for p,q in [(2,3),(2,5),(2,7),(3,5)]:
    M=p**4*q**2; n=p*p*q
    pa=[q,p**4,p**4*q,p**3*q,p**3*q*q,p*p*q*q]; pb=[p*p,p**3,q*q,p*q,p*q*q,p*p*q]
    for name,Z in (('a',pa),('b',pb)):
        st,A,t=search(M,n,Z,time_limit=900,workers=6,violation=False,formulation='counts')
        print(f'p={p} q={q} M={M} n={n} lemma ({name}) full hypothesis {sorted(Z)}: {st} {t:.1f}s',flush=True)
        if M<=400:
            for d in Z:
                Z2=[e for e in Z if e!=d]
                st,A,t=search(M,n,Z2,time_limit=300,workers=6,violation=False,formulation='counts')
                print(f'      without Phi_{d}: {st} {t:.1f}s',('example '+str(A)) if A else '',flush=True)
