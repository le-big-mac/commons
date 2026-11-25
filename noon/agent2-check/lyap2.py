# As lyap.py, but logs growth of the variational vector in SLOW variables (each planet's eccentricity vector),
# where the along-orbit shear that swamps the raw phase-space distance is absent.
import rebound, numpy as np, re, sys, time
src=open('/srv/commons/orrery/src/orrery.c').read()
gm=[float(x) for x in re.search(r'GMkm\[N\] = \{(.*?)\}',src,re.S).group(1).replace('\n',' ').split(',')]
AU=149597870.7; DAY=86400.0; GM=np.array([g*DAY**2/AU**3 for g in gm]); ic=np.loadtxt('/srv/commons/orrery/data/ic.txt')
emb=(GM[3]*ic[3]+GM[4]*ic[4])/(GM[3]+GM[4])
bodies=[(GM[0],ic[0]),(GM[1],ic[1]),(GM[2],ic[2]),(GM[3]+GM[4],emb)]+[(GM[i],ic[i]) for i in (5,6,7,8,9)]
sim=rebound.Simulation(); sim.G=1.0
for m,r in bodies: sim.add(m=m,x=r[0],y=r[1],z=r[2],vx=r[3],vy=r[4],vz=r[5])
sim.move_to_com(); sim.integrator='whfast'; sim.dt=float(sys.argv[2]); sim.init_megno(seed=int(sys.argv[3]))
NR=len(bodies); Tmyr=float(sys.argv[1]); yr=365.25; t0=time.time(); every=float(sys.argv[4]) if len(sys.argv)>4 else 0.1
def evec(r,v,mu):
    h=np.cross(r,v); return np.cross(v,h)/mu-r/np.linalg.norm(r)
def slow():
    p=sim.particles; pv=sim.particles_var; S=p[0]; dS=pv[0]; out=[]; tot=0
    s=np.array([S.x,S.y,S.z,S.vx,S.vy,S.vz]); ds=np.array([dS.x,dS.y,dS.z,dS.vx,dS.vy,dS.vz])
    for i in range(1,NR):
        q=np.array([p[i].x,p[i].y,p[i].z,p[i].vx,p[i].vy,p[i].vz])-s
        dq=np.array([pv[i].x,pv[i].y,pv[i].z,pv[i].vx,pv[i].vy,pv[i].vz])-ds
        tot+=dq@dq; eps=1e-7/np.linalg.norm(dq/np.maximum(np.abs(q),1e-30)); mu=GM[0]+bodies[i][0]
        de=(evec(q[:3]+eps*dq[:3],q[3:]+eps*dq[3:],mu)-evec(q[:3]-eps*dq[:3],q[3:]-eps*dq[3:],mu))/(2*eps)
        out.append(np.log10(np.linalg.norm(de)))
    return np.log10(np.sqrt(tot)),out
print('# t_Myr megno log10|delta| log10|delta e| for Mercury Venus EMB Mars Jupiter Saturn Uranus Neptune',flush=True)
for k in range(1,int(Tmyr/every)+1):
    sim.integrate(k*every*1e6*yr,exact_finish_time=0); d,de=slow()
    print(f'{k*every:.2f} {sim.megno():.3f} {d:.3f} '+' '.join(f'{x:.3f}' for x in de)+f' wall {time.time()-t0:.0f}',flush=True)
