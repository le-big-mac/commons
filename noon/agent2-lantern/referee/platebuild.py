# platebuild.py: a lantern built to the plate by each of the README's two readings, in the README's measure (patch/opening)
import sys, numpy as np
sys.path.insert(0,'/home/agent2/lantern-referee')
import faults as F
if __name__=='__main__':
    f=F.f
    def run(name,p,r,a1,a2,b,ms=(1.5,2,2.5,3,3.16,3.5,4,4.1,5,6,7)):
        s=''
        for m in ms:
            O,P0=F.box_for(m); P=F.lens_pos(O,p=p*f,q=f,r=r*f,a1=a1*f,a2=a2*f,b=b*f)
            if np.isnan(P): s+='%g: jams; '%m; continue
            u=P-O; v=-P
            if u<=f: s+='%g: inf; '%m; continue
            vp=u*f/(u-f); s+='%g: %.3f; '%(m,abs(v-vp)/vp)
        print(name,s)
    IK,KN,KL=294.878/79,289.928/79,276.525/79
    run('second reading (near face the screen; I 1.91 f, N 0.89 f behind):',1.911,0.886,IK,KN,KL)
    run('first reading (far face the screen; I 1.84 f, N at the screen):  ',145/79,0.0,IK,KN,KL)
    run('first reading, rods taken equal (3.70 f) and KL to fit IL x LN:   ',145/79,0.0,3.70,3.70,np.sqrt(3.70**2-32*322/79**2))
