# Independent estimate of the planets' Lyapunov time: REBOUND WHFast + variational equations (MEGNO machinery).
# Newtonian point masses, Sun + 8 planets (Earth and Moon merged at their barycentre), agent1's J2000 state vectors.
import rebound, numpy as np, re, sys, time
src=open('/srv/commons/orrery/src/orrery.c').read()
gm=[float(x) for x in re.search(r'GMkm\[N\] = \{(.*?)\}',src,re.S).group(1).replace('\n',' ').split(',')]
AU=149597870.7; DAY=86400.0; GM=np.array([g*DAY**2/AU**3 for g in gm]); ic=np.loadtxt('/srv/commons/orrery/data/ic.txt')
# order: Sun, Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto
emb=(GM[3]*ic[3]+GM[4]*ic[4])/(GM[3]+GM[4])
bodies=[(GM[0],ic[0]),(GM[1],ic[1]),(GM[2],ic[2]),(GM[3]+GM[4],emb)]+[(GM[i],ic[i]) for i in (5,6,7,8,9)]
sim=rebound.Simulation(); sim.G=1.0
for m,r in bodies: sim.add(m=m,x=r[0],y=r[1],z=r[2],vx=r[3],vy=r[4],vz=r[5])
sim.move_to_com(); sim.integrator='whfast'; sim.dt=float(sys.argv[2]) if len(sys.argv)>2 else 4.0
sim.init_megno(seed=int(sys.argv[3]) if len(sys.argv)>3 else 1)
Tmyr=float(sys.argv[1]); yr=365.25; t0=time.time(); E0=sim.energy()
n=int(Tmyr*10)
for k in range(1,n+1):
    sim.integrate(k*1e5*yr,exact_finish_time=0)
    ly=sim.lyapunov()
    print(f'{k/10:.1f} Myr  megno {sim.megno():.3f}  lyapunov time {1/ly/yr/1e6 if ly>0 else float("inf"):.3f} Myr  dE/E {abs(sim.energy()/E0-1):.1e}  wall {time.time()-t0:.0f}s',flush=True)
