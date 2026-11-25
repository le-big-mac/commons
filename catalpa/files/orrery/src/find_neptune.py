# Inverse problem: where is the planet that disturbs Uranus?
# Data: true heliocentric lon/lat of Uranus, yearly 1781-1845. Unknown: circular ecliptic planet (a, lon in 1846, mass).
import subprocess, os, numpy as np, tempfile, sys
from multiprocessing import Pool
IC0=np.loadtxt('data/ic.txt'); YEARS=220; DT=-4.0; AS=206264.806
GMS=0.01720209895**2  # approx GM_sun au^3/d^2
# merge Moon into Earth (EMB), Moon made massless
mE,mM=398600.435507,4902.800118
IC=IC0.copy(); IC[3]=(mE*IC0[3]+mM*IC0[4])/(mE+mM)
def run(ic, fac):
    with tempfile.NamedTemporaryFile('w',suffix='.txt',delete=False) as f:
        np.savetxt(f, ic, fmt='%.17e'); p=f.name
    env=dict(os.environ); env['GMFAC']=','.join(f'{x:.12g}' for x in fac)
    out=subprocess.run(['./orrery',p,str(YEARS),str(DT),'1','365.25','state'],capture_output=True,text=True,env=env).stdout
    os.unlink(p)
    a=np.array([l.split() for l in out.splitlines()],float).reshape(-1,11,8)
    yr=2000+(a[:,0,0]-2451545)/365.25
    def ll(i):
        h=a[:,i,2:5]-a[:,0,2:5]
        return np.unwrap(np.arctan2(h[:,1],h[:,0])), np.arcsin(h[:,2]/np.linalg.norm(h,axis=1))
    return yr, ll(8), ll(9)
BASE=np.ones(11); BASE[3]=(mE+mM)/mE; BASE[4]=0
yr,(lon_t,lat_t),(nlon,_)=run(IC,BASE)
obs=(yr>=1781)&(yr<=1845.5)
i46=np.argmin(abs(yr-1846)); true46=np.degrees(nlon[i46])%360
scale=np.array([1e-5]*3+[1e-8]*3+[1.0])
def trial(args):
    a,lam46=args
    n=np.sqrt(GMS/a**3); lam=np.radians(lam46)+n*(2451545-(2451545+(yr[i46]-2000)*365.25))
    ic=IC.copy(); ic[9]=[a*np.cos(lam),a*np.sin(lam),0,-a*n*np.sin(lam),a*n*np.cos(lam),0]; ic[9]+=IC[0]
    def res(p):
        c=ic.copy(); c[8]+=p[:6]*scale[:6]; fac=BASE.copy(); fac[9]=p[6]
        _,(lo,la),_=run(c,fac); return np.concatenate([(lo-lon_t)[obs],(la-lat_t)[obs]])
    p=np.zeros(7); p[6]=1.0
    for it in range(3):
        r=res(p); J=np.zeros((len(r),7))
        for k in range(7):
            q=p.copy(); q[k]+=1 if k<6 else 0.5
            J[:,k]=(res(q)-r)/(1 if k<6 else 0.5)
        p+=np.linalg.lstsq(J,-r,rcond=None)[0]
    r=res(p)
    return a,lam46,np.sqrt(np.mean(r**2))*AS,p[6]
if __name__=='__main__':
    print(f'true Neptune heliocentric longitude in 1846: {true46:.1f} deg (a=30.1 au, mass factor 1)')
    grid=[(a,l) for a in (30.1,38.8) for l in range(0,360,15)]
    with Pool(16) as P: out=P.map(trial,grid)
    for a,l,rms,m in out: print(f'a={a:5.1f} lon1846={l:4.0f}  rms={rms:8.3f}"  mass/Neptune={m:7.3f}')
