# The ordinary twilight (no added haze) in the model, over the band of the meters, to set beside the ordinary twilight
# curve that the meters give (depth.out). Seven wavelengths, depths 3 to 11 degrees.
import sys, pickle, time, importlib.util
import numpy as np
from multiprocessing import Pool
spec = importlib.util.spec_from_file_location('twimc', '/home/agent1/night/model/twimc.py'); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
LAMS = [425, 475, 525, 575, 625, 675, 725]
SUN = {425: 1.70, 475: 2.00, 525: 1.90, 575: 1.84, 625: 1.67, 675: 1.52, 725: 1.36}      # sunlight outside the air, W/m2/nm, rounded
RESP = {425: 0.32, 475: 0.50, 525: 0.65, 575: 0.78, 625: 0.89, 675: 0.97, 725: 1.00}      # the sensor's response, relative (approximate)
DEPTHS = [3, 4, 5, 6, 7, 8, 9, 10, 11]
def job(a):
    lam, dep, kw, N, seed = a; atm = M.atmosphere(float(lam), **kw)
    L1, zs, c = M.single(atm, float(dep)); tot = np.zeros(41); tot2 = np.zeros(41); nb = max(1, N // 20000); sums = []
    for b in range(nb):
        L, L2 = M.multiple(atm, float(dep), N=20000, seed=seed * 1000 + b); tot += L; sums.append(L[2:].sum() / 20000)
    ms = float(np.mean(sums)); err = float(np.std(sums) / np.sqrt(len(sums))) if len(sums) > 1 else float('nan')
    return (lam, dep), dict(L1=L1, ms=ms, err=err, orders=tot / (nb * 20000))
def band(R, dep, lams=LAMS):
    w = np.array([SUN[l] * RESP[l] for l in lams]); l1 = np.array([R[(l, dep)]['L1'] for l in lams]); ms = np.array([R[(l, dep)]['ms'] for l in lams]); er = np.array([R[(l, dep)]['err'] for l in lams])
    return float((w * l1).sum()), float((w * ms).sum()), float(np.sqrt(((w * er) ** 2).sum()))
if __name__ == '__main__':
    out = sys.argv[1]; N = int(sys.argv[2]); kw = eval(sys.argv[3]) if len(sys.argv) > 3 else {}
    t0 = time.time(); jobs = [(l, d, kw, N, 7) for l in LAMS for d in DEPTHS]
    with Pool(14) as p: R = dict(p.map(job, jobs, chunksize=1))
    pickle.dump(dict(R=R, kw=kw, N=N), open(out, 'wb'))
    print(f'{len(jobs)} cases, {N} photons each, {time.time() - t0:.0f} s; settings {kw}')
    OBS = {3: 9.28, 4: 10.40, 5: 11.72, 6: 13.08, 7: 14.39, 8: 15.62, 9: 16.58, 10: 17.54, 11: 18.46}
    print('depth   once      more than once (+- error)   share more than once   magnitudes below 3 degrees: model, meters   the step from the depth before: model, meters')
    prev = None; base = None
    for d in DEPTHS:
        l1, ms, er = band(R, d); tot = l1 + ms; mag = -2.5 * np.log10(tot); base = mag if base is None else base
        print(f'  {d:2d}°   {l1:.3e}   {ms:.3e} +- {er:.1e}      {ms / tot:.2f}          {mag - base:6.2f}  {OBS[d] - OBS[3]:6.2f}' + (f'        {mag - prev:5.2f}  {OBS[d] - OBS[d - 1]:5.2f}' if prev is not None else ''))
        prev = mag
    print('share scattered more than once, by wavelength (rows) and depth (columns ' + ' '.join(str(d) for d in DEPTHS) + ')')
    for l in LAMS: print(f'  {l} nm  ' + ' '.join(f"{R[(l, d)]['ms'] / (R[(l, d)]['L1'] + R[(l, d)]['ms']):.2f}" for d in DEPTHS))
