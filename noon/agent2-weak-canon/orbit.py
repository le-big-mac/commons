import numpy as np
from math import gcd
N=72
A=[0,1,5,6,12,25,29,36,42,48,49,53]; B=[0,8,10,18,26,64]
def tiles(A,B): return sorted((a+b)%N for a in A for b in B)==list(range(N))
units=[u for u in range(N) if gcd(u,N)==1]
orb={}
for u in units:
    Bu=tuple(sorted(u*b%N for b in B))
    assert tiles(A,Bu), u
    orb.setdefault(Bu,[]).append(u)
print('units:',len(units),' distinct complements uB:',len(orb))
for Bu,us in orb.items(): print('  ',Bu,'timbres',sorted((t%12)//2 for t in Bu),'u in',us)
fbar=np.zeros(N)
for u in units:
    for b in B: fbar[u*b%N]+=1/len(units)
print('support of the average:',[t for t in range(N) if fbar[t]>0])
print('weights*24:',[int(round(24*fbar[t])) for t in range(N) if fbar[t]>0])
# check: every pulse gets total weight 1
cov=[sum(fbar[(p-a)%N] for a in A) for p in range(N)]
print('coverage min/max:',min(cov),max(cov),' sum of squares (power) of weights at a pulse, min/max:',min(sum(fbar[(p-a)%N]**2 for a in A) for p in range(N)),max(sum(fbar[(p-a)%N]**2 for a in A) for p in range(N)))
# per-instrument totals (t mod 12)//2
print('per-timbre total weight:',[round(sum(fbar[t] for t in range(0,N,2) if (t%12)//2==i),4) for i in range(6)])
