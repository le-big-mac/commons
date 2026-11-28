# The deep end again, where the checker doubts the Monte Carlo: the atmosphere of the comparison years (no plume) run
# by itself (paths drawn in that atmosphere, no weights from another), three times and more, at 8 to 11 degrees; set
# beside what the sealed run gave for the same atmosphere by weights on paths drawn in the haziest one.
import pickle, importlib.util, time
import numpy as np
from multiprocessing import Pool
spec = importlib.util.spec_from_file_location('run_haze', '/home/agent1/night/model/run_haze.py'); RH = importlib.util.module_from_spec(spec); spec.loader.exec_module(RH)
M = RH.M
def job(a):
    lam, dep, i, nb, seed = a; at = RH.atms(lam, 21.0, 5.0)[i]; v3 = []; v2 = []
    for b in range(nb):
        L, _ = M.multiple(at, float(dep), N=20000, seed=seed + b); v3.append(L[3:].sum() / 20000); v2.append(L[2] / 20000)
    return (lam, dep, i), (np.array(v3), np.array(v2))
if __name__ == '__main__':
    X = pickle.load(open('/home/agent1/night/model/haze_central.pkl', 'rb'))['R']; nb = 100; t0 = time.time()
    jobs = [(l, d, i, nb, 770000 + 1000 * j) for j, (l, d, i) in enumerate((l, d, i) for l in RH.LAMS for d in (8, 9, 10, 11) for i in (3, 1))]
    with Pool(15) as p: res = dict(p.map(job, jobs, chunksize=1))
    print(f'{nb * 20000} photons a case, {time.time() - t0:.0f} s. Band sums (the sealed weights).')
    w = {l: RH.RC.SUN[l] * RH.RC.RESP[l] for l in RH.LAMS}
    for d in (8, 9, 10, 11):
        for i, nm in ((3, 'no plume'), (1, 'plume 0.018')):
            own3 = sum(w[l] * res[(l, d, i)][0].mean() for l in RH.LAMS); er3 = np.sqrt(sum((w[l] * res[(l, d, i)][0].std() / np.sqrt(nb)) ** 2 for l in RH.LAMS))
            own2 = sum(w[l] * res[(l, d, i)][1].mean() for l in RH.LAMS); ex2 = RH.band(X, d, i, 'L2'); s3 = RH.band(X, d, i, 'L3')
            print(f'  {d:2d} degrees, {nm:<11}: three times and more, run by itself {own3:.3e} +- {er3:.1e}; in the sealed run {s3:.3e} (ratio {s3 / own3:.2f}); twice-scattered, run by itself {own2:.3e} against the direct sums {ex2:.3e} (ratio {own2 / ex2:.2f})')
        o = {i: sum(w[l] * (X[(l, d)]['L1'][i] + X[(l, d)]['L2'][i] + res[(l, d, i)][0].mean()) for l in RH.LAMS) for i in (1, 3)}
        print(f'      the brightening with the higher orders of these separate runs: {-2.5 * np.log10(o[1] / o[3]):+.3f}; in the sealed run: {-2.5 * np.log10(sum(RH.band(X, d, 1, p) for p in ("L1", "L2", "L3")) / sum(RH.band(X, d, 3, p) for p in ("L1", "L2", "L3"))):+.3f}')
