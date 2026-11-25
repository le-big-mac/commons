import numpy as np, sys
from collections import Counter
from fractions import Fraction
import margin
from multiprocessing import Pool
M=int(sys.argv[1]); b=np.loadtxt(sys.argv[2],dtype=np.int64)
if __name__=='__main__':
    with Pool(14) as p: v=np.concatenate(p.map(margin.chunk,[(M,b[i:i+2000]) for i in range(0,len(b),2000)]))
    n=np.array([bin(int(x)).count('1') for x in b])
    c=Counter(); bad=0
    for val,sz in zip(v,n):
        if val>1-1e-7: continue
        fr=Fraction(float(val)).limit_denominator(200)
        if abs(float(fr)-val)>1e-9: bad+=1
        k=fr*int(sz)                       # value = k/|A| ?
        c[(str(fr), 'k=%s'%k, 'k|M' if k.denominator==1 and M%k.numerator==0 else 'k not a divisor of M')]+=1
    print('not rational with small denominator:',bad)
    for key,cnt in sorted(c.items(),key=lambda x:-x[1])[:14]: print(cnt,key)
    print('rejected values of the form (divisor of M)/|A|:',sum(cnt for k,cnt in c.items() if k[2]=='k|M'),'of',sum(c.values()))
