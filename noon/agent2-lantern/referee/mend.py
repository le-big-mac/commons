# mend.py: checks of the mended README with the referee's blind program (patch / opening)
import sys, numpy as np
sys.path.insert(0,'/home/agent2/lantern-referee')
import faults as F
f=F.f
def patch(m,ftrue=f,**kw):
    O,P0=F.box_for(m); P=F.lens_pos(O,**kw)
    if np.isnan(P): return 'jams'
    u=P-O; v=-P
    if u<=ftrue: return 'inf'
    vp=u*ftrue/(u-ftrue); return '%.3f'%(abs(v-vp)/vp)
if __name__=='__main__':
    a=11*f; b=np.sqrt(a*a-f*f)
    for e in (1.01,0.99,1.005):
        print('rods of 11 f made for f, the lens really %.3f f:'%e,[patch(m,ftrue=e*f,a1=a,a2=a,b=b) for m in (2,5,10,20)])
    def build(tag,p,r,a1,a2,bb): print(tag,[patch(m,p=p*f,q=f,r=r*f,a1=a1*f,a2=a2*f,b=bb*f) for m in (2,3,3.5,4,4.08,5,6)])
    build('far, rounded 1.84; 3.73,3.67,3.50 ',1.84,0,3.73,3.67,3.50)
    build('far, as read 145/79; rods/79      ',145/79,0,294.878/79,289.928/79,276.525/79)
    build('near, rounded 1.91,0.89           ',1.91,0.89,3.73,3.67,3.50)
    build('near, as read                     ',1.911,0.886,294.878/79,289.928/79,276.525/79)
    for aa in (3.73,6,11,26):
        bb=np.sqrt(aa*aa-1); out=[]
        for deg in (30,60):
            d=2*bb*np.cos(np.radians(deg)); out.append('%d deg: above %.1f'%(deg,(d+np.sqrt(d*d+4))/2))
        d=2*bb/np.sqrt(26); print('rods %g f: KL within'%aa,'; '.join(out),'; locks at friction 0.2 below %.2f; reach %.1f'%((d+np.sqrt(d*d+4))/2,(2*aa+np.sqrt(4*aa*aa-4))/2))
