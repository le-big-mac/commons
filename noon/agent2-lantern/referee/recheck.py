# recheck.py: the README's table of faults recomputed by the referee's own blind program (faults.py),
# in the README's measure (patch / lens opening), rods of 11 f; plus rows the README leaves out, and the thrust in KL.
import sys, numpy as np
sys.path.insert(0,'/home/agent2/lantern-referee')
import faults as F
if __name__=='__main__':
    f=F.f; a=11*f; b0=np.sqrt(a*a-f*f); ms=[2,5,10,20]
    def row(name,**kw):
        out=[]
        for m in ms:
            O,P0=F.box_for(m); kk=dict(a1=a,a2=a,b=b0); kk.update(kw)
            P=F.lens_pos(O,**kk)
            if np.isnan(P): out.append('jams '); continue
            u=P-O; v=-P
            if u<=f: out.append('inf  '); continue
            vp=u*f/(u-f); out.append('%.3f'%(abs(v-vp)/vp))
        print('%-52s'%name,'  '.join(out))
    print('a-b = %.4f f'%((a-b0)/f))
    row('none')
    row('k=1.01 f^2',b=np.sqrt(a*a-1.01*f*f))
    row('N 0.01 f above',hN=0.01*f); row('N 0.1 f above',hN=0.1*f)
    row('KN longer 1/1000',a2=a*1.001); row('all three longer 1/1000',a1=a*1.001,a2=a*1.001,b=b0*1.001)
    row('I 0.01 f too far',p=2.01*f); row('L 0.01 f too far',q=1.01*f); row('L 0.02 f above',hL=0.02*f)
    print('--- rows the README does not have')
    row('KL alone longer 1/1000 (2.19 mm at f=200)',b=b0*1.001)
    row('KL alone longer 1/10000 (0.22 mm at f=200)',b=b0*1.0001)
    row('IK alone longer 1/1000',a1=a*1.001)
    row('IK and KN both longer 1/1000, KL right',a1=a*1.001,a2=a*1.001)
    row('I 0.02 f above the line',hI=0.02*f)
    print('1 part in 100 of f^2 is a KL wrong by %.6f f = 1 part in %.0f of its length = %.3f mm at f=200'%(0.01*f*f/(2*b0)/f, b0/(0.01*f*f/(2*b0)), 0.01*200*200/(2*b0/f*200)))
    print('--- KL against the slide: angle, thrust per unit push, friction needed to lock (mu > 1/tan)')
    for aa in (3.7,6,11):
        bb=np.sqrt(aa*aa-1); s=''
        for m in (1.5,2,3,5,10,20):
            ML=(m-1/m)/2
            if ML>bb: s+='m=%g: out of reach; '%m; continue
            h=np.sqrt(bb*bb-ML*ML); s+='m=%g: %.0f deg, x%.1f, mu>%.2f; '%(m,np.degrees(np.arctan2(h,ML)),bb/ML,ML/h)
        print('rods %g f: '%aa+s)
    # bending at length: deal lath 20 mm square, E=10 GPa, 500 kg/m3
    for L in (2.2,5.2):
        E=1e10; I=0.02**4/12; w=500*9.81*4e-4; sag=5*w*L**4/(384*E*I); print('lath 20 mm, %.1f m: sag level %.1f mm, chord shorter %.3f mm, Euler %.0f N'%(L,sag*1e3,8*sag**2/(3*L)*1e3,np.pi**2*E*I/L**2))
    # cam: largest radius by the README's rule
    for m1 in (3,2,1.5,1.2):
        T=(20+1/20+2)-(m1+1/m1+2); print('cam from %g: r >= %.2f f'%(m1,(T/np.radians(300))/(m1*m1-1)/np.tan(np.radians(30))))
