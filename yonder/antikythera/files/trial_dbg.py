import numpy as np, gears, mech, trial
sky, dt = trial.make()
tm = {'then': trial.T0 + trial.SPAN/2, 'now': trial.T1 - trial.SPAN/2}
rs = 360.0/trial.YS
dn = dt/trial.YS
for p in ('mars','jupiter','saturn'):
    rtrue = (360.0*float(1-gears.SYNODIC[p])*dn - trial.PLANT[p])/dt
    for w in ('then','now'):
        s = sky[w]
        sun = mech.fit_sun(s['sun']['jd'], s['sun']['S'], tm[w])
        f = mech.fit_planet(p, s[p]['jd'], s[p]['S'], tm[w], sun)
        Ltrue = (trial.PH0[p] + rtrue*(tm[w]-tm['then'])) % 360
        LsunTrue = (trial.PH0['earth'] + 180 + rs*(tm[w]-tm['then'])) % 360
        print(p, w, 'fit p0 %.4f true %.4f bias %.4f | rate fit %.9f true %.9f diff*dt/2 %.4f | rho %.5f | sun L0 bias %.4f rate diff*span %.5f' % (
            f['p0'], Ltrue, mech.wrap(f['p0']-Ltrue), f['r'], rtrue, (f['r']-rtrue)*dt/2, f['rho'], mech.wrap(sun['L0']-LsunTrue), (sun['r']-rs)*27759))
