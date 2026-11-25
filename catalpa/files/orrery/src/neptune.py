# The Neptune problem: fit a Neptune-less solar system to "observations" of Uranus 1781-1821,
# then watch the residuals grow up to 1846.
import subprocess, os, numpy as np, tempfile
IC=np.loadtxt('data/ic.txt'); YEARS=220; DT=-0.5
def run(ic, noneptune):
    with tempfile.NamedTemporaryFile('w',suffix='.txt',delete=False) as f:
        np.savetxt(f, ic, fmt='%.17e'); p=f.name
    env=dict(os.environ); 
    if noneptune: env['NONEPTUNE']='1'
    out=subprocess.run(['./orrery',p,str(YEARS),str(DT),'1','365.25','state'],capture_output=True,text=True,env=env).stdout
    os.unlink(p)
    a=np.array([l.split() for l in out.splitlines()],float).reshape(-1,11,8)
    yr=2000+(a[:,0,0]-2451545)/365.25
    h=a[:,8,2:5]-a[:,0,2:5]           # heliocentric Uranus
    lon=np.unwrap(np.arctan2(h[:,1],h[:,0])); lat=np.arcsin(h[:,2]/np.linalg.norm(h,axis=1))
    return yr, lon, lat
AS=206264.806
yr, lon_t, lat_t = run(IC, False)
fit=(yr>=1781)&(yr<=1821)
def resid(dp):
    ic=IC.copy(); ic[8]+=dp*scale
    _,lon,lat=run(ic,True)
    return lon-lon_t, lat-lat_t
scale=np.array([1e-5]*3+[1e-8]*3)
p=np.zeros(6)
for it in range(6):
    dl,db=resid(p); r=np.concatenate([dl[fit],db[fit]])
    J=np.zeros((len(r),6))
    for k in range(6):
        q=p.copy(); q[k]+=1
        a,b=resid(q); J[:,k]=np.concatenate([a[fit],b[fit]])-r
    step=np.linalg.lstsq(J,-r,rcond=None)[0]; p+=step
    print(f'iter {it}: rms fit residual {np.sqrt(np.mean(r**2))*AS:.3f}"')
dl,db=resid(p)
print('year   longitude residual (model without Neptune minus truth), arcsec')
for y,d in sorted(zip(yr,dl)):
    if 1780<y<1847 and round(y)%5==0 or round(y) in (1846,): print(f'{y:7.0f} {d*AS:9.2f}')
np.savetxt('neptune_resid.txt', np.c_[yr,dl*AS,db*AS])
