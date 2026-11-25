"""Item 4, anomalies: the Moon's and the Sun's mean anomalies at the first full moon of each start, from the time-based mean elements
(Meeus ch. 47, typed by the checker from memory: M' = 134.9633964 + 477198.8675055 T + ..., M = 357.5291092 + 35999.0502909 T - ...),
evaluated at the instant of true full moon; scores from the checker's c4_all.json."""
import sys, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, own, phases
S = {int(k): v for k, v in json.load(open(os.path.join(HERE, 'c4_all.json')))['18'].items()}
K = sorted(S); K0 = -27255.5
def anom(jde):
    T = (jde - 2451545.0) / 36525.0
    Mp = 134.9633964 + 477198.8675055 * T + 0.0087414 * T * T + T ** 3 / 69699.0 - T ** 4 / 14712000.0
    M = 357.5291092 + 35999.0502909 * T - 0.0001536 * T * T + T ** 3 / 24490000.0
    return M % 360, Mp % 360
w = lambda x: (x + 180) % 360 - 180
full, new = own.syz('then')
M0, Mp0 = anom(full[0])
print(f'first full moon of 205 BC (JPL instant {full[0]:.4f}): Moon\'s mean anomaly {Mp0:.2f} (180 = apogee; {Mp0 - 180:+.2f} from apogee), Sun\'s {M0:.2f} ({M0 - 180:+.2f} from apogee)')
t_mean = 2451550.09766 + 29.530588861 * K0 + 0.00015437 * (K0 / 1236.85) ** 2
Mm, Mpm = anom(t_mean)
print(f'   at the mean full moon ({t_mean:.4f}, {(t_mean - full[0]) * 24:+.1f} h from the true): Moon {Mpm:.2f} ({Mpm - 180:+.2f}), Sun {Mm:.2f} ({Mm - 180:+.2f});  Jones (Almagest, at mean syzygy): Moon -7 08\', Sun -18 25\'')
# movement in 223 and 767 synodic months
syn = 29.530588861; anm = 27.554549878; any_ = 365.259636
for n in (223, 767, 47, 14, 85, 112, 183, 210, 98, 669):
    d = n * syn
    print(f'   {n:4d} months = {d:10.3f} d: Moon\'s anomaly {w(360 * d / anm):+7.2f}, Sun\'s {w(360 * d / any_):+7.2f}  (with a 365.25-day year {w(360 * d / 365.25):+.2f}; tropical {w(360 * d / 365.24219):+.2f}); days over whole {d % 1:.4f} = {(d % 1) * 360:.1f} deg of turning')
dM = np.array([w(anom(phases.true_phase(K0 + k))[1] - Mp0) for k in K]); dS = np.array([w(anom(phases.true_phase(K0 + k))[0] - M0) for k in K]); s = np.array([S[k][0] for k in K])
for thr in (2.3, 2.556, 3.0):
    g = s < thr
    print(f'starts under {thr} h: {int(g.sum())}; Moon\'s anomaly against 205 BC {dM[g].min():+.1f} to {dM[g].max():+.1f}, mean {dM[g].mean():+.1f}, sd {dM[g].std():.1f}; Sun\'s {dS[g].min():+.1f} to {dS[g].max():+.1f}, mean {dS[g].mean():+.1f}, sd {dS[g].std():.1f}')
g = s < 2.3
print(f'   so the thirty best have the Moon\'s anomaly at {Mp0 + dM[g].mean():.1f} on average and the Sun\'s at {M0 + dS[g].mean():.1f}; Carman and Evans, Table 12, row "Excluding 13S, 120M, 125M, 184M": Moon 184.7, Sun 180.4')
# how sharply the score depends on the Moon's anomaly: all starts with |dS| < 25, score against dM in bins
print('median score by the Moon\'s anomaly against 205 BC (all starts; bins of 10 deg):')
for lo in range(-40, 60, 10):
    m = (dM >= lo) & (dM < lo + 10)
    print(f'   {lo:+4d}..{lo + 10:+4d}: n {int(m.sum()):3d}  best {s[m].min():.2f}  median {np.median(s[m]):.2f}')
# is 205 BC's shortfall "meaningful"?  the best score among starts whose anomalies are within 3 deg (Moon) and 12 deg (Sun) of 205 BC's
m = (np.abs(dM) < 3.5) & (np.abs(dS) < 12)
print('starts with the Moon within 3.5 and the Sun within 12 deg of 205 BC\'s anomalies:', [(K[i], round(s[i], 2), round(dM[i], 1), round(dS[i], 1)) for i in np.where(m)[0]])
