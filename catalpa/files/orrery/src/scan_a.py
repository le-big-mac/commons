import sys; sys.path.insert(0,'src')
from find_neptune import *
if __name__=='__main__':
    grid=[(a,l) for a in (24,26,28,30.1,32,34,36,38.8,42) for l in range(295,360,5)]
    with Pool(16) as P: out=P.map(trial,grid)
    for a,l,rms,m in out: print(f'{a:5.1f} {l:4.0f} {rms:8.3f} {m:7.3f}', flush=True)
