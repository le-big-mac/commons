# Score the sealed forecast against observations that did not exist when it was made.  Written before any of them were fetched.
# usage: python -I score.py <window start 'YYYY-MM-DD HH:MM'> <window end>      (fetch the new observations first: ./fetch.sh <station> 20261114 2 force)
import numpy as np, sys, csv
sys.path.insert(0, '/home/agent1/tides')
from tide import *
a, b = day_of(sys.argv[1]), day_of(sys.argv[2])
def peaks(t, y):
    """times of high waters: maxima of a 30-minute running mean, at least 6 hours apart"""
    k = 5; ys = np.convolve(y, np.ones(k) / k, 'same'); out = []
    for i in range(k, len(ys) - k):
        if ys[i] == ys[max(0, i - 30):i + 31].max() and (not out or t[i] - out[-1] > 0.25): out.append(t[i])
    return np.array(out)
print(f'window {sys.argv[1]} to {sys.argv[2]} UTC')
print('station                 hours with data   sd(obs - mine)   sd(obs - NOAA)   ratio    mean(obs - mine)   mean(obs - NOAA)    high waters: n, mean |time error| mine, NOAA (min)   [cm]')
for st, (name, lon) in STATIONS.items():
    rows = list(csv.DictReader(open(f'/home/agent1/tides/forecast_{st}.csv'))); tf = np.array([day_of(r['UTC']) for r in rows]); mine = np.array([float(r['mine_m']) for r in rows]); noaa = np.array([float(r['noaa_m']) for r in rows]); om = np.array([float(r['mine_offset_m']) for r in rows]); on = np.array([float(r['noaa_offset_m']) for r in rows])
    t, y = load_noaa(st, 'water_level'); mk = (t >= a) & (t <= b); t, y = t[mk], y[mk]
    if len(t) < 20: print(f'{name}: no observations yet in the window'); continue
    m6, n6 = np.interp(t, tf, mine), np.interp(t, tf, noaa); hr = np.abs((t * 24) % 1.0) < 1e-6
    em, en = (y - m6)[hr], (y - n6)[hr]
    po = peaks(t, y); fm = (tf >= a - 0.3) & (tf <= b + 0.3); pm, pn = peaks(tf[fm], mine[fm]), peaks(tf[fm], noaa[fm])
    po = po[(po > a + 0.1) & (po < b - 0.1)]
    dm = np.array([np.abs(pm - p).min() for p in po]) * 1440 if len(po) and len(pm) else np.array([np.nan]); dn = np.array([np.abs(pn - p).min() for p in po]) * 1440 if len(po) and len(pn) else np.array([np.nan])
    print(f'{name:22s}  {hr.sum():5d}             {100 * em.std():6.2f}           {100 * en.std():6.2f}        {em.std() / en.std():5.2f}      {100 * em.mean():+6.2f}             {100 * en.mean():+6.2f}              {len(po):2d}   {np.mean(dm):5.1f}   {np.mean(dn):5.1f}')
    lm, ln = (y - m6 - np.interp(t, tf, om))[hr], (y - n6 - np.interp(t, tf, on))[hr]; rms = lambda v: 100 * np.sqrt((v ** 2).mean())
    print(f'      level forecast (tide + carried offset), rms error in cm: mine {rms(lm):.2f}, NOAA with the same recipe {rms(ln):.2f}, NOAA as published {rms(en):.2f}')
