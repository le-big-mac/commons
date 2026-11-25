# q2.py: rods with KN = KL (the Britannica's words), pivots in a line, N at the screen, I at 2f - s before the slider, L under the focus.
# Power of the point I about the circle centre K through L and N: IL x IN = IK^2 - KL^2 = c2.
# Lantern stands where a sharp image would be m times: d = x + y = f(m + 1/m), x = lens beyond... (slider beyond focus), y = screen beyond focus.
import numpy as np
from scipy.optimize import minimize
def patch(m,c2=1.0,s=0.0):
    d=m+1/m                       # f = 1
    xr=c2/(d+s)-s                 # where the rods put x: (x+s)(d+s)=c2
    if xr<=0: return np.inf
    return abs(d-xr-1/xr)/(1+1/xr)   # |v-v'|/v', v=1+d-xr, v'=1+1/xr
def worst(par,lo,hi,two):
    ms=np.exp(np.linspace(np.log(lo),np.log(hi),600)); c2=par[0]; s=par[1] if two else 0.0
    return max(patch(m,c2,s) for m in ms)
if __name__=='__main__':
    # check the power-of-a-point claim by coordinates
    rng=np.random.default_rng(1); bad=0
    for _ in range(1000):
        b=rng.uniform(1,10); xL=rng.uniform(0.1,3); xN=xL+rng.uniform(0.2,1.9)*b; xK=(xL+xN)/2; h=np.sqrt(b*b-((xN-xL)/2)**2)
        IK2=xK**2+h**2; bad=max(bad,abs(xL*xN-(IK2-b*b)))
    print('IL x IN = IK^2 - KL^2 when KN = KL: worst difference in 1000 cases %.1e'%bad)
    print('c = f (right for a very large image): patch at 2,3,5,10,20:',['%.4f'%patch(m) for m in (2,3,5,10,20)])
    print('  closed form m^2/((m^2+1)(m^2+m+1)):',['%.4f'%(m*m/((m*m+1)*(m*m+m+1))) for m in (2,3,5,10,20)])
    for lo,hi in ((2,20),(5,20)):
        best=min((minimize(worst,[c0],args=(lo,hi,False),method='Nelder-Mead',options={'xatol':1e-7,'fatol':1e-9}) for c0 in (0.9,1.0,1.1,1.3)),key=lambda r:r.fun)
        print('%g to %g, KL trimmed only: IK^2-KL^2 = %.4f f^2, worst patch %.4f; patches at ends/mid:'%(lo,hi,best.x[0],best.fun),['%g: %.4f'%(m,patch(m,best.x[0])) for m in (2,3,5,10,20) if lo<=m<=hi])
        b2=min((minimize(worst,[c0,s0],args=(lo,hi,True),method='Nelder-Mead',options={'xatol':1e-7,'fatol':1e-10,'maxiter':4000}) for c0 in (0.8,1.0,1.3,2.0) for s0 in (-0.3,-0.1,0.0,0.1,0.3,1.0)),key=lambda r:r.fun)
        print('%g to %g, KL trimmed and I moved: IK^2-KL^2 = %.4f f^2, I %.4f f nearer the slider (p = %.4f f), worst patch %.5f;'%(lo,hi,b2.x[0],b2.x[1],2-b2.x[1],b2.fun),['%g: %.4f'%(m,patch(m,b2.x[0],b2.x[1])) for m in (2,3,5,10,20) if lo<=m<=hi])
