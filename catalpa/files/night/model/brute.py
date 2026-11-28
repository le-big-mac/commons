# A check of the haze result by the plainest means: two separate Monte Carlo runs, with and without the Hunga layer,
# all orders by random paths (no direct sums, no paired weights), at a few wavelengths and depths.
import sys, pickle, importlib.util, time
import numpy as np
from multiprocessing import Pool
spec = importlib.util.spec_from_file_location('run_haze', '/home/agent1/night/model/run_haze.py'); RH = importlib.util.module_from_spec(spec); spec.loader.exec_module(RH)
M = RH.M
def job(a):
    lam, dep, which, seed = a; A = RH.atms(lam, 21.0, 5.0); at = A[1] if which == 'plume' else A[3]
    L, L2 = M.multiple(at, float(dep), N=20000, seed=seed); return (lam, dep, which), L[1:].sum() / 20000
if __name__ == '__main__':
    cases = [(425, 5), (675, 4), (675, 6), (725, 7), (575, 6)]; nb = 60
    jobs = [(l, d, w, 31000 + 1000 * i + b) for i, (l, d) in enumerate(cases) for w in ('plume', 'none') for b in range(nb)]
    t0 = time.time()
    with Pool(15) as p: res = p.map(job, jobs, chunksize=2)
    X = pickle.load(open('/home/agent1/night/model/haze_central.pkl', 'rb'))['R']
    print(f'{nb * 20000} photons a run, {time.time() - t0:.0f} s')
    for l, d in cases:
        a = np.array([v for k, v in res if k == (l, d, 'plume')]); b = np.array([v for k, v in res if k == (l, d, 'none')])
        dm = -2.5 * np.log10(a.mean() / b.mean()); err = 2.5 / np.log(10) * np.sqrt((a.std() / np.sqrt(nb) / a.mean()) ** 2 + (b.std() / np.sqrt(nb) / b.mean()) ** 2)
        r = X[(l, d)]; t1 = r['L1'][1] + r['L2'][1] + r['L3'][:, 1].mean(); t0_ = r['L1'][3] + r['L2'][3] + r['L3'][:, 3].mean()
        print(f'   {l} nm, {d} degrees: two separate runs {dm:+.3f} +- {err:.3f} magnitude; the sealed run {-2.5 * np.log10(t1 / t0_):+.3f}; no plume, all light: separate {b.mean():.4e}, sealed run {t0_:.4e}')
