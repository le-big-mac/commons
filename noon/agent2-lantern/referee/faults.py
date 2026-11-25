# faults.py: Young's three-rod focusing linkage (Fig. 401), exactness check and fault table.
# Model: thin lens f. x along the track, screen plane at x=0, lantern at x<0.
# I on the box at (O+p, hI); N on the ground at (r, hN); L on the lens slide at (P+q, hL); rods IK=a1, KN=a2, KL=b.
# Nominal: p=2f, q=f, r=0, heights 0, a1=a2=a, b=sqrt(a^2-f^2).
import numpy as np
f=150.0; a=1550.0; Dap=f/4; w=75.0      # mm: focal length, long rods, lens aperture (f/4), width of picture on slide
def lens_pos(O, p=2*f, q=f, r=0.0, hI=0.0, hN=0.0, hL=0.0, a1=a, a2=a, b=None, kf=f):
    if b is None: b=np.sqrt(a*a-kf*kf)
    I=np.array([O+p,hI]); N=np.array([r,hN]); d=N-I; c=np.hypot(*d)
    t=(c*c+a1*a1-a2*a2)/(2*c); h2=a1*a1-t*t
    if h2<0: return np.nan
    e=d/c; n=np.array([-e[1],e[0]])
    if n[1]<0: n=-n
    K=I+t*e+np.sqrt(h2)*n
    s=b*b-(K[1]-hL)**2
    if s<0: return np.nan
    xL=K[0]-np.sqrt(s)          # branch nearer I (enlarged images, m>1)
    return xL-q                  # lens position P
def blur(O,P):
    u=P-O; v=-P; m=v/u
    c=Dap if abs(u-f)<1e-9 else Dap*abs(v-u*f/(u-f))/abs(u*f/(u-f))   # blur circle on the screen, mm (beam is parallel when u=f)
    return m, c, c/(m*w)
def box_for(m):                  # box (object) position for exact focus at magnification m
    u=f*(1+1/m); v=f*(1+m); return -(u+v), -(v)
if __name__=='__main__':
    print('f=%g a=%g b=%.3f (a-b=%.3f) aperture f/4, slide picture %g mm'%(f,a,np.sqrt(a*a-f*f),a-np.sqrt(a*a-f*f),w))
    # 1. exactness of the nominal linkage
    worst=0
    for m in np.linspace(1.02,20,400):
        O,P0=box_for(m); P=lens_pos(O); worst=max(worst,abs(P-P0))
    print('nominal linkage: worst |lens error| over m=1.02..20: %.2e mm'%worst)
    faults=[('IK long 1',dict(a1=a+1)),('KN long 1',dict(a2=a+1)),('IK,KN both long 1',dict(a1=a+1,a2=a+1)),
            ('KL long 1',dict(b=np.sqrt(a*a-f*f)+1)),('all three long 1',dict(a1=a+1,a2=a+1,b=np.sqrt(a*a-f*f)+1)),
            ('KL = IK (rule ignored)',dict(b=a)),
            ('I 1 toward screen',dict(p=2*f+1)),('L 1 toward screen',dict(q=f+1)),('N 1 beyond screen',dict(r=1.0)),
            ('N 35 beyond screen',dict(r=35.0)),
            ('I up 1',dict(hI=1.0)),('L up 1',dict(hL=1.0)),('N up 1 (floor)',dict(hN=1.0)),('N up 10',dict(hN=10.0)),
            ('I and L up 1 (box)',dict(hI=1.0,hL=1.0)),
            ('lens f 1% long (151.5)',None)]
    ms=[1.5,2,5,10,20]
    print('\nlens displacement in mm (+ = toward screen) | blur circle as 1/n of picture width; faults in mm')
    print('%-26s'%'fault'+''.join('   m=%-4g          '%m for m in ms))
    for name,kw in faults:
        row='%-26s'%name
        for m in ms:
            O,P0=box_for(m)
            if kw is None:
                # linkage built for 150 but lens is 151.5: recompute true focus with f'
                P=lens_pos(O); fp=f*1.01; u=P-O; v=-P; vp=u*fp/(u-fp); c=Dap*abs(v-vp)/vp; frac=c/((v/u)*w); dl=np.nan
            else:
                P=lens_pos(O,**kw)
                if np.isnan(P): row+='   jams            '; continue
                dl=P-P0; mm,c,frac=blur(O,P)
            row+=' %+7.2f 1/%-7.0f '%(dl,1/frac if frac>0 else np.inf)
        print(row)

    # as drawn: I is 0.17 f too near the box; KL cut so that focus is right at m=4 (the drawn state)
    from scipy.optimize import brentq
    def err(bb,m=4.0,p=2*f-0.17*f):
        O,P0=box_for(m); return lens_pos(O,p=p,b=bb)-P0
    try:
        bb=brentq(err,a-40,a-0.5)
        print('\nas drawn (I 0.17 f too near the box, KL cut to focus at m=4): KL=%.2f, sqrt(IK^2-KL^2)=%.1f mm (f=150)'%(bb,np.sqrt(a*a-bb*bb)))
        row=''
        for m in [1.5,2,3,4,5,10,20]:
            O,P0=box_for(m); P=lens_pos(O,p=2*f-0.17*f,b=bb); mm,c,frac=blur(O,P); row+='m=%g: %+.2f mm, 1/%.0f;  '%(m,P-P0,1/frac if frac>1e-9 else np.inf)
        print(row)
    except Exception as e: print('as-drawn case failed',e)
