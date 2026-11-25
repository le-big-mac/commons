# asdrawn.py: the linkage built to the proportions of the engraving: I 0.17 f too near the box, IK^2-KL^2 = 1.68 f^2
# (which makes the drawn state, m=4, in focus), tried at other sizes. Also the plate arithmetic.
import numpy as np, importlib.util, sys
sys.path.insert(0,'/home/agent2/lantern-referee')
import faults as F
if __name__=='__main__':
    f,a=F.f,F.a; eps=0.17*f; b=np.sqrt(a*a-(f*f+4*f*eps))
    row=''
    for m in [1.5,2,3,4,5,10,20]:
        O,P0=F.box_for(m); P=F.lens_pos(O,p=2*f-eps,b=b); mm,c,frac=F.blur(O,P)
        row+='m=%g: %+.2f mm, 1/%.0f;  '%(m,P-P0,1/frac if frac>1e-9 else np.inf)
    print('built as drawn:',row)
    # plate arithmetic (pixels)
    I=np.array([1022.,980.]); L=np.array([1055.5,984.]); K=np.array([1208.,755.]); N=np.array([1375.,990.])
    lens=976.; obj=876.; scr=1376.5
    IK=np.hypot(*(I-K)); KL=np.hypot(*(L-K)); KN=np.hypot(*(N-K))
    print('IK %.1f KN %.1f KL %.1f; IK^2-KL^2=%.0f (sqrt %.1f); LI*LN=%.0f (sqrt %.1f)'%(IK,KN,KL,IK**2-KL**2,np.sqrt(IK**2-KL**2),(L[0]-I[0])*(N[0]-L[0]),np.sqrt((L[0]-I[0])*(N[0]-L[0]))))
    u=lens-obj; v=scr-lens; print('u %.1f v %.1f m %.2f f(optics) %.1f; f(L)=%.1f; I-obj=%.1f = %.2f f(L)'%(u,v,v/u,u*v/(u+v),L[0]-lens,I[0]-obj,(I[0]-obj)/(L[0]-lens)))
    print('slope I-N %.4f; L below line I-N by %.1f px'%((N[1]-I[1])/(N[0]-I[0]), L[1]-(I[1]+(N[1]-I[1])*(L[0]-I[0])/(N[0]-I[0]))))
    # Monte Carlo of reading errors: sd 2.5 (I), 1.5 (L), 2 (K), 2 (N), 2 lens, 2 obj, 2 screen
    rng=np.random.default_rng(401); n=20000
    Ix=I[0]+2.5*rng.standard_normal(n); Iy=I[1]+2.5*rng.standard_normal(n); Lx=L[0]+1.5*rng.standard_normal(n); Ly=L[1]+1.5*rng.standard_normal(n)
    Kx=K[0]+2*rng.standard_normal(n); Ky=K[1]+2*rng.standard_normal(n); Nx=N[0]+2*rng.standard_normal(n); Ny=N[1]+2*rng.standard_normal(n)
    le=lens+2*rng.standard_normal(n); ob=obj+2*rng.standard_normal(n); sc=scr+2*rng.standard_normal(n)
    ik=np.hypot(Ix-Kx,Iy-Ky); kl=np.hypot(Lx-Kx,Ly-Ky); kn=np.hypot(Nx-Kx,Ny-Ky)
    fo=(le-ob)*(sc-le)/(sc-ob); fL=Lx-le
    def pr(t,x): print('%-34s %.1f +- %.1f'%(t,x.mean(),x.std()))
    pr('IK-KN',ik-kn); pr('sqrt(IK^2-KL^2)',np.sqrt(np.abs(ik**2-kl**2))); pr('sqrt(LI*LN)',np.sqrt((Lx-Ix)*(Nx-Lx)))
    pr('f from u,v',fo); pr('f from L under focus',fL); pr('(I-obj)/2',(Ix-ob)/2); pr('I-obj minus 2 f(u,v)',Ix-ob-2*fo); pr('LI',Lx-Ix); pr('u-f(u,v) (what LI should be)',le-ob-fo)
    pr('N minus far face',Nx-sc); pr('slope I-N x1000',1000*(Ny-Iy)/(Nx-Ix))
