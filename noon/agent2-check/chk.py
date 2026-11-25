import rebound, numpy as np, re, sys
src=open('/srv/commons/orrery/src/orrery.c').read()
gm=[float(x) for x in re.search(r'GMkm\[N\] = \{(.*?)\}',src,re.S).group(1).replace('\n',' ').split(',')]
AU=149597870.7; DAY=86400.0
GM=[g*DAY**2/AU**3 for g in gm]
ic=np.loadtxt('/srv/commons/orrery/data/ic.txt')
gr=int(sys.argv[1])
sim=rebound.Simulation(); sim.G=1.0; sim.integrator='ias15'
for m,row in zip(GM,ic): sim.add(m=m,x=row[0],y=row[1],z=row[2],vx=row[3],vy=row[4],vz=row[5])
c2=(299792.458*DAY/AU)**2
if gr:
    def f(s):
        p=sim.particles; S=p[0]
        for i in range(1,sim.N):
            q=p[i]; r=np.array([q.x-S.x,q.y-S.y,q.z-S.z]); v=np.array([q.vx-S.vx,q.vy-S.vy,q.vz-S.vz])
            rr=np.sqrt(r@r); a=GM[0]/(c2*rr**3)*((4*GM[0]/rr-v@v)*r+4*(r@v)*v)
            q.ax+=a[0]; q.ay+=a[1]; q.az+=a[2]
    sim.additional_forces=f; sim.force_is_velocity_dependent=1
T=400*365.25; ts=np.arange(0,T+1,2.0); out=[]
for t in ts:
    sim.integrate(t); p=sim.particles
    r=np.array([p[1].x-p[0].x,p[1].y-p[0].y,p[1].z-p[0].z]); v=np.array([p[1].vx-p[0].vx,p[1].vy-p[0].vy,p[1].vz-p[0].vz])
    mu=GM[0]+GM[1]; h=np.cross(r,v); e=np.cross(v,h)/mu-r/np.linalg.norm(r)
    n=np.array([-h[1],h[0],0]); Om=np.arctan2(n[1],n[0])
    w=np.arctan2(np.dot(np.cross(n,e),h)/np.linalg.norm(h),np.dot(n,e))
    out.append(Om+w)
y=np.unwrap(out)*206264.806247
print('gr' if gr else 'newton', np.polyfit(ts/36525,y,1)[0])
