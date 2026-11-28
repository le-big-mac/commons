# The model with the Hunga haze, against the same model with the haze of the comparison years.
# Light scattered once and twice by direct sums in each atmosphere; three times and more by Monte Carlo on paths drawn
# in the haziest atmosphere and weighted for each of the others. Seven wavelengths over the meters' band; depths 3 to 11.
# usage: run_haze.py OUT.pkl NPHOTONS "dict(z0=21.0, fwhm=5.0)"
import sys, pickle, time, importlib.util
import numpy as np
from multiprocessing import Pool
spec = importlib.util.spec_from_file_location('twimc', '/home/agent1/night/model/twimc.py'); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
spec = importlib.util.spec_from_file_location('run_clear', '/home/agent1/night/model/run_clear.py'); RC = importlib.util.module_from_spec(spec); spec.loader.exec_module(RC)
LAMS = RC.LAMS; DEPTHS = RC.DEPTHS
BG = dict(tau=0.008, z0=19.0, fwhm=9.0, rm=0.18, sigma=1.37)                 # the haze of the comparison years
PLUME = dict(rm=0.35, sigma=1.23)                                            # the Hunga droplets
TAUS = (0.022, 0.018, 0.014)                                                 # the plume's optical depth at 550 nm: high, central, low
CLEAR = dict(trop_tau=0.03, o3_du=300.0, albedo=0.15)
def atms(lam, z0, fwhm):
    out = [M.atmosphere(float(lam), layers=[BG, dict(PLUME, tau=t, z0=z0, fwhm=fwhm)], **CLEAR) for t in TAUS]
    out.append(M.atmosphere(float(lam), layers=[BG], **CLEAR)); return out      # last: no plume
def job(a):
    lam, dep, z0, fwhm, N, seed = a; A = atms(lam, z0, fwhm); res = dict(L1=[], L2=[])
    for at in A:
        res['L1'].append(M.single(at, float(dep))[0]); res['L2'].append(M.second(at, float(dep), M.sun_table(at), nel=96, naz=32, ns=140))
    nb = max(1, N // 20000); L3 = np.zeros((nb, len(A))); L2mc = np.zeros((nb, len(A)))
    for b in range(nb):
        L, per = M.paired(A[0], A[1:], float(dep), N=20000, seed=seed * 100000 + int(lam) * 100 + int(dep) * 7 + b); L3[b] = L[:, 3:].sum(axis=1) / 20000; L2mc[b] = L[:, 2] / 20000
    res['L3'] = L3; res['L2mc'] = L2mc; return (lam, dep), res
def band(R, dep, i, part):
    w = np.array([RC.SUN[l] * RC.RESP[l] for l in LAMS])
    if part == 'L3': v = np.array([R[(l, dep)]['L3'][:, i].mean() for l in LAMS])
    elif part == 'L2mc': v = np.array([R[(l, dep)]['L2mc'][:, i].mean() for l in LAMS])
    else: v = np.array([R[(l, dep)][part][i] for l in LAMS])
    return float((w * v).sum())
def table(R, names=('plume 0.022', 'plume 0.018', 'plume 0.014', 'no plume')):
    out = {}
    print('depth   the comparison years: once, twice, more (share more than once)   | brightening in magnitudes (negative: brighter), plume optical depth 0.022, 0.018, 0.014 | by the batches of the Monte Carlo, central: spread of the brightening')
    for d in DEPTHS:
        tot = [band(R, d, i, 'L1') + band(R, d, i, 'L2') + band(R, d, i, 'L3') for i in range(4)]
        dm = [-2.5 * np.log10(tot[i] / tot[3]) for i in range(3)]; out[d] = dm
        w = np.array([RC.SUN[l] * RC.RESP[l] for l in LAMS]); nb = R[(LAMS[0], d)]['L3'].shape[0]
        bt = []
        for b in range(nb):
            t1 = sum(w[j] * (R[(l, d)]['L1'][1] + R[(l, d)]['L2'][1] + R[(l, d)]['L3'][b, 1]) for j, l in enumerate(LAMS)); t0 = sum(w[j] * (R[(l, d)]['L1'][3] + R[(l, d)]['L2'][3] + R[(l, d)]['L3'][b, 3]) for j, l in enumerate(LAMS))
            bt.append(-2.5 * np.log10(t1 / t0))
        l1, l2, l3 = band(R, d, 3, 'L1'), band(R, d, 3, 'L2'), band(R, d, 3, 'L3')
        print(f'  {d:2d}°   {l1:.3e} {l2:.3e} {l3:.3e} ({(l2 + l3) / (l1 + l2 + l3):.2f})   |   {dm[0]:+.3f}  {dm[1]:+.3f}  {dm[2]:+.3f}   |   +- {np.std(bt) / np.sqrt(nb):.3f}   (twice-scattered, direct sums against Monte Carlo, no plume: {band(R, d, 3, "L2"):.3e} {band(R, d, 3, "L2mc"):.3e})')
    return out
if __name__ == '__main__':
    outp = sys.argv[1]
    if len(sys.argv) > 2:
        N = int(sys.argv[2]); kw = eval(sys.argv[3]) if len(sys.argv) > 3 else dict(z0=21.0, fwhm=5.0); t0 = time.time()
        jobs = [(l, d, kw['z0'], kw['fwhm'], N, 11) for l in LAMS for d in DEPTHS]
        with Pool(15) as p: R = dict(p.map(job, jobs, chunksize=1))
        pickle.dump(dict(R=R, kw=kw, N=N), open(outp, 'wb')); print(f'{len(jobs)} cases, {N} photons each, {time.time() - t0:.0f} s; layer {kw}', file=sys.stderr)
    X = pickle.load(open(outp, 'rb')); print(f"the Hunga layer: {X['kw']}; photons for the higher orders: {X['N']} a case"); out = table(X['R'])
    OBS = {3: -0.034, 4: -0.157, 5: -0.214, 6: -0.302, 7: -0.454, 8: -0.654, 9: -0.801, 10: -0.824, 11: -0.834}
    print('\nthe central model (plume 0.018) beside the meters (the ninth sheet, the middle of the southern places)')
    for d in DEPTHS: print(f'  {d:2d}°   model {out[d][1]:+.2f}   meters {OBS[d]:+.2f}   difference {out[d][1] - OBS[d]:+.2f}')
    c = {d: out[d][1] for d in DEPTHS}
    print('\nThe lines of the model sheet')
    print(f"Z1. the model at 10 degrees between -0.40 and -1.60: {c[10]:+.3f}: {'held' if -1.60 <= c[10] <= -0.40 else 'failed'}")
    print(f"Z2. the model at 3 degrees within 0.10 of nothing: {c[3]:+.3f}: {'held' if abs(c[3]) <= 0.10 else 'failed'}")
    print(f"Z3. the model brighter at each step from 4 to 9 degrees: {', '.join(f'{c[d]:+.2f}' for d in (4, 5, 6, 7, 8, 9))}: {'held' if all(c[d + 1] < c[d] for d in (4, 5, 6, 7, 8)) else 'failed'}")
    print(f"Z4. the model at 6 degrees between -0.15 and -0.60: {c[6]:+.3f}: {'held' if -0.60 <= c[6] <= -0.15 else 'failed'}")
    print(f"Z5. the model's step from 10 to 11 degrees smaller in size than 0.10: {c[11] - c[10]:+.3f}: {'held' if abs(c[11] - c[10]) < 0.10 else 'failed'}")
    n = sum(1 for d in (4, 5, 6, 7, 8, 9, 10) if abs(c[d] - OBS[d]) <= 0.15)
    print(f"Z6. the model within 0.15 magnitude of the meters at five or more of the seven depths from 4 to 10 degrees: {n} of 7: {'held' if n >= 5 else 'failed'}")
