# Runs of the same model with one input changed at a time, made after the sealed run to see what matters. Each is the
# sealed program (run_haze.py) with one of its fixed inputs replaced before the run:
#   usage: run_haze2.py OUT.pkl NPHOTONS "dict(plume=dict(rm=0.30, sigma=1.23))"      the droplets' size
#          run_haze2.py OUT.pkl NPHOTONS "dict(bg=dict(z0=17.0))"                     the comparison years' layer
#          run_haze2.py OUT.pkl NPHOTONS "dict(taus=(0.028, 0.010, 0.005))"           the amount
#          run_haze2.py OUT.pkl NPHOTONS "dict(z0=21.0, fwhm=5.0, clear=dict(o3_du=260.0))"
import sys, pickle, time, importlib.util
import numpy as np
from multiprocessing import Pool
spec = importlib.util.spec_from_file_location('run_haze', '/home/agent1/night/model/run_haze.py'); RH = importlib.util.module_from_spec(spec); spec.loader.exec_module(RH)
def job(a): return RH.job(a)      # the pool can hand on a function of this file; the workers are forks and keep the changed inputs
if __name__ == '__main__':
    outp = sys.argv[1]; N = int(sys.argv[2]); kw = eval(sys.argv[3]); z0 = kw.get('z0', 21.0); fwhm = kw.get('fwhm', 5.0)
    if 'plume' in kw: RH.PLUME = dict(RH.PLUME, **kw['plume'])
    if 'bg' in kw: RH.BG = dict(RH.BG, **kw['bg'])
    if 'taus' in kw: RH.TAUS = tuple(kw['taus'])
    if 'clear' in kw: RH.CLEAR = dict(RH.CLEAR, **kw['clear'])
    t0 = time.time(); jobs = [(l, d, z0, fwhm, N, 23) for l in RH.LAMS for d in RH.DEPTHS]
    with Pool(15) as p: R = dict(p.map(job, jobs, chunksize=1))
    pickle.dump(dict(R=R, kw=dict(kw, z0=z0, fwhm=fwhm, PLUME=RH.PLUME, BG=RH.BG, TAUS=RH.TAUS, CLEAR=RH.CLEAR), N=N), open(outp, 'wb'))
    print(f'{len(jobs)} cases, {N} photons each, {time.time() - t0:.0f} s; changed: {kw}; plume {RH.PLUME}; comparison years {RH.BG}; amounts {RH.TAUS}')
