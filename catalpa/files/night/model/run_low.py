# A run made after the fact (model/after_low.md says why and what I guessed): a low layer at 14 km, not absorbing
# and absorbing. The sealed programs (twimc.py, run_haze.py) are used unchanged; the absorbing cases are made by
# scaling the layer's scattering by a single-scattering albedo after the atmosphere is built, leaving its extinction.
#   usage: run_low.py OUT.pkl NPHOTONS
import sys, pickle, time, importlib.util
import numpy as np
from multiprocessing import Pool
spec = importlib.util.spec_from_file_location('run_haze', '/home/agent1/night/model/run_haze.py'); RH = importlib.util.module_from_spec(spec); spec.loader.exec_module(RH)
M = RH.M; BG = dict(RH.BG, tau=0.005); PL = dict(rm=0.22, sigma=1.4); Z0, FWHM = 14.0, 4.0
CASES = ((0.008, 1.0), (0.008, 0.8), (0.016, 0.8))
def atms(lam, z0, fwhm):
    out = []
    for tau, ssa in CASES:
        at = M.atmosphere(float(lam), layers=[BG, dict(PL, tau=tau, z0=z0, fwhm=fwhm)], **RH.CLEAR)
        at['comps'][-1]['sca'] = at['comps'][-1]['sca'] * ssa; at['sca'] = sum(c['sca'] for c in at['comps']); out.append(at)
    out.append(M.atmosphere(float(lam), layers=[BG], **RH.CLEAR)); return out
RH.atms = atms
def job(a): return RH.job(a)
if __name__ == '__main__':
    outp = sys.argv[1]; N = int(sys.argv[2]); t0 = time.time(); jobs = [(l, d, Z0, FWHM, N, 31) for l in RH.LAMS for d in RH.DEPTHS]
    with Pool(15) as p: R = dict(p.map(job, jobs, chunksize=1))
    pickle.dump(dict(R=R, kw=dict(z0=Z0, fwhm=FWHM, PLUME=PL, BG=BG, CASES=CASES, CLEAR=RH.CLEAR), N=N), open(outp, 'wb'))
    RESP = {425: 0.575, 475: 0.670, 525: 0.768, 575: 0.847, 625: 0.924, 675: 0.985, 725: 0.768}
    def tot(d, i): return sum(RH.RC.SUN[l] * RESP[l] * (R[(l, d)]['L1'][i] + R[(l, d)]['L2'][i] + R[(l, d)]['L3'][:, i].mean()) for l in RH.LAMS)
    print(f'a layer at {Z0:g} km, {FWHM:g} km wide, droplets {PL}, the comparison haze {BG["tau"]}; {N} paths a case; {time.time() - t0:.0f} s')
    print('the change of the reading itself, magnitudes (positive: darker), by the depth of the Sun, with the first make\'s response')
    print('   amount at 550 nm, single-scattering albedo   ' + ''.join(f'{d:7g}°' for d in RH.DEPTHS))
    for i, (tau, ssa) in enumerate(CASES): print(f'   {tau:<8g} {ssa:<36g}' + ''.join(f'{-2.5 * np.log10(tot(d, i) / tot(d, 3)):+8.2f}' for d in RH.DEPTHS))
