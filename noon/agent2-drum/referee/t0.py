import sys, time
sys.path.insert(0, '/home/agent2/drum/referee')
import numpy as np
from mem import *
t=time.time()
for i in range(50): x=miss(ratios(step(10,0.4),[0.4],300))
print('per obj N=300: %.2f ms'%((time.time()-t)/50*1e3), x)
t=time.time(); r=ratios(lambda x: np.ones_like(x),[],2000,rich=True); print(r, time.time()-t)
print(ratios(step(10,0.4),[0.4],3000,rich=True))
print(bessel_step(10,0.4,0,3), bessel_step(10,0.4,1,2))
