# What the model says for the other make of sky meter (the SQM), in every run made: the stored results summed over the
# colours with that meter's response as its makers' figure prints it (the checker's blind reading, check/fig3_blind.txt),
# beside the same for the TESS-W. June to August 2022 against the comparison years; magnitudes, negative: brighter.
import os, pickle, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('run_haze', '/home/agent1/night/model/run_haze.py'); RH = importlib.util.module_from_spec(spec); spec.loader.exec_module(RH)
SQM = {425: 0.472, 475: 0.597, 525: 0.673, 575: 0.479, 625: 0.120, 675: 0.009, 725: 0.006}
TESS = {425: 0.575, 475: 0.670, 525: 0.768, 575: 0.847, 625: 0.924, 675: 0.985, 725: 0.768}
def tot(R, d, i, resp): return sum(RH.RC.SUN[l] * resp[l] * (R[(l, d)]['L1'][i] + R[(l, d)]['L2'][i] + R[(l, d)]['L3'][:, i].mean()) for l in RH.LAMS)
B = '/home/agent1/night/model/'
CASES = [('haze_central.pkl', 1, 'the sealed inputs'), ('haze_central.pkl', 2, 'plume 0.014'), ('haze_central.pkl', 0, 'plume 0.022'), ('haze_tau.pkl', 1, 'plume 0.010'), ('haze_tau.pkl', 0, 'plume 0.028'),
         ('haze_z195.pkl', 1, 'the layer at 19.5 km'), ('haze_z225.pkl', 1, 'the layer at 22.5 km'), ('haze_r030.pkl', 1, 'droplets 0.30'), ('haze_r040.pkl', 1, 'droplets 0.40'),
         ('haze_bg17.pkl', 1, 'earlier haze at 17 km'), ('haze_bg21.pkl', 1, 'earlier haze at 21 km')]
D = [3, 4, 5, 6, 7, 8, 9]; rows = {}
print(f"{'the SQM, by the model':<26}" + ''.join(f'{d:6d}°' for d in D) + '   |  the TESS-W, the same run' + ''.join(f'{d:6d}°' for d in D))
for fn, i, name in CASES:
    R = pickle.load(open(B + fn, 'rb'))['R']; s = [-2.5 * np.log10(tot(R, d, i, SQM) / tot(R, d, 3, SQM)) for d in D]; t = [-2.5 * np.log10(tot(R, d, i, TESS) / tot(R, d, 3, TESS)) for d in D]; rows[name] = (s, t)
    print(f'{name:<26}' + ''.join(f'{v:+7.2f}' for v in s) + '   |                           ' + ''.join(f'{v:+7.2f}' for v in t))
S = np.array([r[0] for r in rows.values()]); T = np.array([r[1] for r in rows.values()])
print(f"{'over the eleven runs: from':<26}" + ''.join(f'{v:+7.2f}' for v in S.max(axis=0))); print(f"{'                        to':<26}" + ''.join(f'{v:+7.2f}' for v in S.min(axis=0)))
print('the SQM\'s change as a share of the TESS-W\'s in the same run, at 6, 7, 8 and 9 degrees: ' + ', '.join(f'{d}°: {np.min(S[:, D.index(d)] / T[:, D.index(d)]):+.2f} to {np.max(S[:, D.index(d)] / T[:, D.index(d)]):+.2f}' for d in (6, 7, 8, 9)))
print('by wavelength, the sealed inputs (magnitudes): ' + '; '.join(f"{l} nm: " + ' '.join(f"{-2.5 * np.log10((lambda r: (r['L1'][1] + r['L2'][1] + r['L3'][:, 1].mean()) / (r['L1'][3] + r['L2'][3] + r['L3'][:, 3].mean()))(pickle.load(open(B + 'haze_central.pkl', 'rb'))['R'][(l, d)])):+.2f}" for d in (4, 6, 8)) for l in (425, 525, 625)))
