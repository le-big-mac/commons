"""The 0.4 degree bias of circle-fit mean longitudes on the made-up sky: the steps of trial_dbg.py, run from here
(python -I -B so that nothing is written beside the author's files)."""
import sys
sys.path.insert(0, '/home/agent3/antikythera')
import numpy as np, gears, mech, trial
sky, dt = trial.make()
tm = {'then': trial.T0 + trial.SPAN / 2, 'now': trial.T1 - trial.SPAN / 2}
rs = 360.0 / trial.YS; dn = dt / trial.YS
for p in ('mars', 'jupiter', 'saturn'):
    rtrue = (360.0 * float(1 - gears.SYNODIC[p]) * dn - trial.PLANT[p]) / dt
    out = []
    for w in ('then', 'now'):
        s = sky[w]
        sun = mech.fit_sun(s['sun']['jd'], s['sun']['S'], tm[w])
        f = mech.fit_planet(p, s[p]['jd'], s[p]['S'], tm[w], sun)
        Ltrue = (trial.PH0[p] + rtrue * (tm[w] - tm['then'])) % 360
        bias_c = float(mech.wrap(f['p0'] - Ltrue))
        edge_t = s[p]['jd'][0] if w == 'then' else s[p]['jd'][-1]
        bias_e = float(mech.wrap(f['p0'] + f['r'] * (edge_t - tm[w]) - (trial.PH0[p] + rtrue * (edge_t - tm['then']))))
        out.append((bias_c, bias_e))
        print(f'{p:8s} {w:5s} circle-fit mean longitude minus planted: at window centre {bias_c:+.3f}, at the outer edge {bias_e:+.3f}; rate difference x 38 years {(f["r"] - rtrue) * 13879.5:+.3f}')
    print(f'{p:8s} drift error if circle fits were used: centre to centre {-(out[1][0] - out[0][0]):+.3f}, edge to edge {-(out[1][1] - out[0][1]):+.3f}')
